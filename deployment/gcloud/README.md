# Meeting OS - Google Cloud Run Deployment Guide

## 🚀 Quick Start Deployment

Follow these steps to deploy Meeting OS to Google Cloud Run:

### Prerequisites

1. **Install required tools:**
   - [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
   - [Docker Desktop](https://www.docker.com/products/docker-desktop)

2. **Authenticate with Google Cloud:**
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

### Step-by-Step Deployment

#### 1. Configure Project ID

Edit `deploy.sh` and update the `PROJECT_ID` variable to match your GCP project:
```bash
PROJECT_ID="your-actual-project-id"  # Change this!
```

Do the same in `setup-secrets.sh`, `update-secrets.sh`, and `test-deployment.sh`.

#### 2. Run Deployment

```bash
cd deployment/gcloud
chmod +x *.sh  # Make scripts executable

# Step 1: Deploy the application
./deploy.sh

# Step 2: Setup secrets from your .env file
./setup-secrets.sh

# Step 3: Link secrets to Cloud Run service
./update-secrets.sh

# Step 4: Test the deployment
./test-deployment.sh
```

### 📋 Post-Deployment Configuration

After successful deployment, configure your external services:

#### Fireflies.ai
1. Go to Fireflies Settings → Webhooks
2. Add webhook URL: `https://your-service-url/webhook/fireflies`
3. Select events to trigger webhook

#### WhatsApp Business (Meta/Kapso)
1. Go to Meta Business Dashboard → WhatsApp → Configuration
2. Add webhook URL: `https://your-service-url/webhook/kapso`
3. Use the verification token shown during `setup-secrets.sh`
4. Subscribe to messages webhook events

#### Slack (if using)
1. Go to Slack App settings
2. Update webhook URLs as needed

### 🔧 Troubleshooting

#### View logs:
```bash
gcloud run services logs read meeting-os --region us-central1 --limit 50
```

#### Update environment variable:
```bash
echo -n "new-value" | gcloud secrets versions add secret-name --data-file=-
./update-secrets.sh  # Re-link to Cloud Run
```

#### Redeploy after code changes:
```bash
./deploy.sh  # This rebuilds and redeploys
```

#### Check service status:
```bash
gcloud run services describe meeting-os --region us-central1
```

### 🛡️ Security Notes

- All API keys are stored in Google Secret Manager
- The service allows unauthenticated access (required for webhooks)
- Consider adding IP allowlisting for additional security
- Regularly rotate API keys and update in Secret Manager

### 📊 Monitoring

Set up monitoring in Google Cloud Console:
1. Cloud Run → meeting-os → Metrics
2. Set up alerts for:
   - High error rates
   - High latency
   - Memory usage

### 💰 Cost Optimization

Current configuration:
- Min instances: 1 (always warm)
- Max instances: 10 (auto-scaling)
- Memory: 1GB
- CPU: 2

To reduce costs:
- Set min-instances to 0 (cold starts)
- Reduce memory if not needed
- Use Cloud Scheduler for periodic tasks

### 🆘 Support

For issues:
1. Check logs: `./test-deployment.sh`
2. Verify secrets are set correctly
3. Ensure all external services are configured
4. Check webhook verification tokens match

### 📝 Files in this directory

- `deploy.sh` - Main deployment script
- `setup-secrets.sh` - Import secrets from .env
- `update-secrets.sh` - Link secrets to Cloud Run
- `test-deployment.sh` - Test all endpoints
- `cloudbuild.yaml` - CI/CD configuration (optional)

### 🔄 Continuous Deployment (Optional)

To enable automatic deployment on git push:
1. Connect your GitHub repo to Cloud Build
2. Cloud Build will use `cloudbuild.yaml`
3. Pushes to main will auto-deploy

---

## Environment Variables Reference

| Variable | Description | Where to Get |
|----------|-------------|--------------|
| NOTION_API_KEY | Notion integration key | notion.so/my-integrations |
| GOOGLE_API_KEY | Google/Gemini API key | console.cloud.google.com |
| PERPLEXITY_API_KEY | Perplexity AI key | perplexity.ai/settings |
| FIREFLIES_API_KEY | Fireflies.ai API key | app.fireflies.ai/settings |
| SUPABASE_URL | Supabase project URL | app.supabase.com |
| SUPABASE_KEY | Supabase anon key | app.supabase.com |
| KAPSO_API_KEY | Kapso/WhatsApp key | business.facebook.com |
| WHATSAPP_PHONE_ID | WhatsApp phone ID | business.facebook.com |
| SLACK_BOT_TOKEN | Slack bot OAuth token | api.slack.com/apps |
| KAPSO_VERIFY_TOKEN | Webhook verification | Auto-generated |