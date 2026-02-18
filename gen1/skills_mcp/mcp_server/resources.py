"""
MCP Resources
=============
Exposes the skills directory as a browsable, URI-addressable file tree.
Resources are read-only and cached by MCP clients automatically.
"""

import json
import logging

from core.skills_manager import SkillsManager
from mcp_server.server import mcp

logger = logging.getLogger(__name__)

_manager = SkillsManager()


@mcp.resource(
    "skills://registry",
    name="Skills Registry",
    description="Full JSON index of all available skills with metadata.",
    mime_type="application/json",
    tags={"skills", "registry", "index"},
)
def get_skills_registry() -> str:
    """Structured JSON registry of every skill."""
    skills = _manager._registry.all()
    registry = {
        slug: {
            "name": meta.name,
            "slug": meta.slug,
            "description": meta.description,
            "triggers": meta.triggers,
            "version": meta.version,
            "author": meta.author,
        }
        for slug, meta in skills.items()
    }
    return json.dumps(registry, indent=2)


@mcp.resource(
    "skill://{skill_name}/skill.md",
    name="Skill Instructions",
    description="Full skill.md instruction file for the given skill.",
    mime_type="text/markdown",
    tags={"skills", "instructions"},
)
def get_skill_instructions(skill_name: str) -> str:
    """Read skill.md for the given skill slug."""
    return _manager.load_skill(skill_name)


@mcp.resource(
    "skill://{skill_name}/references/{filename}",
    name="Skill Reference Document",
    description="A reference document from a skill's references/ directory.",
    mime_type="text/markdown",
    tags={"skills", "references"},
)
def get_skill_reference(skill_name: str, filename: str) -> str:
    """Read a reference document from a skill."""
    return _manager.read_resource(skill_name, f"references/{filename}")


@mcp.resource(
    "skill://{skill_name}/scripts/{filename}",
    name="Skill Script",
    description="A Python script from a skill's scripts/ directory.",
    mime_type="text/x-python",
    tags={"skills", "scripts"},
)
def get_skill_script(skill_name: str, filename: str) -> str:
    """Read a script file from a skill."""
    return _manager.read_resource(skill_name, f"scripts/{filename}")
