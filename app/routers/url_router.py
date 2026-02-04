from app.db.deps import get_db
from app.schemas.url_schema import (
   UrlCreate,
   UrlResponse,
   UrlStatsResponse,
   OriginalUrlResponse
)
from app.service.url_service import UrlService

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends

router = APIRouter(
   prefix="/url",
   tags=["url"]
)


async def get_url_service(db: AsyncSession = Depends(get_db)) -> UrlService:
   return UrlService(db)


@router.post("", status_code=201, response_model=UrlResponse)
async def create_short_url(
   url: UrlCreate,
   url_service: UrlService = Depends(get_url_service)
   ):
   """
   Gera uma URL encurtada.

   - **url**: URL que voce deseja encurtar. exemplo: https://youtube.com/sadjAKJskd21123

   """
   return await url_service.create_short_url(url)

@router.get("/{code}", response_model=OriginalUrlResponse)
async def get_original_url(
   code: str,
   url_service: UrlService = Depends(get_url_service)
):
   """
   Retorna uma URL encurtada atraves do seu codigo.

   - **code**: codigo que foi gerada para a URL encurtada. exemplo: Abcd1234
   """
   original_url = await url_service.get_original_url(code)
   return {"url": original_url}

@router.get("/{code}/stats", response_model=UrlStatsResponse)
async def get_url_stats(
   code: str,
   url_service: UrlService = Depends(get_url_service)
):
   """
   Retorna os status de uma URL encurtada atraves de seu codigo.

   - **code**: codigo que foi gerada para a URL encurtada. exemplo: Abcd1234
   """
   return await url_service.get_url_stats(code)
