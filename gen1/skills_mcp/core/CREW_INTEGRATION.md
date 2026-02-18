# CrewAI Integration Architecture (`core/crew.py`)

The `SkillsCrew` integrates the autonomous reasoning capabilities of CrewAI directly into the MCP Skills Server using the `MCPServerAdapter`.

## 🏗️ Architecture Overview

The crew is built using the `@CrewBase` decorator, providing a clean separation of agent and task definitions while utilizing the project's own MCP server as a tool source.

### 1. Unified Agent (`skills_operator`)
The `skills_operator` is the primary agent responsible for executing tasks.
- **Role**: Autonomous Skill-Driven Operator (MCP).
- **Tools**: It uses the `MCPServerAdapter` to dynamically discover and use tools from the local MCP server.
- **Reasoning**: It follows an "MCP-Native" protocol, leveraging `skills__` prefixed tools.

### 2. Task Orchestration (`execute_task`)
A single, highly interpolative task that handles:
- **Task Description**: The primary objective from the user.
- **Chat History**: Context from previous turns to maintain conversation continuity.

## 🛠️ Tool Integration Logic (`MCPServerAdapter`)

The crew uses the native `MCPServerAdapter` from `crewai-tools` to connect to the MCP server via **streamable-HTTP (SSE)**.

### SSE Connection
The crew connects to the running server's SSE endpoint. This is defined in `server_params`:
- **Transport**: `sse`
- **URL**: Defined in `settings.MCP_SSE_URL` (defaults to `http://localhost:8000/mcp`).
- **Lifecycle**: This allows the crew to act as a truly remote client, capable of connecting to the MCP server even if it's running on a different machine.

## 🔄 Execution Flow

1.  **Request**: A POST request is sent to `/api/v1/run`.
2.  **Initialization**: `app.py` instantiates `SkillsCrew`.
3.  **Discovery**: Upon tool access, the `MCPServerAdapter` starts the `mcp_server` via stdio and fetches tool schemas.
4.  **Execution**: The agent uses the discovered tools to iterate on the task.
5.  **Result**: The final output is returned as a JSON response.

## 🛡️ Why it's Production Ready
- **Protocol Parity**: The agent uses the exact same interface as external MCP clients.
- **Environment Isolation**: The server runs in a managed subprocess with controlled environment variables.
- **Scalability**: The modular adapter pattern allows connecting to additional MCP servers easily in the future.
