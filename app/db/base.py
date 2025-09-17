from sqlalchemy.orm import declarative_base
from app.core.config import settings

Base = declarative_base()

DATABASE_URL = (
    f"postgresql+psycopg2://{settings.postgres_user}:{settings.postgres_password}"
    f"@{settings.postgres_host}:{settings.postgres_inner_port}/{settings.postgres_db}"
)
