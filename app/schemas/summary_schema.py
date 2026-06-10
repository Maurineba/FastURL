from pydantic import BaseModel, Field
from pydantic import HttpUrl

class InputAISummary(BaseModel):
   url: HttpUrl

class AISummaryResponse(BaseModel):
   url: HttpUrl
   summary: str
   keywords: list[str]
   category: str = Field(..., max_length=50)
