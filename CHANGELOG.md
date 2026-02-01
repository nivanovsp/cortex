# Changelog

All notable changes to Cortex will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2026-02-01

### Added

- **Standalone Installation** - `cortex init` works from any empty project folder
  - Clones Cortex repo into `.cortex-engine/` automatically
  - Installs Python dependencies
  - Copies `agents/`, `.claude/commands/`, and `CLAUDE.md` into project
  - Runs init → bootstrap → index → verify in sequence
  - Adds `.cortex-engine/` and `.cortex/` to `.gitignore`

- **Cortex Update** - `cortex update` pulls latest and re-bootstraps
  - Pulls from GitHub into `.cortex-engine/`
  - Re-copies methodology files to project root
  - Re-bootstraps with `--force` and rebuilds indices

- **Complete Global CLAUDE.md** - `global/CLAUDE.md` is now fully standalone
  - Includes universal rules (RMS framework, conventions, protocols)
  - Includes Critical Thinking Protocol (4 layers)
  - Includes Cortex session protocol with `.cortex-engine` CLI pattern
  - Includes Cortex Initialization and Update instructions
  - No external dependencies (removed Neocortex/MLDA/Beads references)

- **`/skills:cortex-init`** - Slash command for initialization (via global CLAUDE.md)

### Changed

- **CLI Path Resolution** - All commands now resolve `core/` relative to the engine location
  - Uses `Path(__file__).resolve().parent.parent.parent` instead of project root
  - Backward compatible — works the same when running from Cortex repo directly
  - Enables running from `.cortex-engine/` with `--root ..`

- **CLI Invocation Pattern** - Updated from `python -m cli <cmd>` to:
  - Installed projects: `cd .cortex-engine && python -m cli <cmd> --root ..`
  - Development (in Cortex repo): `python -m cli <cmd>` (unchanged)

- **Session Protocol** - All CLI references updated for `.cortex-engine` pattern
- **Project CLAUDE.md** - Updated CLI Reference with both invocation patterns
- **Global CLAUDE.md** - Complete rewrite as standalone file
- **`core/__init__.py`** - Version updated to 2.0.0

### Fixed

- `core/__init__.py` version was stuck at 1.2.0, now correctly reads 2.0.0

---

## [2.0.0] - 2026-02-01

### Added

- **Complete Standalone Methodology** - Cortex is now a self-contained development methodology
  - 6 specialist agents (Analyst, Architect, Developer, QA, UX Designer, Orchestrator)
  - 29 workflow skills across all agents
  - 6 phase validation checklists
  - 14 artifact templates
  - Bootstrap command for methodology resource indexing

- **QA Agent** - Full quality assurance persona with dedicated skills
  - `/modes:qa` - Test strategy, quality gates, acceptance review
  - Skills: test-strategy, test-case-design, quality-gate, acceptance-review, accessibility-review

- **Agent-Specific Rules** - Hard constraints baked into each agent
  - Developer: verify library currency, no deprecated APIs
  - Architect: validate against current LTS/stable releases
  - Analyst: requirements must be unambiguous, clear, testable, measurable
  - QA: test only against documented acceptance criteria
  - All agents: no time estimates or duration predictions

- **Decentralized Orchestration** - Any agent can be the entry point
  - Topic-first activation: agent greets, user selects topic, then context loads
  - Orchestrator is optional, not required as entry point
  - Handoff skill stores phase transitions as retrievable memories

- **Bootstrap Command** - `python -m cli bootstrap`
  - Chunks agents/ directory into METHODOLOGY domain
  - Makes skills, templates, checklists retrievable via semantic search
  - `--force` flag for re-chunking

- **Handoff Skill** - Structured phase transition protocol
  - Stores as procedural memory with standardized keywords
  - Next agent retrieves handoff context automatically

- **Skills** (27 new)
  - Orchestrator: project-plan, phase-decomposition, handoff, progress-review, risk-assessment
  - Analyst: elicit-requirements, create-prd, gap-analysis, define-acceptance-criteria, stakeholder-analysis
  - Architect: system-design, api-design, nfr-assessment, create-adr, tech-evaluation, security-review
  - Developer: implementation-plan, code-review, debug-workflow, refactor-assessment
  - QA: test-strategy, test-case-design, quality-gate, acceptance-review, accessibility-review
  - UX Designer: wireframe, user-flow, design-system, usability-review

- **Checklists** (6 new)
  - phase-transition, requirements-complete, architecture-ready
  - implementation-done, release-ready, ux-complete

- **Templates** (14 new)
  - project-brief, phase-plan, prd, requirements-spec
  - architecture, api-spec, adr
  - implementation-plan, code-review-report
  - test-plan, qa-report
  - wireframe, user-flow, design-system

### Changed

- **Session Protocol** - Updated to v2.0.0 with decentralized activation
- **Mode Specs** - All 5 existing modes updated with Rules and Skills sections
- **CLAUDE.md** - Full rewrite for v2.0.0 methodology
- **README.md** - Updated for complete methodology

---

## [1.3.0] - 2026-02-01

### Added

- **Agent Orchestration Layer** - Expert agent modes bundled with Cortex
  - 5 specialist modes: Analyst, Architect, Developer, UX Designer, Orchestrator
  - 2 workflow skills: QA Gate, Extract Learnings
  - Tool-agnostic specs in `agents/` directory
  - Claude Code slash commands via `.claude/commands/`

- **Agent Modes**
  - `/modes:analyst` - Requirements analysis, gap identification, acceptance criteria
  - `/modes:architect` - System design, trade-offs, architecture decision records
  - `/modes:developer` - Implementation, debugging, code review
  - `/modes:ux-designer` - Interface design, accessibility, user flows
  - `/modes:orchestrator` - Work planning, phase coordination across modes

- **Workflow Skills**
  - `/skills:qa-gate` - Structured quality validation checklist
  - `/skills:extract-learnings` - Guided session learning extraction

- **Two-Layer Architecture**
  - Layer 0: Session Protocol (always active, unchanged from v1.2.0)
  - Layer 1: Agent Mode (optional, adds persona and domain focus)

- **Tool-Agnostic Design**
  - Agent specs in `agents/modes/*.md` work with any LLM tool
  - Claude Code wrappers in `.claude/commands/` for slash command support

- **New ADR**
  - ADR-017: Agent Orchestration Layer

### Changed

- **CLAUDE.md** - Added Agent Modes section with available modes and suggestions
- **global/CLAUDE.md** - Added agent modes reference
- **README.md** - Added Agent Modes feature section
- **Documentation** - All docs updated for v1.3.0

---

## [1.2.0] - 2026-01-27

### Added

- **Cross-Platform Python CLI** - Replaces PowerShell scripts
  - Works on Windows, Mac, and Linux
  - Uses Typer framework with Rich terminal formatting
  - Invoked via `python -m cli <command>`
  - All 8 commands ported: init, chunk, index, retrieve, assemble, memory, extract, status

- **Chunk Provenance Tracking** - Know where chunks came from
  - `source_path` - Relative path to original source file
  - `source_hash` - SHA256 hash for change detection
  - Stale chunk detection in `status` command
  - `--refresh` flag to update stale chunks

- **Memory Retrieval Tracking** - Feedback loop for relevance
  - Automatically increments `retrieval_count` when memory used
  - Updates `last_retrieved` timestamp
  - Frequency factor now works as intended in scoring

- **New ADRs**
  - ADR-011: Cross-Platform Python CLI
  - ADR-012: Chunk Provenance Tracking
  - ADR-013: Memory Retrieval Tracking
  - ADR-014: Won't Implement - Semantic Deduplication
  - ADR-015: Won't Implement - Memory Confidence Calibration
  - ADR-016: Won't Implement - Query Refinement

### Changed

- **CLI Commands** - PowerShell → Python
  - `.\cortex-chunk.ps1` → `python -m cli chunk`
  - `.\cortex-status.ps1` → `python -m cli status`
  - All commands follow same pattern

- **Dependencies** - Added Typer and Rich to requirements.txt

### Deprecated

- **PowerShell Scripts** - Still present but deprecated
  - Migration guide in `scripts/README.md`
  - Will be removed in future version

### Fixed

- Memory frequency scoring now works (retrieval tracking implemented)
- Chunk frontmatter includes provenance for traceability

---

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
