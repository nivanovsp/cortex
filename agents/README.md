# Cortex Agent Modes

Agent modes are expert personas that layer on top of Cortex's session protocol. Each mode provides domain-specific focus, specialized commands, and tailored output formats.

## Available Modes

| Mode | Activation | Focus |
|------|-----------|-------|
| [Analyst](modes/analyst.md) | `/modes:analyst` | Requirements, gap analysis, stakeholder concerns |
| [Architect](modes/architect.md) | `/modes:architect` | System design, trade-offs, ADRs |
| [Developer](modes/developer.md) | `/modes:developer` | Implementation, debugging, code review |
| [UX Designer](modes/ux-designer.md) | `/modes:ux-designer` | Interface design, user flows, accessibility |
| [Orchestrator](modes/orchestrator.md) | `/modes:orchestrator` | Work planning, phase coordination |

## Available Skills

| Skill | Activation | Purpose |
|-------|-----------|---------|
| [QA Gate](skills/qa-gate.md) | `/skills:qa-gate` | Quality validation checklist |
| [Extract Learnings](skills/extract-learnings.md) | `/skills:extract-learnings` | Session learning extraction |

## How It Works

### Architecture

```
Layer 0: Session Protocol (always active)
  - Status on session start
  - Assemble on task identification
  - Retrieve on information request
  - Extract on session end

Layer 1: Agent Mode (optional, user-activated)
  - Persona-specific interpretation
  - Domain-filtered retrieval
  - Specialized commands and output
```

Modes don't replace the session protocol — they add a persona lens on top of it.

### Usage

**With Claude Code:**
```
/modes:architect
```

**With other LLM tools:**
Point your tool at the mode spec file and instruct it to adopt the persona:
```
Read agents/modes/architect.md and adopt that persona fully.
Follow all instructions for the remainder of this conversation.
```

### Commands (Available in All Modes)

- `*help` — Show mode-specific commands
- `*exit` — Leave the current mode
- `*context` — Show gathered Cortex context summary

### Recommended Workflow

For complex tasks, use the **Orchestrator** first to produce a phased work plan, then activate each mode as directed:

```
1. /modes:orchestrator     → Produces phased plan
2. /modes:analyst          → Phase 1: Clarify requirements
3. /modes:architect        → Phase 2: Design solution
4. /modes:developer        → Phase 3: Implement
5. /skills:qa-gate         → Phase 4: Validate quality
```
