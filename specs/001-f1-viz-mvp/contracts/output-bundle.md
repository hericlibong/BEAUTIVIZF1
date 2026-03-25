# Contract: Output Bundle

## Purpose

Définir le bundle minimal que chaque génération réussie doit produire pour être considérée comme exploitable, vérifiable, réutilisable et intégrable sur le web.

Le contrat verrouille un noyau stable pour le MVP et réserve explicitement l'enrichissement futur des données de survol et de présentation.

## Bundle Contents

| File | Required | Purpose |
|------|----------|---------|
| `manifest.json` | Yes | Résume la demande, la couverture, le statut et les fichiers produits |
| `dataset.csv` | Yes | Contient les données effectivement utilisées pour le rendu |
| `notes.md` | Yes | Documente hypothèses, limites, exclusions et provenance |
| `visualization.html` | Yes | Sortie de visualisation réutilisable pour lecture web |
| `embed.html` ou `embed-snippet.html` | Yes | Sortie explicite d'intégration web pour embarquer la visualisation |

## Bundle Guarantees

- Tous les fichiers doivent se rapporter au même `request_id`.
- Le `manifest.json` doit rappeler le `chart_type`, la couverture analysée et le statut de validation.
- `notes.md` doit rendre explicites les hypothèses et limites qui affectent la lecture.
- `dataset.csv` doit être suffisant pour vérifier la cohérence du rendu sans réinterroger la source.
- L'artefact d'embed doit permettre l'intégration web sans exiger de plateforme de publication dédiée.
- Le bundle doit rester exploitable même si NotebookLM/MCP est indisponible, car cet outil n'est pas une dépendance du pipeline de rendu.

## Stable Data Expectations

Le bundle doit exposer un socle commun minimal, stable et traçable pour les deux formats du MVP.

- `core_render_fields`: obligatoires; ils portent les champs strictement nécessaires au dessin principal de la visualisation.
- `tooltip_fields`: structure prévue dès maintenant; leur contenu peut rester minimal au MVP puis être enrichi ensuite.
- `presentation_fields`: structure prévue dès maintenant; leur contenu peut rester minimal au MVP puis être enrichi ensuite.
- `traceability_keys`, `provenance` et `validation_notes`: obligatoires pour garder la sortie vérifiable et réutilisable.

L'enrichissement futur de `tooltip_fields` et `presentation_fields` est autorisé tant qu'il ne casse pas ce socle minimal ni la structure stable du bundle.

## Failure Contract

Si une demande est rejetée, le système ne produit pas de bundle complet de visualisation. Il produit au minimum une explication exploitable de rejet pour éviter toute sortie trompeuse.
