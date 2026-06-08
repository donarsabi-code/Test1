"""Tests for the validators module."""

from src.validators import (
    is_strong_password,
    is_valid_credit_card,
    is_valid_date,
    is_valid_email,
    is_valid_hex_color,
    is_valid_ip,
    is_valid_phone,
    is_valid_url,
)


class TestIsValidEmail:
    def test_valid(self):
        assert is_valid_email("user@example.com") is True

    def test_valid_with_dots(self):
        assert is_valid_email("first.last@example.co.uk") is True

    def test_missing_at(self):
        assert is_valid_email("userexample.com") is False

    def test_missing_domain(self):
        assert is_valid_email("user@") is False

    def test_empty(self):
        assert is_valid_email("") is False

    def test_special_chars(self):
        assert is_valid_email("user+tag@example.com") is True


class TestIsValidUrl:
    def test_http(self):
        assert is_valid_url("http://example.com") is True

    def test_https(self):
        assert is_valid_url("https://example.com") is True

    def test_with_path(self):
        assert is_valid_url("https://example.com/path/to/page") is True

    def test_no_scheme(self):
        assert is_valid_url("example.com") is False

    def test_ftp(self):
        assert is_valid_url("ftp://example.com") is False

    def test_empty(self):
        assert is_valid_url("") is False


class TestIsValidPhone:
    def test_basic(self):
        assert is_valid_phone("1234567890") is True

    def test_with_country_code(self):
        assert is_valid_phone("+1 234 567 890") is True

    def test_with_dashes(self):
        assert is_valid_phone("123-456-7890") is True

    def test_with_parens(self):
        assert is_valid_phone("(123) 456-7890") is True

    def test_too_short(self):
        assert is_valid_phone("123") is False

    def test_letters(self):
        assert is_valid_phone("abc-def-ghij") is False


class TestIsStrongPassword:
    def test_strong(self):
        assert is_strong_password("Str0ng!Pass") is True

    def test_too_short(self):
        assert is_strong_password("S1!a") is False

    def test_no_uppercase(self):
        assert is_strong_password("str0ng!pass") is False

    def test_no_lowercase(self):
        assert is_strong_password("STR0NG!PASS") is False

    def test_no_digit(self):
        assert is_strong_password("Strong!Pass") is False

    def test_no_special(self):
        assert is_strong_password("Str0ngPass1") is False


class TestIsValidDate:
    def test_valid(self):
        assert is_valid_date("2024-01-15") is True

    def test_invalid_format(self):
        assert is_valid_date("15/01/2024") is False

    def test_custom_format(self):
        assert is_valid_date("15/01/2024", "%d/%m/%Y") is True

    def test_invalid_date(self):
        assert is_valid_date("2024-13-01") is False

    def test_empty(self):
        assert is_valid_date("") is False


class TestIsValidIp:
    def test_valid(self):
        assert is_valid_ip("192.168.1.1") is True

    def test_loopback(self):
        assert is_valid_ip("127.0.0.1") is True

    def test_zeros(self):
        assert is_valid_ip("0.0.0.0") is True

    def test_max(self):
        assert is_valid_ip("255.255.255.255") is True

    def test_out_of_range(self):
        assert is_valid_ip("256.1.1.1") is False

    def test_too_few_octets(self):
        assert is_valid_ip("192.168.1") is False

    def test_leading_zeros(self):
        assert is_valid_ip("192.168.01.1") is False

    def test_non_numeric(self):
        assert is_valid_ip("abc.def.ghi.jkl") is False


class TestIsValidHexColor:
    def test_six_digit(self):
        assert is_valid_hex_color("#ff00aa") is True

    def test_three_digit(self):
        assert is_valid_hex_color("#f0a") is True

    def test_uppercase(self):
        assert is_valid_hex_color("#FF00AA") is True

    def test_no_hash(self):
        assert is_valid_hex_color("ff00aa") is False

    def test_invalid_length(self):
        assert is_valid_hex_color("#ff00a") is False

    def test_invalid_chars(self):
        assert is_valid_hex_color("#gggggg") is False


class TestIsValidCreditCard:
    def test_valid_visa(self):
        assert is_valid_credit_card("4111111111111111") is True

    def test_valid_with_spaces(self):
        assert is_valid_credit_card("4111 1111 1111 1111") is True

    def test_valid_with_dashes(self):
        assert is_valid_credit_card("4111-1111-1111-1111") is True

    def test_invalid_luhn(self):
        assert is_valid_credit_card("4111111111111112") is False

    def test_too_short(self):
        assert is_valid_credit_card("411111") is False

    def test_non_numeric(self):
        assert is_valid_credit_card("abcdefghijklmnop") is False

    def test_empty(self):
        assert is_valid_credit_card("") is False

    def test_mastercard(self):
        # 5500000000000004 is a standard test Mastercard — triggers n>9 in Luhn
        assert is_valid_credit_card("5500000000000004") is True
