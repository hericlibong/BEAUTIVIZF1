from dataclasses import dataclass


@dataclass(slots=True)
class VisualizationIntent:
    intent_id: str
    request_id: str
    analytic_need: str
    subject_scope: dict[str, object]
    clarification_needed: bool
    clarification_note: str | None = None
