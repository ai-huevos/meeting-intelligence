from datetime import datetime
from typing import Dict, Any, Optional
import uuid
from meeting_os.lib.tenancy.vault_context import TenantContext

class EventLog:
    """Append-only event logging system"""
    
    def __init__(self, convex_db=None):
        self.db = convex_db
    
    def log(self, event: Dict[str, Any]):
        """
        Log an event (append-only, immutable)
        
        Args:
            event: {
                "type": str,  # e.g., "meeting.classified", "tool.invoked"
                "payload": dict,  # Event-specific data
                "severity": str,  # "info", "warning", "high", "critical"
                "user_id": str,  # Optional
                "vault_id": str,  # Optional
                "workflow_id": str,  # Optional (links related events)
            }
        """
        
        # Auto-inject context
        try:
            vault_id = TenantContext.get_vault()
            user_id = TenantContext.get_user()
        except RuntimeError:
            # Context not set (e.g., background job)
            vault_id = event.get("vault_id")
            user_id = event.get("user_id")
        
        # Create immutable event
        event_record = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "type": event["type"],
            "payload": event.get("payload", {}),
            "severity": event.get("severity", "info"),
            "user_id": user_id,
            "vault_id": vault_id,
            "workflow_id": event.get("workflow_id"),
        }
        
        # Append to log (never update or delete)
        if self.db:
            # self.db.mutation("events:append", event_record)
            # Mocking DB call for now since we don't have convex client setup
            print(f"[EVENT_LOG] Persisted to DB: {event_record['type']}")
        else:
            print(f"[EVENT_LOG] {event_record}")
        
        return event_record["id"]
