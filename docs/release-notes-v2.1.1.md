# Cortex v2.1.1 Release Notes

**Release Date:** 2026-02-04

## Overview

Cortex v2.1.1 is a patch release that fixes a critical bug in the `extract` command. The bug caused the command to fail when run from an installed project using the `.cortex-engine/` pattern.

## What's Fixed

### Extract Command API Mismatch

The CLI command and core module had incompatible function signatures, causing errors like:

```
ValueError: 'D:\Dev Projects\Tasks app' is not in list
```

**Root cause:** The CLI passed `project_root` as a positional argument where `min_confidence` was expected.

**Fix:**
- `extract_and_format()` now accepts `project_root` as a named parameter
- `extract_and_format()` returns a dict with `memories` key (was returning string)
- `save_proposed_memories()` parameter order fixed and `indices` made optional
- CLI uses explicit keyword arguments to prevent future parameter order bugs

### New Function: `format_proposed_memories()`

Added a new function for CLI standalone use that returns formatted text output. The original `extract_and_format()` now returns structured data for programmatic use.

## Technical Details

### `core/extractor.py` Changes

**Before:**
```python
def extract_and_format(text: str, min_confidence: str = "low") -> str:
def save_proposed_memories(proposed: list[ProposedMemory], indices: list[int], project_root: str = "."):
```

**After:**
```python
def extract_and_format(text: str, project_root: str = ".", min_confidence: str = "low") -> dict:
def save_proposed_memories(memories: list, project_root: str = ".", indices: Optional[list[int]] = None):
def format_proposed_memories(text: str, min_confidence: str = "low") -> str:
```

### `cli/commands/extract.py` Changes

Uses explicit keyword arguments:
```python
result = extract_and_format(text, project_root=str(root))
saved = save_proposed_memories(memories, project_root=str(root))
```

## Migration

No migration needed. Simply update your `.cortex-engine/` directory:

```bash
cd .cortex-engine && git pull
```

Or run "cortex update" if using Claude Code.

## Files Changed

### Code
- `core/extractor.py` — Fixed function signatures, added `format_proposed_memories()`
- `cli/commands/extract.py` — Use keyword arguments

### Documentation
- `CHANGELOG.md` — Added v2.1.1 entry
- `docs/development-history.md` — Added v2.1.1 section
- `docs/release-notes-v2.1.1.md` — This file

---

*Cortex v2.1.1 - Extract Command Bug Fix*
