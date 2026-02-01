# API Design Skill

Design API endpoints with complete request/response specifications. This skill does not activate a persistent mode — it runs once and produces output.

## When to Use

- When designing new API endpoints for a feature
- When restructuring or versioning an existing API
- When documenting an API that lacks formal specification
- When evaluating API consistency across a service

## Procedure

### 1. Define Resources and Relationships

- Identify the core resources (nouns) the API exposes
- Map relationships between resources (one-to-many, many-to-many)
- Determine resource hierarchy and nesting strategy

### 2. Design Endpoints

For each resource, define:
- **HTTP method and path** (REST) or **query/mutation** (GraphQL)
- **Purpose** — what the endpoint does
- **Path parameters, query parameters, and filters**
- **Pagination strategy** (if applicable)

### 3. Specify Request/Response Schemas

For each endpoint:
- **Request body** — fields, types, required/optional, validation rules
- **Response body** — fields, types, envelope structure
- **Example request and response**

### 4. Define Error Codes and Handling

- Map error scenarios to HTTP status codes
- Define error response structure (code, message, details)
- Specify validation error format
- Document domain-specific error codes

### 5. Specify Authentication and Authorization

- Authentication method (API key, JWT, OAuth2, etc.)
- Authorization model (roles, scopes, resource ownership)
- Per-endpoint authorization requirements

### 6. Document Rate Limiting (if applicable)

- Rate limit strategy (per-user, per-key, per-endpoint)
- Rate limit headers in responses
- Behavior when limit exceeded

## Cortex Integration

- Retrieve existing API patterns and conventions before starting
- After completion, store the API specification as a `factual` memory (domain: `API`)
- Reference the `api-spec.yaml` template for structured output

## Output Format

```markdown
## API Design: {API/feature name}

### Resources
| Resource | Description | Relationships |
|----------|-------------|---------------|
| {name} | {description} | {relationships} |

### Endpoints

#### {METHOD} {path}
- **Purpose:** {description}
- **Auth:** {required role/scope}
- **Request:**
  ```json
  {request body example}
  ```
- **Response:** ({status code})
  ```json
  {response body example}
  ```
- **Errors:**
  | Code | Condition |
  |------|-----------|
  | {status} | {when it occurs} |

{repeat for each endpoint}

### Error Format
```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Human-readable message",
    "details": {}
  }
}
```

### Authentication
{Auth method and flow}

### Authorization
| Endpoint | Required Role/Scope |
|----------|-------------------|
| {endpoint} | {role/scope} |

### Rate Limiting
| Tier | Limit | Window |
|------|-------|--------|
| {tier} | {requests} | {period} |
```
