# Refactor Assessment Skill

Assess whether and how to refactor code with risk analysis and verification strategy. This skill does not activate a persistent mode — it runs once and produces output.

## When to Use

- When code smells are identified but the refactoring cost is unclear
- When deciding between refactoring now vs. later
- Before starting a refactoring effort to plan the approach
- When justifying refactoring work to stakeholders

## Procedure

### 1. Identify the Concern

- What specifically is wrong with the current code?
- Why does it matter? (not just "it's messy" — what concrete problem does it cause?)
- How does it affect development velocity, correctness, or maintainability?
- Provide specific examples from the codebase

### 2. Assess Impact

- What breaks or degrades if we do not refactor?
- How often does this code change? (high churn = higher refactoring value)
- How many developers work in this area?
- Is this blocking other work?

### 3. Plan the Transformation

- Define the target state (what the code should look like after)
- Break the refactoring into incremental steps
- Each step must preserve existing behavior (no behavior changes mixed in)
- Identify the order of operations to minimize risk

### 4. Define Verification

- What tests exist today? Are they sufficient?
- What new tests are needed before refactoring? (test the current behavior first)
- How will you prove nothing broke after each step?
- What manual verification is needed?

### 5. Assess Risk vs. Benefit

- **Benefit:** reduced complexity, fewer bugs, faster development, unblocked work
- **Risk:** regressions, wasted effort if requirements change, merge conflicts
- **Verdict:** Is the refactoring justified given the risk/benefit balance?

## Cortex Integration

- Retrieve history and context about the code area before assessing
- After completion, store the assessment as an `experiential` memory
- If refactoring is approved and completed, update with a `procedural` memory documenting the pattern

## Output Format

```markdown
## Refactor Assessment: {area/module name}

### Current State
{What the code looks like now and what's wrong with it}

### Concern
{Specific problem and why it matters — concrete impact}

### Impact of Inaction
{What happens if we do not refactor}

### Target State
{What the code should look like after refactoring}

### Transformation Plan
| Step | Change | Behavior Impact | Verification |
|------|--------|----------------|--------------|
| 1 | {change} | None (preserves behavior) | {how to verify} |
| 2 | {change} | None (preserves behavior) | {how to verify} |

### Test Requirements
- **Existing tests:** {adequate/insufficient — details}
- **Tests to add before refactoring:** {list}
- **Tests to add after refactoring:** {list}

### Risk vs. Benefit
| Factor | Assessment |
|--------|-----------|
| Benefit | {specific benefits} |
| Risk | {specific risks} |
| Code churn | {High/Medium/Low — how often this code changes} |
| Team impact | {how many developers are affected} |
| Blocking? | {Yes/No — is this blocking other work?} |

### Verdict
**{Refactor now | Refactor later | Do not refactor}**

{Justification for the verdict}
```
