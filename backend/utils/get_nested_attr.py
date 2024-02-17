from typing import Any


def get_nested_attr(obj: Any, path: str):
    attrs = path.split('.')
    for attr in attrs:
        if hasattr(obj, attr):
            obj = getattr(object, attr)
        else:
            return None
    return obj
