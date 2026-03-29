from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4

from beautivizf1.domain.conversation_request import ConversationRequest
from beautivizf1.domain.format_selection import MVP_AVAILABLE_FORMATS, VisualizationFormat
from beautivizf1.services.visualization_service import (
    InterpretationFlowResult,
    VisualizationService,
)
from beautivizf1.interpretation.intent_parser import InterpretationOutcome


@dataclass(slots=True)
class FormatProposalOption:
    format: VisualizationFormat
    title: str
    rationale: str


@dataclass(slots=True)
class FormatProposal:
    request_id: str
    intent_id: str
    need_summary: str
    proposal_note: str
    options: tuple[FormatProposalOption, ...]
    available_formats: tuple[VisualizationFormat, ...] = MVP_AVAILABLE_FORMATS
    generation_allowed: bool = False
    next_step: str = "explicit_format_choice_required"


def handle_chat_message(
    user_message: str,
    *,
    request_id: str | None = None,
    created_at: datetime | None = None,
    conversation_context: dict[str, object] | None = None,
    service: VisualizationService | None = None,
) -> InterpretationFlowResult:
    request = ConversationRequest(
        request_id=request_id or f"req-{uuid4().hex}",
        user_message=user_message,
        created_at=created_at or datetime.now(timezone.utc),
        conversation_context=conversation_context,
    )
    return handle_conversation_request(request, service=service)


def handle_conversation_request(
    request: ConversationRequest,
    *,
    service: VisualizationService | None = None,
) -> InterpretationFlowResult:
    interpretation_service = service or VisualizationService()
    return interpretation_service.interpret_request(request)


def propose_formats(interpretation: InterpretationFlowResult) -> FormatProposal:
    if interpretation.outcome is not InterpretationOutcome.INTERPRETED:
        raise ValueError("Format proposal requires an interpreted intent.")

    if interpretation.intent is None:
        raise ValueError("Format proposal requires an interpreted intent.")

    intent = interpretation.intent
    need_summary = intent.analytic_need
    scope_context = _build_scope_context(intent.subject_scope)

    return FormatProposal(
        request_id=interpretation.request.request_id,
        intent_id=intent.intent_id,
        need_summary=need_summary,
        proposal_note=f"J'ai compris ce besoin: {need_summary}",
        options=(
            FormatProposalOption(
                format=VisualizationFormat.HEATMAP,
                title="Heatmap",
                rationale=_build_heatmap_rationale(scope_context),
            ),
            FormatProposalOption(
                format=VisualizationFormat.LINE_CHART_RACE,
                title="Line chart race",
                rationale=_build_line_chart_race_rationale(scope_context),
            ),
        ),
    )


def _build_scope_context(subject_scope: dict[str, object]) -> dict[str, str]:
    subject = "pilotes"
    if subject_scope.get("subject") == "teams":
        subject = "équipes"

    season = ""
    if "season" in subject_scope:
        season = f" sur la saison {subject_scope['season']}"

    session = ""
    if subject_scope.get("session") == "qualifying":
        session = " en qualifications"
    elif subject_scope.get("session") == "race":
        session = " en course"

    metric = ""
    if subject_scope.get("metric") == "gap":
        metric = "écarts"
    elif subject_scope.get("metric") == "performance":
        metric = "performance"
    elif subject_scope.get("metric") == "points":
        metric = "points"

    return {
        "subject": subject,
        "season": season,
        "session": session,
        "metric": metric,
    }


def _build_heatmap_rationale(scope_context: dict[str, str]) -> str:
    if scope_context["metric"]:
        return (
            "La heatmap peut comparer rapidement les "
            f"{scope_context['metric']} des {scope_context['subject']}"
            f"{scope_context['session']}{scope_context['season']}."
        )

    return (
        "La heatmap peut comparer rapidement les "
        f"{scope_context['subject']}{scope_context['session']}{scope_context['season']}."
    )


def _build_line_chart_race_rationale(scope_context: dict[str, str]) -> str:
    if scope_context["metric"]:
        return (
            "La line chart race peut montrer l'évolution des "
            f"{scope_context['metric']} des {scope_context['subject']}"
            f"{scope_context['season']}."
        )

    return (
        "La line chart race peut montrer l'évolution des "
        f"{scope_context['subject']}{scope_context['season']}."
    )
