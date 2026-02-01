# PRD: Ingestion Pipeline MVP - Kompass KOM-01

## 1. Context

### Client Context (Kompass - Holding Group)
- **Business:** Trade company (imports Chinese products)
- **Problem:** Manual bottleneck: WeChat/PDF → Excel → Image cropping → Portfolio creation
- **Volume:** 55 quotes/3 months (freno de mano)
- **Goal:** Automatizar el 80% del proceso

### Hay Huevos Context
- **Proposal:** Montar "Motor de Ingesta" para Kompass
- **IP Ownership:** "Nosotros tenemos el Engine; Kompass tiene la License"
- **Principio:** "Impeccable Agreements" (Mochary)

---

## 2. Current Process (The Pain)

### Manual Chain (El cuello de botella)
```
WeChat PDF (Chino) → Manual Excel Entry → Manual Image Cropping (Google Lens) → Manual Portfolio Upload → Email a cliente
     │                    │                        │                       │                         │
     │                    └────────────────────────────────└─────────────────────────┘
                              ↑                    ↑
                         Toma días completar         Toma semanas completar
```

### Two Critical Bottlenecks

1. **PDF Parsing (Chino):** Toman datos manualmente del WeChat
2. **Image Processing:** Dedican tiempo a "remover backgrounds" con Google Lens

---

## 3. The "Traps" (Socratic Feedback)

### Trap #1: The Image Paradox
**Diagnosis:** Si automatizamos Data Entry (Excel) pero no Design (Imágenes), solo ahorran 50% del tiempo.

**Root Cause:**
- Product Agent crea Excel pero NO remueve backgrounds
- Kompass sigue perdiendo tiempo en Google Lens + Cropping

**Solution:**
- **Vision Model API Requirement:** "Remove Background" endpoint
- Output: PNG limpio + PNG con fondo original (ambos)
- Automatización 100% del flujo

### Trap #2: IP Ownership Ambiguity
**Diagnosis:** ¿Kompass cree que paga por "Custom Dev" que les pertenece?

**Risk:**
- Confusión sobre propiedad intelectual
- Disputas futuras si el "Engine" escala

**Solution:**
- **Claro en el contrato:** "Nosotros tenemos el Engine (IP); Kompass tiene la License de uso"
- **Especificación:** No redistribución, no reventa del código source

---

## 4. Ingestion Pipeline MVP

### User Story
**Como:** Alejo (Operations Manager, Kompass)
**Quiero:** Forward a Chinese PDF to a bot, and have it populate the "Master Excel" automatically.

### Technical Constraints
1. **Must handle Images:** Diana/Alejo usan Google Lens/Cropping
2. **Chinese PDF parsing:** Character encoding issues
3. **Portfolio format:** Excel matrix con image references

---

## 5. Solution Architecture

### Pipeline Flow

```
┌─────────────────────────────────────────────┐
│         INPUT: WeChat PDF (Chino)      │
└─────────────────────────────────────────────┘
                 │
                 ▼
      ┌───────────────────┐
      │  PDF Parser      │ ← Step 1: Extraer texto + datos
      └───────────────────┘
                 │
                 ▼
      ┌───────────────────┐
      │  Image Processor │ ← Step 2: Remove Background
      │  (Vision API)    │    Output: PNG limpio + PNG original
      └───────────────────┘
                 │
                 ▼
      ┌───────────────────┐
      │  Excel Generator  │ ← Step 3: Populate Master Excel
      │  (Row por producto) │    Referencias: PNG limpios
      └───────────────────┘
                 │
                 ▼
      ┌───────────────────┐
      │  Notion/Drive      │ ← Step 4: Almacenar para Kompass
      │  (Master Excel +     │
      │   Imágenes limpias)  │
      └───────────────────┘
```

---

## 6. Tech Stack

### Step 1: PDF Parser
- **Library:** `pdf-parse` (Node.js)
- **Chinese Support:** Font encoding (UTF-8 + CJK fonts)
- **Extracción:**
  - Título del producto
  - Precio (RMB)
  - Especificaciones técnicas
  - URL de imagen (si embedded)

### Step 2: Image Processor (Vision API)
- **Options:**
  - **OpenAI Vision API:** `remove-background` (beta, pero robusto)
  - **Clipdrop:** API especializada en background removal
  - **Stability AI:** `stable-diffusion-xl` + segmentation

**Output:**
- `product_{id}_clean.png` - Sin fondo (para uso en Excel/Notion)
- `product_{id}_original.png` - Con fondo (para backup)

### Step 3: Excel Generator
- **Format:** XLSX (xlsx library)
- **Estructura:**

| ID | Título | Precio (RMB) | Imagen limpia | Imagen original | Notas |
|-----|---------|----------------|----------------|------------------|--------|
| P001 | Nombre | 12.50 | product_001_clean.png | product_001_original.png | {extraction_data} |

### Step 4: Storage Integration
- **Google Drive API:** Subir Master Excel + Imágenes
- **Notion API:** Crear database referenciada

---

## 7. API Endpoints (MVP)

### `POST /api/ingest/pdf`
**Input:** `multipart/form-data`
- `file`: PDF de WeChat
- `options`:
  - `remove_background`: true/false
  - `format`: "excel"|"notion"

**Output:**
```json
{
  "job_id": "ingest_kompass_001",
  "status": "processing",
  "estimated_time": "30s",
  "webhook_url": "https://kompass.ai/webhooks/ingest"
}
```

### `GET /api/ingest/status/:job_id`
**Output:**
```json
{
  "job_id": "ingest_kompass_001",
  "status": "completed"|"processing"|"failed",
  "progress": 75,
  "result": {
    "excel_url": "https://drive.google.com/...",
    "clean_images": ["product_001_clean.png"],
    "original_images": ["product_001_original.png"],
    "total_products": 15
  }
}
```

---

## 8. Success Metrics

| Métrica | Target | "So What?" |
|---------|--------|------------|
| **Processing Time** | <60s por PDF | De 30 min a <1 min |
| **Image Quality** | 95% backgrounds removidos | Productos usables sin editing |
| **Throughput** | 55 quotes/mes → Automatizado | Volumen sostenido sin bots |
| **Error Rate** | <5% parsing failures | Fiabilidad en Chinese characters |

---

## 9. IP Ownership Clause (Crucial)

### Contract Addendum

**Para incluir en contrato con Kompass:**

> "Engine Ownership & Licensing"
>
> **IP Ownership:**
> - Hay Huevos (fundador) mantiene toda la propiedad intelectual del "Ingestion Pipeline" (código fuente, algoritmos, modelos de IA).
> - Kompass recibe una **License exclusiva, no-transferible, no-redistribuible** de uso del Engine.
>
> **Scope de License:**
> - Kompass tiene derecho de USAR el Engine para procesar documentos WeChat → Excel.
> - Kompass NO tiene derecho a redistribuir, vender, o sublicenciar el código fuente.
> - Cualquier mejora o customización se realiza como **servicio adicional** facturado por Hay Huevos.
>
> **Non-Compromise:**
> - Kompass puede acceder a su data procesada (Excel + Imágenes) en todo momento.
> - Hay Huevos mantiene acceso únicamente para soporte y updates del Engine.
>
> **So What?**
> - Elimina el "IP Trap": Kompass sabe exactamente qué están pagando (licencia de uso).
> - Protege a Hay Huevos: No pierden control de su IP.
> - Escalabilidad segura: Si Kompass scale, no pueden "tomar el código y hacerlo ellos".

---

## 10. Pricing Model

### MVP Pricing (Kompass)

| Item | Costo Mensual | Setup Fee |
|------|----------------|------------|
| **Engine License** | $299 | Gratis (onboarding) |
| **Vision API Usage** | Usage based (OpenAI) | Incluido |
| **Support SLA** | 24/7 response | 1 incidento gratis/mes |

### Customization (Opcional)
- $2,000 por feature
- Ejemplo: "Add OCR para manuscritos chinos"
- Ejemplo: "Bulk processing (100+ PDFs)"

---

## 11. Implementation Timeline

### Sprint 1 (Semanas 1-2)
- [ ] **PDF Parser:** Chinese encoding, extracción de datos
- [ ] **Vision API Integration:** OpenAI remove-background
- [ ] **Excel Generator:** Template de Master Matrix

### Sprint 2 (Semanas 3-4)
- [ ] **Google Drive API:** Subir outputs
- [ ] **Notion Integration:** Referencias dinámicas
- [ ] **Webhooks:** Status updates a Kompass

### Sprint 3 (Semanas 5-6)
- [ ] **Error Handling:** Retry logic para fallidos
- [ ] **UI/UX (Ops):** Dashboard para Alejo monitorear jobs
- [ ] **Contract Addendum:** Cláusula de IP Ownership

---

## 12. Risks & Mitigations

| Risk | Probabilidad | Mitigation |
|------|------------|------------|
| **Chinese Parsing Fails** | Media | Fallback: Allow manual override with OCR correction |
| **Vision API Cost** | Alta | Cache results, usage monitoring, rate limiting |
| **Kompass Adoption** | Media | Training + Success stories (55 quotes/month metric) |
| **IP Dispute** | Baja | Contract addendum + Legal review |

---

## 13. Immediate Next Step

### Para Router Agent
Cuando el transcript de Kompass mencione "Chinese PDF" o "Ingestion":

```json
{
  "routing_flags": {
    "requires_product_action": true,
    "priority": "HIGH"
  },
  "context_layer": {
    "diagnosis_pain": "Manual bottleneck: WeChat/PDF → Excel taking 30 min per product. 55 quotes/3 months lost.",
    "technical_facts": {
      "current_stack": "Manual, Google Lens, Excel",
      "requested_features": ["Remove Background", "Chinese PDF Parsing"],
      "constraints": "Vision Model budget, Chinese character encoding"
    }
  }
}
```

**Swarm Instructions for Product Agent:**
```
Create Linear Ticket: "KOM-01: Ingestion Pipeline MVP"

Scope:
1. PDF Parser (Chinese encoding)
2. Vision API (Remove Background)
3. Excel Generator (Master Matrix)
4. Drive/Notion Integration

Priority: HIGH
Assignee: Founder B
```

---

**Next Step:** Implementar Sprint 1 (PDF Parser + Vision API)
