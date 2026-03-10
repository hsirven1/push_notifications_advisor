from __future__ import annotations

from pathlib import Path

from app.guardrails.tenant_isolation import TenantIsolationGuard
from app.guardrails.validator import RequestValidator
from app.schemas.chat import ChatRequest, ChatResponse, RecommendationPayload
from app.tools.recommendation_tools import RecommendationTools


class ChatService:
    """Service layer that orchestrates tool calls for recommendation responses."""

    def __init__(self, tools: RecommendationTools) -> None:
        self.tools = tools
        self.system_prompt = Path("app/prompts/chat_system_prompt.txt").read_text(encoding="utf-8")

    def get_recommendation(self, request: ChatRequest) -> ChatResponse:
        TenantIsolationGuard.assert_tenant_access(request.tenant_id)
        RequestValidator.validate_chat_request(request)

        similar_events = self.tools.get_similar_events(
            event_id=request.event_context.event_id,
            event_type=request.event_context.event_type,
            market=request.event_context.market,
            venue_size=request.event_context.venue_size,
        )
        similar_event_ids = [event["event_id"] for event in similar_events]

        filters = {"event_ids": similar_event_ids}
        best_pushes = self.tools.get_best_performing_pushes(filters)
        best_segments = self.tools.get_best_segments(filters)
        best_send_times = self.tools.get_best_send_times(filters)
        best_destinations = self.tools.get_best_destinations(filters)

        # Future LLM integration point:
        # 1) Build deterministic tool-context payload from best_* variables.
        # 2) Send prompt + context to OpenAI Responses/Chat API.
        # 3) Parse model output into RecommendationPayload.
        recommendation = self._build_rule_based_recommendation(
            best_pushes,
            best_segments,
            best_send_times,
            best_destinations,
        )

        answer = (
            "Based on similar events, this recommendation favors the highest-CTR content, "
            "segment, destination, and send window from historical pushes."
        )
        return ChatResponse(answer=answer, recommendation=recommendation)

    def _build_rule_based_recommendation(
        self,
        best_pushes: list[dict],
        best_segments: list[dict],
        best_send_times: list[dict],
        best_destinations: list[dict],
    ) -> RecommendationPayload:
        top_push = best_pushes[0] if best_pushes else {}
        top_segment = best_segments[0] if best_segments else {"segment": "ticket_holders"}
        top_time = best_send_times[0] if best_send_times else {"hour": 17}
        top_destination = best_destinations[0] if best_destinations else {"destination": "app://event/home"}

        return RecommendationPayload(
            push_content=top_push.get("content", "Event reminder: check your latest event updates."),
            target_segment=top_segment["segment"],
            destination=top_destination["destination"],
            send_window=f"{top_time['hour']:02d}:00-{(top_time['hour'] + 1) % 24:02d}:00 local time",
            rationale=(
                "Selected from top historical CTR results among similar events "
                "for content, segment, destination, and send hour."
            ),
        )
