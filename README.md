# Cortex

**LLM-Native Context Management**

Cortex is a methodology for managing documentation and context in LLM-powered development workflows. It's designed around how LLMs actually process information, not human cognitive metaphors.

## Key Features

- **~8% context consumption** vs 35-60% with traditional approaches
- **Position-aware assembly** - Critical info where LLMs pay attention
- **Semantic retrieval** - Find relevant content via similarity, not manual links
- **Memory system** - Capture and reuse learnings across sessions
- **Markdown-native** - Optimized format for LLM reasoning
- **Local embeddings** - Free, no API costs, works offline

## Installation

### 1. Clone or Copy Cortex

```powershell
# Clone the repository
git clone https://github.com/your-org/cortex.git

# Or copy to your project
Copy-Item -Recurse cortex/ your-project/
```

### 2. Add Global Claude Code Rules (Recommended)

For full Claude Code integration, add the Cortex rules to your global CLAUDE.md:

```powershell
# View the rules to add
Get-Content cortex/global/CLAUDE.md

# Then manually add to: ~/.claude/CLAUDE.md
```

Or copy the contents of `global/CLAUDE.md` and append to your `~/.claude/CLAUDE.md`.

### 3. Initialize in Your Project

```powershell
cd your-project
.\cortex\scripts\cortex-init.ps1
```

## Quick Start

```powershell
# Initialize Cortex in your project
.\scripts\cortex-init.ps1

# Chunk your documents
.\scripts\cortex-chunk.ps1 -Path "docs/"

# Build the index
.\scripts\cortex-index.ps1

# Build context frame for a task
.\scripts\cortex-assemble.ps1 -Task "Implement user authentication"
```

## Scripts Reference

### Core Operations

| Script | Purpose | Example |
|--------|---------|---------|
| `cortex-init.ps1` | Initialize Cortex in project | `.\scripts\cortex-init.ps1` |
| `cortex-chunk.ps1` | Chunk documents into semantic units | `.\scripts\cortex-chunk.ps1 -Path "docs/"` |
| `cortex-index.ps1` | Build/rebuild vector indices | `.\scripts\cortex-index.ps1` |
| `cortex-retrieve.ps1` | Test retrieval with a query | `.\scripts\cortex-retrieve.ps1 -Query "auth token"` |
| `cortex-assemble.ps1` | Build context frame for a task | `.\scripts\cortex-assemble.ps1 -Task "Fix login"` |

### Memory Management

| Script | Purpose | Example |
|--------|---------|---------|
| `cortex-memory.ps1 -Action add` | Create a memory | `-Learning "X requires Y" -Domain AUTH` |
| `cortex-memory.ps1 -Action list` | List all memories | `-Domain AUTH` (optional filter) |
| `cortex-memory.ps1 -Action query` | Search memories | `-Query "form validation"` |
| `cortex-memory.ps1 -Action update` | Update a memory | `-Id "MEM-..." -Verified` |
| `cortex-memory.ps1 -Action delete` | Delete a memory | `-Id "MEM-..."` |
| `cortex-memory.ps1 -Action related` | Find related memories | `-Id "MEM-..."` |

### Session Integration

| Script | Purpose | Example |
|--------|---------|---------|
| `cortex-extract.ps1` | Extract learnings from text | `-Text "Fixed by adding null check"` |
| `cortex-status.ps1` | Show Cortex statistics | `-Json` for programmatic use |

## Claude Code Integration

### Session Workflow

1. **Session Start**: Check status and build context
   ```powershell
   .\scripts\cortex-status.ps1
   .\scripts\cortex-assemble.ps1 -Task "Your task description"
   ```

2. **During Session**: Query for specific knowledge
   ```powershell
   .\scripts\cortex-retrieve.ps1 -Query "relevant topic"
   ```

3. **Session End**: Extract and save learnings
   ```powershell
   .\scripts\cortex-extract.ps1 -Text "Session notes or paste conversation"
   # Or auto-save high confidence memories:
   .\scripts\cortex-extract.ps1 -Text "..." -AutoSave
   ```

### Memory Types

| Type | Description | Example |
|------|-------------|---------|
| **Factual** | Stable knowledge | "API uses REST with JSON responses" |
| **Experiential** | Lessons learned | "FormField wrapper required for PasswordInput" |
| **Procedural** | How to do something | "Run tests before committing" |

### Confidence Levels

| Level | When Assigned | Auto-Save |
|-------|---------------|-----------|
| **High** | Verified fixes, explicit "remember this" | Yes (with `-AutoSave`) |
| **Medium** | Reasonable inference, discoveries | No |
| **Low** | Uncertain, needs verification | No |

## How It Works

```
┌─────────────────────────────────────────────────────┐
│                    CORTEX FLOW                       │
├─────────────────────────────────────────────────────┤
│                                                      │
│  Documents ──► Chunker ──► Embeddings ──► Index     │
│                                                      │
│  Task ──► Query Embed ──► Similarity ──► Retrieve   │
│                                                      │
│  Retrieved ──► Assembler ──► Context Frame ──► LLM  │
│                                                      │
│  Session ──► Extractor ──► Proposed ──► Memories    │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Position-Aware Assembly

Based on "lost in middle" research, Cortex places critical information where LLMs pay most attention:

```
Context Frame Structure:
─────────────────────────────────────
TOP (primacy zone)     → Task Definition
UPPER-MIDDLE           → Relevant Knowledge
LOWER-MIDDLE           → Past Learnings
BOTTOM (recency zone)  → Current State
VERY END               → Instructions
─────────────────────────────────────
```

## Project Structure

```
your-project/
├── .cortex/              # Cortex data (created by cortex-init)
│   ├── chunks/           # Chunked documents by domain
│   │   └── AUTH/         # Domain-specific chunks
│   ├── memories/         # Learnings from sessions
│   └── index/            # Vector indices
│       ├── chunks.pkl    # Chunk embeddings
│       └── memories.pkl  # Memory embeddings
├── scripts/              # PowerShell CLI tools
├── core/                 # Python core modules
├── templates/            # Chunk/memory templates
└── docs/                 # Documentation
```

## Configuration

Environment variables (all optional, defaults work out of the box):

| Variable | Default | Description |
|----------|---------|-------------|
| `CORTEX_EMBEDDING_MODEL` | `intfloat/e5-small-v2` | Embedding model |
| `CORTEX_CHUNK_SIZE` | `500` | Max tokens per chunk |
| `CORTEX_CHUNK_OVERLAP` | `50` | Overlap between chunks |
| `CORTEX_RETRIEVAL_TOP_K` | `10` | Chunks to retrieve |
| `CORTEX_MEMORY_TOP_K` | `5` | Memories to retrieve |
| `CORTEX_TOKEN_BUDGET` | `15000` | Context frame budget |

## Requirements

- Python 3.8+
- PowerShell 5.1+ (Windows) or PowerShell Core (cross-platform)
- ~200MB disk space (for embedding model)

Dependencies installed automatically:
- `sentence-transformers` - Local embeddings
- `numpy` - Vector operations
- `tiktoken` - Token counting

## Documentation

- [Full Specification](docs/cortex-spec.md) - Complete technical details

---

*Cortex v1.0.0 - LLM-Native Context Management*
