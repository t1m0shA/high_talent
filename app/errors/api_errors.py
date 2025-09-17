from app.errors.base import BaseError


class UserApiError(BaseError):

    text = "User processing error occured."
    status = 401


class UserUsernameTakenError(BaseError):

    text = "The username is already taken."
    status = 400


class UserInvalidCredentialsError(BaseError):

    text = "User authentication error occured: invalid credentials."
    status = 401


class AnswerNotFoundApiError(BaseError):

    text = "Answer not found."
    status = 404
