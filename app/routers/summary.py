from app.service.ai_summary_service import AISummaryService
from app.schemas.summary_schema import (
   AISummaryResponse,
   InputAISummary
)

from fastapi import APIRouter, Depends

router = APIRouter(
   prefix="/ai",
   tags=["AI"]
)

async def get_ai_summary_service() -> AISummaryService:
   return AISummaryService()


@router.post("/summary", response_model=AISummaryResponse)
async def summarize_link(
   link: InputAISummary,
   ai_summary_service: AISummaryService = Depends(get_ai_summary_service)
):
   return await ai_summary_service.ai_summary(str(link.url))

