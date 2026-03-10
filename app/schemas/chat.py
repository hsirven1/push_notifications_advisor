from pydantic import BaseModel, Field


class EventContext(BaseModel):
    event_id: str | None = Field(default=None)
    event_type: str = Field(description="Type of event, e.g. concert, sports, conference")
    market: str = Field(description="Geographic market")
    venue_size: int = Field(description="Venue capacity estimate")


class ChatRequest(BaseModel):
    tenant_id: str = Field(description="Tenant identifier for data isolation")
    user_message: str = Field(description="Planner question for push recommendation")
    event_context: EventContext


class RecommendationPayload(BaseModel):
    push_content: str
    target_segment: str
    destination: str
    send_window: str
    rationale: str


class ChatResponse(BaseModel):
    answer: str
    recommendation: RecommendationPayload
