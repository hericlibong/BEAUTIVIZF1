# Contract: Output Bundle

## Purpose

Définir le bundle minimal que chaque génération réussie doit produire pour être considérée comme exploitable, vérifiable, réutilisable et intégrable sur le web.

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

## Failure Contract

Si une demande est rejetée, le système ne produit pas de bundle complet de visualisation. Il produit au minimum une explication exploitable de rejet pour éviter toute sortie trompeuse.
