# Cortex v2.3.0 — Review Findings & Release Tracker

**Date:** 2026-02-11
**Review Type:** Context-aware team review (3 reviewers: code, architecture, QA)
**Status:** All findings confirmed against 21 ADRs and full documentation

---

## Summary

| Category | Count | Status |
|----------|-------|--------|
| HIGH code fixes | 2 | Open |
| MEDIUM code fixes | 3 | Open |
| LOW code fixes | 5 | Open |
| Documentation updates | 8 | Open |
| New documents | 2 | Open |
| **Total** | **20** | **All Open** |

---

## Dependency Graph

```
FIX-001 (index bug)  ─────────────────────────────────┐
FIX-002 (pickle)     ─────────────────────────────────┤
FIX-003 (extractor)  ─────────────────────────────────┤
                                                       ├──► FIX-005 (tests)
FIX-004 (shared parser → creates core/utils.py) ──┐   │
  ├──► FIX-008 (chunk ID parser → into utils.py)  │   │
  │      └──► FIX-006 (shared content loader)      ├───┘
  └──► FIX-007 (shared keyword extraction)         │        All code fixes
                                                   │            │
FIX-009 (unused param)  ──────────────────────────(independent) │
FIX-010 (retrieve default) ───────────────────────(independent) │
                                                                │
                                                                ▼
                                                    DOC-001 through DOC-008
                                                    (update existing docs)
                                                                │
                                                                ▼
                                                    DOC-009, DOC-010
                                                    (new release docs)
```

### Execution Order

| Phase | Tasks | Rationale |
|-------|-------|-----------|
| **1 — Bug fixes** | FIX-001, FIX-002, FIX-003 | Independent of each other. Fix bugs before writing tests against them. |
| **2 — Create utils.py** | FIX-004 | Creates `core/utils.py` with shared `parse_frontmatter()`. Foundation for FIX-006, FIX-007, FIX-008. |
| **3 — Consolidate into utils.py** | FIX-008 → FIX-006 → FIX-007 | FIX-008 (chunk ID parser) before FIX-006 (content loader), because the content loader parses chunk IDs. FIX-007 is independent of 006/008 but same utils.py file. |
| **4 — Quick cleanups** | FIX-009, FIX-010 | Independent, no prerequisites. Can run in parallel with any phase. |
| **5 — Tests** | FIX-005 | Write tests against the final, refactored code. Depends on all bug fixes (Phase 1) and all refactors (Phases 2-3) being complete. |
| **6 — Update docs** | DOC-001 through DOC-008 | After all code changes are final. Reflect v2.3.0 changes in existing documentation. |
| **7 — New release docs** | DOC-009, DOC-010 | Last — release notes and session protocol for v2.3.0. Depends on all other tasks being done. |

### Dependency Table

| Task | Depends On | Blocks |
|------|-----------|--------|
| FIX-001 | — | FIX-005, DOC-* |
| FIX-002 | — | FIX-005, DOC-* |
| FIX-003 | — | FIX-005, DOC-* |
| FIX-004 | — | FIX-006, FIX-007, FIX-008, FIX-005, DOC-* |
| FIX-005 | FIX-001, FIX-002, FIX-003, FIX-004, FIX-006, FIX-007, FIX-008 | DOC-* |
| FIX-006 | FIX-004, FIX-008 | FIX-005, DOC-* |
| FIX-007 | FIX-004 | FIX-005, DOC-* |
| FIX-008 | FIX-004 | FIX-006, FIX-005, DOC-* |
| FIX-009 | — | DOC-* |
| FIX-010 | — | DOC-* |
| DOC-001 to DOC-008 | All FIX-* tasks | DOC-009, DOC-010 |
| DOC-009 | DOC-001 through DOC-008 | — |
| DOC-010 | DOC-001 through DOC-008 | — |

---

## HIGH Priority

### FIX-001: Runtime bug — build_index return type mismatch

- **Severity:** HIGH
- **Status:** Open
- **Location:** `cli/commands/index.py:25-26`
- **Root Cause:** `build_index()` in `core/indexer.py:142` returns `tuple[int, str]` (count, path), but the CLI command at `cli/commands/index.py:26` accesses the result as `chunks_stats['count']`, treating it as a dict.
- **Impact:** Crashes with `TypeError: tuple indices must be integers or slices, not str` on every successful index build. The try/except may mask this as "skipped."
- **Fix:** Change CLI code to unpack the tuple: `count, path = build_index(...)` and use `count` directly. Alternatively, update `build_index()` to return a dict. Check if the same pattern exists for memory index build on the lines below.
- **Similar bug:** v2.1.1 fixed an identical category of API mismatch in the extract command.
- **Dependencies:** None. Blocks FIX-005.

---

### FIX-002: Pickle deserialization in indexer

- **Severity:** HIGH
- **Status:** Open
- **Location:** `core/indexer.py:238-239` (load_index), `core/indexer.py:263-264` (get_index_stats)
- **Root Cause:** `pickle.load()` on `.pkl` index files. ADR-002 chose pickle deliberately but did not address security implications.
- **Impact:** A modified `.pkl` file in `.cortex/index/` could execute arbitrary code on load. Risk is moderate (local-only tool), but the fix is trivial.
- **Fix:** Replace pickle with `np.save()`/`np.load()` for the embeddings array and JSON for the IDs list. The current pickle structure is `{'embeddings': np.ndarray, 'ids': list}` — split into `chunks.npy` + `chunks.ids.json`. Update both `build_index()` (write side) and `load_index()` / `get_index_stats()` (read side).
- **Files to change:** `core/indexer.py` (build, load, stats functions)
- **Note:** Architect reviewer downgraded this (local-only threat model), code reviewer confirmed as HIGH. Use judgment — at minimum, replace pickle with numpy's safer serialization.
- **Dependencies:** None. Blocks FIX-005.

---

## MEDIUM Priority

### FIX-003: Extractor sentence matching bug

- **Severity:** MEDIUM
- **Status:** Open
- **Location:** `core/extractor.py:194-210`
- **Root Cause:** `sentences.index(sent)` at line 202 finds the FIRST occurrence of a sentence. If the same sentence appears multiple times in the input text, the wrong context window is selected.
- **Impact:** Incorrect context attached to extracted memories when duplicate sentences exist.
- **Fix:** Use `enumerate()` with the sentence list to track position directly instead of value-based lookup. Replace `sentences.index(sent)` with the current iteration index.
- **Dependencies:** None. Blocks FIX-005.

---

### FIX-004: Three duplicated frontmatter parsers

- **Severity:** MEDIUM
- **Status:** Open
- **Locations:**
  - `core/indexer.py:17-55` — `parse_frontmatter()` (handles arrays, booleans, ints, null)
  - `core/chunker.py:449-476` — `parse_chunk_metadata()` (simpler, only strips quotes)
  - `core/memory.py:230-267` — inline parsing in `parse_memory_file()` (adds float handling)
- **Root Cause:** Each module implements its own frontmatter parser with subtly different type coercion. Not explained by any ADR.
- **Impact:** Maintenance risk — a fix to one parser doesn't propagate to others. Different modules parse the same format differently.
- **Fix:** Extract a single `parse_frontmatter()` utility into `core/utils.py` that handles all value types (arrays, booleans, ints, floats, null, quoted strings). Update all three modules to use it.
- **Note:** ADR-003 chose YAML frontmatter to avoid a YAML library dependency. The shared parser should remain hand-rolled, not introduce pyyaml.
- **Dependencies:** None. Creates `core/utils.py`. Blocks FIX-006, FIX-007, FIX-008, FIX-005.

---

### FIX-005: Add focused test coverage (~25-30 tests)

- **Severity:** MEDIUM
- **Status:** Open
- **Root Cause:** Zero test files, zero test config, zero test dependencies. No ADR addresses testing — this is an omission, not a decision.
- **Evidence:** v2.1.1 shipped with an API mismatch bug (extract command) that a single interface test would have caught. v2.2.0 verification checklist has 0/6 items checked.
- **Scope:**
  - **Phase 1 — Pure function unit tests (~15 tests, no mocking):**
    - `count_tokens()`, `extract_keywords()`, `parse_sections()`, `split_by_paragraphs()`, `add_overlap()`
    - `compute_keyword_overlap()`, `compute_recency_score()`, `compute_frequency_score()`
    - `ContextBudget.from_total()`, `truncate_to_budget()`
    - `detect_domain()` (both chunker and extractor versions)
    - Scoring formula correctness
  - **Phase 2 — CLI-to-core interface tests (~10 tests):**
    - Verify `extract_and_format()` signature and return type
    - Verify `build_index()` return type matches CLI expectations
    - Verify `save_proposed_memories()` parameter handling
    - Verify all CLI commands call core functions with correct arguments
  - **Phase 3 — File I/O tests with tmpdir (~5 tests):**
    - `chunk_document()` + `save_chunk()` round-trip
    - `create_memory()` + `get_memory()` round-trip
    - `build_index()` + `load_index()` round-trip
- **Infrastructure needed:**
  - Add `pytest` and `pytest-cov` to a `requirements-dev.txt`
  - Create `tests/` directory with `conftest.py`
  - Add `pytest.ini` or `[tool.pytest]` in `pyproject.toml`
- **Not recommended:** Exhaustive coverage. Focus on interface contracts and scoring math.
- **Dependencies:** FIX-001, FIX-002, FIX-003, FIX-004, FIX-006, FIX-007, FIX-008. Do last — write tests against final, refactored code.

---

## LOW Priority

### FIX-006: Duplicated content loaders

- **Severity:** LOW
- **Status:** Open
- **Locations:**
  - `core/retriever.py:225-244` — `_load_content()`
  - `core/assembler.py:161-184` — `load_chunk_content()`
- **Root Cause:** Identical logic (parse domain from chunk ID, find .md file, strip frontmatter, return content) in two modules.
- **Fix:** Extract into a shared utility function in `core/utils.py`. Both modules call the shared function.
- **Dependencies:** FIX-004 (utils.py must exist), FIX-008 (chunk ID parser should be centralized first, since content loader parses chunk IDs). Blocks FIX-005.

---

### FIX-007: Keyword extraction stopword divergence

- **Severity:** LOW
- **Status:** Open
- **Locations:**
  - `core/chunker.py:43-78` — `extract_keywords()` with 49-word stopword list
  - `core/memory.py:85-113` — `extract_keywords()` with 38-word stopword list
- **Root Cause:** Same algorithm copied with different stopword sets. The divergence is unintentional.
- **Note:** `core/retriever.py:92-105` has `extract_query_keywords()` with an intentionally smaller 18-word set for short queries — this one is fine as-is.
- **Fix:** Merge chunker and memory versions into a single shared function in `core/utils.py` with a unified stopword set. Keep the retriever's query-specific version separate.
- **Dependencies:** FIX-004 (utils.py must exist). Blocks FIX-005.

---

### FIX-008: Chunk ID parsing fragility

- **Severity:** LOW
- **Status:** Open
- **Locations:**
  - `core/chunker.py:118-124` — `get_next_doc_number()` assumes `parts[2]` is doc number
  - `core/chunker.py:589-594` — `delete_chunks()` assumes `parts[1]` is domain
  - `core/retriever.py:231-233` — `_load_content()` assumes `parts[1]` is domain
  - `core/assembler.py:163-165` — `load_chunk_content()` assumes `parts[1]` is domain
- **Root Cause:** Chunk ID format `CHK-{DOMAIN}-{DOC}-{SEQ}` is parsed via `split('-')` in 4 places with implicit index assumptions. If a domain contains a hyphen, all break.
- **Fix:** Create a `parse_chunk_id(chunk_id) -> (prefix, domain, doc_num, seq)` utility function. All 4 locations call it instead of splitting manually.
- **Note:** Current domains (AUTH, UI, API, DB, TEST, DEV, GENERAL, METHODOLOGY) are all single-word, so this is theoretical. But a centralized parser prevents future issues.
- **Dependencies:** FIX-004 (utils.py must exist). Blocks FIX-006, FIX-005.

---

### FIX-009: Unused overlap parameter in split_by_paragraphs

- **Severity:** LOW
- **Status:** Open
- **Location:** `core/chunker.py:176`
- **Root Cause:** `split_by_paragraphs(text, max_tokens, overlap)` accepts `overlap` but never uses it. Overlap is applied separately by `add_overlap()` at line 341.
- **Fix:** Remove the `overlap` parameter from the function signature. Update any callers to not pass it.
- **Dependencies:** None. Independent — can be done at any time.

---

### FIX-010: retrieve() default index_type mismatch

- **Severity:** LOW
- **Status:** Open
- **Locations:**
  - `core/retriever.py:112` — defaults to `index_type="both"`
  - `cli/commands/retrieve.py:13` — defaults to `index_type="chunks"`
- **Root Cause:** Core function and CLI have different defaults. The "both" default is never exercised through normal paths (assembler always calls with explicit types).
- **Fix:** Align defaults. Either change the core default to `"chunks"` to match CLI, or change CLI to `"both"` to match core. The assembler is unaffected (always explicit).
- **Dependencies:** None. Independent — can be done at any time.

---

## Documentation — Update Existing (Phase 6)

All documentation updates depend on ALL code fixes (FIX-001 through FIX-010) and tests (FIX-005) being complete. These reflect v2.3.0 changes.

### DOC-001: Update CHANGELOG.md

- **Status:** Open
- **File:** `CHANGELOG.md`
- **Scope:** Add v2.3.0 entry documenting all changes:
  - Fixed: FIX-001 (index command crash), FIX-003 (extractor sentence matching), FIX-010 (retrieve default mismatch)
  - Changed: FIX-002 (pickle replaced with numpy/JSON serialization)
  - Added: `core/utils.py` with shared utilities (FIX-004, FIX-006, FIX-007, FIX-008)
  - Added: Test infrastructure and ~25-30 focused tests (FIX-005)
  - Removed: Unused `overlap` parameter from `split_by_paragraphs` (FIX-009)
  - Added: ADR-022 (Shared Utility Module), ADR-023 (Test Strategy)
- **Dependencies:** All FIX-* tasks. Blocks DOC-009, DOC-010.

---

### DOC-002: Update INSTALL.md

- **Status:** Open
- **File:** `INSTALL.md`
- **Scope:**
  - Add `requirements-dev.txt` mention for development/testing setup
  - Document how to run tests (`pytest` from project root)
  - Note the index file format change (`.pkl` → `.npy` + `.json`) if upgrading from v2.2.0
- **Dependencies:** All FIX-* tasks. Blocks DOC-009, DOC-010.

---

### DOC-003: Update README.md

- **Status:** Open
- **File:** `README.md`
- **Scope:**
  - Bump version to 2.3.0
  - Add mention of test suite in project structure
  - Update index storage format description if changed (FIX-002)
  - Add `core/utils.py` to project structure
  - Add `tests/` to project structure
- **Dependencies:** All FIX-* tasks. Blocks DOC-009, DOC-010.

---

### DOC-004: Update architecture.md

- **Status:** Open
- **File:** `docs/architecture.md`
- **Scope:**
  - Bump version to 2.3.0
  - Update index storage section: `.pkl` files replaced with `.npy` + `.json` (FIX-002)
  - Add `core/utils.py` to component details (shared frontmatter parser, chunk ID parser, content loader, keyword extraction)
  - Update module dependency graph to show utils.py
  - Add `tests/` to file structure
  - Update Security Considerations: note that pickle was removed
- **Dependencies:** All FIX-* tasks. Blocks DOC-009, DOC-010.

---

### DOC-005: Update cortex-spec.md

- **Status:** Open
- **File:** `docs/cortex-spec.md`
- **Scope:**
  - Bump version to 2.3.0
  - Update Section 4.3 (Vector Index): storage format changed from pickle to numpy/JSON
  - Update Appendix A (File Structure): `.pkl` → `.npy` + `.ids.json`
  - Add mention of `core/utils.py` shared utilities
  - Add mention of test infrastructure
- **Dependencies:** All FIX-* tasks. Blocks DOC-009, DOC-010.

---

### DOC-006: Update decisions.md

- **Status:** Open
- **File:** `docs/decisions.md`
- **Scope:** Add new ADRs:
  - **ADR-022: Shared Utility Module** — Decision to create `core/utils.py` for frontmatter parsing, chunk ID parsing, content loading, and keyword extraction. Rationale: DRY consolidation found during team review. No YAML library added (consistent with ADR-003).
  - **ADR-023: Test Strategy** — Decision to add focused automated tests (~25-30). Rationale: v2.1.1 bug proved interface tests are needed. Scope: pure function unit tests, CLI-to-core interface tests, file I/O round-trip tests. Not pursuing exhaustive coverage.
  - **ADR-024: Replace Pickle with NumPy/JSON Serialization** — Decision to remove pickle from index serialization. Rationale: eliminates arbitrary code execution risk at zero functionality cost. Amends ADR-002.
- **Dependencies:** All FIX-* tasks. Blocks DOC-009, DOC-010.

---

### DOC-007: Update development-history.md

- **Status:** Open
- **File:** `docs/development-history.md`
- **Scope:**
  - Add v2.3.0 section documenting:
    - Context-aware team review process (3 reviewers, 2 rounds)
    - How 18 initial findings were filtered to 10 confirmed after reading all ADRs
    - Bug fixes (FIX-001, FIX-003)
    - Pickle replacement (FIX-002)
    - Shared utility module creation (FIX-004, FIX-006, FIX-007, FIX-008)
    - Test infrastructure addition (FIX-005)
    - Cleanup (FIX-009, FIX-010)
  - Complete the v2.2.0 verification checklist (currently 0/6 items checked)
  - Add v2.3.0 verification checklist
- **Dependencies:** All FIX-* tasks. Blocks DOC-009, DOC-010.

---

### DOC-008: Update user-guide.md

- **Status:** Open
- **File:** `docs/user-guide.md`
- **Scope:**
  - Bump version references to 2.3.0
  - Add section on running tests (for contributors/developers)
  - Update any references to index file format if user-facing
  - Note migration steps from v2.2.0 (index rebuild required if pickle replaced)
- **Dependencies:** All FIX-* tasks. Blocks DOC-009, DOC-010.

---

## Documentation — New Documents (Phase 7)

### DOC-009: Create release-notes-v2.3.0.md

- **Status:** Open
- **File:** `docs/release-notes-v2.3.0.md` (new)
- **Scope:** Full release notes for v2.3.0 covering:
  - Overview: Code quality improvements, shared utilities, test infrastructure, security hardening
  - What's Fixed: FIX-001 (index crash), FIX-003 (extractor bug), FIX-010 (retrieve default)
  - What's Changed: FIX-002 (pickle → numpy/JSON), FIX-004/006/007/008 (shared utils), FIX-009 (removed unused param)
  - What's New: Test infrastructure (FIX-005), `core/utils.py`, 3 new ADRs
  - Migration from v2.2.0: Index rebuild required (format change), no breaking API changes
  - Files Changed: list of all modified and new files
- **Dependencies:** DOC-001 through DOC-008 (all doc updates must be final first).

---

### DOC-010: Create session-protocol-v2.3.0.md

- **Status:** Open
- **File:** `docs/session-protocol-v2.3.0.md` (new)
- **Scope:**
  - Based on session-protocol-v2.2.0.md (copy as starting point)
  - Update version to v2.3.0
  - Document what changed from v2.2.0:
    - Index file format: `.pkl` replaced with `.npy` + `.ids.json` (affects `index` command internals, not user-facing behavior)
    - No changes to CLI invocation pattern, natural language triggers, or context budget
    - No changes to agent activation flow or protocol layers
  - If session protocol is truly unchanged in behavior, this document should be brief — noting that v2.3.0 changes are internal (code quality, shared utilities, tests) with no protocol changes
- **Dependencies:** DOC-001 through DOC-008 (all doc updates must be final first).

---

## Dismissed Findings (do not fix)

These were reviewed against the full documentation and confirmed as intentional design decisions:

| Finding | Reason | Citation |
|---------|--------|----------|
| Path traversal in delete | IDs are system-generated; local threat model | Architecture: Security |
| sys.path.insert boilerplate | Engine path resolution by design | ADR-019 |
| No env var validation | ValueError is correct behavior | Spec Appendix C |
| Version mismatch CLI/core | Already fixed in v2.1.0 | CHANGELOG |
| Redundant re.IGNORECASE | Defensive coding, negligible cost | — |
| No atomic writes | Single-user CLI; rebuild is recovery | ADR-002 |
| Full scan O(n) | Designed for <500 vectors | ADR-002 |
| No custom error hierarchy | <5 error conditions; stdlib sufficient | Simplicity philosophy |
| Silent index load failure | Missing index = normal pre-chunk state | Session protocol |
| Unused RetrievalResult dataclass | Dead code, not architectural flaw | — |
| Flat memory storage | Intentional — memories span domains | Architecture doc |

---

## Architecture Verdict

**Strong — minor housekeeping recommended.** Re-confirmed by all three reviewers after reading all 21 ADRs and full documentation.

---

*Generated by context-aware team review, 2026-02-11. Updated with documentation tasks for v2.3.0 release.*
