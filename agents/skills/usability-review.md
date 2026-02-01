# Usability Review Skill

Heuristic evaluation of interface usability based on Nielsen's 10 usability heuristics. This skill does not activate a persistent mode — it runs once and produces output.

## When to Use

- When evaluating an existing interface for usability issues
- Before a major release to catch friction points
- When users report confusion or difficulty with a feature
- When comparing design alternatives

## Procedure

Evaluate the interface against each of Nielsen's 10 usability heuristics. For each heuristic, identify specific issues and recommend improvements.

### 1. Visibility of System Status

- Does the system keep users informed about what is happening?
- Are there loading indicators, progress bars, confirmation messages?
- Can the user tell what state the system is in at any time?

### 2. Match Between System and Real World

- Does the system use language familiar to the user?
- Are concepts, terms, and icons intuitive?
- Does information appear in a natural and logical order?

### 3. User Control and Freedom

- Can users undo and redo actions?
- Are there clear exits from unwanted states (cancel, back, close)?
- Can users navigate freely without being trapped?

### 4. Consistency and Standards

- Are similar actions and elements consistent throughout?
- Does the interface follow platform conventions?
- Are the same words and icons used for the same concepts?

### 5. Error Prevention

- Does the system prevent errors before they happen?
- Are dangerous actions confirmed before execution?
- Are constraints enforced (disabled buttons, input masks)?

### 6. Recognition Rather Than Recall

- Are options and actions visible rather than requiring memory?
- Is context preserved when navigating between views?
- Are recent and frequent items easily accessible?

### 7. Flexibility and Efficiency of Use

- Are there shortcuts for experienced users?
- Can the interface be customized or adapted?
- Are common tasks streamlined?

### 8. Aesthetic and Minimalist Design

- Does every element serve a purpose?
- Is visual noise minimized?
- Is the most important content given visual priority?

### 9. Help Users Recognize, Diagnose, and Recover from Errors

- Are error messages written in plain language?
- Do error messages identify the problem specifically?
- Do error messages suggest a solution?

### 10. Help and Documentation

- Is help available when needed?
- Is documentation easy to search and task-oriented?
- Are instructions concise and contextual?

### Identify Pain Points

After the heuristic evaluation:
- List specific friction points observed
- Note where users are likely to get confused, stuck, or make mistakes
- Prioritize by impact (how many users affected, how severely)

### Recommend Improvements

For each finding:
- Describe the specific fix
- Classify severity (critical, major, minor, cosmetic)
- Note which heuristic it addresses

## Cortex Integration

- Retrieve prior usability findings from Cortex (domain: `UI`, type: `experiential`)
- Query for user feedback or reported issues if stored
- After review, extract findings as memories (domain: `UI`, type: `experiential`)

## Output Format

```markdown
## Usability Review: {interface/feature}

### Summary
- **Scope:** {what was evaluated}
- **Findings:** {total count}
- **Critical:** {count} | **Major:** {count} | **Minor:** {count} | **Cosmetic:** {count}

### Heuristic Evaluation

| # | Heuristic | Rating | Findings |
|---|-----------|--------|----------|
| 1 | Visibility of System Status | Good/Fair/Poor | {count} |
| 2 | Match Between System and Real World | Good/Fair/Poor | {count} |
| 3 | User Control and Freedom | Good/Fair/Poor | {count} |
| 4 | Consistency and Standards | Good/Fair/Poor | {count} |
| 5 | Error Prevention | Good/Fair/Poor | {count} |
| 6 | Recognition Rather Than Recall | Good/Fair/Poor | {count} |
| 7 | Flexibility and Efficiency of Use | Good/Fair/Poor | {count} |
| 8 | Aesthetic and Minimalist Design | Good/Fair/Poor | {count} |
| 9 | Error Recognition and Recovery | Good/Fair/Poor | {count} |
| 10 | Help and Documentation | Good/Fair/Poor | {count} |

### Detailed Findings

#### H{N}: {Heuristic Name}
| # | Finding | Severity | Location | Recommendation |
|---|---------|----------|----------|----------------|
| 1 | {issue observed} | {severity} | {where} | {specific fix} |

### Prioritized Recommendations
1. **Critical:** {issue} — {fix}
2. **Major:** {issue} — {fix}
3. **Minor:** {issue} — {fix}
4. **Cosmetic:** {issue} — {fix}
```
