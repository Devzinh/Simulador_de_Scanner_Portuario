import json
import os
from pathlib import Path

SAVE_FILE = Path(__file__).parent / "save_ebco.json"

SAVE_DEFAULTS = {
    "nome": "Inspetor",
    "strikes": 0,
    "total": 0,
    "acertos": 0,
    "erros": 0,
    "reputacao": 50,
    "casos_graves": 0,
    "falsos_alarmes": 0,
    "eficiencia": 100,
}


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

        if not isinstance(dados.get("nome"), str):
            return None

        for k in ("strikes", "total", "acertos", "erros"):
            if not isinstance(dados.get(k), int) or dados[k] < 0:
                return None

        # Migração transparente de saves antigos + validação do novo schema.
        dados_migrados = SAVE_DEFAULTS | dados

        for k in ("casos_graves", "falsos_alarmes", "eficiencia"):
            if not isinstance(dados_migrados.get(k), int) or dados_migrados[k] < 0:
                return None

        if not isinstance(dados_migrados.get("reputacao"), int):
            return None
        dados_migrados["reputacao"] = max(0, min(100, dados_migrados["reputacao"]))

        return dados_migrados
    except (json.JSONDecodeError, KeyError, OSError) as e:
        print(f"  [AVISO] Arquivo de save corrompido ou inacessível: {e}")
        return None


def _deletar_save():
    if SAVE_FILE.exists():
        try:
            SAVE_FILE.unlink()
        except OSError:
            pass
