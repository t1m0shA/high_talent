from sqlalchemy.orm import Session
from datetime import timedelta
from uuid import UUID

from app.schemas import User
from app.errors import UserNotFoundServiceError
from app.core import settings
from app.db import UserRepository
from app.core import (
    get_password_hash,
    verify_password,
    create_access_token,
)


class AuthService:
    """Service for user authentication, registration, and token management."""

    def __init__(self, db: Session):

        self.repo = UserRepository(db)

    def register_user(self, user_schema: User):

        hashed = get_password_hash(user_schema.password)
        return self.repo.create(username=user_schema.username, password_hash=hashed)

    def authenticate_user(self, username: str, password: str):

        user = self.repo.get_by_username(username)
        if not user or not verify_password(password, user.password_hash):
            return None
        return user

    def create_user_token(self, user_id: UUID, username: str):

        return create_access_token(
            {"sub": str(user_id), "username": username},
            expires_delta=timedelta(minutes=settings.access_token_expire),
        )

    def get_by_username(self, username: str) -> User:

        user_model = self.repo.get_by_username(username)

        if not user_model:
            raise UserNotFoundServiceError(text=f"User {username} not found.")

        return User.model_validate(user_model)
