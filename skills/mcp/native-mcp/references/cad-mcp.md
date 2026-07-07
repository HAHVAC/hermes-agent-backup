# AutoCAD & CAD MCP Integration

This reference notes key implementation details, requirements, and behaviors for interfacing Claude, Cursor, or Codex with CAD software (AutoCAD, AutoCAD LT, ZWCAD, BricsCAD, GstarCAD) using MCP servers.

## Active MCP Servers for CAD
There are two primary open-source MCP implementations:

1. **`AnCode666/multiCAD-mcp`** (Multi-CAD COM Adapter)
2. **`puran-water/autocad-mcp`** (AutoCAD LT focused with Headless ezdxf support)

---

## 1. Connection & Startup Behaviors

### multiCAD-mcp (COM-based)
- **CAD Status Required:** AutoCAD **does not need to be running** beforehand, but if it is running, the connection is established much faster.
- **COM Lifecycle:** It uses Windows COM (`pywin32`) to look for a running CAD instance. If none is found, it attempts to launch the CAD executable.
- **Startup Wait Time:** There is a configurable parameter (`startup_wait_time` in `src/config.json`, defaults to `20` seconds). If the machine is slow or CAD is heavy, launching can timeout. In those environments, either increase the wait time or **open AutoCAD manually first**.
- **Supported CADs:** AutoCAD®, ZWCAD®, GstarCAD®, and BricsCAD® (they share a similar COM model).
- **ZWCAD Support Config:** To target ZWCAD instead of AutoCAD, modify `src/config.json` to configure ZWCAD-specific wait times and target types under `cad.type` (e.g. `"ZWCAD"` or setting ZWCAD settings under the cad adapter configuration block).

### autocad-mcp (LISP/File-IPC & Headless)
This server runs a hybrid architecture based on your environment:
1. **File IPC Backend:** Requires AutoCAD LT 2024+ (or full AutoCAD) on Windows. It requires loading an AutoLISP dispatcher (`mcp_dispatch.lsp`) via `APPLOAD` inside CAD. It uses focus-free `PostMessageW` calls, enabling background operations.
2. **ezdxf Backend (Headless):** Does **not** require AutoCAD to be installed or open. Runs cross-platform (Linux, macOS, Windows) by creating the DXF structure in-memory and outputting the vector files directly.

---

## 2. Selection Criteria: Drawing vs Reading/Quantifying
When deciding which repository to deploy, consider the primary user objective:

### Scenario A: Reading, Comparing Drawings & Quantity Takeoff (No Drawing)
- **Primary Recommendation:** **`AnCode666/multiCAD-mcp`**.
- **Why:** 
  - **`export_data` tool:** Allows extracting data in bulk (scope: `all` or `selected`) into structured `json` (for LLM ingestion) or `excel` (generates multi-sheet `.xlsx` tables with details of Entities, Layers, and Blocks).
  - **Block attributes extraction:** Supported via `get_attrs|handle` commands, enabling precise quantification of attributes and counts of equipment blocks (e.g., PCCC valves, sensors, sprinkler types).
  - **Visual audit / Comparison:** Supports `export_view` and `screenshot` tools for programmatic viewport capture, allowing LLMs to visually compare changes between drawings.

### Scenario B: Dynamic Drawing / Background Creation
- **Primary Recommendation:** **`puran-water/autocad-mcp`** or **`AnCode666/multiCAD-mcp`**.
- **Why:** `puran-water/autocad-mcp` allows background operations using Win32 PostMessage, preventing focus-stealing during drawing tasks, and supports headless rendering via matplotlib when no CAD software is present.

---

## 3. Typical Troubleshooting & Configuration

### Windows COM Troubleshooting
- Ensure Windows COM is registered for your CAD software (run CAD as Administrator once to register COM if connection fails).
- The python environment running the MCP server must have `pywin32` installed and upgraded (`uv run python -m pip install --upgrade pywin32`).
- **Security Check:** Ensure `"output.allow_arbitrary_paths": false` is retained in `config.json` to prevent arbitrary file writes or path traversal vulnerabilities. Run IDEs and MCP clients with normal user permissions, not Administrator.

### Desktop Client Configuration (Claude Desktop / Cursor)
Ensure you point to the absolute path of the virtual environment python interpreter (`.venv\Scripts\python.exe`) rather than system python.

#### Sample `multiCAD-mcp` configuration:
```json
{
  "mcpServers": {
    "multiCAD": {
      "command": "C:\\path\\to\\multiCAD-mcp\\.venv\\Scripts\\python.exe",
      "args": ["C:\\path\\to\\multiCAD-mcp\\src\\server.py"]
    }
  }
}
```

#### Sample `autocad-mcp` configuration:
```json
{
  "mcpServers": {
    "autocad-mcp": {
      "command": "C:\\path\\to\\autocad-mcp\\.venv\\Scripts\\python.exe",
      "args": ["-m", "autocad_mcp"],
      "env": { "AUTOCAD_MCP_BACKEND": "auto" }
    }
  }
}
```
