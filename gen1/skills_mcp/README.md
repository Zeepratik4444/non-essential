# Skills MCP Server

Production-grade Standalone modular MCP server for dynamic skills.

## Features
- **MCP Native**: Full support for tools and URI-addressable resources.
- **Unified Entry Point**: Supports Stdio (local) and HTTP/SSE (remote) transforms.
- **Modular Architecture**: Clean separation between business logic and MCP layer.
- **Hot Reload**: Skills are discovered dynamically via filesystem watch.

## Quick Start
```bash
# 1. Setup
uv sync
cp .env.example .env

# 2. Run over HTTP
uv run uvicorn app:app --reload

# 3. Run over Stdio (for Claude Desktop)
uv run python -m mcp_server
```
