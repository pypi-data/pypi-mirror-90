from dtb.currency import Currency
import pytest


@pytest.fixture
def rub() -> Currency:
    return Currency(code="RUB", scale=1, sign="₽", default=True)
