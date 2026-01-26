# Cortex Installation Guide

## Prerequisites

- Python 3.8+
- PowerShell 5.1+ (Windows) or PowerShell Core (cross-platform)
- ~200MB disk space (for embedding model)
- Claude Code (optional, for full integration)

## Installation Steps

### Step 1: Get Cortex

**Option A: Clone from GitHub**
```powershell
git clone https://github.com/your-org/cortex.git
cd cortex
```

**Option B: Copy to existing project**
```powershell
Copy-Item -Recurse path/to/cortex/ your-project/cortex/
```

### Step 2: Initialize Cortex

```powershell
.\scripts\cortex-init.ps1
```

This will:
- Create `.cortex/` directory structure
- Install Python dependencies (sentence-transformers, numpy, tiktoken)
- Download the e5-small-v2 embedding model (~130MB, first run only)

### Step 3: Configure Claude Code (Recommended)

For full Claude Code integration, add Cortex rules to your global CLAUDE.md:

1. **Open your global CLAUDE.md:**
   ```powershell
   notepad $HOME\.claude\CLAUDE.md
   # Or: code $HOME\.claude\CLAUDE.md
   ```

2. **Copy the contents of `global/CLAUDE.md`** and paste at the end of your global file.

3. **Save and close.**

This enables Claude Code to understand Cortex commands and workflows across all your projects.

### Step 4: Verify Installation

```powershell
.\scripts\cortex-status.ps1
```

You should see:
```
Cortex Status
=============

Status: INITIALIZED

Chunks: 0 total
Memories: 0 total
...
```

## First Use

### Chunk Your Documentation

```powershell
.\scripts\cortex-chunk.ps1 -Path "docs/"
.\scripts\cortex-index.ps1
```

### Test Retrieval

```powershell
.\scripts\cortex-retrieve.ps1 -Query "your search term"
```

### Build a Context Frame

```powershell
.\scripts\cortex-assemble.ps1 -Task "Your task description"
```

## Troubleshooting

### "Python not found"
Install Python 3.8+ and ensure it's in your PATH.

### "sentence-transformers not found"
```powershell
pip install sentence-transformers numpy tiktoken
```

### "Model download fails"
The e5-small-v2 model downloads from HuggingFace. Check your internet connection. The model caches at `~/.cache/huggingface/`.

### "Cortex not initialized"
Run `.\scripts\cortex-init.ps1` first.

## Updating Cortex

```powershell
cd cortex
git pull origin main

# Re-run init to update dependencies if needed
.\scripts\cortex-init.ps1
```

## Uninstalling

To remove Cortex from a project:

```powershell
# Remove runtime data
Remove-Item -Recurse .cortex/

# Remove Cortex folder (if copied)
Remove-Item -Recurse cortex/
```

To remove from global Claude Code rules, edit `~/.claude/CLAUDE.md` and remove the "Cortex Context Management" section.
