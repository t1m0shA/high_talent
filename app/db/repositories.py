from sqlalchemy.orm import Session
from app.db.models import User, Question, Answer
from app.schemas import Question as QuestionSchema, Answer as AnswerSchema
from app.errors import QuestionSchemaError, AnswerSchemaError
from datetime import datetime
from uuid import UUID


class UserRepository:

    def __init__(self, db: Session):

        self.db = db

    def get_by_uuid(self, user_uuid: UUID) -> User | None:

        return self.db.query(User).filter(User.uuid == user_uuid).first()

    def get_by_username(self, username: str) -> User | None:

        return self.db.query(User).filter(User.username == username).first()

    def create(self, username: str, password_hash: str) -> User:

        user = User(username=username, password_hash=password_hash)

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user


class QuestionRepository:

    def __init__(self, db: Session):

        self.db = db

    def get_by_id(self, question_id: int) -> Question | None:

        return self.db.query(Question).filter(Question.id == question_id).first()

    def create(self, question: QuestionSchema) -> Question:

        question = Question(text=question.text, created_at=question.created_at)

        self.db.add(question)
        self.db.commit()
        self.db.refresh(question)

        return question

    def delete(self, question_id: int) -> None:

        question = self.db.query(Question).filter(Question.id == question_id).first()

        if not question:
            raise QuestionSchemaError(
                status=404, text=f"Question {question_id} not found."
            )

        self.db.delete(question)
        self.db.commit()

    def list_all(self) -> list[Question]:

        return self.db.query(Question).all()


class AnswerRepository:

    def __init__(self, db: Session):

        self.db = db

    def get_by_id(self, answer_id: int) -> Answer | None:

        return self.db.query(Answer).filter(Answer.id == answer_id).first()

    def create(self, answer: AnswerSchema, question: QuestionSchema) -> Answer:

        answer = Answer(
            text=answer.text,
            user_id=answer.user.uuid,
            question_id=question.id,
            created_at=answer.created_at,
        )

        self.db.add(answer)
        self.db.commit()
        self.db.refresh(answer)

        return answer

    def delete(self, answer_id: int) -> None:

        answer = self.db.query(Answer).filter(Answer.id == answer_id).first()

        if not answer:
            raise AnswerSchemaError(status=404, text=f"Answer {answer_id} not found.")

        self.db.delete(answer)
        self.db.commit()
