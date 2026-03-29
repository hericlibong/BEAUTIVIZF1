# Tasks: Chatbot simple de datavisualisation F1

**Input**: Design documents from `/specs/001-f1-viz-mvp/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Validation**: Chaque user story inclut des tâches de vérification explicites. Les tests couvrent l’interprétation, le choix explicite du format, le pipeline de données, le rendu D3.js, l’embed et le bundle minimal de vérification. Les vérifications manuelles restent explicites pour la lisibilité du rendu et la qualité du flux conversationnel.

**Organization**: Les tâches sont groupées par phase puis par user story afin de garder un ordre exécutable, des dépendances claires et des incréments testables.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Peut être exécuté en parallèle
- **[Story]**: User story concernée (`US1`, `US2`, `US3`)
- Les tâches respectent le périmètre strict du MVP
- Les enrichissements avancés de `tooltip_fields` et `presentation_fields` restent explicitement différés

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Poser la structure du projet et l’outillage minimal.

### Block 1: Structure du projet et outillage minimal

- [X] T001 Create project package markers in `src/beautivizf1/__init__.py`, `tests/__init__.py`, and `artifacts/.gitkeep`
- [X] T002 Initialize project metadata and dependencies in `pyproject.toml`
- [X] T003 Configure pytest and shared test bootstrapping in `pyproject.toml` and `tests/conftest.py`
- [X] T004 [P] Create minimal documentation scaffolding in `docs/usage/README.md` and `docs/validation/README.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Mettre en place le socle commun avant toute user story.

**⚠️ CRITICAL**: Aucune user story ne commence avant la fin de cette phase.

### Shared domain and validation core

- [X] T005 Create the conversation request and visualization intent domain models in `src/beautivizf1/domain/conversation_request.py` and `src/beautivizf1/domain/visualization_intent.py`
- [X] T006 [P] Create the format selection and artifact bundle domain models in `src/beautivizf1/domain/format_selection.py` and `src/beautivizf1/domain/artifact_bundle.py`
- [X] T007 [P] Create the source and validated dataset domain models in `src/beautivizf1/domain/source_dataset.py` and `src/beautivizf1/domain/validated_visualization_dataset.py`
- [X] T008 Implement the generic F1 provider interface in `src/beautivizf1/data_sources/f1_provider.py`
- [X] T009 Implement shared request validation rules in `src/beautivizf1/validation/request_rules.py`
- [X] T010 [P] Implement shared data validation and provenance rules in `src/beautivizf1/validation/data_rules.py`
- [X] T011 [P] Create bundle and notes writer skeletons in `src/beautivizf1/outputs/bundle_writer.py` and `src/beautivizf1/outputs/notes_writer.py`
- [X] T012 Implement the main generation orchestrator skeleton in `src/beautivizf1/services/visualization_service.py`

### Foundational verification

- [X] T013 [P] Add contract tests for conversation request and format selection in `tests/contract/test_conversation_request_contract.py`
- [X] T014 [P] Add contract tests for the output bundle in `tests/contract/test_output_bundle_contract.py`
- [X] T015 [P] Add unit tests for shared request and data rules in `tests/unit/test_request_rules.py` and `tests/unit/test_data_rules.py`
- [X] T016 [P] Add shared fixtures for conversation requests and format selections in `tests/fixtures/requests/natural_language_need.json` and `tests/fixtures/selections/explicit_choice.json`

**Checkpoint**: Le socle commun est prêt. Les user stories peuvent maintenant commencer.

---

## Phase 3: User Story 1 - Exprimer un besoin de visualisation en langage naturel (Priority: P1) 🎯 MVP

**Goal**: Permettre à l’utilisateur d’exprimer un besoin analytique en langage naturel et obtenir une interprétation exploitable ou une clarification simple.

**Independent Test**: Soumettre une demande analytique en langage naturel et vérifier que le système en extrait une intention exploitable ou demande une précision courte sans parler encore de génération.

### Block 2: Entrée conversationnelle légère (`chat.py`)

- [X] T017 [US1] Implement the lightweight chat entry flow in `src/beautivizf1/chat.py`

### Block 3: Interprétation de la demande utilisateur

- [X] T018 [US1] Implement intent parsing for analytic and editorial needs in `src/beautivizf1/interpretation/intent_parser.py`
- [X] T019 [US1] Connect chat intake to interpretation and clarification outcomes in `src/beautivizf1/chat.py` and `src/beautivizf1/services/visualization_service.py`

### Block 13: Tests et validations MVP

- [X] T020 [P] [US1] Add unit tests for intent parsing and clarification outcomes in `tests/unit/test_intent_parser.py`
- [X] T021 [P] [US1] Add an integration test for natural-language intake and interpretation in `tests/integration/test_chat_interpretation_flow.py`
- [X] T022 [US1] Document manual validation for natural-language interpretation in `docs/validation/chat_interpretation.md`

### Block 14: Documentation minimale utile

- [X] T023 [US1] Add usage documentation for expressing a need in `docs/usage/chat_input.md`

**Checkpoint**: Le chatbot comprend un besoin ou demande une clarification simple, sans encore lancer de génération.

---

## Phase 4: User Story 2 - Être guidé vers l’un des deux formats disponibles du MVP (Priority: P2)

**Goal**: Présenter explicitement la heatmap et la line chart race comme seules options du MVP, puis recueillir un choix explicite avant toute génération.

**Independent Test**: Soumettre un besoin interprété, vérifier que le chatbot présente les deux formats disponibles, exige un choix explicite et ne déclenche aucun rendu avant ce choix.

### Block 4: Présentation des deux formats disponibles

- [X] T024 [US2] Implement the format proposal step in `src/beautivizf1/chat.py`

### Block 5: Recueil du choix explicite utilisateur

- [X] T025 [US2] Implement explicit format choice handling in `src/beautivizf1/chat.py`
- [X] T026 [US2] Enforce the no-generation-before-choice rule in `src/beautivizf1/validation/request_rules.py` and `src/beautivizf1/services/visualization_service.py`

### Block 13: Tests et validations MVP

- [X] T027 [P] [US2] Add unit tests for format proposal and choice gating in `tests/unit/test_format_selection_flow.py`
- [ ] T028 [P] [US2] Add an integration test for interpretation-to-choice flow in `tests/integration/test_format_selection_flow.py`
- [ ] T029 [US2] Document manual validation for explicit format choice in `docs/validation/format_selection.md`

### Block 14: Documentation minimale utile

- [ ] T030 [US2] Add usage documentation for choosing between heatmap and line chart race in `docs/usage/format_selection.md`

**Checkpoint**: Le système suit correctement le flux besoin -> interprétation -> proposition des formats -> choix explicite, sans génération prématurée.

---

## Phase 5: User Story 3 - Récupérer un résultat embeddable et vérifiable (Priority: P3)

**Goal**: Après un choix explicite, produire une visualisation D3.js, un embed explicite et un bundle minimal de vérification pour la heatmap et la line chart race.

**Independent Test**: Suivre le flux complet jusqu’à la génération et vérifier, pour chaque format du MVP, la visualisation web, l’embed explicite, le bundle minimal, la provenance et les limites.

### Block 6: Récupération des données F1

- [ ] T031 [US3] Implement source retrieval after explicit format choice in `src/beautivizf1/data_sources/f1_provider.py` and `src/beautivizf1/services/visualization_service.py`

### Block 7: Validation des demandes et des données

- [ ] T032 [US3] Implement validated dataset assembly and provenance checks in `src/beautivizf1/validation/data_rules.py` and `src/beautivizf1/services/visualization_service.py`

### Block 8: Transformations heatmap

- [ ] T033 [P] [US3] Implement the heatmap transformation in `src/beautivizf1/transforms/heatmap_transform.py`

### Block 9: Transformations line chart race

- [ ] T034 [P] [US3] Implement the line chart race transformation in `src/beautivizf1/transforms/line_chart_race_transform.py`

### Block 10: Rendu D3.js

- [ ] T035 [US3] Implement D3 rendering for both supported formats in `src/beautivizf1/renderers/d3_renderer.py`

### Block 11: Sortie embed

- [ ] T036 [US3] Implement explicit embed export for both supported formats in `src/beautivizf1/renderers/d3_renderer.py` and `src/beautivizf1/outputs/bundle_writer.py`

### Block 12: Bundle minimal de vérification

- [ ] T037 [US3] Implement manifest, dataset export, provenance, and verification note outputs in `src/beautivizf1/outputs/bundle_writer.py` and `src/beautivizf1/outputs/notes_writer.py`
- [ ] T038 [US3] Finalize end-to-end generation flow and bundle assembly in `src/beautivizf1/services/visualization_service.py` and `src/beautivizf1/chat.py`

### Block 13: Tests et validations MVP

- [ ] T039 [P] [US3] Add unit tests for heatmap and line chart race transformations in `tests/unit/test_heatmap_transform.py` and `tests/unit/test_line_chart_race_transform.py`
- [ ] T040 [P] [US3] Add an integration test for the heatmap generation flow in `tests/integration/test_heatmap_generation_flow.py`
- [ ] T041 [P] [US3] Add an integration test for the line chart race generation flow in `tests/integration/test_line_chart_race_generation_flow.py`
- [ ] T042 [P] [US3] Add an integration test for bundle and embed outputs in `tests/integration/test_bundle_and_embed_flow.py`
- [ ] T043 [US3] Document manual validation for generated outputs in `docs/validation/generated_outputs.md`

### Block 14: Documentation minimale utile

- [ ] T044 [US3] Add usage documentation for output bundle and embed reuse in `docs/usage/output_bundle.md`

**Checkpoint**: Le flux complet du MVP fonctionne pour les deux formats pris en charge avec visualisation web, embed explicite et bundle minimal de vérification.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Finaliser la validation transversale et la documentation minimale du MVP.

- [ ] T045 [P] Capture fixture usage guidance in `tests/fixtures/README.md`
- [ ] T046 Run quickstart validation and record MVP checks in `docs/validation/mvp_checklist.md`
- [ ] T047 Update root usage and deferred-items summary in `README.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1: Setup**: démarre immédiatement.
- **Phase 2: Foundational**: dépend de la phase 1 et bloque toutes les user stories.
- **Phase 3: US1**: dépend de la phase 2.
- **Phase 4: US2**: dépend de la phase 3, car la proposition de formats suppose une intention déjà interprétée.
- **Phase 5: US3**: dépend de la phase 4, car aucun pipeline de données ni rendu ne doit démarrer avant le choix explicite du format.
- **Phase 6: Polish**: dépend des user stories visées pour la livraison.

### Major Block Dependencies

- **Block 1 → Shared domain and validation core**: la structure projet et l’outillage minimal précèdent toute implémentation.
- **Blocks 2 and 3 → Blocks 4 and 5**: le point d’entrée conversationnel léger et l’interprétation doivent exister avant la proposition des formats et le choix utilisateur.
- **Blocks 4 and 5 → Blocks 6 to 12**: le pipeline F1, le rendu D3.js, l’embed et le bundle ne commencent qu’après le choix explicite du format.
- **Block 6 → Block 7**: la récupération des données précède leur validation.
- **Block 7 → Blocks 8 and 9**: les transformations ne commencent qu’avec des données validées.
- **Blocks 8 and 9 → Block 10**: le rendu D3.js dépend des transformations du format choisi.
- **Block 10 → Block 11 → Block 12**: le rendu précède l’embed, qui précède le bundle final.
- **Block 13**: les tests et validations ferment chaque phase fonctionnelle.
- **Block 14**: la documentation minimale utile est mise à jour à la fin de chaque user story.

### User Story Dependencies

- **US1 (P1)**: aucune dépendance fonctionnelle sur les autres user stories après la fondation.
- **US2 (P2)**: dépend de US1 pour s’appuyer sur une intention déjà interprétée.
- **US3 (P3)**: dépend de US2 car le choix explicite du format est un prérequis obligatoire à toute génération.

### Within Each User Story

- Définir les validations avant de fermer le flux de la story.
- Connecter les modèles et services avant les intégrations.
- Finaliser la documentation avant de clore la story.

### Parallel Opportunities

- `T004`, `T006`, `T007`, `T010`, `T011`, `T013`, `T014`, `T015`, `T016` peuvent être parallélisés en phases 1 et 2.
- Dans **US1**, `T020` et `T021` peuvent avancer en parallèle après `T018`.
- Dans **US2**, `T027` et `T028` peuvent avancer en parallèle après `T024` et `T025`.
- Dans **US3**, `T033` et `T034` peuvent avancer en parallèle après `T032`; `T040`, `T041` et `T042` peuvent ensuite avancer en parallèle après `T038`.

---

## Parallel Example: User Story 1

```bash
Task: "Add unit tests for intent parsing and clarification outcomes in tests/unit/test_intent_parser.py"
Task: "Add an integration test for natural-language intake and interpretation in tests/integration/test_chat_interpretation_flow.py"
```

---

## Parallel Example: User Story 3

```bash
Task: "Implement the heatmap transformation in src/beautivizf1/transforms/heatmap_transform.py"
Task: "Implement the line chart race transformation in src/beautivizf1/transforms/line_chart_race_transform.py"
Task: "Add an integration test for the heatmap generation flow in tests/integration/test_heatmap_generation_flow.py"
Task: "Add an integration test for the line chart race generation flow in tests/integration/test_line_chart_race_generation_flow.py"
```

---

## Implementation Strategy

### MVP Core

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Complete Phase 4: User Story 2
5. Complete Phase 5: User Story 3
6. Run Phase 6 cross-cutting validation

### Incremental Delivery

1. Setup + Foundational establish the common domain, validation core, provider interface, bundle skeleton, and orchestrator
2. US1 delivers the lightweight conversational entry and interpretation
3. US2 delivers explicit format proposal and explicit user choice
4. US3 delivers the actual generation flow, both supported formats, embed, and verification bundle
5. Phase 6 closes the MVP with final validation and concise documentation

### Deferred (Not in Current Tasks)

- Enrichissement avancé de `tooltip_fields`
- Enrichissement avancé de `presentation_fields`
- Expérience conversationnelle avancée ou agentique
- Formats de visualisation supplémentaires
- Plateforme complète de publication ou galerie

---

## Notes

- Toutes les tâches restent dans le périmètre strict du MVP.
- `NotebookLM/MCP` n’apparaît pas comme moteur métier ni comme dépendance critique d’implémentation.
- Une demande correspond toujours à une seule visualisation exploitable.
