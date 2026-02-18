"""
Standalone Skills Manager
=========================
Self-contained skill engine — zero dependency on MCP or FastAPI.
All path operations are traversal-safe.
Skills are auto-discovered from the SKILLS_DIR at runtime.
Cache invalidates automatically when the directory changes (mtime check).
"""

import logging
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from core.settings import settings

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Skill Metadata
# ---------------------------------------------------------------------------


@dataclass
class SkillMetadata:
    """Parsed metadata for a single skill."""

    name: str
    slug: str               # directory name (kebab-case)
    description: str
    triggers: list[str]
    version: str
    author: str
    path: Path

    def summary_line(self) -> str:
        trigger_str = (
            f" | triggers: {', '.join(self.triggers)}" if self.triggers else ""
        )
        return f"- **{self.name}** (`{self.slug}`): {self.description}{trigger_str}"


# ---------------------------------------------------------------------------
# Skill Registry (cache layer)
# ---------------------------------------------------------------------------


class SkillRegistry:
    """
    Scans SKILLS_DIR and caches SkillMetadata.
    Cache invalidates on directory mtime change.
    """

    def __init__(self, skills_dir: Path) -> None:
        self._dir = skills_dir
        self._cache: dict[str, SkillMetadata] = {}
        self._dir_mtime: float = 0.0
        self._loaded: bool = False

    def _needs_refresh(self) -> bool:
        if not self._dir.exists():
            return False
        return not self._loaded or self._dir.stat().st_mtime != self._dir_mtime

    def _refresh(self) -> None:
        if not self._dir.exists():
            logger.warning("Skills directory not found: %s", self._dir)
            self._cache = {}
            self._loaded = True
            return

        new_cache: dict[str, SkillMetadata] = {}

        for skill_dir in sorted(self._dir.iterdir()):
            # Skip hidden dirs (like _template) and non-directories
            if not skill_dir.is_dir() or skill_dir.name.startswith("_"):
                continue

            skill_md = skill_dir / "skill.md"
            if not skill_md.exists():
                logger.warning(
                    "Skipping '%s': no skill.md found.", skill_dir.name
                )
                continue

            try:
                meta = self._parse(skill_dir, skill_md)
                new_cache[meta.slug] = meta
                logger.debug("Registered skill: '%s'", meta.slug)
            except Exception as exc:
                logger.error(
                    "Failed to parse skill '%s': %s",
                    skill_dir.name, exc, exc_info=True,
                )

        self._cache = new_cache
        self._dir_mtime = self._dir.stat().st_mtime
        self._loaded = True
        logger.info("Skills registry refreshed: %d skills loaded.", len(self._cache))

    def _parse(self, skill_dir: Path, skill_md: Path) -> SkillMetadata:
        content = skill_md.read_text(encoding="utf-8")
        front_matter: dict[str, Any] = {}

        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3 and parts[1].strip():
                front_matter = yaml.safe_load(parts[1]) or {}

        return SkillMetadata(
            name=front_matter.get("name", skill_dir.name.replace("-", " ").title()),
            slug=skill_dir.name,
            description=front_matter.get("description", "No description provided."),
            triggers=front_matter.get("triggers", []),
            version=str(front_matter.get("version", "1.0.0")),
            author=front_matter.get("author", "unknown"),
            path=skill_dir,
        )

    def all(self) -> dict[str, SkillMetadata]:
        if self._needs_refresh():
            self._refresh()
        return self._cache

    def get(self, slug: str) -> SkillMetadata | None:
        return self.all().get(slug)

    def invalidate(self) -> None:
        """Force cache refresh on next access."""
        self._loaded = False


# ---------------------------------------------------------------------------
# Path safety helper
# ---------------------------------------------------------------------------


def _safe_path(base: Path, relative: str) -> Path | None:
    """
    Resolve a relative path and ensure it stays within base.
    Returns None if path traversal is attempted.
    """
    clean = relative.replace("\\", "/").lstrip("/")
    resolved = (base / clean).resolve()
    try:
        resolved.relative_to(base.resolve())
        return resolved
    except ValueError:
        logger.warning("Path traversal blocked: '%s' under '%s'", relative, base)
        return None


# ---------------------------------------------------------------------------
# Skills Manager (main interface)
# ---------------------------------------------------------------------------


class SkillsManager:
    """
    Production-grade skills manager.
    All public methods return plain strings (safe for MCP / REST / CLI).
    """

    def __init__(self) -> None:
        self._registry = SkillRegistry(settings.SKILLS_DIR)

    # ------------------------------------------------------------------
    # Discovery
    # ------------------------------------------------------------------

    def list_skills(self) -> str:
        """Return a formatted registry of all available skills."""
        skills = self._registry.all()

        if not skills:
            return (
                "⚠️ No skills found.\n"
                f"Add skill directories to: {settings.SKILLS_DIR}"
            )

        lines = [
            f"# Skills Registry ({len(skills)} available)\n",
            "PROTOCOL — always follow this order:",
            "  1. list_skills       → you are here",
            "  2. load_skill        → load full instructions",
            "  3. list_resources    → see available references + scripts",
            "  4. read_resource     → load a reference doc",
            "  5. run_script        → execute a utility script",
            "",
        ]
        lines += [meta.summary_line() for meta in skills.values()]
        lines += [
            "",
            "→ Call load_skill(skill_name=<slug>) to load full instructions.",
        ]
        return "\n".join(lines)

    def search_skills(self, query: str) -> str:
        """Search skills by keyword across name, description, and triggers."""
        skills = self._registry.all()
        q = query.lower()

        matches = [
            meta for meta in skills.values()
            if (
                q in meta.name.lower()
                or q in meta.description.lower()
                or q in meta.slug.lower()
                or any(q in t.lower() for t in meta.triggers)
            )
        ]

        if not matches:
            return (
                f"No skills matched '{query}'.\n"
                "Call list_skills() to see all available skills."
            )

        lines = [f"# Search: '{query}' — {len(matches)} match(es)\n"]
        lines += [meta.summary_line() for meta in matches]
        return "\n".join(lines)

    def get_skill_names(self) -> list[str]:
        """Return raw list of skill slugs (for API / programmatic use)."""
        return sorted(self._registry.all().keys())

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    def load_skill(self, skill_name: str) -> str:
        """Load and return the full skill.md content."""
        meta = self._registry.get(skill_name)
        if not meta:
            available = list(self._registry.all().keys())
            return (
                f"❌ Skill '{skill_name}' not found.\n"
                f"Available: {available}\n"
                "Call list_skills() to see descriptions."
            )

        content = (meta.path / "skill.md").read_text(encoding="utf-8")
        logger.info("Loaded skill '%s' (%d chars)", skill_name, len(content))
        return f"# SKILL LOADED: {meta.name} (v{meta.version})\n\n{content}"

    # ------------------------------------------------------------------
    # Resources
    # ------------------------------------------------------------------

    def list_resources(self, skill_name: str) -> str:
        """List all references and scripts for a skill."""
        meta = self._registry.get(skill_name)
        if not meta:
            return f"❌ Skill '{skill_name}' not found."

        refs_dir = meta.path / "references"
        scripts_dir = meta.path / "scripts"

        refs = sorted(p.name for p in refs_dir.iterdir() if p.is_file()) \
            if refs_dir.exists() else []
        scripts = sorted(p.name for p in scripts_dir.iterdir() if p.is_file()) \
            if scripts_dir.exists() else []

        lines = [f"# Resources: {meta.name}\n"]
        lines.append(f"References ({len(refs)}):")
        lines += [f"  - references/{r}" for r in refs] or ["  (none)"]
        lines.append(f"\nScripts ({len(scripts)}):")
        lines += [f"  - scripts/{s}" for s in scripts] or ["  (none)"]
        lines += [
            "",
            "→ read_resource(skill_name, 'references/<file>') to load a doc.",
            "→ run_script(skill_name, '<script>') to execute.",
        ]
        return "\n".join(lines)

    def read_resource(self, skill_name: str, resource_path: str) -> str:
        """Read a file from a skill's references/ or scripts/ directory."""
        meta = self._registry.get(skill_name)
        if not meta:
            return f"❌ Skill '{skill_name}' not found."

        full_path = _safe_path(meta.path, resource_path)
        if not full_path:
            return "❌ Access denied: path escapes skill directory."
        if not full_path.exists():
            return (
                f"❌ Resource '{resource_path}' not found in skill '{skill_name}'.\n"
                "Call list_resources() to see available files."
            )

        content = full_path.read_text(encoding="utf-8")
        max_chars = settings.MAX_FILE_PREVIEW_CHARS

        if len(content) > max_chars:
            return (
                f"# RESOURCE: {skill_name}/{resource_path} "
                f"(truncated — showing {max_chars}/{len(content)} chars)\n\n"
                f"{content[:max_chars]}\n\n"
                "⚠️ File truncated. Request a specific section if needed."
            )

        logger.info(
            "Read resource '%s/%s' (%d chars)", skill_name, resource_path, len(content)
        )
        return f"# RESOURCE: {skill_name}/{resource_path}\n\n{content}"

    def write_resource(
        self, skill_name: str, resource_path: str, content: str
    ) -> str:
        """Write or overwrite a file inside a skill directory."""
        meta = self._registry.get(skill_name)
        if not meta:
            return f"❌ Skill '{skill_name}' not found."

        full_path = _safe_path(meta.path, resource_path)
        if not full_path:
            return "❌ Access denied: path escapes skill directory."

        full_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            full_path.write_text(content, encoding="utf-8")
            logger.info(
                "Wrote resource '%s/%s' (%d chars)",
                skill_name, resource_path, len(content),
            )
            return f"✅ Written: {skill_name}/{resource_path}"
        except Exception as exc:
            logger.error("Write failed: %s", exc)
            return f"❌ Write failed: {exc}"

    # ------------------------------------------------------------------
    # Script execution
    # ------------------------------------------------------------------

    def run_script(
        self, skill_name: str, script_name: str, script_args: str = ""
    ) -> str:
        """Execute a Python script from a skill's scripts/ directory."""
        meta = self._registry.get(skill_name)
        if not meta:
            return f"❌ Skill '{skill_name}' not found."

        script_path = _safe_path(meta.path, f"scripts/{script_name}")
        if not script_path:
            return "❌ Access denied: path escapes skill directory."
        if not script_path.exists():
            return (
                f"❌ Script '{script_name}' not found in "
                f"skills/{skill_name}/scripts/.\n"
                "Call list_resources() to see available scripts."
            )

        cmd = ["python", str(script_path)]
        if script_args:
            cmd += [a for a in script_args.split() if a]

        logger.info("Running script: %s", " ".join(cmd))

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=settings.SCRIPT_TIMEOUT,
                cwd=str(script_path.parent),
            )
        except subprocess.TimeoutExpired:
            return f"❌ Script timed out after {settings.SCRIPT_TIMEOUT}s."
        except Exception as exc:
            return f"❌ Execution error: {exc}"

        return (
            f"# SCRIPT: {skill_name}/scripts/{script_name}\n\n"
            f"STDOUT:\n{result.stdout or '(empty)'}\n\n"
            f"STDERR:\n{result.stderr or '(empty)'}\n\n"
            f"EXIT CODE: {result.returncode}"
        )

    # ------------------------------------------------------------------
    # Skill creation
    # ------------------------------------------------------------------

    def create_skill(self, skill_name: str, skill_content: str) -> str:
        """Create a new skill directory with skill.md + standard subdirs."""
        skills_dir = settings.SKILLS_DIR
        skills_dir.mkdir(parents=True, exist_ok=True)

        skill_path = skills_dir / skill_name
        if skill_path.exists():
            return f"❌ Skill '{skill_name}' already exists."

        # Auto-inject front matter if missing
        if not skill_content.strip().startswith("---"):
            display_name = skill_name.replace("-", " ").title()
            header = (
                f"---\n"
                f"name: {display_name}\n"
                f"description: Auto-created skill for {display_name}\n"
                f"version: 1.0.0\n"
                f"author: unknown\n"
                f"triggers: []\n"
                f"---\n\n"
            )
            skill_content = header + skill_content

        try:
            skill_path.mkdir(parents=True)
            (skill_path / "skill.md").write_text(skill_content, encoding="utf-8")
            (skill_path / "references").mkdir()
            (skill_path / "scripts").mkdir()
            self._registry.invalidate()
            logger.info("Created skill: '%s'", skill_name)
            return f"✅ Skill '{skill_name}' created successfully."
        except Exception as exc:
            logger.error("Failed to create skill '%s': %s", skill_name, exc)
            return f"❌ Failed to create skill: {exc}"
