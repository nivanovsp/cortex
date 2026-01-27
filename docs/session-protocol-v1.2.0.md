# Cortex v1.2.0 - Session Protocol

> Solution Design Document

**Version:** 1.2.0
**Status:** Implemented
**Created:** 2026-01-27
**Based on:** v1.1.0 Semi-Auto Session Protocol

---

## Summary

v1.2.0 extends the Semi-Auto Session Protocol with:
- **Cross-platform Python CLI** - Commands work on Windows, Mac, Linux
- **Stale chunk awareness** - Agent reports outdated chunks at session start
- **Memory retrieval tracking** - Usage feedback loop now active

The core protocol (natural language triggers) remains unchanged from v1.1.0.

---

## What's New in v1.2.0

### 1. Python CLI Commands

All PowerShell scripts replaced with Python CLI:

| v1.1.0 (PowerShell) | v1.2.0 (Python) |
|---------------------|-----------------|
| `cortex-status.ps1` | `python -m cli status` |
| `cortex-assemble.ps1 -Task "X"` | `python -m cli assemble --task "X"` |
| `cortex-retrieve.ps1 -Query "X"` | `python -m cli retrieve --query "X"` |
| `cortex-extract.ps1 -Text "X"` | `python -m cli extract --text "X"` |
| `cortex-index.ps1` | `python -m cli index` |

### 2. Stale Chunk Detection

**Phase 1 Enhancement:** Status now reports stale chunks.

```
Agent Action: python -m cli status --json

Result includes:
- Chunk count and domains
- Memory count
- Index status
- **Stale chunks (NEW)** - Files that changed since chunking
```

**User Experience:** Agent mentions stale chunks if detected.

```
Agent: "Cortex is available. Note: 3 chunks from docs/api.md are stale
        (source file modified). You may want to refresh them."
```

### 3. Memory Retrieval Tracking

**Phase 2 Enhancement:** Memories now track usage.

When a memory is included in a context frame:
1. `retrieval_count` is incremented
2. `last_retrieved` timestamp is updated

This activates the frequency factor (10% weight) in retrieval scoring.

---

## Protocol Phases (Updated)

### Phase 1: Session Start (Automatic)

**Trigger:** Agent awakens / conversation begins

**Action:** Run `python -m cli status --json`

**Result:** Metadata (~50 tokens)
- Chunk count and domains
- Memory count
- Index status
- Stale chunks (v1.2.0)

**User Experience:**
- Agent greets and reports Cortex availability
- If stale chunks exist, agent mentions briefly
- No content loaded

### Phase 2: Task Identification (Automatic)

**Trigger:** User specifies task

**Detection Patterns:**
- "Let's work on {X}"
- "Help me with {X}"
- "I need to implement {X}"
- "Working on {X}"

**Action:** Run `python -m cli assemble --task "{detected task}"`

**Result:** Context frame (~2,500 tokens)
- Relevant chunks
- Relevant memories (retrieval tracked - v1.2.0)
- Position-optimized

**User Experience:** Agent has relevant context. No command visible.

### Phase 3: On-Demand Retrieval (Natural Language)

**Trigger:** User asks for information

**Detection Patterns:**
- "What do we know about {X}"
- "Get more details about {X}"
- "Tell me about {X}"
- "cortex: {X}" (explicit)

**Action:** Run `python -m cli retrieve --query "{X}"`

**Result:** Top relevant chunks (~1,500 tokens)

**User Experience:** Asked question, received answer. Transparent.

### Phase 4: Session End (User-Triggered)

**Trigger:** User requests learning extraction

**Detection Patterns:**
- "Update learning"
- "Save learnings"
- "End session"

**Action:**
1. Identify learnings from session
2. Run `python -m cli extract --text "{learnings}"`
3. Present proposed memories
4. User approves
5. Run `python -m cli index`

**User Experience:** Natural session closure with learning capture.

---

## Context Budget

| Phase | Tokens | % of 200k |
|-------|--------|-----------|
| Session start (metadata) | ~50 | 0.025% |
| Task assembly | ~2,500 | 1.25% |
| On-demand retrieval (×2) | ~3,000 | 1.5% |
| **Typical session** | **~5,550** | **~2.8%** |

*90%+ context remains for actual work.*

---

## Stale Chunk Workflow

When stale chunks are detected:

### Option 1: Continue Working
User can ignore stale chunks if changes are minor.

### Option 2: Refresh Before Work
```
User: "Let's refresh those stale chunks first"

Agent: [Runs python -m cli chunk --path docs/api.md --refresh]
Agent: [Runs python -m cli index]
Agent: "Chunks refreshed. Ready to work."
```

### Option 3: Refresh After Session
```
User: "Update learning and refresh stale chunks"

Agent: [Extracts learnings]
Agent: [Refreshes stale chunks]
Agent: [Rebuilds index]
```

---

## Migration from v1.1.0

No user-facing changes. The natural language interaction is identical.

Behind the scenes:
- Agent uses Python CLI instead of PowerShell
- Agent reports stale chunks at session start
- Memory retrieval is now tracked

---

## Version Comparison

| Feature | v1.1.0 | v1.2.0 |
|---------|--------|--------|
| Natural language triggers | ✓ | ✓ |
| Automatic context assembly | ✓ | ✓ |
| User-triggered learning | ✓ | ✓ |
| Cross-platform CLI | ✗ (Windows) | ✓ (All) |
| Stale chunk detection | ✗ | ✓ |
| Memory retrieval tracking | ✗ | ✓ |

---

*Cortex v1.2.0 - Session Protocol*
