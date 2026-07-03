from app.seed.loader import load_seed_data


class ReadinessService:
    def check(self) -> dict[str, str]:
        store = load_seed_data()
        seed_data_loaded = bool(
            store.orders
            and store.drivers
            and store.assignments
            and store.status_events_by_order_id
        )

        return {
            "persistence": "UP",
            "seedData": "UP" if seed_data_loaded else "DOWN",
        }
