# Cortex Init Skill

Initialize Cortex in the current project. This skill runs the full setup sequence — init, bootstrap, and index — so the project is ready for semantic retrieval and the session protocol.

## When to Use

- Setting up Cortex in a new project
- Re-initializing after a corrupted `.cortex/` directory
- After cloning a Cortex-enabled repo that needs local setup

## Procedure

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
