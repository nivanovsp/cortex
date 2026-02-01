# Release Ready Checklist

Validates that the work meets acceptance criteria and is safe to release. Run this checklist before approving for release.

## Checklist

### Acceptance Criteria
- [ ] All documented acceptance criteria are verified with evidence
- [ ] No criteria have been skipped
- [ ] Any deviations from original criteria are documented and approved

### Test Coverage
- [ ] Positive (happy) paths are tested
- [ ] Negative and error paths are tested
- [ ] Edge cases are tested
- [ ] Accessibility is validated

### Regression
- [ ] Existing functionality is verified to still work
- [ ] No new defects have been introduced
- [ ] Performance is acceptable

### Documentation
- [ ] Changes are reflected in documentation
- [ ] API changes are documented
- [ ] Breaking changes are noted with migration guidance

## Cortex Integration

Record checklist results as an experiential memory in the `TEST` domain:
```
python -m cli memory add --learning "Release validation: {PASS/FAIL}, {version}" --domain TEST --type experiential
```

## Result
- **PASS** — All items checked, proceed to next phase
- **FAIL** — Items unchecked, address before proceeding
