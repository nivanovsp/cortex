# Session Protocol v2.0.0

**Date:** 2026-02-01
**Status:** Active
**Supersedes:** Session Protocol v1.2.0 (in CLAUDE.md), Session Protocol v1.3.0

## Overview

Session Protocol v2.0.0 introduces **decentralized agent activation** and **self-indexing methodology resources**. The core protocol (status → assemble → retrieve → extract) remains unchanged. The key additions are:

1. **Any agent can start first** — no required Orchestrator entry point
2. **Topic-first loading** — agents greet first, retrieve context only after user selects a topic
3. **METHODOLOGY domain** — skills, templates, checklists retrievable via semantic search
4. **No time estimates** — enforced globally across all agents

## Protocol Layers

```
Layer 0: Session Protocol (always active)
  status → assemble → retrieve → extract
  Unchanged from v1.2.0

Layer 1: Agent Mode (optional)
  persona + rules + skills + domain focus
  Updated in v2.0.0 with decentralized activation
```

## Agent Activation Flow (New in v2.0.0)

### Without Mode (Base Protocol)

Same as v1.2.0:
1. Run `python -m cli status --json` silently
2. Note metadata (chunk count, memory count, domains, stale chunks)
3. Greet user, mention Cortex if relevant
4. Wait for task identification

### With Mode (Decentralized)

Every agent follows the same flow:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    AGENT ACTIVATION (v2.0.0)                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────┐                                                      │
│  │ MODE ACTIVATED │  /modes:{agent}                                      │
│  └───────┬────────┘                                                      │
│          │                                                               │
│          ▼                                                               │
│  ┌────────────────┐                                                      │
│  │ LOAD SPEC      │  Mode spec (~2KB)                                   │
│  │                │  • Persona, Rules, Skills list                      │
│  └───────┬────────┘                                                      │
│          │                                                               │
│          ▼                                                               │
│  ┌────────────────┐                                                      │
│  │ cli status     │  Metadata only (~50 tokens)                         │
│  │  [AUTOMATIC]   │                                                      │
│  └───────┬────────┘                                                      │
│          │                                                               │
│          ▼                                                               │
│  ┌────────────────┐                                                      │
│  │ GREET          │  State persona and capabilities                     │
│  │                │  "I'm the Architect. I focus on..."                 │
│  └───────┬────────┘                                                      │
│          │                                                               │
│          ▼                                                               │
│  ┌────────────────┐                                                      │
│  │ WAIT FOR TOPIC │  User selects what to work on                       │
│  │  [USER-DRIVEN] │  DO NOT pre-load or retrieve yet                    │
│  └───────┬────────┘                                                      │
│          │                                                               │
│          ▼                                                               │
│  ┌────────────────┐                                                      │
│  │ RETRIEVE       │  • Handoffs for this topic                          │
│  │ CONTEXT        │  • Existing artifacts                               │
│  │  [AUTOMATIC]   │  • Learnings                                        │
│  └───────┬────────┘  (~2,500 tokens via assemble)                       │
│          │                                                               │
│          ▼                                                               │
│  ┌────────────────┐                                                      │
│  │ WORK PHASE     │  Normal session protocol continues                  │
│  │                │  (retrieve on demand, extract on end)               │
│  └────────────────┘                                                      │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Key Difference from v1.3.0

| Aspect | v1.3.0 | v2.0.0 |
|--------|--------|--------|
| Entry point | Orchestrator recommended first | Any agent can start |
| Context loading | On activation | After user selects topic |
| Available resources | 5 modes, 2 skills | 6 modes, 29 skills, 6 checklists, 14 templates |
| Methodology retrieval | Not available | METHODOLOGY domain via bootstrap |
| Agent rules | Implicit in behavior | Explicit Rules section, enforced |

## Handoff Protocol (New in v2.0.0)

Phase transitions between agents use the handoff skill:

```
┌─────────────────┐     ┌────────────────────┐     ┌─────────────────┐
│ Current Agent   │────►│ /skills:handoff    │────►│ Next Agent      │
│ finishes work   │     │                    │     │ starts work     │
└─────────────────┘     │ Stores as memory:  │     └────────┬────────┘
                        │ type: procedural   │              │
                        │ keywords: handoff, │              ▼
                        │ phase-transition,  │     ┌────────────────┐
                        │ {agent}, {topic}   │     │ Retrieves      │
                        └────────────────────┘     │ handoff via    │
                                                   │ assemble/      │
                                                   │ retrieve       │
                                                   └────────────────┘
```

## Self-Indexing Methodology (New in v2.0.0)

### Bootstrap

```bash
python -m cli bootstrap          # Chunk agents/ into METHODOLOGY domain
python -m cli bootstrap --force  # Re-chunk after modifications
python -m cli index              # Rebuild indices
```

### How Agents Use It

When an agent needs a skill:
1. Agent knows skill names from its mode spec (Skills section)
2. Agent retrieves skill content from METHODOLOGY domain via semantic search
3. Agent executes the skill procedure
4. Context cost: ~1,500 tokens per skill retrieval

This keeps agent activation lightweight (~2KB mode spec) while giving access to the full methodology.

## Context Budget

| Phase | Tokens | % of 200k |
|-------|--------|-----------|
| Mode spec load | ~600 | 0.3% |
| Session start (metadata) | ~50 | 0.025% |
| Topic context (assembly) | ~2,500 | 1.25% |
| Skill retrieval (×1) | ~1,500 | 0.75% |
| On-demand retrieval (×2) | ~3,000 | 1.5% |
| **Typical agent session** | **~7,650** | **~3.8%** |

*96%+ of context remains for actual work.*

## Global Rules (New in v2.0.0)

These rules apply to ALL agents, ALL sessions:

1. **No time estimates** — No agent produces duration predictions, sprint sizing, or timeline estimates
2. **Topic-first loading** — Do not pre-load context before user selects a topic
3. **Commands are invisible** — Users interact through natural language
4. **Session end requires user trigger** — Never auto-extract learnings
5. **Handoffs are mandatory** — Between phases, always run the handoff skill (when using orchestrated workflow)
