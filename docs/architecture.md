# Cortex Architecture

## Overview

Cortex is an LLM-native context management system built on the principle that LLMs process information differently than humans. It optimizes for:

- **Attention patterns** - Critical information positioned where LLMs pay most attention
- **Semantic retrieval** - Content found via embedding similarity, not manual links
- **Minimal context consumption** - Only load what's needed for the current task

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CORTEX SYSTEM                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │   CHUNKER    │    │   EMBEDDER   │    │   INDEXER    │          │
│  │              │    │              │    │              │          │
│  │ - Markdown   │───►│ - e5-small   │───►│ - NumPy      │          │
│  │ - Semantic   │    │ - 384 dims   │    │ - Pickle     │          │
│  │ - 500 tokens │    │ - Local      │    │ - Brute-force│          │
│  └──────────────┘    └──────────────┘    └──────────────┘          │
│         │                   │                   │                   │
│         └───────────────────┼───────────────────┘                   │
│                             │                                        │
│                             ▼                                        │
│                    ┌──────────────────┐                             │
│                    │    RETRIEVER     │                             │
│                    │                  │                             │
│                    │ - Query embed    │                             │
│                    │ - Similarity     │                             │
│                    │ - Multi-factor   │                             │
│                    │   scoring        │                             │
│                    └────────┬─────────┘                             │
│                             │                                        │
│         ┌───────────────────┼───────────────────┐                   │
│         │                   │                   │                   │
│         ▼                   ▼                   ▼                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   MEMORY     │  │  ASSEMBLER   │  │  EXTRACTOR   │             │
│  │   STORE      │  │              │  │              │             │
│  │              │  │ - Position   │  │ - Pattern    │             │
│  │ - CRUD       │  │ - Budget     │  │ - Confidence │             │
│  │ - Types      │  │ - Frame      │  │ - Propose    │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                             │                                        │
│                             ▼                                        │
│                    ┌──────────────────┐                             │
│                    │  CONTEXT FRAME   │                             │
│                    │                  │                             │
│                    │ [Task]     ←TOP  │                             │
│                    │ [Knowledge]      │                             │
│                    │ [Learnings]      │                             │
│                    │ [State]   ←BOT   │                             │
│                    │ [Instructions]   │                             │
│                    └──────────────────┘                             │
│                             │                                        │
│                             ▼                                        │
│                         External LLM                                 │
│                      (Claude Code, etc.)                            │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Chunker (`core/chunker.py`)

Breaks documents into semantic units optimized for retrieval.

**Algorithm:**
1. Parse markdown headers to identify sections
2. Split by headers first (preserve semantic boundaries)
3. If section > 500 tokens, split by paragraphs
4. Merge chunks < 50 tokens with neighbors
5. Add 50-token overlap at boundaries

**Output:**
- `.md` files with YAML frontmatter (metadata)
- `.npy` files with embeddings (NumPy binary)

### 2. Embedder (`core/embedder.py`)

Wraps the e5-small-v2 sentence transformer model.

**Key Features:**
- Lazy loading (model loads on first use)
- Singleton pattern (one model instance)
- e5 prefix handling (`query:` vs `passage:`)
- Normalized embeddings for cosine similarity

**Model Specs:**
| Property | Value |
|----------|-------|
| Model | intfloat/e5-small-v2 |
| Dimensions | 384 |
| Max Tokens | 512 |
| Size | ~130MB |

### 3. Indexer (`core/indexer.py`)

Builds and manages vector indices.

**Storage:**
```
.cortex/index/
├── chunks.pkl          # NumPy array of chunk embeddings
├── chunks.meta.json    # Chunk ID → metadata mapping
├── memories.pkl        # Memory embeddings
└── memories.meta.json  # Memory metadata
```

**Index Structure:**
```python
{
    'embeddings': np.ndarray,  # Shape: (n, 384)
    'ids': list[str]           # Parallel list of IDs
}
```

### 4. Retriever (`core/retriever.py`)

Performs semantic search with multi-factor scoring.

**Scoring Formula:**
```
score = 0.6 × semantic_similarity +
        0.2 × keyword_overlap +
        0.1 × recency_factor +
        0.1 × frequency_factor
```

**Factors:**
| Factor | Weight | Description |
|--------|--------|-------------|
| Semantic | 60% | Cosine similarity of embeddings |
| Keyword | 20% | Overlap between query and chunk keywords |
| Recency | 10% | Newer content scores higher |
| Frequency | 10% | Frequently retrieved content scores higher |

### 5. Memory Store (`core/memory.py`)

Manages atomic learnings from sessions.

**Memory Schema:**
```yaml
id: MEM-YYYY-MM-DD-NNN
type: factual | experiential | procedural
domain: AUTH | UI | API | DB | TEST | DEV | GENERAL
confidence: high | medium | low
keywords: [...]
learning: "The core insight"
context: "When/how this was learned"
verified: true | false
retrieval_count: N
```

### 6. Assembler (`core/assembler.py`)

Builds position-optimized context frames.

**Token Budget Allocation:**
| Section | Tokens | % |
|---------|--------|---|
| Task Definition | 2,000 | 13% |
| Retrieved Chunks | 10,000 | 65% |
| Retrieved Memories | 2,000 | 13% |
| Current State | 1,000 | 6% |
| Instructions | 500 | 3% |
| **Total** | **15,500** | **100%** |

**Position Strategy:**
Based on "lost in middle" research showing U-shaped attention:
- TOP (primacy zone): Task definition - high attention
- MIDDLE: Supporting knowledge and learnings
- BOTTOM (recency zone): State and instructions - high attention

### 7. Extractor (`core/extractor.py`)

Detects learnings in session text.

**Pattern Categories:**
| Category | Confidence | Triggers |
|----------|------------|----------|
| Verified fixes | High | "fixed by", "issue was" |
| Explicit notes | High | "remember:", "note:" |
| Discoveries | Medium | "found that", "turns out" |
| Requirements | Medium | "requires", "needs" |
| Rules | Medium | "always", "never", "must" |
| Facts | Low | "uses", "expects" |

## Data Flow

### Document Ingestion
```
Document → Chunker → Chunks → Embedder → Embeddings → Indexer → Index
```

### Query Processing
```
Task → Embedder → Query Vector → Retriever → Ranked Results → Assembler → Context Frame
```

### Memory Lifecycle
```
Session → Extractor → Proposed Memories → User Approval → Memory Store → Indexer → Index
```

## Storage Layout

```
.cortex/
├── chunks/
│   └── {DOMAIN}/
│       ├── CHK-{DOMAIN}-{DOC}-{SEQ}.md   # Content + frontmatter
│       └── CHK-{DOMAIN}-{DOC}-{SEQ}.npy  # Embedding
├── memories/
│   ├── MEM-{DATE}-{SEQ}.md               # Memory content
│   └── MEM-{DATE}-{SEQ}.npy              # Embedding
├── index/
│   ├── chunks.pkl                         # Consolidated chunk embeddings
│   ├── chunks.meta.json                   # Chunk metadata
│   ├── memories.pkl                       # Consolidated memory embeddings
│   └── memories.meta.json                 # Memory metadata
└── cache/
    └── embeddings/                        # Future: embedding cache
```

## Performance Characteristics

| Operation | Complexity | Typical Time |
|-----------|------------|--------------|
| Chunk document | O(n) | ~100ms per 1000 tokens |
| Embed text | O(1) | ~50ms per chunk |
| Build index | O(n) | ~10ms per 100 chunks |
| Retrieve top-k | O(n) | <1ms for 500 vectors |
| Assemble context | O(k) | ~100ms |

## Security Considerations

- **Local Processing**: All embeddings computed locally (no data leaves machine)
- **No Secrets**: Never chunk files containing API keys or credentials
- **File Permissions**: `.cortex/` inherits project permissions
