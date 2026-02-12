# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Meeting OS - An AI-powered meeting intelligence system that ingests meeting transcripts from multiple channels (Fireflies, Slack, WhatsApp), analyzes content using Gemini & Perplexity AI, routes to specialized agents, and persists insights to Notion CRM and Supabase.

## Architecture

### Event-Driven Design with Universal Context Objects (UCO)
The system uses UCOs as the standard protocol for all events, decoupling input channels from processing logic:
- **Event Sources**: Fireflies, Slack, WhatsApp, Google Calendar, Manual
- **Router Agent**: Central hub that validates, enriches, and routes UCOs
- **Swarm Agents**: Specialized processors (Sales, Research, Ops, Librarian)
- **Persistence**: Supabase for event logs, Notion for CRM

### Core Data Flow
```
Input Channel → FastAPI Endpoint → Router Agent → UCO → Swarm Agents → External Services
```

## Development Commands

### Running the Application
```bash
# Install dependencies
pip install -r meeting_os/requirements.txt

# Set up environment
cp .env.example .env  # Configure API keys

# Run local server
python3 main.py  # Runs on port 8080

# Run with uvicorn (alternative)
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

### Testing
```bash
# Run unit tests (when available)
pytest tests/

# Test specific agent
pytest tests/test_sales_agent.py

# Manual testing scripts
python scripts/test_kapso.py           # Test WhatsApp handler
python scripts/run_e2e_real.py         # End-to-end test
python scripts/manual_test_librarian.py # Test Librarian agent
```

### Database Setup
```bash
# Apply Supabase schema
python scripts/apply_schema.py

# Setup initial database
python scripts/setup_supabase.py
```

### Daily Operations
```bash
# Run daily prep for meetings
python scripts/run_daily_prep.py

# Generate COS workflow
python scripts/generate_cos.py

# Generate Ops workflow
python scripts/generate_ops.py
```

## Key Components

### Universal Context Object (UCO)
Location: `meeting_os/core/uco.py`

All agents communicate via standardized UCO format:
- `event_id`: Unique identifier
- `source`: EventSource enum (Fireflies, Slack, WhatsApp, etc.)
- `routing_flags`: Determines which agents to activate
- `context_layer`: Synthesized understanding (summary, sentiment, topics, entities)
- `status`: Processing status tracking

### Agent System
Base class: `meeting_os/core/base_agent.py`

Agents follow a standard pattern:
1. Inherit from `BaseAgent`
2. Implement `process()` method
3. Return structured results
4. Support idempotency via event_id tracking

Current agents:
- **RouterAgent** (`meeting_os/agents/router_agent.py`): Routes events to appropriate swarm agents
- **SalesAgent** (`meeting_os/agents/sales_agent.py`): Extracts deal info, updates CRM
- **ResearchAgent** (`meeting_os/agents/research_agent.py`): Enriches with external data
- **LibrarianAgent** (`meeting_os/agents/librarian_agent.py`): Manages knowledge base

### External Services
All in `meeting_os/services/`:
- `fireflies.py`: Meeting transcript ingestion
- `notion.py`: CRM integration
- `slack.py`: Team notifications with bio-chromatic UI
- `llm.py`: Gemini integration
- `perplexity.py`: Web search and research
- `database.py`: Supabase operations
- `google_calendar.py`: Calendar integration

## Environment Variables

Required in `.env`:
```bash
# Supabase
SUPABASE_URL=
SUPABASE_KEY=

# LLMs
GEMINI_API_KEY=
PERPLEXITY_API_KEY=

# Integrations
NOTION_API_KEY=
NOTION_DATABASE_ID=
SLACK_WEBHOOK_URL=
FIREFLIES_API_KEY=

# Optional
KAPSO_WEBHOOK_SECRET=
```

## API Endpoints

Main FastAPI app in `main.py`:
- `GET /` - Health check
- `POST /webhook` - Unified webhook handler (WhatsApp, Slack, etc.)
- `POST /transcript` - Fireflies transcript ingestion

## Security Model

4-layer security architecture (`meeting_os/core/security/`):
1. Input Sanitization - Validate and clean all inputs
2. Prompt Wrapping - Secure LLM prompts
3. Tool Allowlist - Restrict agent capabilities
4. Vault Isolation - Secure credential management

## Deployment

### Google Cloud Run
```bash
gcloud run deploy meeting-os \
  --source . \
  --region us-central1 \
  --dockerfile deployment/docker/Dockerfile
```

See `docs/deployment/GCLOUD_DEPLOY.md` for full details.

## Design Philosophy

**Bio-Chromatic Cyberpunk Theme**:
- 🟣 Neural Pink - User interactions
- 🔵 Data Cyan - Ingestion & processing
- 🟢 Bio-Lime - Success & outcomes
- 🟡 Warning Yellow - Alerts & routing

## Testing Strategy

### Unit Tests
Test individual agents and services in isolation

### Integration Tests
Test end-to-end flows with mock external services

### Manual Testing
Use scripts in `scripts/` for testing specific integrations

## Code Patterns

### Adding a New Agent
1. Create class inheriting from `BaseAgent`
2. Implement `process(uco: UniversalContextObject)` method
3. Register in `router_agent.py` routing logic
4. Add tests in `tests/`

### Adding a New Input Channel
1. Create endpoint in `main.py`
2. Transform input to UCO format
3. Pass to RouterAgent
4. Handle response appropriately

## Important Notes

- Always use UCO for inter-agent communication
- Maintain idempotency using event_id
- Log all operations to event_logs table
- Require human approval for external communications
- Use bio-chromatic colors in Slack notifications