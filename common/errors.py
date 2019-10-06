
class CustomError(Exception):
    def __init__(self, message, extra=None):
        Exception.__init__(self, message)
        self.extra = extra or {}


class BadRequestError(CustomError):
    pass


class PermissionError(CustomError):
    pass


class NotFoundError(CustomError):
    pass


class NotAllowedError(CustomError):
    pass


class ConflictError(CustomError):
    pass


class InternalServerError(CustomError):
    pass
