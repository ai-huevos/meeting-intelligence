import json
import uuid
import os
from meeting_os.lib.agents.base_agent import BaseAgent

class LibrarianAgent(BaseAgent):
    def __init__(self, event_log=None):
        super().__init__(event_log)
        self.agent_name = "LibrarianAgent"
    
    def classify_meeting(self, meeting_id, transcript):
        """
        Classifies a meeting into a domain.
        """
        workflow_id = str(uuid.uuid4())
        
        self.event_log.log({
            "type": "workflow.started",
            "payload": {"meeting_id": meeting_id, "agent": "librarian"},
            "workflow_id": workflow_id
        })
        
        # 1. Sanitize
        try:
            clean_transcript = self.sanitize_input(transcript, {"meeting_id": meeting_id, "workflow_id": workflow_id})
        except Exception as e:
            return {"status": "quarantined" if "quarantined" in str(e) else "error", "error": str(e)}
        
        # 2. Prepare Prompt
        # Note: BaseAgent.load_prompt defaults to ../../prompts, but librarian prompts are in ../../prompts/classification
        # The base agent handles this specific fallback now.
        base_prompt = self.load_prompt("domain_classification.txt")
        filled_prompt = base_prompt.replace("{{transcript}}", clean_transcript)
        
        # 3. Apply Securirty Wrapper
        final_prompt = self.prompt_wrapper.wrap_librarian_prompt(filled_prompt)
        
        # 4. Call LLM
        print(f"[LIBRARIAN] Calling LLM with prompt length: {len(final_prompt)}")
        try:
            clean_text = self.call_llm(final_prompt, workflow_id)
            
            # Debug print
            print(f"DEBUG RAW RESPONSE: {repr(clean_text)}")

            result = json.loads(clean_text)
            self.event_log.log({
                "type": "meeting.classified",
                "payload": result,
                "workflow_id": workflow_id
            })
            return result
        except json.JSONDecodeError as e:
             self.event_log.log({
                "type": "error.json_parse",
                "payload": {"error": str(e), "text_preview": clean_text[:500]},
                "workflow_id": workflow_id,
                "severity": "high"
            })
             # Last ditch effort: regex for JSON object
             import re
             try:
                 match = re.search(r'\{.*\}', clean_text, re.DOTALL)
                 if match:
                     return json.loads(match.group(0))
             except:
                 pass
             return None
        except Exception as e:
            self.event_log.log({
                "type": "workflow.failed",
                "payload": {"error": str(e)},
                "workflow_id": workflow_id
            })
            return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    from meeting_os.lib.tenancy.vault_context import TenantContext
    TenantContext.set_vault("test_vault", "user_1")
    
    librarian = LibrarianAgent()
    res = librarian.classify_meeting("123", "We talked about the enterprise contract for 50k.")
    print(res)
