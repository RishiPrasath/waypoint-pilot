import pytest

from app.state import reset_store


@pytest.fixture(autouse=True)
def reset_seed_store() -> None:
    reset_store()
