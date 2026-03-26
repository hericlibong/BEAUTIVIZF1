# Feature Specification: Chatbot simple de datavisualisation F1

**Feature Branch**: `001-f1-viz-mvp`  
**Created**: 2026-03-26  
**Status**: Draft  
**Input**: User description: "Réécrire la feature 001-f1-viz-mvp pour cadrer BEAUTIVIZF1 comme un chatbot simple orienté datavisualisation F1, recevant une demande en langage naturel, limité à une heatmap et une line chart race, avec sortie D3.js, embed explicite et bundle minimal de vérification."

BEAUTIVIZF1 répond à un problème produit précis: un utilisateur veut exprimer simplement un besoin analytique ou éditorial autour de la Formule 1 sans devoir connaître à l'avance la structure des données, le type de graphique exact à produire ni les étapes techniques nécessaires pour obtenir un résultat utile. Le MVP doit donc commencer par une demande conversationnelle en langage naturel, interpréter ce besoin, indiquer clairement que cette première version ne sait produire que deux formats, laisser l'utilisateur choisir l'un d'eux, puis restituer un résultat embeddable et vérifiable dans ce périmètre strict.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Exprimer un besoin de visualisation en langage naturel (Priority: P1)

En tant qu'utilisateur de BEAUTIVIZF1, je veux décrire en langage naturel le besoin analytique ou éditorial que j'ai autour d'un sujet F1 afin que le chatbot comprenne ce que je cherche à montrer sans que j'aie à nommer moi-même un type de graphique.

**Why this priority**: Cette story place au centre la vraie entrée produit du MVP: l'utilisateur ne commence pas par choisir un format, il commence par exprimer un besoin. Sans cette compréhension initiale, le chatbot ne répond pas à sa promesse de simplification.

**Independent Test**: Cette story peut être testée indépendamment en soumettant une demande analytique en langage naturel dans le périmètre du MVP et en vérifiant que le système en extrait une intention exploitable ou demande une précision simple si le besoin reste trop flou.

**Acceptance Scenarios**:

1. **Given** un utilisateur formule en langage naturel un besoin analytique ou éditorial lié à des données F1, **When** le chatbot analyse sa demande, **Then** il identifie l'intention générale, le sujet à comparer ou suivre, et le périmètre utile sans exiger d'entrée technique formelle.
2. **Given** un utilisateur formule une demande en langage naturel trop ambiguë ou incomplète pour être interprétée de façon fiable, **When** le chatbot l'analyse, **Then** il demande une précision courte et ciblée avant de proposer une suite.

---

### User Story 2 - Être guidé vers l’un des deux formats disponibles du MVP (Priority: P2)

En tant qu'utilisateur de BEAUTIVIZF1, je veux que le chatbot me propose les formats disponibles dans cette première version et me laisse choisir celui qui convient le mieux à mon besoin afin d'obtenir une visualisation adaptée sans devoir connaître à l'avance les contraintes du produit.

**Why this priority**: Cette story traduit le comportement produit réel du MVP. Le chatbot ne doit pas supposer que l'utilisateur choisit immédiatement une heatmap ou une line chart race; il doit expliquer que la V1 ne propose que ces deux options et guider l'utilisateur vers le bon choix.

**Independent Test**: Cette story peut être testée indépendamment en soumettant une demande analytique en langage naturel, puis en vérifiant que le chatbot présente clairement la heatmap et la line chart race comme les deux formats disponibles du MVP, et qu'il attend un choix utilisateur ou une précision avant de générer la visualisation.

**Acceptance Scenarios**:

1. **Given** un utilisateur exprime en langage naturel un besoin analytique compatible avec le MVP, **When** le chatbot interprète sa demande, **Then** il indique que cette première version ne sait produire qu'une heatmap ou une line chart race, explique brièvement ces deux options dans le contexte du besoin exprimé, puis invite l'utilisateur à choisir l'un des deux formats.
2. **Given** un utilisateur choisit l'un des deux formats proposés après cette étape de guidage, **When** le chatbot confirme ce choix et dispose des données nécessaires, **Then** il génère la visualisation correspondante, la sortie embed explicite et le bundle minimal de vérification; si le choix ou les données restent insuffisants, il demande une précision simple ou refuse explicitement la demande.

---

### User Story 3 - Récupérer un résultat embeddable et vérifiable (Priority: P3)

En tant qu'utilisateur de BEAUTIVIZF1, je veux récupérer un résultat embeddable et vérifiable après avoir exprimé mon besoin et choisi l'un des formats disponibles afin de pouvoir le réutiliser dans un contexte éditorial, analytique ou de storytelling sans perdre la trace des données et des limites.

**Why this priority**: La valeur du MVP ne vient pas seulement de la compréhension de la demande ou du choix du format, mais du fait que le résultat final peut être relu, repris, intégré et défendu. Sans sortie embed explicite ni bundle de vérification, le chatbot ne fournirait qu'une réponse visuelle partielle.

**Independent Test**: Cette story peut être testée indépendamment en suivant le flux complet demande analytique -> proposition des formats disponibles -> choix utilisateur -> génération, puis en vérifiant que le résultat final contient une visualisation web, un embed explicite et un bundle minimal de vérification suffisamment clair pour une réutilisation immédiate.

**Acceptance Scenarios**:

1. **Given** un utilisateur a exprimé un besoin, reçu les deux formats disponibles du MVP et choisi l'un d'eux, **When** le système génère le résultat, **Then** l'utilisateur peut identifier ce qui a été demandé, quel format a été choisi, quelles données ont été utilisées, d'où elles proviennent, quelles hypothèses s'appliquent et quelles limites doivent être gardées en tête.
2. **Given** une visualisation valide a été générée à l'issue de ce flux, **When** l'utilisateur veut l'intégrer ou la réutiliser, **Then** il dispose d'une sortie embed explicite et d'un bundle minimal lui évitant de reconstruire manuellement la visualisation ou son contexte.

### Edge Cases

- Une demande en langage naturel exprime un besoin analytique pertinent, mais le chatbot ne parvient pas à le rattacher de manière fiable à l'un des deux formats disponibles du MVP.
- Une demande conversationnelle mélange plusieurs visualisations ou plusieurs objectifs analytiques dans un seul message.
- La demande est compréhensible sur le fond mais trop incomplète pour cadrer le périmètre de données nécessaire.
- Les données F1 nécessaires existent partiellement, sont contradictoires ou ne permettent pas une visualisation fiable.
- Après l'interprétation d'un besoin pertinent, l'utilisateur ne choisit pas explicitement entre les deux formats disponibles du MVP.
- Après proposition des deux formats disponibles, le choix utilisateur se porte sur un format qui ne convient pas au besoin interprété ou aux données réellement exploitables.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le système DOIT accepter une demande utilisateur en langage naturel exprimant un besoin analytique ou éditorial autour de la Formule 1.
- **FR-002**: Le système DOIT interpréter cette demande initiale afin d'identifier l'intention générale, le sujet concerné et le périmètre d'analyse utile.
- **FR-003**: Le système DOIT indiquer explicitement que, dans cette première version, il ne sait produire que deux formats de visualisation: heatmap et line chart race.
- **FR-004**: Le système DOIT présenter les deux formats disponibles du MVP dans le contexte de la demande interprétée, exiger que l'utilisateur choisisse explicitement l'un de ces deux formats, et ne DOIT lancer aucune génération avant ce choix explicite.
- **FR-005**: Le système DOIT demander une précision simple lorsque la demande initiale ou le choix utilisateur restent insuffisants pour produire une sortie fiable.
- **FR-006**: Le système DOIT signaler clairement toute demande hors périmètre, ambiguë ou insuffisamment précise pour permettre un résultat fiable.
- **FR-007**: Le système DOIT conserver la règle qu'une demande utilisateur aboutit à une seule visualisation exploitable.
- **FR-008**: Une fois le format choisi et la demande suffisamment cadrée, le système DOIT récupérer les données F1 nécessaires et conserver une provenance explicite de ces données.
- **FR-009**: Le système DOIT vérifier que les données récupérées sont suffisamment cohérentes, complètes et adaptées au format choisi avant de produire un résultat.
- **FR-010**: Le système DOIT produire, pour un choix valide de heatmap, une visualisation web exploitable correspondant au besoin exprimé par l'utilisateur.
- **FR-011**: Le système DOIT produire, pour un choix valide de line chart race, une visualisation web exploitable montrant la progression des pilotes ou des équipes au fil des Grands Prix.
- **FR-012**: Le système DOIT retourner une sortie embed explicite pour toute visualisation valide produite dans le périmètre du MVP.
- **FR-013**: Le système DOIT retourner avec chaque visualisation valide un bundle minimal de vérification comprenant au minimum les données utilisées, leur provenance, les hypothèses retenues et les limites connues.
- **FR-014**: Le système DOIT privilégier la clarté de lecture et la fiabilité du résultat à tout effet visuel secondaire.
- **FR-015**: Toute couche documentaire ou contextuelle, y compris NotebookLM/MCP, DOIT rester distincte du moteur métier et ne DOIT pas être considérée comme source principale des données chiffrées utilisées pour la visualisation.

### Key Entities *(include if feature involves data)*

- **Demande conversationnelle**: Message en langage naturel par lequel l'utilisateur exprime d'abord un besoin analytique ou éditorial autour d'un sujet F1, avant tout choix du format de visualisation.
- **Intention de visualisation**: Interprétation structurée de la demande conversationnelle, indiquant le besoin analytique, le sujet d'analyse et le périmètre nécessaire avant le choix du format.
- **Choix de format**: Sélection par l'utilisateur de l'un des deux formats explicitement proposés dans le MVP après interprétation de la demande.
- **Jeu de données F1**: Ensemble de données récupéré pour répondre à une demande valide, avec sa couverture, sa provenance et son niveau de fiabilité.
- **Résultat embeddable**: Sortie produite pour une demande valide, composée d'une visualisation web et d'un embed explicite.
- **Bundle de vérification**: Ensemble minimal d'informations qui accompagne le résultat pour documenter les données utilisées, la provenance, les hypothèses et les limites.

## Scope Boundaries *(mandatory)*

### In Scope

- Un chatbot simple recevant une demande de visualisation en langage naturel.
- Compréhension d'un besoin utilisateur exprimé en langage naturel, avant la proposition des deux formats du MVP.
- Proposition explicite des deux formats disponibles du MVP: heatmap et line chart race.
- Choix utilisateur de l'un de ces deux formats avant génération.
- Récupération des données F1 nécessaires pour répondre à une demande valide.
- Production d'une visualisation web exploitable pour chacun des deux formats pris en charge.
- Retour d'une sortie embed explicite et d'un bundle minimal de vérification.
- Demande de précision simple ou refus explicite lorsque la demande ne permet pas un résultat fiable.

### Out of Scope

- Tout format de visualisation autre que la heatmap et la line chart race.
- Toute expérience conversationnelle avancée, agentique ou multi-étapes complexe.
- Toute plateforme complète de publication, de galerie ou de diffusion.
- Tout système multi-utilisateur ou gestion avancée de rôles.
- Toute couverture exhaustive de tous les types de données F1.
- Toute logique prédictive, probabiliste ou de recommandation.
- Toute extension à d'autres sports.

### Deferred / Needs Validation

- Enrichissement futur des interactions conversationnelles au-delà d'un chatbot simple.
- Enrichissement futur des bundles, tooltips et métadonnées de présentation au-delà du minimum nécessaire au MVP.
- Ajout futur d'autres formats de visualisation après validation du socle produit.
- Formalisation ultérieure d'une logique de publication ou d'une galerie de résultats une fois la valeur du MVP démontrée.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Sur un lot de 10 demandes en langage naturel relevant du périmètre du MVP, au moins 8 aboutissent à une visualisation exploitable sans reformulation majeure de la demande.
- **SC-002**: 100% des visualisations valides produites incluent une visualisation web, une sortie embed explicite et un bundle minimal de vérification.
- **SC-003**: 100% des demandes hors périmètre, ambiguës ou non vérifiables conduisent à une demande de précision simple ou à un refus explicite.
- **SC-004**: Sur un lot de 10 résultats valides, au moins 9 permettent à l'utilisateur d'identifier sans investigation supplémentaire la visualisation demandée, la provenance des données et les principales limites du résultat.

## Assumptions & Open Questions

- Le premier utilisateur reste le créateur du projet, dans une logique d'exploration, de production éditoriale et de prototypage.
- Le chatbot du MVP peut rester simple tant qu'il comprend une demande en langage naturel, propose clairement les deux formats disponibles, puis sait soit produire un résultat fiable, soit demander une précision courte, soit refuser explicitement.
- Le MVP vise un résultat conversationnel exploitable, embeddable et vérifiable, pas une expérience conversationnelle complète ou sophistiquée.
- Les sources F1 nécessaires aux premières heatmaps et aux premières line chart races sont accessibles dans un niveau de qualité compatible avec le besoin produit.
- La notion de "bundle minimal de vérification" est comprise ici comme l'ensemble minimum requis pour relire et réutiliser le résultat sans perdre la provenance, les hypothèses et les limites.
- Question ouverte: jusqu'où le MVP doit-il tolérer les reformulations utilisateur avant de basculer vers un refus explicite.
- Question ouverte: quel niveau minimal de standardisation visuelle et éditoriale sera considéré comme suffisant pour qu'un résultat soit jugé réellement embeddable dès la première version.
