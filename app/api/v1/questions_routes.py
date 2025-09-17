from sqlalchemy.orm import Session
from app.db.session import get_db
from app.errors import UserAuthError, UserSchemaError
from app.services.question import QuestionService
from app.schemas import Question, QuestionCreate, QuestionRetrieve
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
