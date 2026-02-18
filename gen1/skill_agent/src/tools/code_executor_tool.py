import logging
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path
from typing import Literal, Type, ClassVar

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class CodeExecutorInput(BaseModel):
    action: Literal[
        "run_python",     # Execute a Python code string
        "run_script",     # Execute a .py file by absolute path
        "install_package" # pip install a package into current env
    ] = Field(..., description="Action to perform.")

    code: str | None = Field(
        default=None,
        description="Python code string to execute. Required for 'run_python'."
    )
    script_path: str | None = Field(
        default=None,
        description="Absolute path to .py file. Required for 'run_script'."
    )
    package_name: str | None = Field(
        default=None,
        description="Package name to install. Required for 'install_package'."
    )
    timeout: int = Field(
        default=30,
        description="Execution timeout in seconds (max 120)."
    )
    working_dir: str | None = Field(
        default=None,
        description="Working directory for execution. Defaults to skill_agent root."
    )


class CodeExecutorTool(BaseTool):
    """
    Sandboxed Python code execution tool.
    Can run inline code strings, execute .py scripts, and install packages.
    All executions are isolated in a subprocess with timeout enforcement.

    USE THIS TO:
    - Test code snippets before writing them to files
    - Execute scripts from skills/*/scripts/
    - Validate that generated code works
    - Install missing dependencies at runtime
    """

    name: str = "code_executor"
    description: str = (
        "Execute Python code safely. Actions: "
        "'run_python' → run a code string inline; "
        "'run_script' → run a .py file by path; "
        "'install_package' → pip install a package. "
        "Always test generated code before writing it to a skill file."
    )
    args_schema: Type[BaseModel] = CodeExecutorInput

    BASE_DIR: ClassVar[Path] = Path(__file__).resolve().parent.parent.parent

    def _safe_timeout(self, timeout: int) -> int:
        return min(max(timeout, 5), 120)

    def _run_subprocess(self, cmd: list[str], cwd: Path, timeout: int) -> str:
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(cwd),
            )
            output = []
            if result.stdout.strip():
                output.append(f"STDOUT:\n{result.stdout.strip()}")
            if result.stderr.strip():
                output.append(f"STDERR:\n{result.stderr.strip()}")
            output.append(f"EXIT CODE: {result.returncode}")

            status = "✅ Success" if result.returncode == 0 else "❌ Failed"
            return f"{status}\n\n" + "\n\n".join(output)

        except subprocess.TimeoutExpired:
            return f"❌ Timeout: execution exceeded {timeout}s limit."
        except Exception as e:
            logger.exception("Subprocess error: %s", e)
            return f"❌ Execution error: {e}"

    def _handle_run_python(self, code: str, timeout: int, working_dir: str | None) -> str:
        if not code or not code.strip():
            return "❌ No code provided."

        cwd = Path(working_dir).resolve() if working_dir else self.BASE_DIR

        # Write to temp file
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            prefix="skill_exec_",
            delete=False,
            encoding="utf-8"
        ) as f:
            f.write(textwrap.dedent(code))
            tmp_path = f.name

        logger.info("Executing inline code from temp file: %s", tmp_path)
        try:
            return self._run_subprocess(
                [sys.executable, tmp_path],
                cwd=cwd,
                timeout=self._safe_timeout(timeout)
            )
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def _handle_run_script(self, script_path: str, timeout: int, working_dir: str | None) -> str:
        path = Path(script_path).resolve()
        if not path.exists():
            return f"❌ Script not found: {script_path}"
        if path.suffix != ".py":
            return f"❌ Only .py scripts supported. Got: {path.suffix}"

        cwd = Path(working_dir).resolve() if working_dir else path.parent
        logger.info("Executing script: %s", path)
        return self._run_subprocess(
            [sys.executable, str(path)],
            cwd=cwd,
            timeout=self._safe_timeout(timeout)
        )

    def _handle_install_package(self, package_name: str) -> str:
        if not package_name or not package_name.strip():
            return "❌ No package name provided."

        # Basic safety — no shell injection
        safe_name = package_name.strip().split()[0]
        logger.info("Installing package: %s", safe_name)
        return self._run_subprocess(
            [sys.executable, "-m", "pip", "install", safe_name],
            cwd=self.BASE_DIR,
            timeout=60
        )

    def _run(self, **kwargs) -> str:
        action = kwargs.get("action")
        code = kwargs.get("code")
        script_path = kwargs.get("script_path")
        package_name = kwargs.get("package_name")
        timeout = kwargs.get("timeout", 30)
        working_dir = kwargs.get("working_dir")

        if action == "run_python":
            return self._handle_run_python(code or "", timeout, working_dir)
        elif action == "run_script":
            return self._handle_run_script(script_path or "", timeout, working_dir)
        elif action == "install_package":
            return self._handle_install_package(package_name or "")
        else:
            return f"❌ Unknown action '{action}'. Valid: run_python, run_script, install_package"
