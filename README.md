   # FastURL

   ## descricao
   O FastURl é um api para encurtamento de URL. Ele foi desenvolvido utilizando python fastapi por conta da facilidade de se utilizar assincronismo

   ## instrucao de instalacao
   primeiro crie um arquivo .env na raiz do projeto baseado nessas informacoes:
   ```bash
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

   FastURl é dockerizado, ou seja, voce ira precisar do docker instalado no seu computador.

   visite a pagina oficial do docker para prosseguir no FastURL. LINK PARA INSTALAR DOCKER

   com o docker instalado basta voce voce entrar no root do projeto e rodar os seguintes comandos:
   ```bash
   docker compose build --no-cache
   ```
   e logo em seguida:
   ```bash
   docker compose up -d
   ```
   Pronto! voce acabou de subir os containers do FastURL.

   Agora acesse o swagger do projeto em:
   ```bash
   http://127.0.0.1:8000/docs
   ```
   aqui voce ira encontra todas as rotas organizadas e documentadas no proprio swagger.

   para facilitar a visualizacao do banco de dados utilizei o software adminer que é subido junto aos containeres voce pos acessa lo aqui:
   ```bash
   http://127.0.0.1:8080
   ```
   utilize as credencias da sua .env.
   ```bash
   sistema: PostgreSQL
   servidor: db
   usuario: seu usuario do banco (que voce colocou na .env)
   senha: sua senha do banco (que voce colocou na .env)
   Base de dados: shortener_db
   ```

