from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskStatus(str, Enum):
    TODO = "to_do"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


MAX_TAGS = 5
MAX_TAG_LENGTH = 20


def _normalize_tags(value: Any) -> list[str]:
    """Normalize API tag input while keeping validation strict and predictable."""
    if value is None:
        return []

    if isinstance(value, str):
        raw_tags = value.split(",")
    elif isinstance(value, list):
        raw_tags = value
    else:
        raise ValueError("tags must be a list of strings or a comma-separated string")

    normalized: list[str] = []
    seen: set[str] = set()
    for raw in raw_tags:
        if not isinstance(raw, str):
            raise ValueError("each tag must be a string")
        tag = raw.strip()
        if not tag:
            raise ValueError("tags cannot contain empty values")
        if len(tag) > MAX_TAG_LENGTH:
            raise ValueError(f"each tag must be {MAX_TAG_LENGTH} characters or fewer")
        key = tag.lower()
        if key not in seen:
            normalized.append(tag)
            seen.add(key)

    if len(normalized) > MAX_TAGS:
        raise ValueError(f"a task can have at most {MAX_TAGS} tags")

    return normalized


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: str = ""
    due_date: date | None = None
    tags: list[str] = Field(default_factory=list)

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str) -> str:
        title = value.strip()
        if not title:
            raise ValueError("title cannot be blank")
        return title

    @field_validator("description", "assignee", mode="before")
    @classmethod
    def trim_optional_strings(cls, value: Any) -> str:
        if value is None:
            return ""
        if not isinstance(value, str):
            raise ValueError("value must be a string")
        return value.strip()

    @field_validator("tags", mode="before")
    @classmethod
    def validate_tags(cls, value: Any) -> list[str]:
        return _normalize_tags(value)


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = None
    description: str = None
    status: TaskStatus = None
    priority: TaskPriority = None
    assignee: str = None
    due_date: date | None = None
    tags: list[str] = None

    @field_validator("title")
    @classmethod
    def updated_title_must_not_be_blank(cls, value: str) -> str:
        title = value.strip()
        if not title:
            raise ValueError("title cannot be blank")
        return title

    @field_validator("description", "assignee", mode="before")
    @classmethod
    def trim_optional_update_strings(cls, value: Any) -> str:
        if not isinstance(value, str):
            raise ValueError("value must be a string")
        return value.strip()

    @field_validator("tags", mode="before")
    @classmethod
    def validate_update_tags(cls, value: Any) -> list[str]:
        if value is None:
            raise ValueError("tags cannot be null")
        return _normalize_tags(value)


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: str
    due_date: date | None
    tags: list[str]
    created_at: datetime
    updated_at: datetime
    is_overdue: bool
