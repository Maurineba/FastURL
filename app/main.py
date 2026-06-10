from fastapi import FastAPI

from app.exceptions.handler import register_exception_handlers

from app.routers.redirect import router as redirect_router
from app.routers.url_router import router as url_router
from app.routers.qrcode_router import router as qrcode_router
from app.routers.summary import router as ai_summary_router


app = FastAPI(
   title="FastURL",
   summary="API REST para encurtamento de URLs com estatísticas, expiração, QR Code e prévia com IA.",
   description="""
FastURL é uma API REST desenvolvida com FastAPI para encurtamento e gerenciamento de URLs.

Funcionalidades:
- Criação de URLs encurtadas
- Redirecionamento para a URL original
- Contagem automática de acessos
- Estatísticas de acesso
- Expiração automática de links
- Geração de QR Code
- Prévia automática de links com IA local
- Tratamento centralizado de erros

O projeto utiliza PostgreSQL, SQLAlchemy assíncrono, Alembic, Docker e Ollama, seguindo uma arquitetura em camadas com separação entre rotas, serviços, repositórios, schemas e models.
""",
   version="1.0.0",
   contact={
      "name": "Maurino Martins",
      "email": "maurinojunior2006@yahoo.com",
   },
)

app.include_router(url_router)
app.include_router(redirect_router)
app.include_router(qrcode_router)
app.include_router(ai_summary_router)

register_exception_handlers(app)
