from __future__ import annotations

from decimal import Decimal
import json
from typing import final

from dtb.mapped_collection import MappedCollection
from pydantic import BaseModel

from .errors import EmptyCurrenciesError


@final
class Currency(BaseModel):
    code: str
    scale: float
    sign: str
    default: bool
    precision: Decimal = Decimal(".01")

    def __str__(self) -> str:
        return self.code

    def key(self) -> str:
        return self.code


@final
class CurrencyCollection(MappedCollection[Currency]):
    def __init__(self, currencies: list[Currency]) -> None:
        """
        :raises EmptyCurrenciesError:
        """
        super().__init__(currencies)

        if not currencies:
            raise EmptyCurrenciesError

        self._default_currency = currencies[0]

        defaults = [x for x in currencies if x.default]
        if defaults:
            self._default_currency = defaults[0]

    @classmethod
    def from_json_file(cls, file_name: str) -> CurrencyCollection:
        data = json.load(open(file_name))
        return cls([Currency.parse_obj(x) for x in data])

    def default(self) -> Currency:
        return self._default_currency

    def __eq__(self, other: object) -> bool:
        return (
            super().__eq__(other) and self._default_currency == other._default_currency
        )
