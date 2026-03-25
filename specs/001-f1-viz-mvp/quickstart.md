# Quickstart: BEAUTIVIZF1 MVP initial de datavisualisation F1

## Goal

Valider progressivement le MVP sans élargir le périmètre: d'abord la demande, puis les données, puis le bundle exploitable, puis la lisibilité du rendu et enfin l'intégration web par embed.

## Suggested Validation Order

1. Vérifier qu'une demande invalide est refusée proprement.
2. Vérifier qu'une demande de heatmap valide produit un bundle complet.
3. Vérifier qu'une demande de line chart race valide produit un bundle complet.
4. Vérifier que le dataset validé et le bundle exposent bien le noyau stable attendu: `core_render_fields`, `tooltip_fields`, `presentation_fields`, traçabilité, provenance et notes.
5. Vérifier qu'un manque de couverture ou une donnée incohérente bloque ou limite explicitement la sortie.
6. Vérifier manuellement que la visualisation produite reste lisible et cohérente avec les notes.
7. Vérifier qu'un artefact d'embed dédié est présent et exploitable pour une intégration web simple.

## Reference Scenarios

### Scenario A: Heatmap

- Préparer une demande de heatmap dans le périmètre du MVP.
- Générer la visualisation.
- Vérifier la présence de `visualization.html`, d'un artefact d'embed, de `dataset.csv`, `manifest.json` et `notes.md`.
- Vérifier que les champs de rendu principaux sont présents dans le noyau stable et que les structures `tooltip_fields` et `presentation_fields` existent même avec un contenu minimal.
- Contrôler que les axes, la mesure et les limites sont compréhensibles sans investigation supplémentaire.

### Scenario B: Line Chart Race

- Préparer une demande de `line_chart_race` sur des pilotes ou des équipes couvrant plusieurs Grands Prix.
- Générer la visualisation.
- Vérifier que la progression au fil des Grands Prix est lisible et que les séries sont identifiables.
- Contrôler que la couverture des Grands Prix et les éventuelles exclusions sont explicites dans `manifest.json` et `notes.md`.
- Vérifier que le noyau stable reste identique et que l'éventuel enrichissement des tooltips ou des champs de présentation ne remplace pas les champs de rendu obligatoires.
- Vérifier que l'artefact d'embed permet une intégration web sans retraitement manuel lourd.

### Scenario C: Refusal Path

- Préparer une demande hors périmètre ou incomplète.
- Vérifier que la demande est refusée avant rendu trompeur.
- Vérifier que le motif de refus est explicite et réutilisable pour correction.

## Done When

- Les deux formats du MVP peuvent être générés de bout en bout sur un cas valide chacun.
- Le chemin de refus est explicite pour un cas invalide.
- Chaque bundle réussi contient tous les fichiers du contrat de sortie.
- Chaque bundle réussi contient aussi une sortie d'embed exploitable pour intégration web.
- Chaque bundle réussi expose un noyau stable de données commun, même si les enrichissements futurs restent minimaux au MVP.
- La revue manuelle confirme que la sortie sert l'analyse, l'explication et le storytelling sans masquer les limites.
