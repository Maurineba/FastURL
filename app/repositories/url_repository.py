from app.models.url_model import Url

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

class UrlRepository():
   def __init__(self, db: AsyncSession):
      self.db = db

   async def create(self, url: Url) -> Url:
      self.db.add(url)

   async def get_by_id(self, id: int) -> Url | None:
      stmt = select(Url).where(Url.id == id)
      result = await self.db.execute(stmt)

      return result.scalar_one_or_none()

   async def get_by_url(self, url: str) -> Url | None:
      stmt = select(Url).where(Url.url == url)
      result = await self.db.execute(stmt)

      return result.scalar_one_or_none()

   async def get_by_code(self, code: str) -> Url | None:
      stmt = select(Url).where(Url.code == code)
      result = await self.db.execute(stmt)

      return result.scalar_one_or_none()

   async def get_by_creator(self, creator_name: str) -> Url | None:
      stmt = select(Url).where(Url.created_by == creator_name)
      result = await self.db.execute(stmt)

      return result.scalar_one_or_none()

   async def increment_click(self, url_id: int) -> None:
      stmt = (
         update(Url).
         where(Url.id == url_id).
         values(clicks=Url.clicks + 1)
      )

      await self.db.execute(stmt)

   async def set_expired(self, url_id: int) -> None:
      stmt = (
         update(Url).
         where(Url.id == url_id).
         values(expired=True)
      )

      await self.db.execute(stmt)

   async def delete(self, url: Url) -> None:
      await self.db.delete(url)


