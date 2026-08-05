from app.models import TaskStatus

VALID_STATUS_TRANSITIONS: frozenset[tuple[TaskStatus, TaskStatus]] = frozenset(
    {
        (TaskStatus.TODO, TaskStatus.IN_PROGRESS),
        (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
        (TaskStatus.DONE, TaskStatus.IN_PROGRESS),
    }
)


def is_valid_status_transition(current: TaskStatus, new_status: TaskStatus) -> bool:
    return (current, new_status) in VALID_STATUS_TRANSITIONS
