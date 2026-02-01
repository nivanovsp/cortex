# User Flow Skill

Map complete user interaction sequences from start to finish. This skill does not activate a persistent mode — it runs once and produces output.

## When to Use

- When designing a new feature or workflow
- When documenting how a user accomplishes a goal through the system
- When identifying gaps or friction in an existing interaction sequence
- When communicating expected behavior to developers

## Procedure

### 1. Define Actor and Goal

- Identify who the user is (role, permissions, context)
- Define the goal they are trying to achieve
- Note the entry point (how they arrive at the flow)
- Note the success condition (how they know they are done)

### 2. Map Step-by-Step Interaction

For each step in the flow:
- **User action** — What the user does (clicks, types, selects, navigates)
- **System response** — What the system does in response (displays, validates, saves, navigates)
- **Next step** — Where the flow goes from here

Map the complete happy path first, from entry to success.

### 3. Map Error Paths

At each step where something can go wrong:
- What error can occur (validation failure, server error, permission denied, timeout)
- What the system shows the user
- How the user recovers (retry, correct input, navigate back, contact support)
- Whether the error is blocking or non-blocking

### 4. Identify Edge Cases

- What happens if the user refreshes mid-flow
- What happens if the user navigates away and returns
- What happens with concurrent actions (another user modifies the same data)
- What happens with slow or lost network connections
- What happens if required data is missing or stale

### 5. Note Decision Points

- Steps where the flow branches based on user choice or system state
- Conditions that determine which branch is taken
- Whether branches merge back or lead to different outcomes

## Cortex Integration

- Retrieve existing user flows from Cortex (domain: `UI` or `GENERAL`)
- Query for related requirements or acceptance criteria
- Reference the `user-flow.yaml` template for structured output
- After producing the flow, extract patterns and edge cases as memories (domain: `UI`, type: `procedural`)

## Output Format

```markdown
## User Flow: {flow name}

### Actor
{Who the user is and their context}

### Goal
{What they are trying to accomplish}

### Entry Point
{How they arrive at this flow}

### Success Condition
{How they know they are done}

### Happy Path

| Step | User Action | System Response | Next |
|------|-------------|-----------------|------|
| 1 | {action} | {response} | Step 2 |
| 2 | {action} | {response} | Step 3 |
| ... | ... | ... | ... |
| N | {action} | {success state} | Done |

### Error Paths

| At Step | Error | System Response | Recovery |
|---------|-------|-----------------|----------|
| {step} | {what goes wrong} | {what user sees} | {how to recover} |

### Decision Points

| At Step | Condition | Branch A | Branch B |
|---------|-----------|----------|----------|
| {step} | {condition} | {outcome} | {outcome} |

### Edge Cases
1. {scenario} — {expected behavior}

### Flow Diagram
```
{Text-based flow diagram}
```
```
