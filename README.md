````md
<div align="center">

# ⚡ FastURL

**API REST para encurtamento de URLs com estatísticas, QR Code e prévia automática com IA**

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-Testes-0A9EDC?style=flat&logo=pytest&logoColor=white)

</div>

---

## Sobre o projeto

FastURL é uma API REST desenvolvida com **Python** e **FastAPI** para encurtamento e gerenciamento de URLs.

Além das funcionalidades tradicionais de um encurtador, como redirecionamento, estatísticas e expiração de links, o projeto também possui geração de QR Code e uma funcionalidade experimental de **prévia automática de links com IA local** usando Ollama.

O projeto foi desenvolvido com foco em boas práticas de backend, arquitetura em camadas, persistência com banco relacional, tratamento centralizado de erros, testes automatizados e organização de responsabilidades.

---

## Tecnologias utilizadas

- **Python**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy Async**
- **Alembic**
- **Pydantic**
- **Docker**
- **Docker Compose**
- **Ollama**
- **BeautifulSoup**
- **httpx**
- **Pytest**
- **Adminer**

---

## Funcionalidades

- Criação de URLs encurtadas
- Redirecionamento para a URL original
- Contagem automática de acessos
- Consulta de estatísticas por código
- Expiração automática de URLs
- Geração de QR Code para a URL encurtada
- Geração de prévia automática com IA local
- Extração de conteúdo web com BeautifulSoup
- Tratamento centralizado de erros
- Configuração por variáveis de ambiente
- Testes automatizados com Pytest

---

## Arquitetura

O projeto segue uma arquitetura em camadas, separando responsabilidades entre rotas, serviços, repositórios, schemas, models e tratamento de erros.

```txt
app/
├── ai/             # Cliente Ollama e prompts de IA
├── core/           # Configurações da aplicação
├── db/             # Sessão, base e dependências do banco
├── exceptions/     # Exceções customizadas e handlers globais
├── extractors/     # Extração de conteúdo web
├── models/         # Models SQLAlchemy
├── repositories/   # Acesso ao banco de dados
├── routers/        # Endpoints da API
├── schemas/        # Schemas Pydantic
├── service/        # Regras de negócio
└── tests/          # Testes automatizados
````

Fluxo principal da aplicação:

```txt
Request → Router → Service → Repository → Database
```

Fluxo da funcionalidade de IA:

```txt
URL → WebExtractor → Prompt → Ollama → Validação → Resposta
```

---

## Como rodar o projeto

### Pré-requisitos

* Docker
* Docker Compose
* Ollama instalado localmente, caso queira usar a funcionalidade de IA

---

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/fasturl.git
cd fasturl
```

---

### 2. Configure as variáveis de ambiente

Crie o arquivo `.env` com base no `.env.example`:

```bash
cp .env.example .env
```

Exemplo de configuração:

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

---

### 3. Suba os containers

```bash
docker compose up --build
```

As migrations são aplicadas automaticamente na inicialização, caso o projeto esteja configurado para isso no container.

---

### 4. Acesse a aplicação

| Serviço | URL                          |
| ------- | ---------------------------- |
| API     | `http://127.0.0.1:8000`      |
| Swagger | `http://127.0.0.1:8000/docs` |
| Adminer | `http://127.0.0.1:8080`      |

Credenciais do Adminer:

| Campo         | Valor                  |
| ------------- | ---------------------- |
| Sistema       | PostgreSQL             |
| Servidor      | `db`                   |
| Usuário       | valor de `DB_USER`     |
| Senha         | valor de `DB_PASSWORD` |
| Base de dados | valor de `DB_NAME`     |

---

## Ollama

A funcionalidade de prévia automática depende do Ollama em execução localmente.

Para baixar o modelo usado no projeto:

```bash
ollama pull llama3.2:3b
```

Para iniciar o Ollama:

```bash
ollama serve
```

No Docker, o projeto usa o host configurado em:

```env
OLLAMA_HOST=http://host.docker.internal:11434
```

---

## Endpoints principais

| Método | Rota                 | Descrição                                 |
| ------ | -------------------- | ----------------------------------------- |
| `POST` | `/url`               | Cria uma URL encurtada                    |
| `GET`  | `/url/{code}`        | Retorna a URL original                    |
| `GET`  | `/url/{code}/stats`  | Retorna estatísticas da URL               |
| `GET`  | `/url/{code}/qrcode` | Gera um QR Code da URL encurtada          |
| `GET`  | `/r/{code}`          | Redireciona para a URL original           |
| `POST` | `/ai/summary`        | Gera uma prévia automática do link com IA |

A documentação interativa completa fica disponível em:

```txt
http://127.0.0.1:8000/docs
```

---

## Exemplos de uso

### Criar uma URL encurtada

```bash
curl -X POST http://127.0.0.1:8000/url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://fastapi.tiangolo.com/"}'
```

Exemplo de resposta:

```json
{
  "url": "https://fastapi.tiangolo.com/",
  "shorted_url": "http://127.0.0.1:8000/r/aBcDeFgH"
}
```

---

### Consultar a URL original

```bash
curl http://127.0.0.1:8000/url/aBcDeFgH
```

Exemplo de resposta:

```json
{
  "url": "https://fastapi.tiangolo.com/"
}
```

---

### Redirecionar para a URL original

```bash
curl -I http://127.0.0.1:8000/r/aBcDeFgH
```

Esse endpoint redireciona para a URL original e incrementa a contagem de acessos.

---

### Consultar estatísticas

```bash
curl http://127.0.0.1:8000/url/aBcDeFgH/stats
```

Exemplo de resposta:

```json
{
  "url": "https://fastapi.tiangolo.com/",
  "shorted_url": "http://127.0.0.1:8000/r/aBcDeFgH",
  "clicks": 3,
  "created_at": "2026-06-09T18:02:25.825912Z",
  "expired": false
}
```

---

### Gerar QR Code

```bash
curl http://127.0.0.1:8000/url/aBcDeFgH/qrcode --output qrcode.png
```

Esse endpoint retorna uma imagem PNG contendo o QR Code da URL encurtada.

---

### Gerar prévia com IA

```bash
curl -X POST http://127.0.0.1:8000/ai/summary \
  -H "Content-Type: application/json" \
  -d '{"url": "https://pt.wikipedia.org/wiki/Lobo-guar%C3%A1"}'
```

Exemplo de resposta:

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

A prévia automática acessa a página informada, extrai o conteúdo textual e envia esse conteúdo para um modelo local via Ollama.

A extração de conteúdo usa uma estratégia em camadas:

1. Metadados da página, como Open Graph e Twitter Cards;
2. Conteúdo semântico, como `article`, `main` e containers comuns de artigos;
3. Texto do `body` como fallback.

Essa abordagem reduz ruídos como menus, scripts, rodapés e elementos de navegação, deixando os resumos mais consistentes.

---

## Testes

Para rodar os testes:

```bash
pytest
```

Os testes cobrem fluxos como:

* Criação de URL encurtada
* Validação de URL inválida
* Busca da URL original
* Consulta de estatísticas
* Redirecionamento
* Incremento de cliques
* Erros esperados para códigos inexistentes

---

## Limitações conhecidas

* A extração de conteúdo não executa JavaScript.
* Páginas protegidas por login, captcha ou bloqueio anti-bot podem não gerar prévia.
* A geração de prévia depende do Ollama estar em execução.
* O campo `shorted_url` foi mantido por compatibilidade interna do projeto.

---

## Próximos passos

* Adicionar autenticação de usuários
* Criar painel web para gerenciamento das URLs
* Armazenar prévias geradas para evitar reprocessamento
* Adicionar cache para links já analisados
* Expandir a cobertura de testes
* Melhorar a nomenclatura pública de `shorted_url` para `short_url`

---

## Autor

Desenvolvido por **Maurino Martins**.

```
```
