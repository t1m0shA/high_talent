from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.question import QuestionService
from app.services.answer import AnswerService
from app.services.auth import AuthService
from app.api.deps import get_current_user
from uuid import UUID
from app.schemas import (
    Question,
    QuestionCreate,
    QuestionRetrieve,
    Answer,
    User,
    AnswerCreate,
    AnswerRetrieve,
)
from fastapi import Depends, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime

router = APIRouter(prefix="/questions", tags=["Questions section."])


@router.post("/", response_model=QuestionRetrieve, status_code=status.HTTP_201_CREATED)
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):

    question_entity = Question(
        text=question.text, created_at=datetime.now(), answers=[]
    )

    service = QuestionService(db)
    created = service.create_question(question_entity)

    return created


@router.get("/", response_model=list[QuestionRetrieve])
def list_questions(db: Session = Depends(get_db)):

    service = QuestionService(db)
    questions = service.list_questions()

    return questions


@router.get("/{id}", response_model=QuestionRetrieve)
def get_question(id: int, db: Session = Depends(get_db)):

    service = QuestionService(db)
    question = service.get_question(id)

    return question


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(id: int, db: Session = Depends(get_db)):

    service = QuestionService(db)
    return service.delete_question(id)


@router.post(
    "/{id}/answers",
    response_model=AnswerRetrieve,
    status_code=status.HTTP_201_CREATED,
)
def create_answer(
    id: int,
    answer: AnswerCreate,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user),
):
    question_service = QuestionService(db)
    question_entity = question_service.get_question(id)

    auth_service = AuthService(db)
    user_entity = auth_service.get_by_username(username)

    answer_entity = Answer(
        text=answer.text, user=user_entity, created_at=datetime.now()
    )

    answer_service = AnswerService(db)
    created = answer_service.create_answer(question_entity.id, answer_entity)

    return created
