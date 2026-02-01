# Tech Evaluation Skill

Evaluate technology options against defined criteria with a comparison matrix. This skill does not activate a persistent mode — it runs once and produces output.

## When to Use

- When choosing between libraries, frameworks, or tools
- When evaluating whether to adopt a new technology
- When comparing build-vs-buy options
- When a technology decision needs structured justification

## Procedure

### 1. Define Evaluation Criteria

Establish criteria relevant to the decision. Common criteria include:
- **Maturity** — how established and battle-tested is it?
- **Community** — size, activity, ecosystem of plugins/extensions
- **Performance** — benchmarks relevant to the use case
- **Learning curve** — ease of adoption for the team
- **License** — compatibility with project requirements
- **Maintenance status** — release frequency, responsiveness to issues
- **Integration** — compatibility with existing stack
- **Documentation** — quality and completeness

Weight criteria by importance for the specific decision.

### 2. Score Each Option

- Evaluate each technology against every criterion
- Use a consistent scale (e.g., 1-5 or Low/Medium/High)
- Provide brief justification for each score
- Note any disqualifying factors

### 3. Present Comparison Matrix

- Side-by-side comparison of all options
- Weighted scores if criteria have different importance
- Highlight clear winners and close calls per criterion

### 4. Recommend with Justification

- State the recommended technology
- Explain why it won overall, not just on individual criteria
- Note any caveats or conditions for the recommendation
- Identify migration/adoption considerations

**IMPORTANT:** Always verify that recommended technologies are current stable/LTS releases. Use web search when uncertain about version status, end-of-life dates, or recent breaking changes.

## Cortex Integration

- Retrieve existing technology decisions and stack context before starting
- After completion, store the evaluation result as a `factual` memory (domain: `DEV`)
- If the evaluation leads to adoption, create a follow-up ADR

## Output Format

```markdown
## Tech Evaluation: {decision description}

### Context
{What we need and why we're evaluating options}

### Criteria
| Criterion | Weight | Description |
|-----------|--------|-------------|
| {criterion} | {weight} | {what we're measuring} |

### Options Evaluated

#### {Technology A} (v{version})
- **License:** {license}
- **Latest stable:** {version and date}
- **Summary:** {brief description}

#### {Technology B} (v{version})
{same structure}

### Comparison Matrix
| Criterion | Weight | {Tech A} | {Tech B} | {Tech C} |
|-----------|--------|----------|----------|----------|
| {criterion} | {weight} | {score} | {score} | {score} |
| ... | ... | ... | ... | ... |
| **Weighted Total** | | **{total}** | **{total}** | **{total}** |

### Recommendation
**Recommended: {Technology X}**

{Justification tied to criteria and context}

### Caveats
- {conditions or limitations of the recommendation}

### Adoption Considerations
- {migration steps, learning resources, timeline factors}
```
