# PowerShell Scripts (Deprecated)

**These scripts are deprecated as of Cortex v1.2.0.**

Use the cross-platform Python CLI instead:

```bash
python -m cli <command>
```

## Migration Guide

| Old (PowerShell) | New (Python CLI) |
|------------------|------------------|
| `.\cortex-init.ps1` | `python -m cli init` |
| `.\cortex-chunk.ps1 -Path X` | `python -m cli chunk --path X` |
| `.\cortex-index.ps1` | `python -m cli index` |
| `.\cortex-retrieve.ps1 -Query X` | `python -m cli retrieve --query X` |
| `.\cortex-assemble.ps1 -Task X` | `python -m cli assemble --task X` |
| `.\cortex-memory.ps1 -Action add` | `python -m cli memory add` |
| `.\cortex-memory.ps1 -Action list` | `python -m cli memory list` |
| `.\cortex-memory.ps1 -Action delete -Id X` | `python -m cli memory delete X` |
| `.\cortex-extract.ps1 -Text X` | `python -m cli extract --text X` |
| `.\cortex-status.ps1` | `python -m cli status` |
| `.\cortex-status.ps1 -Json` | `python -m cli status --json` |

## Why Python CLI?

- **Cross-platform**: Works on Windows, Mac, and Linux
- **Single codebase**: Easier to maintain
- **Better features**: Stale chunk detection, refresh support
- **Cleaner architecture**: Direct Python calls, no embedded scripts

## These Scripts Will Be Removed

These PowerShell scripts will be removed in a future version. Please migrate to the Python CLI.

If you have automation depending on these scripts, update to use the Python CLI equivalents.
