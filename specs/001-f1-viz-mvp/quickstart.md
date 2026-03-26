# Quickstart: Chatbot simple de datavisualisation F1

## Goal

Valider progressivement le vrai flux MVP: besoin exprimé en langage naturel, interprétation, proposition des deux formats disponibles, choix explicite du format, récupération des données, génération D3.js, sortie embed et bundle minimal de vérification.

## Suggested Validation Order

1. Vérifier qu'une demande analytique en langage naturel est interprétée ou mène à une clarification simple.
2. Vérifier que le chatbot présente explicitement la heatmap et la line chart race comme les deux formats disponibles du MVP.
3. Vérifier qu'aucune génération ne se lance avant le choix explicite de l'un de ces deux formats.
4. Vérifier qu'un choix valide de heatmap produit une visualisation web, un embed explicite et un bundle minimal de vérification.
5. Vérifier qu'un choix valide de line chart race produit une visualisation web, un embed explicite et un bundle minimal de vérification.
6. Vérifier que le dataset validé et le bundle exposent le noyau stable attendu, la provenance et les notes de validation.
7. Vérifier qu'une demande ambiguë, hors périmètre ou incohérente mène à une clarification simple ou à un refus explicite.

## Reference Scenarios

### Scenario A: Heatmap via guided choice

- L'utilisateur exprime un besoin analytique en langage naturel.
- Le chatbot interprète ce besoin et présente les deux formats disponibles du MVP.
- L'utilisateur choisit la heatmap.
- Le système génère la visualisation, l'embed et le bundle de vérification.
- La validation vérifie la lisibilité, la provenance et la complétude du bundle.

### Scenario B: Line Chart Race via guided choice

- L'utilisateur exprime un besoin analytique en langage naturel.
- Le chatbot interprète ce besoin et présente les deux formats disponibles du MVP.
- L'utilisateur choisit la line chart race.
- Le système génère la visualisation montrant la progression des pilotes ou des équipes au fil des Grands Prix.
- La validation vérifie l'embed, la provenance et la cohérence du bundle.

### Scenario C: Clarification or refusal

- L'utilisateur exprime un besoin trop flou, incohérent ou hors périmètre.
- Le chatbot demande une précision courte ou refuse explicitement.
- Aucune génération ne démarre tant qu'aucun choix explicite de format valide n'existe.

## Done When

- Le chatbot suit correctement le flux demande -> interprétation -> proposition des formats -> choix explicite -> génération.
- Les deux formats du MVP peuvent être générés de bout en bout dans ce flux.
- Chaque résultat valide comprend visualisation web, embed explicite et bundle minimal de vérification.
- Les cas de clarification et de refus sont explicites et ne déclenchent pas de génération prématurée.
