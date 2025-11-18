import json
import os
from backend.utils.path_utils import ensure_dir, join_path

class StateManager:
    """
    Saves monthly scan/join state files into:
    RH/<year>/14/state/<month>.json
    """

    def __init__(self, rh_root: str):
        self.rh_root = rh_root
        self.state_root = join_path(rh_root, "14", "state")
        ensure_dir(self.state_root)

    def _state_file(self, year: str, month_key: str):
        return join_path(self.state_root, f"{month_key}.json")

    def load_state(self, year: str, month_key: str):
        path = self._state_file(year, month_key)
        if not os.path.exists(path):
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_state(self, year: str, month_key: str, data: dict):
        path = self._state_file(year, month_key)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def update_scan_info(self, year: str, month_key: str, groups: list):
        state = self.load_state(year, month_key)
        state["month"] = month_key
        state["groups"] = groups
        state["last_scan"] = "ok"
        self.save_state(year, month_key, state)
