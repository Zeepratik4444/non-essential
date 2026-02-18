import sys
import logging
import uuid
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# Add src to path so relative imports work
sys.path.append(str(Path(__file__).parent / "src"))

from src.crew import SkillsCrew
from src.tools.skills_manager_tool import SkillsManagerTool

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Skill Agent API",
    description="REST API to trigger Skill-Driven CrewAI Operator for dynamic tasks.",
    version="0.2.0"
)

# --- In-Memory Store ---
# thread_id -> list of {"role": "user"|"assistant", "content": "..."}
CHAT_HISTORY: Dict[str, List[Dict[str, str]]] = {}

# Static Files and UI folder (Fixed pathing)
static_path = Path(__file__).parent / "static"
app.mount("/ui", StaticFiles(directory=str(static_path), html=True), name="static")

@app.get("/")
async def read_index():
    """Serve the web interface."""
    return FileResponse(static_path / "index.html")

# --- Pydantic Schemas ---
class RunRequest(BaseModel):
    task_description: str = Field(
        ..., 
        description="Detailed description of the task for the Skills Operator.",
        example="Build a simple React component for a contact form"
    )
    extra_inputs: Dict[str, Any] = Field(
        default_factory=dict,
        description="Optional additional context or parameters for the crew.",
        example={"context": "Use Tailwind CSS for styling"}
    )
    thread_id: str | None = Field(
        default=None,
        description="Optional thread ID to maintain conversation context.",
        example="123e4567-e89b-12d3-a456-426614174000"
    )

class RunResponse(BaseModel):
    success: bool
    result: str
    thread_id: str | None = None
    message: str | None = None

class SkillCreateRequest(BaseModel):
    name: str = Field(..., example="new-skill")
    content: str = Field(..., example="# New Skill\n\nDescription here...")

# --- Endpoints ---

@app.get("/health", tags=["Monitoring"])
async def health_check():
    """Verify the API is running."""
    return {"status": "healthy", "version": "0.2.0"}

@app.get("/api/v1/skills", tags=["Skills"])
async def get_skills():
    """Returns a list of all dynamically discovered skills."""
    try:
        tool = SkillsManagerTool()
        # Returns raw list of names as per my recent update to the tool
        skills = tool._run(action="get_skill_names")
        return {"skills": sorted(skills)}
    except Exception as e:
        logger.error("Error fetching skills: %s", str(e))
        return {"skills": [], "error": str(e)}

@app.post(
    "/api/v1/run", 
    response_model=RunResponse, 
    tags=["Execution"],
    status_code=status.HTTP_200_OK
)
async def run_skill_crew(request: RunRequest):
    """
    Execute the Skill-Driven Operator with a dynamic task description.
    """
    logger.info("Received run request: %s (thread_id: %s)", request.task_description, request.thread_id)
    
    try:
        # 1. Handle thread_id
        thread_id = request.thread_id or str(uuid.uuid4())
        
        # 2. Retrieve and format history
        history_list = CHAT_HISTORY.get(thread_id, [])
        formatted_history = "No previous context."
        if history_list:
            formatted_history = "\n".join([
                f"{msg['role'].upper()}: {msg['content']}" 
                for msg in history_list
            ])
            
        # 3. Initialize and run the crew
        crew = SkillsCrew()
        result = crew.run(
            task_description=request.task_description, 
            chat_history=formatted_history,
            **request.extra_inputs
        )
        
        # 4. Save history
        if thread_id not in CHAT_HISTORY:
            CHAT_HISTORY[thread_id] = []
        
        CHAT_HISTORY[thread_id].append({"role": "user", "content": request.task_description})
        CHAT_HISTORY[thread_id].append({"role": "assistant", "content": result})
        
        # Keep only last 10 turns (20 messages) to avoid context bloat
        if len(CHAT_HISTORY[thread_id]) > 20:
            CHAT_HISTORY[thread_id] = CHAT_HISTORY[thread_id][-20:]
            
        return RunResponse(
            success=True,
            result=result,
            thread_id=thread_id,
            message="Task completed successfully"
        )
        
    except Exception as e:
        logger.error("Error running Skills Crew: %s", str(e), exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=RunResponse(
                success=False,
                result="",
                message=f"Error executing task: {str(e)}"
            ).model_dump()
        )

@app.post("/api/v1/skills", tags=["Skills"])
async def create_skill(request: SkillCreateRequest):
    """Dynamically create a new skill."""
    try:
        tool = SkillsManagerTool()
        # Ensure name is slugified/safe
        safe_name = request.name.lower().replace(" ", "-")
        
        result = tool._run(
            action="create_skill", 
            skill_name=safe_name, 
            skill_content=request.content
        )
        
        return {"success": True, "message": result}
    except Exception as e:
        logger.error("Error creating skill: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))

# --- Static File Catch-All (MUST BE LAST) ---
@app.get("/{file_path:path}")
async def get_static_file(file_path: str):
    file = static_path / file_path
    if file.exists() and file.is_file():
        return FileResponse(file)
    raise HTTPException(status_code=404)

# --- CLI Entry Point ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
