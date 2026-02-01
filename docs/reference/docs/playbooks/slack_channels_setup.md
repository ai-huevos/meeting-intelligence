# Slack Channel Setup - FounderOS

## Channels Created

### 1. #agent-ingest (Input Layer)

**Propósito:** Canal dedicado para recibir inputs de todas las fuentes de comunicaciones.

**Qué recibimos:**
- Audio files (desde Telegram, WhatsApp, etc.)
- Transcripts de Fireflies (vía MCP)
- Links a reuniones
- Notas de reuniones
- Contexto de cualquier tipo

**Regla de uso:**
```
1. Cuando tengas input (audio, transcript, notas):
   - Envía a #agent-ingest
   - Incluye contexto: fuente, participantes, timestamp
2. El Router Agent procesa automáticamente
3. No necesitas hacer nada manual
```

**Configuración:**
```json
{
  "channel": "#agent-ingest",
  "purpose": "Universal input layer para Router Agent",
  "auto_monitor": true,
  "response_emoji": "✅"
}
```

---

### 2. #founder-approval (Output/Convergence Layer)

**Propósito:** Canal para Mission Reports con One-Click Approval.

**Qué recibimos:**
- Outputs de Router Agent (JSON con recommendations)
- Drafts de Sales Agent (WhatsApp)
- Tickets de Product Agent (Linear)
- Alertas de Insights Agent (patrones detectados)
- Tareas de Ops Agent

**Formato de Mission Report:**

```markdown
🤖 Mission Report: {Título del Evento}

## 🟢 Sales Action (@Founder_Rev)
{Acción tomada}
[Botón: Review & Send]

## 🔵 Product Action (@Founder_Ops)
{Acción tomada}
[Botón: View Linear Ticket]

## 🟣 Ops Action (@Founder_C)
{Acción tomada}
[Botón: Assign]

## 🟠 Insight Alert
{Patrón detectado}
{Pregunta para validar}
```

**Botones Interactivos:**
- `[Review & Send]` - Abre draft de WhatsApp, click para enviar
- `[View Tickets]` - Abre Linear con tickets creados
- `[Assign]` - Abre tool de asignación de tareas
- La alerta de insight ya es texto directo (sin botón)

**Configuración:**
```json
{
  "channel": "#founder-approval",
  "purpose": "Mission Reports con One-Click Approval",
  "approval_required": false,
  "auto_post": false,
  "response_emoji": "🤖"
}
```

---

## Integración con Router Agent

### Flujo de Datos:

```
Input → #agent-ingest
    ↓
Router Agent (ingesta + rutea)
    ↓ (outputs JSON)
    ↓
#founder-approval (Mission Report)
    ↓ (Humans: One-Click Approval)
    ↓
Actions enviadas (WhatsApp, Linear, tareas)
```

### Mensaje de Bienvenida (cuando se crea el canal):

```
🎉 ¡Canales de Slack creados!

📥 #agent-ingest → Inputs universales (audio, Fireflies, notas)
📋 #founder-approval → Mission Reports con One-Click Approval

El Router Agent está listo para recibir tus inputs.
```

---

## Testing Simulation

### Escenario: Input de Prueba

**Input simulado:**
```json
{
  "source": "manual_test",
  "context": "Prueba de Router Agent MÍNIMO",
  "timestamp": "2026-01-28T17:00:00Z",
  "content": "Reunión de hoy - testing de arquitectura agéntica"
}
```

**Expected Output del Router:**
```json
{
  "event_meta": {
    "participants_external": ["Cliente Prueba", "Daniel", "Restrepo"],
    "participants_internal": ["Daniel", "Restrepo"]
  },
  "context_layer": {
    "summary": "Testing de Router Agent - validar ingestión, ruteo y Slack integration",
    "diagnosis_pain": "No tiene pain points en esta prueba",
    "agreed_next_steps": ["Validar ingestión", "Probar Slack integration"]
  },
  "swarm_instructions": {
    "sales_agent_draft": "No aplica (sin cliente)",
    "product_agent_ticket": "Crear ticket de test: 'Router Agent Test'",
    "ops_agent_task": "Crear channel #agent-ingest si no existe"
  }
}
```

---

## Comandos para Crear Canales

```bash
# Crear canales en Slack
slack channel create --name "agent-ingest" --description "Input layer para Router Agent - Audio, Fireflies, notas"
slack channel create --name "founder-approval" --description "Mission Reports con One-Click Approval"

# Añadir integraciones (Bot inviter)
slack invite --channel #agent-ingest --message "Router Agent se unirá aquí para procesar inputs"
slack invite --channel #founder-approval --message "Router Agent enviará Mission Reports aquí"
```

---

## Verificación de Canales

```bash
# Listar canales existentes
slack channel list | grep -E "(agent-ingest|founder-approval)"

# Enviar mensaje de prueba al Router Agent
slack message @router-agent "Simulación: Procesando input de prueba..."
```

---

## Next Steps

1. ✅ Crear canales de Slack (hecho en este doc)
2. ⏳ Implementar Router Agent MÍNIMO (basado en PRD)
3. ⏳ Testear con input simulado
4. ⏳ Desplegar integraciones reales (Gmail, WhatsApp, Calendar)
5. ⏳ Expandir a Swarm Agents (Sales, Product, Ops, Insights)

---

**Estado:** Channels creados, esperando implementación de Router Agent.

**Próximo:** ¿Quieres que implemente el Router Agent?
