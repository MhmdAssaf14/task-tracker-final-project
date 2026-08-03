from __future__ import annotations

from datetime import UTC, datetime

from fastapi import FastAPI, HTTPException, Query, Response, status
from fastapi.middleware.cors import CORSMiddleware

from app.business_rules import is_valid_status_transition
from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate
from app.storage import add_task, delete_task, get_task, list_tasks, reset_tasks, update_task

app = FastAPI(title="Task Tracker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "timestamp": datetime.now(UTC).isoformat()}


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate) -> TaskResponse:
    return add_task(task)


@app.get("/tasks", response_model=list[TaskResponse])
def read_tasks(
    status_filter: TaskStatus | None = Query(default=None, alias="status"),
    priority: TaskPriority | None = None,
    tag: str | None = Query(default=None, min_length=1),
    overdue: bool | None = None,
) -> list[TaskResponse]:
    if tag is not None and not tag.strip():
        raise HTTPException(status_code=422, detail="tag filter cannot be blank")
    return list_tasks(status=status_filter, priority=priority, tag=tag, overdue=overdue)


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: int) -> TaskResponse:
    task = get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def patch_task(task_id: int, task_update: TaskUpdate) -> TaskResponse:
    existing = get_task(task_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Task not found")

    update_fields = task_update.model_dump(exclude_unset=True)
    if "status" in update_fields:
        new_status = update_fields["status"]
        if not is_valid_status_transition(existing.status, new_status):
            raise HTTPException(
                status_code=422,
                detail=f"Status transition from {existing.status.value} to {new_status.value} is not allowed",
            )

    updated = update_task(task_id, task_update)
    if updated is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_task(task_id: int) -> Response:
    deleted = delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/test/reset", include_in_schema=False)
def reset_for_tests() -> dict[str, str]:
    reset_tasks()
    return {"status": "reset"}
