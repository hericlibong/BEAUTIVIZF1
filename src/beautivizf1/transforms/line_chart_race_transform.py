import pandas as pd

from beautivizf1.domain.validated_visualization_dataset import ValidatedVisualizationDataset


REQUIRED_LINE_CHART_RACE_COLUMNS = ("round", "event_name", "driver", "position", "points")


def build_line_chart_race_dataset(dataset: ValidatedVisualizationDataset) -> pd.DataFrame:
    _require_columns(dataset.core_render_fields, REQUIRED_LINE_CHART_RACE_COLUMNS)
    transformed = dataset.core_render_fields.loc[:, REQUIRED_LINE_CHART_RACE_COLUMNS].copy()
    transformed = transformed.sort_values(["driver", "round"], ignore_index=True)
    transformed["cumulative_points"] = transformed.groupby("driver")["points"].cumsum()
    return transformed.sort_values(["round", "driver"], ignore_index=True)


def _require_columns(records: pd.DataFrame, required_columns: tuple[str, ...]) -> None:
    missing_columns = [column for column in required_columns if column not in records.columns]
    if missing_columns:
        raise ValueError(
            "Line chart race transformation requires columns: "
            f"{', '.join(missing_columns)}."
        )
