from app.schemas.chat import ChatRequest


class RequestValidator:
    """Placeholder validation guardrails for V1."""

    @staticmethod
    def validate_chat_request(request: ChatRequest) -> None:
        if not request.user_message.strip():
            raise ValueError("user_message cannot be empty")
        if request.project_context.end_date < request.project_context.start_date:
            raise ValueError("end_date must be on or after start_date")
