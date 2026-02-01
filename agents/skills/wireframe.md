# Wireframe Skill

Define interface layout and interaction design for a page or component. This skill does not activate a persistent mode — it runs once and produces output.

## When to Use

- When designing a new page, screen, or component
- When communicating layout intent before implementation
- When exploring layout alternatives for a feature
- When a developer needs a clear specification for building UI

## Procedure

### 1. Identify the User Goal

- Define what the user is trying to accomplish on this page or screen
- Identify the primary action and any secondary actions
- Note the context: where the user comes from and where they go next

### 2. Define Page Layout

- Specify the overall page structure (header, content area, sidebar, footer)
- Place components within the layout grid
- Indicate visual hierarchy — what the user should see first, second, third
- Note content zones and their purpose

### 3. Specify Component Placement

For each component in the layout:
- Name and type (button, form, table, card, modal, etc.)
- Position within the layout
- Relative sizing and spacing
- Content it displays

### 4. Define Interaction States

For each interactive component, specify these states:
- **Default** — Initial appearance
- **Hover** — Mouse over (desktop)
- **Active** — Being clicked or tapped
- **Disabled** — Not currently available
- **Loading** — Waiting for data or action
- **Error** — Something went wrong
- **Empty** — No data to display
- **Success** — Action completed

### 5. Add Behavior Annotations

- Describe what happens on click, submit, or other interactions
- Note any animations or transitions
- Specify validation rules for form inputs
- Document conditional visibility (what shows/hides and when)

### 6. Define Responsive Breakpoints

- **Desktop** (1024px+) — Full layout
- **Tablet** (768px–1023px) — Adapted layout
- **Mobile** (below 768px) — Stacked or simplified layout
- Note which components reflow, collapse, or hide at each breakpoint

## Cortex Integration

- Retrieve existing UI patterns from Cortex (domain: `UI`)
- Query for design system tokens if available
- Reference the `wireframe.yaml` template for structured output
- After producing the wireframe, extract reusable patterns as memories (domain: `UI`, type: `procedural`)

## Output Format

```markdown
## Wireframe: {page/component name}

### User Goal
{What the user is trying to accomplish}

### Layout

```
{ASCII or structured layout diagram}
```

### Components

| Component | Type | Position | Purpose |
|-----------|------|----------|---------|
| {name} | {type} | {location in layout} | {what it does} |

### Interaction States

#### {Component Name}
| State | Appearance | Trigger |
|-------|------------|---------|
| Default | {description} | — |
| Hover | {description} | Mouse over |
| Active | {description} | Click/tap |
| Disabled | {description} | {condition} |
| Loading | {description} | {condition} |
| Error | {description} | {condition} |
| Empty | {description} | {condition} |
| Success | {description} | {condition} |

### Behavior Annotations
1. {component} — {interaction} → {result}

### Responsive Behavior
| Breakpoint | Layout Changes |
|------------|---------------|
| Desktop (1024px+) | {description} |
| Tablet (768–1023px) | {description} |
| Mobile (<768px) | {description} |
```
