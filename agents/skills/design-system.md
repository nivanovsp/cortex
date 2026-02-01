# Design System Skill

Define or extend a component design system. This skill does not activate a persistent mode — it runs once and produces output.

## When to Use

- When starting a new project that needs a consistent component library
- When auditing existing components for consistency gaps
- When adding new components that must integrate with existing patterns
- When documenting design tokens and usage guidelines

## Procedure

### 1. Inventory Existing Components

- List all current components in the codebase or design library
- Note their variants, states, and usage patterns
- Identify inconsistencies (different button styles, inconsistent spacing)

### 2. Identify Gaps

- Compare existing components against the needs of current and planned features
- Note missing components, missing variants, or missing states
- Identify components that are duplicated or overlap in purpose

### 3. Define Components

For each component (new or updated), define:

#### Purpose
- What the component is for
- When to use it (and when not to)

#### Variants
- Visual or behavioral variations (e.g., primary, secondary, ghost buttons)
- When to use each variant

#### States
- Default, hover, active, focus, disabled, loading, error, success
- Visual treatment for each state

#### Props / Inputs
- Configurable properties (size, color, label, icon, etc.)
- Required vs. optional
- Default values

#### Accessibility Requirements
- ARIA roles and properties
- Keyboard interaction pattern
- Screen reader announcements
- Focus management behavior

#### Usage Guidelines
- Do and don't examples
- Composition rules (what components can contain or be placed within)
- Spacing and alignment rules

### 4. Define Design Tokens

- **Colors** — Primary, secondary, neutral, semantic (success, warning, error, info)
- **Spacing** — Scale (4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px)
- **Typography** — Font families, sizes, weights, line heights
- **Borders** — Radius, width, style
- **Shadows** — Elevation levels
- **Breakpoints** — Responsive thresholds

## Cortex Integration

- Retrieve existing design patterns from Cortex (domain: `UI`)
- Query for accessibility requirements and past findings
- Reference the `design-system.yaml` template for structured output
- After producing the specification, extract design decisions as memories (domain: `UI`, type: `factual`)

## Output Format

```markdown
## Design System: {project/scope}

### Design Tokens

#### Colors
| Token | Value | Usage |
|-------|-------|-------|
| {name} | {value} | {when to use} |

#### Spacing
| Token | Value |
|-------|-------|
| {name} | {value} |

#### Typography
| Token | Font | Size | Weight | Line Height |
|-------|------|------|--------|-------------|
| {name} | {family} | {size} | {weight} | {height} |

### Components

#### {Component Name}
- **Purpose:** {what it does}
- **Variants:** {list}
- **States:** {list}
- **Props:**
  | Prop | Type | Required | Default | Description |
  |------|------|----------|---------|-------------|
  | {name} | {type} | {yes/no} | {value} | {description} |
- **Accessibility:** {ARIA roles, keyboard pattern, announcements}
- **Usage:** {guidelines, do/don't}

### Component Inventory
| Component | Status | Variants | Gaps |
|-----------|--------|----------|------|
| {name} | Existing/New/Updated | {count} | {missing items} |
```
