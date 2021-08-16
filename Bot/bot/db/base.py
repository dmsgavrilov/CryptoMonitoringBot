from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from bot.config import settings

SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, max_overflow=settings.SQLALCHEMY_MAX_OVERFLOW,
    pool_size=settings.SQLALCHEMY_POOL_SIZE, pool_timeout=settings.SQLALCHEMY_POOL_TIMEOUT
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
