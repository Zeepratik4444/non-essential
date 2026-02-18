import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings:
    # Paths
    BASE_DIR: Path = BASE_DIR
    SKILLS_DIR: Path = Path(os.getenv("SKILLS_DIR", str(BASE_DIR / "skills")))

    # LLM
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini/gemini-2.5-flash")

    # Skills engine
    SCRIPT_TIMEOUT: int = int(os.getenv("SCRIPT_TIMEOUT", "60"))
    MAX_FILE_PREVIEW_CHARS: int = int(os.getenv("MAX_FILE_PREVIEW_CHARS", "8000"))

    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    RELOAD: bool = os.getenv("RELOAD", "false").lower() == "true"

    # MCP Server identity
    MCP_SERVER_NAME: str = os.getenv("MCP_SERVER_NAME", "skills-mcp-server")
    MCP_SERVER_VERSION: str = os.getenv("MCP_SERVER_VERSION", "1.0.0")

    # SSE endpoint for CrewAI (if using streamable-http)
    @property
    def MCP_SSE_URL(self) -> str:
        # Defaults to local server URL
        return os.getenv("MCP_SSE_URL", f"http://{self.HOST}:{self.PORT}/mcp")

    @classmethod
    def validate(cls) -> None:
        errors = []
        if not cls.GOOGLE_API_KEY:
            errors.append("GOOGLE_API_KEY is not set.")
        if not cls.SKILLS_DIR.exists():
            # Auto-create if not exists for better UX
            cls.SKILLS_DIR.mkdir(parents=True, exist_ok=True)
            
        if errors:
            raise EnvironmentError("\n".join(f"  - {e}" for e in errors))


settings = Settings()
