from pydantic import BaseModel, field_validator
from uuid import UUID
from datetime import datetime
from app.schemas.entities import Question
from app.errors import UserSchemaError


class UserCreate(BaseModel):

    username: str
    password: str


class UserRetrieve(BaseModel):

    uuid: UUID
    username: str


class QuestionCreate(BaseModel):

    text: str


class QuestionRetrieve(BaseModel):

    id: int
    text: str
    created_at: datetime


class AnswerCreate(BaseModel):

    text: str
    question_id: int


class AnswerRetrieve(BaseModel):

    id: int
    text: str
    question: QuestionRetrieve
    user: UserRetrieve
    created_at: datetime


class Token(BaseModel):

    access_token: str
