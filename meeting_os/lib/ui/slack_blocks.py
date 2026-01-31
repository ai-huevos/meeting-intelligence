from typing import List, Dict, Any
from meeting_os.lib.schema.uco import UniversalContextObject, RoutingFlags

class BioChromaticUI:
    """
    Generates 'Bio-chromatic' Slack Interfaces.
    """
    
    # Neon Palette (Slack Attachments support hex colors)
    COLORS = {
        "NEURAL_PINK": "#FF00FF",  # Human/User
        "DATA_CYAN":   "#00FFFF",  # Ingestion/Raw
        "BIO_LIME":    "#00FF00",  # Success/Money
        "VOID_BLACK":  "#000000",  # Background (Implied)
        "ALERT_YELLOW": "#FFFF00"  # Warning/Router
    }

    @staticmethod
    def render_ingestion_card(uco: UniversalContextObject, routes: List[str]) -> Dict[str, Any]:
        """
        Renders a 'Data Cyan' card for new meeting ingestion.
        """
        summary = uco.context_layer.summary
        source_emoji = {
            "Fireflies": "🦋",
            "Slack": "💬",
            "WhatsApp": "📱",
            "GoogleCalendar": "📅"
        }.get(uco.source, "📡")

        return {
            "username": "The Hub (Router)",
            "icon_emoji": ":brain:",
            "attachments": [
                {
                    "color": BioChromaticUI.COLORS["DATA_CYAN"],
                    "blocks": [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": f"{source_emoji} Signal Received: {uco.source}",
                                "emoji": True
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"*Event ID*: `{uco.event_id}`\n*Routes Activated*: `{' | '.join(routes)}`"
                            }
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"> {summary}"
                            }
                        },
                        {
                            "type": "context",
                            "elements": [
                                {
                                    "type": "mrkdwn",
                                    "text": f"🧠 *Analysis*: {uco.context_layer.sentiment}   |   🕒 {uco.timestamp}"
                                }
                            ]
                        }
                    ]
                }
            ]
        }

    @staticmethod
    def render_approval_card(action: str, params: Dict, approval_id: str) -> Dict[str, Any]:
        """
        Renders a 'Neural Pink' card for human approval.
        """
        return {
            "username": "Gatekeeper",
            "icon_emoji": ":shield:",
            "attachments": [
                {
                    "color": BioChromaticUI.COLORS["NEURAL_PINK"],
                    "blocks": [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": "🔐 Authorization Required",
                                "emoji": True
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"Agent requests permission to execute: *{action}*"
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"```\n{params}\n```"
                            }
                        },
                        {
                            "type": "actions",
                            "block_id": approval_id,
                            "elements": [
                                {
                                    "type": "button",
                                    "text": {
                                        "type": "plain_text",
                                        "text": "✅ Approve",
                                        "emoji": True
                                    },
                                    "style": "primary",
                                    "value": "approve"
                                },
                                {
                                    "type": "button",
                                    "text": {
                                        "type": "plain_text",
                                        "text": "❌ Deny",
                                        "emoji": True
                                    },
                                    "style": "danger",
                                    "value": "deny"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
