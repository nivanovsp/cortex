# Changelog

All notable changes to Cortex will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-01-26

### Added

- **Semi-Auto Session Protocol** - Natural language interaction with Cortex
  - Automatic context assembly when task is identified
  - Natural language retrieval triggers ("What do we know about X?")
  - User-triggered learning extraction ("Update learning")
  - Explicit retrieval via "cortex: {query}" pattern

- **Session Protocol Documentation**
  - New `docs/session-protocol-v1.1.0.md` design document
  - Updated `docs/architecture.md` with session flow diagram
  - Updated `docs/cortex-spec.md` Section 8: Session Protocol
  - ADR-010: Semi-Auto Session Protocol decision record

- **Natural Language Triggers**
  - Task detection: "Let's work on...", "Help me with...", etc.
  - Retrieval detection: "What do we know about...", "Tell me about...", etc.
  - Session end detection: "Update learning", "Save learnings", etc.

### Changed

- **Context Budget** - Reduced from ~8% to ~2.8% typical session consumption
- **User Guide** - Rewritten for natural language-first usage
- **README** - Updated with natural language workflow examples
- **CLAUDE.md** (project) - Added session protocol instructions
- **Global CLAUDE.md** - Updated Cortex section with protocol

### Fixed

- Clarified that scripts are internal implementation details
- Users interact through natural language, not script commands

---

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
- Document impact analysis for session-end updates
- Windows encoding fix for cortex-assemble output
