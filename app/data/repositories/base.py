from abc import ABC, abstractmethod
from typing import Any


class PushHistoryRepository(ABC):
    """Data access contract for historical push-performance lookups."""

    @abstractmethod
    def get_similar_events(
        self,
        event_id: str | None,
        event_type: str,
        market: str,
        venue_size: int,
    ) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_push_history(self, similar_event_ids: list[str]) -> list[dict[str, Any]]:
        raise NotImplementedError
