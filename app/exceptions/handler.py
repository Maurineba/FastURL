from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.url import (
   UrlNotFound,
   UrlAlreadyExists,
   UrlExpired,
   InvalidUrl,
   CodeGenerationFailed
)

def register_exception_handlers(app):
   @app.exception_handler(UrlNotFound)
   async def url_not_found_handler(request: Request, exc: UrlNotFound):
      return JSONResponse(
         status_code=404,
         content={"detail": "Url nao encontrada"}
      )

   @app.exception_handler(UrlAlreadyExists)
   async def url_already_exists_handler(request: Request, exc: UrlAlreadyExists):
      return JSONResponse(
         status_code=409,
         content={"detail": "Url ja existe"}
      )

   @app.exception_handler(InvalidUrl)
   async def invalid_url_handler(request: Request, exc: InvalidUrl):
      return JSONResponse(
         status_code=422,
         content={"detail": "Url inválida! certifique-se de incluir http:// ou https://"}
      )

   @app.exception_handler(CodeGenerationFailed)
   async def code_generation_failed_handler(request: Request, exc: CodeGenerationFailed):
      return JSONResponse(
         status_code=500,
         content={"detail": "Nao foi possivel gerar um codigo. tente novamente"}
      )

   @app.exception_handler(UrlExpired)
   async def url_expired_handler(request: Request, exc: UrlExpired):
       return JSONResponse(
         status_code=410,
         content={
            "detail": "Url expirada",
            "expired_at": exc.expired_at.astimezone()
         }
      )



