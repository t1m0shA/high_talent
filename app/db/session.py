from typing import Generator, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.db import DATABASE_URL


engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, Any, None]:
    """Yield a database session and ensure it is closed after use."""

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
