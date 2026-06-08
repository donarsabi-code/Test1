"""Tests for the data_processor module."""

import pytest

from src.data_processor import (
    chunk,
    deep_merge,
    flatten,
    group_by,
    invert_dict,
    paginate,
    pluck,
    sort_by_key,
    transpose,
    unique,
)


class TestFlatten:
    def test_flat_list(self):
        assert flatten([1, 2, 3]) == [1, 2, 3]

    def test_nested_list(self):
        assert flatten([1, [2, 3], [4, [5]]]) == [1, 2, 3, 4, 5]

    def test_deeply_nested(self):
        assert flatten([[[1]], [[2, [3]]]]) == [1, 2, 3]

    def test_empty(self):
        assert flatten([]) == []

    def test_mixed_types(self):
        assert flatten([1, ["a", [True]]]) == [1, "a", True]


class TestChunk:
    def test_even_split(self):
        assert chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]

    def test_uneven_split(self):
        assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]

    def test_size_larger_than_list(self):
        assert chunk([1, 2], 5) == [[1, 2]]

    def test_empty_list(self):
        assert chunk([], 3) == []

    def test_invalid_size(self):
        with pytest.raises(ValueError):
            chunk([1], 0)

    def test_negative_size(self):
        with pytest.raises(ValueError):
            chunk([1], -1)


class TestUnique:
    def test_with_duplicates(self):
        assert unique([1, 2, 2, 3, 1]) == [1, 2, 3]

    def test_no_duplicates(self):
        assert unique([1, 2, 3]) == [1, 2, 3]

    def test_empty(self):
        assert unique([]) == []

    def test_preserves_order(self):
        assert unique([3, 1, 2, 1, 3]) == [3, 1, 2]


class TestGroupBy:
    def test_basic(self):
        items = [
            {"type": "a", "val": 1},
            {"type": "b", "val": 2},
            {"type": "a", "val": 3},
        ]
        result = group_by(items, "type")
        assert len(result["a"]) == 2
        assert len(result["b"]) == 1

    def test_missing_key(self):
        items = [{"val": 1}, {"type": "a", "val": 2}]
        result = group_by(items, "type")
        assert "" in result
        assert "a" in result

    def test_empty(self):
        assert group_by([], "key") == {}


class TestDeepMerge:
    def test_simple(self):
        assert deep_merge({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}

    def test_override(self):
        assert deep_merge({"a": 1}, {"a": 2}) == {"a": 2}

    def test_nested(self):
        base = {"a": {"x": 1, "y": 2}}
        override = {"a": {"y": 3, "z": 4}}
        result = deep_merge(base, override)
        assert result == {"a": {"x": 1, "y": 3, "z": 4}}

    def test_override_dict_with_scalar(self):
        assert deep_merge({"a": {"x": 1}}, {"a": 5}) == {"a": 5}

    def test_empty_base(self):
        assert deep_merge({}, {"a": 1}) == {"a": 1}

    def test_no_mutation_of_base(self):
        base = {"a": {"x": 1}}
        result = deep_merge(base, {"b": 2})
        result["a"]["x"] = 99
        assert base["a"]["x"] == 1


class TestPluck:
    def test_basic(self):
        items = [{"name": "a"}, {"name": "b"}]
        assert pluck(items, "name") == ["a", "b"]

    def test_missing_key(self):
        items = [{"name": "a"}, {"age": 1}]
        assert pluck(items, "name") == ["a", None]

    def test_empty(self):
        assert pluck([], "key") == []


class TestInvertDict:
    def test_basic(self):
        assert invert_dict({"a": 1, "b": 2}) == {1: "a", 2: "b"}

    def test_empty(self):
        assert invert_dict({}) == {}


class TestSortByKey:
    def test_ascending(self):
        items = [{"n": 3}, {"n": 1}, {"n": 2}]
        result = sort_by_key(items, "n")
        assert [i["n"] for i in result] == [1, 2, 3]

    def test_descending(self):
        items = [{"n": 3}, {"n": 1}, {"n": 2}]
        result = sort_by_key(items, "n", reverse=True)
        assert [i["n"] for i in result] == [3, 2, 1]

    def test_missing_key_uses_default(self):
        items = [{"n": "b"}, {"n": "a"}, {"x": "c"}]
        result = sort_by_key(items, "n")
        assert result[0] == {"x": "c"}  # "" sorts first


class TestPaginate:
    def test_first_page(self):
        result = paginate(list(range(10)), page=1, per_page=3)
        assert result["items"] == [0, 1, 2]
        assert result["total"] == 10
        assert result["total_pages"] == 4

    def test_last_page(self):
        result = paginate(list(range(10)), page=4, per_page=3)
        assert result["items"] == [9]

    def test_out_of_range(self):
        result = paginate(list(range(5)), page=10, per_page=3)
        assert result["items"] == []

    def test_invalid_page(self):
        with pytest.raises(ValueError):
            paginate([1], page=0, per_page=1)

    def test_invalid_per_page(self):
        with pytest.raises(ValueError):
            paginate([1], page=1, per_page=0)


class TestTranspose:
    def test_basic(self):
        matrix = [[1, 2], [3, 4], [5, 6]]
        assert transpose(matrix) == [[1, 3, 5], [2, 4, 6]]

    def test_single_row(self):
        assert transpose([[1, 2, 3]]) == [[1], [2], [3]]

    def test_empty(self):
        assert transpose([]) == []
