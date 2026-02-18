import logging
import subprocess
import yaml
from pathlib import Path
from typing import Any, Literal, Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field, model_validator

from src.config.settings import settings

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Internal skill metadata (not exposed outside this module)
# ---------------------------------------------------------------------------

class _SkillMetadata:
    __slots__ = ("name", "description", "path", "triggers")

    def __init__(self, name: str, description: str, path: Path, triggers: list[str]) -> None:
        self.name = name
        self.description = description
        self.path = path
        self.triggers = triggers

    def to_prompt_line(self) -> str:
        trigger_str = f" | triggers: {', '.join(self.triggers)}" if self.triggers else ""
        return f"- **{self.name}**: {self.description}{trigger_str}"


# ---------------------------------------------------------------------------
# Input schema
# ---------------------------------------------------------------------------

class SkillsManagerInput(BaseModel):
    action: Literal[
        "list_skills",       # → returns system-prompt-ready skill registry
        "load_skill",        # → reads skill.md
        "list_resources",    # → lists references/ and scripts/
        "read_resource",     # → loads a reference or script file
        "run_script",        # → executes scripts/<script>.py
    ] = Field(..., description="Action to perform.")

    skill_name: str | None = Field(
        default=None,
        description="Required for all actions except 'list_skills'.",
    )
    resource_path: str | None = Field(
        default=None,
        description="Required for 'read_resource'. Relative path, e.g., 'references/api.md'.",
    )
    script_name: str | None = Field(
        default=None,
        description="Required for 'run_script'. Script filename, e.g., 'validate.py'.",
    )
    script_args: str = Field(
        default="",
        description="Optional space-separated args for 'run_script'.",
    )

    @model_validator(mode="after")
    def validate_required_fields(self) -> "SkillsManagerInput":
        if self.action != "list_skills" and not self.skill_name:
            raise ValueError(f"'skill_name' is required for action '{self.action}'.")
        if self.action == "read_resource" and not self.resource_path:
            raise ValueError("'resource_path' is required for action 'read_resource'.")
        if self.action == "run_script" and not self.script_name:
            raise ValueError("'script_name' is required for action 'run_script'.")
        return self


# ---------------------------------------------------------------------------
# Main tool
# ---------------------------------------------------------------------------

class SkillsManagerTool(BaseTool):
    """
    Single unified tool that owns the entire skills lifecycle:
    - Dynamically scans and caches skill metadata from ./skills/ at first call.
    - Exposes list_skills, load_skill, list_resources, read_resource, run_script.
    - Cache is invalidated and rebuilt if the skills directory changes (mtime check).
    - All path operations are traversal-safe.

    Use 'list_skills' first to discover what is available and build your plan.
    Use 'load_skill' before using any skill.
    """

    name: str = "skills_manager"
    description: str = (
        "Unified skills manager. Actions: "
        "'list_skills' → discover all registered skills with descriptions; "
        "'load_skill' → load full skill.md instructions; "
        "'list_resources' → see available references and scripts for a skill; "
        "'read_resource' → load a reference doc or view a script; "
        "'run_script' → execute a utility script from a skill. "
        "Always call list_skills first, then load_skill before using any capability."
    )
    args_schema: Type[BaseModel] = SkillsManagerInput

    # Internal state — Pydantic-excluded private attributes
    _cache: dict[str, _SkillMetadata] = {}
    _skills_dir_mtime: float = 0.0
    _cache_loaded: bool = False

    # ------------------------------------------------------------------
    # Cache management
    # ------------------------------------------------------------------

    def _get_skills_dir(self) -> Path:
        return settings.SKILLS_DIR

    def _needs_refresh(self) -> bool:
        skills_dir = self._get_skills_dir()
        if not skills_dir.exists():
            return False
        current_mtime = skills_dir.stat().st_mtime
        return not self._cache_loaded or current_mtime != self._skills_dir_mtime

    def _refresh_cache(self) -> None:
        skills_dir = self._get_skills_dir()
        if not skills_dir.exists():
            logger.warning("Skills directory not found: %s", skills_dir)
            self._cache = {}
            self._cache_loaded = True
            return

        new_cache: dict[str, _SkillMetadata] = {}

        for skill_dir in sorted(skills_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "skills.md"
            if not skill_md.exists():
                logger.warning("Skipping '%s': no skills.md found.", skill_dir.name)
                continue
            try:
                meta = self._parse_skill_md(skill_dir, skill_md)
                new_cache[meta.name] = meta
                logger.debug("Cached skill: '%s'", meta.name)
            except Exception as exc:
                logger.error("Failed to parse skill '%s': %s", skill_dir.name, exc, exc_info=True)

        self._cache = new_cache
        self._skills_dir_mtime = skills_dir.stat().st_mtime
        self._cache_loaded = True
        logger.info("Skills cache refreshed: %d skills loaded.", len(self._cache))

    def _parse_skill_md(self, skill_dir: Path, skill_md: Path) -> _SkillMetadata:
        content = skill_md.read_text(encoding="utf-8")
        front_matter: dict[str, Any] = {}

        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 2 and parts[1].strip():
                front_matter = yaml.safe_load(parts[1]) or {}

        name: str = front_matter.get("name", skill_dir.name)
        description: str = front_matter.get("description", "No description provided.")
        triggers: list[str] = front_matter.get("triggers", [])
        return _SkillMetadata(name=name, description=description, path=skill_dir, triggers=triggers)

    def _get_cache(self) -> dict[str, _SkillMetadata]:
        if self._needs_refresh():
            self._refresh_cache()
        return self._cache

    def _resolve_skill(self, skill_name: str) -> _SkillMetadata | None:
        return self._get_cache().get(skill_name)

    # ------------------------------------------------------------------
    # Path safety
    # ------------------------------------------------------------------

    def _safe_resolve(self, skill_meta: _SkillMetadata, relative: str) -> Path | None:
        """Resolve path and verify it stays within the skill's directory."""
        clean = relative.replace("\\", "/").lstrip("/")
        full = (skill_meta.path / clean).resolve()
        try:
            full.relative_to(skill_meta.path.resolve())
            return full
        except ValueError:
            logger.warning(
                "Path traversal blocked: '%s' in skill '%s'", relative, skill_meta.name
            )
            return None

    # ------------------------------------------------------------------
    # Action handlers
    # ------------------------------------------------------------------

    def _handle_list_skills(self) -> str:
        cache = self._get_cache()
        if not cache:
            return "⚠️ No skills found in skills directory. Ensure ./skills/ exists and contains skill.md files."
        lines = ["# Available Skills\n"]
        lines += [meta.to_prompt_line() for meta in cache.values()]
        lines += [
            "",
            "→ Use load_skill('<name>') to load full instructions before using any skill.",
        ]
        return "\n".join(lines)

    def _handle_load_skill(self, skill_name: str) -> str:
        meta = self._resolve_skill(skill_name)
        if not meta:
            available = list(self._get_cache().keys())
            return (
                f"❌ Skill '{skill_name}' not found.\n"
                f"Available: {available}\n"
                "Call action='list_skills' to see descriptions."
            )
        skill_md = meta.path / "skill.md"
        content = skill_md.read_text(encoding="utf-8")
        logger.info("Loaded skill.md: '%s' (%d chars)", skill_name, len(content))
        return f"# SKILL LOADED: {skill_name}\n\n{content}"

    def _handle_list_resources(self, skill_name: str) -> str:
        meta = self._resolve_skill(skill_name)
        if not meta:
            return f"❌ Skill '{skill_name}' not found."

        refs_dir = meta.path / "references"
        scripts_dir = meta.path / "scripts"

        refs = sorted(p.name for p in refs_dir.iterdir() if p.is_file()) if refs_dir.exists() else []
        scripts = sorted(p.name for p in scripts_dir.iterdir() if p.is_file()) if scripts_dir.exists() else []

        lines = [f"# Resources: {skill_name}\n"]
        lines.append(f"References ({len(refs)}):")
        lines += [f"  - references/{r}" for r in refs] or ["  (none)"]
        lines.append(f"\nScripts ({len(scripts)}):")
        lines += [f"  - scripts/{s}" for s in scripts] or ["  (none)"]
        lines += [
            "",
            "→ Use action='read_resource' with resource_path='references/<file>' to load.",
            "→ Use action='run_script' with script_name='<file>' to execute.",
        ]
        return "\n".join(lines)

    def _handle_read_resource(self, skill_name: str, resource_path: str) -> str:
        meta = self._resolve_skill(skill_name)
        if not meta:
            return f"❌ Skill '{skill_name}' not found."

        full_path = self._safe_resolve(meta, resource_path)
        if not full_path:
            return "❌ Access denied: path escapes skill directory."
        if not full_path.exists():
            return (
                f"❌ Resource '{resource_path}' not found in skill '{skill_name}'.\n"
                "Call action='list_resources' to see available files."
            )

        content = full_path.read_text(encoding="utf-8")
        length = len(content)

        if length > settings.MAX_FILE_PREVIEW_CHARS:
            preview = content[: settings.MAX_FILE_PREVIEW_CHARS]
            return (
                f"# RESOURCE: {skill_name}/{resource_path} "
                f"(PREVIEW — {length} total chars, first {settings.MAX_FILE_PREVIEW_CHARS} shown)\n\n"
                f"{preview}\n\n"
                f"⚠️ File truncated. Request a specific section if needed."
            )

        logger.info("Read resource: '%s/%s' (%d chars)", skill_name, resource_path, length)
        return f"# RESOURCE: {skill_name}/{resource_path}\n\n{content}"

    def _handle_run_script(self, skill_name: str, script_name: str, script_args: str) -> str:
        meta = self._resolve_skill(skill_name)
        if not meta:
            return f"❌ Skill '{skill_name}' not found."

        script_path = self._safe_resolve(meta, f"scripts/{script_name}")
        if not script_path:
            return "❌ Access denied: path escapes skill directory."
        if not script_path.exists():
            return (
                f"❌ Script '{script_name}' not found in skills/{skill_name}/scripts/.\n"
                "Call action='list_resources' to see available scripts."
            )

        cmd = ["python", str(script_path)] + ([a for a in script_args.split() if a] if script_args else [])
        logger.info("Running script: %s", " ".join(cmd))

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=settings.SCRIPT_TIMEOUT,
                cwd=script_path.parent,
            )
        except subprocess.TimeoutExpired:
            logger.error("Script '%s' timed out after %ds", script_name, settings.SCRIPT_TIMEOUT)
            return f"❌ Script timed out after {settings.SCRIPT_TIMEOUT}s."
        except Exception as exc:
            logger.exception("Script execution failed for '%s': %s", script_name, exc)
            return f"❌ Execution error: {exc}"

        return (
            f"# SCRIPT RESULT: {skill_name}/scripts/{script_name}\n\n"
            f"STDOUT:\n{result.stdout or '(empty)'}\n\n"
            f"STDERR:\n{result.stderr or '(empty)'}\n\n"
            f"EXIT CODE: {result.returncode}"
        )

    def _run(self, **kwargs: Any) -> str:
        action = kwargs["action"]
        skill_name = kwargs.get("skill_name") or ""
        resource_path = kwargs.get("resource_path") or ""
        script_name = kwargs.get("script_name") or ""
        script_args = kwargs.get("script_args", "")

        dispatch = {
            "list_skills":    lambda: self._handle_list_skills(),
            "load_skill":     lambda: self._handle_load_skill(skill_name),
            "list_resources": lambda: self._handle_list_resources(skill_name),
            "read_resource":  lambda: self._handle_read_resource(skill_name, resource_path),
            "run_script":     lambda: self._handle_run_script(skill_name, script_name, script_args),
        }

        handler = dispatch.get(action)
        if not handler:
            return f"❌ Unknown action '{action}'. Valid: {list(dispatch.keys())}"

        return handler()
