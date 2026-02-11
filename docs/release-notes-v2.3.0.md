# Cortex v2.3.0 Release Notes

**Release Date:** 2026-02-11

## Overview

Cortex v2.3.0 is a quality-focused release that fixes bugs, replaces pickle serialization with a safer format, reduces code duplication through a shared utility module, and adds automated test coverage. The session protocol and agent system are unchanged.

## Fixed

### Index CLI Crash (HIGH)

The `index` CLI command crashed with a `TypeError` on every run. `build_index()` returns a tuple `(count, meta)`, but the CLI handler was treating it as a dict. Fixed in `cli/commands/index.py`.

### Extractor Duplicate Sentence Bug (MEDIUM)

When session text contained duplicate sentences, the extractor's context windowing used `list.index()` which always matched the *first* occurrence, producing incorrect context for later duplicates. Now uses `enumerate()` for positional accuracy. Fixed in `core/extractor.py`.

### Retrieve CLI Default Mismatch (LOW)

The `retrieve` CLI command defaulted `index_type` to `"chunks"`, while the core `retrieve()` function defaulted to `"both"`. The CLI now defaults to `"both"` to match. Fixed in `cli/commands/retrieve.py`.

## Changed

### Index Storage: Pickle Replaced with NumPy/JSON (SECURITY)

Index files now use NumPy `.npy` for embeddings and JSON `.ids.json` for ID lists, replacing pickle (`.pkl`). This eliminates the risk of arbitrary code execution during index deserialization.

**Before:**
```
.cortex/index/
├── chunks.pkl
├── chunks.meta.json
├── memories.pkl
└── memories.meta.json
```

**After:**
```
.cortex/index/
├── chunks.npy
├── chunks.ids.json
├── chunks.meta.json
├── memories.npy
├── memories.ids.json
└── memories.meta.json
```

### Shared Utility Module

Created `core/utils.py` with functions previously duplicated across modules:

| Function | Consolidated From |
|----------|-------------------|
| `parse_frontmatter()` | indexer, chunker, memory |
| `parse_chunk_id()` | chunker, retriever, assembler |
| `load_chunk_content()` | retriever, assembler |
| `extract_keywords()` + `STOPWORDS` | chunker (49 words), memory (38 words) |

The keyword stopword lists were merged into a single unified set.

### Removed Unused Parameter

The `overlap` parameter was removed from `split_by_paragraphs()` in `core/chunker.py` — it was accepted but never used.

## New

### Test Suite

69 focused tests across three layers:

| Layer | Count | Description |
|-------|-------|-------------|
| Pure functions | 49 | Parsing, scoring, formatting — no I/O |
| Interfaces | 15 | Module APIs, return types, error handling |
| I/O round-trips | 5 | Chunk creation, index build/load, memory persistence |

Run with:
```bash
cd .cortex-engine && .venv/Scripts/python -m pytest   # Windows
cd .cortex-engine && .venv/bin/python -m pytest        # Unix
```

### New ADRs

- **ADR-022** — Shared Utility Module
- **ADR-023** — Test Strategy
- **ADR-024** — Replace Pickle with NumPy/JSON (amends ADR-002)

### New Files

- `core/utils.py`
- `requirements-dev.txt`
- `pytest.ini`
- `tests/__init__.py`, `tests/conftest.py`
- `tests/test_pure_functions.py`, `tests/test_interfaces.py`, `tests/test_file_io.py`

## Migration from v2.2.0

### Index Rebuild Required

The pickle index format is no longer supported. Rebuild indices after updating:

```bash
# Windows:
cd .cortex-engine && .venv/Scripts/python -m cli index --root ..
# Unix:
cd .cortex-engine && .venv/bin/python -m cli index --root ..
```

Old `.pkl` files in `.cortex/index/` can be safely deleted after rebuilding.

### No Other Breaking Changes

- Session protocol is unchanged
- CLI commands and flags are unchanged
- Agent system is unchanged
- All existing chunks and memories remain valid

## Files Changed

### Code (New)
- `core/utils.py` — Shared utility functions
- `tests/` — Test suite (5 files)
- `requirements-dev.txt` — Dev dependencies
- `pytest.ini` — Test configuration

### Code (Modified)
- `core/indexer.py` — NumPy/JSON serialization, uses utils.py
- `core/extractor.py` — enumerate() for duplicate sentences
- `core/chunker.py` — Uses utils.py, removed unused overlap param
- `core/memory.py` — Uses utils.py
- `core/retriever.py` — Uses utils.py
- `core/assembler.py` — Uses utils.py
- `cli/commands/index.py` — Fixed return type handling
- `cli/commands/retrieve.py` — Default index_type aligned

### Documentation
- Updated: CHANGELOG, INSTALL, README, architecture, cortex-spec, decisions, development-history, user-guide
- New: release-notes-v2.3.0.md, session-protocol-v2.3.0.md

---

*Cortex v2.3.0 - Bug Fixes, Security, and Test Coverage*
