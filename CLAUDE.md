# Cortex - Claude Code Instructions

> **Inherits from:** `~/.claude/CLAUDE.md` (Global Rules)
>
> All global rules, protocols, and conventions apply. This file contains project-specific additions.

---

## Project Overview

**Cortex** is a complete, self-contained software development methodology with LLM-native context management. It provides expert agents, structured skills, templates, and semantic retrieval — everything needed to go from requirements to delivered software.

**Version:** 2.0.0

---

## Session Protocol (v2.0.0)

This protocol defines how you (the agent) interact with Cortex throughout a session. Follow these instructions automatically — users should not need to know about commands.

### CLI Invocation

All CLI commands run from the `.cortex-engine/` directory with `--root` pointing to the project:

```
cd .cortex-engine && python -m cli <command> --root ..
```

When working inside the Cortex repo itself (development), the simpler `python -m cli <command>` works directly.

### Agent Activation (Decentralized)

**Any agent can be the entry point.** There is no required starting agent. Every agent follows the same activation flow:

1. Load mode spec (~2KB — persona, rules, skills list)
2. Run `cd .cortex-engine && python -m cli status --json --root ..` silently — note metadata
3. Greet the user as your persona — state what you can do
4. **Wait for the user to select a topic/task**
5. THEN retrieve handoffs, artifacts, and learnings for that topic
6. Begin work with relevant context

**Do NOT pre-load content or retrieve context before the user selects a topic.**

### On Session Start (Automatic — No Mode)

When the conversation begins without a mode activation:

1. Run `cd .cortex-engine && python -m cli status --json --root ..` silently
2. Note the result internally (chunk count, memory count, domains, stale chunks)
3. **DO NOT** load any content files — wait for task identification
4. Greet the user and mention Cortex is available if relevant
5. If stale chunks detected, mention briefly (user can refresh if needed)

**Context cost:** ~50 tokens (metadata only)

### On Task Identification (Automatic)

When the user specifies what to work on, detect phrases like:
- "Let's work on {X}"
- "I need to {X}"
- "Help me with {X}"
- "Working on {X}"
- "Going to implement {X}"
- "Want to {X}"
- "Fix/debug/update/modify {X}"

**Action:**
1. Extract the task from their statement
2. Run `cd .cortex-engine && python -m cli assemble --task "{extracted task}" --root ..`
3. Use the returned context frame to inform your work
4. **DO NOT** mention the command to the user — just have the context

**Context cost:** ~2,500 tokens

### On Retrieval Request (Natural Language)

When the user asks for more information, detect phrases like:
- "Get more details about {X}"
- "What do we know about {X}"
- "I need context on {X}"
- "Tell me about {X}"
- "Remind me how {X} works"
- "What did we learn about {X}"

**Explicit trigger:** If user says `cortex: {query}`, always treat as retrieval request.

**Action:**
1. Extract the topic from their question
2. Run `cd .cortex-engine && python -m cli retrieve --query "{topic}" --root ..`
3. Present the information naturally
4. **DO NOT** mention the command — just answer their question

**Context cost:** ~1,500 tokens per retrieval

### On Session End (User-Triggered)

When the user explicitly requests learning extraction, detect phrases like:
- "Update learning"
- "Save learnings"
- "End session"
- "Wrap up and save"
- "Extract what we learned"

**Action:**
1. Identify key learnings from the session (fixes, discoveries, procedures)
2. Run `cd .cortex-engine && python -m cli extract --text "{learnings summary}" --root ..`
3. Present proposed memories to the user with confidence levels
4. Ask which memories to save
5. Save approved memories
6. Run `cd .cortex-engine && python -m cli index --root ..` to rebuild the index

### Context Budget

| Phase | Tokens | % of 200k |
|-------|--------|-----------|
| Session start (metadata) | ~50 | 0.025% |
| Task assembly | ~2,500 | 1.25% |
| On-demand retrieval (×2) | ~3,000 | 1.5% |
| **Typical session total** | **~5,550** | **~2.8%** |

*Assumes 2 retrievals per session. Heavy debugging may reach 10-15%.*

**90%+ of context remains available for actual work.**

### Important Rules

1. **Never pre-load content files** — use retrieval only
2. **Commands are invisible to users** — they interact through natural language
3. **Session end requires user trigger** — never auto-extract learnings
4. **When uncertain, use explicit trigger** — "cortex: {query}" always works
5. **No time estimates** — no agent produces duration predictions or timeline estimates

---

## Project Structure

```
Cortex/
├── core/                 # Python core modules
│   ├── config.py         # Configuration
│   ├── embedder.py       # e5-small-v2 wrapper
│   ├── chunker.py        # Document chunking + provenance
│   ├── indexer.py        # Vector index management
│   ├── retriever.py      # Semantic search
│   ├── memory.py         # Memory CRUD + retrieval tracking
│   ├── assembler.py      # Context frame assembly
│   └── extractor.py      # Memory extraction
├── cli/                  # Python CLI (cross-platform)
│   ├── main.py           # Typer app entry point
│   └── commands/         # Command implementations
├── agents/               # Methodology resources (tool-agnostic)
│   ├── modes/            # Agent personas (6)
│   ├── skills/           # Workflow skills (29)
│   ├── checklists/       # Phase validation checklists (6)
│   └── templates/        # Artifact templates (14)
├── scripts/              # PowerShell CLI (deprecated)
├── docs/                 # Documentation
├── templates/            # Chunk/memory format templates
└── .cortex/              # Runtime data (chunks, memories, indices)
```

---

## Conventions

### Memory Domains
- `AUTH` - Authentication, sessions, tokens
- `UI` - Components, forms, styling
- `API` - Endpoints, requests, responses
- `DB` - Database, queries, migrations
- `TEST` - Testing, fixtures, mocks
- `DEV` - Build, deploy, tooling
- `METHODOLOGY` - Cortex skills, templates, checklists (bootstrapped)
- `GENERAL` - Everything else

### Memory Types
- `factual` - Stable knowledge ("API uses REST")
- `experiential` - Lessons learned ("X requires Y")
- `procedural` - How-to ("Always do X before Y")

### Confidence Levels
- `high` - Verified fixes, explicit notes
- `medium` - Reasonable inference
- `low` - Uncertain, needs verification

---

## Development Guidelines

### Adding New Features
1. Core logic goes in `core/` as Python modules
2. CLI interface in `cli/commands/` as Python (Typer)
3. Update `core/__init__.py` to export new functions
4. Add tests and documentation

### Modifying Chunking/Embedding
- Chunk size: 500 tokens max (matches e5-small-v2)
- Overlap: 50 tokens for continuity
- Always rebuild index after changes: `python -m cli index`
- Use `--refresh` flag when re-chunking modified files

### Environment Variables
All optional - defaults work out of the box:
- `CORTEX_EMBEDDING_MODEL` - Default: `intfloat/e5-small-v2`
- `CORTEX_CHUNK_SIZE` - Default: `500`
- `CORTEX_TOKEN_BUDGET` - Default: `15000`

---

## CLI Reference (Internal)

These commands are called automatically by the session protocol. Users should not need to invoke them directly.

### From installed projects (engine in `.cortex-engine/`)

All commands run from `.cortex-engine/` with `--root` pointing to the project:

```
cd .cortex-engine && python -m cli <command> --root ..
```

| Command | Purpose | When Called |
|---------|---------|-------------|
| `cd .cortex-engine && python -m cli status --root ..` | Get system metadata | Session start |
| `cd .cortex-engine && python -m cli assemble --task "..." --root ..` | Build context frame | Task identified |
| `cd .cortex-engine && python -m cli retrieve --query "..." --root ..` | Search for context | User asks for info |
| `cd .cortex-engine && python -m cli extract --text "..." --root ..` | Extract learnings | User ends session |
| `cd .cortex-engine && python -m cli index --root ..` | Rebuild indices | After saving memories |
| `cd .cortex-engine && python -m cli memory add --learning "..." --root ..` | Add memory manually | Explicit request |
| `cd .cortex-engine && python -m cli init --root ..` | Initialize Cortex | Project setup |
| `cd .cortex-engine && python -m cli bootstrap --root ..` | Chunk methodology | After init |
| `cd .cortex-engine && python -m cli chunk --path "..." --root ..` | Chunk documents | Adding new docs |
| `cd .cortex-engine && python -m cli chunk --path "..." --refresh --root ..` | Re-chunk modified files | Stale chunks |

### From Cortex repo (development)

When working inside the Cortex repo itself, the simpler form works:

```
python -m cli <command>
```

---

## Agent System (v2.0.0)

Cortex ships with a complete agent system — expert personas with dedicated skills, templates, and quality checklists. See `agents/README.md` for full details.

### Available Agents

| Agent | Activation | Focus |
|-------|-----------|-------|
| Analyst | `/modes:analyst` | Requirements, gap analysis, acceptance criteria |
| Architect | `/modes:architect` | System design, trade-offs, ADRs, NFRs |
| Developer | `/modes:developer` | Implementation, debugging, code review |
| QA | `/modes:qa` | Test strategy, quality gates, acceptance review |
| UX Designer | `/modes:ux-designer` | Interface design, accessibility, user flows |
| Orchestrator | `/modes:orchestrator` | Work planning, phase coordination, handoffs |

### Available Skills

| Skill | Activation | Agent |
|-------|-----------|-------|
| QA Gate | `/skills:qa-gate` | QA |
| Extract Learnings | `/skills:extract-learnings` | Any |
| Handoff | `/skills:handoff` | Orchestrator |
| Project Plan | `/skills:project-plan` | Orchestrator |
| Create PRD | `/skills:create-prd` | Analyst |
| System Design | `/skills:system-design` | Architect |
| Code Review | `/skills:code-review` | Developer |
| Test Strategy | `/skills:test-strategy` | QA |
| *(29 total — see agents/README.md)* | | |

### Available Checklists

| Checklist | Activation | Agent |
|-----------|-----------|-------|
| Phase Transition | `/checklists:phase-transition` | Orchestrator |
| Requirements Complete | `/checklists:requirements-complete` | Analyst |
| Architecture Ready | `/checklists:architecture-ready` | Architect |
| Implementation Done | `/checklists:implementation-done` | Developer |
| Release Ready | `/checklists:release-ready` | QA |
| UX Complete | `/checklists:ux-complete` | UX Designer |

### How the Agent System Works

- **Layer 0:** Session Protocol (always active — status, assemble, retrieve, extract)
- **Layer 1:** Agent Mode (optional — adds persona, rules, domain focus, skills)
- **Any agent can start first** — no required entry point
- **Agents retrieve skills on-demand** from Cortex (domain: METHODOLOGY)
- **Handoffs** are stored as memories, retrievable by the next agent
- All agents support `*help`, `*exit`, and `*context` commands
- Specs live in `agents/` (tool-agnostic) with thin wrappers in `.claude/commands/`

### When to Suggest Agents

- Requirements analysis → `/modes:analyst`
- System design or architectural decisions → `/modes:architect`
- Implementation, debugging, code review → `/modes:developer`
- Testing strategy, quality validation → `/modes:qa`
- UI/interaction design → `/modes:ux-designer`
- Complex multi-phase coordination → `/modes:orchestrator`

### Bootstrap

After adding or modifying agents/skills/templates, run bootstrap to make them retrievable:

```bash
python -m cli bootstrap          # Chunk agents/ into METHODOLOGY domain
python -m cli bootstrap --force  # Re-chunk (delete old + create new)
python -m cli index              # Rebuild indices
```

---

## Important Notes

- **Index Rebuild**: After adding chunks or memories, run `python -m cli index`
- **Stale Detection**: Status shows chunks from modified source files
- **Refresh Workflow**: Use `--refresh` flag to delete old chunks and re-chunk
- **Token Budget**: Context frames target ~8% of 200k context window
- **Position Optimization**: Critical info placed at start/end (primacy/recency zones)
- **Local Embeddings**: e5-small-v2 runs locally, no API costs
- **Cross-Platform**: Python CLI works on Windows, Mac, and Linux
- **No Time Estimates**: No agent produces duration predictions or timelines
