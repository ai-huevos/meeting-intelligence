# FounderOS Architecture v2.0 - The Agentic Event Bus

## Tech Stack

```
┌──────────────────────────────────────────────────────────────┐
│                  INPUT LAYER (The "Ear")              │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐    │
│  │ Fireflies  │ │  G Suite   │ │  WhatsApp  │    │
│  │  Transcript │ │    Email    │ │  Text/Call │    │
│  └───────────┘ └───────────┘ └───────────┘    │
│  ┌───────────┐ ┌───────────┐                │
│  │   Slack    │ │  Phone     │                │
│  │ (migrando) │ │  Calls     │                │
│  └───────────┘ └───────────┘                │
└───────────────────────────────────────────────────────────────┘
                      │
                      ▼
              ┌─────────────────────┐
              │   ROUTER AGENT    │ ← The Hub (Chief of Staff)
              │  (The Black Box)    │    Ingests → Cleans → Routes
              └─────────────────────┘
                      │
          ┌───────────┴───────────┐
          │   Universal Context Object│ ← JSON Schema
          └───────────┬───────────┘
                      │
    ┌─────────────────┴─────────────────┐
    │                                  │
    ▼                                  ▼
┌───────────────┐                ┌───────────────┐
│  SALES AGENT │                │ PRODUCT AGENT │
│  (The Closer) │                │  The Architect│
└───────────────┘                └───────────────┘
    │                                  │
    │                                  │
    ▼                                  ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  OPS AGENT    │   │ INSIGHTS AGENT│   │  [More]      │
│  The Operator │   │ The Strategist │   │  Future...    │
└───────────────┘   └───────────────┘   └───────────────┘
    │                  │
    └──────────┬───────┘
               │
               ▼
    ┌─────────────────────┐
    │  SLACK DASHBOARD   │ ← #founder-approval
    │  One-Click Approval │    Mission Reports
    └─────────────────────┘
```

---

## Data Layer

### Universal Context Object (JSON Schema)

**Glue entre Router y Swarm:**

```json
{
  "event_id": "mtg_YYYY_MM_DD_{context}",
  "meta": {
    "timestamp": "ISO-8601",
    "source": "Fireflies|WhatsApp|Email|Slack|Phone",
    "participants": ["Founder_X", "Client_Y"]
  },
  "routing_flags": {
    "requires_sales_action": true|false,
    "requires_product_action": true|false,
    "requires_ops_action": true|false,
    "requires_insights_action": true|false
  },
  "context_layer": {
    "summary": "Natural language summary",
    "tone": "Urgent|Frustrated|Excited|Neutral",
    "commercial_facts": {
      "budget_signal": "$X",
      "timeline_signal": "Q1|Q2|Q3|Q4",
      "decision_maker": "CTO|CEO|VP"
    },
    "technical_facts": {
      "current_stack": "AWS|Python|Excel",
      "requested_features": ["Feature A", "Feature B"],
      "constraints": "On-premise|Security|GDPR"
    },
    "ops_facts": {
      "blockers": ["Blocker 1", "Blocker 2"],
      "resources_needed": ["Resource 1"]
    }
  }
}
```

---

## AI Layer

### Router Agent (The Hub)

**Qué hace:**
1. **Ingest** - Recibe input desde cualquier canal
2. **Transcribe** - Si es audio/video → texto (Fireflies + Whisper)
3. **Extract** - Entities, facts, routing flags
4. **Route** - Envía Context Object a agentes relevantes
5. **Converge** - Agrega outputs de agentes en Slack report

**Tech:**
- TypeScript + Claude Code
- MCP servers (Fireflies, Calendar, Drive)
- GitHub para almacenar Context Objects

---

### Swarm Agents (The Spokes)

Cada agente es dueño de un AOR específico:

| Agente | Owner (AOR) | Trigger | SOP | Output |
|---------|----------------|---------|-----|---------|
| **Sales Agent** | Founder Rev | `commercial_intent = TRUE` | Listen → Diagnose → Price | WhatsApp proposal |
| **Product Agent** | Founder Ops | `feature_request = TRUE` | Requirements → Feasibility → Tickets | Linear tickets + PRD |
| **Ops Agent** | Founder C | `ops_issue = TRUE` | Triage → Assign → Execute | Tasks + OKR updates |
| **Insights Agent** | Shared | `always_active = TRUE` | Pattern Recognition | Persona updates + Pivot signals |

---

### Convergence Layer (Slack Dashboard)

**Formato de Mission Report:**

```
🤖 Mission Report: {Event Title}

1. Sales Action (@Founder_Rev)
   [Action taken]
   [Button: Review & Send]

2. Product Action (@Founder_Ops)
   [Action taken]
   [Button: View Tickets]

3. Ops Action (@Founder_C)
   [Action taken]
   [Button: Assign]

4. Insight Alert
   [Pattern detected]
   [Question to validate]
```

**Botones en Slack:**
- "Review & Send" → Abre draft en Slack, click para enviar
- "View Tickets" → Abre Linear con tickets creados
- "Assign" → Abre Asana/Linear con task asignada

---

## Integration Layer (Input Channels)

| Canal | API/Tool | Estado | Qué ingestamos |
|-------|-----------|--------|----------------|
| Fireflies | MCP | ✅ | Meeting transcripts |
| Google Calendar | MCP | ⚠️ OAuth needed | Events, attendees |
| Gmail | Gmail API | ❌ TBD | Emails, threads |
| WhatsApp | Business API | ❌ TBD | Messages, calls, audios |
| Slack | Slack API | ❌ TBD | Messages, threads |
| Phone | Twilio/AWS | ❌ TBD | Call recordings |

**#agent-ingest channel:**
- Slack channel dedicado para todos los inputs
- Bot escucha y pasa al Router Agent

---

## Orchestration (Event Flow)

```
Input Channel → Router Agent → Universal Context Object
                                         │
                            ┌────────┼────────┐
                            ▼         ▼         ▼
                     Sales Agent   Product Agent   Ops Agent
                            │            │           │
                            └────────────┼───────────┘
                                         ▼
                                   Slack Dashboard
                                         │
                                    Human Approval
```

---

## Security Model

### AI Assistant Contract

| Tier | Qué puede | Aprobación |
|------|-----------|-----------|
| **Tier 1 (Internal)** | Generar drafts de internos | Manager |
| **Tier 2 (External Drafts)** | Generar WhatsApp/Email | Founder clicks button |
| **Tier 3 (Prohibido)** | Hiring/firing, investor terms | ❌ NUNCA |

### Data Access

- **Founders:** Read/Write en todo el repo
- **Router Agent:** Read/Write en Context Objects
- **Swarm Agents:** Read en AORs de su especialidad
- **Slack Dashboard:** Read/Write en `#founder-approval`

---

## Implementation Phases

### Phase 0.1: Router Agent MVP (Semanas 1-2)
- [ ] `#agent-ingest` Slack channel configurado
- [ ] Transcripción: Fireflies + Whisper API (WhatsApp audio)
- [ ] Entity extraction: Reglas basadas en prompts
- [ ] Routing logic: Decision tree (routing_flags)
- [ ] Output: Universal Context Object (validación JSON)

### Phase 0.2: Router → Slack (Semanas 2-3)
- [ ] `#founder-approval` channel creado
- [ ] Slack Bot API configurado
- [ ] One-click approval buttons (Slack Block Kit)
- [ ] Mission report format testeado

### Phase 1: Build the Swarm (Meses 3-6)
- [ ] Sales Agent + WhatsApp Business API
- [ ] Product Agent + Linear API
- [ ] Ops Agent + Asana/Linear
- [ ] Insights Agent + NotebookLM (RAG)

### Phase 2: Expand Input Layer (Meses 6-9)
- [ ] Gmail API integration (Gmail API + webhooks)
- [ ] WhatsApp Business API (messages + calls metadata)
- [ ] Slack API (real-time messages)
- [ ] Phone call transcription (Twilio + Whisper)

### Phase 3: Self-Regulating OS (Meses 9+)
- [ ] Router aprende de feedback humano (reinforcement)
- [ ] Agents negocian entre sí (conflict resolution)
- [ ] Auto-scaling: más agents cuando carga alta
- [ ] Predictive routing: anticipa qué agentes despertar

---

## Success Metrics Tracking

| Metric | Target | Cómo medimos |
|---------|--------|--------------|
| **Message-to-Action Latency** | <5 min | Tiempo de input → Slack notification |
| **Agent Accuracy** | >85% | Drafts necesitan <15% edición humana |
| **Human Approval Time** | <2 min/día | One-click approval, no context switch |
| **Input Coverage** | 100% | Todos los canales ingestados |

---

**Tech Debt:** Ninguno (JSON schema + APIs)

**Scalability:** 3 founders → 25 employees → 250+ sin cambios core
