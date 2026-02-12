import os
import json
from meeting_os.services.llm import LLMClient
from meeting_os.core.security.input_sanitizer import InputSanitizer
from meeting_os.core.security.prompt_wrapper import SecurePromptWrapper
from meeting_os.core.event_log import EventLog

class BaseAgent:
    """Base class for all Meeting OS agents."""
    
    def __init__(self, event_log=None):
        self.event_log = event_log or EventLog()
        self.sanitizer = InputSanitizer(self.event_log)
        self.prompt_wrapper = SecurePromptWrapper()
        self.llm_client = LLMClient(event_logger=self.event_log)
        self.agent_name = "BaseAgent"

    def load_prompt(self, path_fragment):
        """Load prompt from relative path fragment."""
        # path_fragment e.g. "extraction/sales_extraction.txt"
        path = os.path.join(os.path.dirname(__file__), "..", "prompts", path_fragment)
        try:
            with open(path, "r") as f:
                return f.read()
        except FileNotFoundError:
            # Fallback for classification prompts which are in prompts/classification
             path = os.path.join(os.path.dirname(__file__), "..", "prompts", "classification", path_fragment)
             with open(path, "r") as f:
                return f.read()

    def sanitize_input(self, text, metadata=None):
        """Sanitize input text."""
        result = self.sanitizer.sanitize_transcript(text, metadata or {})
        if result["quarantined"]:
            self.event_log.log({
                "type": "security.quarantine",
                "payload": result,
                "workflow_id": metadata.get("workflow_id")
            })
            raise SecurityError("Input quarantined due to security violation.")
        return result["sanitized"]

    def call_llm(self, prompt, workflow_id=None):
        """Call LLM with logging."""
        try:
            response = self.llm_client.generate(prompt)
            # Clean markdown
            clean_text = response.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:]
            if clean_text.startswith("```"):
                clean_text = clean_text[3:]
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]
            return clean_text.strip()
        except Exception as e:
            self.event_log.log({
                "type": "llm.error",
                "payload": {"error": str(e)},
                "workflow_id": workflow_id,
                "severity": "high"
            })
            raise

class SecurityError(Exception):
    pass
