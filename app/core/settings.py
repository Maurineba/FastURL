from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class AppSettings(BaseSettings):
   name: str = None
   company: str = None
   version: str = None
   base_url: str = None

   model_config = SettingsConfigDict(env_file=".env", env_prefix="app_", env_file_encoding="utf-8", extra="ignore")

class DatabaseSettings(BaseSettings):
   url: str = None

   model_config = SettingsConfigDict(env_file=".env", env_prefix="db_", env_file_encoding="utf-8", extra="ignore")


class OllamaSettings(BaseSettings):
   host: str = "http://host.docker.internal:11434"
   model: str = "llama3.2:3b"

   model_config = SettingsConfigDict(env_file=".env", env_prefix="ollama_", env_file_encoding="utf-8", extra="ignore")

class UrlSettings(BaseSettings):
   expiration_days: int

   model_config = SettingsConfigDict(env_file=".env", env_prefix="url_", env_file_encoding="utf-8", extra="ignore")
class Settings(BaseSettings):
   app: AppSettings = AppSettings()
   db: DatabaseSettings = DatabaseSettings()
   ollama: OllamaSettings = OllamaSettings()
   url: UrlSettings = UrlSettings()

@lru_cache
def get_settings() -> Settings:
    return Settings()
