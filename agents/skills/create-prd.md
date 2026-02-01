# Create PRD Skill

Produces a complete Product Requirements Document from gathered requirements and user input. This skill does not activate a persistent mode — it runs once and produces output.

## When to Use

- After requirements have been elicited and confirmed
- When a formal PRD is needed for a feature or project
- When transitioning from analysis to design/architecture phase

## Procedure

### 1. Gather Context

- Retrieve any existing requirements from Cortex
- Review elicited requirements if the `/skills:elicit-requirements` skill was run previously
- If requirements have not been gathered, run elicitation first or ask the user for input

### 2. Define Project Overview

- Product/feature name
- Problem statement
- Target users
- Success metrics (qualitative or quantitative)

### 3. Write User Stories

- Express requirements as user stories: "As a {role}, I want {action} so that {benefit}"
- Group user stories by theme or workflow
- Prioritize using MoSCoW: Must / Should / Could / Won't

### 4. Specify Functional Requirements

- Detail each functional requirement with:
  - Description
  - Inputs and outputs
  - Business rules
  - Acceptance criteria

### 5. Specify Non-Functional Requirements

- Performance targets
- Security requirements
- Accessibility standards
- Compatibility requirements
- Scalability considerations

### 6. Define Constraints and Dependencies

- Technical constraints
- Business constraints
- External dependencies
- Integration points

### 7. Write Acceptance Criteria

- Each requirement gets at least one acceptance criterion
- Use Given-When-Then format
- Include positive, negative, and edge case scenarios

### 8. Review with User

- Present the complete PRD
- Ask for corrections and additions
- Iterate until approved

## Cortex Integration

- Retrieve prior requirements: `retrieve --query "requirements {feature}"`
- Retrieve related PRDs: `retrieve --query "PRD {topic}"`
- Store the PRD: `memory add --learning "PRD for {feature} - {summary}" --domain GENERAL --type factual --confidence high`

## Output Format

```markdown
## Product Requirements Document: {Feature/Product Name}

### 1. Overview
**Problem:** {problem statement}
**Target Users:** {who this is for}
**Success Metrics:** {how success is measured}

### 2. User Stories

| # | Story | Priority |
|---|-------|----------|
| US-1 | As a {role}, I want {action} so that {benefit} | Must |
| US-2 | As a {role}, I want {action} so that {benefit} | Should |

### 3. Functional Requirements

#### FR-1: {Requirement Name}
**Description:** {detail}
**Business Rules:** {rules}
**Acceptance Criteria:**
- Given {context}, when {action}, then {outcome}

#### FR-2: {Requirement Name}
**Description:** {detail}
**Business Rules:** {rules}
**Acceptance Criteria:**
- Given {context}, when {action}, then {outcome}

### 4. Non-Functional Requirements

| # | Requirement | Category | Target |
|---|-------------|----------|--------|
| NFR-1 | {requirement} | Performance | {target} |
| NFR-2 | {requirement} | Security | {target} |

### 5. Constraints and Dependencies
**Constraints:**
- {constraint}

**Dependencies:**
- {dependency}

### 6. Out of Scope
- {explicitly excluded items}

### 7. Open Questions
- {any remaining questions}
```
