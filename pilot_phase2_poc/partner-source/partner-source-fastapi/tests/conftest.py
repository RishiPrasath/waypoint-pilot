import pytest

from app.state import reset_store


@pytest.fixture(autouse=True)
def reset_seed_store() -> None:
    reset_store()


@pytest.fixture
def driver_2001_headers() -> dict[str, str]:
    return {"Authorization": "Bearer demo-driver-2001-token"}


@pytest.fixture
def driver_2002_headers() -> dict[str, str]:
    return {"Authorization": "Bearer demo-driver-2002-token"}


@pytest.fixture
def driver_2003_headers() -> dict[str, str]:
    return {"Authorization": "Bearer demo-driver-2003-token"}


@pytest.fixture
def csa_headers() -> dict[str, str]:
    return {"Authorization": "Bearer demo-csa-5001-token"}
