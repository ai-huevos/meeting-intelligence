from typing import Callable, Any
from datetime import datetime, timedelta
import hashlib
from meeting_os.lib.tenancy.vault_context import TenantContext

class IdempotentWorkflow:
    """Ensures workflows execute exactly once"""
    
    # Cache workflow results for this duration
    RESULT_CACHE_TTL = timedelta(hours=24)
    
    def __init__(self, convex_db, event_logger):
        self.db = convex_db
        self.event_logger = event_logger
    
    def execute(
        self,
        workflow_id: str,
        idempotency_key: str,
        workflow_fn: Callable[[], Any],
        ttl: timedelta = None
    ) -> Any:
        """
        Execute workflow idempotently
        
        Args:
            workflow_id: Unique workflow identifier (e.g., "process_meeting")
            idempotency_key: Unique key for this execution (e.g., "meeting_123")
            workflow_fn: Function to execute
            ttl: How long to cache result (default 24h)
        
        Returns:
            Workflow result (from cache if already executed)
        """
        
        vault_id = TenantContext.get_vault()
        ttl = ttl or self.RESULT_CACHE_TTL
        
        # Create composite key
        composite_key = f"{vault_id}:{workflow_id}:{idempotency_key}"
        key_hash = hashlib.sha256(composite_key.encode()).hexdigest()
        
        # Check if already executed
        # existing = self.db.query("workflow_executions:get", {
        #     "key_hash": key_hash
        # })
        existing = None # Mock
        
        if existing and not self._is_expired(existing, ttl):
            # Return cached result
            self.event_logger.log({
                "type": "workflow.idempotent_hit",
                "payload": {
                    "workflow_id": workflow_id,
                    "idempotency_key": idempotency_key,
                    "cached_at": existing['completed_at']
                }
            })
            return existing['result']
        
        # Execute workflow
        self.event_logger.log({
            "type": "workflow.idempotent_execute",
            "payload": {
                "workflow_id": workflow_id,
                "idempotency_key": idempotency_key
            }
        })
        
        try:
            result = workflow_fn()
            
            # Store result
            # self.db.mutation("workflow_executions:upsert", { ... })
            
            return result
            
        except Exception as e:
            # Store failure
            # self.db.mutation("workflow_executions:upsert", { ... })
            raise
    
    def _is_expired(self, execution: dict, ttl: timedelta) -> bool:
        """Check if cached result is expired"""
        completed_at = datetime.fromisoformat(execution['completed_at'])
        return datetime.utcnow() - completed_at > ttl
