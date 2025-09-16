import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy import UUID
from app.db.base import Base
from datetime import datetime
from sqlalchemy.orm import relationship


class User(Base):

    __tablename__ = "users"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)


class Answer(Base):

    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="CASCADE"),
        nullable=False,
    )
    question_id = Column(
        Integer,
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    user = relationship(User, backref="answers")
    question = relationship("Question", backref="answers")


class Question(Base):

    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    answers = relationship(Answer, backref="question", cascade="all, delete-orphan")
