import json
from datetime import datetime

from beautivizf1.domain.conversation_request import ConversationRequest
from beautivizf1.domain.format_selection import (
    MVP_AVAILABLE_FORMATS,
    FormatSelection,
    VisualizationFormat,
)


def test_conversation_request_fixture_matches_domain_contract(project_root) -> None:
    fixture_path = project_root / "tests/fixtures/requests/natural_language_need.json"
    payload = json.loads(fixture_path.read_text())

    request = ConversationRequest(
        request_id=payload["request_id"],
        user_message=payload["user_message"],
        created_at=datetime.fromisoformat(payload["created_at"]),
        conversation_context=payload["conversation_context"],
    )

    assert request.request_id == payload["request_id"]
    assert request.user_message == payload["user_message"]
    assert request.created_at.isoformat() == payload["created_at"]
    assert request.conversation_context == payload["conversation_context"]


def test_format_selection_fixture_matches_domain_contract(project_root) -> None:
    fixture_path = project_root / "tests/fixtures/selections/explicit_choice.json"
    payload = json.loads(fixture_path.read_text())

    selection = FormatSelection(
        selection_id=payload["selection_id"],
        intent_id=payload["intent_id"],
        available_formats=tuple(
            VisualizationFormat(value) for value in payload["available_formats"]
        ),
        chosen_format=VisualizationFormat(payload["chosen_format"]),
        choice_confirmed_at=datetime.fromisoformat(payload["choice_confirmed_at"]),
        proposal_note=payload["proposal_note"],
    )

    assert selection.selection_id == payload["selection_id"]
    assert selection.intent_id == payload["intent_id"]
    assert selection.available_formats == MVP_AVAILABLE_FORMATS
    assert selection.chosen_format in selection.available_formats
    assert selection.choice_confirmed_at.isoformat() == payload["choice_confirmed_at"]
    assert selection.proposal_note == payload["proposal_note"]
