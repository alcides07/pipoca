from typing import Any


def http_response_openapi(code: int | str, model: Any, description: str = ""):
    return {
        code: {"model": model, "description": description}
    }
