<div align="center">

# ⚡ FastURL

**API REST para encurtamento de URLs com estatísticas, QR Code e prévia automática com IA**

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat\&logo=python\&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat\&logo=fastapi\&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat\&logo=postgresql\&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat\&logo=docker\&logoColor=white)

</div>

---

## Sobre o projeto

FastURL é uma API REST desenvolvida com **Python** e **FastAPI** para encurtamento e gerenciamento de URLs.

O projeto permite criar links encurtados, redirecionar para a URL original, registrar estatísticas de acesso, gerar QR Codes e criar prévias automáticas de links utilizando IA local com Ollama.

A aplicação foi desenvolvida com foco em **arquitetura em camadas**, separação de responsabilidades, persistência com banco relacional, tratamento centralizado de erros e testes automatizados.

---

## Tecnologias utilizadas

* **FastAPI** — criação da API REST
* **SQLAlchemy Async** — ORM assíncrono
* **PostgreSQL** — banco de dados relacional
* **Alembic** — controle de migrations
* **Pydantic** — validação de dados
* **Docker + Docker Compose** — containerização
* **Ollama** — execução local do modelo de IA
* **BeautifulSoup + httpx** — extração de conteúdo web
* **Pytest** — testes automatizados
* **Adminer** — interface visual para o banco

---

## Funcionalidades

* Encurtamento de URLs
* Redirecionamento para a URL original
* Contador de acessos
* Estatísticas por URL
* Expiração automática dos links
* Geração de QR Code
* Prévia automática de links com IA local
* Validação de URLs
* Tratamento centralizado de erros
* Testes automatizados

---

## Arquitetura

O projeto segue uma arquitetura em camadas:

```txt
app/
├── ai/             # Cliente Ollama e prompts de IA
├── core/           # Configurações da aplicação
├── db/             # Configuração e dependências do banco
├── exceptions/     # Exceções customizadas e handlers
├── extractors/     # Extração de conteúdo web
├── models/         # Models SQLAlchemy
├── repositories/   # Camada de acesso ao banco
├── routers/        # Endpoints da API
├── schemas/        # Schemas Pydantic
├── service/        # Regras de negócio
└── tests/          # Testes automatizados
```

Fluxo principal da aplicação:

```txt
Request → Router → Service → Repository → Database
```

Fluxo da prévia com IA:

```txt
URL → WebExtractor → Ollama → Validação → Resposta
```

---

## Endpoints principais

| Método | Rota                 | Descrição                                 |
| ------ | -------------------- | ----------------------------------------- |
| `POST` | `/url`               | Cria uma URL encurtada                    |
| `GET`  | `/url/{code}`        | Retorna a URL original                    |
| `GET`  | `/url/{code}/stats`  | Retorna estatísticas da URL               |
| `GET`  | `/url/{code}/qrcode` | Gera o QR Code da URL encurtada           |
| `GET`  | `/r/{code}`          | Redireciona para a URL original           |
| `POST` | `/ai/summary`        | Gera uma prévia automática do link com IA |

A documentação interativa fica disponível em:

```txt
http://127.0.0.1:8000/docs
```

---

## Como rodar o projeto

### Pré-requisitos

* Docker
* Docker Compose
* Ollama instalado localmente, caso queira usar a funcionalidade de IA

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/fasturl.git
cd fasturl
```

### 2. Configure as variáveis de ambiente

Crie o arquivo `.env` com base no `.env.example`:

```bash
cp .env.example .env
```

Exemplo:

```env
APP_NAME=FastURL
APP_COMPANY=FastURL
APP_VERSION=1.0.0
APP_BASE_URL=http://127.0.0.1:8000

DB_NAME=shortener_db
DB_USER=shortener_admin
DB_PASSWORD=change_me
DB_PORT=5432
DB_URL=postgresql+asyncpg://shortener_admin:change_me@db:5432/shortener_db

OLLAMA_HOST=http://host.docker.internal:11434
OLLAMA_MODEL=llama3.2:3b

URL_EXPIRATION_DAYS=7
```

### Sobre o `APP_BASE_URL` e o QR Code

A variável `APP_BASE_URL` define a base usada para gerar as URLs encurtadas e os QR Codes.

Em ambiente local, ela pode ser configurada assim:

~~~env
APP_BASE_URL=http://127.0.0.1:8000
~~~
Isso funciona no próprio computador, mas pode não funcionar ao ler o QR Code pelo celular, pois 127.0.0.1 no celular aponta para o próprio celular, não para a máquina onde a API está rodando.

Para testar o QR Code em outro dispositivo, utilize uma URL acessível externamente, como um túnel do ngrok:

ngrok http 8000

Depois configure o .env com a URL gerada:

APP_BASE_URL=https://seu-dominio-ngrok.ngrok-free.dev

Também é possível usar o IP da máquina na rede local, caso o computador e o celular estejam conectados à mesma rede:

APP_BASE_URL=http://192.168.0.10:8000

A prévia com IA não depende diretamente do ngrok. Ela pode receber uma URL original ou uma URL encurtada. Quando recebe uma URL encurtada, a aplicação segue o redirecionamento e extrai o conteúdo da página final.

### 3. Suba os containers

```bash
docker compose up --build
```

A API ficará disponível em:

```txt
http://127.0.0.1:8000
```

O Adminer ficará disponível em:

```txt
http://127.0.0.1:8080
```

---

## Ollama

A funcionalidade de prévia automática depende do Ollama.

Para baixar o modelo usado no projeto:

```bash
ollama pull llama3.2:3b
```

Para iniciar o Ollama:

```bash
ollama serve
```

---

## Exemplos de uso

### Criar URL encurtada

```bash
curl -X POST http://127.0.0.1:8000/url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://fastapi.tiangolo.com/"}'
```

Resposta:

```json
{
  "url": "https://fastapi.tiangolo.com/",
  "shorted_url": "http://127.0.0.1:8000/r/aBcDeFgH"
}
```

### Consultar estatísticas

```bash
curl http://127.0.0.1:8000/url/aBcDeFgH/stats
```

Resposta:

```json
{
  "url": "https://fastapi.tiangolo.com/",
  "shorted_url": "http://127.0.0.1:8000/r/aBcDeFgH",
  "clicks": 3,
  "created_at": "2026-06-09T18:02:25.825912Z",
  "expired": false
}
```

### Gerar QR Code

```bash
curl http://127.0.0.1:8000/url/aBcDeFgH/qrcode --output qrcode.png
```

### Gerar prévia com IA

```bash
curl -X POST http://127.0.0.1:8000/ai/summary \
  -H "Content-Type: application/json" \
  -d '{"url": "https://pt.wikipedia.org/wiki/Lobo-guar%C3%A1"}'
```

Resposta:

```json
{
  "url": "https://pt.wikipedia.org/wiki/Lobo-guar%C3%A1",
  "summary": "Artigo sobre o lobo-guará, espécie de canídeo sul-americano conhecida por suas pernas longas e hábitos solitários.",
  "keywords": ["lobo-guará", "canídeo", "fauna"],
  "category": "Science"
}
```

---

## Como funciona a prévia com IA

A API acessa a página informada, extrai o conteúdo textual e envia esse texto para um modelo local via Ollama.

A extração é feita em camadas:

1. Metadados da página, como Open Graph e Twitter Cards;
2. Conteúdo semântico, como `article`, `main` e containers comuns de artigos;
3. Texto do `body` como fallback.

Essa estratégia reduz ruídos como menus, scripts e rodapés, deixando os resumos mais consistentes.

---

## Testes

Para rodar os testes:

```bash
pytest
```

Os testes cobrem os principais fluxos da API, incluindo criação de URL, busca por código, estatísticas, redirecionamento, incremento de cliques e erros esperados.

---

## Limitações

* A extração de conteúdo não executa JavaScript.
* Páginas com login, captcha ou bloqueio anti-bot podem não gerar prévia.
* A geração de prévia depende do Ollama estar em execução.
* O campo `shorted_url` foi mantido por compatibilidade interna do projeto.

---

## Autor

Desenvolvido por **Maurino Martins**.
