from datetime import datetime, timezone
from uuid import uuid4

from beautivizf1.domain.conversation_request import ConversationRequest
from beautivizf1.services.visualization_service import (
    InterpretationFlowResult,
    VisualizationService,
)


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
