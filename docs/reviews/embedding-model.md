# LC-003: Embedding Model Choice

**Priority:** P3 - Defer until evidence of need
**Status:** Deferred
**Category:** Legitimate Concern
**Principle Check:** Is e5-small-v2 good enough, or are we leaving quality on the table?

---

## Summary

e5-small-v2 (384 dimensions, 512 token max) was chosen for:
- Local execution (no API costs)
- Privacy (no data leaves machine)
- Size (~130MB)

However, for code/technical content, domain-specific models (CodeBERT, etc.) might perform better.

## Current Implementation

- `core/embedder.py` uses `intfloat/e5-small-v2`
- Configurable via `CORTEX_EMBEDDING_MODEL` env var
- Lazy-loading singleton pattern

## Questions to Resolve

1. Has retrieval quality been tested against code-specific models?
2. What's the actual quality difference for technical content?
3. Is the 512 token limit causing truncation issues?
4. Would larger e5 variants (base, large) be worth the size increase?

## Options

| Option | Size | Quality | Local | Recommendation |
|--------|------|---------|-------|----------------|
| A. Keep e5-small-v2 | 130MB | Good | Yes | Default choice |
| B. e5-base-v2 | 440MB | Better | Yes | If quality issues proven |
| C. CodeBERT | 500MB | Best for code | Yes | Only if code-heavy projects |
| D. OpenAI embeddings | N/A | Excellent | No | Violates local-first principle |
| E. Make easily swappable | N/A | Flexible | Varies | Already supported via env var |

## Deep Dive

### Analysis (2026-01-27)

**Existing Documentation:** ADR-001 in `docs/decisions.md` already documents this choice thoroughly.

**Key Points from ADR-001:**

| Factor | API-based | Local (e5-small-v2) |
|--------|-----------|---------------------|
| Cost | Per-request fees | Free |
| Privacy | Data sent externally | Data stays local |
| Latency | Network round-trip | ~50ms local |
| Offline | No | Yes |
| Quality | Excellent | Good (sufficient) |

**Already Swappable:**
- `CORTEX_EMBEDDING_MODEL` env var allows changing models
- Power users can already switch to different models if needed
- No code changes required to use a different model

**Chunk Size Alignment:**
- Chunk size (500 tokens) was specifically chosen to match e5-small-v2's 512 token limit
- No truncation issues with current configuration
- Changing models may require reconsidering chunk size

**Evidence Assessment:**
- No reported quality issues with current model
- No benchmarks comparing e5-small-v2 vs alternatives for this use case
- System works as designed

### Conclusion

This is a theoretical concern without supporting evidence. The model choice is sound, well-documented, and already swappable for users who need different characteristics.

Benchmarking effort is not justified without actual quality complaints.

## Decision

**Deferred - No evidence of need**

Rationale:
1. No reported quality issues
2. Model already swappable via env var
3. ADR-001 documents the trade-offs well
4. Benchmarking effort not justified without complaints
5. Aligns with simplicity principle

**Future Trigger:** Revisit if users report poor retrieval quality for code/technical content. At that point, conduct actual benchmarks comparing:
- e5-small-v2 (current)
- e5-base-v2 (larger, potentially better)
- Code-specific models (CodeBERT, etc.)

**No action required at this time.**

---

**Guiding Principle:** Local-first, no API costs. Only change if measurable quality improvement for actual use cases.
