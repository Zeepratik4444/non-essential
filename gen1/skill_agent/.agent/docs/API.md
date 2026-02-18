# API Reference

Base URL: `http://localhost:8000`

---

## GET `/health`

Health check endpoint.

**Response**
```json
{
  "status": "healthy",
  "version": "0.2.0"
}
```


---

## GET `/api/v1/skills`

Returns a sorted list of all dynamically discovered skill names.

**Response**

```json
{
  "skills": [
    "api-development",
    "code-review",
    "customer-support",
    "database-design",
    "document-generation",
    "financial-analysis",
    "frontend-development",
    "hr-recruitment",
    "legal-document-review",
    "research_assistant"
  ]
}
```


---

## POST `/api/v1/run`

Execute a task using the skill-driven agent.

**Request Body**

```json
{
  "task_description": "string (required) — what you want the agent to do",
  "extra_inputs": {}
}
```

**Response (success)**

```json
{
  "success": true,
  "result": "Full agent output string",
  "message": "Task completed successfully"
}
```

**Response (failure)**

```json
{
  "success": false,
  "result": "",
  "message": "Error executing task: <reason>"
}
```

**Example**

```bash
curl -X POST http://localhost:8000/api/v1/run \
  -H "Content-Type: application/json" \
  -d '{
    "task_description": "Analyze gross margin for a SaaS with $10M ARR and $2M COGS",
    "extra_inputs": {}
  }'
```


---

## POST `/api/v1/skills`

Dynamically create a new skill without restarting the server.

**Request Body**

```json
{
  "name": "my-skill-name",
  "content": "# Skill markdown content here"
}
```

**Response**

```json
{
  "success": true,
  "message": "✅ Skill 'my-skill-name' created successfully."
}
```


---

## GET `/ui`

Serves the web interface from `./static/index.html`.

---

## Error Codes

| Code | Meaning |
| :-- | :-- |
| 200 | Success |
| 404 | Route or static file not found |
| 500 | Agent execution error |

