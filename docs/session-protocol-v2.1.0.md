# Session Protocol v2.1.0

**Date:** 2026-02-01
**Status:** Active
**Supersedes:** Session Protocol v2.0.0

## Overview

Session Protocol v2.1.0 updates the CLI invocation pattern for standalone installation. The core protocol (status -> assemble -> retrieve -> extract) and decentralized agent activation are unchanged from v2.0.0. The only change is how CLI commands are invoked.

## What Changed from v2.0.0

### CLI Invocation Pattern

**Before (v2.0.0):**
```bash
python -m cli status --json
python -m cli assemble --task "..."
python -m cli retrieve --query "..."
```

**After (v2.1.0):**
```bash
cd .cortex-engine && python -m cli status --json --root ..
cd .cortex-engine && python -m cli assemble --task "..." --root ..
cd .cortex-engine && python -m cli retrieve --query "..." --root ..
```

**Why:** The engine now lives in `.cortex-engine/` (cloned from GitHub). Python's `-m` flag requires running from the directory containing the `cli/` package. The `--root ..` parameter tells commands where the project data lives.

**Backward compatible:** When working inside the Cortex repo itself, the old `python -m cli <cmd>` still works.

### Cortex Detection

**Before (v2.0.0):** Agent checks if `.cortex/` exists
**After (v2.1.0):** Agent checks if `.cortex-engine/` exists (indicates Cortex is installed)

## Protocol Layers (Unchanged)

```
Layer 0: Session Protocol (always active)
  status -> assemble -> retrieve -> extract

Layer 1: Agent Mode (optional)
  persona + rules + skills + domain focus
```

## Agent Activation Flow (Unchanged)

### Without Mode (Base Protocol)

1. Run `cd .cortex-engine && python -m cli status --json --root ..` silently
2. Note metadata internally
3. Greet user, mention Cortex if relevant
4. Wait for task identification
5. On task: run `cd .cortex-engine && python -m cli assemble --task "..." --root ..`
6. On retrieval: run `cd .cortex-engine && python -m cli retrieve --query "..." --root ..`
7. On session end: run `cd .cortex-engine && python -m cli extract --text "..." --root ..`

### With Mode (Agent Protocol)

1. Load mode spec (~2KB)
2. Run `cd .cortex-engine && python -m cli status --json --root ..` silently
3. Greet as persona
4. Wait for user to select topic/task
5. Retrieve handoffs, artifacts, learnings for that topic
6. Begin work with relevant context

## Cortex Initialization (New in v2.1.0)

When user says "cortex init", "initialize cortex", or "set up cortex":

1. `git clone https://github.com/nivanovsp/cortex.git .cortex-engine`
2. `pip install -r .cortex-engine/requirements.txt`
3. Copy `agents/`, `.claude/commands/`, `CLAUDE.md` from `.cortex-engine/` to project root
4. `cd .cortex-engine && python -m cli init --root ..`
5. `cd .cortex-engine && python -m cli bootstrap --root ..`
6. `cd .cortex-engine && python -m cli index --root ..`
7. Add `.cortex-engine/` and `.cortex/` to `.gitignore`
8. `cd .cortex-engine && python -m cli status --root ..` (verify)

Stop immediately if any step fails.

## Cortex Update (New in v2.1.0)

When user says "cortex update", "update cortex", or "refresh cortex":

1. `cd .cortex-engine && git pull`
2. Re-copy `agents/`, `.claude/commands/`, `CLAUDE.md` to project root
3. `cd .cortex-engine && python -m cli bootstrap --force --root ..`
4. `cd .cortex-engine && python -m cli index --root ..`
5. `cd .cortex-engine && python -m cli status --root ..` (verify)

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

*Cortex v2.1.0 - Session Protocol*
