from meeting_os.agents.research_agent import ResearchAgent
from meeting_os.lib.observability.event_log import EventLog

class EnrichmentRouter:
    """
    Routes enrichment requests based on type and budget.
    """
    
    def __init__(self):
        self.event_log = EventLog()
        self.research_agent = ResearchAgent(self.event_log)
        self.daily_budget_usd = 5.0 # Example limit
        self.current_spend = 0.0

    def enrich_meeting_participants(self, meeting_event):
        """
        Main entry point: Enrich a calendar event.
        """
        summary = meeting_event.get("summary", "")
        attendees = meeting_event.get("attendees", [])
        
        # heuristic: extract company from summary or email domain
        targets = self._identify_targets(summary, attendees)
        results = {}
        
        for target in targets:
            if not self._check_budget():
                print("Budget exceeded, skipping enrichment.")
                break
                
            print(f"Enriching target: {target}...")
            brief = self.research_agent.generate_brief(target, context=f"Meeting: {summary}")
            results[target] = brief
            
            # Mock cost tracking
            self._track_cost(0.01) # Perplexity call approx cost
            
        return results

    def _identify_targets(self, summary, attendees):
        """
        Identify who to research.
        Simple logic: exclude internal, try to parse company name.
        """
        targets = []
        # 1. Look for 'with X' in summary
        if " with " in summary:
            parts = summary.split(" with ")
            if len(parts) > 1:
                targets.append(parts[1].strip())
        
        # 2. Look at domains
        ignored_domains = ["gmail.com", "tbd.com", "yahoo.com"]
        for email in attendees:
            if "@" in email:
                domain = email.split("@")[1]
                if domain not in ignored_domains:
                   # Use domain as target (Research Agent can handle "vercel.com")
                   targets.append(domain)
        
        return list(set(targets)) # Dedup

    def _check_budget(self):
        return self.current_spend < self.daily_budget_usd

    def _track_cost(self, amount):
        self.current_spend += amount
        self.event_log.log({
            "type": "cost.tracked",
            "payload": {"amount": amount, "total_spend": self.current_spend}
        })

if __name__ == "__main__":
    router = EnrichmentRouter()
    mock_event = {
        "summary": "Intro Call with OpenAI",
        "attendees": ["sam@openai.com"]
    }
    results = router.enrich_meeting_participants(mock_event)
    import json
    print(json.dumps(results, indent=2))
