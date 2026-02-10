# Architecture Decision Records (ADRs)

This document records the key architectural decisions made during Cortex development.

---

## ADR-001: Local Embedding Model

**Date:** 2026-01-26
**Status:** Accepted

### Context
Need an embedding model for semantic search. Options include API-based (OpenAI, Cohere) or local models.

### Decision
Use **intfloat/e5-small-v2** running locally via sentence-transformers.

### Rationale
| Factor | API-based | Local (e5-small-v2) |
|--------|-----------|---------------------|
| Cost | Per-request fees | Free |
| Privacy | Data sent externally | Data stays local |
| Latency | Network round-trip | ~50ms local |
| Offline | No | Yes |
| Quality | Excellent | Good (sufficient for retrieval) |

### Consequences
- No API costs or rate limits
- Works offline
- ~130MB model download (one-time)
- Slightly lower quality than large API models (acceptable trade-off)

---

## ADR-002: Brute-Force Vector Index

**Date:** 2026-01-26
**Status:** Accepted

### Context
Need a vector index for similarity search. Options include specialized databases (Pinecone, Weaviate), approximate nearest neighbor libraries (FAISS, Annoy), or simple brute-force.

### Decision
Use **NumPy brute-force** with pickle serialization.

### Rationale
At expected scale (<500 vectors):
- Brute-force: <1ms search time
- Zero dependencies beyond NumPy
- No index corruption issues
- Simple rebuild if needed

Specialized solutions add complexity without benefit at this scale.

### Consequences
- Simple, reliable implementation
- May need upgrade if scale exceeds 10k+ vectors
- Easy to migrate later if needed (just swap indexer)

---

## ADR-003: Markdown with YAML Frontmatter

**Date:** 2026-01-26
**Status:** Accepted

### Context
Need a storage format for chunks and memories. Options include pure JSON, pure YAML, pure Markdown, or hybrid.

### Decision
Use **Markdown with YAML frontmatter**.

### Rationale
Research shows format processing overhead:
| Format | LLM Reasoning Degradation |
|--------|---------------------------|
| Natural Language | 0% (baseline) |
| Markdown | 2-5% |
| YAML | 8-12% |
| JSON | 10-15% |

Markdown body with minimal YAML frontmatter gives:
- Human readable
- LLM optimal (2-5% overhead)
- Structured metadata where needed
- Git-friendly (text-based diffs)

### Consequences
- Slightly more complex parsing than pure JSON
- Best balance of human and LLM readability
- Easy manual editing if needed

---

## ADR-004: Position-Aware Context Assembly

**Date:** 2026-01-26
**Status:** Accepted

### Context
Research shows LLMs exhibit "lost in middle" attention patterns - high attention at start (primacy) and end (recency), lower in middle.

### Decision
Structure context frames with **critical information at edges**.

### Structure
```
TOP (primacy zone)     → Task Definition
UPPER-MIDDLE           → Relevant Knowledge
LOWER-MIDDLE           → Past Learnings
BOTTOM (recency zone)  → Current State
VERY END               → Instructions
```

### Rationale
- Task definition needs high attention → top
- Instructions need high attention → bottom
- Supporting info can tolerate lower attention → middle

### Consequences
- More effective context utilization
- Requires careful section ordering
- May need adjustment for different LLM architectures

---

## ADR-005: Semantic Chunking Strategy

**Date:** 2026-01-26
**Status:** Accepted

### Context
Need to break documents into retrievable units. Options include fixed-size, sentence-based, or semantic chunking.

### Decision
Use **semantic-aware chunking** based on markdown structure.

### Algorithm
1. Split by markdown headers (preserve semantic boundaries)
2. If section > 500 tokens, split by paragraphs
3. Merge chunks < 50 tokens
4. Add 50-token overlap at boundaries

### Parameters
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| MAX_CHUNK_SIZE | 500 tokens | Matches e5-small-v2 max |
| MIN_CHUNK_SIZE | 50 tokens | Avoid fragments |
| OVERLAP | 50 tokens | Context continuity |

### Consequences
- Preserves semantic coherence
- Aligned with embedding model limits
- Overlap prevents information loss at boundaries

---

## ADR-006: Multi-Factor Retrieval Scoring

**Date:** 2026-01-26
**Status:** Accepted

### Context
Pure semantic similarity may not always surface the most useful results.

### Decision
Use **multi-factor scoring** combining multiple signals.

### Formula
```
score = 0.6 × semantic_similarity +
        0.2 × keyword_overlap +
        0.1 × recency_factor +
        0.1 × frequency_factor
```

### Rationale
| Factor | Weight | Why |
|--------|--------|-----|
| Semantic | 60% | Primary signal, embedding similarity |
| Keyword | 20% | Exact matches matter for technical terms |
| Recency | 10% | Newer content often more relevant |
| Frequency | 10% | Often-retrieved content proved useful |

### Consequences
- Better retrieval quality than pure semantic
- Tunable weights for different use cases
- Slightly more complex scoring logic

---

## ADR-007: Hybrid Memory Extraction

**Date:** 2026-01-26
**Status:** Accepted

### Context
Need to extract learnings from session text. Could be fully automatic, fully manual, or hybrid.

### Decision
Use **hybrid extraction with confidence thresholds**.

### Approach
| Confidence | Trigger | Action |
|------------|---------|--------|
| High | Verified fixes, explicit "remember" | Auto-save option |
| Medium | Discoveries, requirements | Propose for approval |
| Low | Inferences | Propose for approval |

### Rationale
- Fully automatic: Risk of noise
- Fully manual: Burden on user
- Hybrid: Best of both worlds

### Consequences
- User retains control
- High-confidence auto-save reduces friction
- Pattern detection may miss some learnings

---

## ADR-008: PowerShell CLI with Python Core

**Date:** 2026-01-26
**Status:** Accepted

### Context
Need a CLI interface. Options include pure Python CLI, pure PowerShell, or hybrid.

### Decision
Use **PowerShell scripts calling Python modules**.

### Rationale
- PowerShell: Native Windows integration, good UX
- Python: ML ecosystem (sentence-transformers, numpy)
- Hybrid: Best of both worlds

### Structure
```
PowerShell (CLI layer)
    │
    └──► Python (core logic)
            │
            └──► sentence-transformers, numpy, tiktoken
```

### Consequences
- Requires both PowerShell and Python
- Clean separation of concerns
- Cross-platform possible with PowerShell Core

---

## ADR-009: Token Budget System

**Date:** 2026-01-26
**Status:** Accepted

### Context
Context frames must fit within LLM context windows while maximizing useful content.

### Decision
Implement **configurable token budgets** with proportional allocation.

### Default Budget (15,000 tokens)
| Section | Tokens | % |
|---------|--------|---|
| Task Definition | 2,000 | 13% |
| Chunks | 10,000 | 65% |
| Memories | 2,000 | 13% |
| State | 1,000 | 6% |
| Instructions | 500 | 3% |

### Rationale
- 15k frame + 70k reserved (system, response) = 85k
- Leaves 115k for conversation in 200k window
- Proportions based on typical importance

### Consequences
- Predictable context consumption (~8%)
- May truncate content to fit budget
- Configurable for different needs

---

## ADR-010: Semi-Auto Session Protocol

**Date:** 2026-01-26
**Status:** Accepted
**Version:** 1.1.0

### Context

In v1.0.0, users must manually invoke PowerShell scripts at specific points in their workflow:
- `cortex-status.ps1` at session start
- `cortex-assemble.ps1` when starting a task
- `cortex-retrieve.ps1` for additional context
- `cortex-extract.ps1` at session end

This creates friction and technical barriers for non-technical users, leading to underutilization of Cortex capabilities.

### Decision

Implement a **Semi-Auto Session Protocol** where:
1. Agent automatically invokes scripts based on detected user intent
2. Users interact through natural language, not script commands
3. Session end remains user-triggered to maintain human control

### Protocol Design

| Phase | Trigger | Agent Action | User Experience |
|-------|---------|--------------|-----------------|
| Start | Agent awakens | `cortex-status` | Transparent |
| Task | "Let's work on X" | `cortex-assemble -Task "X"` | Seamless context |
| Retrieval | "What do we know about X" | `cortex-retrieve -Query "X"` | Natural Q&A |
| End | "Update learning" | `cortex-extract` | Explicit control |

### Natural Language Patterns

**Task Detection:**
- "Let's work on {X}"
- "Help me with {X}"
- "I need to implement {X}"

**Retrieval Detection:**
- "What do we know about {X}"
- "Get more details about {X}"
- "Tell me about {X}"
- "cortex: {X}" (explicit)

**Session End Detection:**
- "Update learning"
- "Save learnings"
- "End session"

### Rationale

| Approach | Pros | Cons |
|----------|------|------|
| Manual (v1.0.0) | Full control | Technical barrier, friction |
| Full-Auto | Zero friction | Loss of control, potential noise |
| **Semi-Auto (v1.1.0)** | Natural UX, human control preserved | Requires intent detection |

Semi-auto provides the best balance:
- Non-technical users can work naturally
- Power users can use explicit "cortex:" prefix
- Learning extraction remains user-controlled

### Context Budget Analysis

| Metric | Previous (Neocortex) | v1.0.0 Manual | v1.1.0 Semi-Auto |
|--------|---------------------|---------------|------------------|
| Start context | ~35% | 0% (user forgot) | ~0.025% |
| Task context | +more | 0% (user forgot) | ~1.25% |
| Total before work | 35%+ | 0% (no context!) | **~1.3%** |

The semi-auto approach ensures context is always available when needed, while staying minimal.

### Implementation

**No code changes required.** The protocol is implemented through agent instructions in:
- Project `CLAUDE.md`
- Global `~/.claude/CLAUDE.md`

Agents learn *when* to invoke existing scripts through documented patterns.

### Consequences

**Positive:**
- Accessible to non-technical users
- Consistent context availability
- Maintains retrieval-based efficiency

**Negative:**
- Requires pattern matching for intent detection
- May occasionally misinterpret user intent
- Explicit "cortex:" escape hatch needed for edge cases

### Testing Criteria

- [ ] Session start loads only metadata (~50 tokens)
- [ ] Task phrases trigger assembly automatically
- [ ] At least 6 retrieval patterns work
- [ ] "cortex:" explicit trigger works
- [ ] "Update learning" triggers extraction
- [ ] Total context < 5% for typical session

---

## ADR-011: Cross-Platform Python CLI

**Date:** 2026-01-27
**Status:** Accepted
**Version:** 1.2.0

### Context

The v1.0.0/v1.1.0 CLI used PowerShell scripts calling Python modules. While this worked well on Windows, it created barriers for Mac/Linux users and added complexity.

### Decision

Replace PowerShell CLI with a **pure Python CLI** using Typer.

### Rationale

| Factor | PowerShell + Python | Pure Python (Typer) |
|--------|---------------------|---------------------|
| Cross-platform | Windows-centric | Full support |
| Dependencies | PowerShell Core needed | Python only |
| Maintenance | Two languages | Single codebase |
| UX | Good | Equally good (Rich) |

### Implementation

```
cli/
├── __init__.py
├── __main__.py      # python -m cli entry point
├── main.py          # Typer app
└── commands/        # Command modules
```

### Consequences

**Positive:**
- Works on Windows, Mac, Linux without changes
- Simpler codebase (one language)
- Easier to maintain and extend

**Negative:**
- PowerShell scripts deprecated (migration guide provided)
- Existing users need to update workflows

---

## ADR-012: Chunk Provenance Tracking

**Date:** 2026-01-27
**Status:** Accepted
**Version:** 1.2.0

### Context

After chunking, there's no link back to source files. When documentation changes, chunks become stale with no way to detect or refresh them.

### Decision

Add **provenance fields** to chunk metadata:
- `source_path` - Relative path to source file
- `source_hash` - SHA256 hash of source content at chunk time

### Implementation

```yaml
# In chunk frontmatter
source_path: "docs/architecture.md"
source_hash: "a1b2c3d4e5f6..."
```

**Stale Detection:**
```bash
python -m cli status  # Shows stale chunks
```

**Refresh Workflow:**
```bash
python -m cli chunk --path docs/file.md --refresh
python -m cli index
```

### Consequences

**Positive:**
- Know exactly where each chunk came from
- Detect when source files change
- Simple refresh workflow

**Negative:**
- Slightly larger chunk metadata
- Requires index rebuild after refresh

---

## ADR-013: Memory Retrieval Tracking

**Date:** 2026-01-27
**Status:** Accepted
**Version:** 1.2.0

### Context

Memory scoring uses a frequency factor (10% weight), but retrieval_count was never actually incremented during context assembly.

### Decision

Implement **automatic retrieval tracking** in the assembler.

### Implementation

When a memory is included in a context frame:
1. Call `increment_retrieval(memory_id, project_root)`
2. This increments `retrieval_count` and updates `last_retrieved`

### Consequences

**Positive:**
- Frequency factor now works as intended
- Frequently-used memories rank higher over time
- Creates feedback loop for relevance

**Negative:**
- Minor write overhead during assembly

---

## ADR-014: Won't Implement - Semantic Deduplication

**Date:** 2026-01-27
**Status:** Won't Implement
**Reference:** MF-001

### Context

Expert review raised concern: semantically similar chunks from different documents could exist.

### Decision

**Won't implement** semantic deduplication.

### Rationale

1. **Retrieval handles it**: Top-k results naturally surface the best match
2. **Duplicates aren't harmful**: Just slightly less efficient retrieval
3. **Complexity cost**: Dedup logic adds maintenance burden
4. **No observed problem**: Not seen in practice

### Conclusion

Solving a theoretical problem with no practical impact violates simplicity principle.

---

## ADR-015: Won't Implement - Memory Confidence Calibration

**Date:** 2026-01-27
**Status:** Won't Implement
**Reference:** MF-003

### Context

Expert review noted: confidence is assigned by extraction pattern, not actual correctness.

### Decision

**Won't implement** confidence calibration.

### Rationale

1. **User approves memories**: Human-in-the-loop catches errors
2. **Patterns are reasonable**: "Fixed by X" → high confidence is sensible
3. **Complexity cost**: Verification systems add significant complexity
4. **No observed problem**: Pattern-based confidence works in practice

### Conclusion

Current approach provides good-enough confidence with minimal complexity.

---

## ADR-016: Won't Implement - Query Refinement

**Date:** 2026-01-27
**Status:** Won't Implement
**Reference:** MF-004

### Context

Expert review noted: if retrieval returns poor results, there's no mechanism to refine the query.

### Decision

**Won't implement** automatic query refinement.

### Rationale

1. **User can rephrase**: Natural interaction allows retry
2. **Explicit trigger**: "cortex: X" provides direct control
3. **Complexity cost**: Multi-turn refinement adds significant complexity
4. **No observed problem**: Single-pass retrieval works well

### Conclusion

Human-in-the-loop query refinement is simpler and equally effective.

---

## ADR-017: Agent Orchestration Layer

**Date:** 2026-02-01
**Status:** Accepted
**Version:** 1.3.0

### Context

Cortex provided the core context management system (chunking, embedding, retrieval, assembly) and a session protocol for natural language interaction. However, users who cloned the repo got only the CLI tool — no agent personas, no structured workflows, no orchestration patterns. The agent layer existed only in the developer's personal `~/.claude/CLAUDE.md`.

### Decision

Bundle an **Agent Orchestration Layer** directly in the Cortex repo with:
- 5 specialist modes (Analyst, Architect, Developer, UX Designer, Orchestrator)
- 2 workflow skills (QA Gate, Extract Learnings)
- Tool-agnostic specs in `agents/` with Claude Code thin wrappers in `.claude/commands/`

### Architecture

**Single-source with thin wrappers:**
- Source of truth: `agents/modes/*.md` (tool-agnostic, any LLM tool can use)
- Claude Code integration: `.claude/commands/modes/*.md` (~4 lines each, reference the spec)
- No duplication — one file to maintain per agent

**Two-layer design:**
- Layer 0: Session Protocol (unchanged, always active)
- Layer 1: Agent Mode (optional, adds persona lens)

### Rationale

| Approach | Pros | Cons |
|----------|------|------|
| No agents (v1.2.0) | Simple | Incomplete package, manual workflow |
| Claude Code only | Works out of box for CC users | Excludes other tools |
| Tool-agnostic only | Universal | No slash command convenience |
| **Both (v1.3.0)** | Universal + convenient | Two file locations (mitigated by thin wrappers) |

### Orchestrator Design

The Orchestrator is a **planning mode**, not a runtime coordinator. Claude Code is single-agent, so the Orchestrator:
1. Analyzes scope and produces a phased work plan
2. Assigns each phase to a specialist mode
3. User activates modes sequentially
4. Progress tracked via Cortex memories

### Consequences

**Positive:**
- Cortex ships as a complete package
- Works with Claude Code and any other LLM tool
- Zero context cost (modes don't consume retrieval budget)
- Modes are optional — core system works without them

**Negative:**
- More files to maintain (7 specs + 7 wrappers)
- Orchestrator coordination is manual (user switches modes)
- Mode persistence depends on conversation context (may drift in long sessions)

---

## ADR-018: Complete Standalone Methodology

**Date:** 2026-02-01
**Status:** Accepted
**Version:** 2.0.0

### Context

Cortex v1.3.0 shipped with 5 agent modes and 2 skills — enough to demonstrate the concept but not enough to be a self-contained methodology. Users still needed external systems (like BMAD) for project planning templates, quality checklists, and structured workflows. Additionally, the Orchestrator was positioned as the required entry point, and there was no QA agent.

### Decision

Transform Cortex into a **complete, standalone software development methodology** with:
- 6 agents (adding QA, promoting from a skill to a full agent)
- 29 workflow skills (purpose-built, not ported from external systems)
- 14 artifact templates
- 6 phase validation checklists
- Decentralized orchestration (any agent can start first)
- Agent-specific hard rules (no deprecated libs, no assumptions, no time estimates)
- Self-indexing via bootstrap command (METHODOLOGY domain)
- Handoff protocol storing phase transitions as retrievable memories

### Alternatives Considered

| Approach | Pros | Cons |
|----------|------|------|
| Bulk-port from BMAD | Fast, many files | Identity confusion, BMAD baggage, not designed for Cortex |
| Minimal additions | Low effort | Incomplete methodology, still needs external tools |
| **Purpose-built (chosen)** | Designed for Cortex, self-indexing, coherent | More effort to create |

### Key Design Decisions

1. **Decentralized orchestration** — Orchestrator is optional, not the entry point. Any agent orients itself from Cortex state.
2. **QA as full agent** — Testing strategy, test case design, and acceptance review warrant more than a single checklist skill.
3. **Agent rules** — Hard constraints baked into mode specs. Developer must verify library currency. Analyst must not work with assumptions. No agent produces time estimates.
4. **Self-indexing** — Bootstrap chunks all methodology resources into Cortex. Agents retrieve skills on-demand via semantic search instead of loading everything into context.
5. **Handoff as memory** — Phase transitions stored as procedural memories with standardized keywords, enabling automatic retrieval by the next agent.

### Consequences

**Positive:**
- Cortex is self-contained — no external methodology dependencies
- Context consumption stays at 3-5% (skills retrieved on-demand, not pre-loaded)
- Any agent can start first (flexibility for users who know the SDLC)
- Methodology resources are searchable through the same engine that manages project content

**Negative:**
- ~80 new files to maintain
- Bootstrap step required after modifying methodology resources
- Templates and checklists need iteration based on real usage

---

## ADR-019: Standalone Installation via .cortex-engine

**Date:** 2026-02-01
**Status:** Accepted
**Version:** 2.1.0

### Context

Cortex v2.0.0 required users to clone the repo, manually copy files, install dependencies, and configure their global CLAUDE.md. Users who tried "cortex init" in a new project got "No module named cli" because the CLI wasn't present. The installation experience needed to be as simple as BMAD's `npx bmad-method install`.

### Decision

Implement a **clone-and-run installation** pattern:
- "cortex init" (natural language) clones the Cortex repo into `.cortex-engine/`
- Copies methodology files (`agents/`, `.claude/commands/`, `CLAUDE.md`) to project root
- Runs `init → bootstrap → index` from `.cortex-engine/` with `--root ..`
- "cortex update" pulls latest and re-bootstraps

### Key Technical Changes

1. **CLI path resolution** — `sys.path.insert` now uses `Path(__file__).resolve().parent.parent.parent` (engine root) instead of project root. This allows `core/` to be found when the engine is in `.cortex-engine/`.

2. **CLI invocation pattern** — `cd .cortex-engine && python -m cli <cmd> --root ..` instead of `python -m cli <cmd>`.

3. **Global CLAUDE.md** — Rewritten as complete standalone file with init/update instructions baked in.

### Alternatives Considered

| Approach | Pros | Cons |
|----------|------|------|
| pip install | Clean, system-wide | Packaging work, where do agents go? |
| Central clone (~/.cortex/engine) | Single copy | Complex path management |
| **Clone per project (.cortex-engine/)** | Simple, self-contained, same as BMAD | Duplicated per project |

### Rationale

Clone-per-project is the simplest approach that works without packaging infrastructure. It mirrors BMAD's pattern where each project gets its own copy. The trade-off (duplication) is acceptable — engine code is small and updates are a simple `git pull`.

### Consequences

**Positive:**
- "cortex init" works from any empty folder
- No pip packaging needed
- Each project is self-contained
- Updates via `git pull`

**Negative:**
- Engine duplicated per project (~10MB)
- `.cortex-engine/` should be in `.gitignore`
- CLI invocation is longer (`cd .cortex-engine && ...`)

---

## ADR-020: Global CLAUDE.md Slimming

**Date:** 2026-02-01
**Status:** Accepted
**Version:** 2.1.0

### Context

The global `~/.claude/CLAUDE.md` had grown to ~450 lines and contained significant problems:

1. **Duplication** — The session protocol, CLI commands, memory domains, agent system, and context budget were duplicated nearly verbatim between global and project CLAUDE.md. Every Cortex project loaded this content twice.
2. **Project-specific content in global scope** — ~60% of the global file (init/update procedures, session protocol, CLI invocation patterns) only applied to projects with `.cortex-engine/`. Non-Cortex projects processed irrelevant instructions.
3. **Critical Thinking Protocol bloat** — ~110 lines of metacognition instructions, where only ~40 lines (the lookup tables) produced measurable behavioral change.

### Decision

**Slim the global CLAUDE.md to ~175 lines** containing only universal rules:

1. **Keep** the four behavioral tables (uncertainty communication, disagreement handling, anti-patterns, external verification) — these are lookup tables with concrete patterns that directly shape model output.
2. **Cut** the four-layer metacognition structure (dispositions, triggers, self-monitoring, domain checkpoints) — abstract virtues and internal questions don't produce verifiable behavior change.
3. **Move** domain-specific checkpoints to agent mode specs — each agent already has its own domain thinking guidance.
4. **Move** session protocol, CLI commands, memory domains, and agent system to the project CLAUDE.md only.
5. **Keep** init/update procedures in both global and project CLAUDE.md — the global file must contain these because it's the only file present before initialization (see Amendment below).

### Analysis: What's Load-Bearing vs Decorative

| Content | Lines | Impact | Decision |
|---------|-------|--------|----------|
| Uncertainty communication table | 12 | High — directly shapes output language | Keep |
| Disagreement handling table | 8 | High — concrete escalation levels | Keep |
| Anti-patterns table | 10 | High — prevents specific failure modes | Keep |
| External verification principle | 8 | High — stops false correctness claims | Keep |
| Layer 1: Default Dispositions | 6 | Low — generic virtues models already exhibit | Cut |
| Layer 2: Automatic Triggers | 8 | Low — describes existing model behavior | Cut |
| Layer 4: Metacognition | 8 | Low — unverifiable internal questions | Cut |
| Domain-Specific Checkpoints | 25 | Medium — but already in agent mode files | Move to agents |
| Session protocol + CLI | ~155 | High — but project-specific | Move to project |
| Init/Update procedures | ~55 | High — must be in global (bootstrap) | Keep in both |

### Consequences

**Positive:**
- Global file reduced from ~450 to ~230 lines (49% reduction)
- Session protocol, agent system, memory domains no longer duplicated
- Non-Cortex projects process less irrelevant content
- All behavioral shaping preserved (the four tables)

**Negative:**
- Init/update procedures intentionally duplicated in both files (bootstrap requirement)

### Amendment: Init/Update Chicken-and-Egg

**Date:** 2026-02-01

Initial implementation moved init/update procedures entirely to project CLAUDE.md. Testing in a new empty folder revealed the chicken-and-egg problem: "cortex init" requires these instructions, but the project CLAUDE.md doesn't exist until after initialization completes (step 3 copies it from the engine).

**Fix:** Restored init/update procedures to the global CLAUDE.md. This duplication is intentional and necessary — the global file bootstraps the project file. Final global file size: ~230 lines (still down from ~450).

---

## ADR-021: Virtual Environment Isolation

**Date:** 2026-02-10
**Status:** Accepted
**Version:** 2.2.0

### Context

When Cortex is installed into a project via `.cortex-engine/`, the initialization runs `pip install -r .cortex-engine/requirements.txt` into whatever Python environment is active. This causes three problems:

1. **Wrong environment** — If the project has its own venv (e.g., Django, Flask), Cortex dependencies (`typer`, `sentence-transformers`, `numpy`) may not get installed there because the system Python was used instead.
2. **Pollution** — If the project's venv IS active, Cortex dependencies pollute it with packages unrelated to the project.
3. **Version conflicts** — Cortex's dependency versions may conflict with the project's own requirements.

When the CLI fails due to missing modules (e.g., `ModuleNotFoundError: No module named 'typer'`), the agent improvises shell commands for status. On Windows, commands like `dir | find /c /v ""` produce hundreds of thousands of lines of garbage output because Windows `find.exe` is completely different from Unix `find`.

### Decision

Create and manage a Cortex-owned virtual environment at `.cortex-engine/.venv/`. All CLI invocations use this venv's Python interpreter directly, without requiring activation.

### Alternatives Considered

| Approach | Pros | Cons |
|----------|------|------|
| System pip install | Simple, one command | Wrong env, conflicts, pollution |
| pipx | Proper isolation | Extra dependency, not self-contained |
| Docker | Full isolation | Heavy, requires Docker installed |
| **Dedicated venv** | Self-contained, no conflicts, stdlib | Platform-specific interpreter paths |

### Rationale

`python -m venv` is part of the Python standard library and works on all platforms. The venv lives inside `.cortex-engine/`, maintaining the self-contained design established in ADR-019. Platform-specific paths (`.venv/Scripts/python` on Windows, `.venv/bin/python` on Unix) are manageable through documentation showing both patterns.

The CLI invocation changes from:
```
cd .cortex-engine && python -m cli <command> --root ..
```
To:
```
# Windows:
cd .cortex-engine && .venv/Scripts/python -m cli <command> --root ..
# Unix:
cd .cortex-engine && .venv/bin/python -m cli <command> --root ..
```

### Consequences

**Positive:**
- Cortex dependencies never conflict with project dependencies
- Works regardless of which venv is active in the shell
- Self-contained inside `.cortex-engine/` (consistent with ADR-019)
- No additional tools required (`venv` is in stdlib)
- Status command reports isolation state

**Negative:**
- CLI invocation path is longer (includes `.venv/Scripts/` or `.venv/bin/`)
- Platform-specific paths require documenting both Windows and Unix variants
- Additional disk space for the venv (~50MB minimum, more with PyTorch for sentence-transformers)
- Pre-v2.2.0 installations need migration (create the venv manually)
