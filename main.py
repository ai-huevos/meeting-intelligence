from fastapi import FastAPI, Request
from pydantic import BaseModel
import os
import uvicorn

# Initialize FastAPI
app = FastAPI(title="Meeting OS Intelligence", version="1.0")

# --- Models ---
class WebhookPayload(BaseModel):
    message: str
    sender: str
    source: str = "unknown"

class TranscriptPayload(BaseModel):
    meeting_id: str
    transcript_text: str

# --- Routes ---

from meeting_os.agents.router_agent import RouterAgent

# Initialize Core Services
router_agent = RouterAgent()

@app.get("/")
def health_check():
    """Health check endpoint for Cloud Run."""
    return {"status": "active", "service": "Meeting OS"}

@app.post("/webhook")
async def handle_webhook(payload: WebhookPayload):
    """
    Unified Webhook Handler (Kapso, Slack, etc.)
    Routes payload to the Router Agent.
    """
    print(f"Received webhook from {payload.source}: {payload.message}")
    
    # Delegate to Router (which logs to Notion)
    # Mocking 'processing_result' for now as we don't have the full pipeline connecting main -> agents -> response
    # In a real flow, 'payload' would go to an agent, which produces a result, which goes to Router.
    # Here we treat the incoming message as a "result" to be routed/logged.
    
    router_agent.route_result(
        meeting_data={"id": "webhook-event", "title": f"Message from {payload.sender}"},
        processing_result={
            "domain": "Kapso" if payload.source == "whatsapp" else "General",
            "summary": payload.message
        }
    )
    
    return {"status": "received", "action": "routed_to_agent"}

@app.post("/transcript")
async def handle_transcript(payload: TranscriptPayload):
    """
    Ingest transcripts from Fireflies.ai or other sources.
    """
    print(f"Processing transcript for meeting {payload.meeting_id}")
    return {"status": "processing", "meeting_id": payload.meeting_id}

# --- Entry Point ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
