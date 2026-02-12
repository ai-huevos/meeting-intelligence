#!/bin/bash

# Meeting OS - Test Cloud Run Deployment
# =======================================

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo -e "${PURPLE}=====================================${NC}"
echo -e "${PURPLE}  Meeting OS Deployment Test Suite${NC}"
echo -e "${PURPLE}=====================================${NC}\n"

# Configuration
PROJECT_ID="meeting-os-prod"
REGION="us-central1"
SERVICE_NAME="meeting-os"

# Get the service URL
echo -e "${YELLOW}Getting service URL...${NC}"
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} \
    --region ${REGION} \
    --project ${PROJECT_ID} \
    --format 'value(status.url)')

if [ -z "$SERVICE_URL" ]; then
    echo -e "${RED}Error: Could not get service URL${NC}"
    echo "Is the service deployed?"
    exit 1
fi

echo -e "${GREEN}Service URL: ${SERVICE_URL}${NC}\n"

# Test function
test_endpoint() {
    local endpoint=$1
    local method=$2
    local data=$3
    local expected_status=$4

    echo -e "${BLUE}Testing ${method} ${endpoint}...${NC}"

    if [ "$method" == "GET" ]; then
        response=$(curl -s -o /dev/null -w "%{http_code}" "${SERVICE_URL}${endpoint}")
    else
        response=$(curl -s -o /dev/null -w "%{http_code}" -X ${method} \
            -H "Content-Type: application/json" \
            -d "${data}" \
            "${SERVICE_URL}${endpoint}")
    fi

    if [ "$response" == "$expected_status" ]; then
        echo -e "${GREEN}✅ Success (HTTP ${response})${NC}"
        return 0
    else
        echo -e "${RED}❌ Failed (Expected ${expected_status}, got ${response})${NC}"
        return 1
    fi
}

# Run tests
echo -e "${YELLOW}Running endpoint tests...${NC}\n"

# Test 1: Health check
test_endpoint "/" "GET" "" "200"

# Test 2: Generic webhook
test_data='{
    "message": "Test message from deployment test",
    "sender": "test_user",
    "source": "test"
}'
test_endpoint "/webhook" "POST" "$test_data" "200"

# Test 3: WhatsApp webhook verification
VERIFY_TOKEN="meeting-os-verify-test"
test_endpoint "/webhook/kapso?hub.mode=subscribe&hub.verify_token=${VERIFY_TOKEN}&hub.challenge=123456" "GET" "" "200"

# Test 4: Fireflies webhook
fireflies_data='{
    "meeting_id": "test-meeting-123",
    "transcript_url": "https://example.com/transcript",
    "transcript": "This is a test transcript from the deployment test."
}'
test_endpoint "/webhook/fireflies" "POST" "$fireflies_data" "200"

# Test 5: Direct transcript API
transcript_data='{
    "meeting_id": "test-meeting-456",
    "transcript_text": "This is a direct transcript test."
}'
test_endpoint "/transcript" "POST" "$transcript_data" "200"

# Performance test
echo -e "\n${YELLOW}Running performance test...${NC}"
echo -e "${BLUE}Testing response time (10 requests)...${NC}"

total_time=0
for i in {1..10}; do
    start=$(date +%s%N)
    curl -s "${SERVICE_URL}/" > /dev/null
    end=$(date +%s%N)
    elapsed=$((($end - $start) / 1000000))  # Convert to milliseconds
    total_time=$(($total_time + $elapsed))
    echo -n "."
done
echo ""

avg_time=$(($total_time / 10))
echo -e "${GREEN}Average response time: ${avg_time}ms${NC}"

# Check logs
echo -e "\n${YELLOW}Recent logs from Cloud Run:${NC}"
gcloud run services logs read ${SERVICE_NAME} \
    --region ${REGION} \
    --project ${PROJECT_ID} \
    --limit 10 \
    --format "table(timestamp,severity,textPayload)"

echo -e "\n${PURPLE}=====================================${NC}"
echo -e "${PURPLE}  Test Suite Complete${NC}"
echo -e "${PURPLE}=====================================${NC}"

echo -e "\n${YELLOW}Webhook URLs for external services:${NC}"
echo -e "🔥 Fireflies:    ${SERVICE_URL}/webhook/fireflies"
echo -e "💬 WhatsApp:     ${SERVICE_URL}/webhook/kapso"
echo -e "📝 Transcript:   ${SERVICE_URL}/transcript"
echo -e "🔧 Generic:      ${SERVICE_URL}/webhook"

echo -e "\n${GREEN}Deployment is working! 🎉${NC}"