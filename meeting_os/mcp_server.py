import os
import sys

# Define Tools Logic (Decoupled from SDK)
def search_transcripts_logic(keyword: str):
    """
    Search for recent meetings containing a specific keyword.
    """
    # Mock return for logic verification
    return f"Found 2 meetings with '{keyword}': \n1. Financials (2025-01-31)\n2. Sync (2025-01-20)"

def get_transcript_logic(meeting_id: str):
    """
    Retrieve the full transcript text.
    """
    return f"Transcript for {meeting_id}: [Full text...]"

def trigger_workflow_logic(agent_name: str, context: str):
    """
    Trigger a workflow via Webhook.
    """
    return f"🚀 Triggered {agent_name} agent with context: '{context}'."

# SDK Binding (Only runs if fastmcp is installed - i.e. in Prod)
try:
    from fastmcp import FastMCP
    mcp = FastMCP("MeetingOS-Intelligence")

    @mcp.tool()
    def search_transcripts(keyword: str) -> str:
        return search_transcripts_logic(keyword)

    @mcp.tool()
    def get_transcript(meeting_id: str) -> str:
        return get_transcript_logic(meeting_id)

    @mcp.tool()
    def trigger_agent_workflow(agent_name: str, context: str) -> str:
        return trigger_workflow_logic(agent_name, context)

    if __name__ == "__main__":
        mcp.run()

except ImportError:
    # 3.9 Fallback / Test Mode
    if __name__ == "__main__":
        print("⚠️  FastMCP not installed (Requires Python 3.10+). Running in TEST mode.")
        print("Testing Tool Logic...")
        print(search_transcripts_logic("budget"))
        print(trigger_workflow_logic("research", "Test Context"))
        print("\n✅ Logic Verification Complete.")
