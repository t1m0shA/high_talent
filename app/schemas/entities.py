from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime
from uuid import uuid4
from typing import Optional
from app.errors import AnswerSchemaError, QuestionSchemaError, UserSchemaError
from uuid import UUID


class User(BaseModel):

    uuid: UUID = Field(default_factory=uuid4)
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:

        if not v.strip():
            raise UserSchemaError("Username cannot be empty.")
        if len(v) < 3:
            raise UserSchemaError("Username must contain at least 3 characters.")

        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:

        if not v.strip():
            raise UserSchemaError("Password cannot be empty.")

        return v


class Answer(BaseModel):

    id: Optional[int] = None
    text: str
    user: User
    created_at: datetime

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:

        if len(v) > 0:
            return v

        raise AnswerSchemaError(text="Answer must not be empty.")


class Question(BaseModel):

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

        raise QuestionSchemaError(text="Question must not be empty.")
