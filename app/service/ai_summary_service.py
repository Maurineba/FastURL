from pydantic import ValidationError

from app.core.settings import get_settings
from app.ai.prompt import build_summary_prompt
from app.schemas.summary_schema import AISummaryResponse
from app.ai.ollama_client import OllamaClient
from app.extractors.webpage_extractor import WebExtractor
from app.exceptions.ai import AIError
from app.exceptions.summary import (
   SummaryGenerationError,
   SummaryValidationError
)

settings = get_settings()

HOST = "http://host.docker.internal:11434"

class AISummaryService():
   def __init__(self,
      text_length: int = 2500,
      host: str = HOST
   ):
      self.text_length = text_length
      self.host = host
      self.ai_client = OllamaClient()
      self.extractor = WebExtractor()

   async def ai_summary(self, url: str) -> AISummaryResponse:
      try:
         text = await self.extractor.extract_text(url)
         response = self._generate_simple_summary(url, text)

         return AISummaryResponse(**response)

      except ValidationError:
         raise SummaryValidationError("A prévia gerada pela IA não passou na validação.")

      except AIError:
         raise SummaryGenerationError("Não foi possível gerar a prévia com IA.")

   def _generate_simple_summary(self, url:str, text: str) -> dict:
      limited_text = text[:self.text_length]

      prompt = build_summary_prompt(url, limited_text)

      return self.ai_client.generate_json(prompt)

   async def _generate_map_reduce_summary(self, url: str, text: str) -> dict:
      pass

   def _fallback_response(self, url: str) -> AISummaryResponse:
      return AISummaryResponse(
         url=url,
         summary="Não foi possível gerar uma prévia confiável para este link.",
         keywords=[],
         category="Unknown"
      )










