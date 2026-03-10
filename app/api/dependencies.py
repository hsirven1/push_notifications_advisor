from functools import lru_cache

from app.data.repositories.mock_repository import MockPushHistoryRepository
from app.services.chat_service import ChatService
from app.tools.recommendation_tools import RecommendationTools


@lru_cache
def get_chat_service() -> ChatService:
    repository = MockPushHistoryRepository()
    tools = RecommendationTools(repository)
    return ChatService(tools)
