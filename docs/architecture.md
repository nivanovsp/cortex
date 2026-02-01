# Cortex Architecture

**Version:** 1.3.0

## Overview

Cortex is an LLM-native context management system built on the principle that LLMs process information differently than humans. It optimizes for:

- **Attention patterns** - Critical information positioned where LLMs pay most attention
- **Semantic retrieval** - Content found via embedding similarity, not manual links
- **Minimal context consumption** - Only load what's needed for the current task
- **Content freshness** - Track source changes and detect stale chunks (v1.2.0)
- **Agent orchestration** - Specialist modes layered on top of the core system (v1.3.0)

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CORTEX SYSTEM (v1.3.0)                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │                    CLI LAYER (cli/)                         │     │
│  │  python -m cli <command>     Cross-platform (Typer)        │     │
│  └────────────────────────────────────────────────────────────┘     │
│                             │                                        │
│                             ▼                                        │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │   CHUNKER    │    │   EMBEDDER   │    │   INDEXER    │          │
│  │              │    │              │    │              │          │
│  │ - Markdown   │───►│ - e5-small   │───►│ - NumPy      │          │
│  │ - Semantic   │    │ - 384 dims   │    │ - Pickle     │          │
│  │ - 500 tokens │    │ - Local      │    │ - Brute-force│          │
│  │ - Provenance │    │              │    │              │          │
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
│  │ - Tracking   │  │ - Tracking   │  │              │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│         ▲                   │                                        │
│         │                   │                                        │
│         └───────────────────┘  Retrieval feedback loop (v1.2.0)    │
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
2. Compute source file hash (SHA256) for provenance tracking (v1.2.0)
3. Split by headers first (preserve semantic boundaries)
4. If section > 500 tokens, split by paragraphs
5. Merge chunks < 50 tokens with neighbors
6. Add 50-token overlap at boundaries

**Output:**
- `.md` files with YAML frontmatter (metadata + provenance)
- `.npy` files with embeddings (NumPy binary)

**Provenance Tracking (v1.2.0):**

Each chunk stores its source file information:
```yaml
source_path: "docs/architecture.md"   # Relative path to source
source_hash: "a1b2c3d4e5f6..."        # SHA256 of source content
```

This enables:
- **Stale detection**: Compare stored hash vs current file hash
- **Refresh workflow**: Delete old chunks, create new ones
- **Traceability**: Know exactly where each chunk came from

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
last_retrieved: "ISO timestamp"
```

**Retrieval Tracking (v1.2.0):**

When a memory is included in a context frame, the system automatically:
1. Increments `retrieval_count`
2. Updates `last_retrieved` timestamp

This creates a feedback loop where frequently-used memories rank higher in future retrievals (10% weight in scoring formula).

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

## Stale Detection & Refresh (v1.2.0)

Cortex tracks source file changes to ensure context is current.

### Detection Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ cli status  │────►│ Read chunks │────►│Compare hash │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                    ┌──────────────────────────┴──────────────────────────┐
                    │                                                      │
                    ▼                                                      ▼
           ┌───────────────┐                                    ┌───────────────┐
           │ Hash matches  │                                    │ Hash differs  │
           │   (fresh)     │                                    │   (stale)     │
           └───────────────┘                                    └───────┬───────┘
                                                                        │
                                                                        ▼
                                                               ┌───────────────┐
                                                               │ Report stale  │
                                                               │ chunks to user│
                                                               └───────────────┘
```

### Refresh Flow

```
┌──────────────────────┐     ┌──────────────────┐     ┌─────────────┐
│ cli chunk --refresh  │────►│ Find old chunks  │────►│Delete old   │
└──────────────────────┘     │ by source_path   │     │chunks       │
                             └──────────────────┘     └──────┬──────┘
                                                             │
                                                             ▼
                                                      ┌─────────────┐
                                                      │Create new   │
                                                      │chunks       │
                                                      └──────┬──────┘
                                                             │
                                                             ▼
                                                      ┌─────────────┐
                                                      │cli index    │
                                                      │(rebuild)    │
                                                      └─────────────┘
```

---

## Storage Layout

```
.cortex/
├── chunks/
│   └── {DOMAIN}/
│       ├── CHK-{DOMAIN}-{DOC}-{SEQ}.md   # Content + frontmatter + provenance
│       └── CHK-{DOMAIN}-{DOC}-{SEQ}.npy  # Embedding
├── memories/
│   ├── MEM-{DATE}-{SEQ}.md               # Memory content + tracking
│   └── MEM-{DATE}-{SEQ}.npy              # Embedding
├── index/
│   ├── chunks.pkl                         # Consolidated chunk embeddings
│   ├── chunks.meta.json                   # Chunk metadata
│   ├── memories.pkl                       # Consolidated memory embeddings
│   └── memories.meta.json                 # Memory metadata
└── cache/
    └── embeddings/                        # Future: embedding cache
```

### Chunk Frontmatter (v1.2.0)

```yaml
id: CHK-AUTH-001-001
source_doc: DOC-AUTH-001
source_section: "Token Refresh"
source_lines: [10, 45]
source_path: "docs/auth/tokens.md"      # v1.2.0
source_hash: "a1b2c3d4e5f6..."          # v1.2.0
tokens: 487
keywords: ["token", "refresh", "auth"]
created: "2026-01-27T10:00:00"
last_retrieved: null
retrieval_count: 0
```

## Performance Characteristics

| Operation | Complexity | Typical Time |
|-----------|------------|--------------|
| Chunk document | O(n) | ~100ms per 1000 tokens |
| Embed text | O(1) | ~50ms per chunk |
| Build index | O(n) | ~10ms per 100 chunks |
| Retrieve top-k | O(n) | <1ms for 500 vectors |
| Assemble context | O(k) | ~100ms |

## CLI Layer (v1.2.0)

The CLI layer (`cli/`) provides a cross-platform interface using Python and Typer.

### Structure

```
cli/
├── __init__.py         # Package init
├── __main__.py         # python -m cli entry point
├── main.py             # Typer app with command registration
└── commands/
    ├── init.py         # cortex init
    ├── chunk.py        # cortex chunk
    ├── index.py        # cortex index
    ├── retrieve.py     # cortex retrieve
    ├── assemble.py     # cortex assemble
    ├── memory.py       # cortex memory add/list/delete
    ├── extract.py      # cortex extract
    └── status.py       # cortex status
```

### Design Principles

- **Single codebase**: One Python CLI works on Windows, Mac, Linux
- **Thin wrapper**: Commands call core modules directly
- **Lazy imports**: Core modules loaded only when needed
- **Natural defaults**: Sensible defaults, minimal required args

---

## Session Protocol (v1.2.0)

The Semi-Auto Session Protocol defines how agents interact with Cortex throughout a working session.

### Session Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     SEMI-AUTO SESSION PROTOCOL (v1.2.0)                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────┐                                                      │
│  │  SESSION START │  Agent awakens                                       │
│  └───────┬────────┘                                                      │
│          │                                                               │
│          ▼                                                               │
│  ┌────────────────┐                                                      │
│  │ cli status     │  Metadata only (~50 tokens)                         │
│  │                │  • Chunk count                                       │
│  │  [AUTOMATIC]   │  • Memory count                                      │
│  │                │  • Domains available                                 │
│  └───────┬────────┘  • Stale chunks (v1.2.0)                            │
│          │                                                               │
│          ▼                                                               │
│  ┌────────────────┐                                                      │
│  │ TASK DETECTED  │  User specifies what to work on                     │
│  │                │  "Let's work on password reset"                      │
│  └───────┬────────┘                                                      │
│          │                                                               │
│          ▼                                                               │
│  ┌────────────────┐                                                      │
│  │ cli assemble   │  Retrieves relevant context (~2,500 tokens)         │
│  │                │  • Relevant chunks                                   │
│  │  [AUTOMATIC]   │  • Relevant memories (tracking updated)             │
│  │                │  • Position-optimized frame                          │
│  └───────┬────────┘                                                      │
│          │                                                               │
│          ▼                                                               │
│  ┌────────────────┐                                                      │
│  │   WORK PHASE   │◄─────────────────────────────┐                      │
│  └───────┬────────┘                              │                      │
│          │                                       │                      │
│          ▼                                       │                      │
│  ┌────────────────┐                              │                      │
│  │ MORE CONTEXT?  │  User asks naturally:        │                      │
│  │                │  "What do we know about X?"  │                      │
│  │ [USER-DRIVEN]  │  "Get details on Y"          │                      │
│  └───────┬────────┘                              │                      │
│          │                                       │                      │
│          ▼                                       │                      │
│  ┌────────────────┐                              │                      │
│  │ cli retrieve   │  On-demand retrieval         │                      │
│  │                │  (~1,500 tokens per query)   │                      │
│  │  [AUTOMATIC]   │                              │                      │
│  └───────┬────────┘                              │                      │
│          │                                       │                      │
│          └───────────────────────────────────────┘                      │
│                                                                          │
│          ▼                                                               │
│  ┌────────────────┐                                                      │
│  │  SESSION END   │  User triggers:                                     │
│  │                │  "Update learning"                                   │
│  │ [USER-TRIGGER] │  "Save learnings"                                   │
│  └───────┬────────┘                                                      │
│          │                                                               │
│          ▼                                                               │
│  ┌────────────────┐                                                      │
│  │ cli extract    │  Proposes memories                                  │
│  │ cli index      │  User approves                                      │
│  │                │  Index rebuilt                                       │
│  │  [AUTOMATIC]   │                                                      │
│  └────────────────┘                                                      │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Context Budget by Phase

| Phase | Tokens | % of 200k |
|-------|--------|-----------|
| Session start (metadata) | ~50 | 0.025% |
| Task context (assembly) | ~2,500 | 1.25% |
| On-demand retrieval (×2) | ~3,000 | 1.5% |
| **Typical total** | **~5,550** | **2.8%** |

*Assumes 2 retrievals per session. Heavy debugging may reach 10-15%.*

### Trigger Detection

The agent detects user intent through natural language patterns:

| Phase | Trigger Type | Examples |
|-------|--------------|----------|
| Task Start | Implicit | "Let's work on...", "Help me with..." |
| Retrieval | Natural | "What do we know about...", "Tell me about..." |
| Retrieval | Explicit | "cortex: {query}" |
| Session End | User command | "Update learning", "Save learnings" |

---

## Agent Orchestration Layer (v1.3.0)

Cortex v1.3.0 adds an agent orchestration layer — expert modes that layer on top of the session protocol.

### Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    AGENT ORCHESTRATION (v1.3.0)                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │               LAYER 1: AGENT MODE (optional)               │     │
│  │                                                            │     │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐    │     │
│  │  │ Analyst  │ │ Architect│ │Developer │ │ UX       │    │     │
│  │  │          │ │          │ │          │ │ Designer │    │     │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘    │     │
│  │                    ┌──────────┐                           │     │
│  │                    │Orchestr. │  (plans which mode next)  │     │
│  │                    └──────────┘                           │     │
│  └────────────────────────────┬───────────────────────────────┘     │
│                               │                                      │
│                               ▼                                      │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │               LAYER 0: SESSION PROTOCOL (always)           │     │
│  │                                                            │     │
│  │  status ──► assemble ──► retrieve ──► extract              │     │
│  └────────────────────────────┬───────────────────────────────┘     │
│                               │                                      │
│                               ▼                                      │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │               CORE SYSTEM                                  │     │
│  │  Chunker → Embedder → Indexer → Retriever → Assembler     │     │
│  └────────────────────────────────────────────────────────────┘     │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Design Principles

- **Additive, not replacement** — Modes layer on top; the session protocol always runs
- **Single-source specs** — Agent definitions in `agents/` are the source of truth
- **Tool-agnostic** — Specs work with any LLM tool; Claude Code wrappers are thin
- **Zero context cost** — Modes don't consume Cortex retrieval budget
- **Planning, not spawning** — Orchestrator plans phases; user activates modes

### File Structure

```
agents/                              # Tool-agnostic specs (source of truth)
├── README.md
├── modes/
│   ├── analyst.md
│   ├── architect.md
│   ├── developer.md
│   ├── ux-designer.md
│   └── orchestrator.md
└── skills/
    ├── qa-gate.md
    └── extract-learnings.md

.claude/commands/                    # Claude Code thin wrappers
├── modes/{name}.md                  # "Read agents/modes/{name}.md, adopt persona"
└── skills/{name}.md                 # "Read agents/skills/{name}.md, execute skill"
```

### Mode Interaction with Core

Each mode specifies which Cortex commands and memory domains it prioritizes:

| Mode | Primary Domains | Primary Commands |
|------|----------------|-----------------|
| Analyst | GENERAL, API, DB | retrieve, assemble |
| Architect | API, DB, DEV | retrieve, assemble, memory add |
| Developer | All | All commands |
| UX Designer | UI | retrieve, assemble, memory add |
| Orchestrator | All | retrieve, assemble, memory add |

---

## Security Considerations

- **Local Processing**: All embeddings computed locally (no data leaves machine)
- **No Secrets**: Never chunk files containing API keys or credentials
- **File Permissions**: `.cortex/` inherits project permissions
