from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_chat_service
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service),
) -> ChatResponse:
    try:
        return chat_service.get_recommendation(request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
