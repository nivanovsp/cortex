# Create ADR Skill

Create an Architecture Decision Record documenting a significant technical decision. This skill does not activate a persistent mode — it runs once and produces output.

## When to Use

- When making a significant architectural or technology choice
- When a decision needs to be recorded for future reference
- When revisiting a past decision to understand the original rationale
- When the team needs alignment on a technical direction

## Procedure

### 1. Define Context

- What situation or problem prompted this decision?
- What forces are at play (technical, business, organizational)?
- What constraints exist?

### 2. List Options Considered

For each option:
- **Description** — what the option entails
- **Pros** — advantages
- **Cons** — disadvantages
- **Disqualifying factors** (if any) — why this option was ruled out

### 3. State the Decision

- Clearly state what was decided
- Provide the rationale — why this option over the others
- Tie the rationale to the specific context and constraints

### 4. Document Consequences

- **Positive consequences** — what improves as a result
- **Negative consequences** — what trade-offs are accepted
- **Neutral consequences** — what changes without clear positive/negative valence

### 5. Note Reversal Conditions

- What would cause this decision to be revisited?
- What signals would indicate the decision was wrong?
- What changes in context would invalidate the rationale?

## Cortex Integration

- Retrieve existing ADRs and related architectural context before starting
- After completion, store the decision as a `factual` memory (domain matching the decision area)
- Reference the `adr.yaml` template for structured output
- Link to related ADRs if they exist

## Output Format

```markdown
## ADR-{NNN}: {Decision Title}

**Status:** Accepted | Proposed | Deprecated | Superseded by ADR-{NNN}
**Date:** {YYYY-MM-DD}
**Deciders:** {who was involved}

### Context
{What prompted this decision. Forces, constraints, and background.}

### Options Considered

#### Option 1: {name}
- **Pros:** {list}
- **Cons:** {list}

#### Option 2: {name}
- **Pros:** {list}
- **Cons:** {list}

#### Option 3: {name} (if applicable)
- **Pros:** {list}
- **Cons:** {list}

### Decision
**We will use {Option X}: {name}.**

{Rationale explaining why, tied to context and constraints.}

### Consequences

**Positive:**
- {positive consequence}

**Negative:**
- {accepted trade-off}

**Neutral:**
- {change without clear valence}

### Reversal Conditions
- {what would cause us to revisit this decision}
- {signals that the decision was wrong}
```
