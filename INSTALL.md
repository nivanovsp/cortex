# Cortex Installation Guide

**Version:** 2.0.0

## Prerequisites

- Python 3.8+
- ~200MB disk space (for embedding model)
- Claude Code (optional, for full integration)

**Note:** As of v1.2.0, Cortex uses a cross-platform Python CLI. PowerShell is no longer required.

## Installation Steps

### Step 1: Get Cortex

**Option A: Clone from GitHub**
```bash
git clone https://github.com/nivanovsp/cortex.git
cd cortex
```

**Option B: Copy to existing project**
```bash
cp -r path/to/cortex/ your-project/cortex/
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `sentence-transformers` - Local embeddings (e5-small-v2)
- `numpy` - Vector operations
- `tiktoken` - Token counting
- `typer` - CLI framework
- `rich` - Terminal formatting

### Step 3: Initialize Cortex

```bash
python -m cli init
```

This will:
- Create `.cortex/` directory structure
- Download the e5-small-v2 embedding model (~130MB, first run only)

### Step 4: Configure Claude Code (Recommended)

For full Claude Code integration with natural language support (v1.2.0), add Cortex rules to your global CLAUDE.md:

1. **Open your global CLAUDE.md:**
   ```bash
   # Windows
   notepad %USERPROFILE%\.claude\CLAUDE.md

   # Mac/Linux
   nano ~/.claude/CLAUDE.md
   ```

2. **Find the "Cortex Context Management" section** and update it with the v1.2.0 version from the project (see `global/CLAUDE.md` for reference).

3. **Save and close.**

This enables:
- Natural language interaction ("Let's work on X", "What do we know about Y")
- Automatic context loading when you specify a task
- Seamless retrieval without running commands
- Stale chunk detection and refresh workflow
- User-triggered learning extraction ("Update learning")
- Agent mode references (see Step 5)

### Step 5: Agent System (Included)

Cortex v2.0.0 ships with a complete methodology — 6 agents, 29 skills, 14 templates, 6 checklists.

**Bootstrap methodology resources (optional but recommended):**
```bash
python -m cli bootstrap
python -m cli index
```

This chunks methodology resources into Cortex for on-demand retrieval by agents.

**With Claude Code:**
```
/modes:analyst
/modes:architect
/modes:developer
/modes:qa
/modes:ux-designer
/modes:orchestrator
```

**With other LLM tools:**
```
Read agents/modes/architect.md and adopt that persona fully.
```

See `agents/README.md` for full agent documentation.

### Step 5: Verify Installation

```bash
python -m cli status
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

```bash
python -m cli chunk --path docs/
python -m cli index
```

### Test Retrieval

```bash
python -m cli retrieve --query "your search term"
```

### Build a Context Frame

```bash
python -m cli assemble --task "Your task description"
```

### Check for Stale Chunks

```bash
# Status shows stale chunks if source files changed
python -m cli status

# Refresh stale chunks
python -m cli chunk --path docs/file.md --refresh
python -m cli index
```

## CLI Commands Reference

| Command | Purpose |
|---------|---------|
| `python -m cli init` | Initialize Cortex |
| `python -m cli status` | Show status and stale chunks |
| `python -m cli chunk --path X` | Chunk documents |
| `python -m cli chunk --path X --refresh` | Refresh stale chunks |
| `python -m cli index` | Build/rebuild indices |
| `python -m cli retrieve --query X` | Search for context |
| `python -m cli assemble --task X` | Build context frame |
| `python -m cli memory add --learning X` | Add a memory |
| `python -m cli memory list` | List memories |
| `python -m cli extract --text X` | Extract learnings |
| `python -m cli bootstrap` | Chunk methodology into Cortex |

## Troubleshooting

### "Python not found"
Install Python 3.8+ and ensure it's in your PATH.

### "No module named 'typer'"
```bash
pip install -r requirements.txt
```

### "No module named 'sentence_transformers'"
```bash
pip install sentence-transformers numpy tiktoken
```

### "Model download fails"
The e5-small-v2 model downloads from HuggingFace. Check your internet connection. The model caches at `~/.cache/huggingface/`.

### "Cortex not initialized"
Run `python -m cli init` first.

### "Stale chunks detected"
Source files have changed since chunking. Refresh with:
```bash
python -m cli chunk --path <file> --refresh
python -m cli index
```

## Updating Cortex

```bash
cd cortex
git pull origin main

# Re-install dependencies if requirements.txt changed
pip install -r requirements.txt
```

## Uninstalling

To remove Cortex from a project:

```bash
# Remove runtime data
rm -rf .cortex/

# Remove Cortex folder (if copied)
rm -rf cortex/
```

To remove from global Claude Code rules, edit `~/.claude/CLAUDE.md` and remove the "Cortex Context Management" section.

## Migrating from v1.3.0

If upgrading from v1.3.0:

1. Pull latest: `git pull origin main`
2. New QA agent, 29 skills, checklists, and templates are available immediately
3. Run bootstrap to index methodology: `python -m cli bootstrap && python -m cli index`
4. All existing agents updated with Rules and Skills sections
5. Optionally update global CLAUDE.md with v2.0.0 references

---

## Migrating from v1.1.0

If upgrading from v1.1.0 (PowerShell scripts):

1. Install new dependencies: `pip install -r requirements.txt`
2. Replace PowerShell commands with Python CLI equivalents
3. Update global CLAUDE.md with v1.2.0 Cortex section
4. Existing chunks and memories remain compatible

See `scripts/README.md` for full command mapping.
