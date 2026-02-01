# Google Cloud Run Deployment Guide

You requested a direct, faster alternative to Render. **Google Cloud Run** is the best fit for your stack (Python, Google APIs). It offers:
- **Serverless**: Scales to zero (costs $0 when idle).
- **Security**: Native integration with Google Secrets Manager.
- **Speed**: Deploys containers in seconds.

## 1. Prerequisites
1.  **Google Cloud SDK**: Install `gcloud` CLI.
2.  **Project**: Review your project ID (`gcloud config get-value project`).
3.  **Billing**: Enable billing on GCP.

## 2. Fast Deploy Command
Run this single command to build and deploy your source code directly:

```bash
gcloud run deploy meeting-intelligence \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "SUPABASE_URL=...,KAPSO_API_KEY=..."
```

*Note: For secrets, it is better to use `--set-secrets` linked to Secret Manager.*

## 3. Persistent Storage (The Token Problem)
Cloud Run files are ephemeral. `token.json` will vanish on restart.
**Solution**:
1.  **Mount a generic secret**: Upload `token.json` to Secret Manager and mount it as a file.
2.  **Use Database**: Modify `google_calendar.py` to store/read the token from Supabase instead of a file.

## 4. Comparison: Render vs. Cloud Run

| Feature | Render | Google Cloud Run |
|---|---|---|
| **Setup** | Extremely Easy (Click & Go) | Medium (CLI/Console) |
| **Speed** | Good | **Excellent** (Global Network) |
| **Cost** | Fixed ($7/mo+) | Pay-per-use (likely cheaper for low volume) |
| **Integrations** | Generic | **Native** (Gmail, Calendar, Vertex AI) |
