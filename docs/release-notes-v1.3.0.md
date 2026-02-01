# Cortex v1.3.0 Release Notes

**Release Date:** 2026-02-01

---

## Highlights

### Agent Orchestration Layer

Cortex now ships as a **complete package** with expert agent modes. Anyone who clones the repo gets the full agent-driven experience — no separate setup required.

Five specialist modes and two workflow skills are included:

| Mode | Focus | Activation |
|------|-------|-----------|
| **Analyst** | Requirements, gap analysis, acceptance criteria | `/modes:analyst` |
| **Architect** | System design, trade-offs, ADRs | `/modes:architect` |
| **Developer** | Implementation, debugging, code review | `/modes:developer` |
| **UX Designer** | Interface design, accessibility, user flows | `/modes:ux-designer` |
| **Orchestrator** | Work planning, phase coordination | `/modes:orchestrator` |

| Skill | Purpose | Activation |
|-------|---------|-----------|
| **QA Gate** | Quality validation checklist | `/skills:qa-gate` |
| **Extract Learnings** | Session learning extraction | `/skills:extract-learnings` |

### Tool-Agnostic Design

Agent specs live in `agents/` as standalone markdown files that work with **any LLM tool**. Claude Code users get slash commands (`/modes:architect`) out of the box via thin wrappers in `.claude/commands/`.

### Two-Layer Architecture

Modes layer on top of the existing session protocol:

```
Layer 0: Session Protocol (always active)
  status → assemble → retrieve → extract

Layer 1: Agent Mode (optional, user-activated)
  persona + domain focus + specialized commands
```

---

## New Features

### Agent Modes

Each mode provides:
- **Persona** — role, expertise, communication style
- **Cortex integration** — which commands the agent uses, primary memory domains
- **Behaviors** — domain-specific analysis patterns
- **Commands** — `*help`, `*exit`, `*context`, plus mode-specific commands
- **Output format** — structured deliverables

**With Claude Code:**
```
/modes:architect
```

**With other LLM tools:**
```
Read agents/modes/architect.md and adopt that persona fully.
```

### Orchestrator Mode

The Orchestrator is a **planning mode** that produces phased work plans with mode assignments. It doesn't execute work directly — it plans which specialist handles each phase:

```
Phase 1: /modes:analyst    → Clarify requirements
Phase 2: /modes:architect  → Design solution
Phase 3: /modes:developer  → Implement
Phase 4: /skills:qa-gate   → Validate quality
```

### Workflow Skills

Skills are one-shot workflows (not persistent personas):

- **QA Gate** — Structured quality checklist covering code quality, correctness, security, testing, documentation, and UI
- **Extract Learnings** — Guided learning extraction with classification (type, domain, confidence) and user approval

### Architecture Decision

- **ADR-017**: Agent Orchestration Layer — single-source specs in `agents/` with Claude Code thin wrappers

---

## New Files

### Agent Specs (tool-agnostic)

```
agents/
├── README.md                    # Agent system overview
├── modes/
│   ├── analyst.md               # Requirements analyst
│   ├── architect.md             # Software architect
│   ├── developer.md             # Senior developer
│   ├── ux-designer.md           # UX designer
│   └── orchestrator.md          # Work planner
└── skills/
    ├── qa-gate.md               # Quality gate checklist
    └── extract-learnings.md     # Learning extraction
```

### Claude Code Wrappers

```
.claude/commands/
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

---

## Changes

### Documentation

Updated for v1.3.0:
- `README.md` — Agent Modes feature section
- `INSTALL.md` — Agent modes setup
- `CLAUDE.md` — Agent modes reference and when to suggest
- `global/CLAUDE.md` — Agent modes reference
- `docs/architecture.md` — Agent layer architecture
- `docs/cortex-spec.md` — Section 9: Agent Orchestration Layer
- `docs/user-guide.md` — Agent modes usage
- `docs/decisions.md` — ADR-017
- `docs/development-history.md` — v1.3.0 section
- `docs/session-protocol-v1.3.0.md` — Protocol with agent layer
- `CHANGELOG.md` — v1.3.0 entry

---

## Upgrade Guide

### From v1.2.0

No breaking changes. Agent modes are purely additive.

1. **Pull latest:**
   ```bash
   git pull origin main
   ```

2. **Agent modes are ready immediately:**
   - Claude Code users: `/modes:architect` works out of the box
   - Other tools: Point at `agents/modes/architect.md`

3. **Update global CLAUDE.md (optional):**
   - Add agent modes reference from `global/CLAUDE.md`

4. **No dependency changes** — no new Python packages required

### Fresh Installation

```bash
git clone https://github.com/nivanovsp/cortex.git
cd cortex
pip install -r requirements.txt
python -m cli init
```

---

## What's Next

Potential future enhancements (not committed):
- Incremental indexing
- Memory decay/archival
- Watch mode for auto-chunking
- Additional agent modes (QA, PM, DevOps)
- Mode-specific memory domain filters

---

*Cortex v1.3.0 - LLM-Native Context Management*
