from dataclasses import dataclass, field

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
