import logging
from fastmcp import FastMCP
from core.settings import settings

logger = logging.getLogger(__name__)

mcp = FastMCP(
    name=settings.MCP_SERVER_NAME,
    version=settings.MCP_SERVER_VERSION,
    description="Production-grade Skills MCP Server with autonomous reasoning.",
    instructions=(
        f"You are the {settings.MCP_SERVER_NAME} operator (v{settings.MCP_SERVER_VERSION}). "
        "You have access to a dynamic skills system. "
        "PROTOCOL: "
        "1. ALWAYS start by calling skills__list_skills to discover capabilities. "
        "2. Then call skills__load_skill before using any skill. "
        "3. Follow the loaded skill protocol exactly. "
        "Never guess — maintain production-grade precision."
    ),
)

logger.info("FastMCP instance '%s' (v%s) initialized.", settings.MCP_SERVER_NAME, settings.MCP_SERVER_VERSION)
