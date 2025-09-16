from typing import Generator, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.db.base import DATABASE_URL


engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, Any, None]:

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
