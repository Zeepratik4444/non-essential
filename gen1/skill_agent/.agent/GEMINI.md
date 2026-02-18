# GEMINI.md — Skill Agent Project Context

This file provides LLM context for the `skill_agent` project inside the `non-essential` repository.

## What This Project Is

`skill_agent` is a **skill-driven CrewAI agent** exposed as a **FastAPI REST API**. The agent dynamically loads structured skill instructions (from `./skills/`) before executing any task — preventing hallucination and ensuring all actions follow defined protocols.

- **Framework**: CrewAI + FastAPI
- **LLM**: `gemini/gemini-2.5-flash` (via LiteLLM)
- **Python**: >= 3.13
- **Package Manager**: `uv`

## How It Works

1. A task description is POSTed to `/api/v1/run`
2. `SkillsCrew` initializes and kicks off the CrewAI crew
3. The `skills_operator` agent calls `SkillsManagerTool` with `list_skills` first
4. It loads the matching `skill.md` via `load_skill`
5. It follows the protocol defined in that skill exactly
6. The result is returned as a structured JSON response

## Project Layout

```

gen1/skill_agent/
├── main.py                  \# FastAPI app — all API endpoints
├── client_test.py           \# CLI test runner hitting the API
├── requirements.txt         \# Minimal deps
├── pyproject.toml           \# uv project config
├── .env                     \# LLM_MODEL, API keys (not committed)
├── .python-version          \# 3.13
├── src/
│   ├── crew.py              \# SkillsCrew class (CrewAI @CrewBase)
│   ├── config/
│   │   ├── agents.yaml      \# skills_operator agent definition
│   │   ├── tasks.yaml       \# execute_task task definition
│   │   └── settings.py      \# Env-based settings (SKILLS_DIR, LLM_MODEL, etc.)
│   └── tools/
│       └── skills_manager_tool.py  \# Core tool: list/load/run skills
├── skills/                  \# Skill modules — each is a directory with skill.md
│   ├── api-development/
│   ├── code-review/
│   ├── customer-support/
│   ├── database-design/
│   ├── document-generation/
│   ├── financial-analysis/
│   ├── frontend-development/
│   ├── hr-recruitment/
│   ├── legal-document-review/
│   └── research_assistant/
└── static/                  \# Web UI (served at /ui)

```

## Key Files to Know

| File | Purpose |
|------|---------|
| `main.py` | FastAPI entrypoint, all routes |
| `src/crew.py` | SkillsCrew — agent + task wiring |
| `src/tools/skills_manager_tool.py` | The only tool the agent uses |
| `src/config/settings.py` | All config loaded from env |
| `src/config/agents.yaml` | Agent role, goal, backstory, protocol |
| `src/config/tasks.yaml` | Task description template |
| `skills/*/skill.md` | Each skill's full instruction set |

## Environment Variables

```env
LLM_MODEL=gemini/gemini-2.5-flash
GEMINI_API_KEY=your_key_here
SCRIPT_TIMEOUT=60
MAX_FILE_PREVIEW_CHARS=5000
LOG_LEVEL=INFO
```


## Running Locally

```bash
cd gen1/skill_agent
uv sync
uvicorn main:app --reload --port 8000
# or
python main.py
```


## API Endpoints

| Method | Path | Description |
| :-- | :-- | :-- |
| GET | `/health` | Health check |
| GET | `/api/v1/skills` | List all available skills |
| POST | `/api/v1/run` | Execute a task |
| POST | `/api/v1/skills` | Create a new skill dynamically |
| GET | `/ui` | Web interface |

### Example Request

```json
POST /api/v1/run
{
  "task_description": "Review this Python function for SQL injection risks: cursor.execute('SELECT * FROM users WHERE id = ' + user_id)",
  "extra_inputs": {}
}