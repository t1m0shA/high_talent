from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jwt import encode, decode
from app.core import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""

    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token with optional expiration."""

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
    """Decode a JWT access token and return its payload."""

    try:
        return decode(
            token, str(settings.auth_secret_key), algorithms=[settings.auth_algorithm]
        )
    except:
        return {}
