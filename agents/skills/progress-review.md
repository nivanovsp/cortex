# Progress Review Skill

Performs a mid-project status assessment by comparing planned deliverables against actual progress. This skill does not activate a persistent mode — it runs once and produces output.

## When to Use

- At planned checkpoints during multi-phase projects
- When the user asks for a status update
- When a phase is taking longer than expected and reassessment is needed
- Before committing to the next phase of work

## Procedure

### 1. Retrieve the Plan

- Retrieve the project plan from Cortex: `retrieve --query "project plan {project}"`
- Retrieve all handoffs: `retrieve --query "handoff phase-transition {project}"`
- If no plan exists in Cortex, ask the user for the plan or reconstruct from context

### 2. Assess Each Phase

For each planned phase, determine:
- **Status**: Not Started / In Progress / Complete / Blocked
- **Deliverables**: Which are delivered, which are pending
- **Deviations**: Any changes from the original plan

### 3. Identify Blockers

- List anything preventing progress
- Distinguish between technical blockers and information/decision blockers
- Note which phases are affected by each blocker

### 4. Identify Gaps

- Compare what was planned vs. what has been delivered
- Flag any scope creep (work done that was not planned)
- Flag any missed items (planned work not yet addressed)

### 5. Recommend Adjustments

- Propose changes to the plan if needed
- Recommend re-prioritization if blockers cannot be resolved quickly
- Suggest phase reordering if dependencies have changed

## Cortex Integration

- Retrieve project plan: `retrieve --query "project plan {project}"`
- Retrieve handoffs: `retrieve --query "handoff phase-transition {project}"`
- Retrieve risk assessments: `retrieve --query "risk assessment {project}"`
- Store the review as a memory: `memory add --learning "Progress review for {project} - {summary}" --domain GENERAL --type experiential --confidence high`

## Output Format

```markdown
## Progress Review: {Project Name}

### Overall Status: {On Track / At Risk / Blocked}

### Phase Status

| # | Phase | Status | Deliverables | Notes |
|---|-------|--------|--------------|-------|
| 1 | {name} | Complete | All delivered | {notes} |
| 2 | {name} | In Progress | 2 of 3 delivered | {notes} |
| 3 | {name} | Not Started | — | {notes} |

### Blockers
| Blocker | Affected Phases | Type | Suggested Resolution |
|---------|----------------|------|---------------------|
| {blocker} | Phase 2, 3 | Technical/Decision | {resolution} |

### Gaps
- {planned item not yet delivered}
- {unplanned work that was added}

### Recommendations
1. {recommendation}
2. {recommendation}
```
