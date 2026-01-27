# MF-002: Chunk Provenance Tracking

**Priority:** P2 - Evaluate soon, implement if validated
**Status:** Accepted (implementation pending)
**Category:** Missing Feature
**Principle Check:** Is document-chunk tracking worth the complexity?

---

## Summary

When source documents update, their chunks become stale. Currently, you must manually delete and re-chunk. There's no tracking of which chunks came from which document version.

## Current Behavior

- Chunks have `source` field (file path)
- No version or hash tracking
- No automatic invalidation on document change
- Manual delete + re-chunk required

## Questions to Resolve

1. How often do source documents change?
2. Is manual re-chunking acceptable workflow?
3. What level of tracking is sufficient?
4. Should this be automatic (watch mode) or manual?

## Options

| Option | Complexity | Automation | Recommendation |
|--------|------------|------------|----------------|
| A. Keep manual | None | None | Acceptable for stable docs |
| B. Source hash in chunk | Low | Detection only | Know when stale, manual action |
| C. Auto-invalidate on hash change | Medium | Semi-auto | Warn user, they re-chunk |
| D. Watch mode + auto-rechunk | High | Full auto | May be over-engineering |

## Deep Dive

### Analysis (2026-01-27)

**Current chunk metadata:**
```yaml
id: CHK-CORTEX-001-001
source_doc: DOC-CORTEX-001      # Document ID, not file path
source_section: "Executive Summary"
source_lines: [10, 22]
tokens: 137
keywords: [...]
created: "2026-01-26T16:01:57"
```

**What's missing:**
- No original file path stored
- No hash/fingerprint of source content
- No way to detect if source file changed after chunking

**The Problem:**
When user edits a source document, chunks become stale but there's no detection. User must remember to re-chunk manually.

### Options Evaluated

| Option | Complexity | Automation | Recommendation |
|--------|------------|------------|----------------|
| A. Keep manual | None | None | No visibility into staleness |
| B. Source hash in chunk | Low | Detection only | Simple, provides visibility |
| C. Auto-invalidate | Medium | Semi-auto | More complexity |
| D. Watch mode | High | Full auto | Over-engineering |

### Selected: Option B - Source Hash Detection

**New fields added to chunk metadata:**
```yaml
source_path: "docs/architecture.md"    # Original file path
source_hash: "a1b2c3d4e5f6..."         # MD5/SHA256 of file content
```

**How detection works:**

1. **During chunking:** Compute hash of source file, store in chunk
2. **During status check:**
   - Read chunk's `source_path` and `source_hash`
   - Compute current file's hash
   - Compare: if different → stale
3. **Report to user:** "5 chunks from architecture.md are stale"
4. **User action:** Run refresh command to re-chunk

**User workflow:**
```
Session start
    │
    ▼
cortex status
    │
    ▼
"⚠️ STALE: docs/architecture.md (5 chunks)"
    │
    ▼
User says: "refresh stale chunks"
    │
    ▼
Agent runs: cortex chunk --path "docs/architecture.md" --refresh
    │
    ▼
Old chunks deleted, new chunks created, index rebuilt
```

**Key principle:** Detection only, user stays in control. No auto-deletion without user action.

### Implementation Scope

1. Add `source_path` and `source_hash` to Chunk dataclass
2. Compute and store hash during `chunk_document()`
3. Add stale detection to `cortex status`
4. Add `--refresh` flag to chunk command (delete old + create new)
5. Update index after refresh

## Decision

**Accepted - Option B: Source hash detection**

Rationale:
1. Low complexity (~30-50 lines of code)
2. Provides visibility into staleness
3. User stays in control (no auto-deletion)
4. Aligns with simplicity principle
5. Clear user workflow

**Implementation:** Tasks created - see related tasks.

---

**Guiding Principle:** Start with detection (option B), only automate if manual proves burdensome.
