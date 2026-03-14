<div align="center">

# ⚡ FastURL

**Serviço de encurtamento de URLs desenvolvido com Python e FastAPI**

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker&logoColor=white)

</div>

---

## Sobre o projeto

FastURL é uma API REST para encurtamento de URLs construída com foco em **arquitetura em camadas**, **código assíncrono** e **boas práticas de desenvolvimento**.

O projeto foi desenvolvido como estudo de arquitetura de software, aplicando separação de responsabilidades entre as camadas de rotas, serviço, repositório e modelos.

### Tecnologias utilizadas

- **FastAPI** — framework web assíncrono de alta performance
- **SQLAlchemy (async)** — ORM com suporte a operações assíncronas
- **PostgreSQL** — banco de dados relacional
- **Alembic** — controle de migrations
- **Docker + Docker Compose** — containerização da aplicação e do banco
- **Adminer** — interface visual para o banco de dados

---

## Arquitetura

O projeto segue o padrão de **arquitetura em camadas**:

```
app/
├── core/           # Configurações e settings da aplicação
├── models/         # Modelos do banco de dados (SQLAlchemy)
├── schemas/        # Schemas de entrada e saída (Pydantic)
├── repositories/   # Camada de acesso ao banco de dados
├── services/       # Regras de negócio
├── routers/        # Endpoints da API (FastAPI)
└── exceptions/     # Exceções customizadas de domínio
```

**Fluxo de uma requisição:**

```
Request → Router → Service → Repository → Database
                ↑
         Validação de schemas (Pydantic)
```

---

## Funcionalidades

- Encurtamento de URLs com código único de 8 caracteres
- Redirecionamento automático pela URL curta
- Expiração de URLs após 7 dias
- Contador de cliques por URL
- Estatísticas de acesso por código
- Validação de URLs duplicadas

---

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/urls/` | Cria uma URL encurtada |
| `GET` | `/r/{code}` | Redireciona para a URL original |
| `GET` | `/urls/{code}/stats` | Retorna estatísticas da URL |

> A documentação interativa completa está disponível via Swagger em `/docs` após subir o projeto.

---

## Como rodar o projeto

### Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) instalado na sua máquina

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/fasturl.git
cd fasturl
```

### 2. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
APP_NAME=URL-SHORTENER
APP_COMPANY=URL-SHORTENER-COMPANY
APP_VERSION=1.0.0
APP_BASE_URL="http://127.0.0.1:8000/"

DB_NAME=shortener_db
DB_USER=shortener_admin
DB_PASSWORD=shortener
DB_PORT=5432
DB_URL=postgresql+asyncpg://shortener_admin:shortener@db:5432/shortener_db
```

### 3. Suba os containers

```bash
docker compose build --no-cache
docker compose up -d
```

As migrations são aplicadas automaticamente na inicialização.

### 4. Acesse a aplicação

| Serviço | URL |
|---------|-----|
| API (Swagger) | http://127.0.0.1:8000/docs |
| Adminer (banco) | http://127.0.0.1:8080 |

**Credenciais do Adminer:**

| Campo | Valor |
|-------|-------|
| Sistema | PostgreSQL |
| Servidor | `db` |
| Usuário | valor do `DB_USER` no `.env` |
| Senha | valor do `DB_PASSWORD` no `.env` |
| Base de dados | `shortener_db` |

---

## Exemplo de uso

**Criar uma URL curta:**

```bash
curl -X POST http://127.0.0.1:8000/urls/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'
```

**Resposta:**

```json
{
  "id": 1,
  "url": "https://www.google.com",
  "shorted_url": "http://127.0.0.1:8000/r/aBcDeFgH",
  "code": "aBcDeFgH",
  "created_at": "2025-01-01T00:00:00Z"
}
```

**Ver estatísticas:**

```bash
curl http://127.0.0.1:8000/urls/aBcDeFgH/stats
```
