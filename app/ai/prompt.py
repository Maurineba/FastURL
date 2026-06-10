def build_summary_prompt(url: str, text: str) -> str:
   return f"""
Você gera prévias curtas para links encurtados.

Analise o conteúdo extraído da página e retorne SOMENTE um JSON válido com EXATAMENTE estes campos:
url, summary, keywords, category.

Não crie campos extras como title, author, content, description, metadata ou source.

Regras:
- Use apenas o conteúdo fornecido.
- Não invente informações.
- Não copie exemplos ou instruções do prompt.
- Não copie o título literalmente.
- Ignore menus, anúncios, rodapés, login, cookies e textos repetidos.
- O campo url deve ser exatamente: {url}
- O campo summary deve explicar diretamente o assunto principal da página.
- O summary deve estar em português brasileiro.
- O summary deve ter uma única frase, entre 50 e 180 caracteres.
- O summary não pode ser genérico.
- O summary não pode ser: "Prévia curta sobre o conteúdo principal do link."
- O summary não pode ser: "Sobre o que é esta página?"
- O campo keywords deve ter de 3 a 6 termos curtos, em minúsculas.
- O campo category deve ser uma das categorias permitidas.

Categorias permitidas:
Programming, Technology, Education, News, Business, Science, Health, Entertainment, Sports, Books, Other, Unknown.

Escolha Programming para código, APIs, frameworks, linguagens e desenvolvimento.
Escolha Technology para tecnologia geral, IA, internet, apps, dispositivos e segurança digital.
Escolha Entertainment para filmes, séries, jogos, música, cultura pop e animes.
Escolha Books para livros, literatura, autores e resenhas literárias.
Escolha Unknown se o conteúdo for insuficiente, login, erro, bloqueio ou página vazia.

Retorne neste formato, preenchendo os valores com base no conteúdo:
{{
  "url": "{url}",
  "summary": "...",
  "keywords": ["...", "...", "..."],
  "category": "Other"
}}

Se o conteúdo for insuficiente, retorne:
{{
  "url": "{url}",
  "summary": "Não foi possível gerar uma prévia confiável para este link.",
  "keywords": [],
  "category": "Unknown"
}}

Conteúdo:
###
{text}
###
"""
