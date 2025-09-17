from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from datetime import datetime
from typing import List, Optional
from app.db.models import Question as QuestionModel
from app.schemas import Question as QuestionSchema, Answer as AnswerSchema
from app.errors import QuestionSchemaError


class QuestionService:

    def __init__(self, db: Session):

        self.db = db

    def create_question(self, question: QuestionSchema) -> QuestionSchema:

        db_question = QuestionModel(text=question.text, created_at=question.created_at)

        self.db.add(db_question)
        self.db.commit()
        self.db.refresh(db_question)

        return self._to_schema(db_question)

    def get_question(self, question_id: int) -> QuestionSchema:

        question = (
            self.db.query(QuestionModel).filter(QuestionModel.id == question_id).first()
        )

        if not question:
            raise QuestionSchemaError(
                status=404, text=f"Question {question_id} not found."
            )

        return self._to_schema(question)

    def list_questions(self) -> List[QuestionSchema]:

        questions = self.db.query(QuestionModel).all()
        return [self._to_schema(q) for q in questions]

    def delete_question(self, question_id: int) -> None:

        question = (
            self.db.query(QuestionModel).filter(QuestionModel.id == question_id).first()
        )

        if not question:
            raise QuestionSchemaError(
                status=404, text=f"Question {question_id} not found."
            )

        self.db.delete(question)
        self.db.commit()

    def _to_schema(self, model: QuestionModel) -> QuestionSchema:

        return QuestionSchema.model_validate(model)
