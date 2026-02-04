from fastapi import FastAPI

from app.exceptions.handler import register_exception_handlers

from app.routers.redirect import router as redirect_router
from app.routers.url_router import router as url_router



app = FastAPI(
    title="FastURL",
    description="""
API para encurtamento de URLs desenvolvida com FastAPI.

Funcionalidades:
- Criação de URLs encurtadas
- Redirecionamento com contagem de acessos
- Expiração automática por tempo
- Estatísticas de acesso
- Tratamento centralizado de erros

Projeto focado em boas práticas, arquitetura em camadas e uso de SQLAlchemy assíncrono.
""",
    summary="API de encurtamento de URLs com expiração e estatísticas",
    version="1.0.0",
    contact={
        "name": "Maurino Martins",
        "email": "maurinojunior2006@yahoo.com",
    },
)

app.include_router(url_router)
app.include_router(redirect_router)

register_exception_handlers(app)
