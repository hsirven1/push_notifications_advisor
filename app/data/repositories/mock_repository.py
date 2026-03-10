from __future__ import annotations

from typing import Any

from app.data.repositories.base import PushHistoryRepository


class MockPushHistoryRepository(PushHistoryRepository):
    """In-memory mock repository for V1 local development."""

    def __init__(self) -> None:
        self._projects = [
            {
                "project_name": "summer_beats_2025",
                "event_category": "concert",
                "country": "US",
                "start_date": "2025-07-10",
                "end_date": "2025-07-12",
                "language": "en",
            },
            {
                "project_name": "city_lights_live",
                "event_category": "concert",
                "country": "US",
                "start_date": "2025-08-20",
                "end_date": "2025-08-20",
                "language": "en",
            },
            {
                "project_name": "arena_night_final",
                "event_category": "sports",
                "country": "US",
                "start_date": "2025-09-01",
                "end_date": "2025-09-01",
                "language": "en",
            },
            {
                "project_name": "festival_france",
                "event_category": "concert",
                "country": "FR",
                "start_date": "2025-06-14",
                "end_date": "2025-06-15",
                "language": "fr",
            },
        ]

        self._pushes = [
            {
                "project_name": "summer_beats_2025",
                "title": "Your show starts tomorrow",
                "message": "Plan your arrival and open your ticket before heading out.",
                "redirection": "app://project/summer_beats_2025/tickets",
                "segment": "ticket_holders",
                "datetime_sent": "2025-07-09T18:00:00",
            },
            {
                "project_name": "summer_beats_2025",
                "title": "Doors open now",
                "message": "Entry gates are open. Use the fast-lane QR check-in.",
                "redirection": "app://project/summer_beats_2025/checkin",
                "segment": "ticket_holders",
                "datetime_sent": "2025-07-10T16:00:00",
            },
            {
                "project_name": "city_lights_live",
                "title": "Event day reminder",
                "message": "Your concert is tonight. View entry details in-app.",
                "redirection": "app://project/city_lights_live/checkin",
                "segment": "ticket_holders",
                "datetime_sent": "2025-08-20T11:00:00",
            },
            {
                "project_name": "city_lights_live",
                "title": "Merch pickup window",
                "message": "Skip lines by checking merch pickup slots before arrival.",
                "redirection": "app://project/city_lights_live/merch",
                "segment": "vip_buyers",
                "datetime_sent": "2025-08-19T17:00:00",
            },
            {
                "project_name": "festival_france",
                "title": "Votre billet pour demain",
                "message": "Consultez votre QR code et les portes d'entrée avant départ.",
                "redirection": "app://project/festival_france/tickets",
                "segment": "ticket_holders",
                "datetime_sent": "2025-06-13T18:00:00",
            },
        ]

    def get_similar_projects(
        self,
        project_name: str,
        event_category: str,
        country: str,
        language: str,
    ) -> list[dict[str, Any]]:
        similar = [
            project
            for project in self._projects
            if project["project_name"] != project_name
            and project["event_category"] == event_category
            and project["country"] == country
            and project["language"] == language
        ]

        if similar:
            return similar

        # Deterministic fallback if exact match is sparse in V1 mock data.
        return [
            project
            for project in self._projects
            if project["project_name"] != project_name and project["event_category"] == event_category
        ]

    def get_push_history(self, project_names: list[str]) -> list[dict[str, Any]]:
        name_set = set(project_names)
        return [push for push in self._pushes if push["project_name"] in name_set]
