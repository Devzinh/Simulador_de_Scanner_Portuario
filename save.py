import json
import os
import re
import hmac
import hashlib
import secrets
from pathlib import Path

SAVE_FILE = Path(__file__).parent / "save_ebco.json"
_KEY_FILE = Path(__file__).parent / ".ebco_key"

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

_NOME_MAX_LEN = 40
_NOME_ALLOWLIST = re.compile(r"[^a-zA-ZÀ-ÿ0-9 .\-_]")
_ANSI_RE = re.compile(r"\x1b\[.*?[a-zA-Z]")
_CONTROL_RE = re.compile(r"[\x00-\x1f\x7f-\x9f]")


def _sanitizar_nome(raw: str) -> str:
    """Strip ANSI/control sequences, enforce allowlist, clamp length."""
    cleaned = _ANSI_RE.sub("", raw)
    cleaned = _CONTROL_RE.sub("", cleaned)
    cleaned = _NOME_ALLOWLIST.sub("", cleaned)
    cleaned = cleaned.strip()[:_NOME_MAX_LEN].strip()
    return cleaned or "Inspetor"


def _obter_chave() -> bytes:
    """Load or create a per-install HMAC key."""
    try:
        if _KEY_FILE.exists():
            return _KEY_FILE.read_bytes()
        chave = secrets.token_bytes(32)
        _KEY_FILE.write_bytes(chave)
        return chave
    except OSError as e:
        raise RuntimeError(f"Falha ao gerenciar chave de integridade: {e}")


def _assinar(payload_bytes: bytes) -> str:
    return hmac.new(_obter_chave(), payload_bytes, hashlib.sha256).hexdigest()


def _salvar(dados: dict) -> bool:
    dados["nome"] = _sanitizar_nome(dados.get("nome", ""))
    payload_json = json.dumps(dados, ensure_ascii=False, indent=2)
    
    try:
        sig = _assinar(payload_json.encode("utf-8"))
    except RuntimeError as e:
        print(f"  [ERRO] Não foi possível assinar o save: {e}")
        return False

    envelope = {"payload": dados, "sig": sig}

    temp_file = SAVE_FILE.with_suffix(".tmp")
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(envelope, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_file, SAVE_FILE)
        return True
    except OSError as e:
        print(f"  [ERRO] Falha ao salvar o progresso: {e}")
        if temp_file.exists():
            temp_file.unlink(missing_ok=True)
        return False


def _carregar() -> dict | None:
    if not SAVE_FILE.exists():
        return None
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)

        if not isinstance(raw, dict):
            return None

        # Legacy save without HMAC envelope — reject and reset
        if "payload" not in raw or "sig" not in raw:
            print("  [AVISO] Save em formato antigo detectado. Iniciando nova partida.")
            return None

        dados = raw["payload"]
        sig_esperada = raw["sig"]

        payload_json = json.dumps(dados, ensure_ascii=False, indent=2)
        
        try:
            sig_calculada = _assinar(payload_json.encode("utf-8"))
        except RuntimeError as e:
            print(f"  [AVISO] {e}. Dados rejeitados por segurança.")
            return None

        if not hmac.compare_digest(sig_esperada, sig_calculada):
            print("  [AVISO] Save adulterado detectado. Dados rejeitados.")
            return None

        if not isinstance(dados, dict):
            return None

        if not isinstance(dados.get("nome"), str):
            return None
        dados["nome"] = _sanitizar_nome(dados["nome"])

        for k in ("strikes", "total", "acertos", "erros"):
            if not isinstance(dados.get(k), int) or dados[k] < 0:
                return None

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
