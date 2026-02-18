# REST API Standards

## HTTP Status Codes
| Code | Name                  | When to Use                              |
|------|-----------------------|------------------------------------------|
| 200  | OK                    | Successful GET, PUT, PATCH               |
| 201  | Created               | Successful POST (resource created)       |
| 204  | No Content            | Successful DELETE                        |
| 400  | Bad Request           | Validation failure, malformed request    |
| 401  | Unauthorized          | Missing or invalid authentication        |
| 403  | Forbidden             | Authenticated but lacks permission       |
| 404  | Not Found             | Resource does not exist                  |
| 409  | Conflict              | Duplicate resource, state conflict       |
| 422  | Unprocessable Entity  | Valid format but semantic errors         |
| 429  | Too Many Requests     | Rate limit exceeded                      |
| 500  | Internal Server Error | Unhandled server error                   |
| 503  | Service Unavailable   | Downstream dependency down               |

## URL Conventions
- Lowercase, hyphen-separated: `/user-profiles` not `/userProfiles`
- Plural nouns for collections: `/orders` not `/order`
- Nested for ownership (max 2 levels): `/users/{id}/orders`
- Filter via query params: `/orders?status=pending&page=1`
- Never verbs in URL: `/orders/cancel` ❌ → `PATCH /orders/{id}` ✅

## Pagination Standard
Request:  GET /resources?page=1&limit=20&sort=created_at&order=desc
Response meta:
{
  "page": 1,
  "limit": 20,
  "total": 245,
  "total_pages": 13,
  "has_next": true,
  "has_prev": false
}

## Versioning
- URL versioning preferred: /api/v1/, /api/v2/
- Deprecation header for old versions:
  Deprecation: true
  Sunset: Sat, 01 Jan 2026 00:00:00 GMT
