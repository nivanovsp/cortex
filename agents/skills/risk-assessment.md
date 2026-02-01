# Risk Assessment Skill

Identifies and assesses project risks with likelihood, impact, and mitigation strategies. This skill does not activate a persistent mode — it runs once and produces output.

## When to Use

- During project planning to proactively identify risks
- When entering a new phase with unknown complexity
- When a blocker is encountered and broader risk review is warranted
- As part of a progress review to reassess the risk landscape

## Procedure

### 1. Gather Context

- Review the project plan, requirements, and architecture
- Retrieve prior risk assessments and learnings from Cortex
- Understand the current phase and upcoming work

### 2. Identify Risks by Category

Systematically consider risks in each category:
- **Technical**: Technology limitations, integration issues, performance concerns
- **Requirements**: Ambiguity, missing requirements, scope creep
- **Dependencies**: External services, third-party libraries, team dependencies
- **Knowledge**: Unfamiliar technology, missing expertise, undocumented systems
- **Quality**: Testing gaps, technical debt, regression risk

### 3. Assess Each Risk

For each identified risk:
- **Likelihood**: High / Medium / Low
- **Impact**: High / Medium / Low
- High likelihood + High impact = critical risk requiring immediate mitigation

### 4. Propose Mitigations

For each risk, propose one or more mitigation strategies:
- **Avoid**: Change the plan to eliminate the risk
- **Mitigate**: Take action to reduce likelihood or impact
- **Accept**: Acknowledge the risk and monitor it
- **Transfer**: Move the risk to another party or system

### 5. Prioritize

- Rank risks by combined likelihood and impact
- Identify the top 3-5 risks that need immediate attention

## Cortex Integration

- Retrieve prior risks: `retrieve --query "risk assessment {project}"`
- Retrieve project plan: `retrieve --query "project plan {project}"`
- Store the assessment: `memory add --learning "Risk assessment for {project} - {count} risks identified" --domain GENERAL --type experiential --confidence medium`

## Output Format

```markdown
## Risk Assessment: {Project/Phase Name}

### Risk Matrix

| # | Risk | Category | Likelihood | Impact | Priority | Mitigation |
|---|------|----------|-----------|--------|----------|------------|
| 1 | {risk} | Technical | High | High | Critical | {strategy} |
| 2 | {risk} | Requirements | Medium | High | High | {strategy} |
| 3 | {risk} | Dependencies | Medium | Medium | Medium | {strategy} |
| 4 | {risk} | Knowledge | Low | Medium | Low | {strategy} |

### Top Risks Requiring Attention
1. **{risk}** — {why this is critical and what to do}
2. **{risk}** — {why this is critical and what to do}
3. **{risk}** — {why this is critical and what to do}

### Accepted Risks
- {risk} — accepted because {rationale}

### Notes
- {any additional context or observations}
```
