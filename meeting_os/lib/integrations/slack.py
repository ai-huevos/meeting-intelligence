import os
import requests
import json
import logging

logger = logging.getLogger(__name__)

class SlackClient:
    def __init__(self, token=None, default_channel=None):
        self.token = token or os.environ.get("SLACK_BOT_TOKEN")
        self.default_channel = default_channel or os.environ.get("SLACK_DEFAULT_CHANNEL")
        # if not self.token:
        #    logger.warning("SLACK_BOT_TOKEN not set. Slack notifications will be simulated.")

    def send_message(self, text, blocks=None, channel=None):
        """Send message to Slack."""
        channel = channel or self.default_channel
        
        if not self.token:
            print(f"[SLACK SIMULATION] Channel: {channel}\nMessage: {text}")
            return {"ok": True, "ts": "1234.5678"}

        url = "https://slack.com/api/chat.postMessage"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        payload = {
            "channel": channel,
            "text": text
        }
        if blocks:
            payload["blocks"] = blocks
            
        try:
            response = requests.post(url, headers=headers, json=payload)
            return response.json()
        except Exception as e:
            logger.error(f"Failed to send Slack message: {e}")
            return {"ok": False, "error": str(e)}

    def send_approval_request(self, action, params, approval_id, channel=None):
        """Send interactive approval request."""
        blocks = [
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"🔐 **Approval Required**\nAction: `{action}`"}
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"```{json.dumps(params, indent=2)}```"}
            },
            {
                "type": "actions",
                "block_id": approval_id,
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "✅ Approve"},
                        "style": "primary",
                        "action_id": f"approve_{approval_id}"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "❌ Deny"},
                        "style": "danger",
                        "action_id": f"deny_{approval_id}"
                    }
                ]
            }
        ]
        return self.send_message("Approval Required", blocks=blocks, channel=channel)
