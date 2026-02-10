# Cortex Init Skill

Initialize Cortex in the current project. This skill runs the full setup sequence — init, bootstrap, and index — so the project is ready for semantic retrieval and the session protocol.

## When to Use

- Setting up Cortex in a new project
- Re-initializing after a corrupted `.cortex/` directory
- After cloning a Cortex-enabled repo that needs local setup

## Procedure

### 0. Create Isolated Environment (when running from `.cortex-engine/`)

If running from an installed project (`.cortex-engine/` pattern), create a venv first:
- **Windows:** `python -m venv .cortex-engine\.venv && .cortex-engine\.venv\Scripts\pip install -r .cortex-engine\requirements.txt`
- **Unix:** `python -m venv .cortex-engine/.venv && .cortex-engine/.venv/bin/pip install -r .cortex-engine/requirements.txt`

All subsequent CLI commands should use the venv python (`.venv/Scripts/python` on Windows, `.venv/bin/python` on Unix).

When running from within the Cortex repo (development), use `python -m cli` directly.

### 1. Initialize

Run `python -m cli init` to create the `.cortex/` runtime directory (chunks, memories, indices).

- If `.cortex/` already exists, inform the user and ask whether to continue or abort.

### 2. Bootstrap

Run `python -m cli bootstrap` to chunk the methodology files (`agents/`) into the METHODOLOGY domain.

- If bootstrapping a second time, use `python -m cli bootstrap --force` to re-chunk.

### 3. Build Index

Run `python -m cli index` to build the vector indices from all chunks and memories.

### 4. Verify

Run `python -m cli status` and confirm:
- Chunk count is greater than zero
- METHODOLOGY domain is present
- Environment shows "Isolated (.venv)" (when using venv)
- No errors reported

## Output

Report the result to the user:

```
Cortex initialized.
- Chunks: {count}
- Memories: {count}
- Domains: {list}
```

If any step fails, report the error and stop — do not continue to the next step.
