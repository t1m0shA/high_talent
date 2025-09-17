from sqlalchemy.orm import Session
from app.db.session import get_db
from app.errors import UserAuthError, UserSchemaError, AnswerSchemaError
from app.services.question import QuestionService
from app.services.answer import AnswerService
from app.services.auth import AuthService
from app.schemas import AnswerRetrieve
from fastapi import Depends, status, APIRouter
from app.api.deps import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime

router = APIRouter(prefix="/answers", tags=["Answers section."])


@router.get("/{id}", response_model=AnswerRetrieve)
def get_answer(id: int, db: Session = Depends(get_db)):

    service = AnswerService(db)
    return service.get_answer(id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(
    id: int,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user),
):
    service = AnswerService(db)
    answer_schema = service.get_answer(id)

    if answer_schema.user.username != username:
        raise AnswerSchemaError(text=f"Answer {id} not found.", status=404)

    return service.delete_answer(id)
