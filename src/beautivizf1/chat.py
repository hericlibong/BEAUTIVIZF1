from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

from beautivizf1.domain.conversation_request import ConversationRequest
from beautivizf1.domain.visualization_intent import VisualizationIntent
from beautivizf1.interpretation.intent_parser import (
    InterpretationOutcome,
    parse_intent,
)


@dataclass(slots=True)
class ChatEntryResult:
    outcome: InterpretationOutcome
    request: ConversationRequest
    intent: VisualizationIntent | None
    notes: list[str] = field(default_factory=list)


def handle_chat_message(
    user_message: str,
    *,
    request_id: str | None = None,
    created_at: datetime | None = None,
    conversation_context: dict[str, object] | None = None,
) -> ChatEntryResult:
    request = ConversationRequest(
        request_id=request_id or f"req-{uuid4().hex}",
        user_message=user_message,
        created_at=created_at or datetime.now(timezone.utc),
        conversation_context=conversation_context,
    )
    return handle_conversation_request(request)


def handle_conversation_request(request: ConversationRequest) -> ChatEntryResult:
    parsing_result = parse_intent(request)
    return ChatEntryResult(
        outcome=parsing_result.outcome,
        request=request,
        intent=parsing_result.intent,
        notes=list(parsing_result.notes),
    )
