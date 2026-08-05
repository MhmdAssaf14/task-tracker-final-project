# AGENTS.md — Task Tracker AI Guardrails

## Project stack

- Backend: Python 3.11, FastAPI, Pydantic v2, in-memory storage.
- Frontend: static HTML, CSS, and vanilla JavaScript Kanban board.
- Tests: pytest with FastAPI `TestClient`.
- Release support: GitHub Actions CI and Docker.

## Read first

Before suggesting edits, read these files first:

1. `README.md`
2. `app/models.py`
3. `app/main.py`
4. `app/storage.py`
5. `app/business_rules.py`
6. `tests/`
7. `docs/release-evidence.md`
8. `docs/final-ai-review.md`

Do not assume the project uses authentication, a production database, user accounts, multi-tenancy, real-time updates, or a frontend framework. Those are outside the course scope.

## Run and test commands

Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the API locally:

```bash
python -m uvicorn app.main:app --reload --port 8000
```

Run the frontend locally:

```bash
cd frontend
python -m http.server 5173
```

Run tests:

```bash
python -m pytest -q
```

Run with Docker:

```bash
docker build -t task-tracker-final .
docker run --rm -p 8000:8000 task-tracker-final
curl -i http://localhost:8000/health
```

## Project rules

- Do not add new product features for the final project.
- Do not add authentication, comments, notifications, a production database, or unrelated UI polish.
- Do not change `app/` or `frontend/` unless the change is a small bug fix, security fix, or documentation-supported correction.
- If `app/` or `frontend/` changes, explain the reason in `docs/final-ai-review.md`.
- Preserve the existing API contract unless the change is explicitly documented and tested.
- Keep status values exactly: `to_do`, `in_progress`, `done`.
- Keep priority values exactly: `low`, `medium`, `high`.
- Never skip pytest, hide failing tests, or use CI shortcuts such as `continue-on-error` or `|| true`.

## Security and data rules

- Never paste or commit real secrets, credentials, `.env` files, access tokens, production logs, or personal/customer data.
- Use `.env.example` only for non-secret sample values.
- Treat AI output as a draft. Review diffs, run tests, and record important accepted/rejected decisions.
- If an AI suggestion cannot be explained by the maintainer, reject it.
