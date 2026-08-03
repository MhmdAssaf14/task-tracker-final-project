# Mini ADR — Mid-Course Feature Extension

## Decision

I implemented two small end-to-end features: **Due dates + overdue filter** and **Tags / labels**. Both are visible in the frontend and both are supported by backend validation and pytest coverage.

The backend remains a simple FastAPI app with Pydantic models and in-memory storage. I added `due_date`, `tags`, and computed `is_overdue` to the task contract. I kept the existing task fields and status-transition business rules intact. The frontend remains a vanilla JavaScript Kanban board with a modal form and compact filters above the board.

## Alternatives AI suggested

AI suggested several alternatives:

1. Add a database table or persistence layer for tags and comments.
2. Store tags as a comma-separated string in the task record.
3. Compute overdue status only in the frontend.
4. Add comments or an activity log as the second feature.

## Rejected options

I rejected database changes because they were too large for a 3–4 hour mid-course sprint and would distract from the course goal of controlled AI-assisted development. I rejected comma-separated tag storage because it makes filtering and validation weaker. I rejected frontend-only overdue logic because backend tests should prove the overdue contract. I rejected comments and activity log because they introduce additional routes, nested resources, and more UI state than needed.

## Consequences

This design keeps the scope small but still demonstrates full-stack change ownership. The new fields are validated at the API boundary, rendered in the UI, and covered by targeted tests. The main limitation is that storage is still in memory, so data resets when the backend restarts. That is acceptable for this learning project and consistent with the baseline scope.
