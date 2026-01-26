# Architecture Decision Records (ADRs)

This document records the key architectural decisions made during Cortex development.

---

## ADR-001: Local Embedding Model

**Date:** 2026-01-26
**Status:** Accepted

### Context
Need an embedding model for semantic search. Options include API-based (OpenAI, Cohere) or local models.

### Decision
Use **intfloat/e5-small-v2** running locally via sentence-transformers.

### Rationale
| Factor | API-based | Local (e5-small-v2) |
|--------|-----------|---------------------|
| Cost | Per-request fees | Free |
| Privacy | Data sent externally | Data stays local |
| Latency | Network round-trip | ~50ms local |
| Offline | No | Yes |
| Quality | Excellent | Good (sufficient for retrieval) |

### Consequences
- No API costs or rate limits
- Works offline
- ~130MB model download (one-time)
- Slightly lower quality than large API models (acceptable trade-off)

---

## ADR-002: Brute-Force Vector Index

**Date:** 2026-01-26
**Status:** Accepted

### Context
Need a vector index for similarity search. Options include specialized databases (Pinecone, Weaviate), approximate nearest neighbor libraries (FAISS, Annoy), or simple brute-force.

### Decision
Use **NumPy brute-force** with pickle serialization.

### Rationale
At expected scale (<500 vectors):
- Brute-force: <1ms search time
- Zero dependencies beyond NumPy
- No index corruption issues
- Simple rebuild if needed

Specialized solutions add complexity without benefit at this scale.

### Consequences
- Simple, reliable implementation
- May need upgrade if scale exceeds 10k+ vectors
- Easy to migrate later if needed (just swap indexer)

---

## ADR-003: Markdown with YAML Frontmatter

**Date:** 2026-01-26
**Status:** Accepted

### Context
Need a storage format for chunks and memories. Options include pure JSON, pure YAML, pure Markdown, or hybrid.

### Decision
Use **Markdown with YAML frontmatter**.

### Rationale
Research shows format processing overhead:
| Format | LLM Reasoning Degradation |
|--------|---------------------------|
| Natural Language | 0% (baseline) |
| Markdown | 2-5% |
| YAML | 8-12% |
| JSON | 10-15% |

Markdown body with minimal YAML frontmatter gives:
- Human readable
- LLM optimal (2-5% overhead)
- Structured metadata where needed
- Git-friendly (text-based diffs)

### Consequences
- Slightly more complex parsing than pure JSON
- Best balance of human and LLM readability
- Easy manual editing if needed

---

## ADR-004: Position-Aware Context Assembly

**Date:** 2026-01-26
**Status:** Accepted

### Context
Research shows LLMs exhibit "lost in middle" attention patterns - high attention at start (primacy) and end (recency), lower in middle.

### Decision
Structure context frames with **critical information at edges**.

### Structure
```
TOP (primacy zone)     → Task Definition
UPPER-MIDDLE           → Relevant Knowledge
LOWER-MIDDLE           → Past Learnings
BOTTOM (recency zone)  → Current State
VERY END               → Instructions
```

### Rationale
- Task definition needs high attention → top
- Instructions need high attention → bottom
- Supporting info can tolerate lower attention → middle

### Consequences
- More effective context utilization
- Requires careful section ordering
- May need adjustment for different LLM architectures

---

## ADR-005: Semantic Chunking Strategy

**Date:** 2026-01-26
**Status:** Accepted

### Context
Need to break documents into retrievable units. Options include fixed-size, sentence-based, or semantic chunking.

### Decision
Use **semantic-aware chunking** based on markdown structure.

### Algorithm
1. Split by markdown headers (preserve semantic boundaries)
2. If section > 500 tokens, split by paragraphs
3. Merge chunks < 50 tokens
4. Add 50-token overlap at boundaries

### Parameters
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| MAX_CHUNK_SIZE | 500 tokens | Matches e5-small-v2 max |
| MIN_CHUNK_SIZE | 50 tokens | Avoid fragments |
| OVERLAP | 50 tokens | Context continuity |

### Consequences
- Preserves semantic coherence
- Aligned with embedding model limits
- Overlap prevents information loss at boundaries

---

## ADR-006: Multi-Factor Retrieval Scoring

**Date:** 2026-01-26
**Status:** Accepted

### Context
Pure semantic similarity may not always surface the most useful results.

### Decision
Use **multi-factor scoring** combining multiple signals.

### Formula
```
score = 0.6 × semantic_similarity +
        0.2 × keyword_overlap +
        0.1 × recency_factor +
        0.1 × frequency_factor
```

### Rationale
| Factor | Weight | Why |
|--------|--------|-----|
| Semantic | 60% | Primary signal, embedding similarity |
| Keyword | 20% | Exact matches matter for technical terms |
| Recency | 10% | Newer content often more relevant |
| Frequency | 10% | Often-retrieved content proved useful |

### Consequences
- Better retrieval quality than pure semantic
- Tunable weights for different use cases
- Slightly more complex scoring logic

---

## ADR-007: Hybrid Memory Extraction

**Date:** 2026-01-26
**Status:** Accepted

### Context
Need to extract learnings from session text. Could be fully automatic, fully manual, or hybrid.

### Decision
Use **hybrid extraction with confidence thresholds**.

### Approach
| Confidence | Trigger | Action |
|------------|---------|--------|
| High | Verified fixes, explicit "remember" | Auto-save option |
| Medium | Discoveries, requirements | Propose for approval |
| Low | Inferences | Propose for approval |

### Rationale
- Fully automatic: Risk of noise
- Fully manual: Burden on user
- Hybrid: Best of both worlds

### Consequences
- User retains control
- High-confidence auto-save reduces friction
- Pattern detection may miss some learnings

---

## ADR-008: PowerShell CLI with Python Core

**Date:** 2026-01-26
**Status:** Accepted

### Context
Need a CLI interface. Options include pure Python CLI, pure PowerShell, or hybrid.

### Decision
Use **PowerShell scripts calling Python modules**.

### Rationale
- PowerShell: Native Windows integration, good UX
- Python: ML ecosystem (sentence-transformers, numpy)
- Hybrid: Best of both worlds

### Structure
```
PowerShell (CLI layer)
    │
    └──► Python (core logic)
            │
            └──► sentence-transformers, numpy, tiktoken
```

### Consequences
- Requires both PowerShell and Python
- Clean separation of concerns
- Cross-platform possible with PowerShell Core

---

## ADR-009: Token Budget System

**Date:** 2026-01-26
**Status:** Accepted

### Context
Context frames must fit within LLM context windows while maximizing useful content.

### Decision
Implement **configurable token budgets** with proportional allocation.

### Default Budget (15,000 tokens)
| Section | Tokens | % |
|---------|--------|---|
| Task Definition | 2,000 | 13% |
| Chunks | 10,000 | 65% |
| Memories | 2,000 | 13% |
| State | 1,000 | 6% |
| Instructions | 500 | 3% |

### Rationale
- 15k frame + 70k reserved (system, response) = 85k
- Leaves 115k for conversation in 200k window
- Proportions based on typical importance

### Consequences
- Predictable context consumption (~8%)
- May truncate content to fit budget
- Configurable for different needs
