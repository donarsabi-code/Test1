"""Data transformation and processing utilities."""

from typing import Any


def flatten(nested: list) -> list:
    result: list = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def chunk(lst: list, size: int) -> list[list]:
    if size <= 0:
        raise ValueError("Chunk size must be positive")
    return [lst[i : i + size] for i in range(0, len(lst), size)]


def unique(lst: list) -> list:
    seen: set = set()
    result: list = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def group_by(items: list[dict], key: str) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = {}
    for item in items:
        k = str(item.get(key, ""))
        groups.setdefault(k, []).append(item)
    return groups


def deep_merge(base: dict, override: dict) -> dict:
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def pluck(items: list[dict], key: str) -> list[Any]:
    return [item.get(key) for item in items]


def invert_dict(d: dict) -> dict:
    return {v: k for k, v in d.items()}


def sort_by_key(items: list[dict], key: str, reverse: bool = False) -> list[dict]:
    return sorted(items, key=lambda x: x.get(key, ""), reverse=reverse)


def paginate(items: list, page: int, per_page: int) -> dict:
    if page < 1 or per_page < 1:
        raise ValueError("Page and per_page must be positive integers")
    total = len(items)
    total_pages = (total + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    return {
        "items": items[start:end],
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
    }


def transpose(matrix: list[list]) -> list[list]:
    if not matrix:
        return []
    return [list(row) for row in zip(*matrix)]
