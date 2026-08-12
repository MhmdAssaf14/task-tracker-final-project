# Task Tracker — Final Course Project

This repository contains the course Task Tracker: a FastAPI backend, a vanilla JavaScript Kanban frontend, pytest coverage, CI, Docker support, and evidence documents showing responsible AI-assisted development.

The original local Module 1–3 repository was unavailable during the mid-course checkpoint, so the baseline Task Tracker was reconstructed from course materials before the feature-extension sprint. The final project does **not** add new product features. It focuses on release readiness, documentation, security review, and ownership evidence.

## Final Project

Branch reviewed: `final-project`

### What this submission demonstrates

- The existing Task Tracker app still runs inside the intended course scope.
- CI runs the pytest suite on push and pull request.
- Docker image builds and runs with `/health` returning HTTP 200.
- AI review, security, and ownership evidence is stored in `docs/`.
- No authentication, production database, notifications, comments, or unrelated UI changes were added.

### How to run locally

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
# .venv\Scripts\activate       # Windows PowerShell
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the backend:

```bash
python -m uvicorn app.main:app --reload --port 8000
```

Check the API health endpoint:

```bash
curl -i http://localhost:8000/health
```

Open the API docs:

```text
http://localhost:8000/docs
```

Run the frontend in a second terminal:

```bash
cd frontend
python -m http.server 5173
```

Open:

```text
http://localhost:5173
```

The frontend calls the backend at `http://localhost:8000`.

### How to run tests

```bash
python -m pytest -q
```

Current local verification result recorded during final packaging:

```text
16 passed
```

### How to run with Docker

Build the image:

```bash
docker build -t task-tracker-final .
```

Run the container:

```bash
docker run --rm -p 8000:8000 task-tracker-final
```

Verify the running container:

```bash
curl -i http://localhost:8000/health
```

Expected result: HTTP 200 with a JSON body containing `"status":"ok"`.

### Evidence files

- `docs/release-evidence.md`
- `docs/final-ai-review.md`
- `docs/ai-playbook.md`
- `AGENTS.md`
- `.github/workflows/ci.yml`
- `Dockerfile`
- `.dockerignore`

### AI assistance summary

AI helped draft and review CI, Docker, documentation, security review notes, and final release evidence. I verified the work through pytest, a local `/health` check, manual diff review, and documentation claim-vs-reality checks. One AI suggestion I rejected was adding authentication or a production database during the final project, because the final brief explicitly says not to add new product features or expand scope.

## Existing Task Tracker behavior

Core routes:

- `GET /health`
- `POST /tasks`
- `GET /tasks`
- `GET /tasks/{task_id}`
- `PATCH /tasks/{task_id}`
- `DELETE /tasks/{task_id}`

Task fields:

- `title`
- `description`
- `status`
- `priority`
- `assignee`
- `due_date`
- `tags`
- `created_at`
- `updated_at`
- `is_overdue`

Supported `GET /tasks` filters:

- `status=to_do|in_progress|done`
- `priority=low|medium|high`
- `tag=<tag>`
- `overdue=true|false`

Status transition rules:

- Allowed: `to_do -> in_progress`
- Allowed: `in_progress -> done`
- Allowed: `done -> in_progress`
- Rejected: `to_do -> done`
- Rejected: `done -> to_do`
- Rejected: same-status transition attempts

## Mid-course documentation

The prior mid-course feature-extension evidence remains in:

```text
docs/midcourse/
```

Included files:

- `user-stories.md`
- `mini-adr.md`
- `prompt-log.md`
- `verification.md`
- `reflection.md`

## Recommended final submission steps

```bash
git checkout -b final-project
git add .
git commit -m "Complete final AI-assisted release evidence project"
git push -u origin final-project
```

After pushing, confirm the GitHub Actions workflow is green, then submit the public GitHub repository URL.
