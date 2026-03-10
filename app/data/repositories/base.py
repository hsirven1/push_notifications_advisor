from abc import ABC, abstractmethod
from typing import Any


class PushHistoryRepository(ABC):
    """Data access contract for historical project + push data lookups."""

    @abstractmethod
    def get_similar_projects(
        self,
        project_name: str,
        event_category: str,
        country: str,
        language: str,
    ) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_push_history(self, project_names: list[str]) -> list[dict[str, Any]]:
        raise NotImplementedError
