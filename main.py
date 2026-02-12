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
    return {"status": "active", "service": "Meeting OS", "version": "1.0"}

@app.post("/webhook")
async def handle_webhook(payload: WebhookPayload):
    """
    Generic Webhook Handler (Legacy, for backward compatibility).
    Routes payload to the Router Agent.
    """
    print(f"Received webhook from {payload.source}: {payload.message}")
    
    # Create UCO and route
    from meeting_os.core.uco import UniversalContextObject, EventSource, RoutingFlags, ContextLayer
    
    uco = UniversalContextObject(
        source=EventSource.MANUAL,
        routing_flags=RoutingFlags(ops=True),
        context_layer=ContextLayer(
            summary=payload.message,
            sentiment="Neutral"
        ),
        metadata={
            "sender": payload.sender,
            "source": payload.source
        }
    )
    
    result = router_agent.ingest_event(uco)
    
    return {"status": "received", "action": "routed_to_agent", "event_id": result['event_id']}

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
    Webhook verification for Kapso/Meta WhatsApp.
    Meta sends a GET request with hub.mode, hub.verify_token, hub.challenge.
    """
    verify_token = os.getenv("KAPSO_VERIFY_TOKEN", "default_verify_token_change_me")
    
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    if mode == "subscribe" and token == verify_token:
        print("✅ Kapso webhook verified!")
        return int(challenge)  # Meta expects the challenge back as an integer
    else:
        print(f"❌ Kapso webhook verification failed. Mode: {mode}, Token match: {token == verify_token}")
        return {"status": "error", "message": "Verification failed"}, 403

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
        transcript_text = payload.get("transcript", "")
        
        if not meeting_id:
            return {"status": "error", "message": "Missing meeting_id"}
        
        # Create UCO and route
        from meeting_os.core.uco import UniversalContextObject, EventSource, RoutingFlags, ContextLayer
        
        uco = UniversalContextObject(
            source=EventSource.FIREFLIES,
            routing_flags=RoutingFlags(sales=True),  # Default to Sales agent for meeting analysis
            context_layer=ContextLayer(
                summary=f"New transcript from meeting {meeting_id}",
                sentiment="Neutral"
            ),
            raw_data=payload,
            metadata={
                "meeting_id": meeting_id,
                "transcript_url": transcript_url,
                "transcript_length": len(transcript_text)
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

@app.post("/transcript")
async def handle_transcript(payload: TranscriptPayload):
    """
    Direct transcript ingestion endpoint (alternative to webhook).
    Ingest transcripts from Fireflies.ai or other sources via API call.
    """
    try:
        print(f"Processing transcript for meeting {payload.meeting_id}")
        
        # Create UCO and route
        from meeting_os.core.uco import UniversalContextObject, EventSource, RoutingFlags, ContextLayer
        
        uco = UniversalContextObject(
            source=EventSource.FIREFLIES,
            routing_flags=RoutingFlags(sales=True),
            context_layer=ContextLayer(
                summary=payload.transcript_text[:200],  # First 200 chars as summary
                sentiment="Neutral"
            ),
            raw_data={"transcript": payload.transcript_text},
            metadata={
                "meeting_id": payload.meeting_id,
                "transcript_length": len(payload.transcript_text)
            }
        )
        
        result = router_agent.ingest_event(uco)
        
        return {
            "status": "processing", 
            "meeting_id": payload.meeting_id,
            "event_id": result['event_id'],
            "routed_to": result['routes']
        }
    except Exception as e:
        print(f"❌ Transcript processing error: {e}")
        return {"status": "error", "message": str(e)}

# --- Entry Point ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"🚀 Starting Meeting OS on port {port}")
    print(f"📡 Webhook endpoints:")
    print(f"   - POST /webhook (generic)")
    print(f"   - POST /webhook/kapso (WhatsApp)")
    print(f"   - GET  /webhook/kapso (WhatsApp verification)")
    print(f"   - POST /webhook/fireflies (Transcripts)")
    print(f"   - POST /transcript (Direct transcript API)")
    print(f"   - GET  / (Health check)")
    uvicorn.run(app, host="0.0.0.0", port=port)
