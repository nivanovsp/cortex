# Cortex - Claude Code Instructions

> **Inherits from:** `~/.claude/CLAUDE.md` (Global Rules)
>
> All global rules, protocols, and conventions apply. This file contains project-specific additions.

---

## Project Overview

**Cortex** is an LLM-native context management system. It optimizes how documentation and learnings are stored, retrieved, and assembled for LLM consumption.

**Version:** 1.1.0

---

## Session Protocol (v1.1.0)

This protocol defines how you (the agent) interact with Cortex throughout a session. Follow these instructions automatically — users should not need to know about scripts.

### On Session Start (Automatic)

When the conversation begins:

1. Run `.\scripts\cortex-status.ps1` silently
2. Note the result internally (chunk count, memory count, domains, index status)
3. **DO NOT** load any content files — wait for task identification
4. Greet the user and mention Cortex is available if relevant

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
2. Run `.\scripts\cortex-assemble.ps1 -Task "{extracted task}"`
3. Use the returned context frame to inform your work
4. **DO NOT** mention the script to the user — just have the context

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
2. Run `.\scripts\cortex-retrieve.ps1 -Query "{topic}"`
3. Present the information naturally
4. **DO NOT** mention the script — just answer their question

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
2. Run `.\scripts\cortex-extract.ps1 -Text "{learnings summary}"`
3. Present proposed memories to the user with confidence levels
4. Ask which memories to save
5. Save approved memories
6. Run `.\scripts\cortex-index.ps1` to rebuild the index

### Context Budget

| Phase | Tokens | % of 200k |
|-------|--------|-----------|
| Session start (metadata) | ~50 | 0.025% |
| Task assembly | ~2,500 | 1.25% |
| On-demand retrieval (×2) | ~3,000 | 1.5% |
| **Typical session total** | **~5,550** | **~2.8%** |

**97%+ of context remains available for actual work.**

### Important Rules

1. **Never pre-load content files** — use retrieval only
2. **Scripts are invisible to users** — they interact through natural language
3. **Session end requires user trigger** — never auto-extract learnings
4. **When uncertain, use explicit trigger** — "cortex: {query}" always works

---

## Project Structure

```
Cortex/
├── core/                 # Python modules
│   ├── config.py         # Configuration
│   ├── embedder.py       # e5-small-v2 wrapper
│   ├── chunker.py        # Document chunking
│   ├── indexer.py        # Vector index management
│   ├── retriever.py      # Semantic search
│   ├── memory.py         # Memory CRUD
│   ├── assembler.py      # Context frame assembly
│   └── extractor.py      # Memory extraction
├── scripts/              # PowerShell CLI
├── docs/                 # Documentation
├── templates/            # Chunk/memory templates
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
2. CLI interface in `scripts/` as PowerShell
3. Update `core/__init__.py` to export new functions
4. Add tests and documentation

### Modifying Chunking/Embedding
- Chunk size: 500 tokens max (matches e5-small-v2)
- Overlap: 50 tokens for continuity
- Always rebuild index after changes: `.\scripts\cortex-index.ps1`

### Environment Variables
All optional - defaults work out of the box:
- `CORTEX_EMBEDDING_MODEL` - Default: `intfloat/e5-small-v2`
- `CORTEX_CHUNK_SIZE` - Default: `500`
- `CORTEX_TOKEN_BUDGET` - Default: `15000`

---

## Script Reference (Internal)

These scripts are called automatically by the session protocol. Users should not need to invoke them directly.

| Script | Purpose | When Called |
|--------|---------|-------------|
| `cortex-status.ps1` | Get system metadata | Session start |
| `cortex-assemble.ps1 -Task "..."` | Build context frame | Task identified |
| `cortex-retrieve.ps1 -Query "..."` | Search for context | User asks for info |
| `cortex-extract.ps1 -Text "..."` | Extract learnings | User ends session |
| `cortex-index.ps1` | Rebuild indices | After saving memories |
| `cortex-memory.ps1 -Action add` | Add memory manually | Explicit request |
| `cortex-init.ps1` | Initialize Cortex | Project setup |
| `cortex-chunk.ps1 -Path "..."` | Chunk documents | Adding new docs |

---

## Important Notes

- **Index Rebuild**: After adding chunks or memories, run `cortex-index.ps1`
- **Token Budget**: Context frames target ~8% of 200k context window
- **Position Optimization**: Critical info placed at start/end (primacy/recency zones)
- **Local Embeddings**: e5-small-v2 runs locally, no API costs
