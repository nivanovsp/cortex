# Stakeholder Analysis Skill

Maps all stakeholders, their concerns, influence levels, and communication needs. This skill does not activate a persistent mode — it runs once and produces output.

## When to Use

- At project inception to understand who is affected
- When requirements seem to conflict (different stakeholder priorities)
- When planning communication or review cycles
- Before making decisions that affect multiple parties

## Procedure

### 1. Identify Direct Stakeholders

- Who uses this system or feature directly?
- Who builds or maintains it?
- Who approves or funds the work?

### 2. Identify Indirect Stakeholders

- Who is affected by the system's output or behavior?
- Who depends on systems this integrates with?
- Who handles support or operations?
- Are there regulatory or compliance stakeholders?

### 3. Map Concerns and Interests

For each stakeholder:
- What do they care about most?
- What are their success criteria?
- What are their pain points or fears?

### 4. Assess Influence

Rate each stakeholder's influence on the project:
- **High**: Can approve, block, or fundamentally change direction
- **Medium**: Input is actively sought and usually incorporated
- **Low**: Informed but does not directly influence decisions

### 5. Define Communication Needs

For each stakeholder:
- What information do they need?
- When do they need it (at what milestones or frequency)?
- What format is appropriate (detailed report, summary, demo)?

### 6. Identify Conflicts

- Where do stakeholder interests conflict?
- Which conflicts need resolution before proceeding?
- Propose resolution approaches for identified conflicts

## Cortex Integration

- Retrieve prior stakeholder analyses: `retrieve --query "stakeholder analysis {project}"`
- Retrieve requirements for stakeholder references: `retrieve --query "requirements {project}"`
- Store the analysis: `memory add --learning "Stakeholder analysis for {project} - {count} stakeholders mapped" --domain GENERAL --type factual --confidence medium`

## Output Format

```markdown
## Stakeholder Analysis: {Project/Feature Name}

### Stakeholder Map

| Stakeholder | Role | Type | Key Concerns | Influence | Communication Needs |
|-------------|------|------|-------------|-----------|-------------------|
| {who} | {role} | Direct | {concerns} | High | {needs} |
| {who} | {role} | Direct | {concerns} | Medium | {needs} |
| {who} | {role} | Indirect | {concerns} | Low | {needs} |

### Influence Matrix

| | High Impact | Low Impact |
|---|-----------|-----------|
| **High Influence** | {stakeholders} — Manage closely | {stakeholders} — Keep satisfied |
| **Low Influence** | {stakeholders} — Keep informed | {stakeholders} — Monitor |

### Conflicts
| Conflict | Stakeholders | Proposed Resolution |
|----------|-------------|-------------------|
| {conflict} | {who vs. who} | {approach} |

### Notes
- {additional observations}
```
