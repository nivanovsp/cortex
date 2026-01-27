# LC-004: Context Claim Accuracy

**Priority:** P1 - Address in next release
**Status:** Completed
**Category:** Legitimate Concern
**Principle Check:** Is the "2.8% context" claim misleading?

---

## Summary

The documentation claims ~2.8% context consumption for typical sessions. This assumes:
- Only 2 retrievals per session
- No follow-up queries
- User doesn't request extensive context

Heavy debugging sessions could hit 10-15% with multiple retrievals stacking.

## Current Numbers

| Phase | Tokens | % of 200k |
|-------|--------|-----------|
| Session start (metadata) | ~50 | 0.025% |
| Task assembly | ~2,500 | 1.25% |
| Retrieval (×2) | ~3,000 | 1.5% |
| **Claimed total** | **~5,550** | **~2.8%** |

## Questions to Resolve

1. What's actual retrieval count in real sessions?
2. Should we track and report actual usage?
3. Is the headline number marketing or accurate guidance?
4. Does the ceiling matter more than the typical case?

## Options

| Option | Effort | Value | Recommendation |
|--------|--------|-------|----------------|
| A. Keep current claim | None | May mislead | Document assumptions clearly |
| B. Add range ("2.8-15%") | Low | More honest | Better expectation setting |
| C. Track actual usage | Medium | Data-driven | Useful but adds complexity |
| D. Add context budget warnings | Medium | User awareness | May add noise |

## Deep Dive

The "2.8%" claim was accurate for its assumptions but presented without context in headlines. The assumptions (2 retrievals, no follow-ups) weren't visible to users scanning documentation.

## Decision

**Accepted - Option B: Clarify with range and assumptions**

Changes made (2026-01-27):

1. **README.md** - Updated headline:
   - Before: "~2.8% context consumption"
   - After: "~3-10% context consumption - Retrieval-based loading (vs 30%+ for full docs)"

2. **Budget tables** - Added assumptions note to:
   - `CLAUDE.md`
   - `docs/session-protocol-v1.1.0.md`
   - `docs/cortex-spec.md`
   - `docs/architecture.md`

   Note added: *"Assumes 2 retrievals per session. Heavy debugging may reach 10-15%."*

3. **Claim adjustment** - Changed "97%+" to "90%+" to reflect realistic ceiling.

4. **Historical docs** - Left CHANGELOG.md and RELEASE-NOTES unchanged (historical accuracy).

**Rationale:** Honest documentation builds trust. Users can now set accurate expectations.

---

**Guiding Principle:** Be honest about limitations. Users should understand what to expect in different scenarios.
