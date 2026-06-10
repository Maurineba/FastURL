from app.exceptions.base import AppException


class ContentNotFound(AppException):
   pass

class InsufficientContent(AppException):
   pass

class WebPageRequestError(AppException):
   pass
