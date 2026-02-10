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

---

## v2.0.0 - Complete Standalone Methodology

**Date:** 2026-02-01
**Objective:** Transform Cortex from a context engine with basic agents into a complete, self-contained software development methodology

### Background

Cortex v1.3.0 demonstrated the agent orchestration concept with 5 modes and 2 skills. However, it was incomplete — users needed external methodologies (like BMAD) for templates, structured workflows, and quality checklists. A plan to bulk-port ~45 files from BMAD was rejected in favor of purpose-built resources designed for Cortex's retrieval-based architecture.

### Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Agent count | 6 (added QA) | Testing deserves a full agent, not just a checklist |
| Orchestration model | Decentralized | Any agent can start first; Orchestrator is optional |
| Skill design | Purpose-built | Designed for Cortex retrieval, not ported from BMAD |
| Methodology indexing | Self-indexing via bootstrap | Skills/templates chunked into METHODOLOGY domain |
| Agent rules | Hard constraints per agent | No deprecated libs, no assumptions, no time estimates |
| Handoff mechanism | Procedural memory | Stored with standardized keywords for retrieval |
| Version number | 2.0.0 (not 1.4.0) | Major evolution — complete methodology, not incremental feature |

### Deliverables

#### Agent System
- 6 agent mode specs (5 updated + 1 new QA) with Rules and Skills sections
- 29 workflow skills across all agents
- 6 phase validation checklists
- 14 artifact templates (YAML)
- 43 Claude Code wrappers

#### CLI
- New `bootstrap` command — chunks agents/ into METHODOLOGY domain

#### Documentation
- Updated all existing docs for v2.0.0
- Added ADR-018: Complete Standalone Methodology
- New release-notes-v2.0.0.md
- New session-protocol-v2.0.0.md

### Verification

- [x] 6 modes with Rules and Skills sections
- [x] 31 skills (29 new + 2 existing)
- [x] 6 checklists
- [x] 14 templates
- [x] Bootstrap creates 207 chunks in METHODOLOGY domain
- [x] Skill retrieval works via semantic search
- [x] Decentralized activation (any agent first)
- [x] No time estimates in any agent output

---

*Cortex v2.0.0 - Development completed 2026-02-01*

---

## v2.1.0 - Standalone Installation

**Date:** 2026-02-01
**Objective:** Make Cortex installable from any project folder with a single natural language command

### Background

Testing v2.0.0 in a new empty folder revealed the chicken-and-egg problem: "cortex init" required the CLI to already be present. The BMAD methodology solved this with `npx bmad-method install` — a single command that sets everything up. Cortex needed the same simplicity.

### Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Engine location | `.cortex-engine/` per project | Simple, self-contained, same as BMAD pattern |
| CLI path resolution | `Path(__file__).parent.parent.parent` | Finds `core/` relative to engine, not project root |
| Invocation pattern | `cd .cortex-engine && python -m cli <cmd> --root ..` | Python `-m` needs to run from engine dir |
| Init trigger | Natural language in global CLAUDE.md | No project files needed to start |
| Update mechanism | `git pull` + re-bootstrap | Simple, no package manager |
| Global CLAUDE.md | Complete standalone rewrite | Removed Neocortex/MLDA/Beads; added init/update instructions |

### Deliverables

#### CLI Changes
- All 9 command files in `cli/commands/` updated: `sys.path.insert` uses engine root
- Backward compatible — running from Cortex repo directly still works

#### Global CLAUDE.md (`global/CLAUDE.md`)
- Complete rewrite as standalone file
- Includes: RMS framework, conventions, protocols, Critical Thinking Protocol
- Includes: Cortex session protocol with `.cortex-engine` CLI pattern
- Includes: Cortex Initialization and Update instructions
- No external dependencies

#### Documentation
- Updated: CHANGELOG, INSTALL, README, architecture, cortex-spec, decisions, user-guide
- New: release-notes-v2.1.0.md, session-protocol-v2.1.0.md
- New ADR-019: Standalone Installation via .cortex-engine

### Verification

- [x] CLI works from `.cortex-engine/` with `--root ..`
- [x] CLI still works from Cortex repo directly (backward compatible)
- [x] Global CLAUDE.md is complete and standalone
- [x] "cortex init" instructions in global CLAUDE.md
- [x] "cortex update" instructions in global CLAUDE.md
- [x] All session protocol CLI references updated
- [x] `core/__init__.py` version corrected to 2.0.0

---

*Cortex v2.1.0 - Development completed 2026-02-01*

---

## v2.1.0 (continued) - Global CLAUDE.md Restructuring

**Date:** 2026-02-01
**Objective:** Eliminate duplication between global and project CLAUDE.md, condense Critical Thinking Protocol

### Background

The global `~/.claude/CLAUDE.md` had grown to ~450 lines with three problems: massive duplication with the project CLAUDE.md, project-specific content in global scope, and a ~110-line Critical Thinking Protocol where only ~40 lines (the four lookup tables) produced measurable behavioral change.

### Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Critical Thinking Protocol | Keep 4 tables, cut 4 layers | Tables are lookup-driven (high impact); layers are abstract virtues (low impact) |
| Domain checkpoints | Move to agent modes | All 6 agents already have domain-specific thinking guidance |
| Session protocol | Keep in project CLAUDE.md only | Project-specific content shouldn't be in global scope |
| Init/update procedures | Keep in both global and project | Global file is the only file present before init — must contain bootstrap instructions |
| Version | Stay at 2.1.0 | No functional change — just content reorganization |

### Deliverables

#### Global CLAUDE.md (`~/.claude/CLAUDE.md` and `global/CLAUDE.md`)
- Reduced from ~450 to ~230 lines (49% reduction)
- Kept: RMS framework, conventions, protocols, 4 behavioral tables, git conventions, init/update procedures
- Cut: Metacognition layers, domain checkpoints, session protocol, memory domains, agent system
- Added: "Cortex-Enabled Projects" pointer section

#### Project CLAUDE.md
- Added: Cortex Initialization and Update procedures (also in global — intentional duplication)
- Bumped: All version references to 2.1.0

#### Chicken-and-Egg Fix
- Initial attempt moved init/update entirely to project CLAUDE.md
- Testing in empty folder failed — no project CLAUDE.md exists before init
- Restored init/update to global file; duplication is intentional for bootstrap

#### Documentation
- Added ADR-020: Global CLAUDE.md Slimming

### Verification

- [x] All 4 behavioral tables preserved in global CLAUDE.md
- [x] Init/update procedures present in project CLAUDE.md
- [x] Init/update intentionally in both files (bootstrap requirement)
- [x] Global and distributable copy (`global/CLAUDE.md`) are identical
- [x] Version consistent at 2.1.0 across all files

---

*Cortex v2.1.0 - Development completed 2026-02-01*

---

## v2.1.1 - Extract Command Bug Fix

**Date:** 2026-02-04
**Objective:** Fix API mismatch between CLI and core extractor module

### Background

User reported errors when running `extract` command from an installed project. Investigation revealed function signature mismatches between `cli/commands/extract.py` and `core/extractor.py`:

1. CLI passed `project_root` as second positional arg, but `extract_and_format()` expected `min_confidence`
2. `extract_and_format()` returned a string, but CLI expected a dict with `memories` key
3. `save_proposed_memories()` expected `(proposed, indices, project_root)` but CLI called with `(memories, project_root)`

### Root Cause

The CLI command was written expecting a different API than what the core functions provided. The bug only manifested when using the `.cortex-engine/` installation pattern with `--root` flag.

### Fix

| Component | Change |
|-----------|--------|
| `core/extractor.py` | `extract_and_format()` now returns dict, accepts `project_root` param |
| `core/extractor.py` | `save_proposed_memories()` reordered params, made `indices` optional |
| `core/extractor.py` | Added `format_proposed_memories()` for string output |
| `cli/commands/extract.py` | Uses explicit keyword arguments |

### Verification

- [x] `extract` command works from `.cortex-engine/` with `--root ..`
- [x] `extract` command still works from Cortex repo directly
- [x] `--auto-save` flag works correctly
- [x] Both dict and ProposedMemory objects handled in save function

---

*Cortex v2.1.1 - Development completed 2026-02-04*

---

## v2.2.0 - Virtual Environment Isolation

**Date:** 2026-02-10
**Objective:** Prevent dependency conflicts between Cortex and host project environments

### Background

When Cortex was installed into a project that has its own virtual environment (e.g., Django, Flask, FastAPI), the initialization step `pip install -r .cortex-engine/requirements.txt` either:
1. Installed into the system Python (not the project's venv)
2. Polluted the project's venv with Cortex-specific dependencies
3. Conflicted with the project's own dependency versions

When Cortex's `typer` dependency wasn't available in the active environment, the CLI failed with `ModuleNotFoundError`, causing the agent to improvise shell commands. On Windows, these improvised commands (e.g., `dir | find /c /v ""`) produced 800K+ lines of garbage output because Windows `find.exe` behaves completely differently from Unix `find`.

### Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Venv location | `.cortex-engine/.venv/` | Self-contained inside engine dir (ADR-019) |
| Creation method | `python -m venv` | Standard library, no extra tools needed |
| CLI invocation | Direct interpreter path | No activation needed, works in any shell context |
| Backward compat | Fall back to bare `python` | Pre-v2.2.0 installs continue working |
| No new CLI command | Venv created before CLI | Chicken-and-egg: typer not available until venv is set up |

### Deliverables

| File | Change |
|------|--------|
| `core/__init__.py` | Version bump to 2.2.0 |
| `core/config.py` | Added `VENV_DIR`, `get_venv_python()`, `has_venv()` |
| `cli/commands/status.py` | Reports venv isolation status |
| `.gitignore` | Added `.venv/` |
| `CLAUDE.md` | Session protocol v2.2.0, venv-aware CLI invocation |
| `global/CLAUDE.md` | Init/update procedures with venv creation |
| `CHANGELOG.md` | v2.2.0 entry |
| `README.md` | Updated installation and CLI examples |
| `INSTALL.md` | Full venv setup instructions, migration guide |
| `docs/architecture.md` | Updated layout and invocation patterns |
| `docs/cortex-spec.md` | Updated CLI appendix |
| `docs/user-guide.md` | Updated setup instructions |
| `docs/decisions.md` | ADR-021: Virtual Environment Isolation |
| `docs/release-notes-v2.2.0.md` | Release notes (new) |
| `docs/session-protocol-v2.2.0.md` | Session protocol v2.2.0 (new) |
| `agents/skills/cortex-init.md` | Updated skill procedure |

### Verification

- [ ] Venv creation works on Windows
- [ ] Venv creation works on Unix
- [ ] CLI works through venv python on both platforms
- [ ] Status command reports venv status
- [ ] Pre-v2.2.0 installations still work (fallback to system python)
- [ ] Project's own venv is unaffected by Cortex dependencies

---

*Cortex v2.2.0 - Development completed 2026-02-10*
