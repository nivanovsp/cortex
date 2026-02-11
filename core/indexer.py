"""
Cortex Indexer

Build and manage vector indices for chunks and memories.
"""

import os
import json
from pathlib import Path
from typing import Optional
import numpy as np

from .config import Config
from .utils import parse_frontmatter


def scan_chunks(chunks_path: str) -> list[dict]:
    """
    Scan all chunks in the chunks directory.

    Returns list of {id, embedding_path, metadata}
    """
    chunks = []

    for domain_dir in os.listdir(chunks_path):
        domain_path = os.path.join(chunks_path, domain_dir)
        if not os.path.isdir(domain_path):
            continue

        for f in os.listdir(domain_path):
            if not f.endswith('.md'):
                continue

            chunk_id = f.replace('.md', '')
            md_path = os.path.join(domain_path, f)
            npy_path = os.path.join(domain_path, f"{chunk_id}.npy")

            # Skip if no embedding file
            if not os.path.exists(npy_path):
                print(f"Warning: No embedding for {chunk_id}")
                continue

            # Read metadata from markdown frontmatter
            with open(md_path, 'r', encoding='utf-8') as mf:
                content = mf.read()
                metadata = parse_frontmatter(content)

            chunks.append({
                'id': chunk_id,
                'embedding_path': npy_path,
                'metadata': metadata
            })

    return chunks


def scan_memories(memories_path: str) -> list[dict]:
    """
    Scan all memories in the memories directory.

    Memories are stored flat (not nested by domain like chunks).

    Returns list of {id, embedding_path, metadata}
    """
    memories = []

    if not os.path.exists(memories_path):
        return memories

    for f in os.listdir(memories_path):
        if not f.endswith('.md'):
            continue

        memory_id = f.replace('.md', '')
        md_path = os.path.join(memories_path, f)
        npy_path = os.path.join(memories_path, f"{memory_id}.npy")

        # Skip if no embedding file
        if not os.path.exists(npy_path):
            print(f"Warning: No embedding for {memory_id}")
            continue

        # Read metadata from markdown frontmatter
        with open(md_path, 'r', encoding='utf-8') as mf:
            content = mf.read()
            metadata = parse_frontmatter(content)

        memories.append({
            'id': memory_id,
            'embedding_path': npy_path,
            'metadata': metadata
        })

    return memories


def build_index(
    project_root: str = ".",
    index_type: str = "chunks",
    full_rebuild: bool = False
) -> tuple[int, str]:
    """
    Build or rebuild the vector index.

    Args:
        project_root: Project root directory
        index_type: Type of index to build ("chunks" or "memories")
        full_rebuild: If True, re-embed everything (currently same as normal)

    Returns:
        Tuple of (count, index_path)
    """
    project_root = os.path.abspath(project_root)
    cortex_path = Config.get_cortex_path(project_root)

    if index_type == "chunks":
        source_path = os.path.join(cortex_path, Config.CHUNKS_DIR)
    else:
        source_path = os.path.join(cortex_path, Config.MEMORIES_DIR)

    if not os.path.exists(source_path):
        print(f"No {index_type} directory found at {source_path}")
        return 0, ""

    # Scan for items
    if index_type == "chunks":
        items = scan_chunks(source_path)
    else:
        items = scan_memories(source_path)

    if not items:
        print(f"No {index_type} found to index")
        return 0, ""

    # Load all embeddings
    embeddings = []
    metadata = {}

    for item in items:
        emb = np.load(item['embedding_path'])
        embeddings.append(emb)
        metadata[item['id']] = item['metadata']

    # Stack into array
    embeddings_array = np.vstack(embeddings)

    # Save index
    index_path = Config.get_index_path(project_root)
    os.makedirs(index_path, exist_ok=True)

    # Save embeddings as numpy array
    npy_path = os.path.join(index_path, f"{index_type}.npy")
    np.save(npy_path, embeddings_array)

    # Save IDs as JSON
    ids_path = os.path.join(index_path, f"{index_type}.ids.json")
    with open(ids_path, 'w', encoding='utf-8') as f:
        json.dump([item['id'] for item in items], f, indent=2)

    # Save metadata as JSON
    meta_path = os.path.join(index_path, f"{index_type}.meta.json")
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)

    print(f"Built {index_type} index:")
    print(f"  Items: {len(items)}")
    print(f"  Shape: {embeddings_array.shape}")
    print(f"  Index: {npy_path}")
    print(f"  Meta:  {meta_path}")

    return len(items), npy_path


def load_index(
    project_root: str = ".",
    index_type: str = "chunks"
) -> tuple[np.ndarray, list[str], dict]:
    """
    Load an index from disk.

    Args:
        project_root: Project root directory
        index_type: Type of index to load ("chunks" or "memories")

    Returns:
        Tuple of (embeddings_array, id_list, metadata_dict)
    """
    project_root = os.path.abspath(project_root)
    index_path = Config.get_index_path(project_root)

    npy_path = os.path.join(index_path, f"{index_type}.npy")
    ids_path = os.path.join(index_path, f"{index_type}.ids.json")
    meta_path = os.path.join(index_path, f"{index_type}.meta.json")

    if not os.path.exists(npy_path):
        raise FileNotFoundError(f"Index not found: {npy_path}")

    # Load embeddings
    embeddings = np.load(npy_path)

    # Load IDs
    ids = []
    if os.path.exists(ids_path):
        with open(ids_path, 'r', encoding='utf-8') as f:
            ids = json.load(f)

    # Load metadata
    metadata = {}
    if os.path.exists(meta_path):
        with open(meta_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

    return embeddings, ids, metadata


def get_index_stats(project_root: str = ".") -> dict:
    """Get statistics about existing indices."""
    project_root = os.path.abspath(project_root)
    index_path = Config.get_index_path(project_root)

    stats = {}

    for index_type in ["chunks", "memories"]:
        npy_path = os.path.join(index_path, f"{index_type}.npy")
        ids_path = os.path.join(index_path, f"{index_type}.ids.json")
        if os.path.exists(npy_path):
            embeddings = np.load(npy_path)
            ids = []
            if os.path.exists(ids_path):
                with open(ids_path, 'r', encoding='utf-8') as f:
                    ids = json.load(f)
            stats[index_type] = {
                'count': len(ids),
                'shape': embeddings.shape,
                'size_bytes': os.path.getsize(npy_path)
            }

    return stats


# CLI entry point
if __name__ == "__main__":
    import sys

    project = sys.argv[1] if len(sys.argv) > 1 else "."
    full = "--full" in sys.argv

    build_index(project, "chunks", full)
