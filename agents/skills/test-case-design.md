# Test Case Design Skill

Design specific test cases from acceptance criteria. This skill does not activate a persistent mode — it runs once and produces output.

## When to Use

- When acceptance criteria are defined and need test coverage
- When translating user stories into verifiable test cases
- When ensuring edge cases and error paths are covered before implementation
- When a tester or developer needs structured test specifications

## Procedure

### 1. Gather Acceptance Criteria

- Collect all acceptance criteria for the feature or story
- Clarify any ambiguous criteria before proceeding
- Note any implicit requirements not captured in criteria

### 2. Design Test Cases Per Criterion

For each acceptance criterion, design the following:

#### Positive Test Cases (Expected Behavior)
- Verify the happy path works as specified
- Test with valid, typical input values
- Confirm expected system responses and state changes

#### Negative Test Cases (Invalid Input and Error Paths)
- Test with invalid input (wrong types, out of range, malformed)
- Test with missing required fields
- Test error messages and error handling behavior
- Test unauthorized or unauthenticated access where applicable

#### Edge Case Tests (Boundary Conditions)
- Test boundary values (min, max, just inside, just outside)
- Test with null, empty, and whitespace values
- Test with extremely large or extremely small values
- Test concurrent or duplicate submissions
- Test with special characters and unicode

### 3. Write Steps and Expected Results

For each test case:
- Write clear, numbered steps to reproduce
- Specify preconditions (state before test)
- Define expected results (what should happen)
- Note any postconditions (state after test)

## Cortex Integration

- Retrieve acceptance criteria from Cortex if stored as chunks
- Query for related test learnings (domain: `TEST`)
- After producing test cases, extract patterns as memories (domain: `TEST`, type: `procedural`)

## Output Format

```markdown
## Test Cases: {feature/story}

### Criterion: {acceptance criterion text}

#### TC-{N}.1: {Positive test name}
- **Type:** Positive
- **Preconditions:** {state before test}
- **Steps:**
  1. {action}
  2. {action}
- **Expected Result:** {what should happen}

#### TC-{N}.2: {Negative test name}
- **Type:** Negative
- **Preconditions:** {state before test}
- **Steps:**
  1. {action}
  2. {action}
- **Expected Result:** {error handling behavior}

#### TC-{N}.3: {Edge case test name}
- **Type:** Edge Case
- **Preconditions:** {state before test}
- **Steps:**
  1. {action}
  2. {action}
- **Expected Result:** {boundary behavior}

---

### Summary
| Criterion | Positive | Negative | Edge Case | Total |
|-----------|----------|----------|-----------|-------|
| {criterion} | {count} | {count} | {count} | {count} |
| **Total** | {sum} | {sum} | {sum} | {sum} |
```
