# Cortex v1.3.0 - Session Protocol

> Solution Design Document

**Version:** 1.3.0
**Status:** Implemented
**Created:** 2026-02-01
**Based on:** v1.2.0 Session Protocol

---

## Summary

v1.3.0 extends the session protocol with an **Agent Orchestration Layer** — expert modes that layer on top of the existing protocol. The core protocol (natural language triggers, automatic commands) remains unchanged from v1.2.0.

New in v1.3.0:
- **Agent modes** — Specialist personas activated via `/modes:{name}`
- **Workflow skills** — One-shot workflows via `/skills:{name}`
- **Two-layer architecture** — Session protocol (Layer 0) + Agent mode (Layer 1)
- **Tool-agnostic specs** — Agent definitions work with any LLM tool

---

## Two-Layer Architecture

### Layer 0: Session Protocol (Always Active)

The base session protocol runs regardless of mode:

| Phase | Trigger | Action |
|-------|---------|--------|
| Start | Agent awakens | `python -m cli status --json` |
| Task | User specifies task | `python -m cli assemble --task "{task}"` |
| Retrieval | User asks for info | `python -m cli retrieve --query "{topic}"` |
| End | User triggers | `python -m cli extract --text "{learnings}"` |

### Layer 1: Agent Mode (Optional)

When a mode is active, it adds:

| Aspect | What Changes |
|--------|-------------|
| **Persona** | Agent adopts specialist role and communication style |
| **Domain focus** | Retrieval and memory operations prioritize mode's domains |
| **Interpretation** | Context is analyzed through mode's lens |
| **Commands** | Mode-specific commands available (`*plan`, `*review`, etc.) |
| **Output** | Deliverables follow mode's structured format |

### Interaction Between Layers

```
User: "Let's work on the login page redesign"

Layer 0 (Session Protocol):
  → Detects task → runs assemble → loads context frame

Layer 1 (UX Designer Mode, if active):
  → Interprets context through UI/accessibility lens
  → Focuses on component patterns, user flows
  → Offers *flow, *component, *audit commands
  → Produces component specs and flow diagrams
```

If no mode is active, Layer 0 operates alone (same as v1.2.0).

---

## Agent Modes

### Available Modes

| Mode | Primary Domains | Key Commands |
|------|----------------|--------------|
| Analyst | GENERAL, API, DB | `*analyze`, `*gaps`, `*criteria` |
| Architect | API, DB, DEV | `*design`, `*options`, `*adr` |
| Developer | All | `*implement`, `*debug`, `*review` |
| UX Designer | UI | `*flow`, `*component`, `*audit` |
| Orchestrator | All | `*plan`, `*status`, `*replan` |

### Mode Activation

**Claude Code:**
```
/modes:architect
```

**Other LLM tools:**
```
Read agents/modes/architect.md and adopt that persona fully.
Follow all instructions for the remainder of this conversation.
```

### Universal Mode Commands

All modes support:
- `*help` — Show mode-specific commands
- `*exit` — Leave the current mode
- `*context` — Show gathered Cortex context summary

### Mode Lifecycle

```
1. User activates mode (/modes:architect)
2. Agent reads spec, adopts persona
3. Agent greets as specialist
4. Session protocol continues running (Layer 0)
5. Agent interprets everything through mode's lens
6. User exits mode (*exit) or session ends
```

---

## Workflow Skills

Skills differ from modes — they run once and produce output, rather than establishing a persistent persona.

| Skill | Purpose | Activation |
|-------|---------|-----------|
| QA Gate | Quality validation checklist | `/skills:qa-gate` |
| Extract Learnings | Guided learning extraction | `/skills:extract-learnings` |

### QA Gate

Runs a structured checklist:
1. Code Quality
2. Correctness
3. Security
4. Testing
5. Documentation
6. UI (if applicable)

Produces a PASS/FAIL report with issues and recommendations.

### Extract Learnings

Guides the learning extraction process:
1. Identify session learnings
2. Classify (type, domain, confidence)
3. Present for approval
4. Save approved memories
5. Rebuild index

---

## Orchestrator Coordination Pattern

The Orchestrator is a planning mode that produces phased work plans. Since Claude Code is a single-agent system, the Orchestrator doesn't spawn sub-agents — it plans which mode the user should activate for each phase.

### Example Workflow

```
User: /modes:orchestrator
User: "Plan the implementation of a new dashboard feature"

Orchestrator produces:
┌─────────────────────────────────────────────────┐
│ Phase 1: /modes:analyst                          │
│   Goal: Clarify dashboard requirements           │
│   Deliverable: Requirements doc with criteria    │
├─────────────────────────────────────────────────┤
│ Phase 2: /modes:ux-designer                      │
│   Goal: Design dashboard layout and interactions │
│   Deliverable: Component specs, user flow        │
├─────────────────────────────────────────────────┤
│ Phase 3: /modes:architect                        │
│   Goal: Design data flow and API contracts       │
│   Deliverable: Design document, ADR             │
├─────────────────────────────────────────────────┤
│ Phase 4: /modes:developer                        │
│   Goal: Implement dashboard components           │
│   Deliverable: Working code with tests           │
├─────────────────────────────────────────────────┤
│ Phase 5: /skills:qa-gate                         │
│   Goal: Validate quality                         │
│   Deliverable: QA report                         │
└─────────────────────────────────────────────────┘

User then activates each mode in sequence.
```

---

## Context Budget (Updated)

Agent modes add zero additional context at activation — the mode instruction is part of the conversation, not a Cortex retrieval.

| Phase | Tokens | % of 200k |
|-------|--------|-----------|
| Session start (metadata) | ~50 | 0.025% |
| Mode activation | 0 | 0% |
| Task assembly | ~2,500 | 1.25% |
| On-demand retrieval (x2) | ~3,000 | 1.5% |
| **Typical session** | **~5,550** | **~2.8%** |

*Same budget as v1.2.0. Modes are free in terms of Cortex context.*

---

## File Structure

### Agent Specs (Source of Truth)

```
agents/
├── README.md
├── modes/
│   ├── analyst.md
│   ├── architect.md
│   ├── developer.md
│   ├── ux-designer.md
│   └── orchestrator.md
└── skills/
    ├── qa-gate.md
    └── extract-learnings.md
```

### Claude Code Wrappers

```
.claude/commands/
├── modes/
│   ├── analyst.md          # "Read agents/modes/analyst.md, adopt persona"
│   ├── architect.md
│   ├── developer.md
│   ├── ux-designer.md
│   └── orchestrator.md
└── skills/
    ├── qa-gate.md
    └── extract-learnings.md
```

Wrappers are thin (~4 lines) and reference the tool-agnostic spec. One source of truth, no duplication.

---

## Version Comparison

| Feature | v1.1.0 | v1.2.0 | v1.3.0 |
|---------|--------|--------|--------|
| Natural language triggers | Yes | Yes | Yes |
| Automatic context assembly | Yes | Yes | Yes |
| User-triggered learning | Yes | Yes | Yes |
| Cross-platform CLI | No | Yes | Yes |
| Stale chunk detection | No | Yes | Yes |
| Memory retrieval tracking | No | Yes | Yes |
| Agent modes | No | No | Yes |
| Workflow skills | No | No | Yes |
| Tool-agnostic specs | No | No | Yes |

---

*Cortex v1.3.0 - Session Protocol*
