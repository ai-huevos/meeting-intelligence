#!/bin/bash

# Meeting OS - Local Docker Testing
# ==================================

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo -e "${PURPLE}=====================================${NC}"
echo -e "${PURPLE}  Meeting OS Local Docker Test${NC}"
echo -e "${PURPLE}=====================================${NC}\n"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${RED}Error: .env file not found${NC}"
    echo "Please ensure you have a .env file with your API keys"
    exit 1
fi

# Build Docker image
echo -e "${YELLOW}Building Docker image...${NC}"
docker build -t meeting-os-test:latest -f deployment/docker/Dockerfile .

# Run container
echo -e "${YELLOW}Starting container...${NC}"
docker run -d \
    --name meeting-os-test \
    -p 8080:8080 \
    --env-file .env \
    meeting-os-test:latest

# Wait for service to start
echo -e "${YELLOW}Waiting for service to start...${NC}"
sleep 5

# Test health endpoint
echo -e "${BLUE}Testing health endpoint...${NC}"
response=$(curl -s http://localhost:8080/)
if echo "$response" | grep -q "Meeting OS"; then
    echo -e "${GREEN}✅ Health check passed${NC}"
    echo "Response: $response"
else
    echo -e "${RED}❌ Health check failed${NC}"
    echo "Response: $response"
fi

# View logs
echo -e "\n${YELLOW}Container logs:${NC}"
docker logs meeting-os-test | tail -20

# Cleanup
echo -e "\n${YELLOW}Cleaning up...${NC}"
docker stop meeting-os-test
docker rm meeting-os-test

echo -e "\n${GREEN}Local test complete!${NC}"
echo -e "${BLUE}If all tests passed, you can deploy with:${NC}"
echo "  cd deployment/gcloud && ./deploy.sh"