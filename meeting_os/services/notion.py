import os
from notion_client import Client
from datetime import datetime

class NotionHandler:
    """
    Handles interactions with Notion for logging conversations and maintaining context.
    Acts as the 'Breadcrumb' storage.
    """
    
    def __init__(self):
        self.api_key = os.getenv("NOTION_API_KEY")
        self.client = Client(auth=self.api_key) if self.api_key else None
        # Ideally this is a specific Database ID for "Conversations" or "Logs"
        # For now we might look for a default or just use a placeholder env var.
        self.conversation_db_id = os.getenv("NOTION_CONVERSATION_DB_ID")
        
    def log_interaction(self, sender: str, message: str, direction: str = "Inbound", metadata: dict = None):
        """
        Log a single interaction (message) to Notion.
        """
        if not self.client or not self.conversation_db_id:
            print(f"[NotionHandler] Skipping log (Missing Key or DB ID): {sender}: {message[:20]}...")
            return None

        try:
            # Construct the page properties for a standard "Conversation" DB
            # Expected DB Columns: Name (Title), Sender (Select), Direction (Select), Metadata (Text/JSON)
            properties = {
                "Name": {"title": [{"text": {"content": f"{sender} - {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"}}]},
                "Sender": {"rich_text": [{"text": {"content": sender}}]},
                "Message": {"rich_text": [{"text": {"content": message}}]},
                "Direction": {"select": {"name": direction}},
                "Timestamp": {"date": {"start": datetime.utcnow().isoformat()}}
            }
            
            if metadata:
                import json
                properties["Metadata"] = {"rich_text": [{"text": {"content": json.dumps(metadata)}}]}

            response = self.client.pages.create(
                parent={"database_id": self.conversation_db_id},
                properties=properties
            )
            return response["id"]
            
        except Exception as e:
            print(f"[NotionHandler] Error logging to Notion: {e}")
            return None

    def create_action_item(self, description: str, owner: str = None):
        """
        Create a task/action item from the conversation.
        """
        # Placeholder for task creation logic
        pass
