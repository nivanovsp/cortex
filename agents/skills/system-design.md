# System Design Skill

Design a system or component with structured trade-off analysis. This skill does not activate a persistent mode — it runs once and produces output.

## When to Use

- When designing a new system, service, or major component
- When restructuring an existing system's architecture
- When evaluating how a new feature fits into the current system
- When the Orchestrator's plan includes a design phase

## Procedure

### 1. Understand Context and Constraints

- Identify the problem being solved and who it serves
- Clarify functional requirements (what the system must do)
- Clarify constraints (budget, timeline, team size, existing tech stack)
- Retrieve existing architecture context from Cortex

### 2. Present Design Options

Present 2-3 design options, each with:
- **Overview** — high-level description of the approach
- **Pros** — advantages and strengths
- **Cons** — disadvantages and limitations
- **Trade-offs** — what you gain vs. what you give up
- **Best suited for** — scenarios where this option excels

### 3. Recommend

- State the recommended option clearly
- Provide rationale tied to the specific context and constraints
- Explain why the alternatives were not chosen

### 4. Define the Design

For the recommended option, define:
- **Component diagram** — major components and their responsibilities
- **Data flow** — how data moves through the system
- **API contracts** — key interfaces between components
- **Data model** — core entities and relationships (if applicable)

### 5. Identify Risks

- List technical risks and their likelihood/impact
- Identify assumptions that could invalidate the design
- Note areas requiring prototyping or further investigation

## Cortex Integration

- Retrieve existing architecture and design decisions before starting
- After completion, store the design decision as a `factual` memory (domain matching the system area)
- Reference the `architecture.yaml` template for structured output

## Output Format

```markdown
## System Design: {system/component name}

### Context
{Problem statement, constraints, and requirements}

### Options

#### Option A: {name}
- **Overview:** {description}
- **Pros:** {list}
- **Cons:** {list}
- **Trade-offs:** {what you gain vs. lose}

#### Option B: {name}
{same structure}

#### Option C: {name} (if applicable)
{same structure}

### Recommendation
**Selected: Option {X} — {name}**

{Rationale tied to context and constraints}

### Design

#### Component Diagram
{Component descriptions and responsibilities}

#### Data Flow
{How data moves through the system}

#### API Contracts
{Key interfaces between components}

#### Data Model
{Core entities and relationships}

### Risks
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| {risk} | Low/Med/High | Low/Med/High | {mitigation} |

### Assumptions
- {assumption that could invalidate this design}

### Open Questions
- {areas requiring further investigation}
```
