class BadRequest(Exception):
    """Exception used to raise a 400 Bad Request"""


class NotFound(Exception):
    """Exception used to raise a 404 not found"""


class Conflict(Exception):
    """Exception used to raise a 409 Conflict"""


class InternalServerError(Exception):
    """Exception used to raise a 500 Internal Server Error"""
