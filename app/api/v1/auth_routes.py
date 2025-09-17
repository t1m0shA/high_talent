from sqlalchemy.orm import Session
from app.db.session import get_db
from app.errors import UserAuthError, UserSchemaError
from app.services.auth import AuthService
from app.schemas import UserCreate, UserRetrieve, Token
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm


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

    if not user.username:
        raise UserSchemaError(text="The username cannot be empty")
    if not user.password:
        raise UserSchemaError(text="The password cannot be blank")

    service = AuthService(db)
    existing = service.repo.get_by_username(user.username)

    if existing:
        raise UserAuthError(text="This username is already in use", status=400)

    return service.register_user(user)


@router.post("/login", response_model=Token, include_in_schema=False)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):

    service = AuthService(db)
    db_user = service.authenticate_user(form_data.username, form_data.password)

    if not db_user:
        raise UserAuthError(text="Invalid credentials")

    token = service.create_user_token(db_user.uuid, db_user.username)
    return Token(access_token=token)
