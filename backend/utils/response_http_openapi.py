from typing import Any


def response_http_openapi(code: int | str, model: Any, description: str = ""):
    return {
        code: {"model": model, "description": description}
    }
