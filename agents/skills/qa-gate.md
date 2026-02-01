# QA Gate Skill

A structured quality validation checklist to run before considering work complete. This skill does not activate a persistent mode — it runs once and produces a pass/fail report.

## When to Use

- After implementing a feature or fix
- Before creating a pull request
- When the Orchestrator's plan includes a QA phase

## Procedure

When invoked, run through each section systematically. Skip sections that don't apply (e.g., skip UI checks for backend-only changes).

### 1. Code Quality

- [ ] Changes are focused — no unrelated modifications
- [ ] No dead code, commented-out blocks, or TODO placeholders left behind
- [ ] Functions are single-purpose and reasonably sized
- [ ] Variable and function names are descriptive
- [ ] No hardcoded secrets, credentials, or environment-specific values

### 2. Correctness

- [ ] Happy path works as expected
- [ ] Error paths are handled (invalid input, missing data, network failures)
- [ ] Edge cases considered (empty collections, null values, boundary conditions)
- [ ] No regressions in existing functionality

### 3. Security

- [ ] User input is validated at system boundaries
- [ ] No SQL injection, XSS, or command injection vectors
- [ ] Authentication/authorization checks in place where needed
- [ ] Sensitive data not logged or exposed in error messages

### 4. Testing

- [ ] Tests exist for new/changed functionality
- [ ] Tests pass locally
- [ ] Test names describe the behavior being verified
- [ ] Edge cases have test coverage

### 5. Documentation

- [ ] Code changes match any related documentation
- [ ] API changes are reflected in specs/contracts
- [ ] Breaking changes are noted

### 6. UI (if applicable)

- [ ] Keyboard navigation works
- [ ] Error states display correctly
- [ ] Loading states are present
- [ ] Empty states are handled
- [ ] Responsive behavior is acceptable

## Cortex Integration

After completing the gate:
- Use `memory add` to record any quality issues discovered (domain: `TEST`, type: `experiential`)
- Retrieved context may highlight prior issues to watch for

## Output Format

```markdown
## QA Gate: {feature/change}

### Result: PASS | FAIL

### Checks
| Section | Status | Notes |
|---------|--------|-------|
| Code Quality | Pass/Fail | ... |
| Correctness | Pass/Fail | ... |
| Security | Pass/Fail | ... |
| Testing | Pass/Fail | ... |
| Documentation | Pass/Fail | ... |
| UI | Pass/Skip/Fail | ... |

### Issues Found
1. {issue} — {severity} — {recommendation}

### Recommendation
{Ready to merge | Needs fixes before merge}
```
