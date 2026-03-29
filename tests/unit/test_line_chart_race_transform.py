import pandas as pd
import pytest

from beautivizf1.domain.format_selection import VisualizationFormat
from beautivizf1.domain.validated_visualization_dataset import (
    ValidatedVisualizationDataset,
    ValidationStatus,
)
from beautivizf1.transforms.line_chart_race_transform import build_line_chart_race_dataset


def test_build_line_chart_race_dataset_adds_cumulative_points_per_driver() -> None:
    dataset = _build_validated_dataset(
        pd.DataFrame(
            [
                {"round": 2, "event_name": "China", "driver": "NOR", "position": 2, "points": 18},
                {"round": 1, "event_name": "Australia", "driver": "NOR", "position": 1, "points": 25},
                {"round": 1, "event_name": "Australia", "driver": "LEC", "position": 2, "points": 18},
                {"round": 2, "event_name": "China", "driver": "LEC", "position": 1, "points": 25},
            ]
        )
    )

    transformed = build_line_chart_race_dataset(dataset)

    assert list(transformed.columns) == [
        "round",
        "event_name",
        "driver",
        "position",
        "points",
        "cumulative_points",
    ]
    assert transformed.to_dict("records") == [
        {
            "round": 1,
            "event_name": "Australia",
            "driver": "LEC",
            "position": 2,
            "points": 18,
            "cumulative_points": 18,
        },
        {
            "round": 1,
            "event_name": "Australia",
            "driver": "NOR",
            "position": 1,
            "points": 25,
            "cumulative_points": 25,
        },
        {
            "round": 2,
            "event_name": "China",
            "driver": "LEC",
            "position": 1,
            "points": 25,
            "cumulative_points": 43,
        },
        {
            "round": 2,
            "event_name": "China",
            "driver": "NOR",
            "position": 2,
            "points": 18,
            "cumulative_points": 43,
        },
    ]


def test_build_line_chart_race_dataset_requires_the_common_source_columns() -> None:
    dataset = _build_validated_dataset(
        pd.DataFrame(
            [
                {"round": 1, "event_name": "Australia", "driver": "NOR", "position": 1},
            ]
        )
    )

    with pytest.raises(ValueError, match="points"):
        build_line_chart_race_dataset(dataset)


def _build_validated_dataset(core_render_fields: pd.DataFrame) -> ValidatedVisualizationDataset:
    return ValidatedVisualizationDataset(
        validated_dataset_id="val-line-chart-race",
        selection_id="sel-1",
        source_dataset_id="src-1",
        chosen_format=VisualizationFormat.LINE_CHART_RACE,
        traceability_keys={"selection_id": "sel-1", "source_dataset_id": "src-1"},
        core_render_fields=core_render_fields,
        tooltip_fields={},
        presentation_fields={},
        coverage_summary={"partial": False},
        provenance={"source_name": "fastf1", "provenance_note": "race results"},
        validation_status=ValidationStatus.READY,
        validation_notes=["Coverage confirmed for requested scope."],
    )
