# MF-004: Query Refinement

**Priority:** P4 - Likely won't implement unless proven necessary
**Status:** Open
**Category:** Missing Feature
**Principle Check:** Is single-pass retrieval sufficient?

---

## Summary

If retrieval returns poor results, there's no mechanism to refine the query or expand the search. A simple "no good results → try synonyms" pass might help.

## Current Behavior

- Single query → single retrieval pass
- Returns top-k results regardless of quality
- No threshold filtering (may return low-similarity results)
- No query expansion or reformulation

## Questions to Resolve

1. How often does initial retrieval fail to find relevant content?
2. What defines "poor results"? Similarity threshold?
3. Would automatic refinement help or add latency?
4. Is manual re-query sufficient workaround?

## Options

| Option | Complexity | Latency | Recommendation |
|--------|------------|---------|----------------|
| A. Keep single-pass | None | Fast | Acceptable if retrieval quality good |
| B. Similarity threshold filter | Low | Same | Don't return junk results |
| C. Synonym expansion | Medium | 2× queries | Only if exact terms miss |
| D. LLM-based query rewrite | High | +API call | Violates local-first principle |
| E. User feedback loop | Low | Interactive | "Not what I wanted" → retry |

## Deep Dive

### Analysis (2026-01-27)

Tested retrieval quality with good vs poor queries:

| Query | Best Semantic Score | Best Match |
|-------|---------------------|------------|
| "context assembly token budget" (good) | **0.849** | CHK-CORTEX-001-003 |
| "something random unrelated xyz" (poor) | **0.810** | CHK-CORTEX-001-024 |

**Key Finding: No clear threshold separates good from bad queries**

Even gibberish returns 0.81 semantic similarity. This is a characteristic of dense embeddings - everything has some similarity to everything else. The difference between a good and poor query is only 0.039.

**Answers to Questions:**

| Question | Answer |
|----------|--------|
| 1. How often does retrieval fail? | Unclear - scores always look "good" (0.8+) |
| 2. What defines "poor results"? | Can't threshold - 0.81 for junk vs 0.85 for real |
| 3. Would refinement help? | Minimal - synonyms won't help if query is wrong |
| 4. Is manual re-query sufficient? | Yes - user can simply rephrase |

**Why this isn't a problem:**
1. Users ask natural language questions, not gibberish
2. If results don't help, users naturally rephrase
3. The agent (Claude) interprets results contextually
4. Adding refinement adds latency for marginal benefit

**Options Evaluated:**

| Option | Complexity | Value | Verdict |
|--------|------------|-------|---------|
| A. Keep single-pass | None | Current | Recommended |
| B. Similarity threshold | Low | Can't distinguish | Not useful |
| C. Synonym expansion | Medium | Minor | Over-engineering |
| D. LLM query rewrite | High | Violates local-first | Won't do |
| E. User feedback loop | Low | Already natural | Implicit |

## Decision

**Won't Implement - Single-pass retrieval is sufficient**

Rationale:
1. No clear threshold to detect "poor" results programmatically
2. Users naturally rephrase if results are unhelpful
3. Agent interprets results contextually and can ask for clarification
4. Adding refinement adds complexity and latency without clear benefit
5. Aligns with simplicity principle

---

**Guiding Principle:** Single-pass retrieval with good embeddings should be sufficient. Add refinement only if proven necessary.
