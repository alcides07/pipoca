from typing import Any


def get_nested_attr(object: Any, path: str):
    attrs = path.split('.')
    for attr in attrs:
        if hasattr(object, attr):
            object = getattr(object, attr)
        else:
            return None
    return object
