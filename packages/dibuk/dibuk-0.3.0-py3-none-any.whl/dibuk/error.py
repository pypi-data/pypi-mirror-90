class DibukError(Exception):
    def __init__(self, message=None, http_body=None):
        super(DibukError, self).__init__(message)

        self.http_body = http_body


class APIError(DibukError):
    pass


class APIConnectionError(APIError):
    pass


class BookNotFoundError(APIError):
    pass
