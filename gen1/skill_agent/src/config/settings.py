import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings:
    SKILLS_DIR: Path = BASE_DIR / "skills"
    SCRIPT_TIMEOUT: int = int(os.getenv("SCRIPT_TIMEOUT", "60"))
    MAX_FILE_PREVIEW_CHARS: int = int(os.getenv("MAX_FILE_PREVIEW_CHARS", "5000"))
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini/gemini-2.5-flash")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def validate(cls) -> None:
        if not cls.SKILLS_DIR.exists():
            raise FileNotFoundError(
                f"Skills directory not found: {cls.SKILLS_DIR}. "
                "Create it and add skill subdirectories."
            )

settings = Settings()
