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

---

## v1.1.0 - Semi-Auto Session Protocol

**Date:** 2026-01-26
**Objective:** Natural language interaction without manual script invocation

### Changes

- Added Semi-Auto Session Protocol
- Natural language triggers for task, retrieval, and session end
- Updated all documentation for natural language-first usage
- No code changes - protocol implemented through agent instructions

See `docs/session-protocol-v1.1.0.md` for full design document.

---

## v1.2.0 - Cross-Platform & Provenance

**Date:** 2026-01-27
**Objective:** Cross-platform CLI, chunk provenance tracking, memory retrieval feedback

### Expert Review Process

An independent expert review was conducted, identifying:
- 5 Legitimate Concerns (LC-001 through LC-005)
- 4 Missing Features (MF-001 through MF-004)

Review documents stored in `docs/reviews/`.

### Implementation Decisions

| Item | Decision | Rationale |
|------|----------|-----------|
| LC-002 | **Implemented** | Memory retrieval tracking (3 lines of code) |
| LC-005 | **Implemented** | Python CLI replaces PowerShell |
| MF-002 | **Implemented** | Chunk provenance with source_path, source_hash |
| LC-001 | Deferred | Pattern extraction works well enough |
| LC-003 | Deferred | e5-small-v2 is sufficient |
| MF-001 | Won't Implement | Retrieval handles duplicates naturally |
| MF-003 | Won't Implement | Pattern-based confidence is good enough |
| MF-004 | Won't Implement | User can rephrase queries naturally |

### Deliverables

#### Python CLI (`cli/`)
```
cli/
├── __init__.py
├── __main__.py         # python -m cli entry point
├── main.py             # Typer app
└── commands/
    ├── init.py
    ├── chunk.py        # Added --refresh flag
    ├── index.py
    ├── retrieve.py
    ├── assemble.py
    ├── memory.py
    ├── extract.py
    └── status.py       # Added stale detection
```

#### Core Changes
- `core/chunker.py` - Added source_path, source_hash, stale detection functions
- `core/assembler.py` - Added increment_retrieval() call for memory tracking

#### Documentation
- Updated all docs for v1.2.0
- Added 6 new ADRs (ADR-011 through ADR-016)
- PowerShell deprecation notice in `scripts/README.md`

### Verification

- [x] Python CLI works on Windows
- [x] Chunk provenance tracked in frontmatter
- [x] Stale detection shows modified files
- [x] --refresh flag deletes old chunks, creates new
- [x] Memory retrieval_count increments during assembly

---

*Cortex v1.2.0 - Development completed 2026-01-27*

---

## v1.3.0 - Agent Orchestration Layer

**Date:** 2026-02-01
**Objective:** Bundle agent modes and workflow skills so Cortex ships as a complete package

### Background

Cortex v1.2.0 provided the core context management system — chunking, embedding, retrieval, assembly, and a session protocol. However, the agent orchestration layer (specialist personas like Architect, Analyst, etc.) lived only in the developer's personal `~/.claude/CLAUDE.md`. Anyone who cloned the repo got the tools but not the agent-driven experience.

### Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Spec location | `agents/` directory | Tool-agnostic, anyone can use |
| Claude Code integration | `.claude/commands/` thin wrappers | Slash commands with no duplication |
| Orchestrator model | Planning mode, not runtime coordinator | Claude Code is single-agent |
| Layer architecture | Session protocol (L0) + Agent mode (L1) | Additive, not replacement |

### Deliverables

#### Agent Specs (`agents/`)
```
agents/
├── README.md
├── modes/
│   ├── analyst.md
│   ├── architect.md
│   ├── developer.md
│   ├── ux-designer.md
│   └── orchestrator.md
└── skills/
    ├── qa-gate.md
    └── extract-learnings.md
```

#### Claude Code Wrappers (`.claude/commands/`)
```
.claude/commands/
├── modes/
│   ├── analyst.md
│   ├── architect.md
│   ├── developer.md
│   ├── ux-designer.md
│   └── orchestrator.md
└── skills/
    ├── qa-gate.md
    └── extract-learnings.md
```

#### Documentation
- Updated all existing docs for v1.3.0
- Added ADR-017: Agent Orchestration Layer
- New `docs/release-notes-v1.3.0.md`
- New `docs/session-protocol-v1.3.0.md`

### Verification

- [x] Agent specs are self-contained and tool-agnostic
- [x] Claude Code wrappers reference specs (no duplication)
- [x] Session protocol unchanged (Layer 0 still works alone)
- [x] All docs updated with v1.3.0 references
- [x] ADR-017 documents the architectural decision

---

*Cortex v1.3.0 - Development completed 2026-02-01*
