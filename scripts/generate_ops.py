import json
import os
from meeting_os.workflows.generator import WorkflowGenerator

def generate_ops():
    print("Generating Ops (Legal/Finance) Workflow...")
    
    with open("meeting_os/agent-templates/ops_agent_template.json", "r") as f:
        template = json.load(f)
        
    generator = WorkflowGenerator()
    workflow = generator.generate_workflow(template)
    
    output_path = "meeting_os/ops_workflow.json"
    with open(output_path, "w") as f:
        json.dump(workflow, f, indent=2)
        
    print(f"✅ Workflow saved to {output_path}")
    
    # Verify Nodes
    nodes = workflow.get("nodes", [])
    print(f"   Nodes Generated: {len(nodes)}")
    types = [n["type"] for n in nodes]
    print(f"   Node Types: {types}")

if __name__ == "__main__":
    generate_ops()
