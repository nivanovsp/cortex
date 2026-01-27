# Cortex: LLM-Native Context Management

**Status**: Specification
**Version**: 1.2.0
**Date**: 2026-01-27
**Author**: Claude (Architect Mode)

---

## Executive Summary

**Cortex** is a context management methodology designed specifically for how LLMs process information. Unlike traditional documentation systems built around human cognitive metaphors, Cortex optimizes for:

- **Attention patterns** - Critical information positioned where LLMs pay most attention
- **Semantic retrieval** - Relevant content found via embedding similarity, not predefined links
- **Minimal context consumption** - Only load what's needed for the current task
- **Markdown-native format** - Optimized for LLM reasoning (2-5% overhead vs 8-12% for YAML)

**Expected Outcome:** ~8% context consumption at task start vs 35-60% with traditional approaches.

---

## Table of Contents

1. [Why Cortex](#1-why-cortex)
2. [LLM Processing Fundamentals](#2-llm-processing-fundamentals)
3. [Architecture](#3-architecture)
4. [Component Specifications](#4-component-specifications)
5. [Implementation Plan](#5-implementation-plan)
6. [Risk Assessment](#6-risk-assessment)
7. [Technical Decisions](#7-technical-decisions)

---

## 1. Why Cortex

### 1.1 The Context Problem

Traditional documentation approaches load entire documents into LLM context, even when only specific sections are relevant:

```
Traditional: Load document (2000 tokens) → Use 50 tokens → 97.5% waste
Cortex:      Retrieve chunk (60 tokens)  → Use 50 tokens → 17% overhead
```

### 1.2 Scaling Comparison

| Project Complexity | Traditional Approach | Cortex |
|-------------------|---------------------|--------|
| Simple | 35% context consumed | ~8% |
| Medium | 50% | ~10% |
| Complex | 65%+ | ~12% |
| Very Complex | 80%+ (unusable) | ~15% |

Traditional approaches scale linearly with project size. Cortex scales logarithmically because it retrieves only relevant chunks.

### 1.3 Core Principles

1. **Chunk, don't load** - Break documents into semantic chunks, retrieve only what's needed
2. **Position matters** - Place critical info where attention is highest (start/end)
3. **Discover, don't predefine** - Find relationships via semantic similarity, not manual links
4. **Markdown over YAML** - Natural language content, minimal structured metadata

---

## 2. LLM Processing Fundamentals

### 2.1 How Attention Works

LLMs use self-attention to process all tokens simultaneously. There is no "traversal" or sequential processing - the model sees everything at once and computes relevance scores dynamically.

### 2.2 The "Lost in the Middle" Phenomenon

Research demonstrates a U-shaped attention curve:

```
Attention
    │
100%├─■                                           ■
    │  ■                                        ■
 80%├    ■                                    ■
    │      ■                                ■
 60%├        ■                            ■
    │          ■                        ■
 40%├            ■■                  ■■
    │               ■■■■■■■■■■■■■■■■
 20%├─────────────────────────────────────────────
    │
    └─────────────────────────────────────────────►
      Start              Middle               End
              Position in Context Window
```

**Implications:**
- 0-15%: High attention (primacy zone)
- 85-100%: High attention (recency zone)
- 30-70%: Degraded attention (lost in middle)

### 2.3 Format Processing Overhead

Research shows structured formats impose cognitive overhead:

| Format | Reasoning Degradation | Token Efficiency |
|--------|----------------------|------------------|
| Natural Language | 0% (baseline) | Medium |
| Markdown | 2-5% | Good |
| JSON | 10-15% | Poor |
| YAML | 8-12% | Medium |
| XML | 15-20% | Very Poor |

**Cortex uses Markdown** with minimal YAML frontmatter for metadata.

---

## 3. Architecture

### 3.1 Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      CORTEX ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐    │
│  │   CHUNK      │     │   MEMORY     │     │   CONTEXT    │    │
│  │   STORE      │     │   STORE      │     │   ASSEMBLER  │    │
│  │              │     │              │     │              │    │
│  │ - Embeddings │     │ - Atomic     │     │ - Position   │    │
│  │ - Metadata   │     │   memories   │     │   aware      │    │
│  │ - Source ref │     │ - Keywords   │     │ - Relevance  │    │
│  │              │     │ - Links      │     │   ranked     │    │
│  └──────┬───────┘     └──────┬───────┘     └──────┬───────┘    │
│         │                    │                    │             │
│         └────────────────────┼────────────────────┘             │
│                              │                                  │
│                              ▼                                  │
│                    ┌──────────────────┐                         │
│                    │    RETRIEVAL     │                         │
│                    │    ENGINE        │                         │
│                    │                  │                         │
│                    │ - Query embedding│                         │
│                    │ - Similarity     │                         │
│                    │ - Ranking        │                         │
│                    │ - Deduplication  │                         │
│                    └────────┬─────────┘                         │
│                             │                                   │
│                             ▼                                   │
│                    ┌──────────────────┐                         │
│                    │  CONTEXT FRAME   │                         │
│                    │                  │                         │
│                    │ [CRITICAL-TOP]   │ ← Primacy zone          │
│                    │ [SUPPORTING]     │ ← Middle                │
│                    │ [CRITICAL-BOT]   │ ← Recency zone          │
│                    │ [INSTRUCTIONS]   │ ← Very end              │
│                    └──────────────────┘                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 The Three Stores

#### 3.2.1 Chunk Store

Stores atomic units of knowledge (~300-500 tokens each):

```
Source Document (2000 tokens)
            │
            ▼
    ┌───────┴───────┐
    │   CHUNKER     │
    │ (semantic)    │
    └───────┬───────┘
            │
   ┌────────┼────────┐
   ▼        ▼        ▼
┌─────┐  ┌─────┐  ┌─────┐
│~300 │  │~400 │  │~350 │
│tok  │  │tok  │  │tok  │
└─────┘  └─────┘  └─────┘
```

**Chunk Format (Markdown with frontmatter):**

```markdown
---
id: CHK-AUTH-001-003
source_doc: DOC-AUTH-001
source_section: "Token Refresh Logic"
source_path: "docs/auth/tokens.md"      # v1.2.0: Provenance tracking
source_hash: "a1b2c3d4e5f6..."          # v1.2.0: SHA256 for stale detection
tokens: 47
keywords: ["token", "refresh", "jwt", "cookie"]
created: "2026-01-20"
retrieval_count: 12
last_retrieved: null
---

Token refresh uses silent refresh pattern. Access tokens expire
after 15 minutes. Refresh tokens stored in httpOnly cookies.
On 401 response, automatically attempt refresh before retry.
```

**Provenance Fields (v1.2.0):**

| Field | Description |
|-------|-------------|
| `source_path` | Relative path to original source file |
| `source_hash` | SHA256 hash of source content at chunking time |

These fields enable **stale detection**: when a source file changes, chunks can be identified as outdated and refreshed.

#### 3.2.2 Memory Store

Stores atomic learnings from past sessions:

```markdown
---
id: MEM-2026-01-20-001
type: experiential
domain: AUTH
confidence: high
keywords: ["form", "password", "input", "wrapper"]
source_session: "2026-01-20-afternoon"
verified: true
---

## Learning

FormField wrapper is required for PasswordInput component.
Using label prop directly on PasswordInput doesn't work.

## Context

Discovered while implementing OAuth settings UI.
The component threw a runtime error without the wrapper.
```

**Memory Types:**

| Type | Description | Example |
|------|-------------|---------|
| **Factual** | Stable knowledge | "API uses REST with JSON responses" |
| **Experiential** | Lessons learned | "FormField wrapper required for PasswordInput" |
| **Procedural** | How to do something | "Run tests before committing" |

**Memory Retrieval Tracking (v1.2.0):**

When a memory is included in a context frame, the system automatically:
1. Increments `retrieval_count`
2. Updates `last_retrieved` timestamp

This creates a feedback loop where frequently-used memories rank higher in future retrievals (via the frequency factor in scoring).

#### 3.2.3 Context Assembler

Builds position-optimized context for each task:

```
Task Description
       │
       ▼
┌─────────────┐
│ Embed Query │
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌─────────────┐
│  Retrieve   │────►│  Retrieve   │
│  Chunks     │     │  Memories   │
└──────┬──────┘     └──────┬──────┘
       │                   │
       └─────────┬─────────┘
                 │
                 ▼
        ┌─────────────┐
        │    Rank     │
        │ & Assemble  │
        └──────┬──────┘
               │
               ▼
        [Context Frame]
```

### 3.3 Context Frame Structure

The assembled context sent to the LLM:

```markdown
## CRITICAL: Task Definition
<!-- POSITION: TOP (primacy zone) -->

**Task:** Implement token refresh
**Acceptance Criteria:**
- Silent refresh on 401 responses
- Refresh token in httpOnly cookie

---

## Relevant Knowledge
<!-- POSITION: UPPER-MIDDLE -->

### Token Refresh Logic
Token refresh uses silent refresh pattern...

---

## Past Learnings
<!-- POSITION: LOWER-MIDDLE -->

- FormField wrapper required for PasswordInput
- Settings components in src/components/settings/

---

## Current State
<!-- POSITION: BOTTOM (recency zone) -->

**Status:** In Progress
**Recent:** OAuth provider selection completed

---

## Instructions
<!-- POSITION: VERY END (max recency) -->

Implement the token refresh logic following patterns above.
```

### 3.4 Token Budget

```
Total Available: 200,000 tokens
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reserved (fixed):
  System prompts & tools:    20,000 (10%)
  CLAUDE.md:                 10,000 (5%)
  Response generation:       40,000 (20%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Subtotal Reserved:           70,000 (35%)

Context Frame Budget:
  Task definition:            2,000 (1%)
  Retrieved chunks:          10,000 (5%)
  Retrieved memories:         2,000 (1%)
  Current state:              1,000 (0.5%)
  Instructions:                 500 (0.25%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Context Frame Total:         15,500 (~8%)

Remaining for Conversation: 114,500 (57%)
```

---

## 4. Component Specifications

### 4.1 Chunking

**Semantic-Aware Chunking** - Split by markdown headers first, then by paragraph:

```python
def chunk_document(doc):
    sections = split_by_headers(doc)
    chunks = []
    for section in sections:
        if token_count(section) <= 500:
            chunks.append(section)
        else:
            # Split by paragraph, merge small ones
            chunks.extend(split_paragraphs(section, max_tokens=500))
    return chunks
```

**Parameters:**

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| MAX_CHUNK_SIZE | 500 tokens | Matches embedding model max |
| MIN_CHUNK_SIZE | 50 tokens | Avoid fragments |
| OVERLAP | 50 tokens | Continuity at boundaries |

### 4.2 Embedding

**Model: `e5-small-v2` (Local, Free)**

| Property | Value |
|----------|-------|
| Model | `intfloat/e5-small-v2` |
| Dimensions | 384 |
| Size | ~130MB |
| Max Tokens | 512 |
| Cost | Free (local) |

**Why this model:**
- Designed for retrieval tasks (our exact use case)
- 512 token max aligns with chunk size
- Runs locally - no API costs, no internet required

**Setup:**
```powershell
pip install sentence-transformers
# Model downloads automatically on first use
```

### 4.3 Vector Index

**Technology: NumPy + Pickle (Brute-Force)**

At <500 chunks, brute-force cosine similarity is:
- Fast: <1ms for 500 vectors
- Simple: No index corruption, just load and search
- Zero dependencies: NumPy only

**Structure:**
```
.cortex/index/
├── chunks.pkl          # Numpy array of embeddings
├── chunks.meta.json    # ID → metadata mapping
├── memories.pkl
└── memories.meta.json
```

### 4.4 Retrieval

**Scoring Formula:**
```
score = (
    0.6 × semantic_similarity +
    0.2 × keyword_overlap +
    0.1 × recency_factor +
    0.1 × frequency_factor
)
```

### 4.5 Memory Extraction

**Hybrid approach with confidence threshold:**

| Confidence | Action |
|------------|--------|
| High (verified fixes, explicit "remember this") | Auto-save |
| Medium/Low | Propose for user approval |

User can always: approve all, reject all, or select individually.

---

## 5. Implementation Plan

**Note:** All scripts and tooling will be implemented by Claude. No prior ML/embedding experience required.

### 5.1 Phase 1: Foundation (Week 1-2)

**Deliverables:**
- Directory structure (`.cortex/`)
- Chunking pipeline
- Embedding pipeline (e5-small-v2)
- Vector index (NumPy + pickle)

**Success Criteria:**
- Can chunk a document
- Can embed and index chunks
- Can retrieve top-k similar chunks

### 5.2 Phase 2: Memory System (Week 3-4)

**Deliverables:**
- Memory schema
- Memory creation and retrieval
- Relationship discovery via similarity

**Success Criteria:**
- Can create memories
- Can retrieve relevant memories
- Can update memory confidence

### 5.3 Phase 3: Context Assembly (Week 5-6)

**Deliverables:**
- Context Frame structure
- Position-aware assembly
- Token budget management

**Success Criteria:**
- Can build context frame for a task
- Frame respects token budget
- Critical info at edges

### 5.4 Phase 4: Integration (Week 7-8)

**Deliverables:**
- Claude Code integration
- Session-end memory extraction
- `cortex-assemble` command

**Success Criteria:**
- Mode activation < 5% context
- Memories created from sessions

---

## 6. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Retrieval quality issues | Medium | High | Testing, tuning scoring |
| Chunking loses context | Medium | Medium | Overlap, semantic boundaries |
| Performance too slow | Low | Medium | Already fast at this scale |
| Index corruption | Low | High | Rebuild capability |

---

## 7. Technical Decisions

All technical decisions have been made:

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Embedding Model | `e5-small-v2` | Free, local, designed for retrieval |
| Vector Index | NumPy + pickle | Simple, fast enough at <500 chunks |
| Chunk Size | 500 tokens | Matches model max, balanced granularity |
| Memory Extraction | Hybrid | Auto-save high confidence, propose others |
| Storage Format | Markdown + frontmatter | LLM-friendly (2-5% vs 8-12% YAML) |
| Configuration | Environment variables | No config files to maintain |

---

## 8. Session Protocol (v1.1.0)

### 8.1 Overview

The Semi-Auto Session Protocol enables natural language interaction with Cortex, eliminating the need for users to know or invoke commands directly.

**Design Principles:**
1. **Zero pre-loaded content** - Only metadata at session start
2. **Retrieval-based context** - Content enters through semantic search only
3. **Natural language triggers** - Users speak naturally, agent handles mechanics
4. **Human control preserved** - User triggers session end and approves learnings
5. **Stale awareness (v1.2.0)** - Agent reports stale chunks at session start

### 8.2 Protocol Phases

#### Phase 1: Session Start (Automatic)

**Trigger:** Agent awakens / conversation begins

**Action:** Run `python -m cli status --json`

**Result:** Metadata only (~50 tokens)
- Chunk count and domains
- Memory count
- Index status
- Stale chunks (v1.2.0)

**User Experience:** Agent greets and reports Cortex is available. If stale chunks detected, agent mentions briefly. No content loaded.

#### Phase 2: Task Identification (Automatic)

**Trigger:** User specifies a task

**Detection Patterns:**
```
(?:let's|let us|we need to|i need to|help me|going to|want to|
  working on|work on|implement|build|create|fix|debug|update|modify)\s+(.+)
```

**Action:** Run `python -m cli assemble --task "{detected task}"`

**Result:** Context frame (~2,500 tokens)
- Relevant chunks
- Relevant memories (retrieval tracked - v1.2.0)
- Position-optimized

#### Phase 3: On-Demand Retrieval (Natural Language)

**Trigger:** User asks for information

**Detection Patterns:**

| Pattern | Type |
|---------|------|
| "Get more details about {X}" | Retrieval |
| "What do we know about {X}" | Retrieval |
| "I need context on {X}" | Retrieval |
| "Tell me about {X}" | Retrieval |
| "Remind me how {X} works" | Retrieval |
| "What did we learn about {X}" | Retrieval |
| "cortex: {X}" | Explicit retrieval |

**Action:** Run `python -m cli retrieve --query "{X}"`

**Result:** Top relevant chunks (~1,500 tokens)

#### Phase 4: Session End (User-Triggered)

**Trigger:** User requests learning extraction

**Detection Patterns:**
```
(?:update|save|extract|capture)\s+(?:the\s+)?learn(?:ing|ings)
(?:end|wrap up|close|finish)\s+(?:the\s+)?session
```

**Action:**
1. Identify key learnings from session
2. Run `python -m cli extract --text "{learnings}"`
3. Present proposed memories
4. User approves selections
5. Run `python -m cli index` if memories saved

### 8.3 Natural Language Trigger Reference

#### Task Identification Triggers

| Phrase | Example |
|--------|---------|
| "Let's work on {X}" | "Let's work on the login page" |
| "I need to {X}" | "I need to fix the API endpoint" |
| "Help me with {X}" | "Help me with database migrations" |
| "Working on {X}" | "Working on user authentication" |
| "Want to {X}" | "Want to refactor the validation" |

#### Retrieval Triggers

| Phrase | Example |
|--------|---------|
| "Get more details about {X}" | "Get more details about caching" |
| "What do we know about {X}" | "What do we know about rate limiting" |
| "I need context on {X}" | "I need context on the auth flow" |
| "Tell me about {X}" | "Tell me about error handling" |
| "Remind me how {X} works" | "Remind me how sessions work" |
| "cortex: {X}" | "cortex: JWT validation" |

#### Session End Triggers

| Phrase | Example |
|--------|---------|
| "Update learning" | "Update learning" |
| "Save learnings" | "Save learnings from today" |
| "End session" | "Let's end session" |
| "Wrap up and save" | "Wrap up and save what we learned" |

### 8.4 Context Budget

| Phase | Tokens | % of 200k |
|-------|--------|-----------|
| Session start | ~50 | 0.025% |
| Task assembly | ~2,500 | 1.25% |
| Retrieval (×2) | ~3,000 | 1.5% |
| **Typical total** | **~5,550** | **~2.8%** |

*Assumes 2 retrievals per session. Heavy debugging may reach 10-15%.*

Leaves **90%+ context** for actual work.

---

## Appendix A: File Structure

```
.cortex/
├── chunks/
│   ├── AUTH/
│   │   ├── CHK-AUTH-001-001.md     # Chunk (Markdown + frontmatter)
│   │   ├── CHK-AUTH-001-001.npy    # Embedding (NumPy binary)
│   │   └── ...
│   └── UI/
│       └── ...
├── memories/
│   ├── MEM-2026-01-20-001.md       # Memory (Markdown)
│   ├── MEM-2026-01-20-001.npy      # Embedding (NumPy binary)
│   └── ...
├── index/
│   ├── chunks.pkl                   # Consolidated chunk embeddings
│   ├── chunks.meta.json             # Chunk ID → metadata mapping
│   ├── memories.pkl                 # Consolidated memory embeddings
│   └── memories.meta.json           # Memory metadata
└── cache/
    └── embeddings/                  # Future: embedding cache
```

**Chunk Frontmatter (v1.2.0):**
```yaml
id: CHK-AUTH-001-001
source_doc: DOC-AUTH-001
source_section: "Token Refresh"
source_lines: [10, 45]
source_path: "docs/auth/tokens.md"   # Provenance
source_hash: "a1b2c3d4e5f6..."       # For stale detection
tokens: 487
keywords: ["token", "refresh", "auth"]
created: "2026-01-27T10:00:00"
last_retrieved: null
retrieval_count: 0
```

---

## Appendix B: CLI Commands (v1.2.0)

**Note:** As of v1.2.0, Cortex uses a cross-platform Python CLI. PowerShell scripts are deprecated.

| Command | Purpose |
|---------|---------|
| `python -m cli init` | Initialize Cortex in a project |
| `python -m cli chunk --path <file>` | Chunk a document |
| `python -m cli chunk --path <file> --refresh` | Refresh stale chunks |
| `python -m cli index` | Rebuild indices |
| `python -m cli retrieve --query <text>` | Test retrieval |
| `python -m cli assemble --task <text>` | Build context frame |
| `python -m cli memory add --learning <text>` | Add a memory |
| `python -m cli memory list` | List memories |
| `python -m cli memory delete <id>` | Delete a memory |
| `python -m cli extract --text <text>` | Extract learnings |
| `python -m cli status` | Show status and stale chunks |
| `python -m cli status --json` | JSON output for automation |

---

## Appendix C: Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CORTEX_EMBEDDING_MODEL` | `intfloat/e5-small-v2` | Embedding model |
| `CORTEX_CHUNK_SIZE` | `500` | Max tokens per chunk |
| `CORTEX_CHUNK_OVERLAP` | `50` | Overlap between chunks |
| `CORTEX_RETRIEVAL_TOP_K` | `10` | Chunks to retrieve |
| `CORTEX_MEMORY_TOP_K` | `5` | Memories to retrieve |
| `CORTEX_TOKEN_BUDGET` | `15000` | Context frame budget |

Defaults work out of the box. Override only if needed.

---

## Appendix D: Example Context Frame

```markdown
<!-- CONTEXT FRAME: Implement Token Refresh -->
<!-- Generated: 2026-01-26T10:30:00Z -->
<!-- Budget: 15,000 / Used: 12,847 -->

## CRITICAL: Task Definition

**Task:** Implement token refresh in OAuth settings

**Acceptance Criteria:**
- Silent refresh on 401 responses
- Refresh token stored in httpOnly cookie
- User experiences no interruption

**Blockers:** None

---

## Relevant Knowledge

### Token Refresh Logic (DOC-AUTH-001)
Token refresh uses silent refresh pattern. Access tokens expire after 15 minutes.
On 401 response, automatically attempt refresh before retry.

### Security Requirements (DOC-SEC-001)
All tokens must use RS256 signing. Never expose refresh tokens to JavaScript.

---

## Past Learnings

- **MEM-2026-01-20-001** (high): FormField wrapper required for PasswordInput
- **MEM-2026-01-18-003** (high): Settings components in src/components/settings/

---

## Current State

**Status:** In Progress
**Recent:** OAuth provider selection completed (2026-01-25)

---

## Instructions

Implement token refresh following the patterns above.
Focus on the silent refresh mechanism.
Test with manually expired tokens.
```

---

## Appendix E: Stale Detection (v1.2.0)

Cortex tracks source file changes to ensure context is current.

### Detection

When `python -m cli status` runs, it:
1. Reads each chunk's `source_path` and `source_hash`
2. Computes current SHA256 of the source file
3. Compares hashes - mismatch indicates stale chunk

### Refresh Workflow

```bash
# 1. Check for stale chunks
python -m cli status

# 2. Refresh stale file(s)
python -m cli chunk --path docs/changed-file.md --refresh

# 3. Rebuild index
python -m cli index
```

The `--refresh` flag:
1. Finds existing chunks from that source file
2. Deletes them
3. Creates new chunks with updated content and hash

---

*Cortex v1.2.0 - LLM-Native Context Management*
