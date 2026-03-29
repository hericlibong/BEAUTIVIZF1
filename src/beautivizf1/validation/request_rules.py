from dataclasses import dataclass, field
from enum import StrEnum

from beautivizf1.domain.conversation_request import ConversationRequest
from beautivizf1.domain.format_selection import (
    MVP_AVAILABLE_FORMATS,
    FormatSelection,
    VisualizationFormat,
)
from beautivizf1.domain.visualization_intent import VisualizationIntent


class RequestDecision(StrEnum):
    EXPLOITABLE = "exploitable"
    CLARIFY = "clarify"
    REJECT = "reject"


@dataclass(slots=True)
class RequestValidationResult:
    decision: RequestDecision
    notes: list[str] = field(default_factory=list)
    generation_allowed: bool = False


@dataclass(slots=True)
class FormatChoiceValidationResult:
    decision: RequestDecision
    chosen_format: VisualizationFormat | None = None
    notes: list[str] = field(default_factory=list)
    generation_allowed: bool = False


OUT_OF_SCOPE_MARKERS = (
    "dashboard",
    "tableau de bord",
    "plusieurs graphiques",
    "plusieurs visualisations",
    "plusieurs graphes",
)

MULTI_VISUALIZATION_MARKERS = (
    ("heatmap", "line chart race"),
    ("heatmap", "line chart"),
)


def validate_conversation_request(
    request: ConversationRequest,
) -> RequestValidationResult:
    message = request.user_message.strip()
    if not message:
        return RequestValidationResult(
            decision=RequestDecision.REJECT,
            notes=["The request message cannot be empty."],
        )

    lowered_message = message.casefold()
    if any(marker in lowered_message for marker in OUT_OF_SCOPE_MARKERS):
        return RequestValidationResult(
            decision=RequestDecision.REJECT,
            notes=["The MVP only supports one guided visualization request at a time."],
        )

    if any(
        first in lowered_message and second in lowered_message
        for first, second in MULTI_VISUALIZATION_MARKERS
    ):
        return RequestValidationResult(
            decision=RequestDecision.REJECT,
            notes=["Only one visualization can be requested at a time."],
        )

    if len(message.split()) < 4:
        return RequestValidationResult(
            decision=RequestDecision.CLARIFY,
            notes=["The request needs a more specific analytic need."],
        )

    return RequestValidationResult(decision=RequestDecision.EXPLOITABLE)


def validate_visualization_intent(
    intent: VisualizationIntent,
) -> RequestValidationResult:
    analytic_need = intent.analytic_need.strip()
    if not analytic_need:
        return RequestValidationResult(
            decision=RequestDecision.REJECT,
            notes=["The interpreted intent must include an analytic need."],
        )

    if intent.clarification_needed:
        note = intent.clarification_note or "The interpreted intent needs clarification."
        return RequestValidationResult(
            decision=RequestDecision.CLARIFY,
            notes=[note],
        )

    if not intent.subject_scope:
        return RequestValidationResult(
            decision=RequestDecision.CLARIFY,
            notes=["The interpreted intent needs a clearer subject scope."],
        )

    return RequestValidationResult(decision=RequestDecision.EXPLOITABLE)


def validate_explicit_format_choice(
    user_choice: str | None,
    *,
    available_formats: tuple[VisualizationFormat, ...] = MVP_AVAILABLE_FORMATS,
) -> FormatChoiceValidationResult:
    if user_choice is None or not user_choice.strip():
        return FormatChoiceValidationResult(
            decision=RequestDecision.CLARIFY,
            notes=["An explicit format choice is required before generation."],
        )

    normalized_choice = _normalize_format_choice(user_choice)
    if normalized_choice is None or normalized_choice not in available_formats:
        return FormatChoiceValidationResult(
            decision=RequestDecision.REJECT,
            notes=["The format choice must be either heatmap or line chart race."],
        )

    return FormatChoiceValidationResult(
        decision=RequestDecision.EXPLOITABLE,
        chosen_format=normalized_choice,
        generation_allowed=True,
    )


def validate_generation_requirements(
    selection: FormatSelection | None,
) -> RequestValidationResult:
    if selection is None:
        return RequestValidationResult(
            decision=RequestDecision.CLARIFY,
            notes=["An explicit format choice is required before generation."],
        )

    if selection.available_formats != MVP_AVAILABLE_FORMATS:
        return RequestValidationResult(
            decision=RequestDecision.REJECT,
            notes=["The available formats must match the MVP format list."],
        )

    if selection.chosen_format not in selection.available_formats:
        return RequestValidationResult(
            decision=RequestDecision.REJECT,
            notes=["The chosen format must belong to the proposed MVP formats."],
        )

    return RequestValidationResult(
        decision=RequestDecision.EXPLOITABLE,
        generation_allowed=True,
    )


def _normalize_format_choice(choice: str) -> VisualizationFormat | None:
    normalized_choice = choice.strip().casefold().replace("-", " ").replace("_", " ")
    normalized_choice = " ".join(normalized_choice.split())

    if normalized_choice == "heatmap":
        return VisualizationFormat.HEATMAP
    if normalized_choice == "line chart race":
        return VisualizationFormat.LINE_CHART_RACE

    return None
