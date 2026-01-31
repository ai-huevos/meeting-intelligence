from meeting_os.lib.observability.event_log import EventLog
from meeting_os.lib.integrations.slack import SlackClient
from meeting_os.lib.integrations.notion import NotionHandler
from meeting_os.lib.schema.uco import UniversalContextObject, RoutingFlags, EventSource
from meeting_os.lib.db import db
import json
import logging

logger = logging.getLogger("RouterAgent")

class RouterAgent:
    """
    The Central Nervous System.
    Ingests Universal Context Objects (UCOs), persists them, and dispatches to Swarms.
    """
    
    def __init__(self, slack_client=None, event_log=None, notion_handler=None, db_client=None):
        self.slack = slack_client or SlackClient()
        self.event_log = event_log or EventLog()
        self.notion = notion_handler or NotionHandler()
        self.db = db_client or db

    def ingest_event(self, uco: UniversalContextObject) -> dict:
        """
        Main Entry Point.
        1. Validates UCO (implicit via Pydantic typing)
        2. Persists to Immutable Log (Supabase)
        3. Routes to Swarms
        """
        
        # 1. Persist UCO to Supabase
        self._persist_uco(uco)
        
        # 2. Log Ingestion
        self.event_log.log({
            "type": "router.ingest",
            "payload": {
                "event_id": uco.event_id,
                "source": uco.source,
                "flags": uco.routing_flags.dict()
            },
            "vault_id": uco.metadata.get("vault_id", "default")
        })

        # 3. Dynamic Routing
        routes_triggered = []
        
        if uco.routing_flags.sales:
            self._dispatch_sales_agent(uco)
            routes_triggered.append("Sales")
            
        if uco.routing_flags.product:
            self._dispatch_product_agent(uco)
            routes_triggered.append("Product")
            
        if uco.routing_flags.ops:
            self._dispatch_ops_agent(uco)
            routes_triggered.append("Ops")

        # 4. Notify Human (The "Push" Principle)
        self._notify_slack(uco, routes_triggered)
        
        return {"status": "routed", "routes": routes_triggered, "event_id": uco.event_id}

    def _persist_uco(self, uco: UniversalContextObject):
        """Writes the UCO to the `universal_context_objects` table."""
        try:
            if self.db.client:
                # Convert to dict, handle enums/datetimes via json_encoders or model_dump
                payload = uco.model_dump(mode='json')
                
                # Reshape for SQL schema
                record = {
                    "event_id": payload["event_id"],
                    "source": payload["source"],
                    "created_at": payload["timestamp"],
                    "routing_flags": payload["routing_flags"],
                    "context_layer": payload["context_layer"],
                    "raw_data": payload.get("raw_data"),
                    "status": "processed"
                }
                
                self.db.table("universal_context_objects").upsert(record).execute()
        except Exception as e:
            logger.error(f"Failed to persist UCO: {e}")
            # Don't crash processing, just log error
            self.event_log.log({
                "type": "router.persist_failed", 
                "payload": {"error": str(e)}, 
                "severity": "error"
            })

    def _dispatch_sales_agent(self, uco: UniversalContextObject):
        """Mock dispatch to Sales Swarm"""
        print(f"🚀 [Router] Dispatching {uco.event_id} to SALES Agent")
        # In real code: SalesAgent.process(uco)
        
    def _dispatch_product_agent(self, uco: UniversalContextObject):
        """Mock dispatch to Product Swarm"""
        print(f"🚀 [Router] Dispatching {uco.event_id} to PRODUCT Agent")

    def _dispatch_ops_agent(self, uco: UniversalContextObject):
        """Mock dispatch to Ops Swarm"""
        print(f"🚀 [Router] Dispatching {uco.event_id} to OPS Agent")

    def _notify_slack(self, uco: UniversalContextObject, routes: list):
        """Sends a Bio-chromatic Block Kit message"""
        try:
            from meeting_os.lib.ui.slack_blocks import BioChromaticUI
            
            # Generate Neon Card
            payload = BioChromaticUI.render_ingestion_card(uco, routes)
            
            # Determine channel based on primary route
            channel = "#sales-leads" if "Sales" in routes else "#general"
            
            # Send using real client
            self.slack.send_message(
                text=f"New Context: {uco.context_layer.summary}", # Fallback text for notifications
                channel=channel,
                attachments=payload.get("attachments"),
                blocks=payload.get("blocks"), # Just in case we switch to blocks later
                username=payload.get("username"),
                icon_emoji=payload.get("icon_emoji")
            )
            
            print(f"🎨 [UI] Sent Bio-chromatic Payload to {channel}")
            # print(json.dumps(payload, indent=2))
            
        except Exception as e:
            logger.error(f"Failed to render UI: {e}")
            self.slack.send_message(f"Error rendering UI: {e}", channel="#debug")

if __name__ == "__main__":
    # Test with a Mock UCO
    from meeting_os.lib.schema.uco import ContextLayer
    
    router = RouterAgent()
    
    mock_uco = UniversalContextObject(
        source=EventSource.FIREFLIES,
        routing_flags=RoutingFlags(sales=True),
        context_layer=ContextLayer(
            summary="Client wants to buy the Enterprise plan.",
            sentiment="Positive"
        ),
        metadata={"vault_id": "test_vault"}
    )
    
    router.ingest_event(mock_uco)
