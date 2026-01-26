# Changelog

All notable changes to Cortex will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-26

### Added

#### Phase 1: Foundation
- **Document Chunking** - Semantic-aware markdown chunking with ~500 token chunks
- **Embedding Pipeline** - Local e5-small-v2 model (384 dimensions, free)
- **Vector Indexing** - NumPy + pickle brute-force index
- **Semantic Retrieval** - Cosine similarity with multi-factor scoring
- Scripts: `cortex-init`, `cortex-chunk`, `cortex-index`, `cortex-retrieve`

#### Phase 2: Memory System
- **Memory CRUD** - Create, read, update, delete memories
- **Memory Types** - Factual, experiential, procedural
- **Confidence Levels** - High, medium, low with verification tracking
- **Relationship Discovery** - Find related memories via embedding similarity
- Script: `cortex-memory` with actions: add, list, query, update, delete, related

#### Phase 3: Context Assembly
- **Context Frame Builder** - Position-optimized context for LLM consumption
- **Token Budget Management** - Configurable budget with section allocation
- **Position Optimization** - Critical info at edges (primacy/recency zones)
- Script: `cortex-assemble` with task, criteria, state, budget options

#### Phase 4: Integration
- **Memory Extraction** - Detect learnings from session text
- **Pattern Detection** - Fixes, discoveries, procedures, facts
- **Auto-Save** - High-confidence memories can be auto-saved
- **Status Reporting** - Quick stats on chunks, memories, indices
- Scripts: `cortex-extract`, `cortex-status`

### Technical Specifications

| Component | Choice |
|-----------|--------|
| Embedding Model | intfloat/e5-small-v2 |
| Vector Dimensions | 384 |
| Chunk Size | 500 tokens max |
| Chunk Overlap | 50 tokens |
| Index Type | NumPy brute-force |
| Storage Format | Markdown + YAML frontmatter |

### Performance

| Metric | Value |
|--------|-------|
| Context Consumption | ~0.6% (vs 35-60% traditional) |
| Retrieval Speed | <1ms for 500 vectors |
| Embedding Speed | ~50ms per chunk |

---

## [Unreleased]

### Planned
- Incremental indexing (add without full rebuild)
- Memory decay/archival for unused memories
- Chunk versioning for document changes
- Watch mode for auto-chunking
- Export/import for sharing between projects
