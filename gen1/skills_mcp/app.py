"""
app.py — Unified ASGI Entry Point
==================================
Mounts FastMCP (MCP over HTTP/SSE) + FastAPI (REST health + skills API)
into a single Starlette app served by Uvicorn.

Endpoints:
  /mcp          → FastMCP streamable HTTP transport (MCP clients)
  /health       → REST health check
  /api/skills   → REST: list skill names
  /docs         → FastAPI Swagger UI

Transports:
  Stdio  → run `python -m mcp_server` (for Claude Desktop / IDEs)
  HTTP   → run `uvicorn app:app` (for remote / multi-user)

Usage:
  uv run uvicorn app:app --host 0.0.0.0 --port 8000 --reload
"""

import logging
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware as StarletteCORS
from starlette.routing import Mount

# Ensure current dir is in sys.path
sys.path.append(str(Path(__file__).parent))

# --- Core ---
from core.settings import settings
from core.crew import SkillsCrew

# --- MCP (imports tools + resources via __init__.py) ---
import mcp_server  # noqa: F401 — registers all tools + resources
from mcp_server.server import mcp

# --- Logging ---
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)

# --- Validate environment on startup ---
try:
    settings.validate()
except EnvironmentError as e:
    logger.error("Startup validation failed:\n%s", e)
    # Don't exit here, allow partial startup if possible or let the user fix env
    
logger.info(
    "Starting %s v%s | skills_dir=%s | model=%s",
    settings.MCP_SERVER_NAME,
    settings.MCP_SERVER_VERSION,
    settings.SKILLS_DIR,
    settings.LLM_MODEL,
)

# ---------------------------------------------------------------------------
# FastAPI — REST companion API
# ---------------------------------------------------------------------------

api = FastAPI(
    title=settings.MCP_SERVER_NAME,
    version=settings.MCP_SERVER_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/health", tags=["Monitoring"])
def health_check():
    """Server health + metadata."""
    from core.skills_manager import SkillsManager
    manager = SkillsManager()
    return {
        "status": "healthy",
        "server": settings.MCP_SERVER_NAME,
        "version": settings.MCP_SERVER_VERSION,
        "model": settings.LLM_MODEL,
        "skills_count": len(manager.get_skill_names()),
        "skills_dir": str(settings.SKILLS_DIR),
    }


@api.get("/api/skills", tags=["Skills"])
def list_skill_names():
    """Return sorted list of all available skill slugs."""
    from core.skills_manager import SkillsManager
    manager = SkillsManager()
    return {"skills": manager.get_skill_names()}


# --- CrewAI Integration ---
from pydantic import BaseModel, Field
from typing import Dict, Any

class RunRequest(BaseModel):
    task_description: str = Field(..., description="Task for the Skills Operator.")
    extra_inputs: Dict[str, Any] = Field(default_factory=dict, description="Additional context.")
    thread_id: str | None = Field(default=None, description="Thread ID.")

@api.post("/api/v1/run", tags=["Execution"])
async def run_skill_crew(request: RunRequest):
    """Execute the Skill-Driven Operator with a dynamic task."""
    try:
        crew = SkillsCrew()
        result = crew.run(
            task_description=request.task_description,
            **request.extra_inputs
        )
        return {"success": True, "result": result}
    except Exception as e:
        logger.error("Error running Skills Crew: %s", str(e), exc_info=True)
        return {"success": False, "error": str(e)}


# ---------------------------------------------------------------------------
# FastMCP ASGI app  (mounts at /mcp)
# ---------------------------------------------------------------------------

mcp_asgi = mcp.http_app()

# ---------------------------------------------------------------------------
# Root Starlette app — combines FastMCP + FastAPI
# ---------------------------------------------------------------------------

app = Starlette(
    routes=[
        Mount("/mcp", app=mcp_asgi),   # MCP over HTTP
        Mount("/", app=api),            # REST API + Swagger
    ],
    middleware=[
        Middleware(
            StarletteCORS,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ],
    lifespan=mcp_asgi.lifespan,
)

# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower(),
    )
