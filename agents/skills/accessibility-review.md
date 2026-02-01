# Accessibility Review Skill

WCAG 2.1 AA compliance audit for interface components or pages. This skill does not activate a persistent mode — it runs once and produces output.

## When to Use

- Before releasing a user-facing feature
- When auditing an existing interface for accessibility compliance
- When accessibility is a requirement in acceptance criteria
- When evaluating a component library or design system for inclusivity

## Procedure

Evaluate the interface against the four WCAG 2.1 principles, then perform targeted checks for common interaction patterns.

### 1. Perceivable

- [ ] **Text alternatives** — All non-text content has a text alternative (alt text, aria-label)
- [ ] **Captions** — Time-based media has captions or transcripts
- [ ] **Adaptable** — Content can be presented in different ways without losing information (semantic HTML, correct heading hierarchy)
- [ ] **Distinguishable** — Text contrast ratio is at least 4.5:1 for normal text, 3:1 for large text
- [ ] **Distinguishable** — Text can be resized up to 200% without loss of content or function
- [ ] **Distinguishable** — Color is not the sole means of conveying information

### 2. Operable

- [ ] **Keyboard accessible** — All functionality is available via keyboard
- [ ] **No keyboard traps** — Focus can be moved away from every component
- [ ] **Enough time** — Users can extend or dismiss time limits
- [ ] **No seizure triggers** — No content flashes more than 3 times per second
- [ ] **Navigable** — Pages have descriptive titles, focus order is logical
- [ ] **Navigable** — Link purpose is clear from link text or context
- [ ] **Input modalities** — Functionality is not dependent on specific input (e.g., multi-point gestures have single-pointer alternatives)

### 3. Understandable

- [ ] **Readable** — Language of the page is programmatically determinable
- [ ] **Predictable** — Navigation is consistent across pages, components behave predictably
- [ ] **Input assistance** — Labels are present for inputs, errors are identified and described, suggestions are provided where possible

### 4. Robust

- [ ] **Compatible** — Valid HTML, ARIA roles and properties used correctly
- [ ] **Compatible** — Status messages are programmatically determinable without receiving focus
- [ ] **Compatible** — Works with common assistive technologies (screen readers, magnifiers)

### 5. Keyboard Navigation Check

- [ ] All interactive elements are reachable via Tab/Shift+Tab
- [ ] Tab order follows a logical reading order
- [ ] Focus indicator is visible on every focused element
- [ ] No focus traps (user can always navigate away)
- [ ] Custom widgets support expected keyboard patterns (arrow keys for menus, Escape to close modals)

### 6. Screen Reader Check

- [ ] Images have meaningful alt text (or are marked decorative)
- [ ] Form inputs have associated labels
- [ ] Dynamic content changes are announced (aria-live regions)
- [ ] Heading hierarchy is logical (h1 > h2 > h3, no skipped levels)
- [ ] Landmark regions are used appropriately (nav, main, aside)

### 7. Color and Contrast Check

- [ ] Color is not the sole indicator of state (errors, success, selection)
- [ ] Text contrast meets minimum ratios (4.5:1 normal, 3:1 large)
- [ ] UI component and graphical object contrast is at least 3:1
- [ ] Interface is usable in high-contrast mode

## Cortex Integration

- Retrieve prior accessibility findings from Cortex (domain: `UI`, type: `experiential`)
- Query for component-specific accessibility requirements
- After review, extract findings as memories (domain: `UI`, type: `experiential`)

## Output Format

```markdown
## Accessibility Review: {component/page}

### Summary
- **Standard:** WCAG 2.1 AA
- **Scope:** {what was audited}
- **Result:** {Compliant | Non-compliant — {n} issues}

### Findings by Principle

#### Perceivable
| # | WCAG Criterion | Status | Finding | Fix |
|---|---------------|--------|---------|-----|
| 1 | {e.g., 1.1.1 Non-text Content} | Pass/Fail | {observation} | {specific fix} |

#### Operable
| # | WCAG Criterion | Status | Finding | Fix |
|---|---------------|--------|---------|-----|
| 1 | {e.g., 2.1.1 Keyboard} | Pass/Fail | {observation} | {specific fix} |

#### Understandable
| # | WCAG Criterion | Status | Finding | Fix |
|---|---------------|--------|---------|-----|
| 1 | {e.g., 3.3.2 Labels} | Pass/Fail | {observation} | {specific fix} |

#### Robust
| # | WCAG Criterion | Status | Finding | Fix |
|---|---------------|--------|---------|-----|
| 1 | {e.g., 4.1.2 Name, Role, Value} | Pass/Fail | {observation} | {specific fix} |

### Targeted Checks
| Area | Status | Notes |
|------|--------|-------|
| Keyboard Navigation | Pass/Fail | {details} |
| Screen Reader | Pass/Fail | {details} |
| Color and Contrast | Pass/Fail | {details} |

### Priority Fixes
1. **Critical:** {issue} — {fix}
2. **Major:** {issue} — {fix}
3. **Minor:** {issue} — {fix}
```
