from beautivizf1.chat import handle_chat_message
from beautivizf1.interpretation.intent_parser import InterpretationOutcome
from beautivizf1.services.visualization_service import VisualizationService


def test_chat_interpretation_flow_returns_an_interpreted_result() -> None:
    service = VisualizationService()

    result = handle_chat_message(
        "Je veux comparer les écarts des pilotes en qualifications 2025.",
        request_id="req-flow-interpreted",
        service=service,
    )

    assert result.outcome is InterpretationOutcome.INTERPRETED
    assert result.request.request_id == "req-flow-interpreted"
    assert result.intent is not None
    assert result.intent.request_id == result.request.request_id
    assert result.notes == []


def test_chat_interpretation_flow_returns_a_clarification_result() -> None:
    service = VisualizationService()

    result = handle_chat_message(
        "Comparer les pilotes en F1",
        request_id="req-flow-clarify",
        service=service,
    )

    assert result.outcome is InterpretationOutcome.CLARIFY
    assert result.intent is not None
    assert result.intent.clarification_needed is True
    assert result.notes == ["Précise la saison ou la période F1 à analyser."]


def test_chat_interpretation_flow_returns_a_rejected_result() -> None:
    service = VisualizationService()

    result = handle_chat_message(
        "Je veux visualiser les ventes de smartphones en Europe.",
        request_id="req-flow-reject",
        service=service,
    )

    assert result.outcome is InterpretationOutcome.REJECT
    assert result.intent is None
    assert result.notes == ["The request is outside the F1 visualization MVP scope."]
