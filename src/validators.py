"""Input validation utility functions."""

import re
from datetime import datetime


def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def is_valid_url(url: str) -> bool:
    pattern = r"^https?://[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})(?:/[^\s]*)?$"
    return bool(re.match(pattern, url))


def is_valid_phone(phone: str) -> bool:
    cleaned = re.sub(r"[\s\-().]+", "", phone)
    if cleaned.startswith("+"):
        cleaned = cleaned[1:]
    return cleaned.isdigit() and 7 <= len(cleaned) <= 15


def is_strong_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True


def is_valid_date(date_str: str, fmt: str = "%Y-%m-%d") -> bool:
    try:
        datetime.strptime(date_str, fmt)
        return True
    except ValueError:
        return False


def is_valid_ip(ip: str) -> bool:
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        num = int(part)
        if num < 0 or num > 255:
            return False
        if len(part) > 1 and part[0] == "0":
            return False
    return True


def is_valid_hex_color(color: str) -> bool:
    return bool(re.match(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$", color))


def is_valid_credit_card(number: str) -> bool:
    """Validate credit card number using Luhn algorithm."""
    digits = re.sub(r"\s|-", "", number)
    if not digits.isdigit() or len(digits) < 13 or len(digits) > 19:
        return False
    total = 0
    for i, d in enumerate(reversed(digits)):
        n = int(d)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0
