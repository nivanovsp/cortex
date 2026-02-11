"""
Cortex Retriever

Similarity search and retrieval with multi-factor scoring.
"""

import os
import json
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional
import numpy as np

from .config import Config
from .embedder import embed_query
from .indexer import load_index
from .utils import parse_chunk_id, load_chunk_content


@dataclass
class RetrievalResult:
    """Represents a retrieval result."""
    id: str
    score: float
    semantic_score: float
    keyword_score: float
    recency_score: float
    frequency_score: float
    metadata: dict
    content: Optional[str] = None


def compute_keyword_overlap(query_keywords: list[str], chunk_keywords: list[str]) -> float:
    """
    Compute keyword overlap score between query and chunk.

    Returns value between 0 and 1.
    """
    if not query_keywords or not chunk_keywords:
        return 0.0

    query_set = set(k.lower() for k in query_keywords)
    chunk_set = set(k.lower() for k in chunk_keywords)

    overlap = len(query_set & chunk_set)
    max_possible = min(len(query_set), len(chunk_set))

    if max_possible == 0:
        return 0.0

    return overlap / max_possible


def compute_recency_score(created: Optional[str]) -> float:
    """
    Compute recency score based on creation date.

    More recent = higher score. Returns value between 0 and 1.
    """
    if not created:
        return 0.5  # Default for unknown

    try:
        # Parse ISO format date
        created_dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
        now = datetime.now(created_dt.tzinfo) if created_dt.tzinfo else datetime.now()

        # Calculate days old
        days_old = (now - created_dt).days

        # Decay function: score = 1 / (1 + days/30)
        # 0 days = 1.0, 30 days = 0.5, 90 days = 0.25
        score = 1.0 / (1.0 + days_old / 30.0)
        return max(0.0, min(1.0, score))
    except (ValueError, TypeError):
        return 0.5


def compute_frequency_score(retrieval_count: int) -> float:
    """
    Compute frequency score based on retrieval count.

    Higher retrieval count = higher score (frequently useful).
    Returns value between 0 and 1.
    """
    # Logarithmic scaling: score = log(1 + count) / log(1 + max_expected)
    # Assuming max expected count is around 100
    max_expected = 100
    score = np.log1p(retrieval_count) / np.log1p(max_expected)
    return max(0.0, min(1.0, score))


def extract_query_keywords(query: str) -> list[str]:
    """Extract keywords from query for keyword matching."""
    import re

    # Simple tokenization
    words = re.findall(r'\b[a-z]{3,}\b', query.lower())

    # Filter common words
    stopwords = {
        'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can',
        'how', 'what', 'when', 'where', 'which', 'this', 'that', 'with'
    }

    return [w for w in words if w not in stopwords]


def retrieve(
    query: str,
    project_root: str = ".",
    top_k: Optional[int] = None,
    index_type: str = "both",
    include_content: bool = False
) -> list[dict]:
    """
    Retrieve relevant chunks/memories for a query.

    Args:
        query: Search query
        project_root: Project root directory
        top_k: Number of results to return (default from config)
        index_type: What to search ("chunks", "memories", or "both")
        include_content: Whether to include full content in results

    Returns:
        List of results sorted by score descending
    """
    project_root = os.path.abspath(project_root)

    if top_k is None:
        top_k = Config.RETRIEVAL_TOP_K

    # Embed query
    query_embedding = embed_query(query)
    query_keywords = extract_query_keywords(query)

    all_results = []

    # Search chunks
    if index_type in ("chunks", "both"):
        try:
            embeddings, ids, metadata = load_index(project_root, "chunks")
            chunk_results = _search_index(
                query_embedding, query_keywords, embeddings, ids, metadata,
                project_root, "chunks", include_content
            )
            all_results.extend(chunk_results)
        except FileNotFoundError:
            pass

    # Search memories
    if index_type in ("memories", "both"):
        try:
            embeddings, ids, metadata = load_index(project_root, "memories")
            mem_results = _search_index(
                query_embedding, query_keywords, embeddings, ids, metadata,
                project_root, "memories", include_content
            )
            all_results.extend(mem_results)
        except FileNotFoundError:
            pass

    # Sort by score and take top_k
    all_results.sort(key=lambda x: x['score'], reverse=True)
    return all_results[:top_k]


def _search_index(
    query_embedding: np.ndarray,
    query_keywords: list[str],
    embeddings: np.ndarray,
    ids: list[str],
    metadata: dict,
    project_root: str,
    index_type: str,
    include_content: bool
) -> list[dict]:
    """Search a single index and return scored results."""
    # Compute cosine similarities (embeddings are normalized)
    similarities = np.dot(embeddings, query_embedding)

    results = []
    for i, (chunk_id, sim) in enumerate(zip(ids, similarities)):
        meta = metadata.get(chunk_id, {})

        # Extract scoring factors
        chunk_keywords = meta.get('keywords', [])
        created = meta.get('created')
        retrieval_count = meta.get('retrieval_count', 0)

        # Compute component scores
        semantic_score = float(sim)
        keyword_score = compute_keyword_overlap(query_keywords, chunk_keywords)
        recency_score = compute_recency_score(created)
        frequency_score = compute_frequency_score(retrieval_count)

        # Compute weighted final score
        final_score = (
            Config.SCORE_SEMANTIC * semantic_score +
            Config.SCORE_KEYWORD * keyword_score +
            Config.SCORE_RECENCY * recency_score +
            Config.SCORE_FREQUENCY * frequency_score
        )

        result = {
            'id': chunk_id,
            'type': index_type,
            'score': round(final_score, 4),
            'semantic_score': round(semantic_score, 4),
            'keyword_score': round(keyword_score, 4),
            'recency_score': round(recency_score, 4),
            'frequency_score': round(frequency_score, 4),
            'metadata': meta
        }

        # Optionally include content
        if include_content:
            result['content'] = _load_content(chunk_id, project_root, index_type)

        results.append(result)

    return results


def _load_content(chunk_id: str, project_root: str, index_type: str) -> Optional[str]:
    """Load content from chunk/memory file."""
    if index_type == "chunks":
        return load_chunk_content(chunk_id, project_root)
    return None


# CLI entry point
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m core.retriever <query> [top_k] [index_type]")
        sys.exit(1)

    query = sys.argv[1]
    top_k = int(sys.argv[2]) if len(sys.argv) > 2 else None
    index_type = sys.argv[3] if len(sys.argv) > 3 else "both"

    results = retrieve(query, ".", top_k, index_type)
    print(json.dumps(results, indent=2))
