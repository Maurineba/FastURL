from app.db.deps import get_db
from app.schemas.url_schema import (
   UrlCreate,
   UrlResponse
)
from app.service.url_service import UrlService

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
   prefix="/r",
   tags=["redirect"]
)


async def get_url_service(db: AsyncSession = Depends(get_db)) -> UrlService:
   return UrlService(db)


@router.get("/{code}", status_code=301)
async def redirect(
   code: str,
   url_service: UrlService = Depends(get_url_service)
):
   return await url_service.redirect(code)
