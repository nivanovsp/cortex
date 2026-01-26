"""
Cortex Embedder

Embedding wrapper for e5-small-v2 model with lazy loading.
Handles the e5 prefix requirements for queries vs passages.
"""

import numpy as np
from typing import Union
from .config import Config


class Embedder:
    """
    Embedding wrapper with lazy model loading.

    e5 models require specific prefixes:
    - "query: " for search queries
    - "passage: " for documents/passages
    """

    _instance = None
    _model = None

    def __new__(cls):
        """Singleton pattern for model reuse."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def model(self):
        """Lazy load the embedding model."""
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(Config.EMBEDDING_MODEL)
        return self._model

    def embed_query(self, text: str) -> np.ndarray:
        """
        Embed a search query.

        Args:
            text: Query text

        Returns:
            384-dimensional embedding vector
        """
        # e5 requires "query: " prefix for queries
        prefixed = f"query: {text}"
        embedding = self.model.encode(prefixed, normalize_embeddings=True)
        return np.array(embedding, dtype=np.float32)

    def embed_passage(self, text: str) -> np.ndarray:
        """
        Embed a document passage.

        Args:
            text: Passage text

        Returns:
            384-dimensional embedding vector
        """
        # e5 requires "passage: " prefix for documents
        prefixed = f"passage: {text}"
        embedding = self.model.encode(prefixed, normalize_embeddings=True)
        return np.array(embedding, dtype=np.float32)

    def embed_passages_batch(self, texts: list[str]) -> np.ndarray:
        """
        Embed multiple passages in a batch.

        Args:
            texts: List of passage texts

        Returns:
            Array of shape (n, 384) with embeddings
        """
        # Add prefix to each passage
        prefixed = [f"passage: {text}" for text in texts]
        embeddings = self.model.encode(prefixed, normalize_embeddings=True)
        return np.array(embeddings, dtype=np.float32)

    def similarity(self, query_emb: np.ndarray, passage_embs: np.ndarray) -> np.ndarray:
        """
        Compute cosine similarity between query and passages.

        Since embeddings are normalized, cosine similarity = dot product.

        Args:
            query_emb: Query embedding (384,)
            passage_embs: Passage embeddings (n, 384)

        Returns:
            Similarity scores (n,)
        """
        return np.dot(passage_embs, query_emb)


# Module-level convenience functions
_embedder = None


def get_embedder() -> Embedder:
    """Get or create the singleton embedder instance."""
    global _embedder
    if _embedder is None:
        _embedder = Embedder()
    return _embedder


def embed_query(text: str) -> np.ndarray:
    """Embed a search query."""
    return get_embedder().embed_query(text)


def embed_passage(text: str) -> np.ndarray:
    """Embed a document passage."""
    return get_embedder().embed_passage(text)


def embed_passages_batch(texts: list[str]) -> np.ndarray:
    """Embed multiple passages in a batch."""
    return get_embedder().embed_passages_batch(texts)
