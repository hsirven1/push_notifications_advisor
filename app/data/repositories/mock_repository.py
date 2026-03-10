from __future__ import annotations

from typing import Any

from app.data.repositories.base import PushHistoryRepository


class MockPushHistoryRepository(PushHistoryRepository):
    """In-memory mock repository for V1 local development."""

    def __init__(self) -> None:
        self._events = [
            {"event_id": "evt_100", "event_type": "concert", "market": "NYC", "venue_size": 12000},
            {"event_id": "evt_101", "event_type": "concert", "market": "NYC", "venue_size": 10000},
            {"event_id": "evt_102", "event_type": "sports", "market": "SF", "venue_size": 18000},
        ]
        self._pushes = [
            {
                "event_id": "evt_100",
                "content": "Doors open in 1 hour. Grab merch early!",
                "segment": "ticket_holders",
                "destination": "app://event/evt_100/merch",
                "send_hour": 17,
                "ctr": 0.14,
                "conversion_rate": 0.05,
            },
            {
                "event_id": "evt_101",
                "content": "Tonight at 8pm—arrive by 7 for faster entry.",
                "segment": "ticket_holders",
                "destination": "app://event/evt_101/checkin",
                "send_hour": 16,
                "ctr": 0.16,
                "conversion_rate": 0.06,
            },
            {
                "event_id": "evt_102",
                "content": "Kickoff reminder: parking lots are filling fast.",
                "segment": "local_fans",
                "destination": "app://event/evt_102/parking",
                "send_hour": 14,
                "ctr": 0.09,
                "conversion_rate": 0.03,
            },
        ]

    def get_similar_events(
        self,
        event_id: str | None,
        event_type: str,
        market: str,
        venue_size: int,
    ) -> list[dict[str, Any]]:
        candidate_events = [
            event
            for event in self._events
            if event["event_type"] == event_type and event["market"] == market
        ]
        if event_id:
            candidate_events = [event for event in candidate_events if event["event_id"] != event_id]

        return sorted(
            candidate_events,
            key=lambda event: abs(event["venue_size"] - venue_size),
        )[:5]

    def get_push_history(self, similar_event_ids: list[str]) -> list[dict[str, Any]]:
        event_id_set = set(similar_event_ids)
        return [push for push in self._pushes if push["event_id"] in event_id_set]
