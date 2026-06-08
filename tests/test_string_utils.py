"""Tests for the string_utils module."""

import pytest

from src.string_utils import (
    capitalize_words,
    char_frequency,
    count_consonants,
    count_vowels,
    is_anagram,
    is_palindrome,
    reverse,
    slugify,
    truncate,
    wrap_text,
)


class TestReverse:
    def test_basic(self):
        assert reverse("hello") == "olleh"

    def test_empty(self):
        assert reverse("") == ""

    def test_single_char(self):
        assert reverse("a") == "a"


class TestIsPalindrome:
    def test_basic(self):
        assert is_palindrome("racecar") is True

    def test_with_spaces(self):
        assert is_palindrome("A man a plan a canal Panama") is True

    def test_not_palindrome(self):
        assert is_palindrome("hello") is False

    def test_with_punctuation(self):
        assert is_palindrome("Was it a car or a cat I saw?") is True


class TestCapitalizeWords:
    def test_basic(self):
        assert capitalize_words("hello world") == "Hello World"

    def test_already_capitalized(self):
        assert capitalize_words("Hello World") == "Hello World"

    def test_single_word(self):
        assert capitalize_words("hello") == "Hello"


class TestCountVowels:
    def test_basic(self):
        assert count_vowels("hello") == 2

    def test_no_vowels(self):
        assert count_vowels("rhythm") == 0

    def test_all_vowels(self):
        assert count_vowels("aeiou") == 5

    def test_uppercase(self):
        assert count_vowels("HELLO") == 2


class TestCountConsonants:
    def test_basic(self):
        assert count_consonants("hello") == 3

    def test_no_consonants(self):
        assert count_consonants("aeiou") == 0

    def test_with_numbers(self):
        assert count_consonants("h3llo") == 3


class TestTruncate:
    def test_no_truncation(self):
        assert truncate("hi", 10) == "hi"

    def test_truncation(self):
        assert truncate("hello world", 8) == "hello..."

    def test_custom_suffix(self):
        assert truncate("hello world", 7, "~") == "hello ~"


class TestSlugify:
    def test_basic(self):
        assert slugify("Hello World") == "hello-world"

    def test_special_chars(self):
        assert slugify("Hello, World!") == "hello-world"

    def test_multiple_spaces(self):
        assert slugify("  hello   world  ") == "hello-world"

    def test_underscores(self):
        assert slugify("hello_world") == "hello-world"


class TestCharFrequency:
    def test_basic(self):
        result = char_frequency("aab")
        assert result["a"] == 2
        assert result["b"] == 1

    def test_empty(self):
        assert char_frequency("") == {}


class TestIsAnagram:
    def test_basic(self):
        assert is_anagram("listen", "silent") is True

    def test_with_spaces(self):
        assert is_anagram("dormitory", "dirty room") is True

    def test_not_anagram(self):
        assert is_anagram("hello", "world") is False

    def test_case_insensitive(self):
        assert is_anagram("Tea", "Eat") is True


class TestWrapText:
    def test_basic(self):
        result = wrap_text("hello world foo", 11)
        assert result == "hello world\nfoo"

    def test_single_word_per_line(self):
        result = wrap_text("a b c", 1)
        assert result == "a\nb\nc"

    def test_invalid_width(self):
        with pytest.raises(ValueError):
            wrap_text("hi", 0)

    def test_empty(self):
        assert wrap_text("", 10) == ""
