# Cortex v2.1.0 Release Notes

**Release Date:** 2026-02-01

## Overview

Cortex v2.1.0 makes the methodology truly standalone. Anyone can now say "cortex init" in an empty project folder and get the full Cortex experience — engine, agents, skills, templates, and semantic retrieval — without manual setup steps.

This release focuses on installation simplicity and the developer experience of getting started.

## What's New

### Standalone Installation

Say "cortex init" in any project folder. The agent (guided by the global CLAUDE.md):

1. Clones the Cortex repo into `.cortex-engine/`
2. Installs Python dependencies
3. Copies `agents/`, `.claude/commands/`, and `CLAUDE.md` into the project
4. Runs init, bootstrap, index, and verify
5. Adds `.cortex-engine/` and `.cortex/` to `.gitignore`

**Prerequisites:** Python 3.8+, Git, and the global `CLAUDE.md` in `~/.claude/`.

### Cortex Update

Say "cortex update" to pull the latest version and re-bootstrap:

1. Pulls latest from GitHub into `.cortex-engine/`
2. Re-copies methodology files to project root
3. Re-bootstraps with `--force`
4. Rebuilds indices

### Complete Global CLAUDE.md

The `global/CLAUDE.md` is now a fully standalone file containing:

- **RMS Framework** — Rules, Modes, Skills methodology structure
- **Universal Conventions** — File naming, code style, documentation
- **Universal Protocols** — Communication, question protocol, safety, quality
- **Critical Thinking Protocol** — 4-layer reasoning framework
- **Cortex Session Protocol** — Full semi-auto protocol with `.cortex-engine` CLI pattern
- **Cortex Initialization** — Step-by-step instructions for "cortex init"
- **Cortex Update** — Instructions for "cortex update"

No external dependencies on Neocortex, MLDA, or Beads.

## What Changed

### CLI Path Resolution

All CLI commands now resolve `core/` relative to the engine's own location (`Path(__file__).resolve().parent.parent.parent`) instead of the project root. This is backward compatible — running from the Cortex repo directly still works.

### CLI Invocation Pattern

**Installed projects:**
```bash
cd .cortex-engine && python -m cli <command> --root ..
```

**Development (in Cortex repo):**
```bash
python -m cli <command>
```

The `--root` parameter (already present on all commands) tells Cortex where the project data lives.

### Session Protocol Updates

All CLI references in CLAUDE.md files updated to use the `.cortex-engine` pattern. The session protocol behavior is unchanged — just the underlying command paths.

## Project Structure After Installation

```
your-project/
├── .cortex-engine/       # Cloned Cortex repo (engine)
├── .cortex/              # Runtime data (chunks, memories, indices)
├── .claude/commands/     # Slash commands (copied)
├── agents/               # Methodology files (copied)
├── CLAUDE.md             # Project instructions (copied)
└── (your project files)
```

## Migration from v2.0.0

1. Clone engine: `git clone https://github.com/nivanovsp/cortex.git .cortex-engine`
2. Install deps: `pip install -r .cortex-engine/requirements.txt`
3. Re-bootstrap: `cd .cortex-engine && python -m cli bootstrap --force --root ..`
4. Rebuild index: `cd .cortex-engine && python -m cli index --root ..`
5. Update `~/.claude/CLAUDE.md` from `.cortex-engine/global/CLAUDE.md`
6. Add `.cortex-engine/` to `.gitignore`

## Files Changed

### Code
- `cli/commands/*.py` (9 files) — `sys.path.insert` uses engine root

### Documentation
- `CHANGELOG.md` — v2.1.0 entry
- `INSTALL.md` — Complete rewrite for standalone setup
- `README.md` — Updated installation, CLI reference, project structure
- `CLAUDE.md` — Updated CLI references and session protocol
- `global/CLAUDE.md` — Complete rewrite as standalone file
- `docs/architecture.md` — Added standalone installation section
- `docs/cortex-spec.md` — Updated CLI appendix
- `docs/decisions.md` — Added ADR-019
- `docs/development-history.md` — Added v2.1.0 section
- `docs/user-guide.md` — Updated getting started and CLI examples

### New Files
- `docs/release-notes-v2.1.0.md` — This file
- `docs/session-protocol-v2.1.0.md` — Updated session protocol

---

*Cortex v2.1.0 - Standalone Installation*
