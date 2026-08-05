# User Stories

## Context

The original local Task Tracker repository was unavailable, so the baseline was reconstructed from the course transcripts and then extended on a dedicated mid-course project version. The reconstructed baseline keeps the Module 1–3 scope: FastAPI backend, simple frontend Kanban board, create/list/update/delete tasks, filtering, Pydantic validation, and status-transition business rules.

---

## Feature 1: Due dates + overdue filter

### Story 1.1 — Add a due date while creating a task

As a team member, I want to add an optional due date when creating a task so that I can track work against deadlines.

Acceptance criteria:

- Given a valid task title and a valid `YYYY-MM-DD` due date, the API creates the task and stores the due date.
- Given a valid task title without a due date, the API creates the task with `due_date` set to `null`.
- Given an invalid due date format, the API rejects the request with HTTP 422.

### Story 1.2 — Update a task due date

As a team member, I want to update a task due date so that changed deadlines are reflected in the tracker.

Acceptance criteria:

- Given an existing task, patching `due_date` with a valid date updates the task.
- Given an existing task, patching `due_date` to `null` clears the date.
- Given a missing task ID, the API returns HTTP 404.

### Story 1.3 — See overdue tasks on the board

As a team member, I want overdue tasks to be visually marked so that I can quickly identify delayed work.

Acceptance criteria:

- Given an open task with a due date before today, the response includes `is_overdue: true`.
- Given a completed task with a past due date, the response includes `is_overdue: false`.
- The frontend card shows an overdue pill when `is_overdue` is true.

### Story 1.4 — Filter overdue tasks

As a team member, I want to filter the board to overdue tasks so that I can focus on urgent follow-up.

Acceptance criteria:

- Given a mix of overdue, future, and completed tasks, `GET /tasks?overdue=true` returns only open overdue tasks.
- Given no overdue matches, the API returns HTTP 200 with an empty list.
- The frontend overdue filter updates the board without a page reload.

### Corrected AI assumption for Feature 1

The first AI draft treated overdue as a frontend-only calculation. I corrected this because tests are clearer and more reliable when the backend owns the `is_overdue` contract. The UI now displays the backend result instead of inventing its own rule.

---

## Feature 2: Tags / labels

### Story 2.1 — Create a task with tags

As a team member, I want to add tags to a task so that I can group related work.

Acceptance criteria:

- Given valid tags, the API stores them as a list.
- Tags are trimmed before storage.
- Duplicate tags are removed case-insensitively.

### Story 2.2 — Reject invalid tags

As a team member, I want invalid tag values rejected so that task data stays clean.

Acceptance criteria:

- Given a blank tag value, the API returns HTTP 422.
- Given more than 5 tags, the API returns HTTP 422.
- Given a tag longer than 20 characters, the API returns HTTP 422.

### Story 2.3 — Update task tags

As a team member, I want to edit tags on an existing task so that task labels stay accurate.

Acceptance criteria:

- Given an existing task, patching `tags` replaces the tag list.
- Given an unrelated update, existing tags are preserved.
- Given a missing task ID, the API returns HTTP 404.

### Story 2.4 — Filter tasks by tag

As a team member, I want to filter tasks by tag so that I can focus on one category of work.

Acceptance criteria:

- Given tasks with different tags, `GET /tasks?tag=api` returns only tasks tagged `api`.
- Tag filtering is case-insensitive.
- The frontend tag filter updates the Kanban board without hiding the columns.

### Corrected AI assumption for Feature 2

The first AI draft suggested storing tags as one comma-separated string. I rejected that because validation, filtering, and frontend chips are cleaner when the backend stores tags as a list. The frontend accepts comma-separated input, but the API contract remains a list.
