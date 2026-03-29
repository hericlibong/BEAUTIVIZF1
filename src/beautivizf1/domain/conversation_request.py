from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class ConversationRequest:
    request_id: str
    user_message: str
    created_at: datetime
    conversation_context: dict[str, object] | None = None
