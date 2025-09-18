class BaseError(Exception):
    """Base class for custom application errors."""

    text = "Base error occured."
    status = 400

    def __init__(self, text: str = None, status: int = None):

        if text:
            self.text = text

        if status:
            self.status = status
