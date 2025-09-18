from sqlalchemy.orm import Session
from typing import List

from app.db import Question as QuestionModel, QuestionRepository
from app.schemas import Question as QuestionSchema
from app.errors import QuestionNotFoundServiceError


class QuestionService:
    """Service for managing questions and related operations."""

    def __init__(self, db: Session):

        self.repo = QuestionRepository(db)

    def create_question(self, question: QuestionSchema) -> QuestionSchema:

        db_question = self.repo.create(question)
        return self._to_schema(db_question)

    def get_question(self, question_id: int) -> QuestionSchema:

        question = self.repo.get_by_id(question_id)

        if not question:
            raise QuestionNotFoundServiceError(
                text=f"Question {question_id} not found."
            )

        return self._to_schema(question)

    def list_questions(self) -> List[QuestionSchema]:

        questions = self.repo.list_all()
        return [self._to_schema(q) for q in questions]

    def delete_question(self, question_id: int) -> None:

        return self.repo.delete(question_id)

    def _to_schema(self, model: QuestionModel) -> QuestionSchema:

        return QuestionSchema.model_validate(model)
