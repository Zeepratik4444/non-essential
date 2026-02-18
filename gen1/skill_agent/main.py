import sys
import logging
from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# Add src to path so relative imports work
sys.path.append(str(Path(__file__).parent / "src"))

from src.crew import SkillsCrew

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

# --- Static Files and Root Endpoint ---
static_path = Path(__file__).parent / "static"
app.mount("/ui", StaticFiles(directory=str(static_path), html=True), name="static")

@app.get("/")
async def read_index():
    """Serve the web interface."""
    return FileResponse(static_path / "index.html")

# Help static files find style.css etc if relative paths are used
@app.get("/{file_path:path}")
async def get_static_file(file_path: str):
    file = static_path / file_path
    if file.exists() and file.is_file():
        return FileResponse(file)
    raise HTTPException(status_code=404)

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

class RunResponse(BaseModel):
    success: bool
    result: str
    message: str | None = None

# --- Endpoints ---

@app.get("/health", tags=["Monitoring"])
async def health_check():
    """Verify the API is running."""
    return {"status": "healthy", "version": "0.2.0"}

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
    logger.info("Received run request: %s", request.task_description)
    
    try:
        # Initialize the crew
        # Note: SkillsCrew extracts settings internally
        crew = SkillsCrew()
        
        # Run the crew
        result = crew.run(
            task_description=request.task_description, 
            **request.extra_inputs
        )
        
        return RunResponse(
            success=True,
            result=result,
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

# --- CLI Entry Point ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
