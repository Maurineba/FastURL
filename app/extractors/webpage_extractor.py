import re
from bs4 import BeautifulSoup, Comment, Tag
import httpx
from app.exceptions.extract import (
   InsufficientContent,
   ContentNotFound,
   WebPageRequestError
)

_NOISE_TAGS = [
   "script", "style", "noscript", "nav", "footer", "header",
   "form", "aside", "sup", "iframe", "button",
]

_SEMANTIC_SELECTORS = [
   {"class": "mw-parser-output"},
   {"id": "mw-content-text"},
   {"role": "main"},
   {"class": "post-content"},
   {"class": "entry-content"},
   {"class": "article-body"},
]

_META_DESCRIPTION_ATTRS = [
   {"property": "og:description"},
   {"name": "twitter:description"},
   {"name": "description"},
]

_META_TITLE_ATTRS = [
   {"property": "og:title"},
   {"name": "twitter:title"},
]

class WebExtractor():
   def __init__(self, timeout: int = 10, min_length: int = 300):
      self.timeout = timeout
      self.min_length = min_length

   async def extract_text(self, url: str) -> str:
      html = await self._fetch_html(url)
      soup = BeautifulSoup(html, "html.parser")

      self._clean_soup(soup)

      text = self._extract_from_metadata(soup)

      if len(text) < self.min_length:
         semantic = self._extract_from_semantic_html(soup)
         text = f"{text} {semantic}".strip() if text else semantic

      if len(text) < self.min_length:
         body_text = self._extract_from_body(soup)
         text = f"{text} {body_text}".strip() if text else body_text

      if not text:
         raise ContentNotFound("Não foi possível encontrar conteúdo na página.")

      if len(text) < self.min_length:
         raise InsufficientContent("Conteúdo insuficiente para gerar prévia.")

      return self._normalize_text(text)

   async def _fetch_html(self, url: str) -> str:
      try:
         async with httpx.AsyncClient(
            timeout=httpx.Timeout(connect=5.0, read=8.0, write=5.0, pool=5.0),
            follow_redirects=True
         ) as client:
            response = await client.get(
               url,
               headers={
                  "ngrok-skip-browser-warning": "1",
                  "User-Agent": (
                     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/124.0.0.0 Safari/537.36"
                  ),
                  "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
                  "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
               }
            )
            response.raise_for_status()
            
         return response.text

      except httpx.TimeoutException:
         raise WebPageRequestError(f"Timeout ao acessar a página: {url}")

      except httpx.RequestError:
         raise WebPageRequestError(f"Não foi possível acessar a página: {url}")

      except httpx.HTTPStatusError as exc:
         raise WebPageRequestError(f"A página retornou erro HTTP {exc.response.status_code}: {url}")

   def _clean_soup(self, soup: BeautifulSoup) -> None:
      for tag in soup(_NOISE_TAGS):
         tag.decompose()
      for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
         comment.extract()

   def _extract_from_metadata(self, soup: BeautifulSoup) -> str:
      parts: list[str] = []

      for attrs in _META_TITLE_ATTRS:
         tag = soup.find("meta", attrs=attrs)
         if tag and tag.get("content", "").strip():
            parts.append(tag["content"].strip())
            break

      if not parts and soup.title and soup.title.string:
         title = soup.title.string.strip()
         if title:
            parts.append(title)

      for attrs in _META_DESCRIPTION_ATTRS:
         tag = soup.find("meta", attrs=attrs)
         if tag and tag.get("content", "").strip():
            parts.append(tag["content"].strip())
            break

      return " ".join(parts)

   def _extract_from_semantic_html(self, soup: BeautifulSoup) -> str:
      container = self._find_semantic_container(soup)
      if container is None:
         return ""
      paragraphs = container.find_all("p")
      text = " ".join(
         p.get_text(separator=" ", strip=True)
         for p in paragraphs
         if p.get_text(strip=True)
      )
      return text.strip()

   def _find_semantic_container(self, soup: BeautifulSoup) -> Tag | None:
      for selector in _SEMANTIC_SELECTORS:
         found = soup.find(attrs=selector)
         if found:
            return found
      for tag in ("article", "main"):
         found = soup.find(tag)
         if found:
            return found
      return None

   def _extract_from_body(self, soup: BeautifulSoup) -> str:
      if soup.body is None:
         return ""
      tags_of_interest = soup.body.find_all(["p", "h1", "h2", "h3", "li"])
      text = " ".join(
         tag.get_text(separator=" ", strip=True)
         for tag in tags_of_interest
         if tag.get_text(strip=True)
      )
      if len(text) < self.min_length:
         text = soup.body.get_text(separator=" ", strip=True)
      return text.strip()

   def _normalize_text(self, text: str) -> str:
      text = re.sub(r"[ \t]+", " ", text)
      text = re.sub(r"\n{2,}", "\n", text)
      lines = [line.strip() for line in text.splitlines()]
      lines = [line for line in lines if len(line) > 2]
      return " ".join(lines).strip()
