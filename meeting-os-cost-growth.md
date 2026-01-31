# Meeting OS: Cost, MCP & Growth Agents Specification

**Budget Controls, MCP Integration & Growth Automation**  
**Version 1.0 | January 2026**

---

## EXECUTIVE SUMMARY

This specification defines **cost control systems**, **MCP (Model Context Protocol) integration**, and **growth agents** for Meeting OS production deployment.

### Critical Components

- **Cost Controller**: Hard budget limits ($50/day per vault)
- **Model Router**: Intelligent model selection for cost optimization
- **MCP Manager**: Configure and secure external tool integrations
- **Credential Manager**: OAuth token management with auto-refresh
- **Growth Agents**: Pipeline risk detection & messaging insights

---

## 1. COST CONTROL SYSTEM

### Budget Requirements

**Target**: $50/day per vault = $1,500/month

**Breakdown**:
- 50 meetings/day
- ~2 LLM calls per meeting (classification + extraction)
- Average 3,000 tokens per call
- Use Sonnet for most tasks, Haiku for simple tasks

**Model Selection Strategy**:
```
Simple tasks (entity extraction, simple classification) → Haiku ($0.25/1M input)
Medium tasks (domain classification, summarization) → Sonnet ($3/1M input)
Complex tasks (strategic insights, deal analysis) → Opus ($15/1M input) - rare
```

### Implementation: `lib/cost/cost_controller.py`

```python
from datetime import datetime, timedelta
from typing import Dict, Any
import hashlib

class CostController:
    """Enforces budget limits and optimizes LLM usage"""
    
    # Budget limits (USD)
    BUDGETS = {
        "daily_per_vault": 50.00,
        "monthly_per_vault": 1500.00,
    }
    
    # Alert thresholds
    ALERT_THRESHOLDS = {
        "daily": 0.8,  # Alert at 80% of daily budget
        "monthly": 0.9  # Alert at 90% of monthly budget
    }
    
    def __init__(self, convex_db, redis_cache, event_logger):
        self.db = convex_db
        self.cache = redis_cache
        self.event_logger = event_logger
    
    def check_budget(self, vault_id: str) -> Dict[str, Any]:
        """Check if vault is within budget limits"""
        
        # Get current spend
        daily_spend = self._get_daily_spend(vault_id)
        monthly_spend = self._get_monthly_spend(vault_id)
        
        # Check limits
        daily_limit = self.BUDGETS["daily_per_vault"]
        monthly_limit = self.BUDGETS["monthly_per_vault"]
        
        status = {
            "within_budget": True,
            "daily_spend": daily_spend,
            "daily_limit": daily_limit,
            "daily_remaining": daily_limit - daily_spend,
            "monthly_spend": monthly_spend,
            "monthly_limit": monthly_limit,
            "monthly_remaining": monthly_limit - monthly_spend,
        }
        
        # Check daily limit
        if daily_spend >= daily_limit:
            status["within_budget"] = False
            status["exceeded"] = "daily"
            
            self.event_logger.log({
                "type": "cost.budget.exceeded",
                "payload": {
                    "vault_id": vault_id,
                    "period": "daily",
                    "spend": daily_spend,
                    "limit": daily_limit
                },
                "severity": "critical"
            })
        
        # Check monthly limit
        elif monthly_spend >= monthly_limit:
            status["within_budget"] = False
            status["exceeded"] = "monthly"
            
            self.event_logger.log({
                "type": "cost.budget.exceeded",
                "payload": {
                    "vault_id": vault_id,
                    "period": "monthly",
                    "spend": monthly_spend,
                    "limit": monthly_limit
                },
                "severity": "critical"
            })
        
        # Check alert thresholds
        elif daily_spend >= daily_limit * self.ALERT_THRESHOLDS["daily"]:
            self.event_logger.log({
                "type": "cost.budget.alert",
                "payload": {
                    "vault_id": vault_id,
                    "period": "daily",
                    "spend": daily_spend,
                    "limit": daily_limit,
                    "threshold": self.ALERT_THRESHOLDS["daily"]
                },
                "severity": "high"
            })
        
        return status
    
    def cached_llm_call(
        self,
        model: str,
        prompt: str,
        llm_client,
        cache_ttl: int = 3600,
        operation_type: str = "meeting"
    ):
        """
        Make LLM call with caching and budget checks
        
        Returns:
            {
                "response": str,
                "cached": bool,
                "cost_usd": float
            }
        """
        
        vault_id = TenantContext.get_vault()
        
        # Check budget
        budget = self.check_budget(vault_id)
        if not budget["within_budget"]:
            raise BudgetExceededError(
                f"Vault {vault_id} has exceeded {budget['exceeded']} budget limit"
            )
        
        # Generate cache key
        cache_key = self._generate_cache_key(model, prompt, operation_type)
        
        # Check cache
        cached_response = self.cache.get(cache_key)
        if cached_response:
            self.event_logger.log({
                "type": "llm.cache_hit",
                "payload": {
                    "cache_key": cache_key,
                    "vault_id": vault_id
                }
            })
            return {
                "response": cached_response,
                "cached": True,
                "cost_usd": 0.0
            }
        
        # Make LLM call
        from lib.observability.model_tracing import ModelTracer
        tracer = ModelTracer(self.event_logger)
        
        result = tracer.trace_llm_call(model, prompt, llm_client)
        
        # Cache response
        self.cache.setex(
            cache_key,
            cache_ttl,
            result["response"]
        )
        
        # Track cost
        self._increment_spend(vault_id, result["metadata"]["cost_usd"])
        
        return {
            "response": result["response"],
            "cached": False,
            "cost_usd": result["metadata"]["cost_usd"]
        }
    
    def _generate_cache_key(
        self,
        model: str,
        prompt: str,
        operation_type: str
    ) -> str:
        """Generate cache key for LLM call"""
        content = f"{model}:{operation_type}:{prompt}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def _get_daily_spend(self, vault_id: str) -> float:
        """Get today's spend for vault"""
        today = datetime.utcnow().date().isoformat()
        
        events = self.db.query("events:list", {
            "vault_id": vault_id,
            "event_type": "llm.response",
            "date": today
        })
        
        return sum(e["payload"].get("cost_usd", 0.0) for e in events)
    
    def _get_monthly_spend(self, vault_id: str) -> float:
        """Get this month's spend for vault"""
        month_start = datetime.utcnow().replace(day=1).isoformat()
        
        events = self.db.query("events:list", {
            "vault_id": vault_id,
            "event_type": "llm.response",
            "since": month_start
        })
        
        return sum(e["payload"].get("cost_usd", 0.0) for e in events)
    
    def _increment_spend(self, vault_id: str, cost: float):
        """Track spend in real-time cache"""
        # Also cache spend in Redis for fast checks
        today = datetime.utcnow().date().isoformat()
        key = f"spend:{vault_id}:{today}"
        
        self.cache.incrbyfloat(key, cost)
        self.cache.expire(key, 86400 * 2)  # Keep for 2 days
    
    def get_cost_report(self, vault_id: str, period: str = "day"):
        """Generate cost report"""
        
        if period == "day":
            spend = self._get_daily_spend(vault_id)
            limit = self.BUDGETS["daily_per_vault"]
        else:
            spend = self._get_monthly_spend(vault_id)
            limit = self.BUDGETS["monthly_per_vault"]
        
        return {
            "period": period,
            "spend_usd": spend,
            "limit_usd": limit,
            "remaining_usd": limit - spend,
            "utilization_pct": (spend / limit) * 100 if limit > 0 else 0
        }
```

### Model Router

**Implementation**: `lib/cost/model_router.py`

```python
from enum import Enum

class TaskComplexity(Enum):
    LOW = "low"      # Simple extraction, binary classification
    MEDIUM = "medium"  # Multi-class classification, summarization
    HIGH = "high"    # Strategic analysis, complex reasoning

class ModelRouter:
    """Routes requests to optimal model based on task complexity"""
    
    MODEL_SELECTION = {
        TaskComplexity.LOW: "claude-3-haiku-20240307",
        TaskComplexity.MEDIUM: "claude-3-sonnet-20240229",
        TaskComplexity.HIGH: "claude-3-opus-20240229",
    }
    
    # Context length limits
    CONTEXT_LIMITS = {
        "claude-3-haiku-20240307": 200_000,
        "claude-3-sonnet-20240229": 200_000,
        "claude-3-opus-20240229": 200_000,
    }
    
    def route_request(
        self,
        task_type: str,
        context_length: int,
        complexity: TaskComplexity = None,
        priority: str = "balanced"  # "cost", "balanced", "quality"
    ) -> str:
        """
        Select optimal model for request
        
        Args:
            task_type: "classification", "extraction", "summarization", "analysis"
            context_length: Number of tokens in input
            complexity: Override automatic complexity detection
            priority: Optimization priority
        
        Returns:
            model name
        """
        
        # Auto-detect complexity if not provided
        if not complexity:
            complexity = self._detect_complexity(task_type, context_length)
        
        # Select base model
        model = self.MODEL_SELECTION[complexity]
        
        # Adjust based on priority
        if priority == "cost":
            # Downgrade by one tier if possible
            if complexity == TaskComplexity.MEDIUM:
                model = self.MODEL_SELECTION[TaskComplexity.LOW]
            elif complexity == TaskComplexity.HIGH:
                model = self.MODEL_SELECTION[TaskComplexity.MEDIUM]
        
        elif priority == "quality":
            # Upgrade by one tier if possible
            if complexity == TaskComplexity.LOW:
                model = self.MODEL_SELECTION[TaskComplexity.MEDIUM]
            elif complexity == TaskComplexity.MEDIUM:
                model = self.MODEL_SELECTION[TaskComplexity.HIGH]
        
        # Check context length
        if context_length > self.CONTEXT_LIMITS[model]:
            # Upgrade to model with larger context
            model = "claude-3-opus-20240229"
        
        return model
    
    def _detect_complexity(self, task_type: str, context_length: int) -> TaskComplexity:
        """Auto-detect task complexity"""
        
        # Simple tasks
        if task_type in ["entity_extraction", "binary_classification"]:
            return TaskComplexity.LOW
        
        # Medium tasks
        if task_type in ["domain_classification", "summarization"]:
            return TaskComplexity.MEDIUM
        
        # Complex tasks
        if task_type in ["deal_analysis", "strategic_insights"]:
            return TaskComplexity.HIGH
        
        # Default based on context length
        if context_length < 1000:
            return TaskComplexity.LOW
        elif context_length < 5000:
            return TaskComplexity.MEDIUM
        else:
            return TaskComplexity.HIGH
```

### Usage Example

```python
cost_controller = CostController(convex_db, redis_cache, event_logger)
model_router = ModelRouter()

def classify_meeting(transcript: str):
    # Route to optimal model
    model = model_router.route_request(
        task_type="domain_classification",
        context_length=len(transcript),
        priority="balanced"
    )
    
    # Make cached LLM call with budget check
    result = cost_controller.cached_llm_call(
        model=model,
        prompt=transcript,
        llm_client=anthropic_client,
        cache_ttl=3600,
        operation_type="meeting"
    )
    
    if result["cached"]:
        print("✅ Cache hit - $0.00")
    else:
        print(f"💰 Cost: ${result['cost_usd']:.4f}")
    
    return result["response"]
```

---

## 2. MCP (MODEL CONTEXT PROTOCOL) INTEGRATION

### Overview

MCP enables Claude Code, Cursor, and Google Antigravity to access external tools (Notion, Fireflies, Closely) securely.

### Architecture

```
Claude Code/Antigravity
    ↓ [MCP Protocol]
MCP Server (per integration)
    ↓ [OAuth/API Key]
External Service (Notion, Fireflies, Closely)
```

### Security Concerns

1. **Credential theft**: OAuth tokens must be stored securely
2. **Unauthorized access**: MCP servers need proper scoping
3. **Token expiration**: Must handle refresh automatically

### Implementation: `lib/integrations/mcp_manager.py`

```python
from typing import Dict, Any, List
import json

class MCPManager:
    """Manages MCP server configurations"""
    
    def __init__(self, config_path: str = "antigravity.config.json"):
        self.config_path = config_path
        self.servers = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load MCP configuration"""
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        return config.get("mcp_servers", {})
    
    def configure_notion_mcp(
        self,
        workspace_id: str,
        access_token: str,
        refresh_token: str
    ):
        """Configure Notion MCP server"""
        
        self.servers["notion"] = {
            "server": "@notionhq/notion-mcp-server",
            "auth": {
                "type": "oauth",
                "workspace_id": workspace_id,
                "access_token_env": "NOTION_ACCESS_TOKEN",
                "refresh_token_env": "NOTION_REFRESH_TOKEN"
            },
            "allowed_operations": [
                "search_pages",
                "get_page",
                "create_page",
                "update_page",
                "query_database"
            ]
        }
        
        self._save_config()
    
    def configure_fireflies_mcp(self, api_key: str):
        """Configure Fireflies MCP adapter"""
        
        self.servers["fireflies"] = {
            "server": "custom",
            "adapter": "lib/integrations/fireflies_mcp_adapter.py",
            "auth": {
                "type": "api_key",
                "key_env": "FIREFLIES_API_KEY"
            },
            "allowed_operations": [
                "get_transcripts",
                "search_meetings"
            ]
        }
        
        self._save_config()
    
    def configure_closely_mcp(self, api_key: str):
        """Configure Closely.ai MCP adapter"""
        
        self.servers["closely"] = {
            "server": "custom",
            "adapter": "lib/integrations/closely_mcp_adapter.py",
            "auth": {
                "type": "api_key",
                "key_env": "CLOSELY_API_KEY"
            },
            "allowed_operations": [
                "enrich_company",
                "find_contacts",
                "get_company_data"
            ]
        }
        
        self._save_config()
    
    def _save_config(self):
        """Save MCP configuration"""
        config = {"mcp_servers": self.servers}
        
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
```

### Credential Management

**Implementation**: `lib/integrations/credential_manager.py`

```python
import os
from datetime import datetime, timedelta
from typing import Dict, Any

class SecureCredentialManager:
    """Manages OAuth tokens and API keys securely"""
    
    def __init__(self, vault_backend: str = "env"):
        """
        Args:
            vault_backend: "env" (environment variables) or "aws_secrets" (AWS Secrets Manager)
        """
        self.vault_backend = vault_backend
    
    def store_oauth_tokens(
        self,
        service: str,
        tokens: Dict[str, str],
        vault_id: str
    ):
        """
        Store OAuth tokens securely
        
        Args:
            service: "notion", "google", etc.
            tokens: {
                "access_token": str,
                "refresh_token": str,
                "expires_at": str (ISO format)
            }
            vault_id: Tenant vault ID
        """
        
        if self.vault_backend == "env":
            # Store in environment (for development)
            os.environ[f"{service.upper()}_ACCESS_TOKEN_{vault_id}"] = tokens["access_token"]
            os.environ[f"{service.upper()}_REFRESH_TOKEN_{vault_id}"] = tokens["refresh_token"]
            os.environ[f"{service.upper()}_EXPIRES_AT_{vault_id}"] = tokens["expires_at"]
        
        elif self.vault_backend == "aws_secrets":
            # Store in AWS Secrets Manager (for production)
            import boto3
            secrets = boto3.client('secretsmanager')
            
            secrets.put_secret_value(
                SecretId=f"{vault_id}/{service}/oauth",
                SecretString=json.dumps(tokens)
            )
    
    def get_oauth_tokens(
        self,
        service: str,
        vault_id: str,
        auto_refresh: bool = True
    ) -> Dict[str, str]:
        """
        Get OAuth tokens (with automatic refresh)
        
        Returns:
            {
                "access_token": str,
                "refresh_token": str,
                "expires_at": str
            }
        """
        
        # Retrieve tokens
        if self.vault_backend == "env":
            tokens = {
                "access_token": os.environ.get(f"{service.upper()}_ACCESS_TOKEN_{vault_id}"),
                "refresh_token": os.environ.get(f"{service.upper()}_REFRESH_TOKEN_{vault_id}"),
                "expires_at": os.environ.get(f"{service.upper()}_EXPIRES_AT_{vault_id}")
            }
        
        elif self.vault_backend == "aws_secrets":
            import boto3
            secrets = boto3.client('secretsmanager')
            
            response = secrets.get_secret_value(
                SecretId=f"{vault_id}/{service}/oauth"
            )
            tokens = json.loads(response['SecretString'])
        
        # Check expiration
        if auto_refresh and self._is_expired(tokens):
            tokens = self._refresh_tokens(service, tokens, vault_id)
        
        return tokens
    
    def _is_expired(self, tokens: Dict[str, str]) -> bool:
        """Check if access token is expired"""
        expires_at = datetime.fromisoformat(tokens["expires_at"])
        # Refresh 5 minutes before expiration
        return datetime.utcnow() >= expires_at - timedelta(minutes=5)
    
    def _refresh_tokens(
        self,
        service: str,
        tokens: Dict[str, str],
        vault_id: str
    ) -> Dict[str, str]:
        """Refresh OAuth tokens"""
        
        if service == "notion":
            # Notion OAuth refresh
            import requests
            
            response = requests.post(
                "https://api.notion.com/v1/oauth/token",
                json={
                    "grant_type": "refresh_token",
                    "refresh_token": tokens["refresh_token"]
                },
                headers={
                    "Authorization": f"Basic {NOTION_CLIENT_CREDENTIALS}"
                }
            )
            
            new_tokens = response.json()
            
            # Update stored tokens
            self.store_oauth_tokens(service, {
                "access_token": new_tokens["access_token"],
                "refresh_token": new_tokens.get("refresh_token", tokens["refresh_token"]),
                "expires_at": (datetime.utcnow() + timedelta(seconds=new_tokens["expires_in"])).isoformat()
            }, vault_id)
            
            return new_tokens
        
        # Add other services as needed
        raise NotImplementedError(f"Token refresh not implemented for {service}")
```

### Example MCP Configuration

**`antigravity.config.json`**:

```json
{
  "mcp_servers": {
    "notion": {
      "server": "@notionhq/notion-mcp-server",
      "auth": {
        "type": "oauth",
        "workspace_id": "abc123",
        "access_token_env": "NOTION_ACCESS_TOKEN_vault_aihuevos_prod",
        "refresh_token_env": "NOTION_REFRESH_TOKEN_vault_aihuevos_prod"
      },
      "allowed_operations": [
        "search_pages",
        "get_page",
        "create_page",
        "update_page",
        "query_database"
      ]
    },
    "fireflies": {
      "server": "custom",
      "adapter": "lib/integrations/fireflies_mcp_adapter.py",
      "auth": {
        "type": "api_key",
        "key_env": "FIREFLIES_API_KEY"
      }
    }
  }
}
```

---

## 3. IDENTITY RESOLUTION

### Problem

Meetings contain duplicate entities:
- "John Smith" vs "John" vs "J. Smith"
- "Acme Inc" vs "Acme" vs "Acme Corporation"

Need canonical IDs for accurate analysis.

### Implementation: `lib/identity/entity_resolver.py`

```python
from typing import Dict, Any, List
import hashlib

class EntityResolver:
    """Resolves entities to canonical IDs with deduplication"""
    
    def __init__(self, convex_db, event_logger):
        self.db = convex_db
        self.event_logger = event_logger
    
    def resolve_person(
        self,
        name: str,
        email: str = None,
        company: str = None
    ) -> str:
        """
        Resolve person to canonical ID
        
        Returns:
            person_id (canonical)
        """
        
        vault_id = TenantContext.get_vault()
        
        # Normalize name
        normalized_name = self._normalize_name(name)
        
        # Search for existing person
        matches = self.db.query("people:search", {
            "vault_id": vault_id,
            "normalized_name": normalized_name,
            "email": email
        })
        
        if matches:
            # Return existing person
            person_id = matches[0]['id']
            
            # Log resolution
            self.event_logger.log({
                "type": "identity.resolved",
                "payload": {
                    "entity_type": "person",
                    "input_name": name,
                    "canonical_id": person_id
                }
            })
            
            return person_id
        
        # Create new person
        person_id = self.db.mutation("people:create", {
            "vault_id": vault_id,
            "name": name,
            "normalized_name": normalized_name,
            "email": email,
            "company": company
        })
        
        return person_id
    
    def resolve_company(
        self,
        name: str,
        domain: str = None
    ) -> str:
        """Resolve company to canonical ID"""
        
        vault_id = TenantContext.get_vault()
        
        # Normalize name
        normalized_name = self._normalize_company_name(name)
        
        # Search by domain first (most reliable)
        if domain:
            matches = self.db.query("companies:search", {
                "vault_id": vault_id,
                "domain": domain
            })
            
            if matches:
                return matches[0]['id']
        
        # Search by normalized name
        matches = self.db.query("companies:search", {
            "vault_id": vault_id,
            "normalized_name": normalized_name
        })
        
        if matches:
            return matches[0]['id']
        
        # Create new company
        company_id = self.db.mutation("companies:create", {
            "vault_id": vault_id,
            "name": name,
            "normalized_name": normalized_name,
            "domain": domain
        })
        
        return company_id
    
    def _normalize_name(self, name: str) -> str:
        """Normalize person name for matching"""
        # Remove titles, lowercase, remove punctuation
        name = name.lower()
        name = name.replace("mr.", "").replace("mrs.", "").replace("dr.", "")
        name = "".join(c for c in name if c.isalnum() or c.isspace())
        return " ".join(name.split())
    
    def _normalize_company_name(self, name: str) -> str:
        """Normalize company name for matching"""
        # Remove legal suffixes, lowercase
        name = name.lower()
        suffixes = ["inc", "corp", "corporation", "llc", "ltd", "limited"]
        for suffix in suffixes:
            name = name.replace(f" {suffix}", "")
            name = name.replace(f".{suffix}", "")
        
        name = "".join(c for c in name if c.isalnum() or c.isspace())
        return " ".join(name.split())
```

---

## 4. GROWTH AGENTS

### 4.1 Pipeline Risk Agent

**Purpose**: Flag at-risk deals based on meeting patterns

**Triggers**:
- Meeting frequency drop-off
- Negative sentiment in recent calls
- Multiple reschedules
- No follow-up actions

**Implementation**: `agents/pipeline_risk_agent.py`

```python
class PipelineRiskAgent:
    """Identifies at-risk opportunities"""
    
    def __init__(self, notion_client, llm_client, event_logger):
        self.notion = notion_client
        self.llm = llm_client
        self.event_logger = event_logger
    
    def analyze_pipeline(self, vault_id: str):
        """Analyze all open opportunities for risk"""
        
        # Get open opportunities
        opportunities = self.notion.query_database(
            "opportunities",
            filters={"status": {"equals": "Open"}}
        )
        
        risk_scores = []
        for opp in opportunities:
            risk_score = self._calculate_risk_score(opp)
            
            if risk_score > 0.7:  # High risk
                # Create alert
                self._create_risk_alert(opp, risk_score)
            
            risk_scores.append({
                "opportunity_id": opp['id'],
                "risk_score": risk_score
            })
        
        return risk_scores
    
    def _calculate_risk_score(self, opportunity: dict) -> float:
        """Calculate 0-1 risk score (1.0 = highest risk)"""
        
        risk_factors = []
        
        # Get associated meetings
        meetings = self._get_opportunity_meetings(opportunity['id'])
        
        # Factor 1: Meeting frequency
        if len(meetings) > 0:
            days_since_last = self._days_since_last_meeting(meetings)
            if days_since_last > 14:
                risk_factors.append(0.3)  # High risk
        
        # Factor 2: Sentiment trend
        sentiment_scores = [m['sentiment'] for m in meetings if 'sentiment' in m]
        if sentiment_scores:
            recent_sentiment = sum(sentiment_scores[-3:]) / min(3, len(sentiment_scores))
            if recent_sentiment < 0.3:  # Negative sentiment
                risk_factors.append(0.4)
        
        # Factor 3: No next steps
        if not opportunity.get('next_steps'):
            risk_factors.append(0.2)
        
        # Factor 4: Stage stagnation
        days_in_stage = self._days_in_current_stage(opportunity)
        if days_in_stage > 30:
            risk_factors.append(0.1)
        
        return min(1.0, sum(risk_factors))
    
    def _create_risk_alert(self, opportunity: dict, risk_score: float):
        """Create Slack alert for at-risk deal"""
        
        message = f"""
🚨 **Deal At Risk**

**Company**: {opportunity['company']}
**Deal Value**: ${opportunity['deal_value']:,}
**Risk Score**: {risk_score:.0%}

**Recommended Actions**:
- Schedule follow-up call
- Review recent meeting notes
- Confirm next steps
"""
        
        # Send to Slack
        slack_client.chat_postMessage(
            channel="#sales-alerts",
            text=message
        )
        
        # Log
        self.event_logger.log({
            "type": "growth.pipeline_risk.alert",
            "payload": {
                "opportunity_id": opportunity['id'],
                "risk_score": risk_score
            },
            "severity": "high"
        })
```

### 4.2 Messaging Insights Agent

**Purpose**: Extract common objection patterns and successful responses

**Implementation**: `agents/messaging_insights_agent.py`

```python
class MessagingInsightsAgent:
    """Analyzes sales conversations for patterns"""
    
    def __init__(self, notion_client, llm_client, event_logger):
        self.notion = notion_client
        self.llm = llm_client
        self.event_logger = event_logger
    
    def extract_objections(self, vault_id: str):
        """Extract common objections from sales meetings"""
        
        # Get closed-won and closed-lost deals
        won_meetings = self._get_meetings_by_outcome("won")
        lost_meetings = self._get_meetings_by_outcome("lost")
        
        # Extract objections
        won_objections = self._extract_objections_from_meetings(won_meetings)
        lost_objections = self._extract_objections_from_meetings(lost_meetings)
        
        # Compare patterns
        insights = {
            "common_objections": self._find_common_objections(won_objections + lost_objections),
            "successful_responses": self._find_successful_responses(won_objections),
            "unresolved_objections": self._find_unresolved_objections(lost_objections)
        }
        
        return insights
    
    def _extract_objections_from_meetings(self, meetings: List[dict]) -> List[dict]:
        """Use LLM to extract objections"""
        
        objections = []
        for meeting in meetings:
            transcript = meeting['transcript']
            
            # LLM prompt
            prompt = f"""
Extract customer objections from this sales call transcript.

For each objection, provide:
1. The objection text (verbatim)
2. The category (price, features, timing, competition, other)
3. How the rep responded (if at all)

Transcript:
{transcript}

Respond with JSON array.
"""
            
            response = self.llm.generate(prompt)
            meeting_objections = json.loads(response)
            
            for obj in meeting_objections:
                obj['meeting_id'] = meeting['id']
                obj['outcome'] = meeting['outcome']
            
            objections.extend(meeting_objections)
        
        return objections
```

---

**This is Part 3 of 3. See security_spec.md and observability_spec.md for complete system architecture.**
