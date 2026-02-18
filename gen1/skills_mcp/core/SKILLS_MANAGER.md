# Skills Manager Logic (`skills_manager.py`)

The `skills_manager.py` file is the **core engine** of the MCP Skills Server. It is designed to be completely independent of the MCP or FastAPI layers, handling the business logic of finding, reading, and executing skills.

## 🏗️ Architecture Breakdown

### 1. Data Model (`SkillMetadata`)
A `dataclass` that serves as a structured container for skill properties:
- **Slug**: The directory name (kebab-case).
- **Metadata**: Parsed info from `skill.md` (Name, Description, Triggers, Version, Author).
- **Paths**: Absolute location for safe resolution.

### 2. Discovery Layer (`SkillRegistry`)
Manages the lifecycle of skill discovery and memory:
- **Dynamic Scanning**: Iterates through `SKILLS_DIR` to find valid skill directories.
- **Smart Caching**: Stores metadata in memory to avoid redundant disk I/O.
- **Hot-Reload**: Automatically detects changes by checking the directory's `mtime`. If you add/remove a skill, it refreshes on the next call.
- **Exclusion Logic**: Dirs starting with `_` (e.g., `_template/`) are hidden from the agent.

### 3. Security Helper (`_safe_path`)
A critical **Production-Grade Security** feature:
- **Path Traversal Prevention**: Resolves all relative paths and verifies that the resulting absolute path remains within the skill's base directory.
- **Blocking**: Any attempt to access files outside the allowed scope (like system files) is caught and blocked.

### 4. Main Interface (`SkillsManager`)
The primary class used by the MCP tools. Key capabilities include:

#### **Discovery & Search**
- `list_skills()`: Returns a formatted registry designed for LLM comprehension.
- `search_skills()`: Allows keyword matching across descriptions and triggers.

#### **Resource Management**
- `load_skill()`: Reads the core instruction set from `skill.md`.
- `read_resource()`/`write_resource()`: Manages supporting documents and scripts inside the `references/` and `scripts/` subfolders.
- **Truncation Support**: Large files are automatically truncated to prevent context window bloat.

#### **Script Execution (`run_script`)**
Handles the safe execution of utility scripts:
- **Isolation**: Runs Python scripts in a separate process.
- **Timeout Protection**: Kills execution if it exceeds `SCRIPT_TIMEOUT` (default: 60s).
- **Output Capture**: Returns `STDOUT`, `STDERR`, and the exit code to the caller.

#### **Dynamic Growth**
- `create_skill()`: Bootstraps new skill directories.
- **Auto-Injection**: If a skill is created without a YAML header, the manager automatically injects a standard production-grade template.

## 🔄 Operational Flow

The following diagram illustrates the lifecycle of a request through the `SkillsManager`:

```mermaid
sequenceDiagram
    participant Agent as Agent / MCP Client
    participant Tool as MCP Tool
    participant SM as SkillsManager
    participant Reg as SkillRegistry
    participant FS as File System

    Agent->>Tool: Request Action (e.g., list_skills)
    Tool->>SM: Call method
    SM->>Reg: all() / get(slug)
    
    Note over Reg: Check Cache Invalidation
    Reg->>FS: stat(SKILLS_DIR) mtime
    
    alt Needs Refresh (mtime changed)
        Reg->>FS: iterdir()
        Reg->>FS: read skill.md
        Reg: Parse & Cache Metadata
    else Use Cache
        Reg: Return Metadata
    end

    Reg-->>SM: SkillMetadata
    SM->>FS: read resource / execute script
    FS-->>SM: File Content / Process Result
    SM-->>Tool: Formatted Markdown String
    Tool-->>Agent: Result
```

### 1. Discovery & Hot-Reload Logic
The `SkillRegistry` ensures the server never needs a restart when you add new skills:
- **Registry Check**: Every time `SkillsManager` asks for skill data, the registry performs an `mtime` check on the directory.
- **Minimal Overhead**: If the directory hasn't changed, it uses the dictionary in memory.
- **Isolation**: When a change is detected, it invalidated the *entire* cache and rebuilds it. This ensures that renamed or deleted skills are handled correctly without dangling references.

### 2. Execution Protocol (`run_script`)
When an agent calls `run_script`, the system follows a strictly controlled pipeline:
1.  **Path Resolution**: The `relative_path` is resolved against the skill's absolute path using `_safe_path`.
2.  **Environment Preparation**: The `cwd` (current working directory) is set to the folder containing the script, ensuring relative imports within the script work correctly.
3.  **Process Forking**: `subprocess.run` is called in `text=True` mode to capture string output.
4.  **Guard Rails**:
    - **Timeout**: The `SCRIPT_TIMEOUT` env var prevents scripts from locking up the server.
    - **Captured Streams**: Both standard output and errors are captured, even if the script crashes.
5.  **Result Synthesis**: The exit code, stdout, and stderr are combined into a single Markdown block so the Agent can "see" what happened inside the terminal.

### 3. State Management
- **Stateless in Memory**: Everything in `SkillsManager` is designed to be rebuildable from the filesystem. If the server crashes, it loses nothing except the current connection; the "state" is the folder structure on disk.
- **Safe Writing**: `write_resource` creates parent directories automatically, allowing agents to create complex nested knowledge bases within their skills.

---

## 🛡️ Why it's Production Ready
1.  **Security**: Hardened against malicious path traversal.
2.  **Reliability**: Subprocess management with timeouts prevents zombie processes.
3.  **Efficiency**: `mtime`-based caching provides high performance with zero-restart updates.
4.  **Portability**: Zero external dependencies outside the standard library and `PyYAML`.
