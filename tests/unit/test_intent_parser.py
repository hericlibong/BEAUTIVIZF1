from datetime import datetime, timezone

from beautivizf1.domain.conversation_request import ConversationRequest
from beautivizf1.interpretation.intent_parser import (
    InterpretationOutcome,
    parse_intent,
)


def test_parse_intent_interprets_a_clear_analytic_need() -> None:
    request = ConversationRequest(
        request_id="req-analytic",
        user_message="Je veux comparer les écarts des pilotes en qualifications 2025.",
        created_at=datetime.now(timezone.utc),
    )

    result = parse_intent(request)

    assert result.outcome is InterpretationOutcome.INTERPRETED
    assert result.intent is not None
    assert result.intent.clarification_needed is False
    assert result.intent.subject_scope == {
        "need_type": "analytic",
        "season": 2025,
        "subject": "drivers",
        "session": "qualifying",
        "metric": "gap",
    }


def test_parse_intent_interprets_a_clear_editorial_need() -> None:
    request = ConversationRequest(
        request_id="req-editorial",
        user_message="Je veux raconter l'histoire des équipes en 2025 en F1.",
        created_at=datetime.now(timezone.utc),
    )

    result = parse_intent(request)

    assert result.outcome is InterpretationOutcome.INTERPRETED
    assert result.intent is not None
    assert result.intent.subject_scope["need_type"] == "editorial"
    assert result.intent.subject_scope["season"] == 2025
    assert result.intent.subject_scope["subject"] == "teams"


def test_parse_intent_requests_clarification_for_vague_f1_need() -> None:
    request = ConversationRequest(
        request_id="req-clarify",
        user_message="Comparer les pilotes en F1",
        created_at=datetime.now(timezone.utc),
    )

    result = parse_intent(request)

    assert result.outcome is InterpretationOutcome.CLARIFY
    assert result.intent is not None
    assert result.intent.clarification_needed is True
    assert result.notes == ["Précise la saison ou la période F1 à analyser."]


def test_parse_intent_rejects_a_request_outside_the_f1_scope() -> None:
    request = ConversationRequest(
        request_id="req-reject",
        user_message="Je veux visualiser les ventes de smartphones en Europe.",
        created_at=datetime.now(timezone.utc),
    )

    result = parse_intent(request)

    assert result.outcome is InterpretationOutcome.REJECT
    assert result.intent is None
    assert result.notes == ["The request is outside the F1 visualization MVP scope."]
