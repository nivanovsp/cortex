# Cortex User Guide

A comprehensive guide to using Cortex for LLM-native context management.

**Version:** 2.1.0

## Table of Contents

1. [Getting Started](#getting-started)
2. [Natural Language Usage](#natural-language-usage)
3. [Agent System](#agent-system) **(Updated in v2.0.0)**
4. [Document Management](#document-management)
5. [Stale Chunk Detection](#stale-chunk-detection)
6. [Memory System](#memory-system)
7. [Context Assembly](#context-assembly)
8. [Session Workflow](#session-workflow)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Quick Setup (with Claude Code)

1. **One-time:** Copy `global/CLAUDE.md` to `~/.claude/CLAUDE.md`
2. **In any project folder:** Say "cortex init"

The agent handles everything automatically.

### Manual Setup

1. **Prerequisites**
   - Python 3.8+
   - Git
   - ~200MB disk space for embedding model

2. **Clone Engine**
   ```bash
   git clone https://github.com/nivanovsp/cortex.git .cortex-engine
   ```

3. **Install Dependencies**
   ```bash
   pip install -r .cortex-engine/requirements.txt
   ```

4. **Copy Methodology Files**
   ```bash
   cp -r .cortex-engine/agents ./agents
   cp -r .cortex-engine/.claude ./.claude
   cp .cortex-engine/CLAUDE.md ./CLAUDE.md
   ```

5. **Initialize and Bootstrap**
   ```bash
   cd .cortex-engine && python -m cli init --root ..
   cd .cortex-engine && python -m cli bootstrap --root ..
   cd .cortex-engine && python -m cli index --root ..
   ```

6. **Verify**
   ```bash
   cd .cortex-engine && python -m cli status --root ..
   ```

### First Steps

---

## Natural Language Usage

You don't need to run CLI commands directly. Just talk naturally to the agent, and it handles Cortex automatically.

### How It Works

| What You Say | What Happens |
|--------------|--------------|
| "Let's work on authentication" | Agent automatically retrieves relevant context |
| "What do we know about tokens?" | Agent searches for token-related knowledge |
| "Update learning" | Agent extracts and proposes memories to save |

### Session Flow (Natural Language)

**1. Start a Session**

Just start talking. The agent automatically checks Cortex status.

**2. Specify Your Task**

Say things like:
- "Let's work on the login page"
- "I need to implement password reset"
- "Help me with the API endpoints"
- "Working on user authentication"

The agent automatically builds a context frame with relevant chunks and memories.

**3. Ask for More Context**

If you need more information during work:
- "What do we know about session tokens?"
- "Get more details about the auth flow"
- "Tell me about error handling"
- "Remind me how the API works"

Or use the explicit trigger: `cortex: JWT validation`

**4. End the Session**

When you're done, say:
- "Update learning"
- "Save learnings"
- "Wrap up and save"

The agent will:
1. Identify learnings from the session
2. Propose memories with confidence levels
3. Ask which to save
4. Rebuild the index

### Natural Language Trigger Reference

| Phrase Pattern | What It Does |
|----------------|--------------|
| "Let's work on {X}" | Builds context frame for task X |
| "Help me with {X}" | Builds context frame for task X |
| "What do we know about {X}" | Retrieves information about X |
| "Tell me about {X}" | Retrieves information about X |
| "Get details on {X}" | Retrieves information about X |
| "cortex: {X}" | Explicit retrieval for X |
| "Update learning" | Extracts session learnings |
| "Save learnings" | Extracts session learnings |

---

## Agent System

**(Updated in v2.0.0)** Cortex is a complete software development methodology with 6 specialist agents, each with dedicated skills, templates, and a quality checklist.

### Available Agents

| Agent | What It Does | Activate |
|-------|-------------|----------|
| **Analyst** | Requirements analysis, gap identification, acceptance criteria | `/modes:analyst` |
| **Architect** | System design, trade-off analysis, ADRs, NFRs | `/modes:architect` |
| **Developer** | Implementation, debugging, code review | `/modes:developer` |
| **QA** | Test strategy, quality gates, acceptance review | `/modes:qa` |
| **UX Designer** | Interface design, accessibility, user flows | `/modes:ux-designer` |
| **Orchestrator** | Work planning, phase coordination, handoffs | `/modes:orchestrator` |

### Any Agent Can Start First

There is no required entry point. Start with whichever agent fits your task:

- Have vague requirements? → `/modes:analyst`
- Know what to build but not how? → `/modes:architect`
- Ready to code? → `/modes:developer`
- Need to validate? → `/modes:qa`

### Using Agents

**With Claude Code:**
```
/modes:architect
```

**With other LLM tools:**
```
Read agents/modes/architect.md and adopt that persona fully.
```

### How Agents Work

Agents add a specialist lens on top of the normal session protocol:

```
Without agent:
  You talk → Cortex retrieves context → Generic answer

With /modes:architect:
  You talk → Cortex retrieves context → Architect answer
  (design focus, trade-offs, rules enforced)
```

Each agent has:
- **Rules** — Hard constraints (e.g., Developer must verify library versions are current)
- **Skills** — Invoke via `/skills:{name}` for structured workflows
- **Templates** — Produce standardized artifacts
- **Checklist** — Validate before concluding work

### Skills (29 total)

Skills are one-shot workflows. Invoke with `/skills:{name}`:

| Agent | Skills Available |
|-------|-----------------|
| Orchestrator | project-plan, phase-decomposition, handoff, progress-review, risk-assessment |
| Analyst | elicit-requirements, create-prd, gap-analysis, define-acceptance-criteria, stakeholder-analysis |
| Architect | system-design, api-design, nfr-assessment, create-adr, tech-evaluation, security-review |
| Developer | implementation-plan, code-review, debug-workflow, refactor-assessment |
| QA | test-strategy, test-case-design, quality-gate, acceptance-review, accessibility-review |
| UX Designer | wireframe, user-flow, design-system, usability-review |
| Shared | qa-gate, extract-learnings |

### Checklists

Run before concluding a phase: `/checklists:{name}`

| Checklist | Agent | Purpose |
|-----------|-------|---------|
| phase-transition | Orchestrator | Verify deliverables before moving on |
| requirements-complete | Analyst | Validate requirements are complete and clear |
| architecture-ready | Architect | Confirm design is ready for implementation |
| implementation-done | Developer | Verify code is complete and tested |
| release-ready | QA | Final quality validation |
| ux-complete | UX Designer | Confirm UX deliverables |

### Example Workflows

**With Orchestrator:**
```
1. /modes:orchestrator     → Produce phased plan
2. /skills:handoff         → Transition to next phase
3. /modes:analyst          → Clarify requirements
4. /skills:handoff         → Transition
5. /modes:architect        → Design solution
6. /modes:developer        → Implement
7. /modes:qa               → Validate quality
```

**Self-Orchestrated:**
```
1. /modes:analyst          → Start with requirements
2. /modes:architect        → Design solution
3. /modes:developer        → Implement
4. /skills:qa-gate         → Quick quality check
```

---

### When to Use CLI Directly

Most users won't need to run commands. However, you can use them for:
- Initial setup (`cd .cortex-engine && python -m cli init --root ..`)
- Bulk document chunking (`cd .cortex-engine && python -m cli chunk --path docs/ --root ..`)
- Refreshing stale chunks (`cd .cortex-engine && python -m cli chunk --path file.md --refresh --root ..`)
- Debugging (`cd .cortex-engine && python -m cli status --json --root ..`)

---

### First Steps (Manual)

All CLI commands run from `.cortex-engine/` with `--root ..`:

1. **Chunk your documentation**
   ```bash
   cd .cortex-engine && python -m cli chunk --path docs/ --root ..
   ```

2. **Build the search index**
   ```bash
   cd .cortex-engine && python -m cli index --root ..
   ```

3. **Test retrieval**
   ```bash
   cd .cortex-engine && python -m cli retrieve --query "authentication" --root ..
   ```

---

## Document Management

### Chunking Documents

Cortex breaks documents into ~500 token semantic units for efficient retrieval.

**Chunk a single file:**
```bash
python -m cli chunk --path docs/api-spec.md
```

**Chunk a directory:**
```bash
python -m cli chunk --path docs/
```

**Override domain detection:**
```bash
python -m cli chunk --path docs/auth.md --domain AUTH
```

**Refresh chunks (delete old, create new):**
```bash
python -m cli chunk --path docs/api-spec.md --refresh
```

### Domain Detection

Cortex auto-detects domains from file paths:

| Path | Detected Domain |
|------|-----------------|
| `docs/auth/login.md` | AUTH |
| `docs/auth-spec.md` | AUTH |
| `docs/readme.md` | GENERAL |

### After Chunking

Always rebuild the index after adding chunks:
```bash
python -m cli index
```

---

## Stale Chunk Detection

**(New in v1.2.0)** Cortex tracks source file changes and alerts you when chunks are stale.

### How It Works

Each chunk stores:
- `source_path` - The original file path
- `source_hash` - SHA256 hash of file content at chunk time

When you run `status`, Cortex compares stored hashes with current files.

### Checking for Stale Chunks

```bash
python -m cli status
```

Output shows stale chunks if any exist:
```
Cortex Status
=============
Status: INITIALIZED

Chunks: 15 total
  - CORTEX: 15

Stale Chunks:
  - docs/architecture.md (5 chunks, modified)

  Refresh with: python -m cli chunk --path <source> --refresh
```

### Refreshing Stale Chunks

```bash
# Refresh a single file
python -m cli chunk --path docs/architecture.md --refresh

# Rebuild index after refresh
python -m cli index
```

The `--refresh` flag:
1. Finds all chunks from the source file
2. Deletes them
3. Creates new chunks from current file content

---

## Memory System

Memories are atomic learnings that persist across sessions.

### Memory Types

| Type | Use For | Example |
|------|---------|---------|
| **Factual** | Stable knowledge | "API returns JSON with camelCase keys" |
| **Experiential** | Lessons learned | "FormField wrapper required for inputs" |
| **Procedural** | How-to knowledge | "Run tests before committing" |

### Creating Memories

**Basic:**
```bash
python -m cli memory add --learning "API requires auth header"
```

**With all options:**
```bash
python -m cli memory add \
    --learning "FormField wrapper is required for PasswordInput" \
    --context "Discovered when component threw runtime error" \
    --type experiential \
    --domain UI \
    --confidence high
```

### Listing Memories

**All memories:**
```bash
python -m cli memory list
```

**Filter by domain:**
```bash
python -m cli memory list --domain AUTH
```

**JSON output:**
```bash
python -m cli memory list --json
```

### Deleting Memories

```bash
python -m cli memory delete MEM-2026-01-26-001
```

---

## Context Assembly

Context frames combine relevant chunks and memories for LLM consumption.

### Basic Assembly

```bash
python -m cli assemble --task "Implement user authentication"
```

### Custom Budget

```bash
python -m cli assemble --task "Quick fix" --budget 5000
```

### Save to File

```bash
python -m cli assemble --task "Implement feature" --output context.md
```

### Context Frame Structure

The assembled context is position-optimized:

```
TOP (high attention)
├── Task Definition
├── Acceptance Criteria
│
MIDDLE (lower attention)
├── Relevant Knowledge (chunks)
├── Past Learnings (memories)
│
BOTTOM (high attention)
├── Current State
└── Instructions
```

---

## Session Workflow

### Natural Language Flow (Recommended - v1.1.0)

```
┌─────────────────────────────────────────────────────┐
│                  SESSION START                       │
├─────────────────────────────────────────────────────┤
│  Just start talking - agent checks Cortex status    │
│  "Let's work on {your task}"                        │
│  → Agent automatically builds context frame         │
├─────────────────────────────────────────────────────┤
│                  DURING SESSION                      │
├─────────────────────────────────────────────────────┤
│  "What do we know about {topic}?"                   │
│  → Agent automatically retrieves relevant info      │
├─────────────────────────────────────────────────────┤
│                  SESSION END                         │
├─────────────────────────────────────────────────────┤
│  "Update learning"                                   │
│  → Agent extracts, proposes, and saves memories     │
└─────────────────────────────────────────────────────┘
```

### Manual CLI Flow (Advanced)

```
┌─────────────────────────────────────────────────────┐
│                  SESSION START                       │
├─────────────────────────────────────────────────────┤
│  1. python -m cli status     # Check state          │
│  2. python -m cli assemble   # Build context        │
├─────────────────────────────────────────────────────┤
│                  DURING SESSION                      │
├─────────────────────────────────────────────────────┤
│  • python -m cli retrieve    # Search as needed     │
│  • python -m cli memory add  # Note learnings       │
├─────────────────────────────────────────────────────┤
│                  SESSION END                         │
├─────────────────────────────────────────────────────┤
│  1. python -m cli extract    # Extract learnings    │
│  2. python -m cli index      # Rebuild if added     │
└─────────────────────────────────────────────────────┘
```

### Extracting Learnings

**From text:**
```bash
python -m cli extract --text "Fixed by adding null check. Found that X requires Y."
```

**Auto-save all extracted:**
```bash
python -m cli extract --text "..." --auto-save
```

---

## Best Practices

### Document Organization

1. **Use descriptive file names** - `auth-token-refresh.md` not `doc1.md`
2. **Organize by domain** - `docs/auth/`, `docs/api/`, etc.
3. **Keep documents focused** - One topic per document
4. **Use markdown headers** - Helps semantic chunking

### Memory Hygiene

1. **Be specific** - "FormField required for PasswordInput" not "wrapper needed"
2. **Include context** - When/why you learned this
3. **Set appropriate confidence** - High only for verified facts
4. **Review periodically** - Delete outdated memories

### Context Assembly

1. **Write clear task descriptions** - Be specific about what you're doing
2. **Include acceptance criteria** - Helps focus the context
3. **Use appropriate budgets** - Smaller for simple tasks
4. **Review the frame** - Check it includes relevant content

### Performance Tips

1. **Rebuild index after bulk changes** - Not after every single addition
2. **Use domain filters** - Narrow searches when possible
3. **Keep chunks reasonable** - Don't chunk massive files unnecessarily
4. **Refresh stale chunks** - Use `--refresh` flag when source files change

---

## Troubleshooting

### Common Issues

**"No chunks found"**
- Did you run `python -m cli chunk --path docs/`?
- Did you run `python -m cli index` after chunking?

**"Index not found"**
```bash
python -m cli index
```

**"Stale chunks detected"**
```bash
# View stale chunks
python -m cli status

# Refresh specific file
python -m cli chunk --path docs/file.md --refresh
python -m cli index
```

**Retrieval returns irrelevant results**
- Try more specific queries
- Check that relevant documents are chunked
- Rebuild index: `python -m cli index`

**Memory extraction finds nothing**
- Text may not match extraction patterns
- Add memories manually: `python -m cli memory add --learning "..."`

**Slow embedding**
- First run downloads model (~130MB)
- Subsequent runs should be fast
- Model is cached at `~/.cache/huggingface/`

### Checking System State

```bash
# Full status
python -m cli status

# JSON output for debugging
python -m cli status --json
```

### Rebuilding Everything

If something is corrupted:

```bash
# Remove indices (keeps chunks and memories)
rm -rf .cortex/index/*

# Rebuild
python -m cli index
```

### Getting Help

- Check `docs/cortex-spec.md` for full technical details
- Check `docs/architecture.md` for system design
- Check `CLAUDE.md` for Claude Code specific guidance
- Check `agents/README.md` for agent mode documentation
