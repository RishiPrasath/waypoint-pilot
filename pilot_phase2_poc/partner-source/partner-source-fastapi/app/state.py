from app.seed.loader import load_seed_data
from app.seed.store import SeedDataStore

_STORE = load_seed_data()


def get_store() -> SeedDataStore:
    return _STORE


def reset_store() -> None:
    global _STORE
    _STORE = load_seed_data()
