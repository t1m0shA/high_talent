"""Custom errors"""

from app.errors.schema_errors import (
    UserEmptyUsernameError,
    UserEmptyPasswordError,
    AnswerEmptyError,
    QuestionEmptyError,
)
from app.errors.base import BaseError
from app.errors.api_errors import (
    UserInvalidCredentialsError,
    UserApiError,
    AnswerNotFoundApiError,
    UserUsernameTakenError,
)
from app.errors.db_errors import QuestionNotFoundDbError, AnswerNotFoundDbError
from app.errors.service_errors import (
    QuestionNotFoundServiceError,
    AnswerNotFoundServiceError,
    UserNotFoundServiceError,
)
