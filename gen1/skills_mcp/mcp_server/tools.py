"""
MCP Tools
=========
Each @mcp.tool is a thin adapter over SkillsManager.
No business logic lives here — only parameter mapping.
"""

import logging

from core.skills_manager import SkillsManager
from mcp_server.server import mcp

logger = logging.getLogger(__name__)

_manager = SkillsManager()


@mcp.tool
def skills__list_skills() -> str:
    """
    Discover all available skills with names, descriptions, and triggers.
    Always call this FIRST before loading or using any skill.
    Returns a formatted registry with the recommended usage protocol.
    """
    return _manager.list_skills()


@mcp.tool
def skills__search_skills(query: str) -> str:
    """
    Search skills by keyword.
    Matches against skill name, slug, description, and trigger keywords.
    Use this when you know what domain you need but not the exact skill name.
    """
    return _manager.search_skills(query)


@mcp.tool
def skills__load_skill(skill_name: str) -> str:
    """
    Load the full skill.md instructions for a specific skill.
    Must be called before using any skill capability.
    skill_name must be the slug (e.g. 'api-development', 'code-review').
    Use skills__list_skills first to discover valid slugs.
    """
    return _manager.load_skill(skill_name)


@mcp.tool
def skills__list_resources(skill_name: str) -> str:
    """
    List all reference documents and executable scripts inside a skill.
    Use this after loading a skill to see what supporting files are available.
    """
    return _manager.list_resources(skill_name)


@mcp.tool
def skills__read_resource(skill_name: str, resource_path: str) -> str:
    """
    Read a file from a skill's directory.
    resource_path format: 'references/<filename>' or 'scripts/<filename>'
    Call skills__list_resources first to see available files.
    """
    return _manager.read_resource(skill_name, resource_path)


@mcp.tool
def skills__run_script(
    skill_name: str,
    script_name: str,
    script_args: str = "",
) -> str:
    """
    Execute a Python script from a skill's scripts/ directory.
    Returns stdout, stderr, and exit code.
    Use skills__list_resources to discover available scripts.
    """
    return _manager.run_script(skill_name, script_name, script_args)


@mcp.tool
def skills__create_skill(skill_name: str, skill_content: str) -> str:
    """
    Create a new skill from scratch.
    skill_name: kebab-case slug e.g. 'data-pipeline', 'email-writer'
    skill_content: full markdown content for skill.md
    Recommended front matter format:
        ---
        name: Human Readable Name
        description: What this skill does
        version: 1.0.0
        author: your-name
        triggers: [keyword1, keyword2]
        ---
    Automatically creates references/ and scripts/ subdirectories.
    """
    return _manager.create_skill(skill_name, skill_content)


@mcp.tool
def skills__write_resource(
    skill_name: str,
    resource_path: str,
    resource_content: str,
) -> str:
    """
    Write or overwrite a file inside an existing skill's directory.
    Use this to add reference documents or utility scripts to a skill.
    resource_path examples: 'references/guide.md', 'scripts/validate.py'
    """
    return _manager.write_resource(skill_name, resource_path, resource_content)
