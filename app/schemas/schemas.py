from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime
from uuid import uuid4, UUID
from typing import Optional

from app.errors import (
    QuestionEmptyError,
    UserEmptyUsernameError,
    UserEmptyPasswordError,
    AnswerEmptyError,
)


class User(BaseModel):
    """Schema for user data and validation."""

    model_config = ConfigDict(from_attributes=True)

    uuid: UUID = Field(default_factory=uuid4)
    username: str
    password: Optional[str] = None

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:

        if not v.strip():
            raise UserEmptyUsernameError()
        if len(v) < 3:
            raise UserEmptyUsernameError("Username must contain at least 3 characters.")

        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:

        if v is not None and not v.strip():
            raise UserEmptyPasswordError()

        return v


class Answer(BaseModel):
    """Schema for answer data and validation."""

    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    text: str
    user: User
    created_at: datetime

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:

        if len(v) > 0:
            return v

        raise AnswerEmptyError()


class Question(BaseModel):
    """Schema for question data and validation."""

    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    text: str
    created_at: datetime
    answers: list[Answer]

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:

        if len(v) > 0:
            return v

        raise QuestionEmptyError()
