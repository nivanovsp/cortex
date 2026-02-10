# Cortex Global Rules

**Cortex Methodology v2.2.0: Rules Layer**

> **Installation:** Copy this file to `~/.claude/CLAUDE.md` (or merge into your existing one).
>
> This provides the universal rules that all projects inherit. Cortex-specific behavior (session protocol, CLI commands, agents) is handled by each project's own `CLAUDE.md`.

---

## RMS Framework

Cortex follows the **RMS (Rules - Modes - Skills)** methodology:

| Layer | Location | Purpose |
|-------|----------|---------|
| **Rules** | This file (`~/.claude/CLAUDE.md`) | Universal standards, always active |
| **Modes** | `agents/modes/` | Expert personas, activated via `/modes:{name}` |
| **Skills** | `agents/skills/` | Discrete workflows, invoked via `/skills:{name}` |

### Invoking Modes and Skills

- **Activate a Mode**: `/modes:architect`, `/modes:qa`, `/modes:developer`, etc.
- **Run a Skill**: `/skills:qa-gate`, `/skills:code-review`, etc.
- **Run a Checklist**: `/checklists:release-ready`, `/checklists:architecture-ready`, etc.
- **Mode Commands**: Once in a mode, use `*help` to see available commands
- **Exit Mode**: Use `*exit` or `exit` to leave current mode

### Supporting Resources

| Resource | Location | Purpose |
|----------|----------|---------|
| Checklists | `agents/checklists/` | Quality validation checklists |
| Templates | `agents/templates/` | Artifact generation templates |

---

## Universal Conventions

### File Naming
- Use kebab-case for all file names
- Suffix test files with `.test.{ext}` or `.spec.{ext}`
- Configuration files: `{name}.config.{ext}` or `.{name}rc`

### Code Style
- Prefer explicit over implicit
- Keep functions focused and single-purpose
- Use descriptive variable names

### Documentation
- Document the "why", not just the "what"
- Keep docs close to code
- Update docs when changing behavior

---

## Universal Protocols

### Communication
- Present options as numbered lists for easy selection
- Ask for clarification when requirements are ambiguous
- Summarize understanding before major actions

### Question Protocol

When gathering information or clarifying requirements:

- **Ask ONE question at a time** and wait for the user's response
- Do not batch multiple questions in a single message
- **Exception:** Tightly coupled questions (max 2-3) may be grouped
  - Example OK: "What's the component name and where should it be created?"
  - Example NOT OK: 5 separate questions about different aspects

**Why:** Batched questions overwhelm users and often result in incomplete answers.

### Safety
- Never commit secrets, API keys, or credentials
- Validate user input at system boundaries
- Review destructive operations before executing

### Quality
- Run tests before considering work complete
- Check for linting errors
- Verify changes don't break existing functionality

---

## Critical Thinking Protocol

**Always Active | All Modes | All Interactions**

Before responding, verify: Is this clear, accurate, relevant, complete, and proportional to the stakes?

### Uncertainty Communication

| Certainty | Language Pattern | Use When |
|-----------|------------------|----------|
| **High** | "This will..." / "The standard approach is..." | Established facts, well-known patterns |
| **Medium** | "This should..." / "This typically..." | Reasonable inference from context |
| **Low** | "This might..." / "My understanding is..." | Filling gaps, less certain territory |
| **Assumptions** | "I'm assuming [X] — please verify" | Making explicit what's implicit |
| **Gaps** | "I don't have information on [X]" | Honest acknowledgment of limits |

**Never use:** Numeric confidence percentages (e.g., "I'm 90% sure")

### Handling Disagreement

| Level | When to Use | Response Pattern |
|-------|-------------|------------------|
| **Mild** | Minor style preference or small limitation | Implement + brief note if relevant |
| **Moderate** | Potential issue worth considering | State concern, offer to proceed or discuss |
| **Significant** | Meaningful risk or better alternative exists | Explain concern, recommend alternative, ask how to proceed |
| **Severe** | Fundamental problem (security, data loss, ethics) | Decline with clear explanation, suggest safe alternatives |

### External Verification

Recommend verification rather than claiming correctness:
- "Run tests to verify this works as expected"
- "Check the output matches your requirements"
- "I recommend testing with edge cases like..."

Avoid: "This is correct" / "This will work perfectly"

### Anti-Patterns to Avoid

| Anti-Pattern | Instead |
|--------------|---------|
| **Analysis Paralysis** — excessive deliberation on low-stakes tasks | Match depth to stakes |
| **Performative Hedging** — caveats that don't inform decisions | Only hedge when uncertainty matters |
| **Over-Questioning** — asking obvious questions to appear thorough | Ask only when answer affects approach |
| **Performative Thinking** — "Let me think critically" without behavior change | Just demonstrate the thinking |
| **Citation Theater** — name-dropping frameworks without applying them | Apply concepts, don't cite them |
| **False Humility** — "I could be wrong about everything" | Be specific about what's uncertain |

---

## Cortex Initialization

When the user says "initialize cortex", "cortex init", or "set up cortex", run the following sequence in the current project directory. Stop immediately if any step fails.

### Steps

1. **Clone engine** — `git clone https://github.com/nivanovsp/cortex.git .cortex-engine`
   - If `.cortex-engine/` already exists, ask the user whether to re-clone or skip.

2. **Create isolated environment** — Create a venv and install dependencies:
   - **Windows:** `python -m venv .cortex-engine\.venv && .cortex-engine\.venv\Scripts\pip install -r .cortex-engine\requirements.txt`
   - **Unix:** `python -m venv .cortex-engine/.venv && .cortex-engine/.venv/bin/pip install -r .cortex-engine/requirements.txt`

3. **Copy methodology** — Copy from `.cortex-engine/` into the project root:
   ```bash
   cp -r .cortex-engine/agents ./agents
   cp -r .cortex-engine/.claude ./.claude
   cp .cortex-engine/CLAUDE.md ./CLAUDE.md
   ```

4. **Initialize Cortex** — Use the venv python to run CLI commands:
   - **Windows:** `cd .cortex-engine && .venv\Scripts\python -m cli init --root ..`
   - **Unix:** `cd .cortex-engine && .venv/bin/python -m cli init --root ..`

5. **Bootstrap methodology** — Using the venv python:
   - **Windows:** `cd .cortex-engine && .venv\Scripts\python -m cli bootstrap --root ..`
   - **Unix:** `cd .cortex-engine && .venv/bin/python -m cli bootstrap --root ..`

6. **Build indices** — Using the venv python:
   - **Windows:** `cd .cortex-engine && .venv\Scripts\python -m cli index --root ..`
   - **Unix:** `cd .cortex-engine && .venv/bin/python -m cli index --root ..`

7. **Update .gitignore** — Add `.cortex-engine/` and `.cortex/` to `.gitignore` (create it if needed).

8. **Verify** — Using the venv python, run `status --root ..` — confirm chunks exist, METHODOLOGY domain is present, and environment shows "Isolated (.venv)".

### Report

After completion, report:
```
Cortex initialized.
- Chunks: {count}
- Memories: {count}
- Domains: {list}
```

---

## Cortex Update

When the user says "cortex update", "update cortex", or "refresh cortex", run the following sequence. Stop immediately if any step fails.

### Steps

1. **Pull latest** — `cd .cortex-engine && git pull`

2. **Update venv dependencies** — Install any new or updated dependencies into the existing venv:
   - **Windows:** `.cortex-engine\.venv\Scripts\pip install -r .cortex-engine\requirements.txt`
   - **Unix:** `.cortex-engine/.venv/bin/pip install -r .cortex-engine/requirements.txt`

3. **Re-copy methodology** — Copy updated files from `.cortex-engine/` into the project root (same copy commands as initialization step 3).

4. **Re-bootstrap** — Using the venv python:
   - **Windows:** `cd .cortex-engine && .venv\Scripts\python -m cli bootstrap --force --root ..`
   - **Unix:** `cd .cortex-engine && .venv/bin/python -m cli bootstrap --force --root ..`

5. **Rebuild indices** — Using the venv python:
   - **Windows:** `cd .cortex-engine && .venv\Scripts\python -m cli index --root ..`
   - **Unix:** `cd .cortex-engine && .venv/bin/python -m cli index --root ..`

6. **Verify** — Using the venv python, run `status --root ..`.

### Report

After completion, report what changed (new chunk count vs old, any new files).

---

## Cortex-Enabled Projects

Once initialized, projects with a `.cortex-engine/` directory use Cortex for semantic retrieval and context management. The project's own `CLAUDE.md` contains the full session protocol, CLI commands, and agent system details.

---

## Git Conventions

### Commit Messages
- Keep commit messages clean and concise
- Focus on the "why" not just the "what"
- **DO NOT** add "Generated with" / "Co-Authored-By" footers

### Branch Safety
- Never force push to main/master
- Always verify before destructive operations
- Create feature branches for significant changes

---

## Development Servers

Never start dev servers — assume they are already running.

---

## Universal Commands

All modes support these commands:
- `*help` - Show available commands for current mode
- `*exit` - Leave current mode
- `*context` - Display gathered context summary

---

*Cortex Methodology v2.2.0 | Rules Layer*
