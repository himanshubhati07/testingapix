<<<<<<< HEAD
# Database configuration and session management.
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

load_dotenv('.env_c517696b-c1ad-4fbe-ac2d-9f27763c2096', override=True)

DEFAULT_DB_URL = "postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_88bf58417e"
=======
# Database configuration and session management
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

load_dotenv('.env_d3b2dbc6-eb80-47a1-8fc6-6d72dad7f2f6', override=True)

DEFAULT_DB_URL = "postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_6511e82291"
>>>>>>> origin/main


def _to_async_url(url: str) -> str:
    if url.startswith("postgresql+asyncpg://"):
        return url
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url


DATABASE_URL = _to_async_url(os.getenv("DATABASE_URL", DEFAULT_DB_URL))

engine = create_async_engine(
    DATABASE_URL,
<<<<<<< HEAD
    echo=False,
=======
>>>>>>> origin/main
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=10,
)

<<<<<<< HEAD
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
=======
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
>>>>>>> origin/main


class Base(DeclarativeBase):
    pass


async def get_db():
<<<<<<< HEAD
    async with async_session() as session:
=======
    async with SessionLocal() as session:
>>>>>>> origin/main
        yield session
