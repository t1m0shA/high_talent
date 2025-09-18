from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError

from app.core import decode_access_token
from app.errors import UserInvalidCredentialsError, UserApiError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """Retrieve the current user's username from the JWT token."""

    try:

        payload = decode_access_token(token)

        username: str = payload.get("username")
        if username is None:
            raise UserInvalidCredentialsError()

        return username

    except PyJWTError as exc:

        raise UserApiError(text=str(exc))
