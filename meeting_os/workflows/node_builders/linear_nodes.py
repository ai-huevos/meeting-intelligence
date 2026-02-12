def create_linear_node(action_params, iterator_index=None):
    """
    Generates an n8n node for creating a Linear Issue.
    """
    # map priority string to Linear priority integer (example)
    # High -> 1, Medium -> 2, Low -> 3
    
    node = {
        "parameters": {
            "resource": "issue",
            "operation": "create",
            "teamId": action_params.get("team_id", "LINEAR_TEAM_ID"),
            "title": action_params.get("title", ""),
            "description": action_params.get("description", ""),
            "priority": 0 # Default to no priority, logic to map string to int would go here in expressions
        },
        "name": "Create Linear Issue",
        "type": "n8n-nodes-base.linear",
        "typeVersion": 1,
        "position": [
            460 + (iterator_index * 200) if iterator_index else 460,
            300
        ],
        "credentials": {
            "linearApi": {
                "id": "LINEAR_CRED_ID",
                "name": "Linear API account"
            }
        }
    }
    return node
