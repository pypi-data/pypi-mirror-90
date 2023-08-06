from __future__ import annotations

from decimal import Decimal
from typing import Union, final

from dtb.currency import Currency

@final
class Money:
    amount: Decimal
    currency: Currency
    def __init__(self, amount: Union[Decimal, float, str], currency: Currency) -> None:
        ...

    def convert_to(self, currency: Currency) -> Money:
        ...

    def _quantized_amount(self) -> Decimal:
        ...

    def __eq__(self, other: object) -> bool:
        ...

    def __add__(self, other: Money) -> Money:
        ...

    def __sub__(self, other: Money) -> Money:
        ...

    def __str__(self) -> str:
        ...
