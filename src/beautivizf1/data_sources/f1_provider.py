from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Sequence

import pandas as pd

from beautivizf1.domain.format_selection import FormatSelection
from beautivizf1.domain.source_dataset import SourceDataset


class F1Provider(ABC):
    source_name: str

    @abstractmethod
    def fetch_dataset(
        self,
        *,
        dataset_id: str,
        selection: FormatSelection,
        season: int,
        covered_rounds: Sequence[int] | None = None,
    ) -> SourceDataset:
        """Return a source dataset for a confirmed format selection."""

    def build_source_dataset(
        self,
        *,
        dataset_id: str,
        selection: FormatSelection,
        season: int,
        records: pd.DataFrame,
        provenance_note: str,
        covered_rounds: Sequence[int] | None = None,
        retrieved_at: datetime | None = None,
    ) -> SourceDataset:
        return SourceDataset(
            dataset_id=dataset_id,
            selection_id=selection.selection_id,
            source_name=self.source_name,
            season=season,
            records=records,
            retrieved_at=retrieved_at or datetime.now(timezone.utc),
            provenance_note=provenance_note,
            covered_rounds=list(covered_rounds) if covered_rounds is not None else None,
        )
