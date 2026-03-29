from datetime import datetime, timezone

import pandas as pd

from beautivizf1.domain.format_selection import VisualizationFormat
from beautivizf1.domain.source_dataset import SourceDataset
from beautivizf1.domain.validated_visualization_dataset import (
    ValidatedVisualizationDataset,
    ValidationStatus,
)
from beautivizf1.validation.data_rules import (
    validate_source_dataset,
    validate_validated_visualization_dataset,
)


def test_validate_source_dataset_accepts_explicit_coverage_and_provenance() -> None:
    dataset = SourceDataset(
        dataset_id="src-1",
        selection_id="sel-1",
        source_name="fastf1",
        season=2025,
        records=pd.DataFrame([{"driver": "NOR", "gap": 0.123}]),
        retrieved_at=datetime.now(timezone.utc),
        provenance_note="fastf1 qualifying dataset",
        covered_rounds=[1, 2],
    )

    result = validate_source_dataset(dataset)

    assert result.status is ValidationStatus.READY
    assert result.notes == []


def test_validate_source_dataset_marks_missing_coverage_as_limited() -> None:
    dataset = SourceDataset(
        dataset_id="src-2",
        selection_id="sel-1",
        source_name="fastf1",
        season=2025,
        records=pd.DataFrame([{"driver": "NOR", "gap": 0.123}]),
        retrieved_at=datetime.now(timezone.utc),
        provenance_note="fastf1 qualifying dataset",
        covered_rounds=None,
    )

    result = validate_source_dataset(dataset)

    assert result.status is ValidationStatus.LIMITED
    assert result.notes == ["The source dataset coverage is not explicit."]


def test_validate_source_dataset_rejects_documentation_as_primary_source() -> None:
    dataset = SourceDataset(
        dataset_id="src-3",
        selection_id="sel-1",
        source_name="NotebookLM",
        season=2025,
        records=pd.DataFrame([{"driver": "NOR", "gap": 0.123}]),
        retrieved_at=datetime.now(timezone.utc),
        provenance_note="NotebookLM synthesis",
        covered_rounds=[1],
    )

    result = validate_source_dataset(dataset)

    assert result.status is ValidationStatus.REJECTED
    assert result.notes == ["NotebookLM/MCP cannot be the primary numerical data source."]


def test_validate_validated_visualization_dataset_accepts_ready_dataset() -> None:
    dataset = ValidatedVisualizationDataset(
        validated_dataset_id="val-1",
        selection_id="sel-1",
        source_dataset_id="src-1",
        chosen_format=VisualizationFormat.HEATMAP,
        traceability_keys={"request_id": "req-1", "intent_id": "intent-1"},
        core_render_fields=pd.DataFrame([{"driver": "NOR", "gap": 0.123}]),
        tooltip_fields={},
        presentation_fields={},
        coverage_summary={"partial": False},
        provenance={"source_name": "fastf1", "provenance_note": "fastf1 qualifying dataset"},
        validation_status=ValidationStatus.READY,
        validation_notes=["Coverage confirmed for requested scope."],
    )

    result = validate_validated_visualization_dataset(dataset)

    assert result.status is ValidationStatus.READY
    assert result.notes == ["Coverage confirmed for requested scope."]


def test_validate_validated_visualization_dataset_marks_partial_coverage_as_limited() -> None:
    dataset = ValidatedVisualizationDataset(
        validated_dataset_id="val-2",
        selection_id="sel-1",
        source_dataset_id="src-1",
        chosen_format=VisualizationFormat.HEATMAP,
        traceability_keys={"request_id": "req-1", "intent_id": "intent-1"},
        core_render_fields=pd.DataFrame([{"driver": "NOR", "gap": 0.123}]),
        tooltip_fields={},
        presentation_fields={},
        coverage_summary={"partial": True},
        provenance={"source_name": "fastf1", "provenance_note": "fastf1 qualifying dataset"},
        validation_status=ValidationStatus.READY,
        validation_notes=["Only part of the requested coverage is available."],
    )

    result = validate_validated_visualization_dataset(dataset)

    assert result.status is ValidationStatus.LIMITED
    assert result.notes == ["Only part of the requested coverage is available."]


def test_validate_validated_visualization_dataset_rejects_missing_core_render_fields() -> None:
    dataset = ValidatedVisualizationDataset(
        validated_dataset_id="val-3",
        selection_id="sel-1",
        source_dataset_id="src-1",
        chosen_format=VisualizationFormat.HEATMAP,
        traceability_keys={"request_id": "req-1", "intent_id": "intent-1"},
        core_render_fields=pd.DataFrame(),
        tooltip_fields={},
        presentation_fields={},
        coverage_summary={"partial": False},
        provenance={"source_name": "fastf1", "provenance_note": "fastf1 qualifying dataset"},
        validation_status=ValidationStatus.READY,
        validation_notes=["No renderable rows found."],
    )

    result = validate_validated_visualization_dataset(dataset)

    assert result.status is ValidationStatus.REJECTED
    assert result.notes == ["The validated dataset must expose core render fields."]
