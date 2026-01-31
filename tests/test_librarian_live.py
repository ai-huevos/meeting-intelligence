import os
import sys

# Add parent dir to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from meeting_os.agents.librarian_agent import LibrarianAgent
from meeting_os.lib.tenancy.vault_context import TenantContext

def test_librarian_live():
    # Setup context
    TenantContext.set_vault("test_vault_1", "user_test")
    
    # Read transcript
    transcript_path = "/Users/tatooine/Documents/Development/tbd/meeting-transcripts/Pricing-AI-Huevos-2f72b1c3-4393.md"
    try:
        with open(transcript_path, "r") as f:
            transcript = f.read()
    except Exception as e:
        print(f"Error reading transcript: {e}")
        return

    print(f"Transcript loaded. Length: {len(transcript)} chars")
    
    # Initialize Agent
    agent = LibrarianAgent()
    
    # Run Classification
    print("Running classification...")
    result = agent.classify_meeting("test_meeting_id_1", transcript)
    
    print("\nResult:")
    print(result)

if __name__ == "__main__":
    test_librarian_live()
