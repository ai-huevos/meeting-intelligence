import json
import os
from meeting_os.workflows.generator import WorkflowGenerator

def generate_cos():
    print("Generating Chief of Staff Workflow...")
    
    with open("meeting_os/agent-templates/cos_agent_template.json", "r") as f:
        template = json.load(f)
        
    generator = WorkflowGenerator()
    workflow = generator.generate_workflow(template)
    
    output_path = "meeting_os/cos_workflow.json"
    with open(output_path, "w") as f:
        json.dump(workflow, f, indent=2)
        
    print(f"✅ Workflow saved to {output_path}")
    
    # Verify Linear Node exists
    nodes = workflow.get("nodes", [])
    linear_nodes = [n for n in nodes if "linear" in n["type"].lower()]
    if linear_nodes:
        print(f"✅ Found {len(linear_nodes)} Linear Node(s).")
    else:
        print("❌ No Linear Nodes found!")

if __name__ == "__main__":
    generate_cos()
