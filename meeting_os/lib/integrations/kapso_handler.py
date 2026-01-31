import os
import requests
import json

class KapsoClient:
    """
    Client for interacting with Kapso (WhatsApp).
    Proxies to Meta WhatsApp Cloud API via Kapso.
    """
    
    def __init__(self, api_key=None, phone_id=None):
        self.api_key = api_key or os.getenv("KAPSO_API_KEY")
        self.phone_id = phone_id or os.getenv("WHATSAPP_PHONE_ID")
        self.base_url = "https://api.kapso.ai/meta/whatsapp"
        
        if not self.api_key:
            print("⚠️ KAPSO_API_KEY not found in env.")
        
    def send_whatsapp_message(self, phone_number, text):
        """
        Send a text message via Kapso/WhatsApp.
        """
        if not self.phone_id:
            print("❌ WHATSAPP_PHONE_ID not found. Cannot send message.")
            return False

        url = f"{self.base_url}/{self.phone_id}/messages"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}", # Standard Bearer for proxy
            "Content-Type": "application/json"
        }
        
        # Standard Meta WhatsApp Payload
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": text
            }
        }
        
        try:
            print(f"📱 [Kapso] Sending to {phone_number} via {url}...")
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            print(f"✅ Message sent! ID: {response.json().get('messages', [{}])[0].get('id')}")
            return True
        except Exception as e:
            print(f"❌ Failed to send WhatsApp: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"   Response: {e.response.text}")
            return False

    def handle_incoming_message(self, payload):
        """
        Parses incoming webhook from Kapso.
        """
        try:
            # Extract standard Meta Webhook structure
            entry = payload.get("entry", [])[0]
            changes = entry.get("changes", [])[0]
            value = changes.get("value", {})
            messages = value.get("messages", [])
            
            if not messages:
                return None
                
            msg = messages[0]
            return {
                "sender": msg.get("from"),
                "text": msg.get("text", {}).get("body"),
                "timestamp": msg.get("timestamp"),
                "type": msg.get("type"),
                "platform": "whatsapp"
            }
        except Exception as e:
            print(f"⚠️ Error parsing webhook: {e}")
            return None

if __name__ == "__main__":
    # Test
    client = KapsoClient()
    # client.send_whatsapp_message("1234567890", "Test from Local")
