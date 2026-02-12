import json
import uuid
import os
# Import node builders
# Import node builders
from meeting_os.workflows.node_builders.trigger_nodes import create_trigger_node, create_filter_nodes
from meeting_os.workflows.node_builders.classification_nodes import create_classification_nodes
from meeting_os.workflows.node_builders.extraction_nodes import create_extraction_node
from meeting_os.workflows.node_builders.action_nodes import create_notion_action_nodes
from meeting_os.workflows.node_builders.linear_nodes import create_linear_node

class WorkflowGenerator:
    def __init__(self):
        pass

    def generate_workflow(self, agent_template, customization_config=None):
        """
        Generates n8n workflow JSON from agent template.
        """
        customization_config = customization_config or {}
        
        agent_name = agent_template.get("agent_name", "Unnamed_Agent")
        domain_name = agent_template.get("domain_name", agent_name)
        
        workflow = {
            "name": f"{domain_name}_Workflow",
            "nodes": [],
            "connections": {},
            "meta": {
                "instanceId": str(uuid.uuid4())
            }
        }
        
        previous_node_name = None
        
        # 1. Add trigger node
        # Handle 'triggers' (new format) vs 'trigger_conditions' (old format)
        triggers = agent_template.get("triggers", agent_template.get("trigger_conditions", []))
        trigger_node = create_trigger_node(triggers)
        workflow["nodes"].append(trigger_node)
        previous_node_name = trigger_node["name"]
        
        # 2. Add Extraction Node
        if "extraction_schema" in agent_template:
            prompt_text = customization_config.get("extraction_prompt", "Extract info...")
            extraction_node = create_extraction_node(agent_template["extraction_schema"], prompt_text)
            workflow["nodes"].append(extraction_node)
            self._add_connection(workflow, previous_node_name, extraction_node["name"])
            previous_node_name = extraction_node["name"]
            
        # 3. Add Action Nodes
        # Support 'actions' (new) and 'action_generators' (old)
        actions = agent_template.get("actions", [])
        if not actions and "action_generators" in agent_template:
            actions = agent_template["action_generators"].get("crm_actions", [])
            
        # 3a. Notion Actions
        notion_actions = [a for a in actions if "notion" in a.get("action_type", "") or "opportunity" in a.get("action_type", "") or "company" in a.get("action_type", "")]
        for i, action in enumerate(notion_actions):
            # Wrap in list because create_notion_action_nodes expects list
            nodes = create_notion_action_nodes([action]) 
            for node in nodes:
                workflow["nodes"].append(node)
                self._add_connection(workflow, previous_node_name, node["name"])
                
        # 3b. Linear Actions
        linear_actions = [a for a in actions if "linear" in a.get("action_type", "")]
        for action in linear_actions:
            node = create_linear_node(action.get("params", {}), iterator_index=0)
            workflow["nodes"].append(node)
            self._add_connection(workflow, previous_node_name, node["name"])
        
        return workflow

    def _add_connection(self, workflow, source_name, target_name):
        """Helper to link nodes"""
        if source_name not in workflow["connections"]:
            workflow["connections"][source_name] = {"main": []}
        
        workflow["connections"][source_name]["main"].append([
            {
                "node": target_name,
                "type": "main",
                "index": 0
            }
        ])

if __name__ == "__main__":
    # Test execution
    template_path = os.path.join(os.path.dirname(__file__), "..", "..", "agent-templates", "sales_agent_template.json")
    with open(template_path, "r") as f:
        template = json.load(f)
    
    # Load prompt
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "..", "prompts", "extraction", "sales_extraction.txt")
    with open(prompt_path, "r") as f:
        prompt_text = f.read()

    generator = WorkflowGenerator()
    wf = generator.generate_workflow(template, customization_config={"extraction_prompt": prompt_text})
    
    # Save to file
    output_path = os.path.join(os.path.dirname(__file__), "..", "..", "sales_workflow.json")
    with open(output_path, "w") as f:
         json.dump(wf, f, indent=2)
         
    print(f"Generated workflow saved to {output_path}")
