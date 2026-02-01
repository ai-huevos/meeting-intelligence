# Implementation Guide

## Getting Started

### Prerequisites

1. **GitHub repository** creado
2. **NotebookLM configurado** con gema Gemini
3. **MCP servers activos** (Fireflies)
4. **Claude Code disponible** para automatización

---

## Phase 0: Foundation (24 horas)

### Step 1: Repo Setup
```bash
# Clonar
git clone git@github.com:ai-huevos/founder-os.git
cd founder-os

# Ver estructura
tree -L 2
```

### Step 2: Configure MCP Servers
```bash
# Fireflies ya está activo
mcporter list fireflies-server

# Calendar (si tienes OAuth ya)
mcporter auth google-calendar-mcp
```

### Step 3: Train NotebookLM
1. Exportar todos los docs `/docs/` como PDF
2. Subir a NotebookLM
3. Crear gema Gemini con el repo como source
4. Test query: "¿Qué es el Top Goal del CEO?"

### Step 4: First Energy Audit
Crear archivo en `data/habits/energy_audit_YYYYMMDD.md`:

```markdown
# Energy Audit - 2025-01-28

**Founder:** [Name]
**Date:** [Date]

## Zone of Genius
- [Task 1] - Deep work required
- [Task 2] - Deep work required

## Draining Tasks
- [Task 1] - Reactive, low leverage
- [Task 2] - Administrative

## Blockers
- [Blocker 1] → [Resolution needed]
```

---

## Phase 1: Assisted Operations (Semanas 1-4)

### Week 1: Base Setup
- [ ] OKRs Q1 definidos en `data/okrs/`
- [ ] AORs documentados en `data/aors/`
- [ ] Primer Command Center draft

### Week 2: NotebookLM Integration
- [ ] Todos los playbooks subidos a NotebookLM
- [ ] Queries de prueba: "¿Quién maneja X?"
- [ ] Ajustar responses para mejor accuracy

### Week 3: Meeting Templates
- [ ] 1:1s usando `templates/meetings/`
- [ ] Sync meetings con pre-work enviado
- [ ] Decision logging activo (RAPID)

### Week 4: KPIs + Counter-Metrics
- [ ] Definir 5 KPIs críticos
- [ ] Para cada KPI, definir counter-metric
- [ ] Crear CSV en `data/kpis/`

---

## Phase 2: Documentation Sprint (Mes 2)

### Regla de Oro
**"When you do it twice, write it down"**

### Week 5-6: Process Documentation
- [ ] Documentar 5 procesos críticos en `docs/playbooks/`
- [ ] Cada proceso: Context → Steps → Owner → Systems
- [ ] Subir a NotebookLM

### Week 7-8: Recruiting Setup
- [ ] Usar `templates/recruiting/who_method.md`
- [ ] Crear scorecards para roles abiertos
- [ ] Definir 90-day roadmap para cada nuevo hire

---

## Phase 3: Full-Scale Automation (Mes 3+)

### Cron Jobs Setup

```bash
# Monday 9 AM Weekly Report
mcporter cron create --schedule "0 9 * * 1" \
  --command "claude generate report weekly" \
  --name "weekly-monday-report"

# Daily 9 AM Top Goal Check
mcporter cron create --schedule "0 9 * * 1-5" \
  --command "claude check top-goal" \
  --name "daily-top-goal"

# Monthly SPOF Audit
mcporter cron create --schedule "0 9 1 * *" \
  --command "claude audit spof" \
  --name "monthly-spof-audit"
```

### Automation Layer

| Automatización | Qué hace | Frecuencia |
|--------------|------------|-------------|
| **Weekly Report** | Genera status Monday 9AM | Lunes |
| **OKR Review** | Alerta KRs en riesgo | Quincenal |
| **SPOF Audit** | Detecta funciones sin backup | Mensual |
| **Process Freshness** | Flag docs sin update >30d | Mensual |

---

## Daily Routine (3 Founders)

### 9:00 AM - Top Goal Block
- [ ] Check Monday report (si aplica)
- [ ] Revisar blockers
- [ ] 2 horas protegidas para Top Goal

### 1:00 PM - Meeting Prep
- [ ] Pre-work enviado 24h antes
- [ ] Issues listados con proposed solutions
- [ ] Decisiones pendientes identificadas

### 6:00 PM - Energy Audit
- [ ] Log día en `data/habits/`
- [ ] Identificar draining tasks vs Zone of Genius
- [ ] Delegar lo posible

---

## Git Workflow

### Branch Strategy
```
main ← production ← deployment
  ↑
development ← main ← releases
  ↑
feature/* ← development ← work
```

### Commit Convention
```bash
git add .
git commit -m "feat(scope): descripción corta

- Cambio específico

🤖 FounderOS
Co-Authored-By: Clawdbot <noreply@clawd.bot>"
```

---

## Troubleshooting

### NotebookLM no responde
- **Check:** Gema Gemini está activa
- **Check:** Docs están subidos como PDF
- **Check:** Query es específico (evitar preguntas generales)

### MCP servers offline
- **Google Calendar:** Necesita OAuth (ver setup)
- **Google Drive:** Falta API key completa

### Claude Code no genera reports
- **Check:** `data/` tiene archivos YAML/CSV válidos
- **Check:** MCP servers responden
- **Check:** Cron jobs configurados

---

## Support

**Docs:** `/docs/`
**Playbooks:** `/docs/playbooks/`
**Templates:** `/templates/`
**PRD:** `/prd/PRD_FOUNDEROS_V1.md`

**Para dudas:** "Ask NotebookLM: ¿Cómo [X]?"
