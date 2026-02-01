# Handoff Skill

Executes a structured phase transition, capturing what was done, what was decided, and what the next agent needs to know. This skill does not activate a persistent mode — it runs once and produces output.

This is the key orchestration mechanism for multi-phase, multi-agent work. Every phase transition should use this skill to ensure continuity.

## When to Use

- When completing a phase and transitioning to the next agent or phase
- When ending a session that will be continued by another agent
- When the Orchestrator coordinates between specialist agents

## Procedure

### 1. Summarize Accomplishments

- List what was completed in the current phase
- Reference specific artifacts produced (files, documents, decisions)
- Note anything that was attempted but not completed, and why

### 2. Document Decisions

- List every significant decision made during this phase
- Include the rationale for each decision
- Note any alternatives that were considered and rejected

### 3. Capture Open Questions

- List questions that remain unanswered
- Indicate which questions block progress and which are informational
- Note any assumptions made in the absence of answers

### 4. List Artifacts

- Enumerate all artifacts produced (files, documents, designs, code)
- Include Cortex chunk references where applicable
- Note the state of each artifact (draft, final, needs review)

### 5. Brief the Next Agent

- State clearly what the next phase needs to accomplish
- Highlight critical context the next agent must understand
- Flag any risks or gotchas discovered during this phase
- Recommend which agent mode should handle the next phase

### 6. Store in Cortex

Store the handoff as a Cortex memory for retrieval by the next agent:

```
memory add --learning "Handoff: phase-transition from {current-agent} on {topic} - {one-line summary}" --context "{detailed handoff content}" --domain GENERAL --type procedural --confidence high
```

**Required keywords in the learning field:**
- "handoff"
- "phase-transition"
- The current agent name (e.g., "analyst", "architect")
- The topic or project name

This ensures the next agent can retrieve it with: `retrieve --query "handoff phase-transition {topic}"`

## Cortex Integration

- Retrieve prior handoffs for context: `retrieve --query "handoff {topic}"`
- Retrieve the project plan: `retrieve --query "project plan {topic}"`
- Store the handoff as described in Step 6 above
- The standardized keyword pattern enables reliable retrieval across sessions

## Output Format

```markdown
## Handoff: {Phase Name} -> {Next Phase Name}

### From
**Agent:** {agent mode}
**Phase:** {phase name/number}

### Accomplishments
- {what was completed}
- {what was completed}

### Decisions Made
| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| {decision} | {why} | {what else was considered} |

### Open Questions
| Question | Blocking? | Assumption Made |
|----------|-----------|-----------------|
| {question} | Yes/No | {assumption if any} |

### Artifacts Produced
| Artifact | Status | Location |
|----------|--------|----------|
| {name} | Draft/Final/Needs Review | {path or reference} |

### Next Phase Briefing
**Objective:** {what the next phase must accomplish}
**Recommended Agent:** {agent mode}
**Critical Context:**
- {key thing the next agent must know}
- {key thing the next agent must know}

**Risks/Gotchas:**
- {risk or gotcha}

### Cortex Memory
Stored as: `handoff: phase-transition from {agent} on {topic}`
```
