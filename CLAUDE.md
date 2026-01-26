# Cortex - Claude Code Instructions

> **Inherits from:** `~/.claude/CLAUDE.md` (Global Rules)
>
> All global rules, protocols, and conventions apply. This file contains project-specific additions.

---

## Project Overview

**Cortex** is an LLM-native context management system. It optimizes how documentation and learnings are stored, retrieved, and assembled for LLM consumption.

## Key Commands

### Session Start
```powershell
# Check Cortex status
.\scripts\cortex-status.ps1

# Build context for your task
.\scripts\cortex-assemble.ps1 -Task "Your task description"
```

### During Session
```powershell
# Search for relevant knowledge
.\scripts\cortex-retrieve.ps1 -Query "topic you need"

# Add a memory on the fly
.\scripts\cortex-memory.ps1 -Action add -Learning "What you learned" -Domain DOMAIN
```

### Session End
```powershell
# Extract learnings from session
.\scripts\cortex-extract.ps1 -Text "paste session notes or key learnings"

# Or auto-save high-confidence memories
.\scripts\cortex-extract.ps1 -Text "..." -AutoSave

# Rebuild index if you added memories
.\scripts\cortex-index.ps1
```

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

## Important Notes

- **Index Rebuild**: After adding chunks or memories, run `cortex-index.ps1`
- **Token Budget**: Context frames target ~8% of 200k context window
- **Position Optimization**: Critical info placed at start/end (primacy/recency zones)
- **Local Embeddings**: e5-small-v2 runs locally, no API costs

## Quick Reference

| Task | Command |
|------|---------|
| Initialize | `.\scripts\cortex-init.ps1` |
| Chunk docs | `.\scripts\cortex-chunk.ps1 -Path "docs/"` |
| Build index | `.\scripts\cortex-index.ps1` |
| Search | `.\scripts\cortex-retrieve.ps1 -Query "..."` |
| Context frame | `.\scripts\cortex-assemble.ps1 -Task "..."` |
| Add memory | `.\scripts\cortex-memory.ps1 -Action add -Learning "..."` |
| List memories | `.\scripts\cortex-memory.ps1 -Action list` |
| Extract learnings | `.\scripts\cortex-extract.ps1 -Text "..."` |
| Status | `.\scripts\cortex-status.ps1` |
