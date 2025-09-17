from sqlalchemy.orm import Session
from app.db.repositories import UserRepository
from app.schemas import User
from app.errors import UserSchemaError
from datetime import timedelta
from app.core.config import settings
from uuid import UUID
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
)


class AuthService:

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
            raise UserSchemaError(text="User {username} not found.", status=404)

        return User.model_validate(user_model)
