# LC-002: No Feedback Loop

**Priority:** P1 - Address in next release
**Status:** Accepted (implementation pending)
**Category:** Legitimate Concern
**Principle Check:** Do we need this, or is static scoring sufficient?

---

## Summary

Memories have `retrieval_count` and `usefulness_score` fields, but these aren't used to:
- Promote frequently-retrieved memories
- Decay/archive rarely-used memories
- Learn which memories are actually helpful

The data exists but has no effect.

## Current Implementation

- `core/memory.py` tracks `retrieval_count` (incremented on retrieval)
- `usefulness_score` field exists but isn't populated
- `core/retriever.py` has `frequency_factor` (10% weight) but it's based on retrieval count, not usefulness

## Questions to Resolve

1. Is frequency of retrieval a good proxy for usefulness?
2. Should memories decay over time if not retrieved?
3. How would users mark memories as useful/not useful?
4. Does this add friction that hurts the "ease of use" principle?

## Options

| Option | Complexity | Value | Recommendation |
|--------|------------|-------|----------------|
| A. Do nothing | None | None | Acceptable if noise doesn't accumulate |
| B. Time-based decay only | Low | Prevents staleness | Simple, automatic |
| C. Retrieval-based promotion | Low | Already partially there | Use existing data |
| D. User feedback ("was this helpful?") | Medium | Accurate signal | Adds friction |
| E. Automatic archival of old/unused | Medium | Cleanup | May lose valuable context |

## Deep Dive

### Analysis (2026-01-27)

Investigated the codebase to understand current state:

**Infrastructure Exists:**
| Component | File:Line | Status |
|-----------|-----------|--------|
| `increment_retrieval()` | `core/memory.py:447-454` | Function exists, never called |
| `compute_frequency_score()` | `core/retriever.py:78-89` | Logic exists, would work |
| `SCORE_FREQUENCY` | `core/config.py:31` | Configured at 0.1 (10% weight) |
| Memory retrieval loop | `core/assembler.py:257-282` | Retrieves memories, doesn't track |

**Root Cause:** The `increment_retrieval()` function was implemented but never wired into the retrieval pipeline.

### Proposed Solution

**Option C: Wire up existing retrieval tracking**

Add ~3 lines to `core/assembler.py` to call `increment_retrieval()` when a memory is included in a context frame.

**Location:** Inside the memory loop (after line 279), after a memory is successfully added:

```python
# Add import at top of file
from .memory import increment_retrieval

# Inside the memory loop, after line 279 (after memories.append(result))
increment_retrieval(result['id'], project_root)
```

**Why assembler, not retriever:**
- Tracks "actually used in context" vs "matched a query"
- More meaningful signal - memory was deemed useful enough to include
- Retriever may return memories that get filtered by budget

**What this enables:**
1. Memories used in context frames get `retrieval_count` incremented
2. `last_retrieved` timestamp updated
3. Next retrieval, `frequency_score` (10% weight) contributes to ranking
4. Frequently-used memories naturally bubble up over time
5. Zero user friction - completely automatic

**What about `usefulness_score`?**
Leave at default 0.5 for now. `retrieval_count` is a reasonable proxy for usefulness. Adding explicit user feedback ("was this helpful?") would violate the simplicity principle and add friction.

**Future consideration (not now):**
- Time-based decay could be added later if noise accumulates
- Would be a separate enhancement, not part of this fix

## Decision

**Accepted - Option C: Wire up existing retrieval tracking**

Rationale:
- Minimal change (~3 lines)
- Uses existing infrastructure
- No user friction
- Aligns with simplicity principle
- Makes dead code functional

**Implementation:** Separate task created (see related tasks)

**Status change:** This evaluation task is complete. Implementation tracked separately.

---

**Guiding Principle:** The existing retrieval_count data should be used if it helps. Avoid adding user friction (no "rate this memory" prompts).
