from src.core.settings import settings
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

def new_engine() -> Engine:
    return create_engine(settings.database_url, future=True)

def new_session(engine) -> Session:
    return sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
    autocommit=False,
    future=True,
)