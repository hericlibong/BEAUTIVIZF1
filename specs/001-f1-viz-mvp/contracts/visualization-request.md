# Contract: Visualization Request

## Purpose

Définir le contrat d'entrée minimal pour demander une visualisation dans le périmètre du MVP.

## Interface

- **Consumer**: créateur du projet BEAUTIVIZF1
- **Provider**: point d'entrée CLI du générateur de visualisation
- **Cardinality**: une demande produit au maximum une visualisation

## Required Fields

| Field | Description |
|-------|-------------|
| `chart_type` | `heatmap` ou `line_chart_race` |
| `season` | Saison F1 ciblée |
| `metric` | Mesure principale à représenter |
| `scope_type` | Type de périmètre demandé |

## Conditional Fields

| Condition | Additional Field | Rule |
|-----------|------------------|------|
| `chart_type = heatmap` | `dimensions` | Doit définir les axes de comparaison |
| `chart_type = line_chart_race` | `subject_type` | Doit être `drivers` ou `teams` |
| `chart_type = line_chart_race` | `round_range` | Doit couvrir au moins deux Grands Prix |
| Périmètre filtré | `filters` | Autorisé seulement s'il reste dans le MVP |

## Validation Outcomes

| Outcome | Meaning |
|---------|---------|
| `accepted` | La demande est assez précise pour lancer la récupération |
| `limited` | La demande est compréhensible mais requiert une note de limite explicite |
| `rejected` | La demande est hors périmètre, ambiguë ou non vérifiable |

## Rejection Rules

- Refuser les demandes multi-visualisations.
- Refuser les demandes hors des deux formats du MVP.
- Refuser les line chart races sans séquence exploitable de Grands Prix.
- Refuser les heatmaps avec mesure ou dimensions non comparables.
