# Project Plan Skill

Creates a phased project work plan with scope definition, agent assignments, and risk identification. This skill does not activate a persistent mode — it runs once and produces output.

## When to Use

- At the start of a new project or initiative
- When a complex task needs structured breakdown before work begins
- When multiple agents will collaborate on a deliverable

## Procedure

### 1. Define Scope

- Clarify the project objective with the user
- Explicitly list what is **in scope**
- Explicitly list what is **out of scope**
- Surface any ambiguities and resolve with the user before proceeding

### 2. Identify Phases

- Break the work into sequential or parallel phases
- Each phase should have a clear, singular objective
- Map dependencies between phases (which phases block others)

### 3. Assign Agents

- For each phase, recommend the most appropriate agent mode:
  - **Analyst** — requirements, gap analysis, acceptance criteria
  - **Architect** — system design, trade-offs, ADRs
  - **Developer** — implementation, debugging, code review
  - **UX Designer** — interface design, accessibility
  - **Orchestrator** — coordination, handoffs, progress reviews

### 4. Define Deliverables

- List concrete deliverables for each phase
- Deliverables must be verifiable (a document, artifact, passing test, etc.)

### 5. Identify Risks

- List risks that could impact the plan
- Assess each as High / Medium / Low likelihood and impact
- Propose a mitigation strategy for each

### 6. Define Handoff Points

- Identify where phase transitions occur
- Specify what information must transfer between phases
- Reference the `/skills:handoff` skill for executing transitions

## Cortex Integration

- Retrieve prior project plans and learnings: `retrieve --query "project plan {topic}"`
- After user approval, store the plan as a Cortex memory: `memory add --learning "Project plan for {project}" --domain GENERAL --type procedural --confidence high`

## Output Format

```markdown
## Project Plan: {Project Name}

### Objective
{One-sentence project objective}

### Scope
**In Scope:**
- {item}

**Out of Scope:**
- {item}

### Phases

| # | Phase | Objective | Agent | Deliverables | Dependencies |
|---|-------|-----------|-------|--------------|--------------|
| 1 | {name} | {objective} | {agent mode} | {deliverables} | None |
| 2 | {name} | {objective} | {agent mode} | {deliverables} | Phase 1 |

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| {risk} | H/M/L | H/M/L | {strategy} |

### Handoff Points
- Phase 1 -> Phase 2: {what transfers}
- Phase 2 -> Phase 3: {what transfers}
```
