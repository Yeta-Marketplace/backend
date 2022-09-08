from typing import Generator

from sqlmodel import create_engine, Session
from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator:
    """ Yields a Session object used to interact with db """
    with Session(engine) as session:
        yield session