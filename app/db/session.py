from app.core.settings import get_settings

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

settings = get_settings()

engine = create_async_engine(settings.db.url)

SessionLocal = async_sessionmaker(
   bind=engine,
   class_=AsyncSession,
   expire_on_commit=False
)

