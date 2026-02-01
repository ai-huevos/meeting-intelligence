from enum import Enum
from typing import Dict, Any, Optional, Literal, List
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

# --- Enums ---

class EventSource(str, Enum):
    FIREFLIES = "Fireflies"
    SLACK = "Slack"
    WHATSAPP = "WhatsApp"
    GOOGLE_CALENDAR = "GoogleCalendar"
    MANUAL = "Manual"

class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

# --- Sub-Models ---

class RoutingFlags(BaseModel):
    """Determines which Swarm Agents should be activated"""
    sales: bool = False
    product: bool = False
    customer_success: bool = False
    ops: bool = False
    finance: bool = False
    requires_human_review: bool = False

class ContextLayer(BaseModel):
    """The synthesized 'understanding' of the event"""
    summary: str
    sentiment: Literal["Positive", "Neutral", "Negative", "Urgent"] = "Neutral"
    topics: List[str] = Field(default_factory=list)
    entities: Dict[str, Any] = Field(default_factory=dict)  # { "people": [...], "companies": [...] }
    intent: Optional[str] = None
    next_steps: List[str] = Field(default_factory=list)

# --- Universal Context Object (UCO) ---

class UniversalContextObject(BaseModel):
    """
    The Standard Protocol for all Meeting OS events.
    Decouples input channels from processing logic.
    """
    event_id: str = Field(default_factory=lambda: f"evt_{uuid.uuid4().hex[:12]}")
    source: EventSource
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # The Brain
    routing_flags: RoutingFlags
    context_layer: ContextLayer
    
    # Audit & Replay
    raw_data: Optional[Dict[str, Any]] = None  # Original webhook payload
    metadata: Dict[str, Any] = Field(default_factory=dict)  # Server ver, Vault ID
    
    status: ProcessingStatus = ProcessingStatus.PENDING

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
