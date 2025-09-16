from app.errors.base import BaseError


class QuestionError(BaseError):

    text = "Question error occured."
    status = 400


class AnswerError(BaseError):

    text = "Answer error occured."
    status = 400


class UserError(BaseError):

    text = "User error occured."
    status = 401
