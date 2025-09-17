from app.errors.base import BaseError


class QuestionNotFoundServiceError(BaseError):

    text = "Question not found."
    status = 404


class AnswerNotFoundServiceError(BaseError):

    text = "Answer not found."
    status = 404


class UserNotFoundServiceError(BaseError):

    text = "User not found."
    status = 404
