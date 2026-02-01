# Define Acceptance Criteria Skill

Converts requirements into testable acceptance criteria using Given-When-Then format. This skill does not activate a persistent mode — it runs once and produces output.

## When to Use

- After requirements have been defined and need verification criteria
- When preparing work for implementation to ensure shared understanding
- When existing acceptance criteria need review or refinement
- As part of QA preparation

## Procedure

### 1. Gather Requirements

- Retrieve or receive the list of requirements to convert
- Clarify any ambiguous requirements with the user before writing criteria

### 2. Write Positive Cases

For each requirement, write the primary success scenario:
- **Given** {precondition or initial state}
- **When** {action or event}
- **Then** {expected outcome}

### 3. Write Negative Cases

For each requirement, consider failure scenarios:
- Invalid input
- Missing required data
- Unauthorized access
- Exceeding limits or boundaries

### 4. Write Edge Cases

Consider boundary conditions and unusual scenarios:
- Empty collections or zero values
- Maximum/minimum values
- Concurrent operations
- First-time vs. repeat usage

### 5. Verify Measurability

For each criterion, confirm:
- The outcome is observable (can be seen, measured, or queried)
- The criterion is unambiguous (only one interpretation)
- The criterion is testable (an automated or manual test can verify it)

### 6. Review with User

- Present all criteria grouped by requirement
- Ask the user to confirm completeness
- Iterate until the user is satisfied

## Cortex Integration

- Retrieve requirements: `retrieve --query "requirements {feature}"`
- Retrieve prior acceptance criteria for patterns: `retrieve --query "acceptance criteria {topic}"`
- Store criteria: `memory add --learning "Acceptance criteria for {feature} - {count} criteria defined" --domain TEST --type factual --confidence high`

## Output Format

```markdown
## Acceptance Criteria: {Feature/Requirement Set}

### {Requirement FR-1}: {Requirement Name}

**Positive Cases:**
- Given {precondition}, when {action}, then {outcome}
- Given {precondition}, when {action}, then {outcome}

**Negative Cases:**
- Given {precondition}, when {invalid action}, then {error handling}
- Given {precondition}, when {unauthorized attempt}, then {rejection}

**Edge Cases:**
- Given {boundary condition}, when {action}, then {outcome}
- Given {empty state}, when {action}, then {outcome}

---

### {Requirement FR-2}: {Requirement Name}

**Positive Cases:**
- Given {precondition}, when {action}, then {outcome}

**Negative Cases:**
- Given {precondition}, when {invalid action}, then {error handling}

**Edge Cases:**
- Given {boundary condition}, when {action}, then {outcome}

---

### Summary
- **Total requirements covered:** {count}
- **Total criteria:** {count}
- **Positive cases:** {count}
- **Negative cases:** {count}
- **Edge cases:** {count}
```
