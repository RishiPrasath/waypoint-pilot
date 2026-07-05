from __future__ import annotations

from typing import Any


class MissingValue:
    def __repr__(self) -> str:
        return "<missing>"


MISSING = MissingValue()


def values_at(data: Any, path: str) -> Any:
    if "[*]" in path:
        prefix, suffix = path.split("[*]", 1)
        values = get_value(data, prefix)
        if not isinstance(values, list):
            return MISSING
        suffix = suffix.lstrip(".")
        if not suffix:
            return values
        return [get_value(item, suffix) for item in values]

    return get_value(data, path)


def get_value(data: Any, path: str) -> Any:
    current = data
    if path == "":
        return current

    for raw_token in path.split("."):
        current = _resolve_token(current, raw_token)
        if current is MISSING:
            return MISSING
    return current


def _resolve_token(current: Any, token: str) -> Any:
    while token:
        if "[" in token:
            field, rest = token.split("[", 1)
            if field:
                current = _resolve_field(current, field)
                if current is MISSING:
                    return MISSING
            index_text, token = rest.split("]", 1)
            if not isinstance(current, list):
                return MISSING
            try:
                current = current[int(index_text)]
            except (ValueError, IndexError):
                return MISSING
        else:
            return _resolve_field(current, token)
    return current


def _resolve_field(current: Any, field: str) -> Any:
    if isinstance(current, dict) and field in current:
        return current[field]
    return MISSING
