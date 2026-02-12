from typing import Set, Dict
from enum import Enum
# from meeting_os.core.tenancy.vault_context import TenantContext # Avoid circular dependency if possible, or inject context

class AgentContext(Enum):
    LIBRARIAN = "librarian"
    SALES = "sales"
    PRODUCT = "product"
    CUSTOMER_SUCCESS = "customer_success"
    FINANCE = "finance"

class ToolAllowlist:
    """Enforces tool access control per agent context"""
    
    # Define allowed tools per agent
    ALLOWLISTS: Dict[AgentContext, Set[str]] = {
        AgentContext.LIBRARIAN: {
            "search_meetings",
            "get_meeting",
        },
        AgentContext.SALES: {
            "search_meetings",
            "get_meeting",
            "create_opportunity",
            "update_opportunity",
            "search_companies",
            "create_company",
            "send_slack_notification",
        },
        AgentContext.PRODUCT: {
            "search_meetings",
            "get_meeting",
            "create_feature_request",
            "update_feature_request",
            "send_slack_notification",
        },
        AgentContext.CUSTOMER_SUCCESS: {
            "search_meetings",
            "get_meeting",
            "create_support_ticket",
            "update_account_health",
            "send_slack_notification",
        },
        AgentContext.FINANCE: {
            "search_meetings",
            "get_meeting",
            "create_contract",
            "update_revenue_forecast",
        }
    }
    
    # Tools that should NEVER be allowed
    NEVER_ALLOWED = {
        "execute_shell_command",
        "write_file",
        "delete_database",
        "modify_permissions",
        "execute_sql",
    }
    
    def __init__(self, event_logger=None):
        self.event_logger = event_logger
    
    def log_event(self, event):
        if self.event_logger:
            self.event_logger.log(event)
        else:
            print(f"[LOG] {event}")

    def is_tool_allowed(
        self,
        agent_context: AgentContext,
        tool_name: str,
        vault_id: str
    ) -> bool:
        """Check if agent is allowed to invoke tool"""
        
        # Block never-allowed tools
        if tool_name in self.NEVER_ALLOWED:
            self.log_event({
                "type": "security.tool.never_allowed",
                "payload": {
                    "agent": agent_context.value,
                    "tool": tool_name,
                    "vault_id": vault_id
                },
                "severity": "critical"
            })
            return False
        
        # Check allowlist
        allowed = tool_name in self.ALLOWLISTS.get(agent_context, set())
        
        if not allowed:
            self.log_event({
                "type": "security.tool.not_allowed",
                "payload": {
                    "agent": agent_context.value,
                    "tool": tool_name,
                    "vault_id": vault_id
                },
                "severity": "high"
            })
        
        return allowed
    
    def get_allowed_tools(self, agent_context: AgentContext) -> Set[str]:
        """Get list of allowed tools for agent"""
        return self.ALLOWLISTS.get(agent_context, set())
