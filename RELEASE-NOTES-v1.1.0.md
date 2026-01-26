# Cortex v1.1.0 Release Notes

**Release Date:** 2026-01-26

---

## Overview

Cortex v1.1.0 introduces the **Semi-Auto Session Protocol** — a major UX improvement that enables natural language interaction with Cortex. Users no longer need to know or run scripts directly; they simply talk to the agent, and Cortex operations happen automatically.

---

## What's New

### Natural Language Interaction

**Before (v1.0.0):**
```powershell
.\scripts\cortex-assemble.ps1 -Task "implement password reset"
.\scripts\cortex-retrieve.ps1 -Query "email templates"
.\scripts\cortex-extract.ps1 -Text "session notes..."
```

**After (v1.1.0):**
```
You: "Let's work on the password reset feature"
     → Context automatically loaded

You: "What do we know about email templates?"
     → Relevant information retrieved

You: "Update learning"
     → Memories extracted and saved
```

### Semi-Auto Session Protocol

The protocol defines four phases:

| Phase | Trigger | What Happens |
|-------|---------|--------------|
| **Start** | Session begins | Agent loads metadata (~50 tokens) |
| **Task** | "Let's work on X" | Agent builds context frame (~2,500 tokens) |
| **Retrieval** | "What do we know about X" | Agent retrieves relevant chunks |
| **End** | "Update learning" | Agent extracts and proposes memories |

### Improved Context Efficiency

| Metric | v1.0.0 | v1.1.0 |
|--------|--------|--------|
| Typical session context | ~8% | **~2.8%** |
| Session start overhead | Variable | ~50 tokens |
| Task context | Variable | ~2,500 tokens |

---

## New Features

### Natural Language Triggers

**Task Identification:**
- "Let's work on {X}"
- "I need to {X}"
- "Help me with {X}"
- "Working on {X}"
- "Fix/debug/update {X}"

**Retrieval Requests:**
- "What do we know about {X}"
- "Get more details about {X}"
- "Tell me about {X}"
- "Remind me how {X} works"
- "cortex: {X}" (explicit trigger)

**Session End:**
- "Update learning"
- "Save learnings"
- "End session"
- "Wrap up and save"

### Explicit Trigger

Power users can bypass natural language detection with:
```
cortex: JWT token validation
```

This always triggers a retrieval, regardless of phrasing.

---

## Updated Documentation

- **New:** `docs/session-protocol-v1.1.0.md` — Full protocol design
- **Updated:** `docs/architecture.md` — Session flow diagram
- **Updated:** `docs/cortex-spec.md` — Section 8: Session Protocol
- **Updated:** `docs/decisions.md` — ADR-010: Semi-Auto Session Protocol
- **Updated:** `docs/user-guide.md` — Natural language usage guide
- **Updated:** `README.md` — Natural language examples
- **Updated:** `CLAUDE.md` — Session protocol instructions

---

## Breaking Changes

None. v1.1.0 is fully backward compatible with v1.0.0. Manual script usage continues to work.

---

## Known Issues

- **Windows Encoding:** The `cortex-assemble.ps1` script may fail to display output on Windows due to cp1252 encoding limitations. The core functionality works correctly; only the console output is affected. Workaround: Use the Python modules directly or redirect output to a file.

---

## Upgrade Instructions

1. **Pull the latest code:**
   ```powershell
   git pull origin main
   ```

2. **Update global CLAUDE.md** (if using Claude Code):
   - Open `~/.claude/CLAUDE.md`
   - Replace the "Cortex Context Management" section with the updated version from the project

3. **No index rebuild required** — Your existing chunks and memories work unchanged.

---

## What's Next (Planned for v1.2.0)

- Document impact analysis (suggest docs to update after changes)
- Incremental indexing (add without full rebuild)
- Memory decay for unused memories
- Windows encoding fix

---

## Credits

Cortex v1.1.0 was developed through human-AI collaboration, focusing on making LLM-native context management accessible to all users regardless of technical background.

---

*Cortex v1.1.0 - LLM-Native Context Management*
