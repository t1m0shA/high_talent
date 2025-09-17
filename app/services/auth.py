from sqlalchemy.orm import Session
from app.db.repositories import UserRepository
from app.schemas import UserCreate
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

    def register_user(self, user_data: UserCreate):

        hashed = get_password_hash(user_data.password)
        return self.repo.create(username=user_data.username, password_hash=hashed)

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
