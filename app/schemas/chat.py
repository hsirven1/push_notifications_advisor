from datetime import date

from pydantic import BaseModel, Field


class ProjectContext(BaseModel):
    project_name: str = Field(description="Current project identifier/name")
    event_category: str = Field(description="Category such as concert, sports, conference")
    country: str = Field(description="Country code or country name")
    start_date: date = Field(description="Project start date")
    end_date: date = Field(description="Project end date")
    language: str = Field(description="Primary language for notifications")


class ChatRequest(BaseModel):
    tenant_id: str = Field(description="Tenant identifier for data isolation")
    user_message: str = Field(description="Planner question for advisory")
    project_context: ProjectContext


class TimingPattern(BaseModel):
    days_before_event_start: int
    days_before_event_end: int
    send_weekday: str
    send_hour_local: int


class PushSuggestion(BaseModel):
    title: str
    message: str
    segment: str
    redirection: str


class PatternRecommendation(BaseModel):
    recommended_segment: str
    recommended_redirection: str
    recommended_timing: TimingPattern
    suggested_push_examples: list[PushSuggestion]
    rationale: str


class ChatResponse(BaseModel):
    answer: str
    recommendation: PatternRecommendation
