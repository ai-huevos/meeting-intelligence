# Webhook Setup Guide - Kapso & Notion

**Last Updated:** 2026-02-01  
**Status:** Ready for Configuration

---

## Overview

This guide covers webhook configuration for:
1. **Kapso (WhatsApp)** - Receive incoming messages
2. **Notion** - Receive database change notifications (optional)
3. **Fireflies.ai** - Receive transcript notifications (optional)

---

## 🔧 Current Configuration Status

### Environment Variables (Verified in `.env`)
```bash
✅ NOTION_API_KEY=<your-notion-api-key>
✅ NOTION_PARENT_PAGE_ID=<your-parent-page-id>
✅ KAPSO_API_KEY=<your-kapso-api-key>
✅ WHATSAPP_PHONE_ID=<your-phone-id>
```

### MCP Server Status
```bash
❌ MCP Server: NOT RUNNING
   To start: python3 meeting_os/mcp_server.py
   (Requires Python 3.10+ and fastmcp)
```

---

## 1. Kapso (WhatsApp) Webhook Configuration 📱

### What Kapso Does
Kapso is a proxy service for Meta's WhatsApp Cloud API that allows your system to:
- **Receive** incoming WhatsApp messages (via webhook)
- **Send** WhatsApp messages (via API)

### A. Your Current Kapso Setup

**API Endpoint (for sending):**
```
POST https://api.kapso.ai/meta/whatsapp/v24.0/{PHONE_ID}/messages
```

**Headers:**
```json
{
  "X-API-Key": "<your-kapso-api-key>",
  "Content-Type": "application/json"
}
```

**Your Phone ID:** `597907523413541`

### B. Webhook Configuration (Receiving Messages)

#### Step 1: Deploy Your FastAPI Server

First, ensure your FastAPI server is publicly accessible:

**Option A: Cloud Run (Recommended)**
```bash
# Deploy to Google Cloud Run
gcloud run deploy meeting-os \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --dockerfile deployment/docker/Dockerfile

# You'll get a URL like:
# https://meeting-os-xxxx-uc.a.run.app
```

**Option B: ngrok (Testing)**
```bash
# Start your local server
python3 main.py  # Runs on port 8080

# In another terminal, expose with ngrok
ngrok http 8080

# You'll get a URL like:
# https://abc123.ngrok.io
```

#### Step 2: Configure Webhook in Kapso Dashboard

1. **Log in to Kapso Dashboard** → https://dashboard.kapso.ai/
2. **Navigate to:** WhatsApp → Settings → Webhooks
3. **Set Webhook URL:**
   ```
   https://YOUR-DOMAIN.com/webhook/kapso
   ```
   Replace `YOUR-DOMAIN.com` with your Cloud Run URL or ngrok URL

4. **Set Verification Token:** (if required)
   ```
   Use any random string, then add to .env:
   KAPSO_VERIFY_TOKEN=your_random_token_here
   ```

5. **Subscribe to Events:**
   - ✅ `messages` - Incoming messages
   - ✅ `message_status` - Delivery status (optional)

#### Step 3: Add Webhook Handler to main.py

We need to add a Kapso-specific endpoint. Let me create an updated main.py:

```python
# Add this to main.py after the existing /webhook endpoint

@app.post("/webhook/kapso")
async def handle_kapso_webhook(request: Request):
    """
    Webhook handler for Kapso/WhatsApp incoming messages.
    Expects Meta WhatsApp webhook format.
    """
    try:
        payload = await request.json()
        
        # Parse the incoming message using KapsoClient
        from meeting_os.services.kapso_handler import KapsoClient
        kapso = KapsoClient()
        
        message_data = kapso.handle_incoming_message(payload)
        
        if not message_data:
            return {"status": "ignored", "reason": "No message in payload"}
        
        # Create UCO and route to Router Agent
        from meeting_os.core.uco import UniversalContextObject, EventSource, RoutingFlags, ContextLayer
        
        uco = UniversalContextObject(
            source=EventSource.WHATSAPP,
            routing_flags=RoutingFlags(ops=True),  # Default to Ops agent
            context_layer=ContextLayer(
                summary=message_data['text'],
                sentiment="Neutral"
            ),
            raw_data=payload,
            metadata={
                "sender_phone": message_data['sender'],
                "timestamp": message_data['timestamp'],
                "platform": "whatsapp"
            }
        )
        
        result = router_agent.ingest_event(uco)
        
        return {
            "status": "success", 
            "event_id": result['event_id'],
            "routed_to": result['routes']
        }
        
    except Exception as e:
        print(f"❌ Kapso webhook error: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/webhook/kapso")
async def verify_kapso_webhook(request: Request):
    """
    Webhook verification for Kapso/Meta.
    Meta sends a GET request with hub.mode, hub.verify_token, hub.challenge.
    """
    verify_token = os.getenv("KAPSO_VERIFY_TOKEN", "default_verify_token")
    
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    if mode == "subscribe" and token == verify_token:
        print("✅ Kapso webhook verified!")
        return int(challenge)  # Meta expects the challenge back
    else:
        return {"status": "error", "message": "Verification failed"}, 403
```

#### Step 4: Test the Webhook

**Test with curl:**
```bash
# Test verification (GET)
curl "https://YOUR-DOMAIN.com/webhook/kapso?hub.mode=subscribe&hub.verify_token=your_token&hub.challenge=12345"

# Should return: 12345

# Test message handling (POST)
curl -X POST https://YOUR-DOMAIN.com/webhook/kapso \
  -H "Content-Type: application/json" \
  -d '{
    "entry": [{
      "changes": [{
        "value": {
          "messages": [{
            "from": "1234567890",
            "text": {"body": "Hello from WhatsApp!"},
            "timestamp": "1234567890",
            "type": "text"
          }]
        }
      }]
    }]
  }'
```

---

## 2. Notion Webhook Configuration 📝

### What Notion Webhooks Do
Notion doesn't have traditional webhooks, but you can:
1. **Poll for changes** using the Notion API
2. **Use Zapier/n8n** as a webhook proxy
3. **Use our existing integration** (write-only, no webhook needed)

### Current Notion Integration

Your system **writes to Notion** but doesn't listen for changes. This is the expected pattern for Meeting OS:

**Write Flow:**
```
Meeting OS → Router Agent → Notion API → Create/Update Pages
```

### If You Want Notion → Meeting OS Updates

**Option A: Polling (Simple)**
Create a cron job that checks for Notion page updates:

```bash
# Add to scripts/poll_notion.py
python3 scripts/poll_notion.py  # Run every 15 minutes
```

**Option B: Zapier/n8n Bridge (Recommended)**

1. Create a Zapier/n8n workflow:
   ```
   Trigger: Notion Database Item Updated
   Action: Webhook POST to https://YOUR-DOMAIN.com/webhook/notion
   ```

2. Add handler to main.py:
   ```python
   @app.post("/webhook/notion")
   async def handle_notion_webhook(request: Request):
       payload = await request.json()
       # Process Notion update
       return {"status": "received"}
   ```

**Option C: No Webhook Needed (Current)**
- Meeting OS only **writes** to Notion (CRM updates, logs)
- No need for Notion to trigger Meeting OS
- This is the **recommended pattern** for your use case

---

## 3. Fireflies.ai Webhook Configuration 🎤

### Purpose
Receive notifications when new meeting transcripts are ready.

### Configuration Steps

1. **Log in to Fireflies.ai** → Settings → Integrations
2. **Find Webhook Settings**
3. **Set Webhook URL:**
   ```
   https://YOUR-DOMAIN.com/webhook/fireflies
   ```
4. **Select Events:**
   - ✅ `transcription.completed` - When transcript is ready
   - ✅ `transcription.updated` - When transcript is edited

### Add Handler to main.py

```python
@app.post("/webhook/fireflies")
async def handle_fireflies_webhook(request: Request):
    """
    Webhook handler for Fireflies.ai transcript notifications.
    """
    try:
        payload = await request.json()
        
        # Extract transcript data
        meeting_id = payload.get("meeting_id")
        transcript_url = payload.get("transcript_url")
        
        # Fetch full transcript
        from meeting_os.services.fireflies import FirefliesClient
        fireflies = FirefliesClient()
        transcript_data = fireflies.fetch_transcript(meeting_id)
        
        if not transcript_data:
            return {"status": "error", "message": "Could not fetch transcript"}
        
        # Create UCO and route
        from meeting_os.core.uco import UniversalContextObject, EventSource, RoutingFlags, ContextLayer
        
        uco = UniversalContextObject(
            source=EventSource.FIREFLIES,
            routing_flags=RoutingFlags(sales=True),  # Default to Sales agent
            context_layer=ContextLayer(
                summary=transcript_data.get("summary", "Meeting transcript"),
                sentiment="Neutral"
            ),
            raw_data=transcript_data,
            metadata={
                "meeting_id": meeting_id,
                "transcript_url": transcript_url
            }
        )
        
        result = router_agent.ingest_event(uco)
        
        return {
            "status": "success",
            "event_id": result['event_id'],
            "routed_to": result['routes']
        }
        
    except Exception as e:
        print(f"❌ Fireflies webhook error: {e}")
        return {"status": "error", "message": str(e)}
```

---

## 4. Starting the MCP Server 🖥️

### Current Status
❌ **MCP Server is NOT running**

### What the MCP Server Does
Exposes Meeting OS tools to Claude Desktop:
- `search_transcripts(keyword)` - Search meeting history
- `get_transcript(meeting_id)` - Retrieve full transcript
- `trigger_agent_workflow(agent, context)` - Manually trigger agents

### How to Start

#### Option 1: Local (Requires Python 3.10+)

```bash
# Install fastmcp (requires Python 3.10+)
pip install fastmcp

# Run the server
python3 meeting_os/mcp_server.py
```

#### Option 2: Docker (Recommended for Production)

```bash
# Build MCP server container
docker build -f deployment/docker/Dockerfile.mcp -t meeting-os-mcp .

# Run the server
docker run -p 5000:5000 --env-file .env meeting-os-mcp
```

#### Option 3: Configure in Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "meeting-os": {
      "command": "python3",
      "args": [
        "/Users/tatooine/Documents/Development/tbd/meeting_os/mcp_server.py"
      ],
      "env": {
        "PYTHONPATH": "/Users/tatooine/Documents/Development/tbd"
      }
    }
  }
}
```

**Note:** This requires Python 3.10+ and `fastmcp` installed globally.

---

## 5. Complete Webhook Summary 📋

| Service | Webhook URL | Method | Purpose | Status |
|---------|-------------|--------|---------|--------|
| **Kapso (WhatsApp)** | `/webhook/kapso` | POST | Receive WhatsApp messages | ⚠️ Needs implementation |
| **Kapso Verification** | `/webhook/kapso` | GET | Verify webhook setup | ⚠️ Needs implementation |
| **Fireflies.ai** | `/webhook/fireflies` | POST | Receive transcript notifications | ⚠️ Optional |
| **Notion** | `/webhook/notion` | POST | Receive Notion updates | ❌ Not needed (write-only) |
| **Health Check** | `/` | GET | Verify server is running | ✅ Working |
| **Generic Webhook** | `/webhook` | POST | Fallback handler | ✅ Working |

---

## 6. Next Steps - Implementation Checklist ✅

### Immediate (Required for Kapso)
- [ ] Deploy FastAPI to Cloud Run or expose with ngrok
- [ ] Add `/webhook/kapso` POST and GET handlers to `main.py`
- [ ] Configure Kapso webhook URL in Kapso dashboard
- [ ] Add `KAPSO_VERIFY_TOKEN` to `.env`
- [ ] Test webhook with curl

### Optional (for complete setup)
- [ ] Add `/webhook/fireflies` handler if using Fireflies
- [ ] Start MCP server for Claude Desktop integration
- [ ] Set up monitoring for webhook failures
- [ ] Add webhook signature verification for security

### For Production
- [ ] Add webhook signature verification (HMAC)
- [ ] Implement rate limiting
- [ ] Add retry logic for failed webhook processing
- [ ] Set up monitoring/alerting (e.g., Sentry)
- [ ] Add webhook queue (e.g., Redis/Celery) for async processing

---

## 7. Testing Your Webhooks 🧪

### Test Kapso Webhook
```bash
# 1. Start your server
python3 main.py

# 2. Send test message
curl -X POST http://localhost:8080/webhook/kapso \
  -H "Content-Type: application/json" \
  -d @scripts/test_data/kapso_webhook_sample.json

# 3. Check logs for UCO creation and routing
```

### Test End-to-End Flow
```bash
# 1. Send WhatsApp message to your Kapso number
# 2. Check server logs for incoming webhook
# 3. Verify UCO created in Supabase
# 4. Verify routing to correct agent
# 5. Verify response sent back to WhatsApp
```

---

## 8. Troubleshooting 🔧

### Webhook not receiving messages
```bash
# Check if server is accessible
curl https://YOUR-DOMAIN.com/

# Check Kapso dashboard for webhook status
# Should show "Connected" with green checkmark

# Check server logs
tail -f logs/meeting-os.log
```

### MCP Server not starting
```bash
# Check Python version
python3 --version  # Should be 3.10+

# Install fastmcp
pip install fastmcp

# Test in fallback mode
python3 meeting_os/mcp_server.py
# Should show "Running in TEST mode" if fastmcp missing
```

### Messages not routing correctly
```bash
# Check EventLog in Supabase
SELECT * FROM event_logs ORDER BY timestamp DESC LIMIT 10;

# Check UCO table
SELECT * FROM universal_context_objects ORDER BY created_at DESC LIMIT 10;
```

---

## Need Help?

- **Kapso Documentation:** https://docs.kapso.ai/
- **Meta WhatsApp API:** https://developers.facebook.com/docs/whatsapp
- **Notion API:** https://developers.notion.com/
- **FastMCP:** https://github.com/jlowin/fastmcp

---

**Status:** Ready to implement Kapso webhook. Notion webhooks not needed for current use case.
