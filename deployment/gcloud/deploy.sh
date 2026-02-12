#!/bin/bash

# Meeting OS - Google Cloud Run Deployment Script
# ================================================

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}  Meeting OS Cloud Run Deployment${NC}"
echo -e "${BLUE}=====================================${NC}\n"

# Configuration
PROJECT_ID="meeting-os-prod"  # Change this to your GCP project ID
REGION="us-central1"
SERVICE_NAME="meeting-os"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"
if ! command_exists gcloud; then
    echo -e "${RED}Error: gcloud CLI is not installed${NC}"
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

if ! command_exists docker; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    echo "Please install Docker Desktop"
    exit 1
fi

# Set the project
echo -e "\n${YELLOW}Setting GCP project...${NC}"
gcloud config set project ${PROJECT_ID} || {
    echo -e "${RED}Error: Could not set project ${PROJECT_ID}${NC}"
    echo "Please create the project first or update PROJECT_ID in this script"
    exit 1
}

# Enable required APIs
echo -e "\n${YELLOW}Enabling required APIs...${NC}"
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    artifactregistry.googleapis.com \
    secretmanager.googleapis.com \
    containerregistry.googleapis.com

# Build the Docker image
echo -e "\n${YELLOW}Building Docker image...${NC}"
docker build -t ${IMAGE_NAME}:latest -f deployment/docker/Dockerfile .

# Configure Docker for GCR
echo -e "\n${YELLOW}Configuring Docker for GCR...${NC}"
gcloud auth configure-docker

# Push the image to GCR
echo -e "\n${YELLOW}Pushing image to Google Container Registry...${NC}"
docker push ${IMAGE_NAME}:latest

# Create secrets in Secret Manager for sensitive environment variables
echo -e "\n${YELLOW}Setting up Secret Manager for environment variables...${NC}"
echo -e "${BLUE}Note: You'll need to manually add your API keys to Secret Manager${NC}"

# List of secrets to create
SECRETS=(
    "notion-api-key"
    "google-api-key"
    "perplexity-api-key"
    "fireflies-api-key"
    "supabase-url"
    "supabase-key"
    "kapso-api-key"
    "whatsapp-phone-id"
    "slack-bot-token"
    "kapso-verify-token"
)

for secret in "${SECRETS[@]}"; do
    if gcloud secrets describe ${secret} --project=${PROJECT_ID} >/dev/null 2>&1; then
        echo "Secret ${secret} already exists"
    else
        echo "Creating secret: ${secret}"
        echo "PLACEHOLDER" | gcloud secrets create ${secret} --data-file=- --replication-policy=automatic
        echo -e "${YELLOW}Remember to update ${secret} with the actual value${NC}"
    fi
done

# Deploy to Cloud Run
echo -e "\n${YELLOW}Deploying to Cloud Run...${NC}"
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME}:latest \
    --region ${REGION} \
    --platform managed \
    --allow-unauthenticated \
    --memory 1Gi \
    --cpu 2 \
    --max-instances 10 \
    --min-instances 1 \
    --port 8080 \
    --set-env-vars PORT=8080

# Get the service URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} \
    --region ${REGION} \
    --format 'value(status.url)')

echo -e "\n${GREEN}=====================================${NC}"
echo -e "${GREEN}  Deployment Complete!${NC}"
echo -e "${GREEN}=====================================${NC}"
echo -e "\n${BLUE}Service URL:${NC} ${SERVICE_URL}"
echo -e "\n${YELLOW}Next Steps:${NC}"
echo "1. Update secrets in Secret Manager with actual values:"
echo "   gcloud secrets versions add SECRET_NAME --data-file=-"
echo ""
echo "2. Update Cloud Run service to use secrets:"
echo "   Run: ./update-secrets.sh"
echo ""
echo "3. Configure webhooks in external services:"
echo "   - Fireflies: ${SERVICE_URL}/webhook/fireflies"
echo "   - WhatsApp/Kapso: ${SERVICE_URL}/webhook/kapso"
echo "   - Generic: ${SERVICE_URL}/webhook"
echo ""
echo "4. Test the deployment:"
echo "   curl ${SERVICE_URL}/"
echo ""
echo -e "${GREEN}Happy Meeting Intelligence! 🚀${NC}"