import pytest

from currency import CurrencyCollection, EmptyCurrenciesError


def test_currency_collection(create_json_file, rub, usd):
    path = create_json_file("currencies.json", [rub.dict(), usd.dict()])

    collection = CurrencyCollection.from_json_file(path)

    assert collection == CurrencyCollection([rub, usd])
    assert collection.default().code == "RUB"


def test_currency_collection_empty(create_json_file):
    path = create_json_file("currencies.json", [])
    with pytest.raises(EmptyCurrenciesError):
        CurrencyCollection.from_json_file(path)
