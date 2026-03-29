from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class VisualizationFormat(StrEnum):
    HEATMAP = "heatmap"
    LINE_CHART_RACE = "line_chart_race"


MVP_AVAILABLE_FORMATS = (
    VisualizationFormat.HEATMAP,
    VisualizationFormat.LINE_CHART_RACE,
)


@dataclass(slots=True)
class FormatSelection:
    selection_id: str
    intent_id: str
    available_formats: tuple[VisualizationFormat, ...]
    chosen_format: VisualizationFormat
    choice_confirmed_at: datetime
    proposal_note: str | None = None
