from datetime import datetime

from app.exceptions.base import AppException

class UrlNotFound(AppException):
   pass

class UrlAlreadyExists(AppException):
   pass

class UrlExpired(AppException):
   def __init__(self, expired_at: datetime):
      self.expired_at = expired_at

class InvalidUrl(AppException):
   pass

class CodeGenerationFailed(AppException):
   pass
