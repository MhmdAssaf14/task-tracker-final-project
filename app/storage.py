from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any

from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate

_tasks: dict[int, dict[str, Any]] = {}
_next_id = 1

_PRIORITY_ORDER = {
    TaskPriority.HIGH: 0,
    TaskPriority.MEDIUM: 1,
    TaskPriority.LOW: 2,
}


def _now() -> datetime:
    return datetime.now(UTC)


def _is_overdue(record: dict[str, Any]) -> bool:
    due_date = record.get("due_date")
    return bool(due_date and due_date < date.today() and record["status"] != TaskStatus.DONE)


def _to_response(record: dict[str, Any]) -> TaskResponse:
    return TaskResponse(**record, is_overdue=_is_overdue(record))


def reset_tasks() -> None:
    global _next_id
    _tasks.clear()
    _next_id = 1


def add_task(task: TaskCreate) -> TaskResponse:
    global _next_id
    timestamp = _now()
    record = task.model_dump()
    record.update({"id": _next_id, "created_at": timestamp, "updated_at": timestamp})
    _tasks[_next_id] = record
    _next_id += 1
    return _to_response(record)


def get_task(task_id: int) -> TaskResponse | None:
    record = _tasks.get(task_id)
    if record is None:
        return None
    return _to_response(record)


def list_tasks(
    *,
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    tag: str | None = None,
    overdue: bool | None = None,
) -> list[TaskResponse]:
    normalized_tag = tag.strip().lower() if tag is not None else None
    records = list(_tasks.values())

    if status is not None:
        records = [record for record in records if record["status"] == status]

    if priority is not None:
        records = [record for record in records if record["priority"] == priority]

    if normalized_tag is not None:
        records = [
            record
            for record in records
            if any(existing.lower() == normalized_tag for existing in record.get("tags", []))
        ]

    if overdue is not None:
        records = [record for record in records if _is_overdue(record) is overdue]

    records.sort(key=lambda record: (_PRIORITY_ORDER[record["priority"]], record["created_at"]))
    return [_to_response(record) for record in records]


def update_task(task_id: int, update: TaskUpdate) -> TaskResponse | None:
    record = _tasks.get(task_id)
    if record is None:
        return None

    updates = update.model_dump(exclude_unset=True)
    if not updates:
        return _to_response(record)

    for field_name, value in updates.items():
        record[field_name] = value
    record["updated_at"] = _now()
    return _to_response(record)


def delete_task(task_id: int) -> bool:
    if task_id not in _tasks:
        return False
    del _tasks[task_id]
    return True
