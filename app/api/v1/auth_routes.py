from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas import User
from app.db import get_db
from app.errors import UserUsernameTakenError, UserInvalidCredentialsError
from app.services import AuthService
from app.schemas import UserCreate, UserRetrieve, Token


router = APIRouter(
    prefix="/auth", tags=["Auth section. Log in with Authorize button above."]
)


@router.post(
    "/register",
    response_model=UserRetrieve,
    description="Try it out -> Edit username and password below.",
    summary="Register a new user with username and password.",
)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user with a username and password."""

    user_schema = User(username=user.username, password=user.password)

    service = AuthService(db)
    existing = service.repo.get_by_username(user_schema.username)

    if existing:
        raise UserUsernameTakenError(text="This username is already in use")

    return service.register_user(user_schema)


@router.post("/login", response_model=Token, include_in_schema=False)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """Authenticate user and return an access token."""

    service = AuthService(db)
    user_schema = User(username=form_data.username, password=form_data.password)
    db_user = service.authenticate_user(user_schema.username, user_schema.password)

    if not db_user:
        raise UserInvalidCredentialsError()

    token = service.create_user_token(user_schema.uuid, user_schema.username)
    return Token(access_token=token)
