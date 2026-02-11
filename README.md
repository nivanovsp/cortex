# Cortex

**Complete Software Development Methodology with LLM-Native Context Management**

Cortex is a self-contained methodology for LLM-powered software development. It provides expert agents, structured skills, artifact templates, and semantic context retrieval — everything needed to go from requirements to delivered software without external dependencies.

**Version:** 2.3.0

## Key Features

- **Complete methodology** - 6 agents, 29 skills, 14 templates, 6 checklists **(New in v2.0.0)**
- **Decentralized orchestration** - Start with any agent, no required entry point **(New in v2.0.0)**
- **Agent-specific rules** - Hard constraints per agent (no deprecated libs, no assumptions, no time estimates) **(New in v2.0.0)**
- **Handoff protocol** - Structured phase transitions stored as retrievable memories **(New in v2.0.0)**
- **Self-indexing methodology** - Skills/templates chunked into Cortex for on-demand retrieval **(New in v2.0.0)**
- **Natural language interaction** - Just talk, agent handles commands automatically
- **Cross-platform CLI** - Python-based, works on Windows, Mac, Linux
- **~3-10% context consumption** - Retrieval-based loading (vs 30%+ for full docs)
- **Position-aware assembly** - Critical info where LLMs pay attention
- **Semantic retrieval** - Find relevant content via similarity, not manual links
- **Memory system** - Capture and reuse learnings across sessions
- **Local embeddings** - Free, no API costs, works offline

## Installation

### Quick Setup (with Claude Code)

1. **One-time:** Copy `global/CLAUDE.md` to `~/.claude/CLAUDE.md`
2. **In any project folder:** Say "cortex init"

That's it. The agent clones the repo, creates an isolated venv, installs dependencies, copies files, and bootstraps everything.

### Manual Setup

```bash
# Clone engine into your project
git clone https://github.com/nivanovsp/cortex.git .cortex-engine

# Create isolated venv and install dependencies
# Windows:
python -m venv .cortex-engine/.venv
.cortex-engine/.venv/Scripts/pip install -r .cortex-engine/requirements.txt
# Unix:
python -m venv .cortex-engine/.venv
.cortex-engine/.venv/bin/pip install -r .cortex-engine/requirements.txt

# Copy methodology files
cp -r .cortex-engine/agents ./agents
cp -r .cortex-engine/.claude ./.claude
cp .cortex-engine/CLAUDE.md ./CLAUDE.md

# Initialize, bootstrap, and index (use venv python)
# Windows: replace `python` with `.venv/Scripts/python`
# Unix: replace `python` with `.venv/bin/python`
cd .cortex-engine && .venv/bin/python -m cli init --root ..
cd .cortex-engine && .venv/bin/python -m cli bootstrap --root ..
cd .cortex-engine && .venv/bin/python -m cli index --root ..

# Copy global rules (one-time)
# Windows: copy .cortex-engine\global\CLAUDE.md %USERPROFILE%\.claude\CLAUDE.md
# Mac/Linux: cp .cortex-engine/global/CLAUDE.md ~/.claude/CLAUDE.md
```

See [INSTALL.md](INSTALL.md) for full details.

## Quick Start

```bash
# All CLI commands run from .cortex-engine/ using the venv python
cd .cortex-engine

# Use the venv python (replace with .venv/Scripts/python on Windows)
# Chunk your documents
.venv/bin/python -m cli chunk --path docs/ --root ..

# Build the index
.venv/bin/python -m cli index --root ..

# Build context frame for a task
.venv/bin/python -m cli assemble --task "Implement user authentication" --root ..

# Check status (including stale chunks and venv isolation)
.venv/bin/python -m cli status --root ..
```

## CLI Reference

All commands run from `.cortex-engine/` using the venv python with `--root ..`:

```bash
# Unix:
cd .cortex-engine && .venv/bin/python -m cli <command> --root ..
# Windows:
cd .cortex-engine && .venv/Scripts/python -m cli <command> --root ..
```

### Core Operations

| Command | Purpose |
|---------|---------|
| `init --root ..` | Initialize Cortex in project |
| `chunk --path docs/ --root ..` | Chunk documents |
| `chunk --path file.md --refresh --root ..` | Refresh stale chunks |
| `index --root ..` | Build/rebuild vector indices |
| `retrieve --query "auth token" --root ..` | Search for context |
| `assemble --task "Fix login" --root ..` | Build context frame |
| `status --root ..` | Show Cortex statistics |
| `bootstrap --root ..` | Chunk methodology into Cortex |

### Memory Management

| Command | Purpose |
|---------|---------|
| `memory add --learning "X requires Y" --domain AUTH --root ..` | Create a memory |
| `memory list --domain AUTH --root ..` | List memories |
| `memory delete MEM-ID --root ..` | Delete a memory |

### Session & Extraction

| Command | Purpose |
|---------|---------|
| `extract --text "Fixed by..." --root ..` | Extract learnings |
| `status --json --root ..` | JSON output for automation |

## Claude Code Integration

### Natural Language Workflow (v1.1.0)

**No scripts required!** Just talk naturally:

| You Say | What Happens |
|---------|--------------|
| "Let's work on user authentication" | Agent builds context automatically |
| "What do we know about tokens?" | Agent retrieves relevant info |
| "Update learning" | Agent extracts and saves memories |

### Example Session

```
You: "Let's work on the password reset feature"
     → Agent automatically loads relevant context

You: "What do we know about email templates?"
     → Agent retrieves email-related chunks

You: "Update learning"
     → Agent proposes memories to save from session
```

### Manual Workflow (Advanced)

For power users who prefer direct CLI control:

1. **Session Start**: Check status and build context
   ```bash
   python -m cli status
   python -m cli assemble --task "Your task description"
   ```

2. **During Session**: Query for specific knowledge
   ```bash
   python -m cli retrieve --query "relevant topic"
   ```

3. **Session End**: Extract and save learnings
   ```bash
   python -m cli extract --text "Session notes"
   ```

### Memory Types

| Type | Description | Example |
|------|-------------|---------|
| **Factual** | Stable knowledge | "API uses REST with JSON responses" |
| **Experiential** | Lessons learned | "FormField wrapper required for PasswordInput" |
| **Procedural** | How to do something | "Run tests before committing" |

### Confidence Levels

| Level | When Assigned | Auto-Save |
|-------|---------------|-----------|
| **High** | Verified fixes, explicit "remember this" | Yes (with `-AutoSave`) |
| **Medium** | Reasonable inference, discoveries | No |
| **Low** | Uncertain, needs verification | No |

## Agent System

Cortex ships with 6 expert agents, each with dedicated skills, templates, and a quality checklist. **Any agent can be your starting point.**

### Agents

| Agent | Focus | Activation |
|-------|-------|-----------|
| **Analyst** | Requirements, gap analysis, acceptance criteria | `/modes:analyst` |
| **Architect** | System design, trade-offs, ADRs, NFRs | `/modes:architect` |
| **Developer** | Implementation, debugging, code review | `/modes:developer` |
| **QA** | Test strategy, quality gates, acceptance review | `/modes:qa` |
| **UX Designer** | Interface design, accessibility, user flows | `/modes:ux-designer` |
| **Orchestrator** | Work planning, phase coordination, handoffs | `/modes:orchestrator` |

### Skills (29 total)

| Agent | Skills |
|-------|--------|
| Orchestrator | project-plan, phase-decomposition, handoff, progress-review, risk-assessment |
| Analyst | elicit-requirements, create-prd, gap-analysis, define-acceptance-criteria, stakeholder-analysis |
| Architect | system-design, api-design, nfr-assessment, create-adr, tech-evaluation, security-review |
| Developer | implementation-plan, code-review, debug-workflow, refactor-assessment |
| QA | test-strategy, test-case-design, quality-gate, acceptance-review, accessibility-review |
| UX Designer | wireframe, user-flow, design-system, usability-review |
| Shared | qa-gate, extract-learnings |

### Checklists

| Checklist | Agent | Purpose |
|-----------|-------|---------|
| phase-transition | Orchestrator | Verify phase deliverables before transition |
| requirements-complete | Analyst | Validate requirement completeness |
| architecture-ready | Architect | Confirm design readiness |
| implementation-done | Developer | Verify code completeness |
| release-ready | QA | Final quality validation |
| ux-complete | UX Designer | Confirm UX deliverables |

### With Claude Code

Agents are available as slash commands:

```
/modes:analyst         → Elicit and document requirements
/modes:architect       → Design the solution
/modes:developer       → Implement it
/modes:qa              → Validate quality
/skills:handoff        → Transition to next phase
```

### With Other LLM Tools

Point your tool at the spec file in `agents/modes/`:

```
Read agents/modes/architect.md and adopt that persona fully.
Follow all instructions for the remainder of this conversation.
```

See [agents/README.md](agents/README.md) for full documentation.

## How It Works

```
┌─────────────────────────────────────────────────────┐
│                    CORTEX FLOW                       │
├─────────────────────────────────────────────────────┤
│                                                      │
│  Documents ──► Chunker ──► Embeddings ──► Index     │
│                                                      │
│  Task ──► Query Embed ──► Similarity ──► Retrieve   │
│                                                      │
│  Retrieved ──► Assembler ──► Context Frame ──► LLM  │
│                                                      │
│  Session ──► Extractor ──► Proposed ──► Memories    │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Position-Aware Assembly

Based on "lost in middle" research, Cortex places critical information where LLMs pay most attention:

```
Context Frame Structure:
─────────────────────────────────────
TOP (primacy zone)     → Task Definition
UPPER-MIDDLE           → Relevant Knowledge
LOWER-MIDDLE           → Past Learnings
BOTTOM (recency zone)  → Current State
VERY END               → Instructions
─────────────────────────────────────
```

## Project Structure

```
your-project/
├── .cortex-engine/       # Cloned Cortex repo (engine)
│   ├── .venv/            # Isolated Python venv (Cortex deps only)
│   ├── cli/              # Python CLI
│   ├── core/             # Python core modules
│   ├── tests/            # Test suite (69 tests)
│   └── ...               # Full Cortex repo
├── .cortex/              # Runtime data (created by init)
│   ├── chunks/           # Chunked documents by domain
│   ├── memories/         # Learnings from sessions
│   └── index/            # Vector indices
├── .claude/commands/     # Slash commands (copied from engine)
├── agents/               # Methodology resources (copied from engine)
│   ├── modes/            # Agent personas (6)
│   ├── skills/           # Workflow skills (32)
│   ├── checklists/       # Phase validation checklists (6)
│   └── templates/        # Artifact templates (14)
├── CLAUDE.md             # Project-level instructions (copied)
└── (your project files)
```

## Configuration

Environment variables (all optional, defaults work out of the box):

| Variable | Default | Description |
|----------|---------|-------------|
| `CORTEX_EMBEDDING_MODEL` | `intfloat/e5-small-v2` | Embedding model |
| `CORTEX_CHUNK_SIZE` | `500` | Max tokens per chunk |
| `CORTEX_CHUNK_OVERLAP` | `50` | Overlap between chunks |
| `CORTEX_RETRIEVAL_TOP_K` | `10` | Chunks to retrieve |
| `CORTEX_MEMORY_TOP_K` | `5` | Memories to retrieve |
| `CORTEX_TOKEN_BUDGET` | `15000` | Context frame budget |

## Requirements

- Python 3.8+
- ~200MB disk space (for embedding model + venv)

Dependencies are installed into an isolated venv at `.cortex-engine/.venv/` — they do not affect your project's own Python environment.

Dependencies:
- `sentence-transformers` - Local embeddings
- `numpy` - Vector operations
- `tiktoken` - Token counting
- `typer` - CLI framework
- `rich` - Terminal formatting

## Documentation

- [User Guide](docs/user-guide.md) - Getting started and usage
- [Full Specification](docs/cortex-spec.md) - Complete technical details
- [Architecture](docs/architecture.md) - System design
- [Decisions](docs/decisions.md) - Architecture decision records
- [Agent Modes](agents/README.md) - Agent system documentation
- [Changelog](CHANGELOG.md) - Version history

---

*Cortex v2.3.0 - Complete Software Development Methodology*
