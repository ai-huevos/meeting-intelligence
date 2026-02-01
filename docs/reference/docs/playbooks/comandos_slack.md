# Comandos de Slack para Crear Canales

## Opción 1: Usando API de tu cuenta de Slack

Daniel ya creó los canales. Solo necesitas ejecutar estos comandos:

```bash
# Crear canal de input (#agent-ingest)
slack channel create --name agent-ingest --description "Input layer universal para Router Agent"

# Crear canal de mission reports (#founder-approval)
slack channel create --name founder-approval --description "Mission Reports con One-Click Approval para FounderOS"

# Invitar a los canales
slack invite --channel agent-ingest
slack invite --channel founder-approval
```

---

## Opción 2: Crear desde tu cuenta directamente

Si prefieres que Daniel cree los canales desde su cuenta de Slack, solo dile que lo haga. Yo no tengo acceso a tu cuenta.

---

## Opción 3: Google Doc compartido (NO RECOMENDADO)

Crear un Google Doc compartido es una opción pero NO recomendada porque:
- Edición en tiempo real (más lento)
- Version control difícil
- Permisos más complejos

**Recomendación:** Colaboración en este repo (helios-prd) es más eficiente.

---

## Qué hace cada canal

### #agent-ingest (Input Layer)
- Recibe todos los inputs de comunicaciones
- Incluye contexto (fuente, participantes, timestamp)
- Router Agent procesa automáticamente

### #founder-approval (Output Layer)
- Recibe outputs del Router Agent
- Mision Reports con botones de One-Click Approval
- Drafts de WhatsApp, Tickets de Linear, Alertas

---

## Workflow completo

```
Input (audio/notes/Fireflies) → #agent-ingest
                                   ↓
                            Router Agent
                                   ↓
                    JSON (insights + tasks) → #founder-approval
                                                      ↓
                                        Human: One-Click Approval
```

---

## Para Daniel

Si necesitas ajustar los canales:
1. Editar este archivo (`slack_channels_setup.md`)
2. Agregar comandos adicionales
3. Documentar el botón de approval
4. Actualizar el README con los nuevos canales

---

**Estado:** Documentación lista. Awaiting ejecución de comandos por Daniel.
