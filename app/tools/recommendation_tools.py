from __future__ import annotations

from collections import Counter
from datetime import datetime
from typing import Any

from app.data.repositories.base import PushHistoryRepository


class RecommendationTools:
    """Business tools available to the assistant orchestration layer."""

    def __init__(self, repository: PushHistoryRepository) -> None:
        self.repository = repository

    def get_similar_projects(
        self,
        project_name: str,
        event_category: str,
        country: str,
        language: str,
    ) -> list[dict[str, Any]]:
        return self.repository.get_similar_projects(project_name, event_category, country, language)

    def get_push_history(self, project_names: list[str]) -> list[dict[str, Any]]:
        return self.repository.get_push_history(project_names)

    def get_common_segments(self, push_history: list[dict[str, Any]]) -> list[dict[str, Any]]:
        counts = Counter(push["segment"] for push in push_history)
        return [{"segment": segment, "count": count} for segment, count in counts.most_common()]

    def get_common_redirections(self, push_history: list[dict[str, Any]]) -> list[dict[str, Any]]:
        counts = Counter(push["redirection"] for push in push_history)
        return [{"redirection": value, "count": count} for value, count in counts.most_common()]

    def get_timing_patterns(
        self,
        push_history: list[dict[str, Any]],
        project_lookup: dict[str, dict[str, Any]],
    ) -> list[dict[str, Any]]:
        pattern_counts: Counter[tuple[int, int, str, int]] = Counter()
        for push in push_history:
            project = project_lookup.get(push["project_name"])
            if not project:
                continue
            send_dt = datetime.fromisoformat(push["datetime_sent"])
            start_dt = datetime.fromisoformat(project["start_date"])
            end_dt = datetime.fromisoformat(project["end_date"])
            key = (
                (start_dt.date() - send_dt.date()).days,
                (end_dt.date() - send_dt.date()).days,
                send_dt.strftime("%A"),
                send_dt.hour,
            )
            pattern_counts[key] += 1

        return [
            {
                "days_before_event_start": key[0],
                "days_before_event_end": key[1],
                "send_weekday": key[2],
                "send_hour_local": key[3],
                "count": count,
            }
            for key, count in pattern_counts.most_common()
        ]

    def get_push_examples(self, push_history: list[dict[str, Any]], limit: int = 3) -> list[dict[str, Any]]:
        ordered = sorted(
            push_history,
            key=lambda push: (
                push["datetime_sent"],
                push["title"],
                push["segment"],
            ),
            reverse=True,
        )
        return [
            {
                "title": push["title"],
                "message": push["message"],
                "segment": push["segment"],
                "redirection": push["redirection"],
            }
            for push in ordered[:limit]
        ]
