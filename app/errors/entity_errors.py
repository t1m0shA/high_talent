from app.errors.base import BaseError


class QuestionSchemaError(BaseError):

    text = "Question schema error occured."
    status = 400


class AnswerSchemaError(BaseError):

    text = "Answer schema error occured."
    status = 400


class UserSchemaError(BaseError):

    text = "User schema error occured."
    status = 400
