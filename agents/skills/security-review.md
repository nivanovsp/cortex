# Security Review Skill

Review system security with threat modeling and prioritized mitigations. This skill does not activate a persistent mode — it runs once and produces output.

## When to Use

- When designing a new system or feature that handles sensitive data
- When preparing for a security audit
- When a security incident prompts a review of existing systems
- When adding authentication, authorization, or data protection features

## Procedure

### 1. Identify Assets and Trust Boundaries

- List assets worth protecting (data, credentials, keys, user sessions)
- Map trust boundaries (client/server, service/service, internal/external)
- Identify data flows that cross trust boundaries

### 2. Model Threats

Use STRIDE or a similar framework:
- **Spoofing** — can an attacker impersonate a user or service?
- **Tampering** — can data be modified in transit or at rest?
- **Repudiation** — can actions be performed without audit trail?
- **Information Disclosure** — can sensitive data leak?
- **Denial of Service** — can the system be made unavailable?
- **Elevation of Privilege** — can an attacker gain unauthorized access?

### 3. Identify Vulnerabilities

- Review authentication and session management
- Check authorization and access control
- Inspect input validation and output encoding
- Examine secrets management and key storage
- Assess dependency vulnerabilities
- Check logging and monitoring for security events

### 4. Assess Risk

For each identified threat/vulnerability:
- **Likelihood** — how probable is exploitation? (Low/Medium/High)
- **Impact** — what is the damage if exploited? (Low/Medium/High)
- **Risk** — Likelihood x Impact

### 5. Recommend Mitigations

- Prioritize mitigations by risk level
- For each mitigation, describe the specific action to take
- Note any mitigations that conflict with other requirements
- Identify quick wins vs. longer-term improvements

## Cortex Integration

- Retrieve existing security decisions and known vulnerabilities before starting
- After completion, store critical findings as `experiential` memories (domain: `AUTH` or relevant domain)
- Flag any findings that contradict existing security assumptions

## Output Format

```markdown
## Security Review: {system/feature name}

### Assets
| Asset | Sensitivity | Location |
|-------|------------|----------|
| {asset} | {Critical/High/Medium/Low} | {where it lives} |

### Trust Boundaries
{Description of trust boundaries and data flows crossing them}

### Threat Model
| ID | Category | Threat | Asset | Likelihood | Impact | Risk |
|----|----------|--------|-------|-----------|--------|------|
| T1 | {STRIDE category} | {threat description} | {asset} | {L/M/H} | {L/M/H} | {L/M/H} |

### Vulnerabilities Found
| ID | Vulnerability | Related Threat | Severity |
|----|--------------|----------------|----------|
| V1 | {description} | T{N} | {Critical/High/Medium/Low} |

### Mitigations (Priority Order)
| Priority | Vulnerability | Mitigation | Effort |
|----------|--------------|------------|--------|
| 1 | V{N} | {specific action} | {Low/Med/High} |

### Summary
- **Critical issues:** {count}
- **High issues:** {count}
- **Medium issues:** {count}
- **Low issues:** {count}

### Recommendations
{Overall security posture assessment and next steps}
```
