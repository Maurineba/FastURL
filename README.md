# ⚡ FastURL

O **FastURL** é uma API para encurtamento de URLs, desenvolvida com **Python** e **FastAPI**.

---

## 🚀 Tecnologias
- **Python 3.10+**
- **FastAPI** 
- **PostgreSQL** 
- **SQLAlchemy + Asyncpg**
- **Docker & Docker Compose** 
- **Adminer** (Interface gráfica para o banco de dados)

---

## 🛠️ Instruções de Instalação

### 1. Configuração do Ambiente (.env)
Antes de subir os containers, crie um arquivo chamado `.env` na raiz do projeto e configure-o com as seguintes informações:

```bash
APP_NAME=URL-SHORTENER
APP_COMPANY=URL-SHORTENER-COMPANY
APP_VERSION=1.0.0
APP_BASE_URL="http://127.0.0.1:8000/" (mantenha esse)

DB_NAME=shortener_db
DB_USER=shortener_admin
DB_PASSWORD=shortener
DB_PORT=5432

DB_URL=postgresql+asyncpg://shortener_admin:shortener@db:5432/shortener_db
```
### 2. Execução com Docker

O FastURL é totalmente dockerizado. Se ainda não possui o Docker, instale-o através do link oficial: [Download Docker.](https://www.docker.com/)

Com o Docker instalado, abra o terminal na pasta raiz do projeto e execute os comandos abaixo:
```bash
# Construir a imagem do projeto sem cache
docker compose build --no-cache
```
```bash
# Iniciar os serviços em segundo plano
docker compose up -d
```
## 📖 Documentação da API

Assim que os containers estiverem ativos, você poderá aceder à documentação interativa (Swagger) para testar todas as rotas:

🔗 Swagger UI: http://127.0.0.1:8000/docs

🗄️ Acesso ao Banco de Dados (Adminer)

Para visualizar os dados de forma simples, utilize o Adminer que sobe junto com a aplicação:

🔗 Acesso: http://127.0.0.1:8080

Utilize estas credenciais para o login:

    Sistema: PostgreSQL

    Servidor: db

    Utilizador: (O DB_USER definido no seu .env)

    Palavra-passe: (A DB_PASSWORD definida no seu .env)

    Base de dados: shortener_db

## 🧪 Testes 

Ao subir os containers você podera executar os testes!
Entre no terminal interativo do container da aplicação com o comando:
```bash
docker compose exec api pytest
```
Pronto! Testes executados.

## 🏗️ Arquitetura do Projeto

O FastURL foi estruturado utilizando **Arquitetura em Camadas** (Layered Architecture), o que permite uma clara separação de responsabilidades:

* **Schemas:** Definição das estruturas de dados para entrada e saída via Pydantic.
* **Routers:** Gerenciamento das requisições HTTP e roteamento.
* **Services:** Onde reside o "coração" da aplicação e as regras de encurtamento.
* **Repositories:** Comunicação direta com o banco de dados via SQLAlchemy.

Esta organização facilita a criação de testes automatizados e a manutenção do código a longo prazo.

📝 Licença

Projeto desenvolvido para fins de estudo. Sinta-se à vontade para utilizar e contribuir!
