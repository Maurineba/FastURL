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

class AuthSettings(BaseSettings):


   model_config = SettingsConfigDict(env_file=".env", env_prefix="auth_", env_file_encoding="utf-8", extra="ignore")


class Settings(BaseSettings):
   app: AppSettings = AppSettings()
   db: DatabaseSettings = DatabaseSettings()
   auth: AuthSettings = AuthSettings()

@lru_cache
def get_settings() -> Settings:
    return Settings()
