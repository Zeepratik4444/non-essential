"""
Stdio entry point.
Allows: python -m mcp_server
Used by Claude Desktop and local IDE integrations.
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import mcp_server  # noqa: F401 — registers tools + resources
from mcp_server.server import mcp
from core.settings import settings

try:
    settings.validate()
except EnvironmentError as e:
    print(f"Startup validation failed:\n{e}", file=sys.stderr)

mcp.run()   # defaults to stdio transport
