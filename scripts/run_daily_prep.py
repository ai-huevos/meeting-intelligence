import sys
import os
import json

# Fix path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meeting_os.lib.integrations.google_calendar import GoogleCalendarClient
from meeting_os.lib.enrichment.enrichment_router import EnrichmentRouter

def run_daily_prep():
    print("🚀 Starting Daily Pre-Meeting Prep...")
    
    # 1. Fetch Calendar
    print("📅 Fetching upcoming meetings...")
    calendar = GoogleCalendarClient(mock_mode=True)
    events = calendar.list_upcoming_meetings()
    print(f"Found {len(events)} relevant meetings.")
    
    # 2. Enrich
    router = EnrichmentRouter()
    
    for event in events:
        print(f"\nProcessing: {event['summary']}")
        briefs = router.enrich_meeting_participants(event)
        
        # 3. Output (In real app, send to Slack/Notion)
        for target, brief in briefs.items():
            print(f"\n--- BRIEF FOR {target} ---")
            print(json.dumps(brief, indent=2))
            print("--------------------------")

if __name__ == "__main__":
    run_daily_prep()
