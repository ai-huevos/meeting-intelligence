# OKRs

Formato YAML: 3 Objectives x 3 KRs cada uno

## Ejemplo

```yaml
quarter: 2025-Q1
objectives:
  - id: OBJ-001
    title: "Cierre de Series A"
    key_results:
      - id: KR-001
        title: "Recaudar $2M"
        target: 2000000
        current: 0
        metric: "ARR"
        counter_metric: "Burn Rate"
      - id: KR-002
        title: "Cierre en 6 meses"
        target_date: "2025-06-30"
        status: "in_progress"
```

## Regla

Cada OKR tiene counter-metric obligatorio (ej: ARR vs Churn, Leads vs Conversion)
