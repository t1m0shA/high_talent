from pydantic import BaseModel, field_validator
from uuid import UUID
from datetime import datetime


class UserCreate(BaseModel):

    username: str
    password: str


class UserRetrieve(BaseModel):

    uuid: UUID
    username: str


class QuestionCreate(BaseModel):

    text: str


class AnswerCreate(BaseModel):

    text: str


class AnswerRetrieve(BaseModel):

    id: int
    text: str
    user: UserRetrieve
    created_at: datetime


class QuestionRetrieve(BaseModel):

    id: int
    text: str
    created_at: datetime
    answers: list[AnswerRetrieve]


class Token(BaseModel):

    access_token: str
