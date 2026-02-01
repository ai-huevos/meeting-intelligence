# PRD: FounderOS - Sistema Operativo para 3 Founders

## 1. ¿Qué es?

Sistema operativo que convierte el conocimiento tribal de 3 founders en una máquina de alta velocidad. Cada función es medible, cada dueño identificado, cada proceso automatizado.

**Tecnología:**
- GitHub como Source of Truth
- NotebookLM como "Librarian" (gema Gemini)
- Claude Code como "Automator"

**🚨 EVOLUCIÓN v2.0:** Ver [MASTER_PRD_V2.md](./MASTER_PRD_V2.md) para arquitectura agéntica (Router + Swarm)

---

## 2. Problema

Los founders operan en modo reactivo:
- **Latencia alta en decisiones** → "fires" y threads de Slack
- **Single Points of Failure (SPOF)** → conocimiento en la cabeza de 1 persona
- **"Tragedy of the commons"** → funciones sin dueño claro no se hacen
- **Fragmentación de información** → Drive, Slack, Notion, Gmail, Fireflies dispersos

---

## 3. Solución: 6 Bloques

### 1. Individual Habits
- **GTD** (Next Actions, Waiting For)
- **Top Goal blocks** - 2 horas/día protegidas
- **Energy Audits** - Zone of Genius vs draining tasks

### 2. Collaboration
- **Written-first meetings** - Issues 24h antes de sync
- **Feedback scripts** - Ask → Fact → Emotion → Request
- **Decision logging** - RAPID framework

### 3. Infrastructure
- **OKRs 3x3** - 3 Objectives, 3 KRs cada uno
- **AORs** - Areas of Responsibility con 1 DRI + 1 Backup
- **Counter-metrics** - Cada KPI con su métrica contraria (ej: ARR vs Churn)

### 4. Group Habits
- **Monday/Friday cadence** - Lunes 9AM: auto reports
- **1:1 templates** - Standard scripts
- **Weekly reviews** - Ajuste de curso

### 5. Processes
- **Sales playbook** - Seeds, Nets, Spears
- **Recruiting ("Who" method)** - Role Definition → 90-day roadmap
- **Fundraising** - Pipeline 7-stage (BACKLOG)

### 6. AI Integration
- **NotebookLM (Librarian)** - Preguntas: "¿Quién es backup de payroll?"
- **Claude Code (Automator)** - Validación de schemas, auto reports

---

## 4. Usuarios (3 Founders)

| Rol | Responsabilidad |
|------|----------------|
| **Founder/CEO** | Visión, Top Goal ejecución, alineación |
| **Founder/COO/Ops** | Arquitectura, SPOF audits, documentación de procesos |
| **Founder/Product** | Roadmap, métricas, decisiones de producto |

---

## 5. Features MVP

### Feature 1: Command Center Dashboard
- **Qué:** Vista centralizada de OKRs 3x3
- **KPI ticker** - Counter-metrics obligatorios
- **AOR Lookup** - DRI + Backup por función
- **Span of Control** - Alert si manager tiene >8 reports

### Feature 2: Meeting Mode
- **Qué:** Interface para written-first meetings
- **Pre-work submission** - 24h antes de sync
- **RAPID decision logger** - Who, What, By When
- **Time-boxing** - Automático

### Feature 3: Individual Habits Panel
- **Qué:** GTD + Energy Audit
- **Next Actions** - Tareas inmediatas
- **Waiting For** - Pendientes de otros
- **Top Goal scheduler** - Bloque diario 2 horas

### Feature 4: AI Chief of Staff (Director AI)
- **Qué:** NotebookLM como interface conversacional
- **Queries naturales:** "¿Cuál es el proceso para contratar?"
- **Búsqueda en docs:** Toda la base de conocimiento indexada
- **Success:** 90% de preguntas sin intervención del founder

### Feature 5: Recruiting Pipeline (BONUS)
- **Qué:** Implementación del método "Who"
- **Roadmap automático** - 90 días desde JD
- **Scorecards** - Standard templates

---

## 6. Estructura de Datos

```
/helios-prd/
├── data/
│   ├── okrs/           # YAML: objetivos trimestrales
│   ├── kpis/           # CSV: métricas + counter-metrics
│   ├── aors/           # YAML: áreas de responsabilidad
│   └── habits/         # YAML: GTD, energy audits
├── templates/
│   ├── meetings/         # Scripts 1:1, feedback
│   ├── recruiting/       # "Who" method templates
│   └── reports/        # Status report templates
├── docs/
│   ├── architecture.md
│   ├── implementation.md
│   └── playbooks/
└── prd/
    └── PRD_FOUNDEROS_V1.md
```

---

## 7. Métricas de Éxito

| Métrica | Target | Impacto |
|---------|--------|---------|
| **Decision Velocity** | 3-5 días | Menos reactividad |
| **Agreement Completion** | 85-90% | "Impeccable Agreements" |
| **Time in Zone of Genius** | +20 hrs/semana | Deep work vs fires |
| **SPOF Coverage** | 100% | DRI + Backup por función |
| **Meeting Efficiency** | >80% tiempo en decisiones | Menos updates |

---

## 8. Roadmap

### Phase 0: Foundation (24 horas)
- [ ] Inicializar repo + estructura
- [ ] Cargar docs existentes en NotebookLM (gema Gemini)
- [ ] Primer Energy Audit

### Phase 1: Assisted Operations (Semanas 1-4)
- [ ] NotebookLM entrenado con docs base
- [ ] Primer Command Center Dashboard
- [ ] AORs iniciales documentados

### Phase 2: Documentation Sprint (Mes 2)
- [ ] Regla: "When you do it twice, write it down"
- [ ] Templates de 1:1 y meetings
- [ ] KPIs con counter-metrics definidos

### Phase 3: Full-Scale Automation (Mes 3+)
- [ ] Reports automáticos los Lunes 9AM
- [ ] SPOF audits mensuales
- [ ] Pipeline de recruiting activo

---

## 9. AI Assistant Contract (Reglas)

### Tier 1: Internal
- AI genera templates → Manager aprueba

### Tier 2: External
- AI genera comunicaciones → CEO revisa texto

### Tier 3: Prohibido
- ❌ NO hiring/firing decisions
- ❌ NO comunicaciones externas sin revisión
- ❌ NO acceso a cap-table

---

## 10. Tech Stack

- **Source of Truth:** GitHub (YAML/CSV/Markdown)
- **Librarian:** NotebookLM (gema Gemini)
- **Automator:** Claude Code
- **Integraciones:** MCP servers (Fireflies, Calendar, Drive)

---

**Next Step:** Implementar Phase 0 - Foundation
