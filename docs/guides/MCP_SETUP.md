# MCP Server Setup Guide

This project includes a custom MCP (Model Context Protocol) server (`meeting_os/mcp_server.py`) that exposes MeetingOS capabilities to Claude Desktop and other MCP clients.

## 1. Prerequisites

- **Python 3.10+**: Required for `fastmcp`. The current project uses Python 3.9, so you may need a separate venv or container for the MCP server if you run it locally.
- **FastMCP**: Install via pip:
  ```bash
  pip install fastmcp
  ```

## 2. Configuration (Claude Desktop)

To use the MeetingOS MCP server with Claude Desktop, add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "meeting-os": {
      "command": "python3",
      "args": [
        "/absolute/path/to/meeting-intelligence/meeting_os/mcp_server.py"
      ],
      "env": {
        "PYTHONPATH": "/absolute/path/to/meeting-intelligence"
      }
    }
  }
}
```

## 3. Supported Tools

The server exposes the following tools:

- `search_transcripts(keyword: str)`: Search for recent meetings by keyword.
- `get_transcript(meeting_id: str)`: Retrieve full transcript text.
- `trigger_agent_workflow(agent_name: str, context: str)`: Trigger a background agent workflow (Sales, Research, Ops).

## 4. Testing the Server

You can test the server logic without Claude by running:

```bash
python3 meeting_os/mcp_server.py
```

If `fastmcp` is not installed, it will run in "Test Mode" and print example outputs.

## 5. Additional Recommended Servers

For a complete "Meeting Intelligence" experience, we recommend adding these standard servers:

1.  **Filesystem**: To read logs and transcripts directly.
2.  **PostgreSQL (Supabase)**: To query the structured database directly.
    ```json
    "supabase-db": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://user:pass@host:5432/postgres"]
    }
    ```
