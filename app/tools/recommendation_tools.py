from __future__ import annotations

from collections import Counter
from statistics import mean
from typing import Any

from app.data.repositories.base import PushHistoryRepository


class RecommendationTools:
    """Business tools available to the assistant orchestration layer."""

    def __init__(self, repository: PushHistoryRepository) -> None:
        self.repository = repository

    def get_similar_events(
        self,
        event_id: str | None,
        event_type: str,
        market: str,
        venue_size: int,
    ) -> list[dict[str, Any]]:
        return self.repository.get_similar_events(event_id, event_type, market, venue_size)

    def get_push_history(self, similar_event_ids: list[str]) -> list[dict[str, Any]]:
        return self.repository.get_push_history(similar_event_ids)

    def get_best_performing_pushes(self, filters: dict[str, Any], limit: int = 3) -> list[dict[str, Any]]:
        pushes = self._apply_filters(self.repository.get_push_history(filters["event_ids"]), filters)
        return sorted(pushes, key=lambda row: (row["ctr"], row["conversion_rate"]), reverse=True)[:limit]

    def get_best_segments(self, filters: dict[str, Any]) -> list[dict[str, Any]]:
        pushes = self._apply_filters(self.repository.get_push_history(filters["event_ids"]), filters)
        segment_scores: dict[str, list[float]] = {}
        for push in pushes:
            segment_scores.setdefault(push["segment"], []).append(push["ctr"])
        return [
            {"segment": segment, "avg_ctr": round(mean(scores), 4)}
            for segment, scores in sorted(segment_scores.items(), key=lambda item: mean(item[1]), reverse=True)
        ]

    def get_best_send_times(self, filters: dict[str, Any]) -> list[dict[str, Any]]:
        pushes = self._apply_filters(self.repository.get_push_history(filters["event_ids"]), filters)
        send_hour_scores: dict[int, list[float]] = {}
        for push in pushes:
            send_hour_scores.setdefault(push["send_hour"], []).append(push["ctr"])
        return [
            {"hour": hour, "avg_ctr": round(mean(scores), 4)}
            for hour, scores in sorted(send_hour_scores.items(), key=lambda item: mean(item[1]), reverse=True)
        ]

    def get_best_destinations(self, filters: dict[str, Any]) -> list[dict[str, Any]]:
        pushes = self._apply_filters(self.repository.get_push_history(filters["event_ids"]), filters)
        destination_counter = Counter(push["destination"] for push in pushes)
        return [
            {"destination": destination, "count": count}
            for destination, count in destination_counter.most_common()
        ]

    def _apply_filters(self, pushes: list[dict[str, Any]], filters: dict[str, Any]) -> list[dict[str, Any]]:
        segment = filters.get("segment")
        if segment:
            pushes = [push for push in pushes if push["segment"] == segment]
        return pushes
