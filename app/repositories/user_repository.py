from app.models.user_model import User

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class UserRepository():
   def __init__(self, db: AsyncSession):
      self.db = db

   async def create(self, user: User) -> User | None:
      self.db.add(user)
      await self.db.commit()
      return user

   async def get_by_id(self, id: int) -> User | None:
      stmt = select(User).where(User.id == id)
      result = await self.db.execute(stmt)

      return result.scalar_one_or_none()

   async def delete (self, user: User) -> User | None:
      await self.db.delete(user)
      await self.db.commit()
