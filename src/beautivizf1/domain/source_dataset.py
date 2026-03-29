from dataclasses import dataclass
from datetime import datetime

import pandas as pd


@dataclass(slots=True)
class SourceDataset:
    dataset_id: str
    selection_id: str
    source_name: str
    season: int
    records: pd.DataFrame
    retrieved_at: datetime
    provenance_note: str
    covered_rounds: list[int] | None = None
