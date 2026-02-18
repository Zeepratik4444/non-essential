# Import tools and resources so their decorators register on `mcp`
import mcp_server.tools       # noqa: F401
import mcp_server.resources   # noqa: F401

from mcp_server.server import mcp

__all__ = ["mcp"]
