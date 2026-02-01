# Implementation Done Checklist

Validates that implementation is complete, high-quality, and ready for review. Run this checklist before concluding implementation work.

## Checklist

### Code Complete
- [ ] All planned changes are implemented
- [ ] No TODO or FIXME placeholders remain
- [ ] Code follows project conventions

### Quality
- [ ] No hardcoded secrets or credentials
- [ ] No deprecated APIs used
- [ ] Libraries are current versions
- [ ] Functions are single-purpose and focused

### Testing
- [ ] Tests exist for new or changed code
- [ ] All tests pass
- [ ] Edge cases are covered
- [ ] No regressions introduced

### Review Ready
- [ ] Changes are focused with no unrelated modifications
- [ ] Code is readable and self-documenting
- [ ] Security boundaries are validated

## Cortex Integration

Record checklist results as an experiential memory in the `DEV` domain:
```
python -m cli memory add --learning "Implementation complete: {PASS/FAIL}, {summary of changes}" --domain DEV --type experiential
```

## Result
- **PASS** — All items checked, proceed to next phase
- **FAIL** — Items unchecked, address before proceeding
