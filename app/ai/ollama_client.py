import json

from app.core.settings import get_settings
from ollama import Client, ChatResponse
from app.exceptions.ai import (
   AIConnectionError,
   AIGenerationError,
   AIInvalidResponse,
   AIModelUnavailable
)

settings = get_settings()

class OllamaClient():
   def __init__(
      self,
      host: str = settings.ollama.host,
      model: str = settings.ollama.model
   ):
      self.client = Client(host=host)
      self.model = model

   def generate_json(self, prompt: str) -> dict:
      try:
         response: ChatResponse = self.client.chat(
            model=self.model,
            messages=[
               {
                  "role": "user",
                  "content": prompt
               }
            ] ,
            format="json",
            options={
               "temperature": 0.2
            }
         )
         return json.loads(response.message.content)

      except ConnectionError:
         raise AIConnectionError("Nao foi possivel se conectar ao Ollama")

      except json.JSONDecodeError:
         raise AIInvalidResponse("IA retornou um JSON invalido")

      except Exception as exc:
         raise AIGenerationError(f"Erro ao gerar resposta com IA: {str(exc)}")
