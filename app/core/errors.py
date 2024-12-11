class APIException(Exception):
    def __init__(self, code: int, error: str, details: str):
        self.code = code
        self.error = error
        self.details = details
