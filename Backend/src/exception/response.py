
from typing import Any


def error_response(
    message: str,
    error_code: str,
    details: Any = None,
):
    return {
        "success": False,
        "error": {
            "code": error_code,
            "message": message,
            "details": details,
        },
    }