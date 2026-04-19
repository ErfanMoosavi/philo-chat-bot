import json
from pathlib import Path


class PhiloChat:
    def __init__(self):
        self.philosophers = self._load_philosophers()

    def get_philosophers(self) -> list[dict]:
        return self.philosophers

    def _find_philosopher(self, philosopher_id: int) -> dict:
        for p in self.philosophers:
            if p["id"] == philosopher_id:
                return p
        raise ValueError(f"Philosopher with id '{philosopher_id}' not found")

    def _load_philosophers(self) -> list[dict]:
        json_path = Path(__file__).parent.parent / "resources" / "philosophers.json"
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
