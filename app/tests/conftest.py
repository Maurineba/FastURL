import os
import pytest
from httpx import AsyncClient, ASGITransport

from sqlalchemy.ext.asyncio import (
   create_async_engine,
   AsyncSession,
   async_sessionmaker
)

from app.main import app
from app.db.base import Base
from app.db.deps import get_db

DATABASE_URL = os.getenv(
   "DATABASE_URL",
   "sqlite+aiosqlite:///./test.db"
)

engine_test = create_async_engine(
   DATABASE_URL,
   echo=False
)

AsyncSessionLocal = async_sessionmaker(
   bind=engine_test,
   class_=AsyncSession,
   expire_on_commit=False
)

@pytest.fixture(scope="session", autouse=True)
async def create_test_database():
   async with engine_test.begin() as conn:
      await conn.run_sync(Base.metadata.create_all)

   yield

   async with engine_test.begin() as conn:
      await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session():
   async with AsyncSessionLocal() as session:
      yield session
      await session.rollback()


async def override_get_db():
   async with AsyncSessionLocal() as session:
      yield session


@pytest.fixture(autouse=True)
def override_dependencies():
   app.dependency_overrides[get_db] = override_get_db
   yield
   app.dependency_overrides.clear()


@pytest.fixture
async def client():
   async with AsyncClient(
      transport=ASGITransport(app=app),
      base_url="http://test"
   ) as ac:
      yield ac
