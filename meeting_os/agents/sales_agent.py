import json
import uuid
from meeting_os.lib.agents.base_agent import BaseAgent

class SalesAgent(BaseAgent):
    def __init__(self, event_log=None):
        super().__init__(event_log)
        self.agent_name = "SalesAgent"

    def extract_info(self, meeting_id, transcript):
        """
        Extract sales information from a meeting.
        """
        workflow_id = str(uuid.uuid4())
        self.event_log.log({
            "type": "workflow.started",
            "payload": {"meeting_id": meeting_id, "agent": self.agent_name},
            "workflow_id": workflow_id
        })

        # 1. Sanitize
        try:
            clean_transcript = self.sanitize_input(transcript, {"meeting_id": meeting_id, "workflow_id": workflow_id})
        except Exception as e:
            return {"status": "error", "error": str(e)}

        # 2. Prepare Prompt
        base_prompt = self.load_prompt("extraction/sales_extraction.txt")
        filled_prompt = base_prompt.replace("{{transcript}}", clean_transcript)
        
        # 3. Security Wrap (Sales context)
        # Note: prompt_wrapper needs a generic method or specific sales one. 
        # Using existing generic constraint injection via prompt text for now 
        # or assuming LLMClient handles it? 
        # Actually SecurePromptWrapper has wrap_sales_agent_prompt but it expects 'meeting_data' dict?
        # Let's verify SecurePromptWrapper.
        # It has wrap_sales_agent_prompt(meeting_data: dict).
        # But here we are sending full transcript for extraction.
        # Let's use a generic method or just append constraints.
        
        final_prompt = f"{self.prompt_wrapper.SYSTEM_CONSTRAINTS}\n\n{filled_prompt}"

        # 4. Call LLM
        try:
            clean_response = self.call_llm(final_prompt, workflow_id)
            result = json.loads(clean_response)
            
            self.event_log.log({
                "type": "extraction.completed",
                "payload": result,
                "workflow_id": workflow_id
            })
            return result
            
        except json.JSONDecodeError as e:
            self.event_log.log({
                "type": "error.json_parse",
                "payload": {"error": str(e), "text_preview": clean_response[:200]},
                "workflow_id": workflow_id
            })
            return {"status": "error", "error": "Failed to parse JSON response"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    from meeting_os.lib.tenancy.vault_context import TenantContext
    TenantContext.set_vault("test_vault", "test_user")
    
    # Test script would go here or separate file
