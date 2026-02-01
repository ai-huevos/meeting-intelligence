# Sprint 1: Router Agent MVP (Phase 0.1)

**Sprint Goal:** Build the core Router Agent that ingests inputs, extracts entities, and generates Universal Context Objects with routing flags.

**Duration:** 2 weeks
**Epic:** Epic 1 - Router Agent Core (Ingest, Transcribe & Context)

---

## Sprint Backlog

### Story 1.1: Configurar Input Channel #agent-ingest

**As a Founder,**
**I want a Slack channel #agent-ingest to drop recordings and voice notes,**
**So that the Router Agent can automatically ingest them.**

**Acceptance Criteria:**
- ✅ Slack API is configured and bot has access
- ✅ File uploads to #agent-ingest trigger Router Agent via webhook
- ✅ File is logged with metadata (timestamp, uploader, file type)
- ✅ File is queued for transcription
- ✅ User receives confirmation message "File received for processing"

**Priority:** P0 (Must-have)
**Estimate:** 2 days
**Dependencies:**
- Slack Bot setup
- Webhook endpoint configuration

---

### Story 1.2: Implementar Transcripción Fireflies

**As a Founder,**
**I want the Router Agent to transcribe Fireflies transcripts,**
**So that audio/video inputs become text for analysis.**

**Acceptance Criteria:**
- ✅ Fireflies MCP server is configured with API key
- ✅ Router Agent fetches transcript text from Fireflies API
- ✅ Transcript is cleaned and normalized
- ✅ Transcript is stored for entity extraction
- ✅ Metadata is extracted (participants, duration, date)

**Priority:** P0 (Must-have)
**Estimate:** 1 day
**Dependencies:**
- Fireflies MCP server (already integrated per TOOLS.md)
- API key: `a77c6f43-bbca-48e4-a56a-832324a49956`

---

### Story 1.4: Extraer Entidades y Routing Flags

**As a Router Agent,**
**I want to extract entities, facts, and routing flags from transcribed text,**
**So that I can route to the appropriate swarm agents.**

**Acceptance Criteria:**
- ✅ Entities extracted: people, companies, budget, timeline, decision makers
- ✅ Technical facts extracted: current stack, requested features, constraints
- ✅ Commercial facts extracted: budget_signal, timeline_signal, decision_maker
- ✅ Routing flags set: requires_sales_action, requires_product_action, requires_ops_action, requires_insights_action
- ✅ Summary generated
- ✅ Tone detected: Urgent/Frustrated/Excited/Neutral

**Priority:** P0 (Must-have)
**Estimate:** 3 days
**Dependencies:**
- Story 1.2 (transcription available)

---

### Story 1.5: Generar Universal Context Object

**As a Router Agent,**
**I want to generate a Universal Context Object in exact JSON format,**
**So that swarm agents can read it consistently.**

**Acceptance Criteria:**
- ✅ JSON follows exact schema from Architecture
- ✅ All required fields populated: event_id, meta, routing_flags, context_layer
- ✅ event_id format: "mtg_YYYY_MM_DD_{context}"
- ✅ meta includes: timestamp (ISO-8601), source, participants
- ✅ routing_flags are boolean values
- ✅ context_layer includes: summary, tone, commercial_facts, technical_facts, ops_facts
- ✅ JSON is valid and parsable

**Priority:** P0 (Must-have)
**Estimate:** 2 days
**Dependencies:**
- Story 1.4 (extraction available)

---

### Story 1.6: Validar JSON Schema del Context Object

**As a Router Agent,**
**I want to validate that generated Context Objects match the required JSON schema,**
**So that downstream agents can parse them correctly.**

**Acceptance Criteria:**
- ✅ JSON is checked against schema
- ✅ Required fields verified to be present
- ✅ Data types validated (strings, booleans, arrays)
- ✅ Validation result logged
- ✅ If validation fails, error is raised and Context Object is not sent
- ✅ Successful validation allows Context Object to proceed to routing

**Priority:** P0 (Must-have)
**Estimate:** 1 day
**Dependencies:**
- Story 1.5 (Context Object generation available)

---

## Sprint Definition of Done

For each story in this sprint to be considered "Done":

- [ ] Code is reviewed and approved
- [ ] Unit tests written and passing
- [ ] Integration tests passing (end-to-end flow)
- [ ] Documentation updated
- [ ] Context Objects generated match schema
- [ ] Logging is in place for debugging
- [ ] Error handling is robust (graceful degradation)

---

## Sprint Timeline

| Day | Focus |
|-----|-------|
| Day 1-2 | Story 1.1: Setup #agent-ingest Slack channel + webhooks |
| Day 3 | Story 1.2: Fireflies transcription integration |
| Day 4-6 | Story 1.4: Entity extraction & routing flags |
| Day 7-8 | Story 1.5: Universal Context Object generation |
| Day 9 | Story 1.6: JSON schema validation |
| Day 10 | End-to-end testing & bug fixes |

---

## Dependencies & Blockers

**External Dependencies:**
- Slack Bot permissions (Channel: Write, Incoming Webhooks)
- Fireflies API access (key available in TOOLS.md)

**Blockers:**
- None identified

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Context Object Generation Time** | < 2 min | From file upload to JSON output |
| **Entity Extraction Accuracy** | > 80% | Manual review of first 20 outputs |
| **JSON Schema Compliance** | 100% | Automated validation |
| **Error Rate** | < 5% | Failed processing events / total events |

---

## Next Sprint (Preview)

**Sprint 2: Router → Slack Integration (Phase 0.2)**
- Story 1.7: Enviar Context Object a GitHub
- Story 1.3: Implementar Transcripción WhatsApp Audio (Whisper API)
- Story 1.8: Integrar Google Calendar (OAuth)
- Story 6.1: Crear #founder-approval channel
- Story 6.2: Desplegar Slack Dashboard con Mission Reports

---

**Sprint Status:** 🟢 Ready to Start
**Start Date:** TBD
**End Date:** TBD (2 weeks from start)
