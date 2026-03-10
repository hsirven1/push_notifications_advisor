from app.schemas.chat import ChatRequest


class RequestValidator:
    """Placeholder validation guardrails for V1."""

    @staticmethod
    def validate_chat_request(request: ChatRequest) -> None:
        if not request.user_message.strip():
            raise ValueError("user_message cannot be empty")
