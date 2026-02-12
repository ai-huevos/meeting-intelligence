import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class PerplexityClient:
    """
    Client for interacting with Perplexity API (sonar-reasoning-pro or sonar-pro).
    """
    BASE_URL = "https://api.perplexity.ai/chat/completions"
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise ValueError("PERPLEXITY_API_KEY not found.")
            
    def research(self, query, model="sonar-pro"):
        """
        Perform a research query.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a B2B Research Expert. Provide accurate, factual information."
                },
                {
                    "role": "user",
                    "content": query
                }
            ]
        }
        
        try:
            response = requests.post(self.BASE_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Perplexity API Error: {e}")
            raise

if __name__ == "__main__":
    # Quick Test
    client = PerplexityClient()
    print(client.research("What is the latest funding round for Linear app?"))
