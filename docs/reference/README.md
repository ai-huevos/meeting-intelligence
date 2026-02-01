# FounderOS - Sistema Operativo para 3 Founders

**Del caos founder-led a máquina agéntica de alta velocidad**

---

## ¿Qué es?

Sistema operativo que convierte el conocimiento tribal de 3 founders en una máquina repetible. Cada función es medible, cada dueño identificado, cada proceso automatizado.

**🌟 EVOLUCIÓN v2.0:** Arquitectura Agéntica (Router + Swarm)

---

## Arquitectura v2.0: The Event Bus

```
INPUT LAYER (6 canales)
    ↓
ROUTER AGENT (The Hub) - Ingesta, limpia, rutea
    ↓
UNIVERSAL CONTEXT OBJECT (JSON Schema)
    ↓
SWARM AGENTS (Especializados por AOR)
    ├─ Sales Agent → WhatsApp proposals
    ├─ Product Agent → Linear tickets
    ├─ Ops Agent → Tasks
    └─ Insights Agent → Pattern recognition
    ↓
SLACK DASHBOARD (#founder-approval) - One-Click Approval
```

---

## 6 Bloques del Sistema

| Bloque | Qué hace (v1) | Qué hace (v2) |
|--------|----------------|---------------|
| **Individual Habits** | GTD, Top Goal blocks | GTD, Top Goal blocks |
| **Collaboration** | Written-first meetings | Written-first meetings + One-Click Approval |
| **Infrastructure** | OKRs 3x3, AORs | OKRs 3x3, AORs + Router (Hub) |
| **Group Habits** | Monday/Friday cadence | Monday/Friday cadence + Slack Dashboard |
| **Processes** | Sales playbook, Recruiting | Swarm Agents (Sales, Product, Ops, Insights) |
| **AI Integration** | NotebookLM + Claude Code | Router Agent (The Dispatcher) + Swarm Agents |

---

## Tech Stack

- **GitHub** - Source of Truth
- **NotebookLM** - Interface conversacional (gema Gemini)
- **Claude Code** - Router Agent + Swarm Agents
- **Input Layer:**
  - ✅ Fireflies (MCP)
  - ⚠️ Google Calendar (MCP, OAuth pendiente)
  - ❌ Gmail (API pendiente)
  - ❌ WhatsApp (API pendiente)
  - ❌ Slack (API migrando)
  - ❌ Phone (API pendiente)

---

## Empezar

```bash
# Clonar
git clone git@github.com:ai-huevos/founder-os.git

# Estructura
./data/        # OKRs, KPIs, AORs (YAML/CSV)
./templates/    # Meetings, 1:1, recruiting
./docs/
  ├── architecture.md              # Event Bus model v2.0
  ├── implementation.md           # Guía paso a paso
  └── playbooks/
      ├── router_agent_prd.md     # 🆕 Router System Prompt
      ├── sales_playbook.md
      └── operations_playbook.md
./prd/
  ├── MASTER_PRD_V2.md           # 🌟 Agentic Living OS
  └── PRD_FOUNDEROS_V1.md          # Updated with link to v2
```

---

## Documentación

| Documento | Qué contiene |
|-----------|-------------|
| **[MASTER_PRD_V2.md](./prd/MASTER_PRD_V2.md)** | 🌟 The Agentic Living OS - Router + Swarm agents + Input layer (6 canales) |
| **[PRD_FOUNDEROS_V1.md](./prd/PRD_FOUNDEROS_V1.md)** | PRD v1 con link a v2 |
| **[architecture.md](./docs/architecture.md)** | Event Bus model v2.0 - Router (Hub) → Slack Dashboard |
| **[router_agent_prd.md](./docs/playbooks/router_agent_prd.md)** | 🆕 System Prompt para Router Agent (The Dispatcher) |

---

**Estado:** Phase 0.1 - Build Router Agent 🚧
**Próximo:** Implementar Router Agent en Claude Code MCP server
