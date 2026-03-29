import pandas as pd
import pytest

from beautivizf1.domain.format_selection import VisualizationFormat
from beautivizf1.domain.validated_visualization_dataset import (
    ValidatedVisualizationDataset,
    ValidationStatus,
)
from beautivizf1.transforms.heatmap_transform import build_heatmap_dataset


def test_build_heatmap_dataset_keeps_the_common_driver_results_shape() -> None:
    dataset = _build_validated_dataset(
        pd.DataFrame(
            [
                {"round": 2, "event_name": "China", "driver": "NOR", "position": 1, "points": 25},
                {"round": 1, "event_name": "Australia", "driver": "LEC", "position": 2, "points": 18},
            ]
        )
    )

    transformed = build_heatmap_dataset(dataset)

    assert list(transformed.columns) == ["round", "event_name", "driver", "position", "points"]
    assert transformed.to_dict("records") == [
        {
            "round": 1,
            "event_name": "Australia",
            "driver": "LEC",
            "position": 2,
            "points": 18,
        },
        {
            "round": 2,
            "event_name": "China",
            "driver": "NOR",
            "position": 1,
            "points": 25,
        },
    ]


def test_build_heatmap_dataset_requires_the_common_source_columns() -> None:
    dataset = _build_validated_dataset(
        pd.DataFrame(
            [
                {"round": 1, "event_name": "Australia", "driver": "NOR", "points": 25},
            ]
        )
    )

    with pytest.raises(ValueError, match="position"):
        build_heatmap_dataset(dataset)


def _build_validated_dataset(core_render_fields: pd.DataFrame) -> ValidatedVisualizationDataset:
    return ValidatedVisualizationDataset(
        validated_dataset_id="val-heatmap",
        selection_id="sel-1",
        source_dataset_id="src-1",
        chosen_format=VisualizationFormat.HEATMAP,
        traceability_keys={"selection_id": "sel-1", "source_dataset_id": "src-1"},
        core_render_fields=core_render_fields,
        tooltip_fields={},
        presentation_fields={},
        coverage_summary={"partial": False},
        provenance={"source_name": "fastf1", "provenance_note": "race results"},
        validation_status=ValidationStatus.READY,
        validation_notes=["Coverage confirmed for requested scope."],
    )
