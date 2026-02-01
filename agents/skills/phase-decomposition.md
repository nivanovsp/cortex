# Phase Decomposition Skill

Breaks complex work into discrete phases with clear boundaries, objectives, and entry/exit criteria. This skill does not activate a persistent mode — it runs once and produces output.

## When to Use

- When a project or feature is too large to execute in a single pass
- When work needs to be divided among multiple agents or sessions
- When dependencies between work items need explicit mapping

## Procedure

### 1. Understand the Whole

- Review the full scope of work with the user
- Identify the end state and key deliverables

### 2. Identify Natural Boundaries

- Look for shifts in concern (e.g., analysis vs. design vs. implementation)
- Look for dependency gates (one thing must complete before another starts)
- Look for agent transitions (different expertise needed)
- Prefer phases that can be completed in a single session where possible

### 3. Define Phase Objectives

- Each phase gets exactly one clear objective
- The objective must be concrete and verifiable
- Avoid vague objectives like "prepare" or "review" without specifics

### 4. Map Dependencies

- Identify which phases block other phases
- Identify which phases can run in parallel
- Flag any circular dependencies as design problems to resolve

### 5. Specify Entry/Exit Criteria

- **Entry criteria**: What must be true before this phase can start
- **Exit criteria**: What must be true before this phase is considered complete
- Exit criteria of one phase should align with entry criteria of dependent phases

## Cortex Integration

- Retrieve prior decompositions for similar work: `retrieve --query "phase decomposition {topic}"`
- Store the decomposition as a memory for future reference: `memory add --learning "Phase decomposition for {topic}" --domain GENERAL --type procedural --confidence high`

## Output Format

```markdown
## Phase Decomposition: {Work Item}

### Overview
{Brief description of the full scope being decomposed}

### Phases

| # | Phase | Objective | Dependencies | Entry Criteria | Exit Criteria |
|---|-------|-----------|--------------|----------------|---------------|
| 1 | {name} | {objective} | None | {criteria} | {criteria} |
| 2 | {name} | {objective} | Phase 1 | {criteria} | {criteria} |
| 3 | {name} | {objective} | Phase 1 | {criteria} | {criteria} |
| 4 | {name} | {objective} | Phase 2, 3 | {criteria} | {criteria} |

### Dependency Graph
{Text representation of phase dependencies}

### Parallel Opportunities
- Phases {X} and {Y} can run in parallel after Phase {Z} completes

### Notes
- {Any important considerations about the decomposition}
```
