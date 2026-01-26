"""
Cortex Configuration

Environment variable defaults for Cortex components.
Override by setting environment variables.
"""

import os


class Config:
    """Configuration with environment variable overrides."""

    # Embedding
    EMBEDDING_MODEL = os.getenv("CORTEX_EMBEDDING_MODEL", "intfloat/e5-small-v2")
    EMBEDDING_DIMENSIONS = 384  # Fixed for e5-small-v2

    # Chunking
    CHUNK_SIZE = int(os.getenv("CORTEX_CHUNK_SIZE", "500"))      # Max tokens per chunk
    CHUNK_MIN = int(os.getenv("CORTEX_CHUNK_MIN", "50"))         # Min tokens per chunk
    CHUNK_OVERLAP = int(os.getenv("CORTEX_CHUNK_OVERLAP", "50")) # Overlap tokens

    # Retrieval
    RETRIEVAL_TOP_K = int(os.getenv("CORTEX_RETRIEVAL_TOP_K", "10"))
    MEMORY_TOP_K = int(os.getenv("CORTEX_MEMORY_TOP_K", "5"))

    # Scoring weights
    SCORE_SEMANTIC = 0.6
    SCORE_KEYWORD = 0.2
    SCORE_RECENCY = 0.1
    SCORE_FREQUENCY = 0.1

    # Token budget
    TOKEN_BUDGET = int(os.getenv("CORTEX_TOKEN_BUDGET", "15000"))

    # Paths (relative to project root)
    CORTEX_DIR = ".cortex"
    CHUNKS_DIR = "chunks"
    MEMORIES_DIR = "memories"
    INDEX_DIR = "index"
    CACHE_DIR = "cache"

    @classmethod
    def get_cortex_path(cls, project_root: str) -> str:
        """Get full path to .cortex directory."""
        return os.path.join(project_root, cls.CORTEX_DIR)

    @classmethod
    def get_chunks_path(cls, project_root: str) -> str:
        """Get full path to chunks directory."""
        return os.path.join(project_root, cls.CORTEX_DIR, cls.CHUNKS_DIR)

    @classmethod
    def get_index_path(cls, project_root: str) -> str:
        """Get full path to index directory."""
        return os.path.join(project_root, cls.CORTEX_DIR, cls.INDEX_DIR)
