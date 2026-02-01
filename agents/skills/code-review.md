# Code Review Skill

Review code for quality, correctness, security, and maintainability. This skill does not activate a persistent mode — it runs once and produces output.

## When to Use

- When reviewing code changes before merge
- When auditing an existing module for quality issues
- When onboarding to unfamiliar code and assessing its state
- When the QA gate identifies areas needing deeper review

## Procedure

### 1. Security

- Check for injection vulnerabilities (SQL, XSS, command injection)
- Verify input validation at system boundaries
- Confirm authentication/authorization is correctly enforced
- Check that secrets are not hardcoded or logged
- Verify sensitive data handling (PII, tokens, passwords)

### 2. Correctness

- Trace logic paths for expected behavior
- Identify edge cases (null, empty, boundary values, concurrent access)
- Verify error handling (are errors caught, logged, and handled appropriately?)
- Check return values and type correctness
- Look for off-by-one errors, race conditions, resource leaks

### 3. Maintainability

- Assess naming clarity (do names reveal intent?)
- Check function size and single-responsibility adherence
- Evaluate coupling between modules
- Look for code duplication that should be extracted
- Check cyclomatic complexity of critical paths

### 4. Performance

- Identify N+1 query patterns
- Check for unnecessary allocations or copies in hot paths
- Look for missing pagination on collection endpoints
- Verify appropriate use of caching
- Check for blocking operations in async contexts

### 5. Positive Patterns

- Identify well-written code worth preserving
- Note good abstractions, clear naming, or effective patterns
- Highlight test quality and coverage strengths

## Cortex Integration

- Retrieve known issues and patterns for the files under review
- After completion, store recurring issues as `experiential` memories (domain matching the code area)
- Reference the `code-review-report.yaml` template for structured output

## Output Format

```markdown
## Code Review: {scope description}

### Summary
{Overall assessment — 1-2 sentences}

### Issues

#### Critical
| # | File | Line(s) | Issue | Recommendation |
|---|------|---------|-------|----------------|
| 1 | {file} | {lines} | {issue} | {fix} |

#### High
| # | File | Line(s) | Issue | Recommendation |
|---|------|---------|-------|----------------|
| 1 | {file} | {lines} | {issue} | {fix} |

#### Medium
| # | File | Line(s) | Issue | Recommendation |
|---|------|---------|-------|----------------|
| 1 | {file} | {lines} | {issue} | {fix} |

#### Low / Suggestions
| # | File | Line(s) | Issue | Recommendation |
|---|------|---------|-------|----------------|
| 1 | {file} | {lines} | {suggestion} | {improvement} |

### Positive Patterns
- {good pattern observed and where}

### Statistics
- **Files reviewed:** {count}
- **Critical issues:** {count}
- **High issues:** {count}
- **Medium issues:** {count}
- **Low/Suggestions:** {count}

### Verdict
{Approve | Approve with suggestions | Request changes}
```
