from app.errors.base import BaseError


class UserEmptyUsernameError(BaseError):

    text = "Username cannot be empty."
    status = 400


class UserEmptyPasswordError(BaseError):

    text = "Password cannot be blank."
    status = 400


class AnswerEmptyError(BaseError):

    text = "Answer must not be empty."
    status = 422


class QuestionEmptyError(BaseError):

    text = "Question must not be empty."
    status = 422
