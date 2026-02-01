import os
import requests
from dotenv import load_dotenv

load_dotenv()

class FirefliesClient:
    """
    Client for interacting with Fireflies.ai API.
    Used to fetch real transcripts instead of using mock files.
    """
    BASE_URL = "https://api.fireflies.ai/graphql"
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("FIREFLIES_API_KEY")
        if not self.api_key:
            print("WARNING: FIREFLIES_API_KEY not found. Client will fail calls.")
            
    def get_transcript(self, meeting_id):
        """
        Fetch transcript for a specific meeting ID.
        """
        query = """
        query Transcript($id: String!) {
            transcript(id: $id) {
                id
                title
                sentences {
                    text
                    speaker_name
                }
            }
        }
        """
        
        response = requests.post(
            self.BASE_URL,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"query": query, "variables": {"id": meeting_id}}
        )
        
        if response.status_code == 200:
            data = response.json()
            # Parse into a single string (similar to our markdown format)
            if "data" in data and "transcript" in data["data"]:
                sentences = data["data"]["transcript"]["sentences"]
                full_text = "\n".join([f"{s['speaker_name']}: {s['text']}" for s in sentences])
                return full_text
            else:
                return None
        else:
            raise Exception(f"Fireflies API Error: {response.text}")

    def get_latest_meeting(self):
        """
        Fetch the most recent meeting transcript.
        """
        # Note: simplistic query, real usage might filter by date
        query = """
        query {
            transcripts(limit: 1) {
                id
                title
                date
            }
        }
        """
        response = requests.post(
            self.BASE_URL,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"query": query}
        )
        if response.status_code == 200:
             data = response.json()
             if "data" in data and "transcripts" in data["data"] and len(data["data"]["transcripts"]) > 0:
                 return data["data"]["transcripts"][0]
        return None

if __name__ == "__main__":
    client = FirefliesClient()
    # Try to fetch latest meeting info (won't work without real ID usually, but tests connection)
    try:
        latest = client.get_latest_meeting()
        if latest:
            print(f"Latest meeting: {latest['title']} ({latest['id']})")
            # transcript = client.get_transcript(latest['id'])
            # print(transcript[:200])
        else:
            print("No recent meetings found or API key invalid.")
    except Exception as e:
        print(f"Error: {e}")
