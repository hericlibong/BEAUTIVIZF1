from datetime import datetime, timezone

from beautivizf1.chat import propose_formats
from beautivizf1.domain.conversation_request import ConversationRequest
from beautivizf1.domain.visualization_intent import VisualizationIntent
from beautivizf1.domain.format_selection import MVP_AVAILABLE_FORMATS, VisualizationFormat
from beautivizf1.interpretation.intent_parser import InterpretationOutcome
from beautivizf1.services.visualization_service import InterpretationFlowResult


def test_propose_formats_returns_the_two_mvp_formats() -> None:
    interpretation = InterpretationFlowResult(
        outcome=InterpretationOutcome.INTERPRETED,
        request=ConversationRequest(
            request_id="req-1",
            user_message="Je veux comparer les écarts des pilotes en qualifications 2025.",
            created_at=datetime.now(timezone.utc),
        ),
        intent=VisualizationIntent(
            intent_id="intent-1",
            request_id="req-1",
            analytic_need="Je veux comparer les écarts des pilotes en qualifications 2025.",
            subject_scope={
                "subject": "drivers",
                "season": 2025,
                "session": "qualifying",
                "metric": "gap",
            },
            clarification_needed=False,
        ),
    )

    proposal = propose_formats(interpretation)

    assert proposal.available_formats == MVP_AVAILABLE_FORMATS
    assert [option.format for option in proposal.options] == [
        VisualizationFormat.HEATMAP,
        VisualizationFormat.LINE_CHART_RACE,
    ]


def test_propose_formats_contextualizes_the_need_and_keeps_generation_disabled() -> None:
    interpretation = InterpretationFlowResult(
        outcome=InterpretationOutcome.INTERPRETED,
        request=ConversationRequest(
            request_id="req-2",
            user_message="Je veux raconter l'histoire des équipes en 2025 en F1.",
            created_at=datetime.now(timezone.utc),
        ),
        intent=VisualizationIntent(
            intent_id="intent-2",
            request_id="req-2",
            analytic_need="Je veux raconter l'histoire des équipes en 2025 en F1.",
            subject_scope={
                "need_type": "editorial",
                "subject": "teams",
                "season": 2025,
            },
            clarification_needed=False,
        ),
    )

    proposal = propose_formats(interpretation)

    assert "équipes" in proposal.proposal_note
    assert "saison 2025" in proposal.options[0].rationale
    assert "équipes" in proposal.options[1].rationale
    assert proposal.generation_allowed is False
    assert proposal.next_step == "explicit_format_choice_required"
