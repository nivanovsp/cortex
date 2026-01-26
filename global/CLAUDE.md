# Cortex - Global CLAUDE.md Addition

> **Installation:** Add this section to your global `~/.claude/CLAUDE.md` file.
>
> This enables Claude Code to understand and use Cortex across all your projects.

---

## Cortex Context Management

**Semantic Retrieval System** - for projects using Cortex:

Cortex provides LLM-native context management through semantic search and position-optimized assembly.

### When to Use

| System | Best For |
|--------|----------|
| **Cortex** | Semantic retrieval, session learnings, context frames |
| **Neocortex/MLDA** | Knowledge graphs, document relationships, topic learning |
| **Both** | Large projects benefiting from both approaches |

### Quick Reference

```powershell
# Session start
.\scripts\cortex-status.ps1                    # Check state
.\scripts\cortex-assemble.ps1 -Task "..."      # Build context frame

# During session
.\scripts\cortex-retrieve.ps1 -Query "..."     # Search knowledge
.\scripts\cortex-memory.ps1 -Action add -Learning "..."  # Note learning

# Session end
.\scripts\cortex-extract.ps1 -Text "..." -AutoSave      # Extract learnings
.\scripts\cortex-index.ps1                              # Rebuild if added
```

### Memory Domains

| Domain | Scope |
|--------|-------|
| `AUTH` | Authentication, sessions, tokens |
| `UI` | Components, forms, styling |
| `API` | Endpoints, requests, responses |
| `DB` | Database, queries, migrations |
| `TEST` | Testing, fixtures, mocks |
| `DEV` | Build, deploy, tooling |
| `GENERAL` | Everything else |

### Memory Types

| Type | Use For |
|------|---------|
| `factual` | Stable knowledge ("API uses REST") |
| `experiential` | Lessons learned ("X requires Y") |
| `procedural` | How-to ("Always do X before Y") |

### Context Frame Budget

Cortex assembles context frames targeting ~8% of context window:

| Section | Purpose | Position |
|---------|---------|----------|
| Task Definition | What to do | TOP (primacy) |
| Relevant Knowledge | Retrieved chunks | Middle |
| Past Learnings | Retrieved memories | Middle |
| Current State | Recent progress | BOTTOM (recency) |
| Instructions | How to proceed | VERY END |

### Integration with Beads

When using both Cortex and Beads:
1. `bd ready` to see tasks
2. `cortex-assemble -Task "task description"` for context
3. Work on task
4. `cortex-extract` to capture learnings
5. `bd close` when complete

### Key Principles

- **Position matters**: Critical info at start/end (LLM attention is U-shaped)
- **Chunk, don't load**: Retrieve only relevant ~500 token chunks
- **Capture learnings**: Extract memories at session end
- **Rebuild after changes**: Run `cortex-index.ps1` after adding content

---
