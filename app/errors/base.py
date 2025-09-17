class BaseError(Exception):

    text = "Base error occured."
    status = 400

    def __init__(self, text=None, status=None):

        if text:
            self.text = text

        if status:
            self.status = status
