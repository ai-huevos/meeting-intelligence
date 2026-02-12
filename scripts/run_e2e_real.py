from meeting_os.services.google_calendar import GoogleCalendarClient
from meeting_os.services.enrichment.enrichment_router import EnrichmentRouter
from meeting_os.services.fireflies import FirefliesClient
import os

def run_full_e2e_real():
    print("🚀 Starting Full E2E with Real Data...")
    
    # 1. Calendar (Real)
    # Requires oauth flow first time. If not authed, this might hang or fail.
    # Since we are in a headless env, we assume the user will authorize locally if prompted 
    # OR we use the mock if auth fails to avoid blocking the user.
    print("📅 1. Checking Calendar (Real)...")
    try:
        if os.path.exists("token.json"): # Only use real if token exists (already authed)
            calendar = GoogleCalendarClient(mock_mode=False)
        else:
            # First time run - we can't do interactive auth here easily.
            print("   ⚠️ No token.json found. Interactive auth required. Falling back to Mock for this run.")
            calendar = GoogleCalendarClient(mock_mode=True)
            
        events = calendar.list_upcoming_meetings()
        print(f"   Found {len(events)} events.")
    except Exception as e:
        print(f"   ❌ Calendar Error: {e}")
        events = []

    # 2. Enrichment (Real Perplexity)
    print("\n🧠 2. Running Research (Real Perplexity)...")
    router = EnrichmentRouter()
    # Test with a known target if no events found
    if not events:
        print("   No events found. Testing with 'Anthropic'.")
        brief = router.research_agent.generate_brief("Anthropic", "AI Lab")
        print(f"   Brief Generated: {len(str(brief))} chars.")
    else:
        for event in events[:1]:
            router.enrich_meeting_participants(event)

    # 3. Transcript Processing (Real Fireflies Logic)
    print("\n📝 3. Checking Fireflies (Real)...")
    ff_client = FirefliesClient()
    try:
        latest = ff_client.get_latest_meeting()
        if latest:
            print(f"   Likely Real Meeting Found: {latest['title']}")
        else:
            print("   No recent meetings in Fireflies (or Key invalid).")
    except Exception as e:
        print(f"   ❌ Fireflies Error: {e}")

    print("\n✅ E2E Check Complete.")

if __name__ == "__main__":
    run_full_e2e_real()
