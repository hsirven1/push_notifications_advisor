# Push Notification Advisor (V1 Foundation)

Minimal FastAPI backend scaffold for a recommendation assistant that advises event teams on what push notification to send.

## What V1 does
- Exposes a `GET /health` endpoint.
- Exposes a `POST /chat` endpoint (deterministic recommendation stub).
- Uses a service layer to orchestrate tool calls.
- Uses a data access layer (mock repository) for historical push data.
- Keeps prompt templates separate from business logic.
- Includes placeholder guardrails for validation and tenant isolation.

## What V1 does **not** do
- It does **not** send notifications.
- It does **not** allow the LLM to generate SQL.
- It does **not** include a production database yet (mock data only).

## Recommended folder structure

```text
app/
  api/
    dependencies.py
    routes/
      chat.py
      health.py
  config/
    settings.py
  data/
    repositories/
      base.py
      mock_repository.py
  guardrails/
    tenant_isolation.py
    validator.py
  prompts/
    chat_system_prompt.txt
  schemas/
    chat.py
  services/
    chat_service.py
  tools/
    recommendation_tools.py
  main.py
.env.example
requirements.txt
README.md
```

## Local setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy env file:

```bash
cp .env.example .env
```

4. Run locally:

```bash
uvicorn app.main:app --reload
```

## Quick API usage

### Health

```bash
curl http://127.0.0.1:8000/health
```

### Chat

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": "tenant_demo",
    "user_message": "What push should we send for tonight?",
    "event_context": {
      "event_id": "evt_200",
      "event_type": "concert",
      "market": "NYC",
      "venue_size": 11000
    }
  }'
```

## Mocked vs real in V1

Keep mocked in V1:
- `MockPushHistoryRepository` dataset and scoring assumptions.
- Rule-based response builder in `ChatService`.
- Guardrails are placeholders (basic checks only).

Replace with real components next:
- Add Postgres-backed repository implementing `PushHistoryRepository`.
- Add authentication + strict tenant partitioning checks.
- Plug OpenAI API into `ChatService` at the marked integration point, while keeping tool-calling constrained to backend functions.
- Add structured observability, retries, and evaluation tests.
