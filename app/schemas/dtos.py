from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    username: str
    password: str


class UserRetrieve(BaseModel):
    """Schema for retrieving user information."""

    uuid: UUID
    username: str


class QuestionCreate(BaseModel):
    """Schema for creating a new question."""

    text: str


class AnswerCreate(BaseModel):
    """Schema for creating a new answer."""

    text: str


class AnswerRetrieve(BaseModel):
    """Schema for retrieving answer information."""

    id: int
    text: str
    user: UserRetrieve
    created_at: datetime


class QuestionRetrieve(BaseModel):
    """Schema for retrieving question information with answers."""

    id: int
    text: str
    created_at: datetime
    answers: list[AnswerRetrieve]


class Token(BaseModel):
    """Schema for authentication token."""

    access_token: str
