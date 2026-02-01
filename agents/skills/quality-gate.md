# Quality Gate Skill

Comprehensive quality validation checklist for release readiness. This skill does not activate a persistent mode — it runs once and produces output.

## When to Use

- Before a release or deployment
- After completing a significant feature or milestone
- When validating that all quality dimensions are covered
- As a broader alternative to the QA Gate skill (which focuses on code-level checks)

## Procedure

Run through each section systematically. Skip sections that do not apply (e.g., skip Accessibility for backend-only changes). Every applicable item must be evaluated.

### 1. Code Quality

- [ ] Changes are focused — no unrelated modifications
- [ ] No dead code, commented-out blocks, or TODO placeholders left behind
- [ ] Functions are single-purpose and reasonably sized
- [ ] Variable and function names are descriptive
- [ ] No hardcoded secrets, credentials, or environment-specific values
- [ ] Consistent code style throughout changes
- [ ] No unnecessary duplication

### 2. Correctness

- [ ] Happy path works as expected
- [ ] Error paths are handled (invalid input, missing data, network failures)
- [ ] Edge cases considered (empty collections, null values, boundary conditions)
- [ ] No regressions in existing functionality
- [ ] State management is correct (no stale state, race conditions)
- [ ] Data transformations produce correct results

### 3. Security

- [ ] User input is validated at system boundaries
- [ ] No SQL injection, XSS, or command injection vectors
- [ ] Authentication and authorization checks in place where needed
- [ ] Sensitive data not logged or exposed in error messages
- [ ] No secrets or credentials in committed code
- [ ] Dependencies checked for known vulnerabilities

### 4. Testing

- [ ] Tests exist for new and changed functionality
- [ ] Tests pass locally and in CI
- [ ] Edge cases have test coverage
- [ ] Test names describe the behavior being verified
- [ ] Integration points are tested
- [ ] No flaky or intermittent test failures introduced

### 5. Documentation

- [ ] Code changes match any related documentation
- [ ] API changes are reflected in specs or contracts
- [ ] Breaking changes are noted with migration guidance
- [ ] Configuration changes are documented
- [ ] Changelog or release notes updated if applicable

### 6. Accessibility (if applicable)

- [ ] Keyboard navigation works for all interactive elements
- [ ] Error states are announced to screen readers
- [ ] Loading states are communicated
- [ ] Responsive behavior is acceptable across breakpoints
- [ ] Color contrast meets WCAG AA (4.5:1 for text)
- [ ] Focus management is correct

### 7. Performance (if applicable)

- [ ] No N+1 query patterns
- [ ] No unnecessary memory allocations or object creation
- [ ] Response times are acceptable under expected load
- [ ] No blocking operations on the main thread (UI)
- [ ] Assets are appropriately sized and optimized
- [ ] Caching is used where beneficial

## Cortex Integration

- Retrieve prior quality issues from Cortex (domain: `TEST`, type: `experiential`)
- After completing the gate, record any new quality issues as memories
- Reference the `qa-report.yaml` template for structured output

## Output Format

```markdown
## Quality Gate: {feature/release}

### Result: PASS | FAIL

### Section Results

| Section | Status | Items Checked | Issues |
|---------|--------|---------------|--------|
| Code Quality | Pass/Fail | {n}/{total} | {count} |
| Correctness | Pass/Fail | {n}/{total} | {count} |
| Security | Pass/Fail | {n}/{total} | {count} |
| Testing | Pass/Fail | {n}/{total} | {count} |
| Documentation | Pass/Fail | {n}/{total} | {count} |
| Accessibility | Pass/Fail/Skip | {n}/{total} | {count} |
| Performance | Pass/Fail/Skip | {n}/{total} | {count} |

### Issues Found

| # | Section | Severity | Description | Recommendation |
|---|---------|----------|-------------|----------------|
| 1 | {section} | Critical/Major/Minor | {issue} | {fix} |

### Recommendation
{Ready for release | Blocked — must fix critical/major issues | Conditionally ready — minor issues noted}
```
