# Debug Workflow Skill

Structured debugging workflow for systematic root cause analysis. This skill does not activate a persistent mode — it runs once and produces output.

## When to Use

- When a bug needs systematic investigation rather than guesswork
- When a fix attempt has failed and a more structured approach is needed
- When the root cause is unclear and symptoms are misleading
- When documenting a debugging process for team learning

## Procedure

### 1. Reproduce

- Confirm the bug exists and is reproducible
- Document exact steps to reproduce
- Record the actual behavior observed
- Record the expected behavior
- Note the environment (OS, versions, configuration)

### 2. Isolate

- Narrow down the location of the problem
- Use bisection: does the issue occur with half the code path disabled?
- Check recent changes (git log, git bisect) for likely culprits
- Determine the minimal reproduction case

### 3. Hypothesize

- Form a theory about the **root cause** (not the symptom)
- Consider all possible causes, not just the obvious one
- Ask: "Is the error where it appears, or upstream?"
- Ask: "What assumption is being violated?"
- Rank hypotheses by probability

### 4. Verify

- Design a test that distinguishes between hypotheses
- Test the most likely hypothesis first
- If disproven, move to the next hypothesis
- Avoid changing multiple things at once

### 5. Fix

- Apply the minimal correct fix for the root cause
- Do not fix the symptom if the root cause is different
- Ensure the fix does not introduce new issues
- Consider whether similar bugs exist elsewhere

### 6. Confirm

- Verify the original reproduction case no longer fails
- Run related tests to check for regressions
- Verify edge cases related to the fix
- Document what was learned

## Cortex Integration

- Retrieve context about the affected area before starting
- After completion, store the root cause and fix as an `experiential` memory
- If the bug reveals a systemic issue, store as a `procedural` memory

## Output Format

```markdown
## Debug Report: {bug title}

### Symptom
{What was observed}

### Expected Behavior
{What should have happened}

### Reproduction Steps
1. {step}
2. {step}
3. {observed failure}

### Investigation

#### Hypotheses Considered
1. {hypothesis} — {confirmed/disproven and why}
2. {hypothesis} — {confirmed/disproven and why}

#### Root Cause
{Explanation of the actual root cause, not just the symptom}

### Fix Applied
- **File(s):** {files changed}
- **Change:** {what was changed and why}

### Verification
- [ ] Original reproduction case passes
- [ ] Related tests pass
- [ ] Edge cases checked: {list}
- [ ] No regressions detected

### Lessons Learned
- {what this bug teaches about the system}
```
