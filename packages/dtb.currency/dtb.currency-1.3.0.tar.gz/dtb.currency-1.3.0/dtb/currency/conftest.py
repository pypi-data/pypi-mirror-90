from pathlib import Path
from typing import Any, Callable

import pytest
import simplejson

from currency import Currency


@pytest.fixture
def rub() -> Currency:
    return Currency(code="RUB", scale=1, sign="₽", default=True)


@pytest.fixture
def usd() -> Currency:
    return Currency(code="USD", scale=80, sign="$", default=False)


@pytest.fixture
def create_json_file(tmp_path: Path) -> Callable[[str, Any], str]:
    def wrapper(filename: str, data: Any) -> str:
        path = tmp_path / filename
        path.write_text(simplejson.dumps(data))
        return str(path)

    return wrapper
