# Meeting OS: Observability & Reliability Specification

**Append-Only Logging, Idempotency & Regression Testing**  
**Version 1.0 | January 2026**

---

## EXECUTIVE SUMMARY

This specification defines the **observability architecture** for Meeting OS: append-only event logging, idempotent workflow execution, and automated regression testing.

### Critical Components

- **Event Log**: Append-only audit trail (immutable history)
- **Idempotent Workflows**: Safe re-execution with deduplication
- **Replay Testing**: Automated regression detection on new agent versions
- **Prompt Versioning**: Track all prompt changes over time
- **Model Tracing**: Log all LLM calls with inputs/outputs

---

## 1. APPEND-ONLY EVENT LOG

### Purpose

- **Audit trail**: Who did what, when, and why
- **Debugging**: Reconstruct exact sequence of events
- **Compliance**: Immutable evidence for audits
- **Analytics**: Business intelligence on system usage

### Implementation: `lib/observability/event_log.py`

```python
from datetime import datetime
from typing import Dict, Any, Optional
import uuid

class EventLog:
    """Append-only event logging system"""
    
    def __init__(self, convex_db):
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
        from lib.tenancy.vault_context import TenantContext
        
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
        self.db.mutation("events:append", event_record)
        
        return event_record["id"]
    
    def query_events(
        self,
        vault_id: str,
        event_type: Optional[str] = None,
        since: Optional[datetime] = None,
        limit: int = 100
    ):
        """Query events with filters"""
        return self.db.query("events:list", {
            "vault_id": vault_id,
            "event_type": event_type,
            "since": since.isoformat() if since else None,
            "limit": limit
        })
    
    def get_workflow_events(self, workflow_id: str):
        """Get all events for a workflow (reconstruct execution)"""
        return self.db.query("events:by_workflow", {
            "workflow_id": workflow_id
        })
    
    def get_security_events(
        self,
        vault_id: str,
        since: Optional[datetime] = None
    ):
        """Get security-related events"""
        return self.query_events(
            vault_id,
            event_type="security.*",  # Wildcard match
            since=since
        )
```

### Event Types

```python
# Standard event taxonomy
EVENT_TYPES = {
    # Workflows
    "workflow.started": "Workflow execution started",
    "workflow.completed": "Workflow completed successfully",
    "workflow.failed": "Workflow failed",
    
    # Meetings
    "meeting.received": "Fireflies webhook received",
    "meeting.classified": "Librarian classified meeting",
    "meeting.processed": "Domain agent processed meeting",
    
    # Tools
    "tool.invoked": "Agent invoked a tool",
    "tool.failed": "Tool invocation failed",
    
    # Security
    "security.input.injection_detected": "Prompt injection detected",
    "security.tool.not_allowed": "Unauthorized tool access",
    "security.approval.requested": "Approval requested",
    "security.approval.approved": "Approval granted",
    "security.approval.denied": "Approval denied",
    
    # Database
    "database.query": "Database queried",
    "database.create": "Record created",
    "database.update": "Record updated",
    
    # LLM
    "llm.call": "LLM API call made",
    "llm.response": "LLM response received",
}
```

### Usage Example

```python
event_logger = EventLog(convex_db)

def process_meeting_workflow(meeting_id: str):
    # Generate workflow ID
    workflow_id = str(uuid.uuid4())
    
    # Log workflow start
    event_logger.log({
        "type": "workflow.started",
        "payload": {
            "meeting_id": meeting_id,
            "workflow": "process_meeting"
        },
        "workflow_id": workflow_id
    })
    
    try:
        # Step 1: Classify
        domain = librarian_agent.classify(meeting_id)
        event_logger.log({
            "type": "meeting.classified",
            "payload": {
                "meeting_id": meeting_id,
                "domain": domain
            },
            "workflow_id": workflow_id
        })
        
        # Step 2: Process
        result = domain_agents[domain].process(meeting_id)
        event_logger.log({
            "type": "meeting.processed",
            "payload": {
                "meeting_id": meeting_id,
                "domain": domain,
                "result": result
            },
            "workflow_id": workflow_id
        })
        
        # Log success
        event_logger.log({
            "type": "workflow.completed",
            "payload": {
                "meeting_id": meeting_id
            },
            "workflow_id": workflow_id
        })
        
    except Exception as e:
        # Log failure
        event_logger.log({
            "type": "workflow.failed",
            "payload": {
                "meeting_id": meeting_id,
                "error": str(e),
                "traceback": traceback.format_exc()
            },
            "severity": "high",
            "workflow_id": workflow_id
        })
        raise
```

---

## 2. IDEMPOTENT WORKFLOWS

### Purpose

- **Safe retries**: Re-run workflows without side effects
- **Exactly-once execution**: Prevent duplicate operations
- **Recovery**: Resume from failures without duplication

### Implementation: `lib/observability/idempotent_workflow.py`

```python
from typing import Callable, Any
from datetime import datetime, timedelta
import hashlib

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
        existing = self.db.query("workflow_executions:get", {
            "key_hash": key_hash
        })
        
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
            self.db.mutation("workflow_executions:upsert", {
                "key_hash": key_hash,
                "workflow_id": workflow_id,
                "idempotency_key": idempotency_key,
                "vault_id": vault_id,
                "result": result,
                "status": "completed",
                "completed_at": datetime.utcnow().isoformat()
            })
            
            return result
            
        except Exception as e:
            # Store failure
            self.db.mutation("workflow_executions:upsert", {
                "key_hash": key_hash,
                "workflow_id": workflow_id,
                "idempotency_key": idempotency_key,
                "vault_id": vault_id,
                "status": "failed",
                "error": str(e),
                "failed_at": datetime.utcnow().isoformat()
            })
            raise
    
    def _is_expired(self, execution: dict, ttl: timedelta) -> bool:
        """Check if cached result is expired"""
        completed_at = datetime.fromisoformat(execution['completed_at'])
        return datetime.utcnow() - completed_at > ttl
```

### Usage Example

```python
idempotent = IdempotentWorkflow(convex_db, event_logger)

def process_meeting(meeting_id: str):
    # Wrap in idempotent execution
    return idempotent.execute(
        workflow_id="process_meeting",
        idempotency_key=f"meeting_{meeting_id}",
        workflow_fn=lambda: _process_meeting_internal(meeting_id)
    )

# Safe to call multiple times
result1 = process_meeting("meeting_123")
result2 = process_meeting("meeting_123")  # Returns cached result
assert result1 == result2
```

---

## 3. REGRESSION TESTING (REPLAY HARNESS)

### Purpose

- **Test new agent versions**: Ensure no regressions before deployment
- **Quantify impact**: Measure accuracy improvements/degradations
- **Catch edge cases**: Surface issues on real historical data

### Implementation: `lib/observability/replay_harness.py`

```python
from typing import List, Dict
from datetime import datetime

class ReplayHarness:
    """Test agent changes against historical data"""
    
    def __init__(self, convex_db, notion_client, agent_factory):
        self.db = convex_db
        self.notion = notion_client
        self.agent_factory = agent_factory
    
    def replay_meeting(
        self,
        meeting_id: str,
        agent_version: str = "current"
    ) -> Dict:
        """
        Replay meeting processing with specified agent version
        
        Returns:
            {
                "meeting_id": str,
                "original_result": dict,  # What production agent did
                "replay_result": dict,  # What new agent did
                "regression_score": float,  # 0.0-1.0 (1.0 = perfect match)
                "differences": list  # Detailed diff
            }
        """
        
        # Get original meeting data
        meeting = self.notion.pages.retrieve(meeting_id)
        original_classification = meeting['properties']['domain']['select']['name']
        original_entities = meeting['properties']['entities']['rich_text']
        
        # Get meeting transcript
        transcript = self._get_meeting_transcript(meeting_id)
        
        # Instantiate agent version
        agent = self.agent_factory.create(agent_version)
        
        # Replay classification
        replay_result = agent.classify(transcript)
        
        # Compare results
        differences = self._compute_diff(
            original={
                "domain": original_classification,
                "entities": original_entities
            },
            replay=replay_result
        )
        
        # Calculate regression score
        regression_score = self._calculate_regression_score(differences)
        
        return {
            "meeting_id": meeting_id,
            "original_result": {
                "domain": original_classification,
                "entities": original_entities
            },
            "replay_result": replay_result,
            "regression_score": regression_score,
            "differences": differences
        }
    
    def batch_replay(
        self,
        sample_size: int = 100,
        agent_version: str = "current",
        stratify_by_domain: bool = True
    ) -> Dict:
        """
        Replay multiple meetings and generate report
        
        Returns:
            {
                "total_replayed": int,
                "avg_regression_score": float,
                "domain_breakdown": dict,
                "critical_regressions": list,  # score < 0.7
                "overall_verdict": str  # "PASS" or "FAIL"
            }
        """
        
        # Sample meetings
        meetings = self._sample_meetings(sample_size, stratify_by_domain)
        
        results = []
        for meeting_id in meetings:
            result = self.replay_meeting(meeting_id, agent_version)
            results.append(result)
        
        # Aggregate statistics
        avg_score = sum(r['regression_score'] for r in results) / len(results)
        
        # Find critical regressions
        critical = [r for r in results if r['regression_score'] < 0.7]
        
        # Domain breakdown
        domain_scores = {}
        for result in results:
            domain = result['original_result']['domain']
            if domain not in domain_scores:
                domain_scores[domain] = []
            domain_scores[domain].append(result['regression_score'])
        
        domain_breakdown = {
            domain: sum(scores) / len(scores)
            for domain, scores in domain_scores.items()
        }
        
        # Verdict
        verdict = "PASS" if avg_score >= 0.85 and len(critical) == 0 else "FAIL"
        if avg_score >= 0.85 and len(critical) > 0:
            verdict = "PASS_WITH_WARNINGS"
        
        return {
            "total_replayed": len(results),
            "avg_regression_score": avg_score,
            "domain_breakdown": domain_breakdown,
            "critical_regressions": critical,
            "overall_verdict": verdict,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _compute_diff(self, original: dict, replay: dict) -> List[Dict]:
        """Compute differences between original and replay results"""
        diffs = []
        
        # Domain mismatch
        if original['domain'] != replay.get('domain'):
            diffs.append({
                "field": "domain",
                "original": original['domain'],
                "replay": replay.get('domain'),
                "severity": "high"
            })
        
        # Entity differences (simplified)
        original_entities = set([e['name'] for e in original.get('entities', [])])
        replay_entities = set([e['name'] for e in replay.get('entities', [])])
        
        missing = original_entities - replay_entities
        extra = replay_entities - original_entities
        
        if missing:
            diffs.append({
                "field": "entities",
                "type": "missing",
                "values": list(missing),
                "severity": "medium"
            })
        
        if extra:
            diffs.append({
                "field": "entities",
                "type": "extra",
                "values": list(extra),
                "severity": "low"
            })
        
        return diffs
    
    def _calculate_regression_score(self, differences: List[Dict]) -> float:
        """Calculate 0-1 score (1.0 = perfect match)"""
        if not differences:
            return 1.0
        
        # Weight by severity
        severity_weights = {
            "high": 0.4,
            "medium": 0.2,
            "low": 0.1
        }
        
        total_penalty = sum(
            severity_weights[diff['severity']]
            for diff in differences
        )
        
        return max(0.0, 1.0 - total_penalty)
    
    def _sample_meetings(
        self,
        sample_size: int,
        stratify_by_domain: bool
    ) -> List[str]:
        """Sample meetings for testing"""
        vault_id = TenantContext.get_vault()
        
        if stratify_by_domain:
            # Get equal samples from each domain
            domains = ["sales", "product", "customer_success", "finance"]
            per_domain = sample_size // len(domains)
            
            meeting_ids = []
            for domain in domains:
                domain_meetings = self.db.query("meetings:sample", {
                    "vault_id": vault_id,
                    "domain": domain,
                    "limit": per_domain
                })
                meeting_ids.extend([m['id'] for m in domain_meetings])
            
            return meeting_ids
        else:
            # Random sample
            meetings = self.db.query("meetings:sample", {
                "vault_id": vault_id,
                "limit": sample_size
            })
            return [m['id'] for m in meetings]
```

### Usage Example

```python
replay = ReplayHarness(convex_db, notion_client, agent_factory)

# Test new agent version
report = replay.batch_replay(
    sample_size=50,
    agent_version="v2.1.0",
    stratify_by_domain=True
)

print(f"Average Regression Score: {report['avg_regression_score']:.2f}")
print(f"Verdict: {report['overall_verdict']}")

if report['critical_regressions']:
    print("\n⚠️ Critical Regressions:")
    for reg in report['critical_regressions']:
        print(f"  - {reg['meeting_id']}: {reg['regression_score']:.2f}")
        for diff in reg['differences']:
            print(f"    {diff}")

# Example output:
# Average Regression Score: 0.92
# Verdict: PASS
```

---

## 4. PROMPT VERSIONING

### Purpose

- **Track prompt changes**: Know exactly what prompt was used
- **Rollback capability**: Revert to previous prompt version
- **A/B testing**: Compare prompt variants

### Implementation: `lib/observability/prompt_versioning.py`

```python
import hashlib
from datetime import datetime

class PromptVersionManager:
    """Manages prompt versions and tracks usage"""
    
    def __init__(self, convex_db, event_logger):
        self.db = convex_db
        self.event_logger = event_logger
    
    def register_prompt(
        self,
        name: str,
        template: str,
        metadata: dict = None
    ) -> str:
        """
        Register a prompt version
        
        Returns:
            version_id (hash of content)
        """
        
        # Hash prompt content
        version_id = hashlib.sha256(template.encode()).hexdigest()[:12]
        
        # Check if already exists
        existing = self.db.query("prompts:get", {
            "name": name,
            "version_id": version_id
        })
        
        if existing:
            return version_id
        
        # Store version
        self.db.mutation("prompts:create", {
            "name": name,
            "version_id": version_id,
            "template": template,
            "metadata": metadata or {},
            "created_at": datetime.utcnow().isoformat()
        })
        
        # Log
        self.event_logger.log({
            "type": "prompt.registered",
            "payload": {
                "name": name,
                "version_id": version_id
            }
        })
        
        return version_id
    
    def get_prompt(self, name: str, version_id: str = None) -> str:
        """Get prompt by name/version (latest if version not specified)"""
        
        if version_id:
            prompt = self.db.query("prompts:get", {
                "name": name,
                "version_id": version_id
            })
        else:
            # Get latest
            prompt = self.db.query("prompts:get_latest", {
                "name": name
            })
        
        if not prompt:
            raise ValueError(f"Prompt {name} (version {version_id}) not found")
        
        return prompt['template']
    
    def track_usage(self, name: str, version_id: str, meeting_id: str):
        """Track which prompt version was used for a meeting"""
        
        self.event_logger.log({
            "type": "prompt.used",
            "payload": {
                "prompt_name": name,
                "version_id": version_id,
                "meeting_id": meeting_id
            }
        })
```

### Usage Example

```python
prompt_manager = PromptVersionManager(convex_db, event_logger)

# Register prompt
LIBRARIAN_PROMPT_V1 = """
Classify this meeting into one domain: sales, product, customer_success, finance, other.

Meeting: {transcript}
"""

version_id = prompt_manager.register_prompt(
    "librarian_classify",
    LIBRARIAN_PROMPT_V1,
    metadata={"author": "user123", "description": "Initial version"}
)

# Use prompt
def classify_meeting(meeting_id: str):
    # Get latest prompt
    prompt_template = prompt_manager.get_prompt("librarian_classify")
    
    # Fill template
    prompt = prompt_template.format(transcript=get_transcript(meeting_id))
    
    # Call LLM
    response = llm_client.generate(prompt)
    
    # Track usage
    prompt_manager.track_usage("librarian_classify", version_id, meeting_id)
    
    return response
```

---

## 5. MODEL TRACING

### Purpose

- **Cost tracking**: Know exactly what each LLM call costs
- **Performance monitoring**: Track latency and failures
- **Debugging**: Inspect inputs/outputs for issues

### Implementation: `lib/observability/model_tracing.py`

```python
from datetime import datetime
import time

class ModelTracer:
    """Traces all LLM API calls"""
    
    # Model costs (per 1M tokens)
    MODEL_COSTS = {
        "claude-3-opus-20240229": {"input": 15.00, "output": 75.00},
        "claude-3-sonnet-20240229": {"input": 3.00, "output": 15.00},
        "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},
    }
    
    def __init__(self, event_logger):
        self.event_logger = event_logger
    
    def trace_llm_call(
        self,
        model: str,
        prompt: str,
        llm_client,
        max_tokens: int = 1024,
        temperature: float = 0.7
    ):
        """
        Wrap LLM call with tracing
        
        Returns:
            response (with cost and latency metadata)
        """
        
        vault_id = TenantContext.get_vault()
        call_id = str(uuid.uuid4())
        
        # Count input tokens (approximate)
        input_tokens = len(prompt) // 4  # ~4 chars per token
        
        # Log call start
        start_time = time.time()
        self.event_logger.log({
            "type": "llm.call",
            "payload": {
                "call_id": call_id,
                "model": model,
                "input_tokens": input_tokens,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "prompt_preview": prompt[:200]
            }
        })
        
        try:
            # Make LLM call
            response = llm_client.generate(
                model=model,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # Calculate cost
            output_tokens = len(response) // 4
            cost = self._calculate_cost(model, input_tokens, output_tokens)
            
            # Log response
            latency = time.time() - start_time
            self.event_logger.log({
                "type": "llm.response",
                "payload": {
                    "call_id": call_id,
                    "model": model,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "cost_usd": cost,
                    "latency_seconds": latency,
                    "response_preview": response[:200]
                }
            })
            
            # Return with metadata
            return {
                "response": response,
                "metadata": {
                    "call_id": call_id,
                    "cost_usd": cost,
                    "latency_seconds": latency
                }
            }
            
        except Exception as e:
            # Log failure
            self.event_logger.log({
                "type": "llm.failed",
                "payload": {
                    "call_id": call_id,
                    "model": model,
                    "error": str(e)
                },
                "severity": "high"
            })
            raise
    
    def _calculate_cost(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """Calculate cost in USD"""
        
        if model not in self.MODEL_COSTS:
            return 0.0
        
        costs = self.MODEL_COSTS[model]
        
        input_cost = (input_tokens / 1_000_000) * costs["input"]
        output_cost = (output_tokens / 1_000_000) * costs["output"]
        
        return input_cost + output_cost
```

### Usage Example

```python
tracer = ModelTracer(event_logger)

def classify_meeting(transcript: str):
    # Wrap LLM call
    result = tracer.trace_llm_call(
        model="claude-3-sonnet-20240229",
        prompt=transcript,
        llm_client=anthropic_client
    )
    
    print(f"Cost: ${result['metadata']['cost_usd']:.4f}")
    print(f"Latency: {result['metadata']['latency_seconds']:.2f}s")
    
    return result['response']
```

---

## 6. MONITORING DASHBOARD

### Key Metrics

```python
def get_observability_dashboard(vault_id: str, period: str = "day"):
    """Generate observability dashboard data"""
    
    since = datetime.utcnow() - timedelta(days=1 if period == "day" else 7)
    
    # Get all events
    events = event_logger.query_events(vault_id, since=since)
    
    return {
        "period": period,
        "total_events": len(events),
        
        # Workflow metrics
        "workflows": {
            "total": len([e for e in events if e['type'].startswith('workflow.')]),
            "completed": len([e for e in events if e['type'] == 'workflow.completed']),
            "failed": len([e for e in events if e['type'] == 'workflow.failed']),
        },
        
        # LLM metrics
        "llm": {
            "total_calls": len([e for e in events if e['type'] == 'llm.call']),
            "total_cost_usd": sum(
                e['payload'].get('cost_usd', 0)
                for e in events
                if e['type'] == 'llm.response'
            ),
            "avg_latency_seconds": statistics.mean([
                e['payload']['latency_seconds']
                for e in events
                if e['type'] == 'llm.response'
            ]),
        },
        
        # Security metrics
        "security": {
            "injection_attempts": len([
                e for e in events
                if e['type'] == 'security.input.injection_detected'
            ]),
            "unauthorized_tool_access": len([
                e for e in events
                if e['type'] == 'security.tool.not_allowed'
            ]),
            "approval_requests": len([
                e for e in events
                if e['type'] == 'security.approval.requested'
            ]),
        }
    }
```

---

**This is Part 2 of 3. Continue to cost_mcp_growth_spec.md for cost controls, MCP integration, and growth agents.**
