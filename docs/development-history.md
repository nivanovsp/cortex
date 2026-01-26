# Cortex Development History

This document chronicles the development of Cortex from specification to implementation.

## Project Genesis

**Date:** 2026-01-26
**Objective:** Build an LLM-native context management system that optimizes for how LLMs actually process information.

### The Problem

Traditional documentation systems are built around human cognitive metaphors:
- Hierarchical navigation (like filing cabinets)
- Manual cross-references (like footnotes)
- Load entire documents (like reading a book)

But LLMs process information differently:
- Attention-based (not sequential)
- Semantic similarity (not predefined links)
- Context windows (not unlimited memory)

### The Solution

Cortex - a system designed for LLM consumption:
- Chunk documents into retrievable semantic units
- Embed and index for similarity search
- Assemble position-optimized context frames
- Capture and reuse learnings across sessions

---

## Development Timeline

### Phase 1: Foundation
**Duration:** Session 1
**Objective:** Core chunking, embedding, indexing, and retrieval

#### Deliverables
1. **core/config.py** - Environment configuration with sensible defaults
2. **core/embedder.py** - e5-small-v2 wrapper with lazy loading
3. **core/chunker.py** - Semantic markdown chunking
4. **core/indexer.py** - NumPy vector index management
5. **core/retriever.py** - Multi-factor similarity search

#### Scripts
- `cortex-init.ps1` - Project initialization
- `cortex-chunk.ps1` - Document chunking
- `cortex-index.ps1` - Index building
- `cortex-retrieve.ps1` - Retrieval testing

#### Verification
- Chunked cortex-spec.md into 24 semantic units
- Built index (24 vectors, 384 dimensions)
- Retrieval working with relevance scoring

---

### Phase 2: Memory System
**Duration:** Session 1 (continued)
**Objective:** Persistent learning storage and retrieval

#### Deliverables
1. **core/memory.py** - Full CRUD operations for memories
2. **Memory schema** - Type, domain, confidence, keywords, content
3. **Relationship discovery** - Find related memories via similarity

#### Scripts
- `cortex-memory.ps1` - Full memory management CLI

#### Verification
- Created test memories across domains (UI, AUTH, DEV)
- Built memory index (3 vectors)
- Query and relationship discovery working

#### Bug Fix
- Fixed memory ID generation race condition (rsplit instead of split)

---

### Phase 3: Context Assembly
**Duration:** Session 1 (continued)
**Objective:** Position-optimized context frame generation

#### Deliverables
1. **core/assembler.py** - Context frame builder
2. **Token budget management** - Configurable allocation
3. **Position optimization** - Critical info at edges

#### Scripts
- `cortex-assemble.ps1` - Context frame generation

#### Verification
- Generated context frames for test tasks
- Budget respected (1,793 of 15,000 tokens used)
- Position structure correct (task at top, instructions at bottom)

---

### Phase 4: Integration
**Duration:** Session 1 (continued)
**Objective:** Claude Code integration and session memory extraction

#### Deliverables
1. **core/extractor.py** - Learning detection from text
2. **Pattern detection** - Fixes, discoveries, procedures, facts
3. **Confidence assignment** - High/medium/low based on patterns

#### Scripts
- `cortex-extract.ps1` - Session-end extraction
- `cortex-status.ps1` - Quick statistics

#### Verification
- Extracted 6 learnings from sample text
- Correct confidence assignment
- Status reporting accurate
- Context consumption: 0.63% (under 5% target)

---

### Documentation Phase
**Duration:** Session 1 (final)
**Objective:** Complete project documentation

#### Deliverables
1. **CLAUDE.md** - Claude Code integration guide
2. **CHANGELOG.md** - Release notes
3. **docs/architecture.md** - Technical architecture
4. **docs/user-guide.md** - Comprehensive usage guide
5. **docs/decisions.md** - Architecture Decision Records
6. **docs/development-history.md** - This document

---

## Technical Decisions Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Embedding model | e5-small-v2 | Free, local, retrieval-optimized |
| Vector index | NumPy brute-force | Simple, fast at <500 vectors |
| Storage format | Markdown + YAML | LLM-friendly (2-5% overhead) |
| CLI | PowerShell + Python | Native Windows + ML ecosystem |
| Chunk size | 500 tokens | Matches model max |
| Position strategy | Edges = critical | "Lost in middle" research |

---

## Metrics Achieved

| Metric | Target | Actual |
|--------|--------|--------|
| Context consumption | <8% | ~0.6% |
| Mode activation | <5% | 0.63% |
| Retrieval speed | Fast | <1ms |
| Embedding speed | Acceptable | ~50ms |

---

## Files Created

### Core Modules (Python)
```
core/
├── __init__.py      # Package with lazy imports
├── config.py        # Configuration
├── embedder.py      # e5-small-v2 wrapper
├── chunker.py       # Document chunking
├── indexer.py       # Vector index
├── retriever.py     # Similarity search
├── memory.py        # Memory CRUD
├── assembler.py     # Context assembly
└── extractor.py     # Learning extraction
```

### Scripts (PowerShell)
```
scripts/
├── cortex-init.ps1      # Initialize project
├── cortex-chunk.ps1     # Chunk documents
├── cortex-index.ps1     # Build indices
├── cortex-retrieve.ps1  # Test retrieval
├── cortex-assemble.ps1  # Build context
├── cortex-memory.ps1    # Manage memories
├── cortex-extract.ps1   # Extract learnings
└── cortex-status.ps1    # Show statistics
```

### Documentation
```
├── README.md                    # Project overview
├── CLAUDE.md                    # Claude Code guide
├── CHANGELOG.md                 # Release notes
└── docs/
    ├── cortex-spec.md           # Full specification
    ├── architecture.md          # Technical architecture
    ├── user-guide.md            # Usage guide
    ├── decisions.md             # ADRs
    └── development-history.md   # This file
```

---

## Lessons Learned

1. **PowerShell here-strings** - Can have quoting issues; use temp files for complex Python code
2. **Unicode on Windows** - Console encoding issues; write to files instead of stdout
3. **Memory ID parsing** - Use `rsplit` from right to handle dates with hyphens
4. **e5 model prefixes** - Queries need "query:" prefix, passages need "passage:"

---

## Future Enhancements

Potential improvements not in current scope:

1. **Incremental indexing** - Add without full rebuild
2. **Memory decay** - Archive unused memories
3. **Chunk versioning** - Track document changes
4. **Watch mode** - Auto-chunk on file changes
5. **Export/import** - Share between projects
6. **Web UI** - Browser-based management

---

*Cortex v1.0.0 - Development completed 2026-01-26*
