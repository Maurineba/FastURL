import string
import random
from datetime import datetime, timedelta, timezone

from app.core.settings import get_settings
from app.repositories.url_repository import UrlRepository
from app.models.url_model import Url
from app.schemas.url_schema import (
   UrlCreate,
   UrlResponse
)
from app.exceptions.url import(
   UrlAlreadyExists,
   UrlNotFound,
   UrlExpired,
   InvalidUrl,
   CodeGenerationFailed
)

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.responses import RedirectResponse

settings = get_settings()

LETTERS = tuple(string.ascii_lowercase + string.ascii_uppercase)

class UrlService():
   def __init__(self, db: AsyncSession):
      self.db: AsyncSession = db
      self.url_repo = UrlRepository(db)
      self.base_url = settings.app.base_url
      self.CODE_LENGTH = 8
      self.url_expiration_time = 7 # dias

   async def _generate_unique_code(self):
      attempts = 1
      max_attempts = 3

      while attempts <= max_attempts:
         code = "".join(random.choice(LETTERS) for _ in range(self.CODE_LENGTH))

         exists_code = await self.url_repo.get_by_code(code)
         if not exists_code:
            return code

         attempts += 1

      raise CodeGenerationFailed()


   async def create_short_url(self, url_data: UrlCreate) -> Url:
      if not url_data.url.startswith(("http://", "https://")):
         raise InvalidUrl()

      try:
         existing_url = await self.url_repo.get_by_url(url_data.url)
         if existing_url:
            raise UrlAlreadyExists()

         code = await self._generate_unique_code()

         short_url = self.base_url + "r/" + code

         url_model = Url(
            url = url_data.url,
            shorted_url = short_url,
            code=code
         )
         await self.url_repo.create(url_model)
         await self.db.commit()
         await self.db.refresh(url_model)

         return url_model

      except Exception as error:
         await self.db.rollback()
         print("erro inesperado:", error)
         raise


   async def get_original_url(self, code):
      original_url = await self.url_repo.get_by_code(code)
      if not original_url:
         raise UrlNotFound()

      return original_url.url

   async def verify_expiration(self, url: Url):
      now = datetime.now(timezone.utc)

      expiration_date = url.created_at + timedelta(days=self.url_expiration_time)

      return now >= expiration_date, expiration_date

   async def redirect(self, code: str):
      original_url = await self.url_repo.get_by_code(code)
      if not original_url:
         raise UrlNotFound()

      is_expired, expired_at = await self.verify_expiration(original_url)
      if is_expired:

         await self.url_repo.set_expired(original_url.id)
         await self.db.commit()

         raise UrlExpired(expired_at)

      await self.url_repo.increment_click(original_url.id)
      await self.db.commit()

      return RedirectResponse(
         url=original_url.url,
         status_code=301
      )

   async def get_url_stats(self, code: str):
      short_url = await self.url_repo.get_by_code(code)
      if not short_url:
         raise UrlNotFound()

      return short_url
