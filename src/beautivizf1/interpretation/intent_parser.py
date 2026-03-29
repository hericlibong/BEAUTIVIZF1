from dataclasses import dataclass, field
from enum import StrEnum
import re

from beautivizf1.domain.conversation_request import ConversationRequest
from beautivizf1.domain.visualization_intent import VisualizationIntent
from beautivizf1.validation.request_rules import (
    RequestDecision,
    validate_conversation_request,
    validate_visualization_intent,
)


class InterpretationOutcome(StrEnum):
    INTERPRETED = "interpreted"
    CLARIFY = "clarify"
    REJECT = "reject"


@dataclass(slots=True)
class IntentParsingResult:
    outcome: InterpretationOutcome
    intent: VisualizationIntent | None
    notes: list[str] = field(default_factory=list)


EDITORIAL_MARKERS = (
    "éditorial",
    "editorial",
    "raconter",
    "histoire",
    "storytelling",
    "mettre en avant",
)

F1_MARKERS = (
    "f1",
    "formule 1",
    "grand prix",
    "gp",
    "pilote",
    "pilotes",
    "driver",
    "drivers",
    "équipe",
    "équipes",
    "ecurie",
    "écurie",
    "qualification",
    "qualifications",
    "qualif",
    "quali",
    "course",
    "racing",
    "championnat",
)


def parse_intent(
    request: ConversationRequest,
    *,
    intent_id: str | None = None,
) -> IntentParsingResult:
    request_validation = validate_conversation_request(request)
    if request_validation.decision is RequestDecision.REJECT:
        return IntentParsingResult(
            outcome=InterpretationOutcome.REJECT,
            intent=None,
            notes=list(request_validation.notes),
        )

    analytic_need = _normalize_need(request.user_message)
    subject_scope = _extract_subject_scope(request.user_message)
    parsed_intent = VisualizationIntent(
        intent_id=intent_id or f"intent-{request.request_id}",
        request_id=request.request_id,
        analytic_need=analytic_need,
        subject_scope=subject_scope,
        clarification_needed=False,
        clarification_note=None,
    )

    if not _looks_like_f1_need(request.user_message):
        return IntentParsingResult(
            outcome=InterpretationOutcome.REJECT,
            intent=None,
            notes=["The request is outside the F1 visualization MVP scope."],
        )

    if request_validation.decision is RequestDecision.CLARIFY:
        clarification_intent = _with_clarification(
            parsed_intent,
            request_validation.notes[0],
        )
        return IntentParsingResult(
            outcome=InterpretationOutcome.CLARIFY,
            intent=clarification_intent,
            notes=list(request_validation.notes),
        )

    clarification_note = _get_scope_clarification(subject_scope)
    if clarification_note:
        clarification_intent = _with_clarification(parsed_intent, clarification_note)
        return IntentParsingResult(
            outcome=InterpretationOutcome.CLARIFY,
            intent=clarification_intent,
            notes=[clarification_note],
        )

    intent_validation = validate_visualization_intent(parsed_intent)
    if intent_validation.decision is RequestDecision.CLARIFY:
        clarification_intent = _with_clarification(
            parsed_intent,
            intent_validation.notes[0],
        )
        return IntentParsingResult(
            outcome=InterpretationOutcome.CLARIFY,
            intent=clarification_intent,
            notes=list(intent_validation.notes),
        )

    if intent_validation.decision is RequestDecision.REJECT:
        return IntentParsingResult(
            outcome=InterpretationOutcome.REJECT,
            intent=None,
            notes=list(intent_validation.notes),
        )

    return IntentParsingResult(
        outcome=InterpretationOutcome.INTERPRETED,
        intent=parsed_intent,
    )


def _normalize_need(message: str) -> str:
    return " ".join(message.strip().split())


def _extract_subject_scope(message: str) -> dict[str, object]:
    lowered_message = message.casefold()
    subject_scope: dict[str, object] = {
        "need_type": "editorial"
        if any(marker in lowered_message for marker in EDITORIAL_MARKERS)
        else "analytic"
    }

    season = _extract_season(lowered_message)
    if season is not None:
        subject_scope["season"] = season

    if "pilote" in lowered_message or "driver" in lowered_message:
        subject_scope["subject"] = "drivers"
    elif "équipe" in lowered_message or "ecurie" in lowered_message or "écurie" in lowered_message:
        subject_scope["subject"] = "teams"

    if (
        "qualification" in lowered_message
        or "qualifications" in lowered_message
        or "qualif" in lowered_message
        or "quali" in lowered_message
    ):
        subject_scope["session"] = "qualifying"
    elif "course" in lowered_message or "grand prix" in lowered_message or "gp" in lowered_message:
        subject_scope["session"] = "race"

    if "écart" in lowered_message or "gap" in lowered_message:
        subject_scope["metric"] = "gap"
    elif "performance" in lowered_message or "rythme" in lowered_message:
        subject_scope["metric"] = "performance"
    elif "point" in lowered_message or "classement" in lowered_message:
        subject_scope["metric"] = "points"

    return subject_scope


def _extract_season(message: str) -> int | None:
    match = re.search(r"\b(20\d{2})\b", message)
    if match is None:
        return None
    return int(match.group(1))


def _looks_like_f1_need(message: str) -> bool:
    lowered_message = message.casefold()
    return any(marker in lowered_message for marker in F1_MARKERS)


def _get_scope_clarification(subject_scope: dict[str, object]) -> str | None:
    if "season" not in subject_scope:
        return "Précise la saison ou la période F1 à analyser."
    if "subject" not in subject_scope:
        return "Précise si tu veux analyser les pilotes ou les équipes."
    return None


def _with_clarification(
    intent: VisualizationIntent,
    clarification_note: str,
) -> VisualizationIntent:
    return VisualizationIntent(
        intent_id=intent.intent_id,
        request_id=intent.request_id,
        analytic_need=intent.analytic_need,
        subject_scope=intent.subject_scope,
        clarification_needed=True,
        clarification_note=clarification_note,
    )
