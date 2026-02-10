# Cortex v2.2.0 Release Notes

**Release Date:** 2026-02-10

## Overview

Cortex v2.2.0 introduces **virtual environment isolation** — Cortex now creates and manages its own venv at `.cortex-engine/.venv/`, preventing dependency conflicts with the host project's Python environment. This is a non-breaking change with full backward compatibility.

## What's New

### Virtual Environment Isolation

Previously, `pip install -r .cortex-engine/requirements.txt` installed Cortex dependencies into whatever Python was active. If the host project had its own venv (e.g., Django, Flask), this caused:
- `ModuleNotFoundError` when the project's venv didn't have Cortex deps
- Dependency pollution when Cortex deps leaked into the project's venv
- Version conflicts between Cortex and project requirements

**Now:** Cortex creates a dedicated venv at `.cortex-engine/.venv/` during initialization. All CLI commands use this venv's Python interpreter directly, with no activation required.

### New Initialization Flow

**Before (v2.1.x):**
```bash
pip install -r .cortex-engine/requirements.txt
cd .cortex-engine && python -m cli init --root ..
```

**After (v2.2.0):**
```bash
# Windows:
python -m venv .cortex-engine\.venv
.cortex-engine\.venv\Scripts\pip install -r .cortex-engine\requirements.txt
cd .cortex-engine && .venv\Scripts\python -m cli init --root ..

# Unix:
python -m venv .cortex-engine/.venv
.cortex-engine/.venv/bin/pip install -r .cortex-engine/requirements.txt
cd .cortex-engine && .venv/bin/python -m cli init --root ..
```

### Status Reports Isolation

The `status` command now shows the environment isolation state:

```
Status: INITIALIZED
Environment: Isolated (.venv)
```

Or for pre-v2.2.0 installations without a venv:

```
Status: INITIALIZED
Environment: System Python (not isolated)
```

### Config Helpers

New classmethods in `core/config.py`:
- `Config.get_venv_python(engine_root)` — Returns the platform-correct path to the venv Python interpreter
- `Config.has_venv(engine_root)` — Checks if the Cortex venv exists

## Migration from v2.1.x

1. Create the isolated venv:
   ```bash
   # Windows:
   python -m venv .cortex-engine\.venv
   .cortex-engine\.venv\Scripts\pip install -r .cortex-engine\requirements.txt

   # Unix:
   python -m venv .cortex-engine/.venv
   .cortex-engine/.venv/bin/pip install -r .cortex-engine/requirements.txt
   ```

2. Update your workflow to use the venv python for CLI commands:
   ```bash
   # Windows:
   cd .cortex-engine && .venv\Scripts\python -m cli <command> --root ..
   # Unix:
   cd .cortex-engine && .venv/bin/python -m cli <command> --root ..
   ```

3. If using Claude Code, update your project's `CLAUDE.md` from the latest engine:
   ```bash
   cp .cortex-engine/CLAUDE.md ./CLAUDE.md
   ```

**Backward compatible:** If `.cortex-engine/.venv/` does not exist, the old `python -m cli` pattern still works.

## Files Changed

### Code
- `core/__init__.py` — Version bump to 2.2.0
- `core/config.py` — Added `VENV_DIR`, `get_venv_python()`, `has_venv()`
- `cli/commands/status.py` — Venv isolation status reporting
- `.gitignore` — Added `.venv/`

### Documentation
- `CLAUDE.md` — Session protocol v2.2.0, venv-aware CLI invocation
- `global/CLAUDE.md` — Init/update procedures with venv creation
- `CHANGELOG.md` — v2.2.0 entry
- `README.md` — Updated installation, CLI examples, project structure
- `INSTALL.md` — Venv setup instructions, troubleshooting, migration
- `docs/architecture.md` — Updated layout and invocation patterns
- `docs/cortex-spec.md` — Updated CLI appendix
- `docs/user-guide.md` — Updated setup instructions
- `docs/decisions.md` — ADR-021: Virtual Environment Isolation
- `docs/development-history.md` — v2.2.0 section
- `docs/release-notes-v2.2.0.md` — This file
- `docs/session-protocol-v2.2.0.md` — Session protocol v2.2.0
- `agents/skills/cortex-init.md` — Updated skill procedure

---

*Cortex v2.2.0 - Virtual Environment Isolation*
