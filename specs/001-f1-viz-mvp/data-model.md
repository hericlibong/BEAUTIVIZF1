# Data Model: BEAUTIVIZF1 MVP initial de datavisualisation F1

## 1. VisualizationRequest

Représente la demande utilisateur normalisée avant toute récupération de données.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `request_id` | string | Yes | Identifiant de traçabilité du traitement |
| `chart_type` | enum | Yes | `heatmap` ou `line_chart_race` |
| `season` | integer | Yes | Saison F1 ciblée |
| `scope_type` | enum | Yes | `single_event`, `grand_prix_sequence`, `season_slice` |
| `subject_type` | enum | Conditional | `drivers` ou `teams`, requis pour `line_chart_race` |
| `metric` | string | Yes | Mesure principale à représenter |
| `dimensions` | object | Conditional | Axes de comparaison requis pour `heatmap` |
| `round_range` | object | Conditional | Borne de Grands Prix requise pour `line_chart_race` et certaines heatmaps |
| `filters` | object | No | Filtres additionnels autorisés dans le périmètre du MVP |
| `analysis_note` | string | No | Formulation courte de l'intention éditoriale |

### Validation Rules

- `chart_type` doit appartenir aux deux formats du MVP.
- Une demande ne peut porter que sur une seule visualisation.
- Une `line_chart_race` exige au minimum une séquence de deux Grands Prix.
- Une `heatmap` exige des axes de comparaison et une mesure visuellement comparable.
- Toute demande ambiguë ou hors périmètre est rejetée avant récupération.

## 2. SourceDataset

Jeu de données récupéré depuis la source F1 avant transformation métier.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `dataset_id` | string | Yes | Identifiant interne du lot récupéré |
| `source_name` | string | Yes | Source de données chiffrées utilisée, distincte des outils documentaires |
| `season` | integer | Yes | Saison couverte |
| `covered_rounds` | list | Yes | Rounds effectivement présents dans le lot |
| `subject_type` | enum | No | `drivers`, `teams` ou vide selon le lot |
| `records` | table reference | Yes | Table brute ou quasi brute |
| `retrieved_at` | datetime | Yes | Horodatage de récupération |
| `provenance_note` | string | Yes | Note courte de provenance et couverture |

### Validation Rules

- Les rounds attendus doivent être explicitement comparés aux rounds couverts.
- Les colonnes nécessaires au format demandé doivent être présentes avant transformation.
- Les incohérences de granularité ou de couverture doivent être signalées avant rendu.
- NotebookLM/MCP ne peut pas être enregistré comme source principale de données chiffrées dans ce modèle.

## 3. ValidatedVisualizationDataset

Jeu de données transformé et contrôlé, prêt pour un rendu déterministe.

### Noyau stable du MVP

Le MVP verrouille maintenant un noyau commun minimal pour toutes les visualisations. Ce noyau doit rester stable d'un format à l'autre et d'une itération à l'autre.

- `core_render_fields`: champs indispensables pour dessiner la visualisation; obligatoires dès le MVP.
- `tooltip_fields`: structure prévue dès maintenant pour les enrichissements de survol; enrichissement progressif ensuite.
- `presentation_fields`: structure prévue dès maintenant pour les enrichissements de présentation; enrichissement progressif ensuite.

L'objectif est de stabiliser le socle de rendu et de traçabilité sans figer trop tôt l'ensemble des métriques secondaires, tooltips enrichis ou conventions de présentation.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `validated_dataset_id` | string | Yes | Identifiant du lot prêt à rendre |
| `request_id` | string | Yes | Référence à `VisualizationRequest` |
| `source_dataset_id` | string | Yes | Référence au lot source utilisé pour construire ce dataset validé |
| `chart_type` | enum | Yes | Format final visé |
| `traceability_keys` | object | Yes | Identifiants et clés permettant de relier demande, source, couverture et bundle |
| `core_render_fields` | table reference | Yes | Champs minimaux obligatoires pour dessiner la visualisation principale |
| `tooltip_fields` | object | Yes | Structure prévue pour les données de survol; contenu minimal possible au MVP, enrichissement extensible ensuite |
| `presentation_fields` | object | Yes | Structure prévue pour labels, couleurs et autres aides de présentation; contenu minimal possible au MVP, enrichissement extensible ensuite |
| `series_definition` | object | Yes | Définition des lignes ou cellules à afficher à partir du noyau de rendu |
| `coverage_summary` | object | Yes | Résumé de couverture et éventuelles exclusions |
| `provenance` | object | Yes | Provenance de la donnée, source chiffrée retenue et contexte de couverture |
| `validation_status` | enum | Yes | `ready`, `limited`, `rejected` |
| `validation_notes` | list | Yes | Hypothèses, limites et points de vigilance |

### Validation Rules

- `core_render_fields` doit suffire à produire la visualisation sans dépendre d'un enrichissement ultérieur.
- `tooltip_fields` et `presentation_fields` doivent exister comme structures stables, même si leur contenu reste minimal au MVP.
- L'enrichissement futur de `tooltip_fields` et `presentation_fields` ne doit pas casser le socle défini par `core_render_fields`, `traceability_keys`, `provenance` et `validation_notes`.
- Le statut `ready` n'est autorisé que si les données et le cadrage sont cohérents.
- Le statut `limited` exige des notes explicites sur la limite restante.
- Le statut `rejected` bloque toute génération de visualisation présentée comme fiable.

## 4. VisualizationBundle

Ensemble des artefacts livrés au créateur pour usage éditorial, reprise et intégration web.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `bundle_id` | string | Yes | Identifiant du lot exporté |
| `request_id` | string | Yes | Référence à la demande initiale |
| `chart_type` | enum | Yes | Format rendu |
| `rendered_visualization` | file reference | Yes | Fichier de visualisation exporté |
| `embed_export` | file reference | Yes | Artefact dédié à l'intégration web de la visualisation |
| `dataset_export` | file reference | Yes | Export tabulaire des données utilisées |
| `manifest` | file reference | Yes | Fichier de synthèse exploitable |
| `verification_notes` | file reference | Yes | Notes de limites et hypothèses |
| `core_schema_version` | string | Yes | Version du noyau stable du bundle et du dataset validé |
| `created_at` | datetime | Yes | Horodatage d'export |

### Validation Rules

- Aucun bundle réussi ne peut être publié ou intégré sans `manifest`, `dataset_export`, `verification_notes` et `embed_export`.
- Le bundle doit exposer un noyau stable comprenant au minimum les clés de traçabilité, la provenance, les notes de validation et les champs de rendu principaux.
- Le bundle peut enrichir ensuite les données de tooltip et de présentation sans casser sa structure de base.
- Le bundle doit référencer les mêmes hypothèses et limites que le dataset validé.

## Relationships

- `VisualizationRequest` déclenche la récupération d'un `SourceDataset`.
- `SourceDataset` est transformé en `ValidatedVisualizationDataset`.
- `ValidatedVisualizationDataset` est exporté dans un `VisualizationBundle`.
- `VisualizationBundle` hérite des notes de validation et de provenance des étapes précédentes.
