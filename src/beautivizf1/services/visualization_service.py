from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence

from beautivizf1.data_sources.f1_provider import F1Provider
from beautivizf1.domain.conversation_request import ConversationRequest
from beautivizf1.domain.format_selection import FormatSelection
from beautivizf1.domain.source_dataset import SourceDataset
from beautivizf1.domain.visualization_intent import VisualizationIntent
from beautivizf1.domain.validated_visualization_dataset import (
    ValidatedVisualizationDataset,
    ValidationStatus,
)
from beautivizf1.interpretation.intent_parser import (
    InterpretationOutcome,
    parse_intent,
)
from beautivizf1.validation.data_rules import (
    DataValidationResult,
    assemble_validated_visualization_dataset,
    validate_source_dataset,
    validate_validated_visualization_dataset,
)
from beautivizf1.validation.request_rules import (
    RequestValidationResult,
    validate_generation_requirements,
)


@dataclass(slots=True)
class InterpretationFlowResult:
    outcome: InterpretationOutcome
    request: ConversationRequest
    intent: VisualizationIntent | None
    notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class GenerationPreparation:
    selection_validation: RequestValidationResult
    source_dataset: SourceDataset | None = None
    source_validation: DataValidationResult | None = None
    validated_dataset: ValidatedVisualizationDataset | None = None
    validated_validation: DataValidationResult | None = None
    next_step: str = "waiting_for_explicit_choice"


class VisualizationService:
    def __init__(
        self,
        *,
        provider: F1Provider | None = None,
        output_dir: Path | None = None,
        core_schema_version: str = "1.0",
    ) -> None:
        self.provider = provider
        self.output_dir = output_dir
        self.core_schema_version = core_schema_version

    def interpret_request(self, request: ConversationRequest) -> InterpretationFlowResult:
        parsing_result = parse_intent(request)
        return InterpretationFlowResult(
            outcome=parsing_result.outcome,
            request=request,
            intent=parsing_result.intent,
            notes=list(parsing_result.notes),
        )

    def prepare_generation(
        self,
        *,
        bundle_id: str,
        dataset_id: str,
        selection: FormatSelection | None,
        season: int,
        covered_rounds: Sequence[int] | None = None,
    ) -> GenerationPreparation:
        selection_validation = validate_generation_requirements(selection)
        if not selection_validation.generation_allowed or selection is None:
            return GenerationPreparation(selection_validation=selection_validation)

        if self.provider is None:
            raise ValueError("VisualizationService requires a provider.")

        source_dataset = self.provider.fetch_dataset(
            dataset_id=dataset_id,
            selection=selection,
            season=season,
            covered_rounds=covered_rounds,
        )
        source_validation = validate_source_dataset(source_dataset)

        if source_validation.status is ValidationStatus.REJECTED:
            return GenerationPreparation(
                selection_validation=selection_validation,
                source_dataset=source_dataset,
                source_validation=source_validation,
                next_step="source_dataset_rejected",
            )

        validated_dataset = assemble_validated_visualization_dataset(
            validated_dataset_id=f"validated-{dataset_id}",
            selection=selection,
            source_dataset=source_dataset,
        )
        validated_validation = validate_validated_visualization_dataset(validated_dataset)

        if validated_validation.status is ValidationStatus.REJECTED:
            return GenerationPreparation(
                selection_validation=selection_validation,
                source_dataset=source_dataset,
                source_validation=source_validation,
                validated_dataset=validated_dataset,
                validated_validation=validated_validation,
                next_step="validated_dataset_rejected",
            )

        next_step = "transformation_required"
        if validated_validation.status is ValidationStatus.LIMITED:
            next_step = "transformation_required_with_limited_data"

        return GenerationPreparation(
            selection_validation=selection_validation,
            source_dataset=source_dataset,
            source_validation=source_validation,
            validated_dataset=validated_dataset,
            validated_validation=validated_validation,
            next_step=next_step,
        )
