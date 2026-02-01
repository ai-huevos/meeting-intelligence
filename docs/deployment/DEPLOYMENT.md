# Deployment Guide (Safe Production)

## 1. Environment & Secrets
**Crucial**: Never commit `.env`, `credentials.json`, or `token.json` to Git.

### Required Environment Variables (Production)
Set these in your Render/Cloud dashboard:

| Variable | Description |
|---|---|
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_KEY` | Service Role Key (Server-side only) |
| `OPENAI_API_KEY` | For LLM logic |
| `PERPLEXITY_API_KEY` | For Research Agent |
| `FIREFLIES_API_KEY` | For Meeting Transcripts |
| `KAPSO_API_KEY` | For WhatsApp integration |
| `WHATSAPP_PHONE_ID` | From Meta/Kapso |

### Google Calendar Auth
The `token.json` is generated interactively. For production:
1.  **Option A (Recommended)**: Implement a proper OAuth flow (Web Server flow) storing tokens in Supabase DB, not a file.
2.  **Option B (Simple)**: Generate `token.json` locally, encode it (base64), store it as a secret env var `GOOGLE_TOKEN_BASE64`, and have the app write it to disk on startup.

## 2. Render Deployment

This project includes a `render.yaml` for Blueprint deployment.

1.  **Connect Repo**: Link `https://github.com/ai-huevos/meeting-intelligence`.
2.  **Service**: It defines a `n8n-meeting-os` web service (Docker).
    *   *Note*: The current `render.yaml` points to `n8nio/n8n:latest`. Verify if you are deploying the Python app or N8N.
    *   **If deploying the Python App**: Update `render.yaml` to build from `Dockerfile` (create one) or use Python Environment.

### Python Dockerfile Example
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "scripts/run_daily_prep.py"] # Or your main entrypoint
```

## 3. Database Migrations
Run migrations manually or via a startup script:
```bash
python scripts/schema_deployer.py
```

## 4. MCP Server Validation
The MCP server (`meeting_os/mcp_server.py`) requires `fastmcp` (Python 3.10+). Ensure your production container meets this requirement if you plan to host the MCP server remotely (via SSE/WebSockets).
