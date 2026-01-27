# Cortex v1.2.0 Release Notes

**Release Date:** 2026-01-27

---

## Highlights

### Cross-Platform Python CLI

Cortex now works seamlessly on **Windows, Mac, and Linux**. The new Python CLI replaces the Windows-only PowerShell scripts.

```bash
# Works everywhere
python -m cli status
python -m cli chunk --path docs/
python -m cli assemble --task "Your task"
```

### Stale Chunk Detection

Know when your documentation chunks are out of date. Cortex tracks source file changes and alerts you when chunks need refreshing.

```bash
python -m cli status
# Shows: "Stale Chunks: docs/api.md (5 chunks, modified)"

python -m cli chunk --path docs/api.md --refresh
python -m cli index
```

### Memory Retrieval Tracking

The feedback loop is now active. When memories are used in context frames, their retrieval count increments, making frequently-useful memories rank higher over time.

---

## New Features

### CLI Commands

| Command | Description |
|---------|-------------|
| `python -m cli init` | Initialize Cortex |
| `python -m cli chunk --path <file>` | Chunk documents |
| `python -m cli chunk --path <file> --refresh` | Refresh stale chunks |
| `python -m cli index` | Build/rebuild indices |
| `python -m cli retrieve --query <text>` | Search for context |
| `python -m cli assemble --task <text>` | Build context frame |
| `python -m cli memory add` | Add a memory |
| `python -m cli memory list` | List memories |
| `python -m cli memory delete <id>` | Delete a memory |
| `python -m cli extract --text <text>` | Extract learnings |
| `python -m cli status` | Show status and stale chunks |
| `python -m cli status --json` | JSON output |

### Chunk Provenance

Every chunk now stores:
- `source_path` - Where it came from
- `source_hash` - SHA256 for change detection

### Stale Detection Workflow

1. Run `python -m cli status` to see stale chunks
2. Run `python -m cli chunk --path <file> --refresh` to update
3. Run `python -m cli index` to rebuild

---

## Changes

### Dependencies

New requirements in `requirements.txt`:
- `typer>=0.9.0` - CLI framework
- `rich>=13.0.0` - Terminal formatting

### Deprecated

PowerShell scripts are deprecated. See `scripts/README.md` for migration guide.

| Old Command | New Command |
|-------------|-------------|
| `.\cortex-init.ps1` | `python -m cli init` |
| `.\cortex-chunk.ps1 -Path X` | `python -m cli chunk --path X` |
| `.\cortex-status.ps1` | `python -m cli status` |

---

## Architecture Decisions

Six new ADRs document the v1.2.0 decisions:

- **ADR-011**: Cross-Platform Python CLI
- **ADR-012**: Chunk Provenance Tracking
- **ADR-013**: Memory Retrieval Tracking
- **ADR-014**: Won't Implement - Semantic Deduplication
- **ADR-015**: Won't Implement - Memory Confidence Calibration
- **ADR-016**: Won't Implement - Query Refinement

---

## Expert Review Outcomes

An independent expert review identified 9 items. Outcomes:

| Item | Topic | Decision |
|------|-------|----------|
| LC-002 | Feedback Loop | **Implemented** |
| LC-005 | Windows-Centric CLI | **Implemented** |
| MF-002 | Chunk Provenance | **Implemented** |
| LC-001 | Pattern Extraction | Deferred |
| LC-003 | Embedding Model | Deferred |
| MF-001 | Semantic Dedup | Won't Implement |
| MF-003 | Confidence Calibration | Won't Implement |
| MF-004 | Query Refinement | Won't Implement |

See `docs/reviews/` for detailed analysis of each item.

---

## Upgrade Guide

### From v1.1.0

1. **Install new dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Update your workflow:**
   - Replace PowerShell commands with Python CLI equivalents
   - See migration table in `scripts/README.md`

3. **Update global CLAUDE.md:**
   - Copy the updated Cortex section from project CLAUDE.md
   - Or reference `global/CLAUDE.md` in the repo

4. **Existing data is compatible:**
   - Chunks and memories work without changes
   - New chunks will include provenance fields
   - Old chunks work but won't have stale detection

### Fresh Installation

```bash
git clone https://github.com/nivanovsp/cortex.git
cd cortex
pip install -r requirements.txt
python -m cli init
```

---

## Documentation

Updated for v1.2.0:
- `README.md` - Overview and quick start
- `INSTALL.md` - Installation guide
- `CLAUDE.md` - Claude Code integration
- `docs/architecture.md` - System design
- `docs/cortex-spec.md` - Technical specification
- `docs/user-guide.md` - Usage guide
- `docs/decisions.md` - ADRs
- `docs/session-protocol-v1.2.0.md` - Session protocol
- `docs/development-history.md` - Development chronicle
- `CHANGELOG.md` - Version history

---

## What's Next

Potential future enhancements (not committed):
- Incremental indexing
- Memory decay/archival
- Watch mode for auto-chunking
- Web UI

---

*Cortex v1.2.0 - LLM-Native Context Management*
