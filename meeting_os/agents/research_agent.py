import json
import uuid
from meeting_os.lib.agents.base_agent import BaseAgent
from meeting_os.lib.integrations.perplexity import PerplexityClient

class ResearchAgent(BaseAgent):
    def __init__(self, event_log=None):
        super().__init__(event_log)
        self.agent_name = "ResearchAgent"
        self.perplexity = PerplexityClient()

    def generate_brief(self, target_name, context=""):
        """
        Generates a pre-meeting brief.
        target_name: Company or Person name
        context: Additional info (e.g., "SaaS company", "CTO")
        """
        workflow_id = str(uuid.uuid4())
        self.event_log.log({
            "type": "workflow.started",
            "payload": {"target": target_name, "agent": self.agent_name},
            "workflow_id": workflow_id
        })

        # 1. Prepare Prompt
        base_prompt = self.load_prompt("research/brief_generation.txt")
        filled_prompt = base_prompt.replace("{{target_name}}", target_name)\
                                   .replace("{{context}}", context)
        
        # 2. Call Perplexity (instead of Gemini)
        try:
            response_text = self.perplexity.research(filled_prompt)
            
            # Clean response (remove markdown if present - same logic as BaseAgent but applied to Pplx result)
            clean_text = response_text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:]
            if clean_text.startswith("```"):
                clean_text = clean_text[3:]
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]
            clean_text = clean_text.strip()
            
            result = json.loads(clean_text)
            
            self.event_log.log({
                "type": "research.completed",
                "payload": {"target": target_name, "data_points": len(result)},
                "workflow_id": workflow_id
            })
            return result
            
        except Exception as e:
            self.event_log.log({
                "type": "research.failed",
                "payload": {"error": str(e)},
                "workflow_id": workflow_id,
                "severity": "error"
            })
            return {"error": str(e)}

if __name__ == "__main__":
    agent = ResearchAgent()
    brief = agent.generate_brief("Vercel", "Frontend Cloud Platform")
    print(json.dumps(brief, indent=2))
