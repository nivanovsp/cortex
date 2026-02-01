# Requirements Complete Checklist

Validates that requirements analysis is thorough, unambiguous, and ready for design. Run this checklist before concluding requirements analysis.

## Checklist

### Completeness
- [ ] All functional requirements are documented
- [ ] Non-functional requirements (NFRs) are identified
- [ ] Stakeholders are mapped with roles and interests
- [ ] Dependencies on external systems or teams are listed

### Clarity
- [ ] No ambiguous language remains (e.g., "fast", "easy", "intuitive" without definition)
- [ ] No unstated assumptions — all assumptions are explicit
- [ ] Every requirement has acceptance criteria

### Testability
- [ ] Each requirement is measurable and verifiable
- [ ] Acceptance criteria use Given-When-Then format
- [ ] Edge cases are identified for each requirement

### Alignment
- [ ] Stakeholders agree on scope
- [ ] Conflicts between requirements are resolved
- [ ] Priorities are clear (must-have vs. nice-to-have)

## Cortex Integration

Record checklist results as an experiential memory in the `GENERAL` domain:
```
python -m cli memory add --learning "Requirements analysis complete: {PASS/FAIL}, {number} requirements documented" --domain GENERAL --type experiential
```

## Result
- **PASS** — All items checked, proceed to next phase
- **FAIL** — Items unchecked, address before proceeding
