def create_classification_nodes(prompts):
    """
    Creates n8n nodes to call Claude for classification.
    """
    nodes = []
    
    # We create an HTTP Request node to call internal Agent API or direct Anthropic API
    # Assuming direct Anthropic API for now or wrapped via Antigravity API
    
    for key, prompt in prompts.items():
        node = {
            "parameters": {
                "method": "POST",
                "url": "https://api.anthropic.com/v1/messages", # Or internal proxy
                "authentication": "predefinedCredentialType",
                "nodeCredentialType": "anthropicApi",
                "sendHeaders": True,
                "headerParameters": {
                    "parameters": [
                        {
                            "name": "anthropic-version",
                            "value": "2023-06-01"
                        }
                    ]
                },
                "sendBody": True,
                "bodyParameters": {
                    "parameters": [
                        {
                            "name": "model",
                            "value": "claude-3-haiku-20240307"
                        },
                        {
                            "name": "max_tokens",
                            "value": 1024
                        },
                        {
                            "name": "messages",
                            "value": f"[{{ \"role\": \"user\", \"content\": \"{prompt} \\n\\n transcript: {{$json.body.transcript}}\" }}]" 
                        }
                    ]
                }
            },
            "name": f"Classify_{key}",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 3,
            "position": [
                300, 
                300 # Position logic needed
            ]
        }
        nodes.append(node)
        
    return nodes
