class Error(Exception):
    def __init__(self, message):
        self.message = message
        self.name = str(self.__class__.__name__)

    def __repr__(self):
        return "{0}: {1}".format(self.name, self.message)


class RequestError(Error):
    status_code = 400


class AuthError(Error):
    status_code = 401


class ForbiddenError(Error):
    status_code = 403


class NotFoundError(Error):
    status_code = 404


class ConflictError(Error):
    status_code = 409


class UnprocessableEntityError(Error):
    status_code = 422


class InternalServerError(Error):
    status_code = 500


# a lookup of all errors
ERRORS = {
    "RequestError": RequestError,
    "AuthError": AuthError,
    "ForbiddenError": ForbiddenError,
    "NotFoundError": NotFoundError,
    "ConflictError": ConflictError,
    "UnprocessableEntityError": UnprocessableEntityError,
    "InternalServerError": InternalServerError,
}
