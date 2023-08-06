from decimal import Decimal
from typing import Union

from dtb.currency import Currency
import pytest

from money import Money

RUB = Currency(code="RUB", scale=1, sign="₽", default=True)
USD = Currency(code="USD", scale=80, sign="$", default=False)
EUR = Currency(code="EUR", scale=90, sign="€", default=False)


@pytest.mark.parametrize("amount", [1, 1.1, Decimal("1.1"), "1.1"])
def test_money_init(amount: Union[int, float, Decimal, str], rub):
    assert Money(amount, rub)


@pytest.mark.parametrize(
    ["money_from", "currency_to", "expected"],
    [
        (Money(1, USD), RUB, Money(80, RUB)),
        (Money(1, USD), USD, Money(1, USD)),
        (Money(0, USD), RUB, Money(0, RUB)),
        (Money(80, RUB), USD, Money(1, USD)),
    ],
)
def test_money_convert(money_from, currency_to, expected):
    assert money_from.convert_to(currency_to) == expected


@pytest.mark.parametrize(
    ["m1", "m2", "expected"],
    [(Money(1, RUB), Money(1, RUB), Money(2, RUB)), (Money(1, RUB), Money(1, USD), Money(81, RUB))],
)
def test_money_add(m1, m2, expected):
    assert m1 + m2 == expected


@pytest.mark.parametrize(
    ["m1", "m2", "expected"],
    [
        (Money(1, RUB), Money(1, RUB), Money(0, RUB)),
        (Money(1, RUB), Money(1, USD), Money(-79, RUB)),
    ],
)
def test_money_sub(m1, m2, expected):
    assert m1 - m2 == expected


@pytest.mark.parametrize(
    ["money", "expected"],
    [
        (Money(1, RUB), "1.00 RUB"),
        (Money(100.12, RUB), "100.12 RUB"),
        (Money(1, USD), "1.00 USD"),
    ],
)
def test_money_str(money, expected):
    assert str(money) == expected
