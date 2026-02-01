# Test Strategy Skill

Define a comprehensive testing strategy for a feature or project. This skill does not activate a persistent mode — it runs once and produces output.

## When to Use

- At the start of a new feature or project
- When planning a testing approach for a complex change
- When the current test coverage is unclear or insufficient
- When onboarding a new component that needs test infrastructure

## Procedure

### 1. Identify What Needs Testing

- List all components, modules, or features in scope
- Identify integration points between components
- Note external dependencies (APIs, databases, third-party services)
- Determine which areas carry the most risk

### 2. Determine Test Types Needed

For each area in scope, assess which test types apply:

- **Unit tests** — Individual functions, methods, and classes in isolation
- **Integration tests** — Interactions between components, API contracts, database queries
- **End-to-end tests** — Complete user workflows through the full stack
- **Accessibility tests** — WCAG compliance, screen reader compatibility, keyboard navigation
- **Performance tests** — Response times, load handling, resource usage

### 3. Define Coverage Targets

- Set coverage goals per test type (e.g., 80% unit, critical path e2e)
- Identify must-cover areas (auth, payments, data mutations)
- Identify areas where testing provides low value (generated code, trivial getters)

### 4. Identify Test Data Requirements

- Define what test data is needed (fixtures, factories, seeds)
- Determine if production-like data is required
- Note any data privacy or anonymization needs
- Specify mock/stub requirements for external services

### 5. Specify Test Environments

- Local development environment requirements
- CI/CD pipeline integration
- Staging or pre-production environment needs
- Browser/device matrix for UI testing

## Cortex Integration

- Retrieve existing test learnings: query for domain `TEST` memories
- After producing the strategy, extract key decisions as memories (domain: `TEST`, type: `procedural`)
- Reference the `test-plan.yaml` template for structured output

## Output Format

```markdown
## Test Strategy: {feature/project}

### Scope
{What is being tested and why}

### Test Types

| Type | Scope | Coverage Target | Priority |
|------|-------|----------------|----------|
| Unit | {areas} | {target} | {P0-P3} |
| Integration | {areas} | {target} | {P0-P3} |
| E2E | {workflows} | {target} | {P0-P3} |
| Accessibility | {areas} | {target} | {P0-P3} |
| Performance | {areas} | {target} | {P0-P3} |

### Test Data Requirements
- {data need} — {approach (fixture/factory/mock)}

### Test Environments
- {environment} — {purpose}

### Risks and Gaps
1. {risk} — {mitigation}

### Recommendations
{Key decisions and next steps}
```
