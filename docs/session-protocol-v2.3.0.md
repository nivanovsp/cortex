# Session Protocol v2.3.0

**Date:** 2026-02-11
**Status:** Active
**Supersedes:** Session Protocol v2.2.0

## Overview

Session Protocol v2.3.0 is unchanged from v2.2.0 in behavior. The core protocol (status -> assemble -> retrieve -> extract), decentralized agent activation, CLI invocation pattern, and natural language triggers all remain the same.

The v2.3.0 release focused on internal code quality: bug fixes, security improvements (pickle replaced with NumPy/JSON for index storage), a shared utility module, and automated tests. None of these changes affect the session protocol.

## What Changed from v2.2.0

### Internal Changes Only

| Change | Impact on Protocol |
|--------|--------------------|
| Index format: pickle -> NumPy/JSON | None — index is rebuilt transparently |
| Shared `core/utils.py` module | None — internal refactoring |
| Extractor duplicate sentence fix | Slightly more accurate memory extraction |
| Index CLI crash fix | Index command now works correctly |
| 69 automated tests added | None — development tooling only |

### No Protocol Changes

- CLI invocation pattern: **unchanged** (venv python, same as v2.2.0)
- Agent activation flow: **unchanged**
- Natural language triggers: **unchanged**
- Context budget: **unchanged**
- Important rules: **unchanged**

## Protocol Layers (Unchanged)

```
Layer 0: Session Protocol (always active)
  status -> assemble -> retrieve -> extract

Layer 1: Agent Mode (optional)
  persona + rules + skills + domain focus
```

## Agent Activation Flow (Unchanged)

### Without Mode (Base Protocol)

1. Run `status --json --root ..` using the venv python silently
2. Note metadata internally
3. Greet user, mention Cortex if relevant
4. Wait for task identification
5. On task: run `assemble --task "..." --root ..` using the venv python
6. On retrieval: run `retrieve --query "..." --root ..` using the venv python
7. On session end: run `extract --text "..." --root ..` using the venv python

### With Mode (Agent Protocol)

1. Load mode spec (~2KB)
2. Run `status --json --root ..` using the venv python silently
3. Greet as persona
4. Wait for user to select topic/task
5. Retrieve handoffs, artifacts, learnings for that topic
6. Begin work with relevant context

## CLI Invocation (Unchanged from v2.2.0)

**Windows:**
```bash
cd .cortex-engine && .venv/Scripts/python -m cli <command> --root ..
```

**Unix:**
```bash
cd .cortex-engine && .venv/bin/python -m cli <command> --root ..
```

**Fallback:** If `.cortex-engine/.venv/` does not exist, use `python -m cli`.

## Context Budget (Unchanged)

| Phase | Tokens | % of 200k |
|-------|--------|-----------|
| Session start (metadata) | ~50 | 0.025% |
| Task assembly | ~2,500 | 1.25% |
| On-demand retrieval (x2) | ~3,000 | 1.5% |
| **Typical session total** | **~5,550** | **~2.8%** |

97%+ of context remains for actual work.

## Natural Language Triggers (Unchanged)

| Phase | Trigger Examples |
|-------|-----------------|
| Task | "Let's work on {X}", "Help me with {X}", "Fix/debug/update {X}" |
| Retrieval | "What do we know about {X}", "Tell me about {X}", "cortex: {X}" |
| Session End | "Update learning", "Save learnings", "Wrap up and save" |
| Init | "cortex init", "initialize cortex", "set up cortex" |
| Update | "cortex update", "update cortex", "refresh cortex" |

## Important Rules (Unchanged)

1. **Never pre-load content files** — use retrieval only
2. **Commands are invisible to users** — natural language interaction
3. **Session end requires user trigger** — never auto-extract
4. **Explicit trigger always works** — "cortex: {query}"
5. **Cross-platform** — Python CLI works on Windows, Mac, Linux
6. **No time estimates** — no agent produces duration predictions

---

*Cortex v2.3.0 - Session Protocol*
