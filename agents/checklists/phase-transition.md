# Phase Transition Checklist

Validates that the current phase is complete and the next phase is properly set up. Run this checklist before transitioning between phases or agents.

## Checklist

### Current Phase Completion
- [ ] All planned deliverables have been produced
- [ ] Acceptance criteria for the current phase are met
- [ ] Open questions are documented with owners assigned

### Handoff Prepared
- [ ] Handoff skill executed and output reviewed
- [ ] Key decisions recorded with rationale
- [ ] All artifacts listed and accessible
- [ ] Next agent identified and appropriate for upcoming work

### Risk Check
- [ ] Risks for the next phase identified and documented
- [ ] Mitigations are in place for high-priority risks
- [ ] No critical blockers remain unresolved

## Cortex Integration

Record checklist results as an experiential memory in the `GENERAL` domain:
```
python -m cli memory add --learning "Phase transition from {current} to {next}: {PASS/FAIL}" --domain GENERAL --type experiential
```

## Result
- **PASS** — All items checked, proceed to next phase
- **FAIL** — Items unchecked, address before proceeding
