# Meeting OS: Co-Founder Testing Guide 🤝

This guide explains how **Team Members** (non-developers) can test and use the system.

## 1. Context
We have built a "Meeting OS" that listens to meetings, extracts data, and updates our tools (Notion/Slack/Linear). It runs 24/7 in the cloud (Render).

**Your Role**:
1.  **Feed the Beast**: Record meetings.
2.  **Verify Output**: Check Slack/Notion.
3.  **Command It**: (Optional) Chat with it via Cursor/Claude.

## 2. Setup (10 Mins)

### A. Shared Accounts (Foundations)
Ensure you have access to:
1.  **Notion**: The `Meeting OS` Page/Database.
2.  **Slack**: The `#alerts-meeting-os` channel.
3.  **Fireflies**: The shared account (or auto-join enabled).

### B. The "Power User" Setup (Optional)
If you want to *chat* with the data (like "What did we decide yesterday?"), install **Cursor** or **Claude Desktop**.
1.  Install Cursor.
2.  Settings -> Features -> MCP.
3.  Add the **MeetingOS Server**:
    -   Command: `npx -y fastmcp run mcp_server.py` (Ask your tech co-founder for the exact path/repo connection).

## 3. How to Test (The Loop)

### Scenario 1: The "Passive" Test
1.  **Have a Meeting**: Ensure Fireflies joins (or upload a recording to Fireflies).
2.  **Wait**: ~5-10 mins after the meeting ends.
3.  **Check Slack**: Did you get a notification?
    -   *Success*: "🚀 Research Agent finished processing..."
4.  **Check Notion**: Is there a new row in the Meetings database? Are there new Tasks?

### Scenario 2: The "Active" Test (WhatsApp)
1.  **Send a Message**: WhatsApp the Kapso Bot Number.
    -   *Text*: "Update on the Acme Contract?"
2.  **Wait**: The `CoS Agent` should reply via WhatsApp or Slack.

## 4. Troubleshooting
-   **"I didn't get a Slack msg"**: Check Fireflies. Did it generate a transcript?
-   **"The answer was wrong"**: Report it in the `#feedback-loop` channel (The system learns!).
