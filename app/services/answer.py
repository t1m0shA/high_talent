from sqlalchemy.orm import Session
from app.db.models import Question as QuestionModel, Answer as AnswerModel
from app.db.repositories import AnswerRepository, QuestionRepository
from app.schemas import Answer as AnswerSchema, Question as QuestionSchema
from app.errors import AnswerSchemaError, QuestionSchemaError


class AnswerService:

    def __init__(self, db: Session):

        self.repo = AnswerRepository(db)
        self.question_repo = QuestionRepository(db)

    def create_answer(self, question_id: int, answer: AnswerSchema) -> AnswerSchema:

        question = self.question_repo.get_by_id(question_id)
        if not question:
            raise QuestionSchemaError(
                status=404, text=f"Question {question_id} not found."
            )

        question_entity = QuestionSchema.model_validate(question)
        created = self.repo.create(answer, question_entity)

        return AnswerSchema(
            id=created.id,
            text=created.text,
            user=answer.user,
            created_at=created.created_at,
        )

    def get_answer(self, answer_id: int) -> AnswerSchema:

        answer = self.repo.get_by_id(answer_id)

        if not answer:
            raise AnswerSchemaError(status=404, text=f"Answer {answer_id} not found.")

        return AnswerSchema(
            id=answer.id,
            text=answer.text,
            user=answer.user,
            created_at=answer.created_at,
        )

    def delete_answer(self, answer_id: int) -> None:

        return self.repo.delete(answer_id)
