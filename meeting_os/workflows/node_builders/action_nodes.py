def create_notion_action_nodes(action_generators):
    """
    Creates n8n Notion nodes based on action generators.
    """
    nodes = []
    x_pos = 1000 # Start position
    
    for action in action_generators:
        action_type = action["action_type"]
        params = action["params"]
        
        node_name = action_type.replace("_", " ").title()
        
        node = {
            "parameters": {},
            "name": node_name,
            "type": "n8n-nodes-base.notion",
            "typeVersion": 2,
            "position": [x_pos, 300]
        }
        
        if action_type == "create_or_update_opportunity":
            # Configure for Opportunity Database
            node["parameters"] = {
                "resource": "databasePage",
                "operation": "create",
                "databaseId": {"__rl": True, "value": "NOTION_OPPORTUNITY_DB_ID", "mode": "id"},
                "title": {"title": params.get("name", "")},
                "propertiesUi": {
                    "propertyValues": [
                        {"key": "Stage|select", "selectValue": params.get("stage", "")},
                        {"key": "Value|number", "numberValue": params.get("value", 0)},
                        {"key": "Close Date|date", "date": params.get("close_date", "")}
                    ]
                }
            }
        elif action_type == "create_or_update_company":
             # Configure for Company Database
            node["parameters"] = {
                "resource": "databasePage",
                "operation": "create",
                "databaseId": {"__rl": True, "value": "NOTION_COMPANY_DB_ID", "mode": "id"},
                "title": {"title": params.get("name", "")},
                 # Add mapping logic for domain/duplicates if complex
            }
            
        nodes.append(node)
        x_pos += 200
        
    return nodes
