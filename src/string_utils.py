"""String manipulation utility functions."""

import re
from collections import Counter


def reverse(s: str) -> str:
    return s[::-1]


def is_palindrome(s: str) -> bool:
    cleaned = re.sub(r"[^a-zA-Z0-9]", "", s).lower()
    return cleaned == cleaned[::-1]


def capitalize_words(s: str) -> str:
    return " ".join(word.capitalize() for word in s.split())


def count_vowels(s: str) -> int:
    return sum(1 for ch in s.lower() if ch in "aeiou")


def count_consonants(s: str) -> int:
    return sum(1 for ch in s.lower() if ch.isalpha() and ch not in "aeiou")


def truncate(s: str, max_length: int, suffix: str = "...") -> str:
    if len(s) <= max_length:
        return s
    return s[: max_length - len(suffix)] + suffix


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def char_frequency(s: str) -> dict[str, int]:
    return dict(Counter(s))


def is_anagram(s1: str, s2: str) -> bool:
    clean1 = re.sub(r"\s", "", s1).lower()
    clean2 = re.sub(r"\s", "", s2).lower()
    return sorted(clean1) == sorted(clean2)


def wrap_text(text: str, width: int) -> str:
    if width <= 0:
        raise ValueError("Width must be positive")
    words = text.split()
    lines: list[str] = []
    current_line: list[str] = []
    current_length = 0
    for word in words:
        if current_length + len(word) + len(current_line) > width:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_length = len(word)
        else:
            current_line.append(word)
            current_length += len(word)
    if current_line:
        lines.append(" ".join(current_line))
    return "\n".join(lines)
