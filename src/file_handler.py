"""File I/O utility functions."""

import csv
import json
import os
from pathlib import Path


def read_text(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def write_text(filepath: str, content: str) -> None:
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def read_json(filepath: str) -> dict | list:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(filepath: str, data: dict | list, indent: int = 2) -> None:
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent)


def read_csv(filepath: str) -> list[dict]:
    with open(filepath, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_csv(filepath: str, data: list[dict]) -> None:
    if not data:
        return
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(data[0].keys())
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def file_exists(filepath: str) -> bool:
    return os.path.isfile(filepath)


def get_file_size(filepath: str) -> int:
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    return os.path.getsize(filepath)


def list_files(directory: str, extension: str | None = None) -> list[str]:
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"Not a directory: {directory}")
    files = []
    for entry in os.scandir(directory):
        if entry.is_file():
            if extension is None or entry.name.endswith(extension):
                files.append(entry.name)
    return sorted(files)


def append_text(filepath: str, content: str) -> None:
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(content)
