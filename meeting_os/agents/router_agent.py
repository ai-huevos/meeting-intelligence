import json
from meeting_os.lib.observability.event_log import EventLog
from meeting_os.lib.integrations.slack import SlackClient

class RouterAgent:
    """
    Routes processed meeting results to the appropriate channels
    and manages notifications.
    """
    
    def __init__(self, slack_client=None, event_log=None):
        self.slack = slack_client or SlackClient()
        self.event_log = event_log or EventLog()

    def route_result(self, meeting_data, processing_result):
        """
        Route the result to notifications and storage.
        """
        domain = processing_result.get("domain", "Other")
        summary = processing_result.get("summary", "No summary available.")
        
        # Log routing
        self.event_log.log({
            "type": "router.routing",
            "payload": {
                "meeting_id": meeting_data.get("id"),
                "domain": domain
            }
        })
        
        # Determine channel based on domain (Mock logic)
        channel_map = {
            "Sales": "#sales-leads",
            "Product": "#product-feedback",
            "CS": "#cs-alerts",
            "Finance": "#finance-ops",
            "Ops": "#biz-ops"
        }
        channel = channel_map.get(domain, "#general")
        
        # Send Notification
        message = f"📢 **New Meeting Processed**\nDomain: *{domain}*\nTitle: {meeting_data.get('title', 'Untitled')}\n\n{summary}"
        
        self.slack.send_message(message, channel=channel)
        
        # In a real scenario, this would also trigger domain-specific workflows via n8n
        # or call other agents.
        
        return {"status": "routed", "channel": channel}

if __name__ == "__main__":
    # Test
    router = RouterAgent()
    router.route_result(
        {"id": "123", "title": "Sales Call with Acme"}, 
        {"domain": "Sales", "summary": "Great call, they want to buy."}
    )
