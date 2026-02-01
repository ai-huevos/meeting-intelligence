# MASTER PRD: The Agentic Living OS (Kernel v1.0)

## Objective

Build a self-regulating Operating System where a central "Router" ingests raw events and broadcasts structured "Context Objects" to specialized "Sub-Agents" (The Swarm).

---

## Core Philosophy

**The Hub (Router):** The "Chief of Staff." It listens, cleans, and routes. It does no execution.

**The Spokes (Swarm):** Specialized Agents (Sales, Product, Ops, Insights) that execute specific AORs based on Router's signal.

**The Protocol:** All agents communicate via standardized JSON schema to ensure "Impeccable Agreements."

---

## I. System Architecture: The "Event Bus"

We are replicating a high-functioning Executive Team meeting where everyone listens to the same update, but processes it through their unique functional lens.

### 1. The Input Layer (The "Ear")

**Trigger:** A meeting recording, voice note, or text dump is dropped into `#agent-ingest`.

**Channels:**
- ✅ **Fireflies** (transcripts) - Ya integrado
- ✅ **Google Calendar** (events) - MCP disponible
- ✅ **G Suite Email** (emails) - Pendiente integración
- ✅ **WhatsApp** (texts, calls, audios) - Pendiente integración
- ✅ **Slack** (migrando) - Pendiente integración
- ✅ **Phone calls** (recordings) - Pendiente integración

**The Gatekeeper:** The Router Agent

**Role:** Transcription, Entity Extraction, and creation of "Universal Context Object."

**Authority:** It decides which sub-agents need to wake up.

---

### 2. The Processing Layer (The "Swarm")

Once Router broadcasts Context Object, these agents run in parallel:

#### Agent A: The Closer (Revenue AOR)
- **Owner:** Founder A (Sales/Revenue)
- **Trigger:** `commercial_intent = TRUE`
- **SOP:** "Listen → Diagnose → Price."
- **Output:** Drafts WhatsApp proposal

#### Agent B: The Architect (Product AOR)
- **Owner:** Founder B (Product/Tech)
- **Trigger:** `feature_request = TRUE`
- **SOP:** "Requirements → Feasibility → Tickets."
- **Output:** Drafts Linear/Jira tickets and PRD scope

#### Agent C: The Strategist (Insights AOR)
- **Owner:** Shared (Co-CEO/Strategic)
- **Trigger:** Always Active
- **SOP:** "Pattern Recognition."
- **Output:** Updates Customer Persona and flags "Pivot Signals" (Steve Blank Validation)

#### Agent D: The Operator (Ops AOR)
- **Owner:** Founder C (Ops/People)
- **Trigger:** `ops_issue = TRUE`
- **SOP:** "Triage → Assign → Execute."
- **Output:** Creates tasks and updates OKRs

---

### 3. The Convergence Layer (The "Executive Dashboard")

**The Aggregator:** Collects outputs from Sales, Product, Ops, and Insights agents.

**The Human Interface:** Presents a Single Mission Report to Founders in Slack for "One-Click Approval."

---

## II. The Data Protocol: The "Universal Context Object"

This is the glue. The Router must output this exact JSON format so sub-agents can read it.

```json
{
  "event_id": "mtg_2026_01_28_client_alpha",
  "meta": {
    "timestamp": "2026-01-28T10:00:00Z",
    "source": "Zoom_Transcript",
    "participants": ["Founder_Rev", "Client_CTO"]
  },
  "routing_flags": {
    "requires_sales_action": true,
    "requires_product_action": true,
    "requires_legal_action": false,
    "requires_ops_action": false
  },
  "context_layer": {
    "summary": "Client wants to automate data entry but has strict security constraints.",
    "tone": "Urgent/Frustrated",
    "commercial_facts": {
      "budget_signal": "$20k - $30k",
      "timeline_signal": "Q1 Launch",
      "decision_maker": "CTO (Technical Buyer)"
    },
    "technical_facts": {
      "current_stack": "AWS, Python, Excel",
      "requested_features": ["PDF Parsing", "SSO Integration"],
      "constraints": "On-premise deployment only"
    }
  }
}
```

---

## III. The User Experience (The "Happy Path")

This is how the system feels to you (The Founder).

### Step 1: The Dump
You finish a call. You upload audio file to `#agent-ingest`.

### Step 2: The Black Box
The Router analyzes the file. It pings Sales Agent and Product Agent. They run their prompts in background.

### Step 3: The Notification
You receive ONE message in your `#founder-approval` channel:

```
🤖 Mission Report: Client Alpha

1. Sales Action (@Founder_Rev):
   I have drafted WhatsApp proposal based on $25k pricing matrix.
   [Button: Review & Send]

2. Product Action (@Founder_Ops):
   I have identified 2 new features.
   Feature A: PDF Parser (Standard)
   Feature B: SSO (High Complexity)
   [Button: View Linear Tickets]

3. Insight Alert:
   This is 3rd client asking for SSO this week. Validate "Enterprise Plan" hypothesis?
```

---

## IV. Immediate Next Step: Build the Router

We cannot build the Swarm until we build the Hub.

**Phase 0.1: Router Agent MVP**
- [ ] Input layer: #agent-ingest channel configured
- [ ] Transcription: Fireflies + WhatsApp audio
- [ ] Entity extraction: Built-in
- [ ] Routing logic: Decision tree
- [ ] Output: Universal Context Object (JSON)

**Phase 0.2: Router → Slack Integration**
- [ ] #founder-approval channel created
- [ ] One-click approval buttons configured
- [ ] Mission report format tested

---

## V. Roadmap

### Phase 1: Build the Swarm (Months 1-3)
- [ ] **Sales Agent** (Revenue AOR) - WhatsApp proposal drafts
- [ ] **Product Agent** (Product AOR) - Linear tickets generator
- [ ] **Ops Agent** (Ops AOR) - Task assignment
- [ ] **Insights Agent** (Strategic) - Pattern recognition

### Phase 2: Expand Input Layer (Months 3-6)
- [ ] Gmail API integration (emails)
- [ ] WhatsApp Business API (texts + calls)
- [ ] Slack API (messages)
- [ ] Phone call transcription (Twilio/AWS)

### Phase 3: Self-Regulating OS (Months 6+)
- [ ] Router learns from human feedback
- [ ] Agents negotiate with each other
- [ ] Auto-scaling agents based on workload
- [ ] Predictive routing (anticipates which agents to wake up)

---

## VI. Success Metrics

| Metric | Target | "So What?" |
|---------|--------|------------|
| **Message-to-Action Latency** | <5 min | Founder doesn't wait |
| **Agent Accuracy** | >85% | First drafts need minimal edits |
| **Human Approval Time** | <2 min/day | One-click, no context switch |
| **Input Coverage** | 100% | All comms channels ingested |

---

## VII. The AI Assistant Contract

### Tier 1: Internal Drafts
- AI generates internal proposals, tickets, insights
- **Approval:** Manager reviews before action

### Tier 2: External Communications
- AI drafts WhatsApp messages, emails
- **Approval:** Founder clicks button to send

### Tier 3: Prohibited
- ❌ NO hiring/firing decisions
- ❌ NO investor term sheets
- ❌ NO contract signing without review

---

## VIII. Tech Stack

### Input Layer
| Channel | API/Tool | Status |
|---------|------------|--------|
| Fireflies | MCP | ✅ Active |
| Google Calendar | MCP | ⚠️ Needs OAuth |
| Gmail | Gmail API | ❌ TBD |
| WhatsApp | Business API | ❌ TBD |
| Slack | Slack API | ❌ TBD |
| Phone | Twilio/AWS | ❌ TBD |

### Router Agent
- **Language:** TypeScript (Claude Code)
- **Storage:** GitHub (Context Objects)
- **Orchestration:** Claude Code MCP servers

### Swarm Agents
- **Sales Agent:** Claude Code + WhatsApp Business API
- **Product Agent:** Claude Code + Linear API
- **Ops Agent:** Claude Code + Asana/Linear
- **Insights Agent:** Claude Code + NotebookLM (RAG)

### Dashboard
- **Platform:** Slack
- **Channel:** `#founder-approval`
- **Format:** Buttons (Review & Send, View Tickets)

---

**Next:** Build Router Agent MVP (Phase 0.1)
