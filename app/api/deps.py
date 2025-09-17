from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.errors import UserAuthError
from jwt import decode, PyJWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):

    try:

        payload = decode(
            token,
            str(settings.auth_secret_key),
            algorithms=[settings.auth_algorithm],
        )

        username: str = payload.get("sub")
        if username is None:
            raise UserAuthError(text="Invalid authentication credentials")

        return username

    except PyJWTError as exc:

        raise UserAuthError(text=str(exc))
