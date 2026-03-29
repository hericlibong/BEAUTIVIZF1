from datetime import datetime, timezone

from beautivizf1.domain.conversation_request import ConversationRequest
from beautivizf1.domain.format_selection import MVP_AVAILABLE_FORMATS, FormatSelection
from beautivizf1.domain.visualization_intent import VisualizationIntent
from beautivizf1.validation.request_rules import (
    RequestDecision,
    validate_conversation_request,
    validate_generation_requirements,
    validate_visualization_intent,
)


def test_validate_conversation_request_accepts_a_clear_single_need() -> None:
    request = ConversationRequest(
        request_id="req-1",
        user_message="Je veux comparer les écarts des pilotes en qualifications 2025.",
        created_at=datetime.now(timezone.utc),
    )

    result = validate_conversation_request(request)

    assert result.decision is RequestDecision.EXPLOITABLE
    assert result.notes == []
    assert result.generation_allowed is False


def test_validate_conversation_request_requests_clarification_for_sparse_message() -> None:
    request = ConversationRequest(
        request_id="req-2",
        user_message="Comparer pilotes",
        created_at=datetime.now(timezone.utc),
    )

    result = validate_conversation_request(request)

    assert result.decision is RequestDecision.CLARIFY
    assert result.notes == ["The request needs a more specific analytic need."]


def test_validate_conversation_request_rejects_multi_visualization_requests() -> None:
    request = ConversationRequest(
        request_id="req-3",
        user_message="Je veux une heatmap et une line chart race pour 2025.",
        created_at=datetime.now(timezone.utc),
    )

    result = validate_conversation_request(request)

    assert result.decision is RequestDecision.REJECT
    assert result.notes == ["Only one visualization can be requested at a time."]


def test_validate_visualization_intent_requests_clarification_when_marked_ambiguous() -> None:
    intent = VisualizationIntent(
        intent_id="intent-1",
        request_id="req-1",
        analytic_need="Comparer les performances",
        subject_scope={"season": 2025},
        clarification_needed=True,
        clarification_note="Précise si tu veux les pilotes ou les équipes.",
    )

    result = validate_visualization_intent(intent)

    assert result.decision is RequestDecision.CLARIFY
    assert result.notes == ["Précise si tu veux les pilotes ou les équipes."]


def test_validate_generation_requirements_requires_an_explicit_choice() -> None:
    result = validate_generation_requirements(None)

    assert result.decision is RequestDecision.CLARIFY
    assert result.notes == ["An explicit format choice is required before generation."]
    assert result.generation_allowed is False


def test_validate_generation_requirements_allows_generation_after_choice() -> None:
    selection = FormatSelection(
        selection_id="sel-1",
        intent_id="intent-1",
        available_formats=MVP_AVAILABLE_FORMATS,
        chosen_format=MVP_AVAILABLE_FORMATS[0],
        choice_confirmed_at=datetime.now(timezone.utc),
    )

    result = validate_generation_requirements(selection)

    assert result.decision is RequestDecision.EXPLOITABLE
    assert result.generation_allowed is True
