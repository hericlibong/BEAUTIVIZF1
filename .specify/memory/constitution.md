<!--
Sync Impact Report
Version change: N/A -> 1.0.0
Modified principles:
- Principe template 1 -> I. Fiabilité avant effet
- Principe template 2 -> II. Simplicité et lisibilité
- Principe template 3 -> III. Validation progressive
- Principe template 4 -> IV. Documentation utile
- Principe template 5 -> V. Discipline de périmètre
- Added -> VI. Décisions explicites
- Added -> VII. Testabilité
- Added -> VIII. Usage raisonné des outils d'assistance
Added sections:
- Règles de travail
- Application aux spécifications, plans et tâches
Removed sections:
- Aucune
Templates requiring updates:
- ✅ updated: .specify/templates/plan-template.md
- ✅ updated: .specify/templates/spec-template.md
- ✅ updated: .specify/templates/tasks-template.md
- ℹ not present: .specify/templates/commands/
Follow-up TODOs:
- Aucun
-->

# Constitution du projet BEAUTIVIZF1

Cette constitution fixe les règles de travail du projet BEAUTIVIZF1, dédié à la
datavisualisation autour de la Formule 1. Elle encadre la manière de spécifier,
planifier, exécuter et réviser le travail sans définir ici le MVP, l'architecture,
les formats, les endpoints ni les choix d'implémentation.

## Core Principles

### I. Fiabilité avant effet
Règle : Toute décision de conception, d'analyse ou de restitution DOIT préserver
l'exactitude des informations, la traçabilité des sources et la clarté des
transformations avant toute recherche d'effet visuel ou de sophistication.

Justification : Une datavisualisation n'a de valeur que si son fond reste
contrôlable, compréhensible et défendable.

### II. Simplicité et lisibilité
Règle : Le projet DOIT privilégier les solutions les plus simples qui couvrent le
besoin validé, avec du code, des structures et des documents faciles à relire,
expliquer et maintenir.

Justification : La lisibilité réduit les erreurs, accélère les revues et facilite
les reprises de travail.

### III. Validation progressive
Règle : Le travail DOIT avancer par étapes courtes avec validation explicite des
hypothèses, risques et arbitrages importants avant tout élargissement du
périmètre ou approfondissement technique.

Justification : Valider tôt limite les dérives, révèle les incertitudes réelles et
évite d'investir dans de mauvaises directions.

### IV. Documentation utile
Règle : La documentation DOIT rester concise, à jour et suffisante pour permettre
à une autre personne de comprendre l'intention, l'état d'avancement et les points
de vigilance sans reconstituer le contexte.

Justification : Une documentation courte mais fiable coûte moins cher à maintenir
et sert réellement de support de reprise.

### V. Discipline de périmètre
Règle : Seuls les éléments reliés à un besoin validé DOIVENT entrer dans le
périmètre actif. Toute idée intéressante mais non priorisée DOIT être explicitement
mise en attente plutôt qu'introduite discrètement.

Justification : La maîtrise du périmètre protège la qualité d'exécution et garde
le projet focalisé.

### VI. Décisions explicites
Règle : Tout arbitrage important DOIT être formulé clairement, avec son contexte,
sa justification et, si utile, l'alternative écartée. Les décisions implicites
ou enfouies dans le code ne sont pas acceptables.

Justification : Les décisions explicites améliorent la cohérence du projet et
évitent de rouvrir les mêmes débats sans base commune.

### VII. Testabilité
Règle : Toute partie importante du projet DOIT pouvoir être vérifiée de manière
claire. La validation manuelle est acceptable au départ si elle est décrite sans
ambiguïté, puis elle DOIT devenir plus reproductible lorsque le risque, la
fréquence ou la maturité du projet l'exigent.

Justification : La testabilité rend les progrès observables et réduit le coût des
régressions.

### VIII. Usage raisonné des outils d'assistance
Règle : Les outils d'IA, de recherche ou d'automatisation DOIVENT accélérer le
travail sans remplacer la compréhension technique, l'esprit critique ni la mise
en évidence des incertitudes restantes.

Justification : L'assistance est utile tant qu'elle ne masque ni les hypothèses,
ni les lacunes, ni les responsabilités de décision.

## Règles de travail

- Chaque nouvelle étape DOIT préciser son objectif, ses hypothèses, ses limites
  et son mode de validation avant de produire du travail aval.
- Toute information incertaine DOIT être signalée explicitement ; une hypothèse
  critique ne DOIT jamais être dissimulée dans l'implémentation ou la rédaction.
- Toute extension de périmètre DOIT faire l'objet d'un arbitrage explicite avant
  d'entrer dans un plan ou une liste de tâches.
- Chaque livrable DOIT laisser une trace minimale exploitable : décisions prises,
  validation réalisée, documentation à jour ou dette documentaire identifiée.

## Application aux spécifications, plans et tâches

- Les spécifications DOIVENT décrire le besoin, les limites de périmètre, les
  hypothèses, les incertitudes et les critères de validation sans glisser vers des
  choix d'architecture ou d'implémentation non décidés.
- Les plans DOIVENT découper le travail en étapes contrôlables, expliciter les
  principaux arbitrages et prévoir des points d'arrêt où les hypothèses sont
  revues avant de continuer.
- Les tâches DOIVENT être petites, traçables et ordonnées. Toute tâche importante
  DOIT indiquer comment elle sera vérifiée et si elle implique une mise à jour de
  documentation ou de décision.
- Aucun artefact ne DOIT introduire implicitement un périmètre, une complexité ou
  une certitude qui n'ont pas été clairement validés.

## Governance

- Cette constitution prévaut sur les habitudes locales du projet lorsqu'un conflit
  d'interprétation apparaît.
- Toute spécification, tout plan et toute liste de tâches DOIVENT inclure une
  vérification explicite de conformité à cette constitution avant approbation ou
  exécution.
- Toute modification de la constitution DOIT être motivée par écrit, inclure son
  impact sur les templates et être versionnée selon une logique sémantique :
  MAJOR pour une rupture de gouvernance, MINOR pour un ajout ou un renforcement
  significatif, PATCH pour une clarification sans changement de fond.
- La revue de conformité DOIT vérifier au minimum : la clarté du périmètre, la
  justification des décisions, l'existence d'un mode de validation et l'adéquation
  de la documentation au niveau d'avancement.

**Version**: 1.0.0 | **Ratified**: 2026-03-25 | **Last Amended**: 2026-03-25
