# Prompt Log

## Weak prompt rewritten into a stronger prompt

### Weak prompt

> Add due dates and tags to my task tracker.

### Why it was weak

It did not identify files, field names, validation rules, frontend behavior, tests, or what not to change. It could easily cause scope creep or inconsistent backend/frontend contracts.

### Stronger prompt

> You are a senior FastAPI and vanilla JavaScript developer extending my existing Task Tracker. Use the current files `app/models.py`, `app/storage.py`, `app/main.py`, `frontend/index.html`, `frontend/app.js`, and `frontend/styles.css`. Add two scoped features only: optional `due_date` with backend-computed `is_overdue`, and `tags` as a validated list. Do not add authentication, a database, external frontend libraries, comments, activity log, or bulk operations. Preserve existing CRUD endpoints and status-transition business rules. Output small patches by layer: backend model/storage/API first, tests second, frontend last.

AI returned a controlled plan separating backend contract, pytest tests, and frontend integration. I accepted the small-step structure, edited the tag validation rules, and rejected extra features.

---

## Feature 1: Due dates + overdue filter

### Prompt 1.1 — Backend contract

> In `app/models.py` and `app/storage.py`, add optional `due_date` to create/update/response models. Compute `is_overdue` in the backend when a task has a due date before today and status is not `done`. Preserve all existing fields and status-transition behavior. Do not add a database or new routes yet. Show only the relevant code changes.

AI returned `due_date` as a Pydantic `date | None` field and an overdue helper in storage. I accepted the `date | None` approach and edited the overdue rule so completed tasks are never overdue.

### Prompt 1.2 — API filter

> In `app/main.py`, extend `GET /tasks` to support `overdue=true|false`. Keep existing `status` and `priority` filters. Invalid enum filters should still return HTTP 422 through FastAPI validation. Do not change route paths or response shape.

AI returned a query parameter and passed it into the storage list function. I accepted the route shape and edited naming so the `status` query alias stayed compatible with the existing API.

### Prompt 1.3 — Due date tests

> Write focused pytest tests for due dates: create with valid due date, reject invalid date format, update due date, and `overdue=true` returning only open overdue tasks. Use the existing TestClient fixture and one behavior per test. Do not write browser tests.

AI returned several tests. I accepted four and edited the overdue test to include a completed past-due task to prove the backend does not mark done tasks as overdue.

---

## Feature 2: Tags / labels

### Prompt 2.1 — Tag validation

> In `app/models.py`, add `tags` as a list of strings. Validate by trimming values, rejecting blank tags, removing duplicates case-insensitively, allowing at most 5 tags, and limiting each tag to 20 characters. Accept list input; optional support for comma-separated strings is okay. Do not store tags as one string.

AI initially suggested storing tags as comma-separated text. I rejected that assumption and kept the API contract as a list. I accepted the trimming and deduplication idea.

### Prompt 2.2 — Tag filtering

> Extend `GET /tasks` and the storage list function to support `tag=<value>`. The filter should be case-insensitive and should combine with existing status, priority, and overdue filters. Do not create a separate tags endpoint.

AI returned tag filtering in the list function. I accepted the case-insensitive comparison and edited the blank tag query handling so whitespace-only filters return HTTP 422.

### Prompt 2.3 — Frontend tags and due date UI

> Update the vanilla JavaScript frontend only. Add due date and tags to the modal, show due/overdue pills and tag chips on cards, and add an overdue checkbox plus tag filter above the board. Preserve the three Kanban columns, drag/drop rollback on failed PATCH, and empty states. Do not add frameworks.

AI returned a larger frontend patch. I accepted the UI fields and rejected unrelated animation/theme suggestions. I edited the update flow so the edit modal sends only changed fields, avoiding accidental same-status transition failures.

---

## Targeted correction prompts used

### Correction 1 — Same-status edit risk

> The edit modal is sending the unchanged `status` field during every PATCH. The backend correctly rejects same-status transitions. Change the frontend update path so it compares the original task with the form values and sends only changed fields.

Accepted. This prevented ordinary title/tag/due-date edits from being blocked by status-transition validation.

### Correction 2 — Empty tag bug

> The tag validator currently drops blank tags silently. That weakens the API contract. Change it so any blank tag in the provided list raises validation error and returns HTTP 422.

Accepted. I then used a Break Test to prove `test_empty_tag_value_is_rejected` catches this behavior.
