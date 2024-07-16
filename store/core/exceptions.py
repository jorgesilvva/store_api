class BaseException(Exception):
    message: str = "Internal Server Error"

    def __init__(self, message: str | None = None) -> None:
        if message:
            self.message = message

class NotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class InsertionException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
