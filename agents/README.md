# Cortex Methodology — Agent System

Cortex ships with a complete agent system: expert personas with dedicated skills, artifact templates, and quality checklists. **Any agent can be your starting point** — there is no required entry sequence.

## Agents (6)

| Agent | Activation | Focus |
|-------|-----------|-------|
| [Analyst](modes/analyst.md) | `/modes:analyst` | Requirements, gap analysis, acceptance criteria |
| [Architect](modes/architect.md) | `/modes:architect` | System design, trade-offs, ADRs, NFRs |
| [Developer](modes/developer.md) | `/modes:developer` | Implementation, debugging, code review |
| [QA](modes/qa.md) | `/modes:qa` | Test strategy, quality gates, acceptance review |
| [UX Designer](modes/ux-designer.md) | `/modes:ux-designer` | Interface design, accessibility, user flows |
| [Orchestrator](modes/orchestrator.md) | `/modes:orchestrator` | Work planning, phase coordination, handoffs |

## Skills (29)

### Orchestrator Skills
| Skill | Activation | Purpose |
|-------|-----------|---------|
| [Project Plan](skills/project-plan.md) | `/skills:project-plan` | Define scope, phases, agent assignments |
| [Phase Decomposition](skills/phase-decomposition.md) | `/skills:phase-decomposition` | Break complex work into discrete phases |
| [Handoff](skills/handoff.md) | `/skills:handoff` | Structured phase transition protocol |
| [Progress Review](skills/progress-review.md) | `/skills:progress-review` | Compare delivered vs planned |
| [Risk Assessment](skills/risk-assessment.md) | `/skills:risk-assessment` | Identify risks, assess impact, propose mitigation |

### Analyst Skills
| Skill | Activation | Purpose |
|-------|-----------|---------|
| [Elicit Requirements](skills/elicit-requirements.md) | `/skills:elicit-requirements` | Structured questioning for complete requirements |
| [Create PRD](skills/create-prd.md) | `/skills:create-prd` | Produce Product Requirements Document |
| [Gap Analysis](skills/gap-analysis.md) | `/skills:gap-analysis` | Compare current vs desired state |
| [Define Acceptance Criteria](skills/define-acceptance-criteria.md) | `/skills:define-acceptance-criteria` | Convert requirements to testable criteria |
| [Stakeholder Analysis](skills/stakeholder-analysis.md) | `/skills:stakeholder-analysis` | Map stakeholders and their concerns |

### Architect Skills
| Skill | Activation | Purpose |
|-------|-----------|---------|
| [System Design](skills/system-design.md) | `/skills:system-design` | Design with options, trade-offs, recommendation |
| [API Design](skills/api-design.md) | `/skills:api-design` | Design endpoints, contracts, error handling |
| [NFR Assessment](skills/nfr-assessment.md) | `/skills:nfr-assessment` | Assess performance, security, scalability |
| [Create ADR](skills/create-adr.md) | `/skills:create-adr` | Architecture Decision Record |
| [Tech Evaluation](skills/tech-evaluation.md) | `/skills:tech-evaluation` | Evaluate technology options with criteria matrix |
| [Security Review](skills/security-review.md) | `/skills:security-review` | Threat modeling and vulnerability assessment |

### Developer Skills
| Skill | Activation | Purpose |
|-------|-----------|---------|
| [Implementation Plan](skills/implementation-plan.md) | `/skills:implementation-plan` | Break task into steps with file targets |
| [Code Review](skills/code-review.md) | `/skills:code-review` | Security, correctness, maintainability review |
| [Debug Workflow](skills/debug-workflow.md) | `/skills:debug-workflow` | Structured debugging procedure |
| [Refactor Assessment](skills/refactor-assessment.md) | `/skills:refactor-assessment` | Assess refactoring need and plan |

### QA Skills
| Skill | Activation | Purpose |
|-------|-----------|---------|
| [Test Strategy](skills/test-strategy.md) | `/skills:test-strategy` | Define test types, coverage, data needs |
| [Test Case Design](skills/test-case-design.md) | `/skills:test-case-design` | Design test cases from acceptance criteria |
| [Quality Gate](skills/quality-gate.md) | `/skills:quality-gate` | Comprehensive quality checklist |
| [Acceptance Review](skills/acceptance-review.md) | `/skills:acceptance-review` | Verify against documented criteria |
| [Accessibility Review](skills/accessibility-review.md) | `/skills:accessibility-review` | WCAG 2.1 AA compliance audit |

### UX Designer Skills
| Skill | Activation | Purpose |
|-------|-----------|---------|
| [Wireframe](skills/wireframe.md) | `/skills:wireframe` | Layout, states, annotations |
| [User Flow](skills/user-flow.md) | `/skills:user-flow` | Actor-goal-steps interaction mapping |
| [Design System](skills/design-system.md) | `/skills:design-system` | Components, tokens, guidelines |
| [Usability Review](skills/usability-review.md) | `/skills:usability-review` | Heuristic evaluation |

### Shared Skills
| Skill | Activation | Purpose |
|-------|-----------|---------|
| [QA Gate](skills/qa-gate.md) | `/skills:qa-gate` | Lightweight quality checklist |
| [Extract Learnings](skills/extract-learnings.md) | `/skills:extract-learnings` | Session learning extraction |

## Checklists (6)

| Checklist | Activation | Agent | Purpose |
|-----------|-----------|-------|---------|
| [Phase Transition](checklists/phase-transition.md) | `/checklists:phase-transition` | Orchestrator | Verify before moving to next phase |
| [Requirements Complete](checklists/requirements-complete.md) | `/checklists:requirements-complete` | Analyst | Validate requirement completeness |
| [Architecture Ready](checklists/architecture-ready.md) | `/checklists:architecture-ready` | Architect | Confirm design readiness |
| [Implementation Done](checklists/implementation-done.md) | `/checklists:implementation-done` | Developer | Verify code completeness |
| [Release Ready](checklists/release-ready.md) | `/checklists:release-ready` | QA | Final quality validation |
| [UX Complete](checklists/ux-complete.md) | `/checklists:ux-complete` | UX Designer | Confirm UX deliverables |

## Templates (14)

| Template | Agent | Purpose |
|----------|-------|---------|
| [Project Brief](templates/project-brief.yaml) | Orchestrator | Project overview, goals, scope |
| [Phase Plan](templates/phase-plan.yaml) | Orchestrator | Phase objectives, deliverables, criteria |
| [PRD](templates/prd.yaml) | Analyst | Product requirements document |
| [Requirements Spec](templates/requirements-spec.yaml) | Analyst | Detailed requirements specification |
| [Architecture](templates/architecture.yaml) | Architect | System design with options and trade-offs |
| [API Spec](templates/api-spec.yaml) | Architect | API endpoints and contracts |
| [ADR](templates/adr.yaml) | Architect | Architecture decision record |
| [Implementation Plan](templates/implementation-plan.yaml) | Developer | Step-by-step implementation plan |
| [Code Review Report](templates/code-review-report.yaml) | Developer | Review findings and recommendations |
| [Test Plan](templates/test-plan.yaml) | QA | Test strategy and test cases |
| [QA Report](templates/qa-report.yaml) | QA | Test results and recommendations |
| [Wireframe](templates/wireframe.yaml) | UX Designer | Layout and interaction design |
| [User Flow](templates/user-flow.yaml) | UX Designer | User interaction sequences |
| [Design System](templates/design-system.yaml) | UX Designer | Component system specification |

## Architecture

```
Layer 0: Session Protocol (always active)
  - Status on session start
  - Assemble on task identification
  - Retrieve on information request
  - Extract on session end

Layer 1: Agent Mode (optional, user-activated)
  - Persona with hard rules
  - Domain-filtered retrieval
  - Specialized skills and commands
  - Quality checklist at phase end
```

Modes don't replace the session protocol — they add a persona lens on top of it.

## Activation Flow

Every agent follows the same decentralized activation:

1. Load mode spec (~2KB — persona, rules, skills)
2. Run status — see what's in Cortex
3. Greet as persona — state what you can do
4. User selects topic/task
5. Retrieve handoffs, artifacts, learnings for that topic
6. Begin work with relevant context

**No agent is required as entry point.** Start with whichever agent fits your task.

## Usage

**With Claude Code:**
```
/modes:architect
/skills:system-design
/checklists:architecture-ready
```

**With other LLM tools:**
```
Read agents/modes/architect.md and adopt that persona fully.
Follow all instructions for the remainder of this conversation.
```

## Commands (Available in All Modes)

- `*help` — Show mode-specific commands
- `*exit` — Leave the current mode
- `*context` — Show gathered Cortex context summary

## Bootstrap

To make skills and templates retrievable via Cortex semantic search:

```bash
python -m cli bootstrap          # Chunk agents/ into METHODOLOGY domain
python -m cli bootstrap --force  # Re-chunk (delete old + create new)
python -m cli index              # Rebuild indices
```

## Example Workflows

### With Orchestrator
```
1. /modes:orchestrator     → Produce phased plan
2. /skills:handoff         → Transition to next phase
3. /modes:analyst          → Clarify requirements
4. /skills:handoff         → Transition
5. /modes:architect        → Design solution
6. /skills:handoff         → Transition
7. /modes:developer        → Implement
8. /modes:qa               → Validate quality
```

### Self-Orchestrated
```
1. /modes:analyst          → Start with requirements
2. /modes:architect        → Design solution
3. /modes:developer        → Implement
4. /skills:qa-gate         → Quick quality check
```
