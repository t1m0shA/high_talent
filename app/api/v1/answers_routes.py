from sqlalchemy.orm import Session
from fastapi import Depends, status, APIRouter

from app.api.deps import get_current_user
from app.db import get_db
from app.errors import AnswerNotFoundApiError
from app.services import AnswerService
from app.schemas import AnswerRetrieve


router = APIRouter(prefix="/answers", tags=["Answers section."])


@router.get("/{id}", response_model=AnswerRetrieve)
def get_answer(id: int, db: Session = Depends(get_db)):
    """Retrieve an answer by its ID."""

    service = AnswerService(db)
    return service.get_answer(id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(
    id: int,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user),
):
    """Delete an answer if the current user is the author."""

    service = AnswerService(db)
    answer_schema = service.get_answer(id)

    if answer_schema.user.username != username:
        raise AnswerNotFoundApiError(text=f"Answer {id} not found.")

    return service.delete_answer(id)
