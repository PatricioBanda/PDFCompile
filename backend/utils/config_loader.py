import json
import os
from functools import lru_cache


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(BASE_DIR, "config")


@lru_cache
def load_json_config(filename: str) -> dict:
    """
    Carrega um ficheiro JSON da pasta backend/config.
    """
    path = os.path.join(CONFIG_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@lru_cache
def get_settings() -> dict:
    """
    Carrega settings.json (configuração geral).
    """
    return load_json_config("settings.json")
