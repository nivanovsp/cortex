# Cortex v1.1.0 - Semi-Auto Session Protocol

> Solution Design Document

**Version:** 1.1.0
**Status:** Design
**Created:** 2026-01-26
**Author:** Agent + Human collaboration

---

## Executive Summary

Cortex v1.1.0 introduces the **Semi-Auto Session Protocol** — a user-friendly workflow that eliminates manual script invocation while maintaining human control over learning extraction. The protocol enables natural language interaction with Cortex's retrieval capabilities, making the system accessible to non-technical users.

---

## Problem Statement

### Current State (v1.0.0)

Users must manually invoke PowerShell scripts at specific points:

```powershell
# Session start
.\scripts\cortex-status.ps1
.\scripts\cortex-assemble.ps1 -Task "..."

# During work
.\scripts\cortex-retrieve.ps1 -Query "..."

# Session end
.\scripts\cortex-extract.ps1 -Text "..."
```

### Issues

1. **Technical barrier**: Non-technical users won't know or remember script commands
2. **Friction**: Manual invocation interrupts workflow
3. **Underutilization**: Capabilities go unused if users don't know how to trigger them
4. **Context bloat risk**: Previous solutions (Neocortex) loaded 35%+ context before work began

---

## Solution: Semi-Auto Session Protocol

### Design Principles

1. **Zero pre-loaded content**: Only metadata at session start (~50 tokens)
2. **Retrieval-based context**: Content enters through semantic search only
3. **Natural language triggers**: Users speak naturally, agent handles mechanics
4. **Human control preserved**: User triggers session end and approves learnings

### Protocol Phases

#### Phase 1: Session Start (Automatic)

**Trigger**: Agent awakens / conversation begins

**Agent Action**:
```
Run: cortex-status.ps1
Result: Metadata only (chunk count, memory count, domains, index status)
Context cost: ~50 tokens
```

**User Experience**: Agent greets and reports Cortex availability. No content loaded yet.

#### Phase 2: Task Identification (Automatic)

**Trigger**: User specifies what to work on

**Detection Patterns**:
- "Let's work on {X}"
- "I need to implement {X}"
- "Help me with {X}"
- "Today we're doing {X}"
- Any clear task statement

**Agent Action**:
```
Run: cortex-assemble.ps1 -Task "{detected task}"
Result: Context frame with relevant chunks + memories
Context cost: ~2,000-3,000 tokens (budget-controlled)
```

**User Experience**: Agent seamlessly has relevant context. No script mentioned.

#### Phase 3: On-Demand Retrieval (Natural Language)

**Trigger**: User asks for more information

**Detection Patterns**:
| User Says | Agent Understands |
|-----------|-------------------|
| "Get more details about {X}" | Retrieval request |
| "What do we know about {X}" | Retrieval request |
| "I need context on {X}" | Retrieval request |
| "Tell me about {X}" | Retrieval request |
| "Remind me how {X} works" | Retrieval request |
| "What did we learn about {X}" | Retrieval request |
| "cortex: {X}" | Explicit retrieval (power users) |

**Agent Action**:
```
Run: cortex-retrieve.ps1 -Query "{X}"
Result: Top relevant chunks
Context cost: ~1,000-1,500 tokens per retrieval
```

**User Experience**: Asked a question, received relevant information. Transparent.

#### Phase 4: Session End (User-Triggered)

**Trigger**: User explicitly requests

**Detection Patterns**:
- "Update learning"
- "Save learnings"
- "End session"
- "Wrap up and save"
- "Extract what we learned"

**Agent Action**:
```
1. Identify key learnings from session
2. Run: cortex-extract.ps1 -Text "{learnings}"
3. Present proposed memories with confidence levels
4. User approves selections
5. Run: cortex-index.ps1 (if memories saved)
```

**User Experience**: Natural session closure with learning capture.

---

## Context Budget Analysis

### Comparison: v1.0.0 Manual vs v1.1.0 Semi-Auto

| Phase | v1.0.0 (if user forgets) | v1.1.0 Semi-Auto |
|-------|--------------------------|------------------|
| Session start | 0 tokens (nothing loaded) | ~50 tokens (metadata) |
| Task identified | 0 tokens (user forgot) | ~2,500 tokens (auto) |
| During work | 0 tokens (user forgot) | ~1,500 tokens (on-demand) |
| **Total before work** | 0 (no context!) | ~2,550 tokens (~1.3%) |

### Comparison: Neocortex (old) vs Cortex v1.1.0

| Metric | Neocortex | Cortex v1.1.0 |
|--------|-----------|---------------|
| Start context | ~35% (70k tokens) | ~0.025% (50 tokens) |
| Task context | +more | ~1.25% (2,500 tokens) |
| Total before work | 35%+ | **~1.3%** |

### Token Budget Breakdown

Based on 200k context window:

| Phase | Tokens | % of Context |
|-------|--------|--------------|
| Status metadata | 50 | 0.025% |
| Task context frame | 2,500 | 1.25% |
| On-demand retrieval (x2) | 3,000 | 1.5% |
| **Max typical session** | 5,550 | **2.8%** |

Leaves **97%+ context** for actual work.

---

## Implementation Scope

### Files to Modify

| File | Changes |
|------|---------|
| `CLAUDE.md` (project) | Add Session Protocol section |
| `~/.claude/CLAUDE.md` (global) | Update Cortex section with protocol |
| `docs/architecture.md` | Add session flow diagram |
| `docs/cortex-spec.md` | Add natural language triggers spec |
| `docs/decisions.md` | Add ADR for Semi-Auto Protocol |
| `docs/user-guide.md` | Rewrite for natural language usage |

### No Code Changes Required

The v1.1.0 release is **documentation/configuration only**. The PowerShell scripts and Python core remain unchanged. The agent learns *when* to call existing capabilities through instructions.

---

## Natural Language Trigger Specification

### Task Identification Triggers

```regex
# Patterns that indicate task start
(?:let's|let us|we need to|i need to|help me|going to|want to|working on|work on|implement|build|create|fix|debug|update|modify)\s+(.+)
```

### Retrieval Triggers

```regex
# Patterns that indicate retrieval request
(?:get|need|want|give me|show me)\s+(?:more\s+)?(?:details?|info|information|context)\s+(?:about|on|for)\s+(.+)

(?:what do we know about|what did we learn about|remind me (?:about|how)|tell me about)\s+(.+)

(?:cortex:)\s*(.+)  # Explicit trigger
```

### Session End Triggers

```regex
# Patterns that indicate session end
(?:update|save|extract|capture)\s+(?:the\s+)?learn(?:ing|ings)

(?:end|wrap up|close|finish)\s+(?:the\s+)?session

(?:wrap up and save|save what we learned)
```

---

## User Experience Examples

### Example 1: Natural Flow

```
User: "Hi, let's work on the password reset feature"

Agent: [Internally runs cortex-assemble -Task "password reset feature"]
Agent: "I've loaded context about authentication and password flows.
        I see we have 3 related chunks and 1 memory about token handling.
        What aspect should we start with?"

User: "What do we know about email templates?"

Agent: [Internally runs cortex-retrieve -Query "email templates"]
Agent: "Based on the codebase, email templates are stored in..."

[... work proceeds ...]

User: "Great work. Update learning and wrap up."

Agent: [Internally runs cortex-extract]
Agent: "I found 4 potential learnings from this session:
        1. [H] Password reset tokens expire in 24h (verified fix)
        2. [M] Email service requires SMTP auth
        ...
        Which should I save?"
```

### Example 2: Power User

```
User: "cortex: authentication middleware error handling"

Agent: [Runs cortex-retrieve -Query "authentication middleware error handling"]
Agent: "Here's what Cortex has on auth middleware errors..."
```

---

## Testing Plan

### Test Cases

1. **Session start**: Verify only metadata loaded (~50 tokens)
2. **Task detection**: Verify various phrasings trigger assembly
3. **Retrieval triggers**: Verify natural language patterns work
4. **Explicit trigger**: Verify "cortex: X" works
5. **Session end**: Verify learning extraction triggers
6. **Context budget**: Verify total context stays under 5% for typical session

### Acceptance Criteria

- [ ] Agent loads only status metadata at start
- [ ] Task identification triggers context assembly automatically
- [ ] At least 6 natural language retrieval patterns work
- [ ] "cortex:" explicit trigger works
- [ ] "Update learning" triggers extraction flow
- [ ] Total context consumption < 5% for typical session

---

## Rollout Plan

1. **Design** (this document) — Define the solution
2. **Specification** — Update technical docs
3. **Implementation** — Update CLAUDE.md files
4. **Testing** — Verify all triggers work
5. **Documentation** — Update user-facing docs
6. **Release** — Push to GitHub as v1.1.0

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2026-01-26 | Semi-Auto Session Protocol |
| 1.0.0 | 2026-01-26 | Initial release |

---

## Appendix: Full Trigger Reference

### Task Triggers (Automatic Assembly)

| Phrase Pattern | Example |
|----------------|---------|
| "Let's work on {X}" | "Let's work on the login page" |
| "I need to {X}" | "I need to fix the API endpoint" |
| "Help me with {X}" | "Help me with database migrations" |
| "Working on {X}" | "Working on user authentication" |
| "Going to {X}" | "Going to implement dark mode" |
| "Want to {X}" | "Want to refactor the form validation" |

### Retrieval Triggers (On-Demand)

| Phrase Pattern | Example |
|----------------|---------|
| "Get more details about {X}" | "Get more details about caching" |
| "What do we know about {X}" | "What do we know about rate limiting" |
| "I need context on {X}" | "I need context on the auth flow" |
| "Tell me about {X}" | "Tell me about error handling" |
| "Remind me how {X} works" | "Remind me how sessions work" |
| "What did we learn about {X}" | "What did we learn about tokens" |
| "cortex: {X}" | "cortex: JWT validation" |

### Session End Triggers

| Phrase Pattern | Example |
|----------------|---------|
| "Update learning" | "Update learning" |
| "Save learnings" | "Save learnings from today" |
| "End session" | "Let's end session" |
| "Wrap up and save" | "Wrap up and save what we learned" |
| "Extract what we learned" | "Extract what we learned today" |
