# Implementation Plan: Chatbot simple de datavisualisation F1

**Branch**: `001-f1-viz-mvp` | **Date**: 2026-03-26 | **Spec**: [/home/hericdev/BEAUTIVIZF1/specs/001-f1-viz-mvp/spec.md](/home/hericdev/BEAUTIVIZF1/specs/001-f1-viz-mvp/spec.md)
**Input**: Feature specification from `/specs/001-f1-viz-mvp/spec.md`

## Summary

Le MVP de BEAUTIVIZF1 est un chatbot simple de datavisualisation F1. Le flux validé est désormais: l'utilisateur exprime un besoin analytique ou éditorial en langage naturel, le chatbot interprète ce besoin, rappelle que la V1 ne sait produire qu'une heatmap ou une line chart race, attend un choix explicite de l'utilisateur, puis seulement lance le pipeline de données F1 et la génération du résultat. L'architecture retenue reste volontairement simple, avec une séparation claire entre interface conversationnelle, interprétation, données, rendu D3.js et sortie. Le résultat attendu comprend une visualisation web, une sortie embed explicite et un bundle minimal de vérification. NotebookLM/MCP reste une couche documentaire et contextuelle uniquement.

## Technical Context

**Language/Version**: Python 3.11  
**Primary Python Dependencies**: fastf1, pandas  
**Rendering Dependency**: d3.js  
**Storage**: fichiers locaux pour les artefacts de sortie, les exports de vérification et le cache de données hors logique métier  
**Testing**: pytest pour les validations reproductibles, complété par des vérifications manuelles du flux conversationnel, du rendu et du bundle  
**Target Platform**: application locale simple avec interface conversationnelle légère et sorties web embeddables  
**Project Type**: application Python avec couche conversationnelle simple, pipeline de données local et rendu web exportable  
**Performance Goals**: interpréter une demande et proposer les deux formats du MVP ou une clarification simple en moins de 5 secondes; produire un bundle complet en moins de 30 secondes quand les données requises sont déjà disponibles localement  
**Constraints**: une demande correspond à une seule visualisation; aucun rendu avant choix explicite du format; deux formats uniquement; pas de plateforme complète de publication; NotebookLM/MCP jamais moteur métier ni source principale des données chiffrées  
**Scale/Scope**: un seul utilisateur, conversation courte et guidée, une analyse à la fois, périmètre limité à la heatmap et à la line chart race

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Research Gate

- [x] Reliability first: la provenance, le bundle de vérification et le refus explicite des demandes insuffisantes sont prévus dès l'entrée conversationnelle
- [x] Simplicity: le MVP reste un chatbot simple sans agent complexe, sans plateforme de publication et sans formats additionnels
- [x] Progressive validation: le flux conversation -> interprétation -> choix -> génération prévoit des points de contrôle clairs avant la production
- [x] Scope discipline: seuls les deux formats validés et le bundle minimal embeddable entrent dans le périmètre actif
- [x] Explicit decisions: les arbitrages sur le choix explicite du format, le rôle de D3.js et le statut non critique de NotebookLM/MCP sont consignés
- [x] Testability: le plan prévoit des vérifications sur l'interprétation, le choix du format, le bundle et l'embed
- [x] Documentation: `research.md`, `data-model.md`, `contracts/`, `quickstart.md` et `AGENTS.md` sont identifiés avant implémentation

### Post-Design Re-check

- [x] Reliability first: la séparation conversation -> interprétation -> données -> rendu -> sortie renforce la traçabilité et les refus explicites
- [x] Simplicity: l'architecture ne rajoute ni agent multi-étapes ni plateforme web complète
- [x] Progressive validation: les contrats et le quickstart couvrent le choix explicite du format avant génération
- [x] Scope discipline: aucun format ou enrichissement hors MVP n'entre dans les artefacts régénérés
- [x] Explicit decisions: les décisions techniques importantes sont réécrites dans `research.md`
- [x] Testability: le modèle de données, les contrats et le quickstart rendent le nouveau flux testable de bout en bout
- [x] Documentation: tous les artefacts de planification nécessaires ont été réalignés sur la spec actuelle

## Decision Log

| Decision | Status | Rationale |
|----------|--------|-----------|
| Conserver un chatbot simple comme point d'entrée produit | Accepted | Reflète la spec validée sans dériver vers une expérience conversationnelle complexe |
| Séparer l'interprétation du besoin utilisateur du choix de format | Accepted | Le produit ne doit pas supposer le format à la place de l'utilisateur |
| Exiger un choix explicite entre heatmap et line chart race avant toute génération | Accepted | Verrouille le flux MVP et supprime l'ambiguïté produit précédente |
| Conserver Python comme cœur du pipeline de données F1 | Accepted | Garde une architecture lisible et adaptée à la récupération, la validation et la transformation des données |
| Utiliser D3.js comme renderer cible | Accepted | Maintient une sortie web exploitable et une intégration embed explicite sans plateforme complète |
| Produire un bundle minimal de vérification avec sortie embed | Accepted | Assure la réutilisabilité et la traçabilité attendues par le produit |
| Limiter NotebookLM/MCP à une couche documentaire et contextuelle | Accepted | Préserve la compréhension documentaire sans déplacer la logique métier ni la donnée chiffrée hors du projet |
| Reporter l'enrichissement avancé de la conversation, des tooltips et des métadonnées de présentation | Deferred | Utile plus tard, mais hors périmètre du MVP validé |

## Project Structure

### Documentation (this feature)

```text
specs/001-f1-viz-mvp/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── conversation-request.md
│   └── output-bundle.md
└── tasks.md
```

### Source Code (repository root)

```text
src/
└── beautivizf1/
    ├── interpretation/
    │   └── intent_parser.py
    ├── domain/
    │   ├── conversation_request.py
    │   ├── visualization_intent.py
    │   ├── format_selection.py
    │   ├── source_dataset.py
    │   ├── validated_visualization_dataset.py
    │   └── artifact_bundle.py
    ├── data_sources/
    │   └── f1_provider.py
    ├── validation/
    │   ├── request_rules.py
    │   └── data_rules.py
    ├── transforms/
    │   ├── heatmap_transform.py
    │   └── line_chart_race_transform.py
    ├── renderers/
    │   └── d3_renderer.py
    ├── outputs/
    │   ├── bundle_writer.py
    │   └── notes_writer.py
    ├── chat.py
    └── services/
        └── visualization_service.py

tests/
├── contract/
├── integration/
├── unit/
└── fixtures/

artifacts/
└── .gitkeep
```

**Structure Decision**: le projet reste un monoprojet Python. La couche conversationnelle est volontairement légère pour la V1: `chat.py` suffit pour recevoir la demande, présenter les deux formats disponibles, recueillir le choix explicite et transmettre une demande cadrée au pipeline. `interpretation/` traduit le besoin exprimé en intention exploitable. `data_sources/`, `validation/` et `transforms/` prennent en charge le pipeline F1 après le choix explicite du format. `renderers/` produit la visualisation D3.js. `outputs/` assemble l'embed explicite et le bundle minimal. `services/visualization_service.py` orchestre la génération sans multiplier les orchestrateurs ni transformer le chatbot simple en mini-architecture trop riche.

## Complexity Tracking

Aucune dérogation à la constitution n'est requise. La complexité volontairement exclue du MVP reste différée: conversation avancée, autres formats, publication complète, enrichissements avancés de présentation.
