from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jwt import encode, decode
from app.core import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:

    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):

    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = encode(
        to_encode, str(settings.auth_secret_key), algorithm=settings.auth_algorithm
    )

    return encoded_jwt


def decode_access_token(token: str) -> dict:

    try:
        return decode(
            token, str(settings.auth_secret_key), algorithms=[settings.auth_algorithm]
        )
    except:
        return {}
