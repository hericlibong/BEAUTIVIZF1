import pandas as pd

from beautivizf1.domain.validated_visualization_dataset import ValidatedVisualizationDataset


REQUIRED_HEATMAP_COLUMNS = ("round", "event_name", "driver", "position", "points")


def build_heatmap_dataset(dataset: ValidatedVisualizationDataset) -> pd.DataFrame:
    _require_columns(dataset.core_render_fields, REQUIRED_HEATMAP_COLUMNS)
    transformed = dataset.core_render_fields.loc[:, REQUIRED_HEATMAP_COLUMNS].copy()
    return transformed.sort_values(["round", "driver"], ignore_index=True)


def _require_columns(records: pd.DataFrame, required_columns: tuple[str, ...]) -> None:
    missing_columns = [column for column in required_columns if column not in records.columns]
    if missing_columns:
        raise ValueError(
            f"Heatmap transformation requires columns: {', '.join(missing_columns)}."
        )
