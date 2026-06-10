class SummaryError(Exception):
   pass

class SummaryGenerationError(SummaryError):
   pass

class SummaryValidationError(SummaryError):
   pass

class SummaryUnavailable(SummaryError):
   pass
