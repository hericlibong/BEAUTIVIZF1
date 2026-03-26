# Phase 0 Research: Chatbot simple de datavisualisation F1

## Decision 1: Conserver une entrée conversationnelle simple

- **Decision**: le produit démarre par une couche conversationnelle simple où l'utilisateur exprime un besoin analytique ou éditorial en langage naturel.
- **Rationale**: c'est désormais l'entrée produit validée par la spec. Le chatbot doit simplifier l'accès à la datavisualisation au lieu de demander un format technique dès le départ.
- **Alternatives considered**:
  - Entrée directe par type de graphique: rejetée car contraire au flux produit validé.
  - Agent conversationnel complexe multi-étapes: rejeté car hors périmètre du MVP.

## Decision 2: Séparer interprétation et choix du format

- **Decision**: l'application interprète d'abord le besoin utilisateur, puis présente les deux formats disponibles du MVP avant toute génération.
- **Rationale**: cette séparation supprime l'ambiguïté produit et garantit qu'aucune visualisation n'est produite avant un choix explicite de l'utilisateur.
- **Alternatives considered**:
  - Choix automatique du format par le système: rejeté car trop opaque et non conforme à la spec.
  - Demande immédiate d'un type de graphique: rejetée car elle recentre le produit sur un moteur interne au lieu d'un chatbot simple.

## Decision 3: Exiger un choix explicite avant le pipeline de données

- **Decision**: aucune récupération de données ou génération de visualisation ne démarre avant le choix explicite d'une heatmap ou d'une line chart race.
- **Rationale**: ce verrou protège la lisibilité du flux, rend le comportement du chatbot prévisible et évite des générations fondées sur une hypothèse non confirmée.
- **Alternatives considered**:
  - Générer une proposition par défaut: rejeté car contraire au cadrage produit.
  - Lancer plusieurs rendus en parallèle: rejeté car hors périmètre et inutilement complexe.

## Decision 4: Garder Python comme cœur du pipeline F1

- **Decision**: Python reste le cœur de la récupération, de la validation et de la transformation des données F1 après le choix du format.
- **Rationale**: cette structure reste simple, lisible et cohérente avec le besoin du MVP.
- **Alternatives considered**:
  - Déplacer la logique dans une couche frontend: rejeté car cela brouille la séparation des responsabilités.
  - Pipeline majoritairement manuel: rejeté car peu testable et peu réutilisable.

## Decision 5: Conserver D3.js comme renderer cible

- **Decision**: D3.js reste le renderer cible pour les deux formats pris en charge.
- **Rationale**: il permet une sortie web exploitable et un embed explicite sans exiger une plateforme complète de publication.
- **Alternatives considered**:
  - Altair ou matplotlib comme renderer principal: rejetés car moins alignés avec la cible web embeddable retenue.
  - Plusieurs renderers: rejeté car contraire à la simplicité du MVP.

## Decision 6: Verrouiller un bundle minimal embeddable et vérifiable

- **Decision**: chaque génération valide doit retourner une visualisation web, un embed explicite et un bundle minimal de vérification.
- **Rationale**: cela correspond directement à la promesse produit de réutilisabilité, d'intégration et de traçabilité.
- **Alternatives considered**:
  - Visualisation seule: trop pauvre pour l'usage éditorial.
  - Données seules: insuffisant pour répondre au besoin utilisateur.

## Decision 7: Limiter NotebookLM/MCP à un rôle documentaire

- **Decision**: NotebookLM/MCP reste une couche documentaire et contextuelle pour la documentation FastF1, les champs utiles et les références visuelles.
- **Rationale**: ce rôle accélère la compréhension sans devenir moteur métier, source principale des données chiffrées ni dépendance critique du pipeline.
- **Alternatives considered**:
  - Utiliser NotebookLM/MCP pour piloter la génération: rejeté car contraire aux contraintes du MVP.
  - Supprimer totalement cette couche: possible, mais moins utile pour la recherche documentaire.
