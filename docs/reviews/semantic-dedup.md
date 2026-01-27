# MF-001: Semantic Deduplication

**Priority:** P3 - Defer until evidence of need
**Status:** Open
**Category:** Missing Feature
**Principle Check:** Is deduplication necessary, or does retrieval scoring handle it?

---

## Summary

When chunking multiple related documents, semantically identical chunks can exist. Two chunks saying the same thing in different words both get retrieved, wasting context budget.

## Current Behavior

- No deduplication during chunking or retrieval
- Similar chunks may both appear in results
- Retrieval returns top-k by score without similarity filtering

## Questions to Resolve

1. How often does this actually happen in practice?
2. Does the multi-factor scoring naturally separate duplicates?
3. What similarity threshold defines "duplicate"?
4. Should dedup happen at chunk time or retrieval time?

## Options

| Option | Complexity | When | Recommendation |
|--------|------------|------|----------------|
| A. Do nothing | None | N/A | If problem is rare |
| B. Retrieval-time dedup | Low | Query | Filter results > 0.95 similarity |
| C. Chunk-time dedup | Medium | Index | Prevent duplicates entering index |
| D. Document-level awareness | High | Chunk | Know which doc chunks came from |

## Deep Dive

### Analysis (2026-01-27)

Analyzed similarity distribution across 24 chunks from cortex-spec.md:

**Findings:**
- 23 pairs have similarity > 0.9
- Max similarity: 0.929 (CHK-022 ↔ CHK-024)
- Mean similarity: 0.866

**Key Insight: High similarity ≠ duplicate content**

The highest-similarity pair (0.929):
- CHK-022: File structure directory tree
- CHK-024: Environment variables table

These are semantically similar (both about Cortex config/structure) but contain **different, complementary information**. A user querying "cortex structure" benefits from seeing both.

**Answers to Questions:**

| Question | Answer |
|----------|--------|
| 1. How often does duplication happen? | Rarely - high similarity but distinct content |
| 2. Does scoring handle it naturally? | Yes - multi-factor scoring differentiates |
| 3. What threshold = duplicate? | Unclear - even 0.93 isn't a true duplicate |
| 4. Chunk time or retrieval time? | Neither needed |

## Decision

**Won't Implement - No evidence of need**

Rationale:
1. No actual duplicates observed in current data
2. High semantic similarity means "related topic", not "redundant content"
3. Deduplication would risk filtering out useful complementary information
4. Current behavior is desirable - users get multiple relevant perspectives
5. Aligns with simplicity principle: don't solve problems that don't exist

---

**Guiding Principle:** Only implement if duplicate retrieval is actually wasting context in practice.
