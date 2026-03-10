from __future__ import annotations

from pathlib import Path

from app.guardrails.tenant_isolation import TenantIsolationGuard
from app.guardrails.validator import RequestValidator
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    PatternRecommendation,
    PushSuggestion,
    TimingPattern,
)
from app.tools.recommendation_tools import RecommendationTools


class ChatService:
    """Service layer that orchestrates deterministic pattern-based advisory responses."""

    def __init__(self, tools: RecommendationTools) -> None:
        self.tools = tools
        self.system_prompt = Path("app/prompts/chat_system_prompt.txt").read_text(encoding="utf-8")

    def get_recommendation(self, request: ChatRequest) -> ChatResponse:
        TenantIsolationGuard.assert_tenant_access(request.tenant_id)
        RequestValidator.validate_chat_request(request)

        context = request.project_context
        similar_projects = self.tools.get_similar_projects(
            project_name=context.project_name,
            event_category=context.event_category,
            country=context.country,
            language=context.language,
        )
        project_lookup = {project["project_name"]: project for project in similar_projects}
        similar_project_names = sorted(project_lookup.keys())

        push_history = self.tools.get_push_history(similar_project_names)
        segments = self.tools.get_common_segments(push_history)
        redirections = self.tools.get_common_redirections(push_history)
        timing_patterns = self.tools.get_timing_patterns(push_history, project_lookup)
        examples = self.tools.get_push_examples(push_history, limit=3)

        # Future LLM integration point:
        # 1) Build deterministic tool-context payload from similar project patterns.
        # 2) Send prompt + context to OpenAI API with strict tool-only orchestration.
        # 3) Parse model output into PatternRecommendation.
        recommendation = self._build_pattern_recommendation(segments, redirections, timing_patterns, examples)

        answer = (
            "Recommendation generated from recurring historical patterns in similar projects "
            "(event category, country, language)."
        )
        return ChatResponse(answer=answer, recommendation=recommendation)

    def _build_pattern_recommendation(
        self,
        segments: list[dict],
        redirections: list[dict],
        timing_patterns: list[dict],
        examples: list[dict],
    ) -> PatternRecommendation:
        top_segment = segments[0]["segment"] if segments else "ticket_holders"
        top_redirection = redirections[0]["redirection"] if redirections else "app://project/home"
        top_timing = timing_patterns[0] if timing_patterns else {
            "days_before_event_start": 1,
            "days_before_event_end": 1,
            "send_weekday": "Thursday",
            "send_hour_local": 18,
        }

        suggestion_models = [PushSuggestion(**example) for example in examples]
        if not suggestion_models:
            suggestion_models = [
                PushSuggestion(
                    title="Event reminder",
                    message="Your event is coming up. Open the app for entry details.",
                    segment=top_segment,
                    redirection=top_redirection,
                )
            ]

        return PatternRecommendation(
            recommended_segment=top_segment,
            recommended_redirection=top_redirection,
            recommended_timing=TimingPattern(
                days_before_event_start=top_timing["days_before_event_start"],
                days_before_event_end=top_timing["days_before_event_end"],
                send_weekday=top_timing["send_weekday"],
                send_hour_local=top_timing["send_hour_local"],
            ),
            suggested_push_examples=suggestion_models[:3],
            rationale=(
                "These choices reflect the most repeated segment, redirection, and send-time pattern "
                "found in similar historical projects."
            ),
        )
