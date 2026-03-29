from datetime import datetime, timezone
from typing import Sequence

import pandas as pd

from beautivizf1.domain.format_selection import FormatSelection
from beautivizf1.domain.source_dataset import SourceDataset


class F1Provider:
    source_name = "fastf1"

    def fetch_dataset(
        self,
        *,
        dataset_id: str,
        selection: FormatSelection,
        season: int,
        covered_rounds: Sequence[int] | None = None,
    ) -> SourceDataset:
        requested_rounds = self._resolve_rounds(season, covered_rounds)
        records, retrieved_rounds = self._fetch_race_results(season, requested_rounds)

        return self.build_source_dataset(
            dataset_id=dataset_id,
            selection=selection,
            season=season,
            records=records,
            provenance_note=self._build_provenance_note(
                season=season,
                requested_rounds=requested_rounds,
                retrieved_rounds=retrieved_rounds,
            ),
            covered_rounds=retrieved_rounds,
        )

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

    def _resolve_rounds(self, season: int, covered_rounds: Sequence[int] | None) -> list[int]:
        if covered_rounds:
            return sorted({round_number for round_number in covered_rounds if round_number > 0})

        fastf1 = self._import_fastf1()
        schedule = fastf1.get_event_schedule(season, include_testing=False)
        round_numbers = schedule["RoundNumber"].dropna().astype(int)
        return sorted({round_number for round_number in round_numbers if round_number > 0})

    def _fetch_race_results(
        self,
        season: int,
        round_numbers: Sequence[int],
    ) -> tuple[pd.DataFrame, list[int]]:
        frames = []
        retrieved_rounds: list[int] = []

        for round_number in round_numbers:
            results, event_name = self._load_race_results(season, round_number)
            if results is None or results.empty:
                continue

            frames.append(
                pd.DataFrame(
                    {
                        "round": round_number,
                        "event_name": event_name,
                        "driver": self._string_column(results, "Abbreviation"),
                        "position": self._numeric_column(results, "Position"),
                        "points": self._numeric_column(results, "Points"),
                    }
                )
            )
            retrieved_rounds.append(round_number)

        if not frames:
            return pd.DataFrame(), []

        return pd.concat(frames, ignore_index=True), retrieved_rounds

    def _load_race_results(
        self,
        season: int,
        round_number: int,
    ) -> tuple[pd.DataFrame | None, str]:
        fastf1 = self._import_fastf1()

        try:
            session = fastf1.get_session(season, round_number, "R")
            session.load(laps=False, telemetry=False, weather=False, messages=False)
        except Exception:
            return None, ""

        event_name = str(session.event["EventName"])
        return session.results.copy(), event_name

    def _build_provenance_note(
        self,
        *,
        season: int,
        requested_rounds: Sequence[int],
        retrieved_rounds: Sequence[int],
    ) -> str:
        return (
            f"fastf1 race results for season {season}; "
            f"requested_rounds={list(requested_rounds)}; "
            f"retrieved_rounds={list(retrieved_rounds)}"
        )

    def _import_fastf1(self):
        import fastf1

        return fastf1

    def _string_column(self, results: pd.DataFrame, column: str) -> pd.Series:
        if column not in results:
            return pd.Series([""] * len(results), index=results.index)
        return results[column].fillna("").astype(str)

    def _numeric_column(self, results: pd.DataFrame, column: str) -> pd.Series:
        if column not in results:
            return pd.Series([float("nan")] * len(results), index=results.index, dtype="float64")
        return pd.to_numeric(results[column], errors="coerce")
