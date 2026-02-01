# Elicit Requirements Skill

Conducts structured requirements elicitation through focused questioning and assumption surfacing. This skill does not activate a persistent mode — it runs once and produces output.

## When to Use

- At the start of a new feature or project before any design or implementation
- When requirements are vague, incomplete, or contradictory
- When the Analyst agent needs to gather information from the user

## Procedure

### 1. Understand the Goal

- Ask the user to describe what they need in their own words
- Identify the core problem being solved
- Ask: "Who is this for?" and "What does success look like?"

### 2. Ask Focused Questions

Follow the global question protocol: **ask one question at a time** and wait for the response.

Work through these areas systematically:

**Functional Requirements:**
- What must the system do?
- What are the key user actions?
- What inputs and outputs are expected?

**Non-Functional Requirements:**
- Performance expectations
- Security requirements
- Accessibility needs
- Compatibility constraints

**Stakeholders:**
- Who uses this directly?
- Who is affected indirectly?
- Who approves or owns the outcome?

**Edge Cases:**
- What happens with invalid input?
- What happens at scale boundaries?
- What happens when dependencies fail?

### 3. Surface Assumptions

- Explicitly state any assumption you are making
- Ask the user to confirm or correct each assumption
- **Never silently assume** — every gap must be surfaced

### 4. Identify Dependencies

- What existing systems or components does this depend on?
- What other work must complete before or after this?
- Are there external dependencies (APIs, services, approvals)?

### 5. Define Acceptance Criteria

- For each functional requirement, draft a testable acceptance criterion
- Use Given-When-Then format where applicable
- Verify with the user that the criteria match their intent

### 6. Compile and Verify

- Present the full requirements document to the user
- Ask them to review for completeness and accuracy
- Iterate until the user confirms the requirements are complete

## Cortex Integration

- Retrieve prior requirements for related work: `retrieve --query "requirements {topic}"`
- Store finalized requirements: `memory add --learning "Requirements for {feature} - {count} functional, {count} NFRs" --domain GENERAL --type factual --confidence high`

## Output Format

```markdown
## Requirements: {Feature/Project Name}

### Problem Statement
{What problem is being solved and for whom}

### Functional Requirements
| # | Requirement | Priority | Acceptance Criteria |
|---|-------------|----------|-------------------|
| FR-1 | {requirement} | Must/Should/Could | {criteria} |
| FR-2 | {requirement} | Must/Should/Could | {criteria} |

### Non-Functional Requirements
| # | Requirement | Category | Criteria |
|---|-------------|----------|----------|
| NFR-1 | {requirement} | Performance | {measurable criteria} |
| NFR-2 | {requirement} | Security | {measurable criteria} |

### Stakeholders
| Stakeholder | Role | Key Concern |
|-------------|------|-------------|
| {who} | {role} | {concern} |

### Assumptions
- {assumption} — confirmed by user / pending confirmation

### Dependencies
- {dependency}

### Edge Cases
- {edge case and expected behavior}

### Open Questions
- {any remaining questions}
```
