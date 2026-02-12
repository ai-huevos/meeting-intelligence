#!/bin/bash

# Meeting OS - Update Cloud Run Service with Secrets
# ===================================================

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}  Updating Cloud Run with Secrets${NC}"
echo -e "${BLUE}=====================================${NC}\n"

# Configuration
PROJECT_ID="meeting-os-prod"  # Change this to match your project
REGION="us-central1"
SERVICE_NAME="meeting-os"

echo -e "${YELLOW}Updating Cloud Run service with Secret Manager references...${NC}"

gcloud run services update ${SERVICE_NAME} \
    --region ${REGION} \
    --update-secrets \
NOTION_API_KEY=notion-api-key:latest,\
GOOGLE_API_KEY=google-api-key:latest,\
PERPLEXITY_API_KEY=perplexity-api-key:latest,\
FIREFLIES_API_KEY=fireflies-api-key:latest,\
SUPABASE_URL=supabase-url:latest,\
SUPABASE_KEY=supabase-key:latest,\
KAPSO_API_KEY=kapso-api-key:latest,\
WHATSAPP_PHONE_ID=whatsapp-phone-id:latest,\
SLACK_BOT_TOKEN=slack-bot-token:latest,\
KAPSO_VERIFY_TOKEN=kapso-verify-token:latest

echo -e "\n${GREEN}✅ Secrets updated successfully!${NC}"
echo -e "\n${YELLOW}Note: Make sure you've added the actual secret values:${NC}"
echo "Example:"
echo "  echo -n 'your-actual-api-key' | gcloud secrets versions add notion-api-key --data-file=-"