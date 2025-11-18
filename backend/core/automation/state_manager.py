import json
import os
from backend.utils.path_utils import join_path, ensure_dir

class StateManager:
    def __init__(self, rh_root: str):
        self.state_root = join_path(rh_root, "state")
        ensure_dir(self.state_root)

    def _month_file(self, year: str, month_key: str):
        year_dir = join_path(self.state_root, year)
        ensure_dir(year_dir)
        return join_path(year_dir, f"{month_key}.json")

    def load_state(self, year: str, month_key: str):
        f = self._month_file(year, month_key)
        if not os.path.exists(f):
            return {}
        with open(f, "r", encoding="utf-8") as fp:
            return json.load(fp)

    def save_state(self, year: str, month_key: str, data: dict):
        f = self._month_file(year, month_key)
        with open(f, "w", encoding="utf-8") as fp:
            json.dump(data, fp, indent=2)
