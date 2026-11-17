# openclaw-genpark-envoy

[![Organization](https://img.shields.io/badge/AlphaPark-OpenSource-blue.svg)](https://github.com/Alpha-Park)
[![Model Context Protocol](https://img.shields.io/badge/MCP-Standard-orange.svg)](https://modelcontextprotocol.io)
[![MCP Dependency](https://img.shields.io/badge/MCP-mcp%20SDK-blue.svg)](requirements.txt)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](#)
[![Security Rating](https://img.shields.io/badge/Status-Grade_A_Production-success.svg)](#)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

OpenClaw GenPark agent skill with a standard-library core client and an MCP SDK server. Provides high-throughput deterministic execution, cryptographic security, and quantitative analysis via the Model Context Protocol (MCP).

---

## Architecture & Data Flow

```mermaid
flowchart TD
    Input[Incoming Agent Telemetry / Task Input] --> Core["OpenClawGenParkEnvoy"]
    Core --> Model[Mathematical Logic Engine]
    Model --> MCPResponse[Deterministic JSON Output / MCP Tool Result]
```

---

## MCP Runtime Requirements

Use Python 3.10+ for the MCP server. The core `client.py` has no external dependencies; MCP transport requires `mcp>=1.0.0,<2`. From this checkout, install it into the Python environment used by your MCP client:

```bash
python -m pip install -r requirements.txt
```

Use the same Python interpreter to launch `mcp_server.py`. In desktop client configuration, set `command` to that interpreter's absolute path.

## Quickstart & Usage

### 1. Direct Python Client Execution
```bash
python example_usage.py
```

### 2. Standalone MCP Server Launch
Run the MCP SDK server over STDIO:
```bash
python mcp_server.py
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
