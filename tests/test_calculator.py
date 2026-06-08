"""Tests for the calculator module."""

import pytest

from src.calculator import (
    add,
    divide,
    factorial,
    gcd,
    is_prime,
    lcm,
    multiply,
    power,
    sqrt,
    subtract,
)


class TestBasicArithmetic:
    def test_add(self):
        assert add(2, 3) == 5
        assert add(-1, 1) == 0
        assert add(0, 0) == 0

    def test_subtract(self):
        assert subtract(5, 3) == 2
        assert subtract(3, 5) == -2

    def test_multiply(self):
        assert multiply(3, 4) == 12
        assert multiply(0, 100) == 0
        assert multiply(-2, 3) == -6

    def test_divide(self):
        assert divide(10, 2) == 5.0
        assert divide(7, 2) == 3.5

    def test_divide_by_zero(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(1, 0)


class TestPower:
    def test_basic(self):
        assert power(2, 3) == 8

    def test_zero_exponent(self):
        assert power(5, 0) == 1

    def test_negative_exponent(self):
        assert power(2, -1) == 0.5


class TestSqrt:
    def test_perfect_square(self):
        assert sqrt(9) == 3.0

    def test_zero(self):
        assert sqrt(0) == 0.0

    def test_negative(self):
        with pytest.raises(ValueError, match="negative"):
            sqrt(-1)


class TestFactorial:
    def test_zero(self):
        assert factorial(0) == 1

    def test_positive(self):
        assert factorial(5) == 120

    def test_one(self):
        assert factorial(1) == 1

    def test_negative(self):
        with pytest.raises(ValueError):
            factorial(-1)

    def test_non_integer(self):
        with pytest.raises(ValueError):
            factorial(2.5)


class TestIsPrime:
    def test_primes(self):
        assert is_prime(2) is True
        assert is_prime(7) is True
        assert is_prime(13) is True

    def test_non_primes(self):
        assert is_prime(1) is False
        assert is_prime(4) is False
        assert is_prime(9) is False

    def test_negative(self):
        assert is_prime(-5) is False

    def test_non_integer(self):
        assert is_prime(2.5) is False


class TestGcd:
    def test_basic(self):
        assert gcd(12, 8) == 4

    def test_coprime(self):
        assert gcd(7, 13) == 1

    def test_with_zero(self):
        assert gcd(5, 0) == 5

    def test_negative(self):
        assert gcd(-12, 8) == 4


class TestLcm:
    def test_basic(self):
        assert lcm(4, 6) == 12

    def test_with_zero(self):
        assert lcm(0, 5) == 0

    def test_same(self):
        assert lcm(7, 7) == 7

    def test_negative(self):
        assert lcm(-4, 6) == 12
