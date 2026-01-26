# Cortex User Guide

A comprehensive guide to using Cortex for LLM-native context management.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Document Management](#document-management)
3. [Memory System](#memory-system)
4. [Context Assembly](#context-assembly)
5. [Session Workflow](#session-workflow)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Installation

1. **Prerequisites**
   - Python 3.8+
   - PowerShell 5.1+ (Windows) or PowerShell Core
   - ~200MB disk space for embedding model

2. **Initialize Cortex**
   ```powershell
   cd your-project
   .\path\to\cortex\scripts\cortex-init.ps1
   ```

   This creates:
   - `.cortex/` directory structure
   - Installs Python dependencies
   - Downloads embedding model (~130MB, first run only)

3. **Verify Installation**
   ```powershell
   .\scripts\cortex-status.ps1
   ```

### First Steps

1. **Chunk your documentation**
   ```powershell
   .\scripts\cortex-chunk.ps1 -Path "docs/"
   ```

2. **Build the search index**
   ```powershell
   .\scripts\cortex-index.ps1
   ```

3. **Test retrieval**
   ```powershell
   .\scripts\cortex-retrieve.ps1 -Query "authentication"
   ```

---

## Document Management

### Chunking Documents

Cortex breaks documents into ~500 token semantic units for efficient retrieval.

**Chunk a single file:**
```powershell
.\scripts\cortex-chunk.ps1 -Path "docs/api-spec.md"
```

**Chunk a directory:**
```powershell
.\scripts\cortex-chunk.ps1 -Path "docs/"
```

**Override domain detection:**
```powershell
.\scripts\cortex-chunk.ps1 -Path "docs/auth.md" -Domain "AUTH"
```

**Force re-chunk:**
```powershell
.\scripts\cortex-chunk.ps1 -Path "docs/" -Force
```

### Domain Detection

Cortex auto-detects domains from file paths:

| Path | Detected Domain |
|------|-----------------|
| `docs/auth/login.md` | AUTH |
| `docs/auth-spec.md` | AUTH |
| `docs/readme.md` | GENERAL |

### After Chunking

Always rebuild the index after adding chunks:
```powershell
.\scripts\cortex-index.ps1
```

---

## Memory System

Memories are atomic learnings that persist across sessions.

### Memory Types

| Type | Use For | Example |
|------|---------|---------|
| **Factual** | Stable knowledge | "API returns JSON with camelCase keys" |
| **Experiential** | Lessons learned | "FormField wrapper required for inputs" |
| **Procedural** | How-to knowledge | "Run tests before committing" |

### Creating Memories

**Basic:**
```powershell
.\scripts\cortex-memory.ps1 -Action add -Learning "API requires auth header"
```

**With all options:**
```powershell
.\scripts\cortex-memory.ps1 -Action add `
    -Learning "FormField wrapper is required for PasswordInput" `
    -Context "Discovered when component threw runtime error" `
    -Type experiential `
    -Domain UI `
    -Confidence high
```

### Listing Memories

**All memories:**
```powershell
.\scripts\cortex-memory.ps1 -Action list
```

**Filter by domain:**
```powershell
.\scripts\cortex-memory.ps1 -Action list -Domain AUTH
```

### Searching Memories

```powershell
.\scripts\cortex-memory.ps1 -Action query -Query "form validation"
```

### Updating Memories

**Mark as verified:**
```powershell
.\scripts\cortex-memory.ps1 -Action update -Id "MEM-2026-01-26-001" -Verified
```

**Change confidence:**
```powershell
.\scripts\cortex-memory.ps1 -Action update -Id "MEM-2026-01-26-001" -Confidence high
```

### Finding Related Memories

```powershell
.\scripts\cortex-memory.ps1 -Action related -Id "MEM-2026-01-26-001" -TopK 5
```

### Deleting Memories

```powershell
.\scripts\cortex-memory.ps1 -Action delete -Id "MEM-2026-01-26-001"
```

---

## Context Assembly

Context frames combine relevant chunks and memories for LLM consumption.

### Basic Assembly

```powershell
.\scripts\cortex-assemble.ps1 -Task "Implement user authentication"
```

### With Acceptance Criteria

```powershell
.\scripts\cortex-assemble.ps1 `
    -Task "Fix login bug" `
    -Criteria "Users can log in,Sessions persist,Error messages shown"
```

### With Current State

```powershell
.\scripts\cortex-assemble.ps1 `
    -Task "Add OAuth support" `
    -State "Basic auth working, need OAuth"
```

### Custom Budget

```powershell
.\scripts\cortex-assemble.ps1 -Task "Quick fix" -Budget 5000
```

### Save to File

```powershell
.\scripts\cortex-assemble.ps1 -Task "Implement feature" -Output "context.md"
```

### Context Frame Structure

The assembled context is position-optimized:

```
TOP (high attention)
├── Task Definition
├── Acceptance Criteria
│
MIDDLE (lower attention)
├── Relevant Knowledge (chunks)
├── Past Learnings (memories)
│
BOTTOM (high attention)
├── Current State
└── Instructions
```

---

## Session Workflow

### Recommended Flow

```
┌─────────────────────────────────────────────────────┐
│                  SESSION START                       │
├─────────────────────────────────────────────────────┤
│  1. cortex-status.ps1        # Check state          │
│  2. cortex-assemble.ps1      # Build context        │
├─────────────────────────────────────────────────────┤
│                  DURING SESSION                      │
├─────────────────────────────────────────────────────┤
│  • cortex-retrieve.ps1       # Search as needed     │
│  • cortex-memory.ps1 add     # Note learnings       │
├─────────────────────────────────────────────────────┤
│                  SESSION END                         │
├─────────────────────────────────────────────────────┤
│  1. cortex-extract.ps1       # Extract learnings    │
│  2. cortex-index.ps1         # Rebuild if added     │
└─────────────────────────────────────────────────────┘
```

### Extracting Learnings

**From text:**
```powershell
.\scripts\cortex-extract.ps1 -Text "Fixed by adding null check. Found that X requires Y."
```

**From file:**
```powershell
.\scripts\cortex-extract.ps1 -File "session-notes.txt"
```

**Auto-save high confidence:**
```powershell
.\scripts\cortex-extract.ps1 -Text "..." -AutoSave
```

**Filter by confidence:**
```powershell
.\scripts\cortex-extract.ps1 -Text "..." -MinConfidence high
```

---

## Best Practices

### Document Organization

1. **Use descriptive file names** - `auth-token-refresh.md` not `doc1.md`
2. **Organize by domain** - `docs/auth/`, `docs/api/`, etc.
3. **Keep documents focused** - One topic per document
4. **Use markdown headers** - Helps semantic chunking

### Memory Hygiene

1. **Be specific** - "FormField required for PasswordInput" not "wrapper needed"
2. **Include context** - When/why you learned this
3. **Set appropriate confidence** - High only for verified facts
4. **Review periodically** - Delete outdated memories

### Context Assembly

1. **Write clear task descriptions** - Be specific about what you're doing
2. **Include acceptance criteria** - Helps focus the context
3. **Use appropriate budgets** - Smaller for simple tasks
4. **Review the frame** - Check it includes relevant content

### Performance Tips

1. **Rebuild index after bulk changes** - Not after every single addition
2. **Use domain filters** - Narrow searches when possible
3. **Keep chunks reasonable** - Don't chunk massive files unnecessarily

---

## Troubleshooting

### Common Issues

**"No chunks found"**
- Did you run `cortex-chunk.ps1`?
- Did you run `cortex-index.ps1` after chunking?

**"Index not found"**
```powershell
.\scripts\cortex-index.ps1
```

**Retrieval returns irrelevant results**
- Try more specific queries
- Check that relevant documents are chunked
- Rebuild index: `.\scripts\cortex-index.ps1 -Full`

**Memory extraction finds nothing**
- Text may not match extraction patterns
- Try lowering confidence: `-MinConfidence low`
- Add memories manually if patterns don't match

**Slow embedding**
- First run downloads model (~130MB)
- Subsequent runs should be fast
- Model is cached at `~/.cache/huggingface/`

### Checking System State

```powershell
# Full status
.\scripts\cortex-status.ps1

# JSON output for debugging
.\scripts\cortex-status.ps1 -Json
```

### Rebuilding Everything

If something is corrupted:

```powershell
# Remove indices (keeps chunks and memories)
Remove-Item .cortex\index\* -Force

# Rebuild
.\scripts\cortex-index.ps1
```

### Getting Help

- Check `docs/cortex-spec.md` for full technical details
- Check `docs/architecture.md` for system design
- Check `CLAUDE.md` for Claude Code specific guidance
