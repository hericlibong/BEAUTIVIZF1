# Implementation Plan: BEAUTIVIZF1 MVP initial de datavisualisation F1

**Branch**: `001-f1-viz-mvp` | **Date**: 2026-03-25 | **Spec**: [/home/hericdev/BEAUTIVIZF1/specs/001-f1-viz-mvp/spec.md](/home/hericdev/BEAUTIVIZF1/specs/001-f1-viz-mvp/spec.md)
**Input**: Feature specification from `/specs/001-f1-viz-mvp/spec.md`

## Summary

Le MVP reste strictement limité à deux sorties: une heatmap et une line chart race montrant la progression des pilotes ou des équipes au fil des Grands Prix. Le plan retient une architecture locale simple en Python, organisée en quatre couches explicites: récupération des données, validation/transformation, bundle de sortie exploitable, puis rendu de visualisation. Le rendu cible du MVP est basé sur D3.js pour produire une visualisation web et une sortie d'intégration web explicite de type embed, sans introduire de plateforme complète. La validation est progressive: validation de la demande, vérification de complétude des données, contrôle du bundle produit, puis revue visuelle ciblée. NotebookLM/MCP reste une couche documentaire et de recherche, utile pour la documentation FastF1, les champs utiles et les références visuelles, mais jamais le moteur métier, jamais la source principale des données chiffrées et jamais une dépendance critique du pipeline de rendu.

## Technical Context

**Language/Version**: Python 3.11  
**Primary Python Dependencies**: fastf1, pandas  
**Rendering Dependency**: d3.js  
**Storage**: fichiers locaux versionnables ou régénérables pour les artefacts, avec cache de données local hors logique métier  
**Testing**: pytest pour les validations reproductibles, complété par une revue manuelle des sorties visuelles  
**Target Platform**: environnement local de production éditoriale sur machine développeur, avec sorties réutilisables sur le web et intégrables par embed  
**Project Type**: package Python avec point d'entrée CLI pour générer une visualisation par demande  
**Performance Goals**: produire un bundle exploitable pour une demande dans le périmètre en moins de 30 secondes quand les données requises sont déjà disponibles localement; refuser une demande invalide en moins de 5 secondes  
**Constraints**: fiabilité avant effet visuel; une seule visualisation par demande; deux formats maximum; refus explicite des demandes ambiguës ou non vérifiables; NotebookLM/MCP limité à la documentation et à la recherche documentaire; aucune dépendance critique du rendu à NotebookLM/MCP  
**Scale/Scope**: un seul utilisateur, une demande à la fois, périmètre de données limité à une course ou à une séquence bornée de Grands Prix, comparaison sur pilotes ou équipes uniquement

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Research Gate

- [x] Reliability first: assumptions, data constraints, and traceability needs are explicit
- [x] Simplicity: the simplest workable approach is selected or extra complexity is justified
- [x] Progressive validation: major hypotheses have a planned checkpoint before broader build-out
- [x] Scope discipline: out-of-scope items and deferred ideas are named explicitly
- [x] Explicit decisions: important trade-offs are recorded with rationale
- [x] Testability: verification approach is defined, manual first if needed, then more reproducible when justified
- [x] Documentation: impacted docs and decision records are identified before implementation

### Post-Design Re-check

- [x] Reliability first: la séparation provider -> validation -> transformation -> bundle -> rendu garde la traçabilité et permet les refus explicites
- [x] Simplicity: une seule application Python locale, sans service web ni base de données, couvre le besoin MVP
- [x] Progressive validation: le quickstart et les contrats prévoient des checkpoints avant tout élargissement de périmètre
- [x] Scope discipline: aucun format, profil utilisateur ou canal de publication hors MVP n'entre dans le design
- [x] Explicit decisions: les arbitrages techniques retenus et différés sont consignés dans `research.md`
- [x] Testability: les contrats, le modèle de données et le quickstart définissent des vérifications manuelles et automatisables
- [x] Documentation: `research.md`, `data-model.md`, `contracts/`, `quickstart.md` et `AGENTS.md` sont identifiés comme artefacts à maintenir

## Decision Log

| Decision | Status | Rationale |
|----------|--------|-----------|
| Utiliser un package Python local avec un point d'entrée CLI | Accepted | Couvre le besoin du créateur sans introduire de plateforme ou service hors MVP |
| Encapsuler la récupération F1 derrière un provider dédié | Accepted | Isole la dépendance aux données et protège la suite du pipeline contre les changements de source |
| Séparer validation, transformation, bundle de sortie et rendu | Accepted | Rend le flux lisible, testable et cohérent avec la constitution |
| Produire un bundle de sortie standardisé (`manifest`, `dataset`, `notes`, `visualisation`, `embed`) | Accepted | Garantit réutilisabilité, vérifiabilité, intégration web et support du storytelling |
| Utiliser D3.js comme renderer cible du MVP | Accepted | Aligne le rendu avec l'intention initiale du projet et garde une sortie web intégrable sans plateforme complète |
| Utiliser NotebookLM/MCP uniquement comme couche documentaire et de recherche | Accepted | Permet d'exploiter la documentation FastF1, les champs utiles et les références visuelles sans déplacer la logique métier ni la source chiffrée hors du projet |
| Garder la sortie web limitée à des artefacts exportés et intégrables, sans plateforme de publication | Accepted | Respecte le MVP et limite les dépendances |
| Standardiser plus tard les gabarits éditoriaux avancés et la publication | Deferred | Important pour la suite, mais non nécessaire pour produire les deux premiers formats du MVP |

## Project Structure

### Documentation (this feature)

```text
specs/001-f1-viz-mvp/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── output-bundle.md
│   └── visualization-request.md
└── tasks.md
```

### Source Code (repository root)

```text
src/
└── beautivizf1/
    ├── cli/
    │   └── generate_visualization.py
    ├── domain/
    │   ├── artifact_bundle.py
    │   ├── source_dataset.py
    │   └── visualization_request.py
    ├── data_sources/
    │   └── fastf1_provider.py
    ├── validation/
    │   ├── data_rules.py
    │   └── request_rules.py
    ├── transforms/
    │   ├── heatmap_transform.py
    │   └── line_chart_race_transform.py
    ├── outputs/
    │   ├── bundle_writer.py
    │   └── notes_writer.py
    ├── renderers/
    │   └── d3_renderer.py
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

**Structure Decision**: structure monoprojet en package Python. `data_sources/` porte uniquement la récupération, `validation/` et `transforms/` portent les contrôles et remises en forme, `outputs/` assemble la sortie exploitable et l'artefact d'embed, `renderers/` génère la visualisation D3.js. `services/` orchestre un flux unique de bout en bout sans introduire de couches supplémentaires.

## Complexity Tracking

Aucune dérogation à la constitution n'est requise à ce stade. Les éléments différés restent hors du périmètre actif du MVP.
