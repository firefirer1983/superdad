from werkzeug.http import HTTP_STATUS_CODES


class JsonErrorResponse(Exception):
    status_code = None
    
    def __init__(self, message=None, payload=None):
        super().__init__(message)
        self.message = message
        self.payload = payload
    
    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message or HTTP_STATUS_CODES[self.status_code]
        return rv


class BadRequestError(JsonErrorResponse):
    status_code = 400


class UnauthorizedError(JsonErrorResponse):
    status_code = 401


class BasicAuthUnauthorizedError(Exception):
    pass


class ServiceUnavailableError(JsonErrorResponse):
    status_code = 503


class SessionCreateReplicateError(ServiceUnavailableError):
    def __init__(self):
        super().__init__("Create Replicated Session Error")


class SessionExpiredError(BadRequestError):
    def __init__(self):
        super().__init__("Session Expired Error")


class JWTExpireError(BadRequestError):
    def __init__(self):
        super().__init__("Json Web Token Expired Error")


class JWTInvalidError(BadRequestError):
    def __init__(self):
        super().__init__("Invalid Json Web Token Error")


class NotAuthOTPError(UnauthorizedError):
    def __init__(self):
        super().__init__("No OTP Authorization Error")
