from datetime import datetime

from pydantic import BaseModel, Field

class UrlBase(BaseModel):
   url: str

class UrlCreate(UrlBase):
   pass

class OriginalUrlResponse(UrlBase):
   pass

class UrlResponse(UrlBase):
   id: int
   shorted_url: str

class UrlStatsResponse(UrlBase):
   shorted_url: str
   clicks: int
   created_at: datetime
   expired: bool
