class BaseError(Exception):

    text = "Base error occured."
    status = 400

    def __init__(self, text, status=None):

        self.text = text

        if status:
            self.status = status
