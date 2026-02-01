# NFR Assessment Skill

Assess non-functional requirements with specific, measurable targets. This skill does not activate a persistent mode — it runs once and produces output.

## When to Use

- When starting a new system or feature that needs quality attribute targets
- When existing NFRs are vague or missing measurable criteria
- When preparing for load testing or security auditing
- When evaluating whether a system meets its quality goals

## Procedure

### 1. Performance

Evaluate and set targets for:
- **Throughput** — requests per second, messages per second
- **Latency** — p50, p95, p99 response times
- **Concurrency** — simultaneous users/connections supported
- **Resource usage** — CPU, memory, disk, network under expected load

### 2. Security

Evaluate requirements for:
- **Authentication** — method, token lifetime, multi-factor
- **Authorization** — model (RBAC, ABAC), granularity
- **Encryption** — at rest, in transit, key management
- **Data protection** — PII handling, retention policies, anonymization
- **Compliance** — relevant standards (SOC2, GDPR, HIPAA, etc.)

### 3. Scalability

Evaluate approach for:
- **Scaling strategy** — horizontal vs. vertical, auto-scaling triggers
- **Bottleneck identification** — database, compute, network, external services
- **Data growth** — expected growth rate, partitioning strategy
- **Geographic distribution** — regions, CDN, data locality

### 4. Maintainability

Evaluate requirements for:
- **Complexity** — cyclomatic complexity targets, module coupling
- **Testability** — coverage targets, test pyramid balance
- **Deployment** — deployment frequency target, rollback capability
- **Observability** — logging, metrics, tracing, alerting
- **Documentation** — API docs, runbooks, architecture diagrams

## Cortex Integration

- Retrieve existing NFR decisions and system constraints before starting
- After completion, store NFR targets as `factual` memories in the relevant domain
- Flag any conflicts between new targets and existing architectural decisions

## Output Format

```markdown
## NFR Assessment: {system/feature name}

### Performance
| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| Throughput | {X} req/s | {how to measure} |
| Latency (p50) | {X} ms | {how to measure} |
| Latency (p95) | {X} ms | {how to measure} |
| Latency (p99) | {X} ms | {how to measure} |
| Concurrency | {X} simultaneous | {how to measure} |

### Security
| Requirement | Target | Status |
|-------------|--------|--------|
| {requirement} | {specific target} | Met/Gap/Unknown |

### Scalability
| Aspect | Current | Target | Approach |
|--------|---------|--------|----------|
| {aspect} | {current state} | {target} | {strategy} |

### Maintainability
| Metric | Target | Current |
|--------|--------|---------|
| Test coverage | {X}% | {Y}% |
| Deployment frequency | {target} | {current} |
| {other metric} | {target} | {current} |

### Risks and Gaps
| Gap | Impact | Recommendation |
|-----|--------|---------------|
| {gap} | {impact} | {recommendation} |

### Priority Order
1. {highest priority NFR and why}
2. {next priority}
3. {next priority}
```
