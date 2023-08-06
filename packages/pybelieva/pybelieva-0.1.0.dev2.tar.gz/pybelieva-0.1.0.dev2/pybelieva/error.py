import inspect
from typing import Optional

__all__ = (
    "BadRequestException",
    "ForbiddenException",
    "HTTPException",
    "InternalServerErrorException",
    "PybelievaException",
    "TooManyRequestsException",
    "UnauthorizedException",
    "NotFoundException",
)


class PybelievaException(Exception):
    pass


class HTTPException(PybelievaException):
    def __init__(self, *, message: Optional[str] = None):
        msg = inspect.getdoc(type(self))
        if message is not None:
            msg += " " + message  # type: ignore
        return super().__init__(message)


class TooManyRequestsException(HTTPException):
    """You are sending requests too quickly."""

    def __init__(self, message: str, **kwargs):
        if retry_after := kwargs.get("retry_after"):
            message += f" Retry after {retry_after}ms."
        if kwargs.get("global"):
            message += " This is a global rate limit."
        return super().__init__(message=message)


class BadRequestException(HTTPException):
    """Your request is invalid."""


class UnauthorizedException(HTTPException):
    """Your API token is invalid."""


class ForbiddenException(HTTPException):
    """You do not have permission to access the requested resource."""


class NotFoundException(HTTPException):
    """The specified resource could not be found."""


class InternalServerErrorException(HTTPException):
    """We had a problem with our server. Try again later."""
