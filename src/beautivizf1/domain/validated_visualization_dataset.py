from dataclasses import dataclass
from enum import StrEnum

import pandas as pd

from beautivizf1.domain.format_selection import VisualizationFormat


class ValidationStatus(StrEnum):
    READY = "ready"
    LIMITED = "limited"
    REJECTED = "rejected"


@dataclass(slots=True)
class ValidatedVisualizationDataset:
    validated_dataset_id: str
    selection_id: str
    source_dataset_id: str
    chosen_format: VisualizationFormat
    traceability_keys: dict[str, object]
    core_render_fields: pd.DataFrame
    tooltip_fields: dict[str, object]
    presentation_fields: dict[str, object]
    coverage_summary: dict[str, object]
    provenance: dict[str, object]
    validation_status: ValidationStatus
    validation_notes: list[str]
