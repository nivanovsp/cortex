# MF-003: Memory Confidence Calibration

**Priority:** P4 - Likely won't implement unless proven necessary
**Status:** Open
**Category:** Missing Feature
**Principle Check:** Is pattern-based confidence good enough?

---

## Summary

Memory confidence (high/medium/low) is assigned by extraction pattern, not actual correctness. A memory from "fixed by changing X" is marked high confidence, but could still be wrong. There's no verification mechanism.

## Current Behavior

- `core/extractor.py` assigns confidence by pattern type
- "fixed by" / "remember:" → high
- "found that" / "discovered" → medium
- "uses" / "expects" → low
- No post-hoc verification

## Questions to Resolve

1. Does pattern-based confidence correlate with actual accuracy?
2. How would verification work without adding friction?
3. Is "wrong memory" retrieval a real problem?
4. Should users be able to adjust confidence manually?

## Options

| Option | Complexity | Accuracy | Recommendation |
|--------|------------|----------|----------------|
| A. Keep pattern-based | None | Approximate | Acceptable as heuristic |
| B. User correction on retrieval | Low | Improves over time | "Was this helpful?" prompt |
| C. Verification pass | High | Better accuracy | Requires re-checking facts |
| D. Confidence decay over time | Low | Reduces stale confidence | Simple time-based adjustment |

## Deep Dive

### Analysis (2026-01-27)

**Current pattern-based assignment:**

| Confidence | Triggers | Rationale |
|------------|----------|-----------|
| **High** | "fixed by", "problem was", "remember:" | Verified actions, explicit notes |
| **Medium** | "found that", "turns out", "requires", "always/never" | Discoveries, rules |
| **Low** | "uses", "is located" | Factual statements that may change |

**Existing memories (3 total):**

| ID | Confidence | Verified | Learning |
|----|------------|----------|----------|
| MEM-001 | high | true | FormField wrapper required for PasswordInput |
| MEM-027 | high | false | Token refresh uses 15 min expiry |
| MEM-028 | medium | false | Always run tests before committing |

**Answers to Questions:**

| Question | Answer |
|----------|--------|
| 1. Does pattern correlate with accuracy? | Reasonable - "fixed by" more reliable than "uses" by nature |
| 2. How would verification work? | Adds friction - prompts violate simplicity |
| 3. Is wrong memory retrieval a problem? | No evidence - only 3 memories, all accurate |
| 4. User adjust confidence manually? | Already possible - can edit memory files |

**Key Observations:**
1. The heuristic is sound - a verified fix is inherently more certain than a general observation
2. Infrastructure exists but unused (`verified`, `usefulness_score` fields)
3. No calibration problem observed with current memory count
4. Adding calibration/verification adds friction without demonstrated benefit

## Decision

**Won't Implement - Pattern-based confidence is sufficient**

Rationale:
1. Pattern-based confidence is a reasonable heuristic by design
2. No evidence of wrong memories causing retrieval problems
3. Adding calibration/verification adds friction
4. `verified` field already exists for manual override if needed
5. Aligns with simplicity principle

**Future consideration:** If memory count grows large (100+) and wrong retrievals become common, revisit Option D (time-based decay).

---

**Guiding Principle:** Pattern-based confidence is a reasonable heuristic. Only add verification if wrong memories prove problematic.
