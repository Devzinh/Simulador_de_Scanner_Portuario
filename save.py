import json
from pathlib import Path

SAVE_FILE = Path(__file__).parent / "save_ebco.json"

def _salvar(dados: dict):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def _carregar() -> dict | None:
    if not SAVE_FILE.exists():
        return None
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, KeyError):
        return None

def _deletar_save():
    if SAVE_FILE.exists():
        SAVE_FILE.unlink()
