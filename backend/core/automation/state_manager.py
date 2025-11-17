import os
import json
from datetime import datetime

class StateManager:

    def __init__(self, rh_root):
        self.rh_root = rh_root  # Ex: C:/.../RH/
        self.status_path = os.path.join(rh_root, "14", "status")
        os.makedirs(self.status_path, exist_ok=True)

    def _get_state_file(self, year):
        return os.path.join(self.status_path, f"state_{year}.json")

    def initialize_state(self, year):
        """
        Cria o ficheiro de estado para um ano (state_YYYY.json)
        apenas com grupos 2..13 (Base Join).
        """
        state_file = self._get_state_file(year)

        state = {
            "year": year,
            "root_path": self.rh_root,
            "last_global_scan": None,
            "months": {}
        }

        with open(state_file, "w", encoding="utf8") as f:
            json.dump(state, f, indent=4)

        return state_file

    def load_state(self, year):
        """
        Carrega o ficheiro de estado existente ou cria um novo.
        """
        state_file = self._get_state_file(year)

        if not os.path.exists(state_file):
            return self.initialize_state(year)

        with open(state_file, "r", encoding="utf8") as f:
            return json.load(f)

    def save_state(self, year, state):
        """
        Guarda o ficheiro estado após atualizar os meses/grupos.
        """
        state_file = self._get_state_file(year)

        with open(state_file, "w", encoding="utf8") as f:
            json.dump(state, f, indent=4)

    def ensure_month(self, state, month_key):
        """
        Garante que o mês existe no ficheiro.
        month_key = '07_2025'
        """
        if month_key not in state["months"]:
            state["months"][month_key] = {
                "last_scan": None,
                "groups": {
                    str(i): {
                        "path": "",
                        "files": [],
                        "hash": "",
                        "status": "missing"
                    }
                    for i in range(2, 14)
                },
                "base_join": {
                    "exists": False,
                    "path": "",
                    "hash": "",
                    "generated_on": ""
                },
                "final_join": {
                    "exists": False,
                    "path": "",
                    "hash": "",
                    "generated_on": ""
                }
            }

    def update_global_timestamp(self, state):
        state["last_global_scan"] = datetime.now().isoformat()
