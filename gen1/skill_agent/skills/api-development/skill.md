---
name: api-development
description: >
  Design, build, and review REST or GraphQL APIs. Use when user needs
  API endpoints, request/response schemas, authentication flows,
  error handling, rate limiting, or API documentation. Supports
  FastAPI, Express, and Node.js stacks.
triggers:
  - "build an API"
  - "REST endpoint"
  - "API design"
  - "fastapi route"
  - "express endpoint"
  - "api authentication"
  - "api error handling"
  - "openapi schema"
---

# API Development

## When to Use
- Designing REST API structure and endpoints
- Building FastAPI or Express route handlers
- Authentication (JWT, OAuth2, API keys)
- Request validation and response schemas
- Error handling and status codes
- Rate limiting and middleware
- OpenAPI / Swagger documentation

## Protocol
1. Identify the API type (REST, GraphQL) and framework (FastAPI, Express)
2. Identify the specific task (design, implement, review, document)
3. Load references/rest_standards.md for conventions
4. Apply the correct patterns for the framework
5. Return complete, production-ready code

## REST Design Principles (Always Apply)
- Resources are nouns, never verbs: `/users` not `/getUsers`
- HTTP methods carry the action:
  - `GET` → read (idempotent)
  - `POST` → create
  - `PUT` → full replace
  - `PATCH` → partial update
  - `DELETE` → remove
- Status codes must be precise (see references/rest_standards.md)
- Always version: `/api/v1/resource`
- Pagination on all list endpoints: `?page=1&limit=20`
- Consistent error response shape across all endpoints

## Standard Error Response Shape
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable message",
    "details": [{ "field": "email", "issue": "Invalid format" }]
  },
  "request_id": "uuid"
}
```

## Standard Success Response Shape
```json
{
  "success": true,
  "data": {},
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

## FastAPI Endpoint Template
```python
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/resource", tags=["resource"])

class ResourceCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None)

class ResourceResponse(BaseModel):
    id: str
    name: str
    description: str | None
    created_at: datetime

@router.post(
    "/",
    response_model=ResourceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new resource",
)
async def create_resource(
    payload: ResourceCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ResourceResponse:
    """Create a new resource. Requires authentication."""
    try:
        resource = await resource_service.create(db, payload, current_user.id)
        return ResourceResponse.model_validate(resource)
    except DuplicateError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "DUPLICATE_RESOURCE", "message": str(exc)},
        )
```

## Output Format

### API Task: {design | implement | review | document}

**Framework**: {FastAPI | Express | GraphQL}
**Endpoint(s)**: {method} {path}

#### Schema

```python / typescript
{request and response models}
```

#### Implementation

```python / typescript
{complete route handler}
```

#### Example Request / Response

```bash
curl -X POST /api/v1/resource \
  -H "Authorization: Bearer {token}" \
  -d '{"name": "example"}'
```

## Rules
- Never expose internal errors or stack traces in responses
- Always validate input with Pydantic (FastAPI) or Zod (Express/TS)
- Auth check before any business logic — never after
- Database errors must be caught and mapped to HTTP errors
- Log errors server-side with request_id, never in response body
- Rate limit all public endpoints

## References
- REST conventions and status codes: read references/rest_standards.md
- Authentication patterns (JWT/OAuth2): read references/auth_patterns.md
- Rate limiting and middleware: read references/middleware_guide.md
