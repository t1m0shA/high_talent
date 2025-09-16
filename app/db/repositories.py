from sqlalchemy.orm import Session
from app.db.models import User, Question, Answer
from datetime import datetime
import uuid


class UserRepository:

    def __init__(self, db: Session):

        self.db = db

    def get_by_uuid(self, user_uuid: uuid.UUID) -> User | None:

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

    def create(self, text: str) -> Question:

        question = Question(text=text, created_at=datetime.now())
        self.db.add(question)
        self.db.commit()
        self.db.refresh(question)
        return question

    def list_all(self) -> list[Question]:

        return self.db.query(Question).all()


class AnswerRepository:

    def __init__(self, db: Session):

        self.db = db

    def get_by_id(self, answer_id: int) -> Answer | None:

        return self.db.query(Answer).filter(Answer.id == answer_id).first()

    def create(self, text: str, user_id, question_id) -> Answer:

        answer = Answer(
            text=text,
            user_id=user_id,
            question_id=question_id,
            created_at=datetime.now(),
        )
        self.db.add(answer)
        self.db.commit()
        self.db.refresh(answer)
        return answer

    def list_all(self) -> list[Answer]:

        return self.db.query(Answer).all()
