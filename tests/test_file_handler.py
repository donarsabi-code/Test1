"""Tests for the file_handler module."""

import json
import os
import tempfile

import pytest

from src.file_handler import (
    append_text,
    file_exists,
    get_file_size,
    list_files,
    read_csv,
    read_json,
    read_text,
    write_csv,
    write_json,
    write_text,
)


@pytest.fixture
def tmp_dir():
    with tempfile.TemporaryDirectory() as d:
        yield d


class TestReadWriteText:
    def test_write_and_read(self, tmp_dir):
        path = os.path.join(tmp_dir, "test.txt")
        write_text(path, "hello world")
        assert read_text(path) == "hello world"

    def test_creates_parent_dirs(self, tmp_dir):
        path = os.path.join(tmp_dir, "sub", "dir", "test.txt")
        write_text(path, "nested")
        assert read_text(path) == "nested"

    def test_overwrite(self, tmp_dir):
        path = os.path.join(tmp_dir, "test.txt")
        write_text(path, "first")
        write_text(path, "second")
        assert read_text(path) == "second"

    def test_read_nonexistent(self, tmp_dir):
        with pytest.raises(FileNotFoundError):
            read_text(os.path.join(tmp_dir, "nope.txt"))


class TestAppendText:
    def test_append(self, tmp_dir):
        path = os.path.join(tmp_dir, "test.txt")
        write_text(path, "hello")
        append_text(path, " world")
        assert read_text(path) == "hello world"

    def test_append_creates_file(self, tmp_dir):
        path = os.path.join(tmp_dir, "new.txt")
        append_text(path, "content")
        assert read_text(path) == "content"


class TestReadWriteJson:
    def test_dict(self, tmp_dir):
        path = os.path.join(tmp_dir, "data.json")
        data = {"key": "value", "num": 42}
        write_json(path, data)
        assert read_json(path) == data

    def test_list(self, tmp_dir):
        path = os.path.join(tmp_dir, "data.json")
        data = [1, 2, 3]
        write_json(path, data)
        assert read_json(path) == data

    def test_custom_indent(self, tmp_dir):
        path = os.path.join(tmp_dir, "data.json")
        write_json(path, {"a": 1}, indent=4)
        content = read_text(path)
        assert "    " in content

    def test_creates_parent_dirs(self, tmp_dir):
        path = os.path.join(tmp_dir, "nested", "data.json")
        write_json(path, {"a": 1})
        assert read_json(path) == {"a": 1}


class TestReadWriteCsv:
    def test_basic(self, tmp_dir):
        path = os.path.join(tmp_dir, "data.csv")
        data = [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]
        write_csv(path, data)
        result = read_csv(path)
        assert len(result) == 2
        assert result[0]["name"] == "Alice"
        assert result[1]["age"] == "25"

    def test_empty_data(self, tmp_dir):
        path = os.path.join(tmp_dir, "empty.csv")
        write_csv(path, [])
        assert not os.path.exists(path)

    def test_creates_parent_dirs(self, tmp_dir):
        path = os.path.join(tmp_dir, "nested", "data.csv")
        write_csv(path, [{"a": "1"}])
        assert read_csv(path) == [{"a": "1"}]


class TestFileExists:
    def test_existing(self, tmp_dir):
        path = os.path.join(tmp_dir, "test.txt")
        write_text(path, "x")
        assert file_exists(path) is True

    def test_nonexistent(self, tmp_dir):
        assert file_exists(os.path.join(tmp_dir, "nope.txt")) is False

    def test_directory(self, tmp_dir):
        assert file_exists(tmp_dir) is False


class TestGetFileSize:
    def test_basic(self, tmp_dir):
        path = os.path.join(tmp_dir, "test.txt")
        write_text(path, "12345")
        assert get_file_size(path) == 5

    def test_nonexistent(self, tmp_dir):
        with pytest.raises(FileNotFoundError):
            get_file_size(os.path.join(tmp_dir, "nope.txt"))


class TestListFiles:
    def test_basic(self, tmp_dir):
        write_text(os.path.join(tmp_dir, "a.txt"), "")
        write_text(os.path.join(tmp_dir, "b.py"), "")
        result = list_files(tmp_dir)
        assert result == ["a.txt", "b.py"]

    def test_filter_extension(self, tmp_dir):
        write_text(os.path.join(tmp_dir, "a.txt"), "")
        write_text(os.path.join(tmp_dir, "b.py"), "")
        assert list_files(tmp_dir, ".txt") == ["a.txt"]

    def test_empty_dir(self, tmp_dir):
        assert list_files(tmp_dir) == []

    def test_not_a_dir(self, tmp_dir):
        with pytest.raises(NotADirectoryError):
            list_files(os.path.join(tmp_dir, "nope"))
