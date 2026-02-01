# Deployment: From Laptop to the Cloud

You asked: *"I just did all that in kapso, what else should I need to do to what you call production y deploy"*

## 1. The Concept
*   **Development (Local)**:
    *   **Where**: Your laptop.
    *   **State**: You start the script manually (`python scripts/...`). It stops when you close the terminal or sleep the computer.
    *   **Data**: Uses your local `.env` file for secrets.
    *   **Kapso**: Uses "Sandbox" mode for free testing.

*   **Production (Cloud)**:
    *   **Where**: A server (Render, AWS, Heroku) that never sleeps.
    *   **State**: The app runs automatically, forever. It wakes up on schedules (CRON) or events (Webhooks).
    *   **Data**: Uses "Environment Variables" configured in the cloud dashboard (NOT a file).
    *   **Kapso**: Uses "Live" mode with real phone numbers and paid templates.

## 2. Your Deployment Checklist (Render)
To "Deploy" means to push your code to the server so it starts running `Production` mode.

1.  **Push Code**: You already did this (`git push origin development`).
2.  **Create Service in Render**:
    *   Go to Render Dashboard -> New -> Web Service (or Blueprint).
    *   Connect your Github Repo (`meeting-intelligence`).
    *   **Runtime**: Python 3.
    *   **Build Command**: `pip install -r requirements.txt`.
    *   **Start Command**: `gunicorn meeting_os.mcp_server:app` (or your specific entry point script).
3.  **Add Secrets**:
    *   Copy every line from your local `.env` -> Render "Environment" tab.
    *   **Crucial Switch**: Validated `KAPSO_API_KEY` and `WHATSAPP_PHONE_ID` for the **Live/Production** account (8733...), NOT the Sandbox.
4.  **Google Auth**:
    *   Production servers cannot open a browser window to click "Allow".
    *   **Solution**: Upload your locally generated `token.json` as a "Secret File" in Render (path: `/etc/secrets/token.json` or similar) OR stick to the Base64 env var method described in `DEPLOYMENT.md`.

## 3. What Happens Next?
Once deployed:
*   The "Server" listens for incoming WhatsApp messages 24/7.
*   It runs the daily prep script automatically at 8 AM (if configured as a Cron Job).
*   You don't need to touch your laptop for the bot to work.
