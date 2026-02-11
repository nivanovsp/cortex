"""Shared fixtures for Cortex tests."""

import os
import json
import pytest
import numpy as np


@pytest.fixture
def sample_frontmatter_content():
    """Sample markdown content with frontmatter."""
    return '''---
id: CHK-AUTH-001-001
source_doc: DOC-AUTH-001
source_section: "Authentication"
source_lines: [1, 50]
tokens: 120
keywords: ["auth", "login", "session"]
created: "2026-01-15T10:30:00"
last_retrieved: null
retrieval_count: 0
---

This is the chunk content about authentication.
'''


@pytest.fixture
def sample_markdown_document():
    """Sample markdown document for chunking tests."""
    return '''# Introduction

This is the introduction section with enough content to be meaningful.
It discusses the overall architecture of the system and how components interact.
The system uses a microservices pattern with REST APIs for communication.

# Authentication

The authentication module handles user login and session management.
It uses JWT tokens for stateless authentication across services.
Password hashing uses bcrypt with a cost factor of 12.

Sessions expire after 24 hours of inactivity.
Refresh tokens are stored in HTTP-only cookies for security.

# API Design

The API follows REST conventions with JSON request and response bodies.
All endpoints require authentication except the login and registration routes.
Rate limiting is applied at 100 requests per minute per user.
'''


@pytest.fixture
def project_root(tmp_path):
    """Create a temporary project root with .cortex directory structure."""
    cortex_dir = tmp_path / ".cortex"
    chunks_dir = cortex_dir / "chunks"
    memories_dir = cortex_dir / "memories"
    index_dir = cortex_dir / "index"

    chunks_dir.mkdir(parents=True)
    memories_dir.mkdir(parents=True)
    index_dir.mkdir(parents=True)

    return str(tmp_path)


@pytest.fixture
def sample_embedding():
    """A normalized 384-dimensional embedding vector."""
    rng = np.random.default_rng(42)
    vec = rng.standard_normal(384).astype(np.float32)
    vec = vec / np.linalg.norm(vec)
    return vec
