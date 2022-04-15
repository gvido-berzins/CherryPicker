from typing import Any, Callable

import pytest

from tests import DATA_DIR


@pytest.fixture
def load_data() -> Callable[[str], str]:
    def load_file(filename: str, ext: str = ".yaml") -> Any:
        return (DATA_DIR / f"{filename}{ext}").read_text()

    return load_file
