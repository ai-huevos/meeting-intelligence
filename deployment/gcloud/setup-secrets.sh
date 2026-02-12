#!/bin/bash

# Meeting OS - Setup Secrets from .env file
# ==========================================
# This script reads your .env file and creates/updates secrets in GCP Secret Manager

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}  Setting up GCP Secrets from .env${NC}"
echo -e "${BLUE}=====================================${NC}\n"

# Configuration
PROJECT_ID="meeting-os-prod"  # Change this to match your project

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${RED}Error: .env file not found${NC}"
    echo "Please ensure you're running this from the project root"
    exit 1
fi

echo -e "${YELLOW}Reading .env file and creating/updating secrets...${NC}\n"

# Function to create or update a secret
update_secret() {
    local secret_name=$1
    local secret_value=$2

    # Convert to lowercase and replace underscores with hyphens for GCP secret names
    local gcp_secret_name=$(echo "$secret_name" | tr '[:upper:]' '[:lower:]' | tr '_' '-')

    echo -n "Setting ${gcp_secret_name}... "

    # Check if secret exists
    if gcloud secrets describe ${gcp_secret_name} --project=${PROJECT_ID} >/dev/null 2>&1; then
        # Update existing secret
        echo -n "${secret_value}" | gcloud secrets versions add ${gcp_secret_name} \
            --data-file=- --project=${PROJECT_ID} >/dev/null 2>&1
        echo -e "${GREEN}updated${NC}"
    else
        # Create new secret
        echo -n "${secret_value}" | gcloud secrets create ${gcp_secret_name} \
            --data-file=- --replication-policy=automatic --project=${PROJECT_ID} >/dev/null 2>&1
        echo -e "${GREEN}created${NC}"
    fi
}

# Read .env file and process each line
while IFS='=' read -r key value; do
    # Skip empty lines and comments
    if [[ -z "$key" || "$key" == \#* ]]; then
        continue
    fi

    # Remove any quotes from the value
    value="${value%\"}"
    value="${value#\"}"
    value="${value%\'}"
    value="${value#\'}"

    # Process specific keys we need for deployment
    case "$key" in
        NOTION_API_KEY|\
        GOOGLE_API_KEY|\
        PERPLEXITY_API_KEY|\
        FIREFLIES_API_KEY|\
        SUPABASE_URL|\
        SUPABASE_KEY|\
        KAPSO_API_KEY|\
        WHATSAPP_PHONE_ID|\
        SLACK_BOT_TOKEN)
            update_secret "$key" "$value"
            ;;
        *)
            # Skip other variables
            ;;
    esac
done < .env

# Add KAPSO_VERIFY_TOKEN if not in .env (with a default value)
echo -n "Setting kapso-verify-token... "
DEFAULT_VERIFY_TOKEN="meeting-os-verify-$(date +%s)"
echo -n "${DEFAULT_VERIFY_TOKEN}" | gcloud secrets create kapso-verify-token \
    --data-file=- --replication-policy=automatic --project=${PROJECT_ID} >/dev/null 2>&1 || \
echo -n "${DEFAULT_VERIFY_TOKEN}" | gcloud secrets versions add kapso-verify-token \
    --data-file=- --project=${PROJECT_ID} >/dev/null 2>&1
echo -e "${GREEN}set (Token: ${DEFAULT_VERIFY_TOKEN})${NC}"

echo -e "\n${GREEN}=====================================${NC}"
echo -e "${GREEN}  Secrets Setup Complete!${NC}"
echo -e "${GREEN}=====================================${NC}"
echo -e "\n${YELLOW}Next step:${NC} Run ./update-secrets.sh to link these secrets to Cloud Run"
echo -e "\n${BLUE}Important:${NC} Save this WhatsApp verification token: ${DEFAULT_VERIFY_TOKEN}"
echo "You'll need it when configuring the WhatsApp webhook in Meta Business"