from functools import wraps
from .exceptions import BadRequest, NotFound, InternalServerError
from fastapi.responses import JSONResponse


def pretty_resp(func):
    """Response wrapper function"""

    @wraps(func)
    def wrap(*args, **kwargs):
        try:
            _response: JSONResponse = func(*args, **kwargs)
            return _response
        except BadRequest as e:
            print(f"BadRequest: {e}")
            return JSONResponse(content={"error": str(e)}, status_code=400)
        except NotFound as e:
            print(f"NotFound: {e}")
            return JSONResponse(content={"error": str(e)}, status_code=404)
        except InternalServerError as e:
            print(f"InternalServerError: {e}")
            return JSONResponse(
                content={"error": "Internal server error"}, status_code=500
            )
        except Exception as e:
            print(f"Unhandled Exception: {e}")
            return JSONResponse(
                content={"error": "Internal server error"}, status_code=500
            )

    return wrap
