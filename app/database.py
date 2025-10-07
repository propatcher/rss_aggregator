from sqlalchemy import NullPool, create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
    SYNC_DATABASE_URL = settings.TEST_SYNC_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    SYNC_DATABASE_URL = settings.SYNC_DATABASE_URL
    DATABASE_PARAMS = {}

engine = create_async_engine(url=DATABASE_URL, **DATABASE_PARAMS)

async_session = async_sessionmaker(engine, expire_on_commit=False)
    
sync_engine = create_engine(url=SYNC_DATABASE_URL, echo=False)

sync_session = sessionmaker(
    autocommit=False, autoflush=False, bind=sync_engine
)


Base = declarative_base()
