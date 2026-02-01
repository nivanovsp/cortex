# Cortex v2.0.0 Release Notes

**Release Date:** 2026-02-01

## Overview

Cortex v2.0.0 transforms the project from an LLM-native context engine into a **complete, self-contained software development methodology**. It provides everything needed to go from requirements to delivered software — 6 specialist agents, 29 workflow skills, 14 artifact templates, and 6 quality checklists — all powered by Cortex's semantic retrieval engine.

This is a major release. The version jump from 1.3.0 to 2.0.0 reflects the fundamental shift from "context management tool" to "complete development methodology."

## What's New

### Complete Agent System

**6 specialist agents**, each with dedicated skills, rules, templates, and a quality checklist:

| Agent | Activation | Skills | Focus |
|-------|-----------|--------|-------|
| Analyst | `/modes:analyst` | 5 | Requirements, gap analysis, acceptance criteria |
| Architect | `/modes:architect` | 6 | System design, trade-offs, ADRs, NFRs |
| Developer | `/modes:developer` | 4 | Implementation, debugging, code review |
| QA | `/modes:qa` | 5 | Test strategy, quality gates, acceptance review |
| UX Designer | `/modes:ux-designer` | 4 | Interface design, accessibility, user flows |
| Orchestrator | `/modes:orchestrator` | 5 | Work planning, phase coordination, handoffs |

### QA Agent (New)

Promoted from a single checklist skill to a full agent with 5 dedicated skills:
- `test-strategy` — Define test types, coverage, data needs
- `test-case-design` — Design test cases from acceptance criteria
- `quality-gate` — Comprehensive quality checklist
- `acceptance-review` — Verify against documented criteria
- `accessibility-review` — WCAG 2.1 AA compliance audit

### Decentralized Orchestration

**Any agent can be the entry point.** The Orchestrator is optional — use it when you want planning help, skip it when you know what to do.

Every agent follows the same activation flow:
1. Load mode spec → 2. Run status → 3. Greet → 4. User selects topic → 5. Retrieve context → 6. Work

### Agent-Specific Rules

Hard constraints baked into each agent's mode spec:

- **Developer:** Always verify library versions are current. Never use deprecated APIs.
- **Architect:** Validate technology choices against current LTS/stable releases.
- **Analyst:** Requirements must be unambiguous, clear, testable, measurable. No assumptions.
- **QA:** Test only against documented acceptance criteria. No assumed behavior.
- **All agents:** No time estimates or duration predictions.

### Handoff Protocol

A dedicated skill (`/skills:handoff`) for structured phase transitions:
- Summarizes accomplishments, decisions, open questions
- Stores as a Cortex memory with standardized keywords
- Next agent retrieves handoff context automatically

### Self-Indexing Methodology

The `bootstrap` command chunks all methodology resources into Cortex:
```bash
python -m cli bootstrap    # Chunk agents/ into METHODOLOGY domain
python -m cli index        # Rebuild indices
```

Agents retrieve skills on-demand via semantic search — no need to load all skills into context.

### 29 Workflow Skills

| Agent | Skills |
|-------|--------|
| Orchestrator | project-plan, phase-decomposition, handoff, progress-review, risk-assessment |
| Analyst | elicit-requirements, create-prd, gap-analysis, define-acceptance-criteria, stakeholder-analysis |
| Architect | system-design, api-design, nfr-assessment, create-adr, tech-evaluation, security-review |
| Developer | implementation-plan, code-review, debug-workflow, refactor-assessment |
| QA | test-strategy, test-case-design, quality-gate, acceptance-review, accessibility-review |
| UX Designer | wireframe, user-flow, design-system, usability-review |
| Shared | qa-gate, extract-learnings |

### 6 Quality Checklists

| Checklist | Agent | Purpose |
|-----------|-------|---------|
| phase-transition | Orchestrator | Verify before moving to next phase |
| requirements-complete | Analyst | Validate requirement completeness |
| architecture-ready | Architect | Confirm design readiness |
| implementation-done | Developer | Verify code completeness |
| release-ready | QA | Final quality validation |
| ux-complete | UX Designer | Confirm UX deliverables |

### 14 Artifact Templates

Templates for all major deliverables: project-brief, phase-plan, prd, requirements-spec, architecture, api-spec, adr, implementation-plan, code-review-report, test-plan, qa-report, wireframe, user-flow, design-system.

## What Changed

### Updated Mode Specs

All 5 existing modes updated with:
- **Rules section** — Non-negotiable constraints per agent
- **Skills section** — Available skills with descriptions
- **Updated activation flow** — Decentralized (greet → wait for topic → then retrieve)

### Updated Session Protocol

Session protocol v2.0.0 adds:
- Decentralized activation (topic-first loading)
- METHODOLOGY domain for self-indexed resources
- No-time-estimates as a global rule

### Bootstrap Command

New CLI command: `python -m cli bootstrap`
- Chunks `agents/` directory into METHODOLOGY domain
- `--force` flag for re-chunking
- 207 chunks generated from 56 methodology files

## Migration from v1.3.0

1. `git pull origin main`
2. Run `python -m cli bootstrap && python -m cli index`
3. New QA agent, skills, checklists, and templates available immediately
4. Existing agents updated with Rules and Skills sections
5. All existing chunks and memories remain compatible

## File Counts

| Category | v1.3.0 | v2.0.0 |
|----------|--------|--------|
| Agent modes | 5 | 6 |
| Skills | 2 | 31 |
| Checklists | 0 | 6 |
| Templates | 2 | 16 |
| Claude Code wrappers | 7 | 43 |
| CLI commands | 8 | 9 |

## Context Budget

Unchanged. The methodology uses Cortex's own retrieval — agents pull skills on-demand (~1,500 tokens per retrieval) instead of loading everything. Typical session context consumption remains ~3-5%.
