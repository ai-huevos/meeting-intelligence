import json
from meeting_os.services.llm import LLMClient
from meeting_os.services.learning.doc_retriever import DocRetriever

class TemplateImprover:
    """
    Self-improvement engine.
    Reads an agent template, fetches relevant docs, and proposes upgrades.
    """
    
    def __init__(self, event_log=None):
        self.llm = LLMClient(event_logger=event_log)
        self.retriever = DocRetriever()
        
    def improve_template(self, template_path, focus_area="integrations"):
        """
        Analyze a template file and suggest improvements.
        """
        print(f"🛠️  Improving Template: {template_path}...")
        
        with open(template_path, 'r') as f:
            template_content = f.read()
            
        # 1. Identify Tools in Template
        template_json = json.loads(template_content)
        actions = template_json.get("actions", [])
        
        suggestions = []
        
        for action in actions:
            action_type = action.get("action_type")
            print(f"   Analyzing Action: {action_type}...")
            
            # Simple heuristic mapping
            tool_name = "Notion" if "notion" in action_type else "Unknown"
            
            if tool_name != "Unknown":
                # 2. Retrieve Latest Docs
                docs = self.retriever.get_api_docs(tool_name, f"Params for {action_type}")
                
                if docs:
                    # 3. Ask Gemini to Compare
                    prompt = f"""
                    You are a Senior Systems Architect.
                    Compare our current JSON Action Template with the Latest Documentation found.
                    
                    CURRENT TEMPLATE SEGMENT:
                    {json.dumps(action, indent=2)}
                    
                    LATEST DOCUMENTATION (Retrieved):
                    {docs}
                    
                    Identify missing parameters or deprecated fields.
                    Output a JSON object with a 'suggested_action_update' containing the improved JSON for this action.
                    """
                    
                    response = self.llm.generate_content(prompt)
                    suggestions.append(response)
                    
        return suggestions

if __name__ == "__main__":
    improver = TemplateImprover()
    # Mock path for testing
    import os
    path = "meeting_os/agent-templates/sales_agent_template.json"
    if os.path.exists(path):
        results = improver.improve_template(path)
        for r in results:
            print("\n---------- SUGGESTION ----------")
            print(r)
