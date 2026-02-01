# Acceptance Review Skill

Verify implementation against documented acceptance criteria. This skill does not activate a persistent mode — it runs once and produces output.

## When to Use

- After a feature is implemented and before it is merged
- When validating that a story or task meets its definition of done
- When a product owner or QA reviewer needs a structured acceptance check
- Before closing a ticket or issue

## Procedure

### 1. Retrieve Acceptance Criteria

- Gather all documented acceptance criteria for the feature or story
- Source criteria from tickets, specs, or Cortex-stored chunks
- List each criterion explicitly before testing

### 2. Test Each Criterion Individually

For each acceptance criterion:
- Determine how to verify it (code inspection, running the application, automated test)
- Execute the verification
- Record the result as Pass or Fail
- Capture evidence of what was observed

### 3. Record Results with Evidence

For each criterion, document:
- The criterion text (verbatim)
- Pass or Fail status
- What was observed (specific output, behavior, or code reference)
- For failures: what happened instead of the expected behavior

### 4. Document Deviations

- Note any implemented behavior that differs from criteria, even if it passes
- Flag criteria that were interpreted or clarified during implementation
- Record any additional behavior implemented beyond the criteria

### 5. Flag Gaps

- Identify criteria that are ambiguous or untestable as written
- Note behaviors that are not covered by any criterion but seem important
- **Important:** Only test against documented criteria — if behavior is not specified, flag it as a gap rather than passing or failing it

## Cortex Integration

- Use `retrieve` to find acceptance criteria stored in Cortex chunks
- Query for related implementation context (domain: `GENERAL` or feature-specific)
- After review, extract any lessons about criteria quality as memories (domain: `TEST`, type: `experiential`)

## Output Format

```markdown
## Acceptance Review: {feature/story}

### Summary
- **Criteria Total:** {count}
- **Passed:** {count}
- **Failed:** {count}
- **Gaps Identified:** {count}

### Criterion Results

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | {criterion text} | Pass/Fail | {what was observed} |
| 2 | {criterion text} | Pass/Fail | {what was observed} |

### Failures
{For each failed criterion:}
#### AC-{N}: {criterion text}
- **Expected:** {what should happen}
- **Observed:** {what actually happened}
- **Impact:** {severity and affected areas}

### Deviations
{Behaviors that differ from criteria or extend beyond them}

### Gaps
{Criteria that are ambiguous, untestable, or missing}

### Verdict
{Accepted | Rejected — {reason} | Conditionally accepted — {conditions}}
```
