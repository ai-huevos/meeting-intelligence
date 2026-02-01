import json

def create_extraction_node(extraction_schema, prompt_template):
    """
    Creates n8n node for LLM extraction (Gemini).
    """
    schema_str = json.dumps(extraction_schema, indent=2).replace('"', '\\"')
    
    # We construct the prompt to include the schema validation instruction
    full_prompt = f"{prompt_template}\\n\\nOutput JSON matching this schema:\\n{schema_str}\\n\\nTranscript: {{$json.body.transcript}}"
    
    node = {
        "parameters": {
            "method": "POST",
            "url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=GOOGLE_API_KEY",
            "sendHeaders": True,
            "headerParameters": {
                "parameters": [
                    {
                        "name": "Content-Type",
                        "value": "application/json"
                    }
                ]
            },
            "sendBody": True,
            "bodyParameters": {
                "parameters": [
                    {
                        "name": "contents",
                        "value": f"{{ \"parts\": [{{ \"text\": \"{full_prompt}\" }}] }}"
                    },
                    {
                        "name": "generationConfig",
                        "value": "{ \"response_mime_type\": \"application/json\" }" # JSON mode
                    }
                ]
            }
        },
        "name": "Sales Extraction (Gemini)",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 3,
        "position": [
            300,
            300
        ]
    }
    return node
