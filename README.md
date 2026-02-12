# Meeting OS - Intelligent Meeting Assistant

> **AI-powered meeting intelligence system** that transforms conversations into actionable insights.

## 🎯 Overview

Meeting OS is an autonomous AI system that:
- 📝 **Ingests** meeting transcripts from Fireflies, Slack, WhatsApp
- 🧠 **Analyzes** content using Gemini & Perplexity AI
- 🎯 **Routes** to specialized agents (Sales, Ops, Research)
- 💾 **Persists** to Notion CRM and Supabase
- 📢 **Notifies** teams via Slack with rich, bio-chromatic UI

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Supabase account
- Google Gemini API key
- Notion workspace

### Installation

```bash
# Clone and navigate
git clone <your-repo>
cd tbd

# Install dependencies
pip install -r meeting_os/requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run locally
python3 main.py
```

### First Test

```bash
# Health check
curl http://localhost:8080/

# Test webhook
curl -X POST http://localhost:8080/webhook \
  -H "Content-Type: application/json" \
  -d '{"message":"Test meeting about enterprise deal","sender":"user@example.com","source":"test"}'
```

## 📚 Documentation

- **[Architecture Design](docs/architecture/DESIGN.md)** - System design & data flows
- **[Deployment Guide](docs/deployment/)** - Cloud Run, Render, Docker setup
- **[Security Overview](docs/security/SECURITY.md)** - 4-layer security model
- **[Codebase Audit](CODEBASE_STATE_AUDIT.md)** - Implementation status

## 🏗️ Project Structure

```
tbd/
├── main.py                 # FastAPI entry point
├── meeting_os/             # Core application
│   ├── agents/            # AI agents (Router, Sales, Research)
│   ├── core/              # UCO, EventLog, Security
│   ├── services/          # External integrations
│   ├── prompts/           # LLM prompt templates
│   └── workflows/         # n8n workflow definitions
├── deployment/            # Docker, Cloud Run configs
├── docs/                  # Documentation
├── tests/                 # Test suite
└── .secrets/             # Credentials (gitignored)
```

## 🔑 Key Concepts

### Universal Context Object (UCO)
The "nervous system" of Meeting OS - a standardized data structure that flows through all agents:

```python
{
  "event_id": "evt_abc123",
  "source": "Fireflies",
  "routing_flags": {"sales": true, "ops": false},
  "context_layer": {
    "summary": "Client interested in Enterprise plan",
    "sentiment": "Positive",
    "next_steps": ["Send proposal", "Schedule demo"]
  }
}
```

### Agent Architecture
- **Router Agent**: Ingests UCOs, persists to Supabase, dispatches to swarms
- **Sales Agent**: Extracts deals, updates Notion CRM
- **Research Agent**: Pre-meeting briefs using Perplexity
- **Ops Agent**: Action items, task tracking

## 🛠️ Development

### Running Tests
```bash
# Unit tests (coming soon)
pytest tests/unit/

# Integration tests
pytest tests/integration/
```

### Code Quality
- Uses Pydantic for strict type validation
- 4-layer security (Input Sanitization, Prompt Wrapping, Tool Allowlist, Vault Isolation)
- Append-only event logs for auditability

## 🎨 Design Philosophy

**Bio-Chromatic Cyberpunk**: Premium, neon-accented dark mode UI
- 🟣 Neural Pink - User interactions
- 🔵 Data Cyan - Ingestion & processing
- 🟢 Bio-Lime - Success & outcomes
- 🟡 Warning Yellow - Alerts & routing decisions

## 🚢 Deployment

### Google Cloud Run
```bash
gcloud run deploy meeting-os \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --dockerfile deployment/docker/Dockerfile
```

See [docs/deployment/GCLOUD_DEPLOY.md](docs/deployment/GCLOUD_DEPLOY.md) for details.

## 📊 Monitoring
- **Event Logs**: All actions logged to Supabase `event_logs` table
- **Slack Notifications**: Real-time updates via bio-chromatic cards
- **Notion Dashboard**: CRM updates visible in workspace

## 🤝 Contributing

1. Read [CODEBASE_STATE_AUDIT.md](CODEBASE_STATE_AUDIT.md) to understand current state
2. Follow the established patterns (UCO, Agent base classes)
3. Add tests for new features
4. Update documentation

## 📄 License

[Your License Here]

## 🙏 Acknowledgments

Built with:
- Google Gemini 1.5
- Perplexity AI
- Supabase
- FastAPI
- Notion API

---

**Status**: ✅ Production-ready core • ⚠️ Advanced features in testing

For questions, see [docs/guides/](docs/guides/) or raise an issue.
