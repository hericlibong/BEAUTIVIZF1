# Feature Specification: MVP initial de datavisualisation F1

**Feature Branch**: `001-f1-viz-mvp`  
**Created**: 2026-03-25  
**Status**: Draft  
**Input**: User description: "Rédige la spécification initiale du projet BEAUTIVIZF1 pour un MVP limité à une heatmap et un race line chart de datavisualisation F1 fiables, compréhensibles, vérifiables et réutilisables."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Produire une heatmap fiable (Priority: P1)

En tant que créateur de BEAUTIVIZF1, je veux formuler une demande simple de heatmap F1 afin d'obtenir rapidement une visualisation comparative exploitable pour l'analyse et le storytelling.

**Why this priority**: La heatmap constitue un premier format compact pour comparer des valeurs F1 sur un axe éditorial clair. C'est un format simple à cadrer et utile pour valider le socle du MVP.

**Independent Test**: Cette story peut être testée indépendamment en soumettant une demande de heatmap dans le périmètre du MVP et en vérifiant que le résultat comprend la visualisation, les données utilisées et les limites explicites.

**Acceptance Scenarios**:

1. **Given** une demande qui précise le format heatmap, le périmètre d'analyse et une mesure comparable, **When** le système traite la demande avec des données disponibles et cohérentes, **Then** il produit une heatmap exploitable accompagnée du jeu de données utilisé et de notes de vérification.
2. **Given** une demande de heatmap incomplète ou portant sur une mesure non comparable, **When** le système tente de la traiter, **Then** il signale clairement pourquoi la demande ne peut pas être produite telle quelle et n'affiche pas de visualisation trompeuse.

---

### User Story 2 - Produire une line chart race lisible (Priority: P2)

En tant que créateur de BEAUTIVIZF1, je veux obtenir une line chart race à partir d'une demande simple afin de montrer la progression des pilotes ou des équipes au fil des Grands Prix de manière lisible et vérifiable.

**Why this priority**: La line chart race répond à un besoin narratif fort à l'échelle d'une saison ou d'une séquence de Grands Prix. Elle complète la heatmap avec une lecture dynamique de la progression et permet de raconter l'évolution d'un championnat de façon éditorialement utile.

**Independent Test**: Cette story peut être testée indépendamment en soumettant une demande de line chart race portant sur des pilotes ou des équipes sur plusieurs Grands Prix, puis en vérifiant que la progression est compréhensible, que les séries affichées sont identifiables et que les limites explicites sont bien présentes.

**Acceptance Scenarios**:

1. **Given** une demande de line chart race portant sur des pilotes ou des équipes et sur une séquence identifiable de Grands Prix, **When** le système traite la demande avec des données cohérentes et comparables, **Then** il produit une visualisation exploitable montrant clairement la progression au fil des Grands Prix, accompagnée du jeu de données utilisé et de notes de vérification.
2. **Given** une demande de line chart race dont la couverture en Grands Prix, les séries à comparer ou les données de progression sont manquantes, partielles ou incohérentes, **When** le système l'évalue, **Then** il refuse ou limite explicitement la sortie au lieu de produire une visualisation présentée comme fiable.

---

### User Story 3 - Vérifier et réutiliser le résultat (Priority: P3)

En tant que créateur de BEAUTIVIZF1, je veux comprendre immédiatement ce que montre la visualisation, d'où viennent les données et quelles hypothèses s'appliquent afin de réutiliser le résultat dans un travail éditorial sans ambiguïté.

**Why this priority**: La valeur du projet repose sur la confiance et sur la réutilisation. Une visualisation non vérifiable ou difficile à réexploiter ne répond pas à l'intention produit, même si elle est visuellement correcte.

**Independent Test**: Cette story peut être testée indépendamment en examinant une visualisation produite dans le périmètre et en vérifiant que son contexte, ses hypothèses et son matériau de base sont suffisamment explicites pour une relecture éditoriale.

**Acceptance Scenarios**:

1. **Given** une visualisation générée dans le périmètre du MVP, **When** le créateur consulte le résultat, **Then** il peut identifier la source, la couverture analysée, les hypothèses retenues et les limites connues sans recherche supplémentaire.
2. **Given** une visualisation générée dans le périmètre du MVP, **When** le créateur veut la retravailler ou la republier, **Then** il peut récupérer un résultat réutilisable accompagné des données correspondantes.

### Edge Cases

- Une demande vise un type de visualisation autre qu'une heatmap ou un race line chart.
- Une demande mélange plusieurs intentions analytiques ou plusieurs formats dans une seule sortie.
- Une demande ne fournit pas les informations minimales pour cadrer le périmètre d'analyse.
- Les données nécessaires à la visualisation existent mais sont partielles, contradictoires ou non comparables.
- Une line chart race demandée couvre trop de pilotes ou d'équipes, ou une séquence de Grands Prix insuffisamment cadrée, pour rester lisible.
- Une heatmap est demandée sur une mesure qui ne supporte pas une comparaison visuelle pertinente.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le système DOIT accepter une demande simple de visualisation F1 limitée à deux formats pris en charge: heatmap et race line chart.
- **FR-002**: Le système DOIT exiger les informations minimales nécessaires pour cadrer la demande, notamment le format demandé, le périmètre d'analyse et la mesure ou lecture recherchée.
- **FR-003**: Le système DOIT rejeter explicitement toute demande hors périmètre du MVP ou ambiguë au point de ne pas pouvoir produire une sortie fiable.
- **FR-004**: Le système DOIT récupérer les données F1 nécessaires à la demande retenue et conserver une référence claire à leur provenance.
- **FR-005**: Le système DOIT vérifier avant production que les données sont suffisamment complètes, cohérentes et adaptées au format demandé.
- **FR-006**: Le système DOIT signaler explicitement les hypothèses, limitations ou absences de données qui affectent l'interprétation du résultat.
- **FR-007**: Le système DOIT produire, pour une demande de heatmap valide, une sortie exploitable présentant clairement les axes de comparaison, l'intensité visuelle et le sujet analysé.
- **FR-008**: Le système DOIT produire, pour une demande valide de line chart race, une sortie exploitable présentant clairement la progression des pilotes ou des équipes au fil des Grands Prix et les séries affichées.
- **FR-009**: Chaque visualisation produite DOIT être accompagnée d'un contexte de lecture comprenant au minimum le périmètre analysé, la source des données, les hypothèses retenues et les limites connues.
- **FR-010**: Le système DOIT rendre disponible le matériau de base utilisé pour la visualisation afin que le créateur puisse vérifier et réutiliser le résultat.
- **FR-011**: Le système DOIT privilégier la clarté de lecture à l'effet visuel lorsque ces deux objectifs entrent en tension.
- **FR-012**: Le système DOIT conserver un cadrage strictement limité à une seule visualisation exploitable par demande.

### Key Entities *(include if feature involves data)*

- **Demande de visualisation**: Expression simple du besoin utilisateur, incluant le format demandé, le périmètre d'analyse et la lecture recherchée.
- **Jeu de données F1**: Ensemble des données retenues pour répondre à une demande, avec sa couverture, sa provenance et son niveau de complétude.
- **Sortie de visualisation**: Résultat exploitable produit par le MVP sous forme de heatmap ou de race line chart, accompagné de son contexte de lecture.
- **Note de vérification**: Informations explicites qui documentent les hypothèses, les limites, les exclusions et les points de vigilance associés à la sortie.

## Scope Boundaries *(mandatory)*

### In Scope

- Production d'une heatmap F1 à partir d'une demande simple et cadrée.
- Production d'un race line chart F1 à partir d'une demande simple et cadrée.
- Récupération des données nécessaires à ces deux formats dans la limite du périmètre analysé.
- Vérification minimale de cohérence et d'adéquation des données avant production.
- Restitution d'un résultat compréhensible, vérifiable et réutilisable pour un usage éditorial ou exploratoire.
- Documentation explicite des hypothèses et limites lorsqu'elles affectent la lecture.

### Out of Scope

- Tout autre type de visualisation au-delà de la heatmap et du race line chart.
- Tout système multi-utilisateur ou gestion complexe de profils.
- Toute plateforme complète de publication, de diffusion ou de galerie.
- Tout moteur conversationnel avancé.
- Toute couverture exhaustive de tous les types de données F1.
- Toute logique probabiliste, prédictive ou de recommandation.
- Toute optimisation avancée de performance.
- Toute extension à d'autres sports.

### Deferred / Needs Validation

- Extension future à d'autres formats de datavisualisation F1 une fois le socle fiabilité et réutilisabilité validé.
- Formalisation d'une bibliothèque éditoriale réutilisable de visualisations une fois les premiers usages confirmés.
- Élargissement progressif des jeux de données pris en charge après validation des besoins réels du créateur.
- Définition d'un mode de publication ou de diffusion plus structuré une fois la valeur du MVP démontrée.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Sur un lot de 10 demandes représentatives et dans le périmètre du MVP, au moins 8 aboutissent à une visualisation exploitable sans redéfinir le besoin initial.
- **SC-002**: 100% des visualisations produites incluent la source des données, la couverture analysée, les hypothèses retenues et les limites connues.
- **SC-003**: 100% des demandes hors périmètre, ambiguës ou non vérifiables sont refusées avec un motif explicite.
- **SC-004**: Sur un lot de 10 visualisations générées dans le périmètre, au moins 9 permettent au créateur d'identifier en première relecture le message principal, la provenance des données et les principales limites sans investigation supplémentaire.

## Assumptions & Open Questions

- Le premier utilisateur est le créateur du projet et travaille seul dans une logique d'exploration, de production éditoriale et de prototypage.
- Le MVP vise d'abord des sorties réutilisables et vérifiables, pas une expérience produit complète pour des utilisateurs externes.
- Une demande simple de visualisation peut être formulée avec assez de précision pour décrire un seul besoin analytique à la fois.
- Les données F1 nécessaires aux premières heatmaps et aux premiers race line charts sont accessibles dans un niveau de qualité compatible avec l'objectif de fiabilité.
- La notion de "sortie exploitable" est comprise ici comme un résultat directement mobilisable pour analyse, explication ou retravail éditorial, avec accès aux données utilisées.
- Question ouverte: quel sous-ensemble exact de sujets F1 sera priorisé en premier à l'intérieur des deux formats pris en charge.
- Question ouverte: quel niveau minimal de standardisation éditoriale sera attendu pour considérer une visualisation comme réutilisable sans reprise supplémentaire.
