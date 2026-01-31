import os
import datetime
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class GoogleCalendarClient:
    """
    Client for fetching Google Calendar events.
    Supporting Mock mode for development without credentials.
    """
    
    def __init__(self, mock_mode=True):
        self.mock_mode = mock_mode
        self.creds = None
        self.service = None
        
        if not mock_mode:
            self._authenticate()

    def _authenticate(self):
        """Standard Google Auth flow."""
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if os.path.exists('credentials.json'):
                    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                    self.creds = flow.run_local_server(port=0)
                    with open('token.json', 'w') as token:
                        token.write(self.creds.to_json())
                else:
                     print("Warning: credentials.json not found. Switching to mock mode.")
                     self.mock_mode = True
                     return

        self.service = build('calendar', 'v3', credentials=self.creds)

    def list_upcoming_meetings(self, max_results=10):
        """
        List upcoming meetings with external participants.
        """
        if self.mock_mode:
            return self._get_mock_meetings()
            
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = self.service.events().list(
            calendarId='primary', timeMin=now,
            maxResults=max_results, singleEvents=True,
            orderBy='startTime').execute()
        return self._filter_events(events_result.get('items', []))

    def _filter_events(self, events):
        """Filter for relevant external meetings."""
        filtered = []
        for event in events:
            attendees = event.get('attendees', [])
            # Simple heuristic: if any attendee is not internal domain (tbd for now)
            # In real app, check against internal domain list
            external_attendees = [a['email'] for a in attendees if '@gmail.com' not in a['email']] # Placeholder logic
            
            if external_attendees or 'meeting' in event.get('summary', '').lower():
                 filtered.append({
                     "id": event['id'],
                     "summary": event.get('summary'),
                     "start": event['start'].get('dateTime', event['start'].get('date')),
                     "attendees": [a.get('email') for a in attendees],
                     "description": event.get('description', '')
                 })
        return filtered

    def _get_mock_meetings(self):
        """Return sample data for testing pipeline."""
        return [
            {
                "id": "mock_1",
                "summary": "Sales Demo with Acme Corp",
                "start": (datetime.datetime.now() + datetime.timedelta(hours=2)).isoformat(),
                "attendees": ["founder@acme.com", "tatooine@tbd.com"],
                "description": "Discussing Q1 Pilot."
            },
            {
                "id": "mock_2",
                "summary": "Sync with Linear",
                "start": (datetime.datetime.now() + datetime.timedelta(days=1)).isoformat(),
                "attendees": ["pm@linear.app"],
                "description": "Integration roadmap."
            }
        ]

if __name__ == "__main__":
    client = GoogleCalendarClient(mock_mode=True)
    events = client.list_upcoming_meetings()
    print(json.dumps(events, indent=2))
