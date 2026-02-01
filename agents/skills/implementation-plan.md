# Implementation Plan Skill

Plan implementation of a feature or fix with ordered steps and verification. This skill does not activate a persistent mode — it runs once and produces output.

## When to Use

- Before starting implementation of a non-trivial feature
- When a task involves coordinated changes across multiple files
- When the Orchestrator breaks a phase into implementation work
- When clarifying the approach before writing code

## Procedure

### 1. Break Task into Ordered Steps

- Decompose the feature/fix into discrete, sequential steps
- Each step should be small enough to verify independently
- Order steps so each builds on the previous (dependencies flow downward)

### 2. Identify Files to Create or Modify

For each step:
- List files that will be created
- List files that will be modified
- Note any files that will be deleted or renamed

### 3. Identify Dependencies Between Steps

- Map which steps block other steps
- Identify steps that can be done in parallel
- Note external dependencies (APIs, packages, configuration)

### 4. Define Verification Strategy Per Step

For each step, specify:
- How to verify it works (test, manual check, build succeeds)
- What the expected output or behavior is
- What regressions to watch for

### 5. Note Potential Risks

- What could go wrong during implementation?
- What assumptions are being made?
- Are there areas of the codebase that are fragile or poorly understood?

## Cortex Integration

- Retrieve existing code patterns and past implementation decisions before planning
- After completion, the plan can be fed into beads for task tracking
- Reference the `implementation-plan.yaml` template for structured output
- Store any discovered architectural constraints as `factual` memories

## Output Format

```markdown
## Implementation Plan: {feature/fix name}

### Overview
{Brief description of what will be implemented and why}

### Prerequisites
- {required before starting}

### Steps

#### Step 1: {description}
- **Files:** {create/modify/delete list}
- **Details:** {what to do}
- **Verify:** {how to confirm this step works}
- **Depends on:** {nothing or previous step}

#### Step 2: {description}
- **Files:** {create/modify/delete list}
- **Details:** {what to do}
- **Verify:** {how to confirm this step works}
- **Depends on:** Step 1

{continue for all steps}

### Dependency Graph
```
Step 1 → Step 2 → Step 4
              ↘ Step 3 → Step 5
```

### Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| {risk} | {impact} | {mitigation} |

### Assumptions
- {assumption being made}

### Definition of Done
- [ ] {criteria for considering this complete}
```
