# Cortex - Global CLAUDE.md Addition

> **Installation:** Add this section to your global `~/.claude/CLAUDE.md` file.
>
> This enables Claude Code to understand and use Cortex across all your projects.

---

## Cortex Context Management (v1.2.0)

**Semantic Retrieval System** - for projects using Cortex:

Cortex provides LLM-native context management through semantic search and position-optimized assembly. **Version 1.2.0** adds cross-platform Python CLI, stale chunk detection, and memory retrieval tracking.

### When to Use

| System | Best For |
|--------|----------|
| **Cortex** | Semantic retrieval, session learnings, context frames |
| **Neocortex/MLDA** | Knowledge graphs, document relationships, topic learning |
| **Both** | Large projects benefiting from both approaches |

### Semi-Auto Session Protocol

**Users interact through natural language. You handle commands automatically.**

#### On Session Start (Automatic)

When conversation begins in a Cortex-enabled project:
1. Run `python -m cli status --json` silently
2. Note metadata internally (chunk count, memory count, domains, stale chunks)
3. **DO NOT** load content files — wait for task identification
4. Greet user, mention Cortex is available if relevant
5. If stale chunks detected, mention briefly (user can refresh if needed)

**Context cost:** ~50 tokens (metadata only)

#### On Task Identification (Automatic)

Detect when user specifies a task:
- "Let's work on {X}"
- "Help me with {X}"
- "I need to implement {X}"
- "Working on {X}"
- "Fix/debug/update {X}"

**Action:**
1. Extract task from their statement
2. Run `python -m cli assemble --task "{task}"`
3. Use context frame to inform your work
4. **DO NOT** mention the command — just have the context

**Context cost:** ~2,500 tokens

#### On Retrieval Request (Natural Language)

Detect when user asks for information:
- "Get more details about {X}"
- "What do we know about {X}"
- "I need context on {X}"
- "Tell me about {X}"
- "Remind me how {X} works"
- "cortex: {X}" (explicit trigger)

**Action:**
1. Extract topic from their question
2. Run `python -m cli retrieve --query "{topic}"`
3. Present information naturally
4. **DO NOT** mention the command

**Context cost:** ~1,500 tokens per retrieval

#### On Session End (User-Triggered)

Detect when user requests learning extraction:
- "Update learning"
- "Save learnings"
- "End session"
- "Wrap up and save"

**Action:**
1. Identify key learnings from session
2. Run `python -m cli extract --text "{learnings}"`
3. Present proposed memories with confidence levels
4. User approves selections
5. Run `python -m cli index` to rebuild index

### Stale Chunk Detection (v1.2.0)

Cortex tracks source file changes. Status shows stale chunks when source files are modified.

**Workflow:**
1. Status reports stale chunks: `python -m cli status`
2. Refresh stale chunks: `python -m cli chunk --path <file> --refresh`
3. Rebuild index: `python -m cli index`

### Context Budget

| Phase | Tokens | % of 200k |
|-------|--------|-----------|
| Session start (metadata) | ~50 | 0.025% |
| Task assembly | ~2,500 | 1.25% |
| On-demand retrieval (×2) | ~3,000 | 1.5% |
| **Typical session total** | **~5,550** | **~2.8%** |

**97%+ of context remains for actual work.**

### Important Rules

1. **Never pre-load content files** — use retrieval only
2. **Commands are invisible to users** — natural language interaction
3. **Session end requires user trigger** — never auto-extract
4. **Explicit trigger always works** — "cortex: {query}"
5. **Cross-platform** — Python CLI works on Windows, Mac, Linux

### Memory Domains

| Domain | Scope |
|--------|-------|
| `AUTH` | Authentication, sessions, tokens |
| `UI` | Components, forms, styling |
| `API` | Endpoints, requests, responses |
| `DB` | Database, queries, migrations |
| `TEST` | Testing, fixtures, mocks |
| `DEV` | Build, deploy, tooling |
| `GENERAL` | Everything else |

### Memory Types

| Type | Use For |
|------|---------|
| `factual` | Stable knowledge ("API uses REST") |
| `experiential` | Lessons learned ("X requires Y") |
| `procedural` | How-to ("Always do X before Y") |

### Integration with Beads

When using both Cortex and Beads:
1. `bd ready` to see tasks
2. User selects task → run `python -m cli assemble` automatically
3. Work on task
4. User says "update learning" → run extraction
5. `bd close` when complete

### Key Principles

- **Position matters**: Critical info at start/end (LLM attention is U-shaped)
- **Chunk, don't load**: Retrieve only relevant ~500 token chunks
- **Natural language first**: Users don't need to know about commands
- **Capture learnings**: Extract memories when user triggers session end
- **Track freshness**: Stale detection ensures context is current

---
