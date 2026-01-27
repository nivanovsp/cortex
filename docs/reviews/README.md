# Cortex Review Topics

> **Guiding Principle:** Simplicity and ease of use. We do not overcomplicate things.

This folder tracks discussion topics from the independent expert review (2026-01-27). Each document captures a concern or gap, with space for deep-dive analysis and decisions.

## Decision Framework

Before adding complexity, ask:
1. Does this solve a problem users actually have?
2. Is the simplest solution sufficient?
3. Does the benefit justify the added complexity?
4. Can we defer this until proven necessary?

**Default stance:** Don't implement unless clear value is demonstrated.

## Priority Definitions

| Priority | Meaning | Action |
|----------|---------|--------|
| **P1** | Address in next release | Low effort, high value, or honesty issue |
| **P2** | Evaluate soon | Implement if validated |
| **P3** | Defer until evidence | Don't solve preemptively |
| **P4** | Likely won't implement | Unless proven necessary |

## Current Approach Comparison

| Approach | Cortex Choice | Why |
|----------|---------------|-----|
| Vector DB | Local NumPy brute-force | Simple, fast at <500 vectors, no infra |
| Full-document loading | Removed | Consumes too much context |
| Graph-based relationships | Removed | Semantic similarity is simpler |
| External APIs | Local embeddings | Free, private, no dependencies |

## Review Topics

### Legitimate Concerns

| ID | Priority | Topic | Status | Document |
|----|----------|-------|--------|----------|
| LC-004 | **P1** | Context Claim Accuracy | **Completed** | [context-claim.md](./context-claim.md) |
| LC-002 | **P1** | No Feedback Loop | **Implemented v1.2.0** | [feedback-loop.md](./feedback-loop.md) |
| LC-001 | P2 | Pattern-Based Extraction | **Deferred** | [pattern-extraction.md](./pattern-extraction.md) |
| LC-003 | P3 | Embedding Model Choice | **Deferred** | [embedding-model.md](./embedding-model.md) |
| LC-005 | P3 | Windows-Centric CLI | **Implemented v1.2.0** | [cross-platform.md](./cross-platform.md) |

### Missing Features

| ID | Priority | Topic | Status | Document |
|----|----------|-------|--------|----------|
| MF-002 | P2 | Chunk Provenance Tracking | **Implemented v1.2.0** | [chunk-provenance.md](./chunk-provenance.md) |
| MF-001 | P3 | Semantic Deduplication | **Won't Implement** | [semantic-dedup.md](./semantic-dedup.md) |
| MF-003 | P4 | Memory Confidence Calibration | **Won't Implement** | [confidence-calibration.md](./confidence-calibration.md) |
| MF-004 | P4 | Query Refinement | **Won't Implement** | [query-refinement.md](./query-refinement.md) |

## Status Legend

- **Open** - Under discussion
- **Accepted** - Will implement
- **Deferred** - Valid but not now
- **Rejected** - Won't implement (with rationale)
