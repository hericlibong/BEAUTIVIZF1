from dataclasses import dataclass, field
from enum import StrEnum

from beautivizf1.domain.conversation_request import ConversationRequest
from beautivizf1.domain.format_selection import MVP_AVAILABLE_FORMATS, FormatSelection
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
