from app.errors.base import BaseError


class UserAuthError(BaseError):

    text = "User authentication error occured."
    status = 401
