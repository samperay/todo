from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

Priority = Literal["low", "medium", "high"]


def _required_title(value: str) -> str:
    stripped = value.strip()
    if not stripped:
        raise ValueError("Title is required")
    if len(stripped) > 200:
        raise ValueError("Title must be at most 200 characters")
    return stripped


def _optional_description(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    if not stripped:
        return None
    if len(stripped) > 2000:
        raise ValueError("Description must be at most 2000 characters")
    return stripped


class TodoCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    priority: Priority | None = None

    @model_validator(mode="after")
    def priority_cannot_be_null(self) -> "TodoCreate":
        if "priority" in self.model_fields_set and self.priority is None:
            raise ValueError("Priority is invalid")
        return self

    @field_validator("title")
    @classmethod
    def title_has_text(cls, value: str) -> str:
        return _required_title(value)

    @field_validator("description")
    @classmethod
    def description_or_none(cls, value: str | None) -> str | None:
        return _optional_description(value)


class TodoUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    priority: Priority | None = None

    @field_validator("title")
    @classmethod
    def title_has_text(cls, value: str | None) -> str | None:
        if value is None:
            raise ValueError("Title is required")
        return _required_title(value)

    @field_validator("description")
    @classmethod
    def description_or_none(cls, value: str | None) -> str | None:
        return _optional_description(value)

    @model_validator(mode="after")
    def at_least_one_field(self) -> "TodoUpdate":
        if "priority" in self.model_fields_set and self.priority is None:
            raise ValueError("Priority is invalid")
        if not self.model_fields_set:
            raise ValueError("At least one of title, description, or priority is required")
        return self


class TodoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str | None
    completed: bool
    priority: Priority
    created_at: datetime
    updated_at: datetime
