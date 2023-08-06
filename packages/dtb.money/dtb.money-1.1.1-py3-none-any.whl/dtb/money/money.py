from __future__ import annotations

from decimal import Decimal
from typing import Union, final

from dtb.currency import Currency


@final
class Money:
    def __init__(self, amount: Union[Decimal, float, str], currency: Currency) -> None:
        if not isinstance(amount, Decimal):
            amount = Decimal(amount)
        self.amount = amount
        self.currency = currency

    def convert_to(self, currency: Currency) -> Money:
        if currency == self.currency:
            return self

        if not self.amount:
            return Money(self.amount, currency)

        amount = self.amount * Decimal(self.currency.scale) / Decimal(currency.scale)
        return Money(amount, currency)

    def _quantized_amount(self) -> Decimal:
        return self.amount.quantize(self.currency.precision)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            raise NotImplementedError
        return self.amount == other.amount and self.currency == other.currency

    def __add__(self, other: Money) -> Money:
        return Money(self.amount + other.convert_to(self.currency).amount, self.currency)

    def __sub__(self, other: Money) -> Money:
        return Money(
            self.amount - other.convert_to(self.currency).amount, self.currency
        )

    def __str__(self) -> str:
        return f"{self._quantized_amount()} {self.currency}"

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self._quantized_amount()} {self.currency}>"
