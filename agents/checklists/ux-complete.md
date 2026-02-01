# UX Complete Checklist

Validates that UX design work is thorough, accessible, and ready for implementation. Run this checklist before concluding UX design work.

## Checklist

### Completeness
- [ ] User flows are documented for all scenarios
- [ ] Wireframes cover all screens and states
- [ ] Design system is followed consistently

### States
- [ ] All component states are defined: default, hover, active, disabled, loading, error, empty, success

### Accessibility
- [ ] WCAG 2.1 AA compliance is verified
- [ ] Keyboard navigation is specified
- [ ] Screen reader behavior is defined
- [ ] Color contrast meets standards

### Responsiveness
- [ ] Mobile behavior is specified
- [ ] Tablet behavior is specified
- [ ] Desktop behavior is specified (if web-based)

## Cortex Integration

Record checklist results as an experiential memory in the `UI` domain:
```
python -m cli memory add --learning "UX design complete: {PASS/FAIL}, {summary of deliverables}" --domain UI --type experiential
```

## Result
- **PASS** — All items checked, proceed to next phase
- **FAIL** — Items unchecked, address before proceeding
