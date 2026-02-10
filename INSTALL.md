# Cortex Installation Guide

**Version:** 2.2.0

## Prerequisites

- Python 3.8+
- Git
- ~200MB disk space (for embedding model)
- Claude Code (recommended, for full integration)

## Quick Setup (Recommended)

### Option A: Natural Language (with Claude Code)

1. **Copy `global/CLAUDE.md`** to `~/.claude/CLAUDE.md` (one-time setup)
2. **Open any project** in Claude Code
3. **Say:** "cortex init"

The agent handles everything — cloning, installing, copying files, bootstrapping, and indexing.

### Option B: Manual Setup

#### Step 1: Clone Cortex Engine

```bash
git clone https://github.com/nivanovsp/cortex.git .cortex-engine
```

#### Step 2: Install Dependencies

**Windows:**
```bash
python -m venv .cortex-engine/.venv && .cortex-engine/.venv/Scripts/pip install -r .cortex-engine/requirements.txt
```

**Unix:**
```bash
python -m venv .cortex-engine/.venv && .cortex-engine/.venv/bin/pip install -r .cortex-engine/requirements.txt
```

#### Step 3: Copy Methodology Files

```bash
cp -r .cortex-engine/agents ./agents
cp -r .cortex-engine/.claude ./.claude
cp .cortex-engine/CLAUDE.md ./CLAUDE.md
```

#### Step 4: Initialize Cortex

**Windows:**
```bash
cd .cortex-engine && .venv/Scripts/python -m cli init --root ..
```

**Unix:**
```bash
cd .cortex-engine && .venv/bin/python -m cli init --root ..
```

This creates `.cortex/` directory and downloads the embedding model (~130MB, first run only).

#### Step 5: Bootstrap Methodology

**Windows:**
```bash
cd .cortex-engine && .venv/Scripts/python -m cli bootstrap --root ..
cd .cortex-engine && .venv/Scripts/python -m cli index --root ..
```

**Unix:**
```bash
cd .cortex-engine && .venv/bin/python -m cli bootstrap --root ..
cd .cortex-engine && .venv/bin/python -m cli index --root ..
```

#### Step 6: Update .gitignore

Add to your `.gitignore`:
```
.cortex-engine/
.cortex/
```

#### Step 7: Configure Global Rules

Copy `global/CLAUDE.md` from the Cortex repo to `~/.claude/CLAUDE.md`:

**Windows:**
```bash
copy .cortex-engine\global\CLAUDE.md %USERPROFILE%\.claude\CLAUDE.md
```

**Mac/Linux:**
```bash
cp .cortex-engine/global/CLAUDE.md ~/.claude/CLAUDE.md
```

#### Step 8: Verify

**Windows:**
```bash
cd .cortex-engine && .venv/Scripts/python -m cli status --root ..
```

**Unix:**
```bash
cd .cortex-engine && .venv/bin/python -m cli status --root ..
```

You should see chunks in the METHODOLOGY domain.

## Project Structure After Setup

```
your-project/
├── .cortex-engine/       # Cloned Cortex repo (engine + source)
├── .cortex/              # Runtime data (chunks, memories, indices)
├── .claude/commands/     # Slash commands for Claude Code
├── agents/               # Modes, skills, templates, checklists
├── CLAUDE.md             # Project-level Cortex instructions
└── (your project files)
```

## CLI Commands Reference

All commands run from `.cortex-engine/` with `--root` pointing to the project:

**Windows:**
```bash
cd .cortex-engine && .venv/Scripts/python -m cli <command> --root ..
```

**Unix:**
```bash
cd .cortex-engine && .venv/bin/python -m cli <command> --root ..
```

| Command | Purpose |
|---------|---------|
| `init --root ..` | Initialize Cortex |
| `status --root ..` | Show status and stale chunks |
| `chunk --path <file> --root ..` | Chunk documents |
| `chunk --path <file> --refresh --root ..` | Refresh stale chunks |
| `index --root ..` | Build/rebuild indices |
| `retrieve --query <text> --root ..` | Search for context |
| `assemble --task <text> --root ..` | Build context frame |
| `memory add --learning <text> --root ..` | Add a memory |
| `memory list --root ..` | List memories |
| `extract --text <text> --root ..` | Extract learnings |
| `bootstrap --root ..` | Chunk methodology into Cortex |

## Updating Cortex

Say "cortex update" in Claude Code, or manually:

```bash
cd .cortex-engine && git pull
```

Then re-copy methodology files (Step 3 above) and re-bootstrap:

**Windows:**
```bash
cd .cortex-engine && .venv/Scripts/python -m cli bootstrap --force --root ..
cd .cortex-engine && .venv/Scripts/python -m cli index --root ..
```

**Unix:**
```bash
cd .cortex-engine && .venv/bin/python -m cli bootstrap --force --root ..
cd .cortex-engine && .venv/bin/python -m cli index --root ..
```

## Agent System

Cortex ships with 6 agents, 29+ skills, 14 templates, 6 checklists.

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

See `agents/README.md` for full documentation.

## Troubleshooting

### "No module named cli"
You're running from the wrong directory. Run from `.cortex-engine/`:

**Windows:**
```bash
cd .cortex-engine && .venv/Scripts/python -m cli status --root ..
```

**Unix:**
```bash
cd .cortex-engine && .venv/bin/python -m cli status --root ..
```

### "Python not found"
Install Python 3.8+ and ensure it's in your PATH.

### "No module named 'typer'"

**Windows:**
```bash
.cortex-engine/.venv/Scripts/pip install -r .cortex-engine/requirements.txt
```

**Unix:**
```bash
.cortex-engine/.venv/bin/pip install -r .cortex-engine/requirements.txt
```

### "Model download fails"
The e5-small-v2 model downloads from HuggingFace. Check your internet connection. The model caches at `~/.cache/huggingface/`.

### "Cortex not initialized"

**Windows:**
```bash
cd .cortex-engine && .venv/Scripts/python -m cli init --root ..
```

**Unix:**
```bash
cd .cortex-engine && .venv/bin/python -m cli init --root ..
```

### "Stale chunks detected"

**Windows:**
```bash
cd .cortex-engine && .venv/Scripts/python -m cli chunk --path <file> --refresh --root ..
cd .cortex-engine && .venv/Scripts/python -m cli index --root ..
```

**Unix:**
```bash
cd .cortex-engine && .venv/bin/python -m cli chunk --path <file> --refresh --root ..
cd .cortex-engine && .venv/bin/python -m cli index --root ..
```

### ModuleNotFoundError when project venv is active

Cortex uses its own isolated venv at `.cortex-engine/.venv/`. If you see import errors, ensure you're using the venv python path, not your project's python.

## Uninstalling

```bash
# Remove engine and runtime data
rm -rf .cortex-engine/ .cortex/

# Remove methodology files (optional)
rm -rf agents/ .claude/commands/ CLAUDE.md
```

To remove global rules, edit `~/.claude/CLAUDE.md` and remove the Cortex sections.

## Migrating from v2.0.0

If upgrading from v2.0.0:

1. Clone engine: `git clone https://github.com/nivanovsp/cortex.git .cortex-engine`
2. Install deps: `pip install -r .cortex-engine/requirements.txt`
3. Re-copy methodology files (Step 3 above)
4. Re-bootstrap: `cd .cortex-engine && python -m cli bootstrap --force --root ..`
5. Rebuild index: `cd .cortex-engine && python -m cli index --root ..`
6. Update `~/.claude/CLAUDE.md` from `global/CLAUDE.md`
7. Add `.cortex-engine/` to `.gitignore`

### Migrating from v2.1.x

1. Create the isolated venv:
   - Windows: `python -m venv .cortex-engine/.venv && .cortex-engine/.venv/Scripts/pip install -r .cortex-engine/requirements.txt`
   - Unix: `python -m venv .cortex-engine/.venv && .cortex-engine/.venv/bin/pip install -r .cortex-engine/requirements.txt`
2. All CLI commands now use the venv python instead of bare `python`
3. Your project's own venv is no longer affected by Cortex dependencies
