class AIError(Exception):
   pass

class AIConnectionError(AIError):
   pass

class AIModelUnavailable(AIError):
   pass

class AIInvalidResponse(AIError):
   pass

class AIGenerationError(AIError):
   pass
