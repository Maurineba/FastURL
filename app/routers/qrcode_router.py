from app.db.deps import get_db
from app.service.qrcode_service import QrcodeService

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends

router = APIRouter(
   prefix="/url",
   tags=["Qr-code"]
)


async def get_qrcode_service(db: AsyncSession = Depends(get_db)) -> QrcodeService:
   return QrcodeService(db)

@router.get("/{code}/qrcode", status_code=200)
async def generate_qrcode(
   code: str,
   qrcode_service: QrcodeService = Depends(get_qrcode_service)
):
   """
   Gera um qrcode para uma url encurtada.

   - **code**: codigo encurtado da url
   """
   return await qrcode_service.generate_qrcode(code)
