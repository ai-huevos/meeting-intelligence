# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FounderOS v2.0 - An agentic operating system that transforms founder knowledge into automated business processes. The system uses a Router Agent (The Hub) that ingests events from multiple channels and dispatches them to specialized Swarm Agents (Sales, Product, Ops, Insights).

## Architecture

The system follows an Event Bus architecture with three layers:

1. **Input Layer**: 6 channels (Fireflies, Google Calendar, Gmail, WhatsApp, Slack, Phone)
2. **Router Agent**: Central hub that ingests, cleans, and routes events via Universal Context Objects
3. **Swarm Agents**: Specialized agents that execute based on their Area of Responsibility (AOR)

Key data flow:
```
Input Channel → Router Agent → Universal Context Object → Swarm Agents → Slack Dashboard
```

## Development Commands

### BMAD Workflow Commands

This project uses BMAD (Business Methodology and Design) workflows. Key commands:

- `/bmad-bmm-create-prd` - Create a Product Requirements Document
- `/bmad-bmm-create-architecture` - Design system architecture
- `/bmad-bmm-create-story` - Create user stories from epics
- `/bmad-bmm-dev-story` - Execute a story implementation
- `/bmad-bmm-quick-dev` - Flexible development with optional planning
- `/bmad-bmm-code-review` - Adversarial code review (finds 3-10 issues minimum)
- `/bmad-bmm-sprint-status` - Summarize sprint status and surface risks
- `/bmad-help` - Get workflow guidance

### Testing Commands

- `/bmad-bmm-testarch-atdd` - Generate acceptance tests before implementation
- `/bmad-bmm-testarch-test-review` - Review test quality
- `/bmad-bmm-testarch-trace` - Requirements-to-tests traceability

### Documentation Commands

- `/bmad-bmm-document-project` - Document brownfield projects
- `/bmad-index-docs` - Generate index.md for directories

## Universal Context Object Schema

All agents communicate via this standardized JSON format:

```json
{
  "event_id": "mtg_YYYY_MM_DD_{context}",
  "meta": {
    "timestamp": "ISO-8601",
    "source": "Fireflies|WhatsApp|Email|Slack|Phone",
    "participants": ["Founder_X", "Client_Y"]
  },
  "routing_flags": {
    "requires_sales_action": boolean,
    "requires_product_action": boolean,
    "requires_ops_action": boolean,
    "requires_insights_action": boolean
  },
  "context_layer": {
    "summary": "string",
    "tone": "Urgent|Frustrated|Excited|Neutral",
    "commercial_facts": {},
    "technical_facts": {},
    "ops_facts": {}
  }
}
```

## Agent Responsibilities

| Agent | Owner (AOR) | Trigger | Output |
|-------|-------------|---------|---------|
| Sales Agent | Founder Rev | commercial_intent = TRUE | WhatsApp proposal |
| Product Agent | Founder Ops | feature_request = TRUE | Linear tickets + PRD |
| Ops Agent | Founder C | ops_issue = TRUE | Tasks + OKR updates |
| Insights Agent | Shared | always_active = TRUE | Persona updates + Pivot signals |

## Directory Structure

- `/prd/` - Product Requirements Documents (MASTER_PRD_V2.md is the main spec)
- `/docs/` - Architecture and implementation documentation
  - `/docs/playbooks/` - Agent SOPs and operational playbooks
- `/data/` - OKRs, KPIs, AORs (YAML/CSV format)
- `/templates/` - Meeting and process templates
- `/_bmad/` - BMAD configuration files
- `/_bmad-output/` - Generated BMAD artifacts
- `/.claude/commands/` - BMAD workflow command definitions

## Current Development Phase

**Phase 0.1: Router Agent MVP**
- Building the Router Agent in Claude Code MCP server
- Implementing Fireflies MCP integration
- Creating Universal Context Object validation

## Integration Status

- ✅ Fireflies (MCP integrated)
- ⚠️ Google Calendar (MCP available, OAuth pending)
- ❌ Gmail (API integration pending)
- ❌ WhatsApp (Business API pending)
- ❌ Slack (API migration in progress)
- ❌ Phone (Twilio/AWS pending)

## Key Technical Decisions

1. **Language**: All content and code comments should be in Spanish (founders' native language)
2. **Data Format**: Universal Context Objects use JSON Schema for validation
3. **Storage**: GitHub as source of truth for all Context Objects
4. **Approval**: Human-in-the-loop via Slack #founder-approval channel
5. **Security**: Tiered approval model (Internal → External Drafts → Prohibited actions)

## Development Workflow

1. Use BMAD commands for structured development
2. Router Agent validates all Context Objects against JSON Schema
3. Swarm Agents operate independently based on routing_flags
4. All external communications require founder approval via Slack buttons
5. Mission Reports aggregate all agent outputs for one-click review

## Success Metrics

- Message-to-Action Latency: <5 min
- Agent Accuracy: >85% (drafts need <15% human editing)
- Human Approval Time: <2 min/day
- Input Coverage: 100% of channels ingested