# Architecture Ready Checklist

Validates that the architecture and design are sound, complete, and feasible. Run this checklist before concluding architecture or design work.

## Checklist

### Design Quality
- [ ] Multiple options were evaluated, not just one
- [ ] Trade-offs are documented for each option
- [ ] An ADR (Architecture Decision Record) has been created
- [ ] The recommendation is justified with clear rationale

### Completeness
- [ ] Component diagram is defined
- [ ] Data flow is documented
- [ ] API contracts are specified
- [ ] Error handling strategy is designed

### Technical Currency
- [ ] All recommended technologies are current stable or LTS versions
- [ ] No deprecated dependencies are included
- [ ] Security concerns are addressed

### Feasibility
- [ ] Design maps to documented requirements
- [ ] Non-functional requirements are achievable with this design
- [ ] Integration points with external systems are identified

## Cortex Integration

Record checklist results as an experiential memory in the `DEV` domain:
```
python -m cli memory add --learning "Architecture review complete: {PASS/FAIL}, ADR-{number} created" --domain DEV --type experiential
```

## Result
- **PASS** — All items checked, proceed to next phase
- **FAIL** — Items unchecked, address before proceeding
