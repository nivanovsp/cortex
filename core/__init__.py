"""
Cortex Core - LLM-Native Context Management

Core modules for chunking, embedding, indexing, and retrieval.
"""

__version__ = "2.1.1"

# Lazy imports to avoid circular dependencies
from .config import Config

__all__ = [
    'Config',
    'Embedder',
    'chunk_document',
    'chunk_directory',
    'get_stale_chunks',
    'get_chunks_by_source',
    'delete_chunks',
    'build_index',
    'load_index',
    'retrieve',
    'create_memory',
    'get_memory',
    'list_memories',
    'update_memory',
    'delete_memory',
    'find_related_memories',
    'increment_retrieval',
    'assemble_context',
    'assemble_and_render',
    'extract_memories',
    'extract_and_format',
    'format_proposed_memories',
    'save_proposed_memories',
]


def __getattr__(name):
    """Lazy import for module components."""
    if name == 'Embedder':
        from .embedder import Embedder
        return Embedder
    elif name == 'chunk_document':
        from .chunker import chunk_document
        return chunk_document
    elif name == 'chunk_directory':
        from .chunker import chunk_directory
        return chunk_directory
    elif name == 'get_stale_chunks':
        from .chunker import get_stale_chunks
        return get_stale_chunks
    elif name == 'get_chunks_by_source':
        from .chunker import get_chunks_by_source
        return get_chunks_by_source
    elif name == 'delete_chunks':
        from .chunker import delete_chunks
        return delete_chunks
    elif name == 'build_index':
        from .indexer import build_index
        return build_index
    elif name == 'load_index':
        from .indexer import load_index
        return load_index
    elif name == 'retrieve':
        from .retriever import retrieve
        return retrieve
    elif name == 'create_memory':
        from .memory import create_memory
        return create_memory
    elif name == 'get_memory':
        from .memory import get_memory
        return get_memory
    elif name == 'list_memories':
        from .memory import list_memories
        return list_memories
    elif name == 'update_memory':
        from .memory import update_memory
        return update_memory
    elif name == 'delete_memory':
        from .memory import delete_memory
        return delete_memory
    elif name == 'find_related_memories':
        from .memory import find_related_memories
        return find_related_memories
    elif name == 'increment_retrieval':
        from .memory import increment_retrieval
        return increment_retrieval
    elif name == 'assemble_context':
        from .assembler import assemble_context
        return assemble_context
    elif name == 'assemble_and_render':
        from .assembler import assemble_and_render
        return assemble_and_render
    elif name == 'extract_memories':
        from .extractor import extract_memories
        return extract_memories
    elif name == 'extract_and_format':
        from .extractor import extract_and_format
        return extract_and_format
    elif name == 'format_proposed_memories':
        from .extractor import format_proposed_memories
        return format_proposed_memories
    elif name == 'save_proposed_memories':
        from .extractor import save_proposed_memories
        return save_proposed_memories
    raise AttributeError(f"module 'core' has no attribute '{name}'")
