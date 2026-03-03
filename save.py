import json
import os
from pathlib import Path

SAVE_FILE = Path(__file__).parent / "save_ebco.json"

def _salvar(dados: dict):
    temp_file = SAVE_FILE.with_suffix(".tmp")
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_file, SAVE_FILE)
    except OSError as e:
        print(f"  [ERRO] Falha ao salvar o progresso: {e}")
        if temp_file.exists():
            temp_file.unlink(missing_ok=True)

def _carregar() -> dict | None:
    if not SAVE_FILE.exists():
        return None
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            dados = json.load(f)
            
        if not isinstance(dados, dict):
            return None
            
        expected_keys = {"nome", "strikes", "total", "acertos", "erros"}
        if not expected_keys.issubset(dados.keys()):
            return None
            
        if not isinstance(dados["nome"], str):
            return None
            
        for k in ("strikes", "total", "acertos", "erros"):
            if not isinstance(dados[k], int) or dados[k] < 0:
                return None
                
        return dados
    except (json.JSONDecodeError, KeyError, OSError) as e:
        print(f"  [AVISO] Arquivo de save corrompido ou inacessível: {e}")
        return None

def _deletar_save():
    if SAVE_FILE.exists():
        try:
            SAVE_FILE.unlink()
        except OSError:
            pass
