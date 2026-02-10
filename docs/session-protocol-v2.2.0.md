# Session Protocol v2.2.0

**Date:** 2026-02-10
**Status:** Active
**Supersedes:** Session Protocol v2.1.0

## Overview

Session Protocol v2.2.0 updates the CLI invocation pattern to use an isolated virtual environment. The core protocol (status -> assemble -> retrieve -> extract) and decentralized agent activation are unchanged from v2.1.0. The only change is how CLI commands are invoked — through the venv Python interpreter instead of system Python.

## What Changed from v2.1.0

### CLI Invocation Pattern

**Before (v2.1.0):**
```bash
cd .cortex-engine && python -m cli status --json --root ..
cd .cortex-engine && python -m cli assemble --task "..." --root ..
cd .cortex-engine && python -m cli retrieve --query "..." --root ..
```

**After (v2.2.0) — Windows:**
```bash
cd .cortex-engine && .venv/Scripts/python -m cli status --json --root ..
cd .cortex-engine && .venv/Scripts/python -m cli assemble --task "..." --root ..
cd .cortex-engine && .venv/Scripts/python -m cli retrieve --query "..." --root ..
```

**After (v2.2.0) — Unix:**
```bash
cd .cortex-engine && .venv/bin/python -m cli status --json --root ..
cd .cortex-engine && .venv/bin/python -m cli assemble --task "..." --root ..
cd .cortex-engine && .venv/bin/python -m cli retrieve --query "..." --root ..
```

**Why:** Cortex dependencies (`typer`, `sentence-transformers`, etc.) are installed in `.cortex-engine/.venv/`, isolated from the host project's Python environment. Using the venv interpreter directly avoids `ModuleNotFoundError` when the project's own venv is active.

**Backward compatible:** If `.cortex-engine/.venv/` does not exist (pre-v2.2.0), fall back to `python -m cli`.

### Initialization

**Before (v2.1.0):**
```bash
pip install -r .cortex-engine/requirements.txt
```

**After (v2.2.0):**
```bash
# Windows:
python -m venv .cortex-engine/.venv
.cortex-engine/.venv/Scripts/pip install -r .cortex-engine/requirements.txt
# Unix:
python -m venv .cortex-engine/.venv
.cortex-engine/.venv/bin/pip install -r .cortex-engine/requirements.txt
```

### Status Output

The `status` command now reports venv isolation state:
- `Environment: Isolated (.venv)` — venv exists and is used
- `Environment: System Python (not isolated)` — no venv, using system Python

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

## Cortex Initialization (Updated in v2.2.0)

When user says "cortex init", "initialize cortex", or "set up cortex":

1. `git clone https://github.com/nivanovsp/cortex.git .cortex-engine`
2. Create venv and install deps (platform-specific — see "What Changed" above)
3. Copy `agents/`, `.claude/commands/`, `CLAUDE.md` from `.cortex-engine/` to project root
4. Run `init --root ..` using the venv python
5. Run `bootstrap --root ..` using the venv python
6. Run `index --root ..` using the venv python
7. Add `.cortex-engine/` and `.cortex/` to `.gitignore`
8. Run `status --root ..` using the venv python (verify)

Stop immediately if any step fails.

## Cortex Update (Updated in v2.2.0)

When user says "cortex update", "update cortex", or "refresh cortex":

1. `cd .cortex-engine && git pull`
2. Update venv deps (platform-specific pip install into existing venv)
3. Re-copy `agents/`, `.claude/commands/`, `CLAUDE.md` to project root
4. Run `bootstrap --force --root ..` using the venv python
5. Run `index --root ..` using the venv python
6. Run `status --root ..` using the venv python (verify)

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

*Cortex v2.2.0 - Session Protocol*
