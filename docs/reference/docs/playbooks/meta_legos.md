# Meta Legos - Bloques Reutilizables para Diferentes Contextos

## Concepto

Los "Meta Legos" son los bloques/módulos construidos con `meta-skill-maker` que se pueden combinar de diferentes formas para construir skills deterministas para diferentes contextos (Helios, Helios, MetaGente, etc.).

---

## Legos Disponibles

### 1. meta-skill-maker

**Qué es:** Framework para crear meta skills deterministas

**Ubicación:** `/home/danny/.npm-global/lib/node_modules/clawdbot/skills/meta-skill-maker/SKILL.md`

**Patrones implementados:**
- Sequential (uno tras otro)
- Parallel Branching (multiple caminos condicionales)
- Conditional Branching (if/else lógico)

**Usado para crear:**
- meeting-orchestrator
- meeting-analyzer
- extractor-dispatcher

---

### 2. meeting-orchestrator

**Qué es:** Meta skill que orquesta reuniones usando Fireflies MCP

**Ubicación:** `/home/danny/clawd/mcp-servers/meeting-orchestrator/skill/SKILL.md`

**Lógica determinista:**
- Detecta tipo de reunión (business_sales, product_project, strategic_founders, operations, general)
- Rutea a extractor específico según tipo
- Llama extractor como session spawn (contexto aislado)

**Input:**
- Transcripts de Fireflies (vía MCP)
- Eventos de Google Calendar

**Output schema:**
- meeting_type (clasificación)
- metadata (summary, attendees, duration)
- next_skill (extractor recomendado)
- insights + tasks (delegados al extractor correcto)

---

### 3. meeting-analyzer

**Qué es:** Skill que analiza reunión + clasifica tipo

**Ubicación:** `/home/danny/.npm-global/lib/node_modules/clawdbot/skills/meeting-analyzer/SKILL.md`

**Lógica determinista:**
- Classification tree para meeting types
- Keywords matching (CEO, sales, product, ops)
- Fallback a "general" si no match

**Usado en:**
- meeting-orchestrator (como primer filtro)

---

### 4. extractor-dispatcher

**Qué es:** Meta skill que rutea al extractor correcto

**Ubicación:** `/home/danny/.npm-global/lib/node_modules/clawdbot/skills/extractor-dispatcher/SKILL.md`

**Patrón de Session Spawn:**
- Llama extractor como session independiente
- Contexto aislado (no contaminación entre meetings)

**Lógica de routing:**
| meeting_type | extractor_destino |
|-------------|------------------|
| business_sales | business_sales_extractor |
| product_project | product_project_extractor |
| strategic_founders | strategic_founders_extractor |
| operations | operations_extractor |
| general | general_extractor |

---

### 5. strategic-founders-extractor

**Qué es:** Extrae insights de meetings de CEO/founders

**Ubicación:** `/home/danny/.npm-global/lib/node_modules/clawdbot/skills/strategic-founders-extractor/SKILL.md`

**Output schema:**
- strategic_insights (decisiones, partnerships, comunicación)
- action_items (con responsible, priority, deadline)
- ceo_tasks (tareas para CEO)
- cos_tasks (tareas para CoS)
- next_steps (acciones siguientes)
- risk_assessment (estratégico, alineación, timeline)

**Probado con:**
- Danke reVIEW (CEO meeting) ✅
- Clasificación correcta como strategic_founders

---

## Extractors Creados (Backlog)

### business_sales_extractor ❌
- **Estado:** Pendiente de crear
- **Contexto:** Reuniones de ventas con clientes específicos
- **Output:** Customer feedback, pricing, pipeline, next steps

### product_project_extractor ❌
- **Estado:** Pendiente de crear
- **Contexto:** Reuniones de producto/ingeniería
- **Output:** KPIs, tecnología, decisions técnicas, roadmap

### operations_extractor ❌
- **Estado:** Pendiente de crear
- **Contexto:** Reuniones de operaciones
- **Output:** Process improvements, tools, tasks, SPOFs

### general_extractor ❌
- **Estado:** Pendiente de crear
- **Contexto:** Reuniones genéricas o sin clasificar
- **Output:** Summary general, action items sin contexto específico

---

## Cómo Combinar Meta Legos

### Escenario 1: Contexto de Helios

**Meta Legos necesarios:**
1. **meeting-orchestrator** - Orquestar reuniones de 3 founders
2. **strategic-founders-extractor** - Extraer insights de CEO/founders meetings
3. **meta-skill-maker** - Crear skill específica para Helios

**Workflow:**
```
Helios Context (Fireflies + Router Agent)
            ↓
      meeting-orchestrator (Helios-optimized)
            ↓
      strategic-founders-extractor (Helios-optimized)
            ↓
      Insights + Tasks → Project Management
```

---

### Escenario 2: Contexto de MetaGente

**Meta Legos necesarios:**
1. **meeting-orchestrator** - Orquestar reuniones de Meta (empresa, producto, marketing)
2. **product_project_extractor** - Extraer decisions de producto
3. **business_sales_extractor** - Extraer insights de ventas
4. **meta-skill-maker** - Crear skill específica para MetaGente

**Workflow:**
```
MetaGente Context (transcripts + product decisions)
            ↓
      meeting-orchestrator (Meta-optimized)
            ↓
      [product_extractor | sales_extractor] (ambos en paralelo)
            ↓
      Insights + Tasks → Project Management
```

---

### Escenario 3: Contexto de Cliente Específico

**Meta Legos necesarios:**
1. **meeting-analyzer** - Detectar contexto de cliente
2. **business_sales_extractor** - Extraer feedback de ventas
3. **custom_extractor** - (creado con meta-skill-maker) para cliente específico

**Workflow:**
```
Cliente Context (transcripts + notas)
            ↓
      meeting-analyzer (detectar customer context)
            ↓
      business_sales_extractor (customer feedback)
            ↓
      Insights + Tasks → Project Management
```

---

## Patrones Reutilizables

### Pattern 1: Orquestación Base
```
Input (transcripts/eventos)
      ↓
meeting-orchestrator (detecta tipo + rutea)
      ↓
[extractor específico] → insights + tasks
      ↓
Project Management Tool
```

### Pattern 2: Session Spawn para Aislamiento
```
Contexto compartido
      ↓
extractor-dispatcher (session spawn)
      ↓
Extractor independiente (contexto aislado)
      ↓
Output específico (sin contaminación)
```

### Pattern 3: Customización por Contexto
```
Contexto específico (ej: Helios, MetaGente)
      ↓
meta-skill-maker (crear skill específica)
      ↓
Skill optimizada para ese contexto
      ↓
Output adaptado
```

---

## Recomendaciones de Uso

### 1. Para Nuevos Contextos
1. **Identificar tipo de contexto** (Helios = founders, MetaGente = empresa, Cliente = específico)
2. **Seleccionar Meta Legos apropiados** (ver tabla de escenarios arriba)
3. **Usar meta-skill-maker** para crear skill específica si no existe
4. **Reutilizar extractores existentes** cuando apliquen

### 2. Para Expandir Meta Legos
1. **Crear extractor nuevo** (ej: financas_extractor para reuniones de CFO)
2. **Probar en múltiples contextos** antes de marcar como "reutilizable"
3. **Documentar input/output schema** en el archivo del extractor

### 3. Para Mantener Meta Legos
1. **Versionar** (v1.0, v1.1, etc.) cuando haya cambios mayores
2. **Taggear con tipo de contexto** (ej: #helios, #metagente, #cliente-x)
3. **Documentar dependencias** (qué otros Meta Legos requiere)

---

## Roadmap de Meta Legos

### Fase 1: Consolidación (Semanas 1-2)
- [ ] Documentar todos los Meta Legos existentes
- [ ] Crear extractors pendientes (business_sales, product_project, operations, general)
- [ ] Probar combinación de 2+ Meta Legos

### Fase 2: Especialización (Meses 3-4)
- [ ] Crear meta-skill-maker-v2 (para customización de contextos)
- [ ] Crear extractor para finanzas/CFO meetings
- [ ] Crear extractor para marketing meetings
- [ ] Crear extractor para HR/recruiting meetings

### Fase 3: Escalabilidad (Meses 5+)
- [ ] Sistema de versionado de Meta Legos
- [ ] Testing suite para validar combinaciones
- [ ] Documentación de patrones reutilizables

---

## Ejemplo: Crear Skill para Helios

### Usando meta-skill-maker

```bash
# Input para meta-skill-maker
cat > /tmp/helios_skill_request.json << 'EOF
{
  "skill_name": "helios-founder-insights",
  "skill_type": "extractor",
  "context": "helios",
  "purpose": "Extraer insights de reuniones de 3 founders de Helios",
  "input_schema": {
    "meeting_transcript": "string (transcript from Fireflies)",
    "context_type": "string (helios, metagente, cliente)"
  },
  "output_schema": {
    "strategic_insights": "array (decisiones, partnerships)",
    "action_items": "array (con responsible, deadline)",
    "ceo_tasks": "array (tareas para 3 founders)",
    "next_steps": "array (acciones siguientes)",
    "risk_assessment": "object (stratégico, alineación, timeline)"
  },
  "deterministic_rules": [
    "If meeting_participants include 'CEO' or 'Founder', classify as strategic_founders",
    "If 3+ founders present, require consensus on all major decisions",
    "Extract Top Goal progress and blockers"
  ],
  "meta_legos_used": [
    "meeting-orchestrator",
    "strategic-founders-extractor"
  ]
}
EOF

# Llamar a meta-skill-maker (si existe como MCP server)
mcporter call skill_creator.generate_skill request_path:/tmp/helios_skill_request.json
```

---

## Archivos Relacionados

| Archivo | Ubicación | Propósito |
|---------|-----------|-----------|
| **`meta-skill-maker/SKILL.md`** | skills/meta-skill-maker/ | Framework para crear skills |
| **`meeting-orchestrator/SKILL.md`** | mcp-servers/meeting-orchestrator/ | Orquestar reuniones |
| **`meeting-analyzer/SKILL.md`** | skills/meeting-analyzer/ | Analizar reuniones |
| **`extractor-dispatcher/SKILL.md`** | skills/extractor-dispatcher/ | Rutear a extractores |
| **`strategic-founders-extractor/SKILL.md`** | skills/strategic-founders-extractor/ | Extraer insights de founders |

---

**Próximo paso:** ¿Quieres que cree extractor para Helios usando meta-skill-maker?
