# Gap Analysis Skill

Compares current state against desired state to identify gaps, assess impact, and recommend actions. This skill does not activate a persistent mode — it runs once and produces output.

## When to Use

- When evaluating what exists vs. what is needed for a project or feature
- When assessing readiness before starting implementation
- When auditing a system or codebase against requirements
- When planning migration or upgrade paths

## Procedure

### 1. Define Desired State

- Clarify the target state with the user
- List specific capabilities, features, or qualities expected
- Reference requirements documents or PRDs if available

### 2. Inventory Current State

- Examine what currently exists
- Document current capabilities, components, and behaviors
- Note the state and quality of existing assets

### 3. Identify Gaps

For each element of the desired state:
- Does it exist in the current state?
- If yes, does it meet the desired specification?
- If partially, what is missing or insufficient?
- If no, it is a complete gap

### 4. Assess Impact

For each gap, assess:
- **Impact**: High / Medium / Low — what happens if this gap is not addressed
- **Effort**: High / Medium / Low — relative effort to close the gap
- **Priority**: Derived from impact and effort

### 5. Recommend Actions

For each gap, recommend one of:
- **Build**: Create from scratch
- **Modify**: Adapt existing assets
- **Acquire**: Obtain from external source
- **Defer**: Acceptable to address later
- **Accept**: Gap is tolerable as-is

## Cortex Integration

- Retrieve requirements: `retrieve --query "requirements {topic}"`
- Retrieve architecture context: `retrieve --query "architecture {topic}"`
- Store the analysis: `memory add --learning "Gap analysis for {topic} - {count} gaps identified" --domain GENERAL --type experiential --confidence medium`

## Output Format

```markdown
## Gap Analysis: {Subject}

### Desired State
{Description of the target state}

### Current State
{Description of what exists today}

### Gaps

| # | Gap | Current | Desired | Impact | Effort | Action |
|---|-----|---------|---------|--------|--------|--------|
| 1 | {gap} | {what exists} | {what's needed} | High | Medium | Build |
| 2 | {gap} | {what exists} | {what's needed} | Medium | Low | Modify |
| 3 | {gap} | Absent | {what's needed} | High | High | Build |
| 4 | {gap} | {what exists} | {what's needed} | Low | Low | Defer |

### Summary
- **Total gaps:** {count}
- **Critical gaps (High impact):** {count}
- **Quick wins (Low effort):** {count}

### Recommended Priority Order
1. {gap} — {rationale}
2. {gap} — {rationale}
3. {gap} — {rationale}

### Notes
- {additional observations}
```
