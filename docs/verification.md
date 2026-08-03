# Verification

## Baseline check before feature work

Because the original local repository was unavailable, I first reconstructed the Module 1–3 baseline behavior before implementing the mid-course features.

Baseline behavior verified:

- `GET /health` returns HTTP 200 and `status: ok`.
- `POST /tasks` creates a task with defaults.
- Blank title is rejected with HTTP 422.
- `GET /tasks` supports status and priority filters.
- Invalid status transition `to_do -> done` is rejected with HTTP 422.
- `DELETE /tasks/{id}` removes a task and later `GET` returns HTTP 404.

Baseline tests included in `tests/test_baseline_api.py`.

## Backend test results after feature work

Command:

```bash
python -m pytest -q
```

Result:

```text
..............                                                           [100%]
14 passed in 0.08s
```

The suite includes 6 baseline API tests and 8 mid-course feature tests.

## New mid-course tests

Due date / overdue tests:

- `test_create_task_with_valid_due_date`
- `test_invalid_due_date_format_is_rejected`
- `test_overdue_filter_returns_only_open_overdue_tasks`
- `test_update_due_date_changes_overdue_state`

Tags / labels tests:

- `test_create_task_with_tags_normalizes_values`
- `test_empty_tag_value_is_rejected`
- `test_filter_by_tag_is_case_insensitive`
- `test_update_tags_and_preserve_after_unrelated_update`

## Manual browser checks

Manual checks performed against the frontend at `http://localhost:5173` with backend running on `http://localhost:8000`:

1. Opened the board and confirmed three visible columns: To do, In progress, Done.
2. Created a task with title only and confirmed default status and priority.
3. Created a task with a future due date and tags; confirmed due date pill and tag chips appear on the card.
4. Created a past-due task and confirmed the overdue pill appears.
5. Enabled overdue-only filter and confirmed only overdue open tasks remain visible while all columns stay present.
6. Filtered by tag and confirmed only matching tagged tasks appear.
7. Edited a task title without changing status and confirmed tags were preserved.
8. Dragged a task from To do to Done and confirmed the UI rolled back after backend rejection.
9. Dragged a task from To do to In progress and confirmed the UI stayed updated after backend success.
10. Deleted a task from the edit modal and confirmed the card disappeared.

## Behavior contract before refactor

Before frontend cleanup, I defined this behavior contract:

- Board always renders the three columns.
- Empty columns show an empty state.
- Cards show title, status, priority, optional assignee, optional due date / overdue pill, and optional tag chips.
- Create modal requires title.
- Edit modal reuses the same form and pre-fills existing values.
- Drag/drop uses optimistic UI update but rolls back if the backend rejects the transition.
- Overdue and tag filters call the backend and do not filter only local stale data.
- Failed API responses appear as visible error messages.

## Behavior contract after refactor

After refactoring the frontend update path to send only changed fields, I rechecked the same contract. The important result was that normal edits no longer accidentally sent unchanged status values, while drag/drop status changes still used backend validation.

## Break Test evidence 1 — Overdue detection

Target test:

```bash
python -m pytest tests/test_midcourse_features.py::test_overdue_filter_returns_only_open_overdue_tasks -q
```

Intentional break:

```python
return False  # BREAK TEST: disables overdue detection
```

Expected failure observed:

```text
FAILED tests/test_midcourse_features.py::test_overdue_filter_returns_only_open_overdue_tasks
E       assert [] == [1]
```

Restored source behavior and reran the targeted test:

```text
1 passed in 0.03s
```

## Break Test evidence 2 — Empty tag validation

Target test:

```bash
python -m pytest tests/test_midcourse_features.py::test_empty_tag_value_is_rejected -q
```

Intentional break:

```python
if not tag:
    continue  # BREAK TEST: silently drop empty tags
```

Expected failure observed:

```text
FAILED tests/test_midcourse_features.py::test_empty_tag_value_is_rejected
E       assert 201 == 422
```

Restored source behavior and reran the targeted test:

```text
1 passed in 0.03s
```

## Final verification

After restoring both intentional Break Test changes, I ran the full suite again:

```text
14 passed in 0.08s
```
