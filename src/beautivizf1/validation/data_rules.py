from dataclasses import dataclass, field

from beautivizf1.domain.format_selection import FormatSelection
from beautivizf1.domain.source_dataset import SourceDataset
from beautivizf1.domain.validated_visualization_dataset import (
    ValidatedVisualizationDataset,
    ValidationStatus,
)


@dataclass(slots=True)
class DataValidationResult:
    status: ValidationStatus
    notes: list[str] = field(default_factory=list)


def validate_source_dataset(dataset: SourceDataset) -> DataValidationResult:
    if dataset.season <= 0:
        return DataValidationResult(
            status=ValidationStatus.REJECTED,
            notes=["The source dataset season must be a positive integer."],
        )

    if dataset.records.empty:
        return DataValidationResult(
            status=ValidationStatus.REJECTED,
            notes=["The source dataset must contain records."],
        )

    if not dataset.source_name.strip():
        return DataValidationResult(
            status=ValidationStatus.REJECTED,
            notes=["The source dataset must declare its primary source."],
        )

    if _uses_documentation_as_primary_source(dataset.source_name, dataset.provenance_note):
        return DataValidationResult(
            status=ValidationStatus.REJECTED,
            notes=["NotebookLM/MCP cannot be the primary numerical data source."],
        )

    if not dataset.provenance_note.strip():
        return DataValidationResult(
            status=ValidationStatus.REJECTED,
            notes=["The source dataset must include a provenance note."],
        )

    if not dataset.covered_rounds:
        return DataValidationResult(
            status=ValidationStatus.LIMITED,
            notes=["The source dataset coverage is not explicit."],
        )

    return DataValidationResult(status=ValidationStatus.READY)


def validate_validated_visualization_dataset(
    dataset: ValidatedVisualizationDataset,
) -> DataValidationResult:
    if dataset.core_render_fields.empty:
        return DataValidationResult(
            status=ValidationStatus.REJECTED,
            notes=["The validated dataset must expose core render fields."],
        )

    if not dataset.traceability_keys:
        return DataValidationResult(
            status=ValidationStatus.REJECTED,
            notes=["The validated dataset must expose traceability keys."],
        )

    if not dataset.provenance:
        return DataValidationResult(
            status=ValidationStatus.REJECTED,
            notes=["The validated dataset must expose provenance."],
        )

    if _uses_documentation_as_primary_source(
        str(dataset.provenance.get("source_name", "")),
        str(dataset.provenance.get("provenance_note", "")),
    ):
        return DataValidationResult(
            status=ValidationStatus.REJECTED,
            notes=["NotebookLM/MCP cannot be the primary numerical data source."],
        )

    if not dataset.validation_notes:
        return DataValidationResult(
            status=ValidationStatus.REJECTED,
            notes=["The validated dataset must expose validation notes."],
        )

    if dataset.validation_status is ValidationStatus.REJECTED:
        return DataValidationResult(
            status=ValidationStatus.REJECTED,
            notes=list(dataset.validation_notes),
        )

    if dataset.validation_status is ValidationStatus.LIMITED or _has_limited_coverage(
        dataset.coverage_summary
    ):
        return DataValidationResult(
            status=ValidationStatus.LIMITED,
            notes=list(dataset.validation_notes),
        )

    return DataValidationResult(status=ValidationStatus.READY, notes=list(dataset.validation_notes))


def assemble_validated_visualization_dataset(
    *,
    validated_dataset_id: str,
    selection: FormatSelection,
    source_dataset: SourceDataset,
) -> ValidatedVisualizationDataset:
    source_validation = validate_source_dataset(source_dataset)
    validation_notes = list(source_validation.notes)

    if source_validation.status is ValidationStatus.READY:
        validation_notes = ["Coverage confirmed for requested scope."]
    elif not validation_notes:
        validation_notes = ["The source dataset is usable with limited coverage."]

    return ValidatedVisualizationDataset(
        validated_dataset_id=validated_dataset_id,
        selection_id=selection.selection_id,
        source_dataset_id=source_dataset.dataset_id,
        chosen_format=selection.chosen_format,
        traceability_keys={
            "intent_id": selection.intent_id,
            "selection_id": selection.selection_id,
            "source_dataset_id": source_dataset.dataset_id,
            "season": source_dataset.season,
        },
        core_render_fields=source_dataset.records.copy(),
        tooltip_fields={},
        presentation_fields={},
        coverage_summary=_build_coverage_summary(source_dataset, source_validation.status),
        provenance={
            "source_name": source_dataset.source_name,
            "season": source_dataset.season,
            "covered_rounds": list(source_dataset.covered_rounds or []),
            "retrieved_at": source_dataset.retrieved_at.isoformat(),
            "provenance_note": source_dataset.provenance_note,
        },
        validation_status=source_validation.status,
        validation_notes=validation_notes,
    )


def _uses_documentation_as_primary_source(source_name: str, provenance_note: str) -> bool:
    primary_source = f"{source_name} {provenance_note}".casefold()
    return "notebooklm" in primary_source or "mcp" in primary_source


def _has_limited_coverage(coverage_summary: dict[str, object]) -> bool:
    return bool(
        coverage_summary.get("partial")
        or coverage_summary.get("coverage_gap")
        or coverage_summary.get("missing_rounds")
        or coverage_summary.get("excluded_rounds")
    )


def _build_coverage_summary(
    source_dataset: SourceDataset,
    status: ValidationStatus,
) -> dict[str, object]:
    covered_rounds = list(source_dataset.covered_rounds or [])
    has_explicit_coverage = source_dataset.covered_rounds is not None
    return {
        "season": source_dataset.season,
        "covered_rounds": covered_rounds,
        "covered_round_count": len(covered_rounds),
        "partial": status is ValidationStatus.LIMITED,
        "coverage_gap": not has_explicit_coverage,
        "missing_rounds": [],
        "excluded_rounds": [],
    }
