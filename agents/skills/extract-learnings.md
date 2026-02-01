# Extract Learnings Skill

A structured workflow for extracting and saving session learnings to Cortex memory. This skill guides the learning extraction process that normally triggers on session end.

## When to Use

- End of a work session
- After resolving a significant bug
- After making an architectural decision
- When the user says "save learnings" or "update learning"

## Procedure

### Step 1: Identify Learnings

Review the session for:

- **Fixes discovered** — What was broken and what fixed it?
- **Constraints found** — What limitations were discovered?
- **Patterns established** — What approach worked well?
- **Decisions made** — What was decided and why?
- **Gotchas** — What was surprising or counterintuitive?

### Step 2: Classify Each Learning

For each learning, determine:

| Field | Options | Guidance |
|-------|---------|----------|
| **Type** | `factual`, `experiential`, `procedural` | Fact, lesson, or how-to? |
| **Domain** | `AUTH`, `UI`, `API`, `DB`, `TEST`, `DEV`, `GENERAL` | Which area? |
| **Confidence** | `high`, `medium`, `low` | Verified fix = high; inference = medium; uncertain = low |

### Step 3: Present for Approval

Show each proposed memory to the user with:
- The learning text
- Type, domain, and confidence
- Why it's worth remembering

Ask the user which ones to save.

### Step 4: Save Approved Memories

For each approved memory:
```bash
python -m cli memory add --learning "{text}" --domain {DOMAIN} --type {type} --confidence {level}
```

### Step 5: Rebuild Index

After saving all memories:
```bash
python -m cli index
```

## Output Format

```markdown
## Session Learnings

### Proposed Memories

1. **{Learning}**
   - Type: {factual|experiential|procedural}
   - Domain: {domain}
   - Confidence: {high|medium|low}
   - Reason: {why this is worth remembering}

2. ...

### Save which memories? (list numbers or "all")
```

## Tips

- Prefer specific, actionable learnings over vague observations
- "FormField wrapper is required for PasswordInput validation" > "Form validation is tricky"
- One learning per memory — don't combine unrelated facts
- High confidence = you verified it works. Medium = reasonable inference. Low = needs verification.
