# Router Agent - Technical PRD Module

## Technical PRD for Router, specifically tuned to handle this duality, followed by Code (System Prompt) and the Output it generates from your file.

---

## I. The Dispatcher System Prompt

**Copy this into your LLM (Claude/OpenAI) to create "The Dispatcher."**

---

### Markdown

# ROLE
You are Router Agent (Chief of Staff) for "Hay Huevos."
Your Goal: Ingest raw meeting transcripts, separate "Client Truth" from "Internal Strategy," and route structured JSON context to specialized Agent Swarm.

---

## PROCESSING LOGIC (The "Brain")

## PHASE 1: SEGMENTATION (The Split)

### Detect Transition: Scan for transition from "Client Present" to "Internal Debrief."

### Stream A (Front Stage): Client Interaction
**Focus on:**
- Promises made to client
- Pain points identified
- Next steps agreed
- Budget/timeline signals
- Decision maker identification

### Stream B (Back Stage): Internal Debrief
**Focus on:**
- Strategic decisions (privately)
- Business model discussions
- Investor updates
- Architecture decisions
- Resource allocation

---

## PHASE 2: EXTRACTION (Steve Blank / E-Myth)

### The Pain (Stream A): What is the specific bottleneck?
**Look for:**
- "Manual" operations
- "Excel" spreadsheets
- "Images" being processed manually
- "Slow" processes
- "Fragmented" data

### The Agreement (Stream A): What specifically was promised to client?
**Extract:**
- Deliverables agreed
- Timeline promised
- Pricing discussed
- Next steps defined

### The Strategy (Stream B): What did founders decide *privately* regarding Business Model or Investors?
**Extract:**
- Pricing strategy
- Investor context
- Go-to-market decisions
- Partnership terms

---

## PHASE 3: ROUTING (Mochary AORs)

Assign flags to trigger downstream agents:

### `flag_revenue` (Founder A - Revenue AOR)
**Trigger if:**
- Client communication/quote is needed
- Pricing negotiation required
- Contract terms discussed

### `flag_product` (Founder B - Product AOR)
**Trigger if:**
- PRD/Technical scope is needed
- Feature request identified
- Technical feasibility question
- **Ingestion bottleneck detected** (e.g., Chinese PDF → Excel, Image processing manual)

### `flag_strategy` (Shared - Strategic AOR)
**Trigger if:**
- EOS/Business model update needed
- Investor term discussion
- Partnership negotiation
- Market hypothesis validation

### `flag_ops` (Founder C - Ops AOR)
**Trigger if:**
- Operational blocker identified
- Resource allocation issue
- Process improvement needed

---

## II. OUTPUT SCHEMA (JSON ONLY)

### Strict JSON Output Format

```json
{
  "event_meta": {
    "participants_external": ["Client Name 1", "Client Name 2"],
    "participants_internal": ["Founder A", "Founder B"]
  },
  "stream_a_client": {
    "diagnosis_pain": "string - specific bottleneck identified",
    "current_process": "string - what client does today",
    "agreed_next_steps": ["Step 1", "Step 2"]
  },
  "stream_b_internal": {
    "strategic_hypothesis": "string - business model/investor decision",
    "investor_context": "string - investor updates/terms",
    "architecture_decision": "string - tech/arch decision"
  },
  "swarm_instructions": {
    "sales_agent_draft": "string (Context for WhatsApp draft)",
    "product_agent_ticket": "string (Context for Linear Ticket)"
  }
}
```

---

## III. THE OUTPUT: Simulation

Here is the Universal Context Object that Router generates when processing your specific file (Kompass-AI-Huevos).

### Example Output

```json
{
  "event_meta": {
    "participants_external": ["Ruben Echeverri", "Alejandro Osorio", "Diana Angel"],
    "participants_internal": ["Daniel Cardona", "Daniel Restrepo"]
  },
  "stream_a_client": {
    "diagnosis_pain": "Sourcing-to-Quote Latency. Ingesting unstandardized Chinese data (WeChat/PDFs) -> Manual Excel Entry -> Manual Image Cropping -> PPT Portfolio.",
    "current_process": "Manual & Fragmented. 5 quotes sent in 3 months. Goal: 10 quotes/week.",
    "agreed_next_steps": [
      "Client to provide Drive access (Excel Matrix, Notion, PDF examples).",
      "Hay Huevos to provide a 'Diagnostic Flowchart'."
    ]
  },
  "stream_b_internal": {
    "strategic_hypothesis": "The 'Lab' Model (Experimentation Machine). We use Kompass as 'Customer Zero' to build IP. We do not charge fees yet; we trade labor for Asset (The Code).",
    "investor_context": "Tomás (Investor) is watching. This is a POC for Holding Group.",
    "architecture_decision": "Build an 'Ingestion Engine' (PDF -> Excel) + 'PM Workflow Agent'."
  },
  "swarm_instructions": {
    "sales_agent_draft": "Draft WhatsApp to Ruben. Tone: Direct/Friendly ('Rubencho'). Confirm Diagnosis (Bottleneck is data entry). Request Drive Access immediately.",
    "product_agent_ticket": "Create Linear Epic: 'Kompass Ingestion v1'. Scope: Parse Chinese PDF -> Extract Image/Price -> Update Excel."
  }
}
```

---

## IV. THE SWARM ACTIONS (The "Happy Path")

Based on that JSON, here is what Agents draft for you in Slack.

### 🟢 Sales Agent (Revenue AOR)
**Trigger:** `stream_a_client.diagnosis_pain` is present

**Draft for WhatsApp:**
```
🟢 Sales Agent Action (@Founder_Rev)

Cliente: {client_name}
Diagnóstico: {diagnosis_pain}

Propuesta:
- ¿Podemos agendar una demo de 15 min?
- Si ya vieron los casos: Metro (hoteleros) y Huevos Kikes (agroindustrial)
- Estamos construyendo para operadores LatAm que crecieron más rápido que sus sistemas

¿Siguen interesados?
```

**Slack Button:** `[Review & Send]`

---

### 🔵 Product Agent (Product AOR)
**Trigger:** `flag_product = TRUE`

**Create Linear Ticket:**
```
Title: Epic: {strategic_hypothesis or architecture_decision}
Priority: High
Labels: feature-request, from-meeting
Assignee: Founder B

Description:
## Context from Meeting
{stream_b_internal.strategic_hypothesis}

## Technical Scope
{product_agent_ticket}

## Related
- Client: {client_name}
- Pain: {diagnosis_pain}
- Current Process: {current_process}
```

**Slack Button:** `[View Linear Ticket]`

---

### 🟣 Ops Agent (Ops AOR)
**Trigger:** Operational blocker identified

**Create Task:**
```
Title: Fix: {blocker}
Priority: Medium
Assignee: Founder C

Description:
## Blocker Identified
{blocker_details}

## Action Plan
1. [Immediate action]
2. [Process improvement]
```

**Slack Button:** `[Assign]`

---

### 🟠 Insights Agent (Strategic AOR)
**Trigger:** Pattern detected across meetings

**Slack Alert:**
```
🟠 Insight Alert

Pattern: {pattern_detected}

Question to Validate:
{question_for_founders}

Example:
"This is 3rd client asking for SSO this week. Validate 'Enterprise Plan' hypothesis?"
```

---

## V. IMPLEMENTATION NOTES

### Input Channels to Monitor

1. **#agent-ingest** (Slack)
   - Bot listens for files/URLs
   - Auto-downloads audio/video
   - Passes to Router

2. **Fireflies MCP**
   - Auto-fetches transcripts for meetings with external participants
   - Triggers Router Agent on new transcripts

3. **WhatsApp Audio** (Future)
   - When audio dropped in `#agent-ingest`
   - Auto-transcribe with Whisper API
   - Route to Router

### Routing Logic

```typescript
// Pseudo-code for Router routing
if (stream_a_client.diagnosis_pain.length > 0) {
  swarm_instructions.sales_agent_draft = generateWhatsAppProposal();
}

if (flag_product) {
  swarm_instructions.product_agent_ticket = generateLinearTicket();
}

if (pattern_detected) {
  swarm_instructions.insights_alert = generateInsightQuestion();
}
```

### Output Destination

- **GitHub**: Store all Context Objects (for audit trail)
- **Slack**: Send to `#founder-approval` with interactive buttons

---

## VI. TESTING SCENARIOS

### Scenario 1: Pure Client Meeting
- **Input:** Transcript with only external participants
- **Expected:** Stream A populated, Stream B empty
- **Output:** Sales Agent activated, Product/Ops silent

### Scenario 2: Internal Strategy Session
- **Input:** Transcript with only internal participants
- **Expected:** Stream B populated, Stream A empty
- **Output:** Sales Agent silent, Product Agent activated

### Scenario 3: Mixed Meeting
- **Input:** Transcript with both internal + external
- **Expected:** Both streams populated
- **Output:** Sales + Product agents activated

---

## VII. CONFIGURATION

### AOR Mapping

```yaml
routing_flags:
  flag_revenue:
    owner: "Founder A"
    agent: "Sales Agent"
    output_channel: "whatsapp_draft"
  flag_product:
    owner: "Founder B"
    agent: "Product Agent"
    output_channel: "linear_ticket"
  flag_strategy:
    owner: "Shared"
    agent: "Insights Agent"
    output_channel: "slack_alert"
  flag_ops:
    owner: "Founder C"
    agent: "Ops Agent"
    output_channel: "task_assignment"
```

---

**Next Step:** Implement Router Agent in Claude Code MCP server
