# Phase 0 Research: BEAUTIVIZF1 MVP initial de datavisualisation F1

## Decision 1: Conserver un moteur métier local en Python

- **Decision**: le moteur métier sera un package Python local avec un point d'entrée CLI, et non un notebook, un service web ou un outil de publication.
- **Rationale**: cette forme couvre le besoin réel du MVP, garde le flux lisible et testable, et évite d'introduire une plateforme hors périmètre.
- **Alternatives considered**:
  - Notebook unique: trop peu structuré pour séparer récupération, validation, bundle et rendu.
  - Application web: surdimensionnée pour un usage solo et pour ce périmètre.
  - Pipeline entièrement manuel: insuffisant pour la répétabilité et la vérification.

## Decision 2: Encapsuler la récupération des données F1 derrière un provider dédié

- **Decision**: la récupération des données passera par un module `fastf1_provider` derrière une interface interne unique.
- **Rationale**: ce choix garde la dépendance documentaire et technique isolée, facilite la validation des données récupérées et laisse ouverte une substitution future de source sans réécrire le reste du pipeline.
- **Alternatives considered**:
  - Appels directs à la source depuis les transformations: trop couplé et difficile à tester.
  - Import manuel de CSV ad hoc: possible ponctuellement, mais trop fragile comme socle MVP.

## Decision 3: Utiliser une validation en couches avant toute génération visuelle

- **Decision**: la validation sera découpée en trois niveaux: validité de la demande, complétude/cohérence des données, préconditions de rendu.
- **Rationale**: ce découpage permet de refuser tôt les demandes ambiguës, d'expliciter les limites et de protéger la sortie contre des visualisations trompeuses.
- **Alternatives considered**:
  - Validation uniquement en fin de pipeline: trop tardive et peu explicable.
  - Validation uniquement manuelle: insuffisante pour un usage reproductible.

## Decision 4: Standardiser un bundle de sortie exploitable

- **Decision**: chaque exécution réussie produira un bundle minimal contenant une visualisation exportée, le jeu de données utilisé, un manifeste, des notes de vérification et un artefact explicite d'intégration web de type embed.
- **Rationale**: cela répond directement aux exigences de réutilisabilité, de vérifiabilité, de traçabilité et d'intégration web du projet sans introduire de plateforme de publication.
- **Alternatives considered**:
  - Image seule: trop pauvre pour la vérification.
  - Données seules: ne répond pas au besoin de rendu narratif.
  - Persistance en base de données: inutilement complexe pour le MVP.

## Decision 5: Retenir D3.js comme renderer cible pour les deux formats

- **Decision**: D3.js est retenu comme renderer cible pour la heatmap et la line chart race, piloté par le pipeline Python local.
- **Rationale**: ce choix aligne le rendu avec l'intention initiale du projet, reste adapté à une sortie web réutilisable et permet un contrat d'embed explicite sans introduire de plateforme frontend complète.
- **Alternatives considered**:
  - altair: utile pour du prototypage, mais moins aligné avec la cible D3.js du projet.
  - matplotlib: robuste mais moins naturelle pour la réutilisation web et l'embed.
  - Combinaison de plusieurs bibliothèques: contraire à la simplicité recherchée.

## Decision 6: Encadrer explicitement le rôle de NotebookLM/MCP

- **Decision**: NotebookLM/MCP est retenu comme couche documentaire et de recherche uniquement, pour consulter la documentation FastF1, explorer les champs utiles et rassembler des références ou specs visuelles.
- **Rationale**: cela accélère la compréhension du domaine et la préparation du travail sans faire dépendre le moteur métier, les données chiffrées ou le rendu d'un outil externe.
- **Alternatives considered**:
  - Utiliser NotebookLM/MCP comme source métier ou de données: rejeté car contraire à la fiabilité et à la traçabilité attendues.
  - Ne pas utiliser NotebookLM/MCP du tout: possible, mais moins efficace pour la recherche documentaire.

## Decision 7: Laisser différés les standards éditoriaux avancés

- **Decision**: le MVP ne fixe pas encore de charte éditoriale complète, de galerie de visualisations ou de publication automatisée.
- **Rationale**: ces sujets sont utiles mais non bloquants pour valider les deux formats et la fiabilité du pipeline.
- **Alternatives considered**:
  - Définir immédiatement une chaîne éditoriale complète: hors périmètre.
  - Reporter aussi le bundle minimal: incompatible avec les objectifs de vérification et de réutilisation.
