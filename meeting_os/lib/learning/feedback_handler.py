import uuid
from datetime import datetime
from meeting_os.lib.observability.event_log import EventLog

class FeedbackHandler:
    """
    Handles user feedback on agent actions.
    Implements the Gamified Correction Protocol.
    """
    
    POINTS_MAP = {
        "correction": 10,  # Fixing a mistake
        "validation": 1,   # Confirming correctness
        "refinement": 5    # Improving detail
    }
    
    def __init__(self, event_log=None):
        self.event_log = event_log or EventLog()
        
    def handle_feedback(self, feedback_data):
        """
        Process feedback from user (e.g. via Slack interactivity).
        
        feedback_data: {
            "workflow_id": str,
            "step_id": str, # which step (classification, extraction)
            "feedback_type": "positive|negative|correction",
            "correction_payload": dict (optional),
            "user_id": str
        }
        """
        workflow_id = feedback_data.get("workflow_id")
        user_id = feedback_data.get("user_id")
        feedback_type = feedback_data.get("feedback_type")
        
        # 1. Log the raw feedback
        self.event_log.log({
            "type": "feedback.received",
            "payload": feedback_data,
            "workflow_id": workflow_id,
            "user_id": user_id
        })
        
        # 2. Gamification Logic
        points = 0
        if feedback_type == "correction":
            points = self.POINTS_MAP["correction"]
        elif feedback_type == "positive":
            points = self.POINTS_MAP["validation"]
            
        if points > 0:
            self._award_points(user_id, points, workflow_id)
            
        # 3. Learning trigger (future: auto-optimize prompt)
        if feedback_type == "correction":
            self._trigger_learning_event(workflow_id, feedback_data)

        return {"status": "success", "points_awarded": points}

    def _award_points(self, user_id, points, ref_id):
        """Award points to the user."""
        self.event_log.log({
            "type": "gamification.points_awarded",
            "payload": {"points": points, "reason": f"Feedback on {ref_id}"},
            "user_id": user_id
        })
        # In a real app, this would write to a User/Leaderboard DB
        print(f"🏆 Awarded {points} points to {user_id}!")

    def _trigger_learning_event(self, workflow_id, feedback_data):
        """Flag this interaction for the Template Improver."""
        self.event_log.log({
            "type": "learning.dataset_candidate",
            "payload": {
                "reason": "User correction provided",
                "correction": feedback_data.get("correction_payload")
            },
            "workflow_id": workflow_id
        })
