# Cortex

**Complete Software Development Methodology with LLM-Native Context Management**

Cortex is a self-contained methodology for LLM-powered software development. It provides expert agents, structured skills, artifact templates, and semantic context retrieval — everything needed to go from requirements to delivered software without external dependencies.

**Version:** 2.0.0

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

### 1. Clone or Copy Cortex

```bash
# Clone the repository
git clone https://github.com/nivanovsp/cortex.git

# Or copy to your project
cp -r cortex/ your-project/
```

### 2. Install Dependencies

```bash
cd cortex
pip install -r requirements.txt
```

### 3. Add Global Claude Code Rules (Recommended)

For full Claude Code integration, add the Cortex rules to your global CLAUDE.md:

```bash
# View the rules to add
cat cortex/global/CLAUDE.md

# Then manually add to: ~/.claude/CLAUDE.md
```

Or copy the contents of `global/CLAUDE.md` and append to your `~/.claude/CLAUDE.md`.

### 4. Initialize in Your Project

```bash
cd your-project
python -m cli init
```

## Quick Start

```bash
# Initialize Cortex in your project
python -m cli init

# Chunk your documents
python -m cli chunk --path docs/

# Build the index
python -m cli index

# Build context frame for a task
python -m cli assemble --task "Implement user authentication"

# Check status (including stale chunks)
python -m cli status
```

## CLI Reference

### Core Operations

| Command | Purpose | Example |
|---------|---------|---------|
| `init` | Initialize Cortex in project | `python -m cli init` |
| `chunk` | Chunk documents into semantic units | `python -m cli chunk --path docs/` |
| `index` | Build/rebuild vector indices | `python -m cli index` |
| `retrieve` | Search for relevant context | `python -m cli retrieve --query "auth token"` |
| `assemble` | Build context frame for a task | `python -m cli assemble --task "Fix login"` |
| `status` | Show Cortex statistics | `python -m cli status` |

### Memory Management

| Command | Purpose | Example |
|---------|---------|---------|
| `memory add` | Create a memory | `python -m cli memory add --learning "X requires Y" --domain AUTH` |
| `memory list` | List all memories | `python -m cli memory list --domain AUTH` |
| `memory delete` | Delete a memory | `python -m cli memory delete MEM-2026-01-26-001` |

### Session & Extraction

| Command | Purpose | Example |
|---------|---------|---------|
| `extract` | Extract learnings from text | `python -m cli extract --text "Fixed by..."` |
| `status --json` | JSON output for automation | `python -m cli status --json` |

### Stale Chunk Management (v1.2.0)

| Command | Purpose | Example |
|---------|---------|---------|
| `status` | Shows stale chunks | `python -m cli status` |
| `chunk --refresh` | Refresh stale chunks | `python -m cli chunk --path file.md --refresh` |

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
├── .cortex/              # Cortex data (created by init)
│   ├── chunks/           # Chunked documents by domain
│   │   └── AUTH/         # Domain-specific chunks
│   ├── memories/         # Learnings from sessions
│   └── index/            # Vector indices
│       ├── chunks.pkl    # Chunk embeddings
│       └── memories.pkl  # Memory embeddings
├── cli/                  # Python CLI (cross-platform)
│   ├── main.py           # Typer app entry point
│   └── commands/         # Command implementations
├── core/                 # Python core modules
├── agents/               # Methodology resources (tool-agnostic)
│   ├── modes/            # Agent personas (6)
│   ├── skills/           # Workflow skills (29)
│   ├── checklists/       # Phase validation checklists (6)
│   └── templates/        # Artifact templates (14)
├── scripts/              # PowerShell CLI (deprecated)
├── templates/            # Chunk/memory templates
└── docs/                 # Documentation
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
- ~200MB disk space (for embedding model)

Install dependencies:
```bash
pip install -r requirements.txt
```

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

*Cortex v2.0.0 - Complete Software Development Methodology*
