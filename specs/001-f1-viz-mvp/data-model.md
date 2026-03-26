# Data Model: Chatbot simple de datavisualisation F1

## 1. ConversationRequest

Représente le message initial en langage naturel par lequel l'utilisateur exprime un besoin analytique ou éditorial autour de la Formule 1.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `request_id` | string | Yes | Identifiant de traçabilité de la demande |
| `user_message` | string | Yes | Expression libre du besoin utilisateur |
| `created_at` | datetime | Yes | Horodatage de la demande |
| `conversation_context` | object | No | Contexte minimal utile si la demande s'inscrit dans un échange court |

### Validation Rules

- La demande initiale ne porte pas encore sur un format choisi.
- La demande doit rester centrée sur un seul besoin analytique exploitable.

## 2. VisualizationIntent

Interprétation structurée du besoin exprimé avant tout choix du format de visualisation.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `intent_id` | string | Yes | Identifiant de l'intention interprétée |
| `request_id` | string | Yes | Référence à `ConversationRequest` |
| `analytic_need` | string | Yes | Formulation synthétique du besoin compris |
| `subject_scope` | object | Yes | Sujet, périmètre et angle d'analyse utiles |
| `clarification_needed` | boolean | Yes | Indique si le besoin est suffisamment clair |
| `clarification_note` | string | No | Précision attendue si l'intention reste insuffisante |

### Validation Rules

- L'intention doit être exploitable avant la présentation des formats.
- Si l'intention reste ambiguë, aucune proposition de génération ne doit suivre sans clarification.

## 3. FormatSelection

Trace la présentation des deux formats du MVP et le choix explicite fait par l'utilisateur.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `selection_id` | string | Yes | Identifiant de l'étape de choix |
| `intent_id` | string | Yes | Référence à `VisualizationIntent` |
| `available_formats` | list | Yes | Doit contenir `heatmap` et `line_chart_race` |
| `chosen_format` | enum | Yes | `heatmap` ou `line_chart_race` |
| `choice_confirmed_at` | datetime | Yes | Horodatage du choix explicite |
| `proposal_note` | string | No | Formulation courte du guidage présenté à l'utilisateur |

### Validation Rules

- Aucune génération ne peut démarrer sans `chosen_format`.
- Le format choisi doit faire partie des deux formats explicitement proposés.

## 4. SourceDataset

Jeu de données récupéré depuis les sources F1 après le choix explicite du format.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `dataset_id` | string | Yes | Identifiant interne du lot récupéré |
| `selection_id` | string | Yes | Référence à `FormatSelection` |
| `source_name` | string | Yes | Source principale des données chiffrées |
| `season` | integer | Yes | Saison couverte |
| `covered_rounds` | list | No | Rounds effectivement présents si pertinents |
| `records` | table reference | Yes | Table brute ou quasi brute |
| `retrieved_at` | datetime | Yes | Horodatage de récupération |
| `provenance_note` | string | Yes | Note courte de provenance et couverture |

### Validation Rules

- La provenance doit être explicite et traçable.
- NotebookLM/MCP ne peut pas apparaître comme source principale des données chiffrées.

## 5. ValidatedVisualizationDataset

Jeu de données transformé et contrôlé, prêt pour le rendu après interprétation du besoin et choix du format.

### Noyau stable du MVP

Le MVP verrouille un noyau commun stable pour le rendu, la traçabilité et la vérification.

- `core_render_fields`: obligatoires; suffisent à dessiner la visualisation.
- `tooltip_fields`: structure prévue maintenant, enrichissement différé.
- `presentation_fields`: structure prévue maintenant, enrichissement différé.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `validated_dataset_id` | string | Yes | Identifiant du dataset validé |
| `selection_id` | string | Yes | Référence à `FormatSelection` |
| `source_dataset_id` | string | Yes | Référence au dataset source |
| `chosen_format` | enum | Yes | Format validé pour le rendu |
| `traceability_keys` | object | Yes | Liens entre demande, intention, choix, source et bundle |
| `core_render_fields` | table reference | Yes | Champs minimaux nécessaires au rendu principal |
| `tooltip_fields` | object | Yes | Structure stable prévue pour les enrichissements futurs |
| `presentation_fields` | object | Yes | Structure stable prévue pour les enrichissements futurs |
| `coverage_summary` | object | Yes | Résumé de couverture et exclusions éventuelles |
| `provenance` | object | Yes | Source chiffrée retenue et contexte de couverture |
| `validation_status` | enum | Yes | `ready`, `limited`, `rejected` |
| `validation_notes` | list | Yes | Hypothèses, limites et points de vigilance |

### Validation Rules

- `core_render_fields` doit suffire au rendu du MVP.
- `tooltip_fields` et `presentation_fields` existent comme structures stables même si leur contenu reste minimal.
- L'enrichissement futur de ces structures ne doit pas casser le socle défini par `traceability_keys`, `core_render_fields`, `provenance` et `validation_notes`.

## 6. VisualizationBundle

Ensemble des artefacts finaux livrés à l'utilisateur après génération.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `bundle_id` | string | Yes | Identifiant du lot exporté |
| `selection_id` | string | Yes | Référence au choix de format confirmé |
| `rendered_visualization` | file reference | Yes | Visualisation web produite |
| `embed_export` | file reference | Yes | Sortie explicite d'intégration web |
| `dataset_export` | file reference | Yes | Export des données utilisées |
| `manifest` | file reference | Yes | Synthèse exploitable de la génération |
| `verification_notes` | file reference | Yes | Notes de provenance, hypothèses et limites |
| `core_schema_version` | string | Yes | Version du socle stable du bundle |
| `created_at` | datetime | Yes | Horodatage d'export |

### Validation Rules

- Aucun bundle n'est valide sans visualisation web, embed explicite et bundle minimal de vérification.
- Le bundle doit exposer le choix du format, la provenance, les notes de validation et le noyau stable du dataset validé.

## Relationships

- `ConversationRequest` est interprétée en `VisualizationIntent`.
- `VisualizationIntent` mène à une `FormatSelection`.
- `FormatSelection` autorise la récupération d'un `SourceDataset`.
- `SourceDataset` est transformé en `ValidatedVisualizationDataset`.
- `ValidatedVisualizationDataset` est exporté dans un `VisualizationBundle`.
