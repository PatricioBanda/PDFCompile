import os
import hashlib
from datetime import datetime
from backend.core.automation.state_manager import StateManager


class RHScanner:

    def __init__(self, rh_root):
        self.rh_root = rh_root
        self.state_manager = StateManager(rh_root)

    def compute_file_hash(self, file_path):
        """
        Gera hash SHA256 de um ficheiro.
        """
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    def scan_month(self, year, month_key):
        """
        Scaneia os grupos 2..13 para um mês (ex: '07_2025').
        Atualiza o state_YYYY.json
        """

        # Carregar ou criar estado
        state = self.state_manager.load_state(year)
        self.state_manager.ensure_month(state, month_key)

        month_entry = state["months"][month_key]

        print(f"\n[SCAN] Iniciando scan para {month_key}")

        for group in range(2, 14):
            group_str = str(group)
            group_path = os.path.join(self.rh_root, str(group), month_key)

            group_info = month_entry["groups"][group_str]
            group_info["path"] = group_path
            group_info["files"] = []
            group_info["hash"] = ""
            group_info["status"] = "missing"

            if not os.path.exists(group_path):
                print(f" - Grupo {group}: pasta não encontrada.")
                continue

            files = [
                f for f in os.listdir(group_path)
                if f.lower().endswith((".pdf", ".jpg", ".jpeg", ".png", ".tif", ".tiff"))
            ]

            if not files:
                print(f" - Grupo {group}: sem ficheiros.")
                continue

            print(f" - Grupo {group}: {len(files)} ficheiro(s) encontrado(s).")

            total_hash_string = ""

            for fname in sorted(files):
                fpath = os.path.join(group_path, fname)

                # obter info
                fsize = os.path.getsize(fpath)
                mtime = datetime.fromtimestamp(os.path.getmtime(fpath)).isoformat()
                fhash = self.compute_file_hash(fpath)

                # registar no JSON
                group_info["files"].append({
                    "name": fname,
                    "size": fsize,
                    "modified": mtime,
                    "hash": fhash
                })

                total_hash_string += fhash

            # hash final do grupo (para detectar alterações)
            group_info["hash"] = hashlib.sha256(total_hash_string.encode()).hexdigest()
            group_info["status"] = "ok"
            # validação avançada será configurada no futuro por JSON
            print(f"   Estado: {group_info['status']}")

        # atualizar timestamp
        month_entry["last_scan"] = datetime.now().isoformat()
        self.state_manager.update_global_timestamp(state)

        # guardar estado atualizado
        self.state_manager.save_state(year, state)

        print(f"[SCAN] Concluído para {month_key}")
        return state["months"][month_key]
