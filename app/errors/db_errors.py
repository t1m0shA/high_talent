from app.errors.base import BaseError


class QuestionNotFoundDbError(BaseError):

    text = "Question not found."
    status = 404


class AnswerNotFoundDbError(BaseError):

    text = "Answer not found."
    status = 404
