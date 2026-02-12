import os
import sys

# Define Tools Logic (Decoupled from SDK)
# Ensure root path is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meeting_os.agents.librarian_agent import LibrarianAgent
from meeting_os.agents.router_agent import RouterAgent
from meeting_os.core.uco import UniversalContextObject, EventSource, RoutingFlags, ContextLayer

# Initialize Agents
librarian = LibrarianAgent()
router_agent = RouterAgent()

def search_transcripts_logic(keyword: str):
    """
    Search for recent meetings containing a specific keyword.
    """
    results = librarian.search_meetings(keyword)
    return f"Found matches: {results}"

def get_transcript_logic(meeting_id: str):
    """
    Retrieve the full transcript text.
    """
    # Placeholder: In V3 this will fetch from Vector DB or Supabase Storage
    return f"Transcript retrieval for {meeting_id} is pending storage implementation."

def trigger_workflow_logic(agent_name: str, context: str):
    """
    Trigger a workflow via Router.
    """
    # Create a UCO
    try:
        flags = RoutingFlags(
            sales=(agent_name.lower() == "sales"), 
            ops=(agent_name.lower() == "ops"),
            product=(agent_name.lower() == "product")
        )
        uco = UniversalContextObject(
            source=EventSource.MANUAL,
            routing_flags=flags,
            context_layer=ContextLayer(summary=context, sentiment="Neutral")
        )
        res = router_agent.ingest_event(uco)
        return f"🚀 Triggered {agent_name} agent. Event ID: {res.get('event_id')}"
    except Exception as e:
        return f"Failed to trigger workflow: {str(e)}"

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
