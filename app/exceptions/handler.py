from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.exceptions.url import (
   UrlNotFound,
   UrlAlreadyExists,
   UrlExpired,
   InvalidUrl,
   CodeGenerationFailed
)
from app.exceptions.extract import (
   ContentNotFound,
   InsufficientContent,
   WebPageRequestError
)
from app.exceptions.ai import (
   AIConnectionError,
   AIModelUnavailable,
   AIInvalidResponse,
   AIGenerationError
)
from app.exceptions.summary import (
   SummaryValidationError,
   SummaryGenerationError
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
         content=jsonable_encoder({
            "detail": "Url expirada",
            "expired_at": exc.expired_at.astimezone()
        })
      )

   @app.exception_handler(ContentNotFound)
   async def content_not_found_handler(request: Request, exc: ContentNotFound):
      return JSONResponse(
         status_code=422,
         content={"detail": "Nao foi possivel encontrar conteudo principal da pagina"}
      )

   @app.exception_handler(InsufficientContent)
   async def insufficient_content_handler(request: Request, exc: InsufficientContent):
      return JSONResponse(
         status_code=422,
         content={"detail": "Conteudo da pagina insuficiente para geracao de previa"}
      )

   @app.exception_handler(WebPageRequestError)
   async def web_page_request_handler(request: Request, exc: WebPageRequestError):
      return JSONResponse(
         status_code=502,
         content={"detail": "Nao foi possivel acessar a pagina informada"}
      )

   @app.exception_handler(AIConnectionError)
   async def ai_connection_error_handler(request: Request, exc: AIConnectionError):
      return JSONResponse(
         status_code=503,
         content={"detail": "Nao foi possivel conectar ao servico de IA"}
      )

   @app.exception_handler(AIModelUnavailable)
   async def ai_model_unavailable_handler(request: Request, exc: AIModelUnavailable):
      return JSONResponse(
         status_code=503,
         content={"detail": "Modelo de IA indisponivel ou nao encontrado"}
      )

   @app.exception_handler(AIInvalidResponse)
   async def ai_invalid_response_handler(request: Request, exc: AIInvalidResponse):
      return JSONResponse(
         status_code=502,
         content={"detail": "A IA retornou uma resposta invalida"}
      )

   @app.exception_handler(AIGenerationError)
   async def ai_generation_error_handler(request: Request, exc: AIGenerationError):
      return JSONResponse(
         status_code=500,
         content={"detail": "Nao foi possivel gerar resposta com IA"}
      )

   @app.exception_handler(SummaryValidationError)
   async def summary_validation_error_handler(request: Request, exc: SummaryValidationError):
      return JSONResponse(
         status_code=502,
         content={"detail": "A previa gerada nao passou na validacao"}
      )

   @app.exception_handler(SummaryGenerationError)
   async def summary_generation_error_handler(request: Request, exc: SummaryGenerationError):
      return JSONResponse(
         status_code=500,
         content={"detail": "Nao foi possivel gerar a previa do link"}
      )
