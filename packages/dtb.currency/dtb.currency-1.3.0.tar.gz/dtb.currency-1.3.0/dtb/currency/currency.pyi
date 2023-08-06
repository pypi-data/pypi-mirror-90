from __future__ import annotations

from decimal import Decimal
import json
from typing import final

from dtb.mapped_collection import MappedCollection
from pydantic import BaseModel

@final
class Currency(BaseModel):
    code: str
    scale: float
    sign: str
    default: bool
    precision: Decimal = Decimal(".01")

    def __str__(self) -> str:
        ...

    def key(self) -> str:
        ...


@final
class CurrencyCollection(MappedCollection[Currency]):
    _default_currency: Currency

    def __init__(self, currencies: list[Currency]) -> None:
        ...

    @classmethod
    def from_json_file(cls, file_name: str) -> CurrencyCollection:
        ...

    def default(self) -> Currency:
        ...
