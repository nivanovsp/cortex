# LC-005: Windows-Centric CLI

**Priority:** P3 - Defer until evidence of need
**Status:** Accepted (implementation pending)
**Category:** Legitimate Concern
**Principle Check:** Is Windows-only acceptable for target audience?

---

## Summary

PowerShell scripts assume Windows. The Python core is portable, but the CLI layer isn't. For broader adoption, a cross-platform CLI would be more inclusive.

## Current Implementation

- `scripts/*.ps1` - All PowerShell
- `core/*.py` - Python (portable)
- No Unix shell equivalents

## Questions to Resolve

1. Who is the target audience? Windows-only devs?
2. Is cross-platform support a real need or theoretical?
3. What's the simplest path to cross-platform?
4. Should we maintain two CLI implementations?

## Options

| Option | Effort | Maintenance | Recommendation |
|--------|--------|-------------|----------------|
| A. Stay Windows-only | None | Low | Fine if audience is Windows |
| B. Add Bash equivalents | Medium | 2× maintenance | Duplication burden |
| C. Python CLI (Click/Typer) | Medium | Single codebase | Clean, portable |
| D. Compiled binary (Go/Rust) | High | Single binary | Overkill for this project |

## Deep Dive

### Analysis (2026-01-27)

**Current Architecture:**
- PowerShell scripts (`scripts/*.ps1`) wrap Python core
- Scripts embed Python code as strings, write to temp files, execute
- Works on Windows only (or requires PowerShell Core on Mac/Linux)
- Python core (`core/*.py`) is already cross-platform

**Options Evaluated:**

| Option | Effort | Maintenance | Cross-Platform |
|--------|--------|-------------|----------------|
| A. Stay Windows-only | None | Low | No |
| B. Add Bash equivalents | Medium | High (2×) | Yes |
| C. Python CLI (Typer) | Medium | Low | Yes |
| D. Compiled binary | High | Medium | Yes (overkill) |

**Option C Selected** - Python CLI with Typer because:
- Single codebase, cross-platform
- Python already required for embeddings
- Cleaner architecture (no embedded Python strings)
- ~290 lines replaces ~950 lines of PowerShell
- Core logic (`core/*.py`) unchanged

**User Workflow Impact:**
- Daily workflow (natural language) unchanged
- Agent calls different commands internally (invisible to user)
- Initial setup syntax slightly different
- Works on Windows, Mac, Linux without extra runtime

### Installation Approach

**Option A: Module in project (selected for now)**
```bash
# Cortex copied to project folder
python -m cortex.cli init
python -m cortex.cli chunk --path "docs/"
python -m cortex.cli assemble --task "X"
```

> **Note:** Option B (Global install via `pip install cortex-context`) may be
> desirable in the future for cleaner commands (`cortex init` instead of
> `python -m cortex.cli init`). The CLI structure should be designed to
> support both approaches - module invocation now, pip install later.

### Structure

```
cortex/
├── cli/
│   ├── __init__.py
│   ├── main.py           # Typer app entry point
│   └── commands/
│       ├── __init__.py
│       ├── init.py       # cortex init
│       ├── chunk.py      # cortex chunk
│       ├── index.py      # cortex index
│       ├── retrieve.py   # cortex retrieve
│       ├── assemble.py   # cortex assemble
│       ├── memory.py     # cortex memory
│       ├── extract.py    # cortex extract
│       └── status.py     # cortex status
├── core/                 # UNCHANGED
├── scripts/              # DEPRECATED (keep during transition)
└── ...
```

### Command Mapping

| PowerShell | Python CLI |
|------------|------------|
| `.\scripts\cortex-init.ps1` | `python -m cortex.cli init` |
| `.\scripts\cortex-chunk.ps1 -Path X` | `python -m cortex.cli chunk --path X` |
| `.\scripts\cortex-index.ps1` | `python -m cortex.cli index` |
| `.\scripts\cortex-retrieve.ps1 -Query X` | `python -m cortex.cli retrieve --query X` |
| `.\scripts\cortex-assemble.ps1 -Task X` | `python -m cortex.cli assemble --task X` |
| `.\scripts\cortex-memory.ps1 -Action add` | `python -m cortex.cli memory add` |
| `.\scripts\cortex-extract.ps1 -Text X` | `python -m cortex.cli extract --text X` |
| `.\scripts\cortex-status.ps1` | `python -m cortex.cli status` |

## Decision

**Accepted - Option C: Python CLI with Typer (Module in project)**

Rationale:
1. Cross-platform requirement met (Windows, Mac, Linux)
2. Single codebase, low maintenance
3. Core logic unchanged
4. User workflow unchanged (natural language still works)
5. Cleaner architecture

**Future consideration:** Add global install option (`pip install`) when broader distribution needed.

**Implementation:** Multiple tasks created - see related tasks.

---

**Guiding Principle:** Solve real problems. If Windows is the target, don't add cross-platform complexity preemptively.
