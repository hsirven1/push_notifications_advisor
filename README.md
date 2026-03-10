# Push Notification Advisor (V1 Foundation)

Minimal FastAPI backend scaffold for a recommendation assistant that advises event teams what push to prepare using recurring historical patterns from similar projects.

## Real data model used in V1

### Push fields
- `title`
- `message`
- `redirection`
- `segment`
- `datetime_sent`

### Project fields
- `project_name`
- `event_category`
- `country`
- `start_date`
- `end_date`
- `language`

V1 intentionally does **not** assume recipient count or any engagement outcome metrics.

## What V1 does
- Exposes a `GET /health` endpoint.
- Exposes a `POST /chat` endpoint with deterministic advisory output.
- Uses a service layer to orchestrate tool calls.
- Uses a data access layer (mock repository) for historical project/push data.
- Performs recurring-pattern analysis (frequency-based, deterministic).
- Computes derived timing fields:
  - `days_before_event_start`
  - `days_before_event_end`
  - `send_weekday`
  - `send_hour_local`
- Similarity is primarily based on:
  - `event_category`
  - `country`
  - `language`

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
    "user_message": "What push pattern should we use?",
    "project_context": {
      "project_name": "new_york_fall_live",
      "event_category": "concert",
      "country": "US",
      "start_date": "2025-10-12",
      "end_date": "2025-10-12",
      "language": "en"
    }
  }'
```

## Mocked vs real in V1

Keep mocked in V1:
- `MockPushHistoryRepository` dataset.
- Rule-based response builder in `ChatService`.
- Guardrails are placeholders (basic checks only).

Replace with real components next:
- Add Postgres-backed repository implementing `PushHistoryRepository`.
- Add authentication + strict tenant partitioning checks.
- Plug OpenAI API into `ChatService` at the marked integration point, while keeping orchestration constrained to backend business functions.
- Add structured observability and evaluation tests.
