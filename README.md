# Task Tracker — Mid-Course Project

This repository contains a reconstructed Module 1–3 Task Tracker baseline plus the Mid-Course Project feature extension sprint.

## Submission note

The original local Task Tracker repository was not available, so the baseline was reconstructed from the course transcripts and module requirements before the mid-course sprint was completed. The submitted work is still organized as a normal Task Tracker repository and should be pushed on a branch named `mid-course-project`.

## Implemented mid-course features

1. **Due dates + overdue filter**
   - `due_date` is optional on create and update.
   - Invalid date formats return HTTP 422.
   - Backend computes `is_overdue` when `due_date` is before today and the task is not `done`.
   - Frontend shows due date / overdue pill on task cards.
   - Frontend includes an overdue-only filter.

2. **Tags / labels**
   - `tags` is a validated list.
   - Tags are trimmed, deduplicated case-insensitively, limited to 5 tags, and limited to 20 characters each.
   - Empty tag values are rejected.
   - Frontend modal accepts comma-separated tags.
   - Frontend renders tag chips on cards.
   - Frontend includes tag filtering.

## Backend behavior

The backend uses Python FastAPI, Pydantic validation, and an in-memory storage layer.

Core routes:

- `GET /health`
- `POST /tasks`
- `GET /tasks`
- `GET /tasks/{task_id}`
- `PATCH /tasks/{task_id}`
- `DELETE /tasks/{task_id}`

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

## How to run the backend

```bash
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
# .venv\Scripts\activate       # Windows PowerShell
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open the API docs:

```text
http://localhost:8000/docs
```

## How to open the frontend

In a second terminal:

```bash
cd frontend
python -m http.server 5173
```

Open:

```text
http://localhost:5173
```

The frontend calls the backend at `http://localhost:8000`.

## How to run tests

```bash
python -m pytest -q
```

Current verified result:

```text
14 passed
```

## Recommended GitHub submission steps

```bash
git init -b mid-course-project
git add .
git commit -m "Complete mid-course feature extension sprint"
git remote add origin <your-public-github-repo-url>
git push -u origin mid-course-project
```

Before submitting, confirm the GitHub repository is public and that this branch is selected.

## Documentation

Required project documentation is in:

```text
docs/midcourse/
```

Included files:

- `user-stories.md`
- `mini-adr.md`
- `prompt-log.md`
- `verification.md`
- `reflection.md`
