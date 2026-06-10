import qrcode

from io import BytesIO

from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import get_settings
from app.exceptions.url import UrlNotFound
from app.repositories.url_repository import UrlRepository

settings = get_settings()

class QrcodeService():
   def __init__(self, db: AsyncSession):
      self.db: AsyncSession = db
      self.url_repo = UrlRepository(db)
      self.base_url = settings.app.base_url

   async def generate_qrcode(self, code: str):
      short_url = await self.url_repo.get_by_code(code)
      if not short_url:
         raise UrlNotFound()

      link = self.base_url + "/r/" + code

      img = qrcode.make(link)
      buffer = BytesIO()
      img.save(buffer, format="PNG")
      buffer.seek(0)

      return StreamingResponse(buffer, media_type="image/png")
