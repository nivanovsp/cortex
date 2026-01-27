# LC-001: Pattern-Based Extraction is Brittle

**Priority:** P2 - Evaluate soon, implement if validated
**Status:** Deferred
**Category:** Legitimate Concern
**Principle Check:** Simplicity vs. robustness tradeoff

---

## Summary

The extractor uses regex patterns (`fixed by`, `remember:`, `found that`) to detect learnings. This misses:
- Novel phrasings ("The culprit was...", "Turns out...")
- Non-English sessions
- Implicit learnings not explicitly stated

## Current Implementation

Located in `core/extractor.py`. Uses ~12 regex patterns grouped by confidence level.

## Questions to Resolve

1. How often do users actually miss learnings due to pattern limitations?
2. Would a semantic classifier add unacceptable complexity?
3. Is "explicit trigger" (`remember: X`) sufficient as workaround?
4. Do we have evidence this is a real problem vs. theoretical concern?

## Options

| Option | Complexity | Effectiveness | Recommendation |
|--------|------------|---------------|----------------|
| A. Keep current patterns | None | Known gaps | Acceptable if gaps rare |
| B. Add more patterns | Low | Incremental | Easy win if patterns identified |
| C. Semantic classifier | High | Better coverage | Violates simplicity principle |
| D. Hybrid: patterns + LLM fallback | Medium | Good | Only if proven necessary |

## Deep Dive

### Analysis (2026-01-27)

**Reviewed:** `core/extractor.py` - 11 extraction patterns across 3 confidence levels.

**Pattern Coverage:**

| Confidence | Count | Examples |
|------------|-------|----------|
| High | 3 | `fixed by X`, `the issue was X`, `remember: X` |
| Medium | 6 | `found that X`, `turns out X`, `always/never X` |
| Low | 2 | `X uses Y`, `X is located in Y` |

**Key Findings:**

1. **"Turns out" IS covered** - Initially flagged as missing, but exists at line 55-60
2. **Explicit escape hatch exists** - `remember: X`, `note: X`, `important: X` forces high-confidence capture
3. **Domain auto-detection** - Keywords map to AUTH, UI, API, DB, TEST, DEV, GENERAL
4. **Adding patterns is trivial** - ~5 lines per new pattern

**Evidence Assessment:**
- No reported missed learnings
- Explicit trigger provides user control
- Pattern set covers common phrasings for fixes, discoveries, procedures

### Workaround Documentation

Users can force memory capture with explicit triggers:
```
remember: FormField wrapper is required for PasswordInput
note: Always run migrations before seeding
important: API tokens expire after 24 hours
```

These trigger high-confidence extraction regardless of phrasing.

## Decision

**Deferred - No evidence of need**

Rationale:
1. Current 11 patterns cover common phrasings
2. Explicit trigger (`remember: X`) provides escape hatch
3. No reported missed learnings in practice
4. Adding patterns is trivial (~5 lines) if gaps identified
5. Semantic classifier would violate simplicity principle

**Future Trigger:** If users report specific phrasings that weren't captured, add those patterns. Each new pattern is ~5 lines of code.

**Documentation Action:** Consider making the explicit trigger (`remember: X`) more prominent in user documentation.

**No code changes required at this time.**

---

**Guiding Principle:** Simplicity first. Only add complexity if pattern gaps prove problematic in actual use.
