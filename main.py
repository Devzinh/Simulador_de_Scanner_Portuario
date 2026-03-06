import csv
import json
import random
from datetime import datetime
from pathlib import Path

from motor import gerar_conteiner, simular_scanner
from eventos import tomar_decisao
from save import _salvar, _carregar, _deletar_save, _sanitizar_nome

W = 62
REPORT_DIR = Path(__file__).parent / "reports"

DIFICULDADES = {
    "1": {
        "nome": "Treinamento",
        "max_strikes": 4,
        "risco_escala": 0.85,
        "suspeito_escala": 0.80,
        "pressao_operacional": 0.85,
    },
    "2": {
        "nome": "Operacional",
        "max_strikes": 3,
        "risco_escala": 1.0,
        "suspeito_escala": 1.0,
        "pressao_operacional": 1.0,
    },
    "3": {
        "nome": "Crítico",
        "max_strikes": 2,
        "risco_escala": 1.15,
        "suspeito_escala": 1.25,
        "pressao_operacional": 1.20,
    },
}


def _c(texto, codigo, tema_ansi=False):
    if not tema_ansi:
        return texto
    return f"\033[{codigo}m{texto}\033[0m"


def _box(linhas, char_topo="═", char_lado="║", tema_ansi=False):
    borda = char_topo * (W - 2)
    print(_c(f"╔{borda}╗", "36", tema_ansi))
    for linha in linhas:
        texto = linha[:W - 4]
        print(_c(f"{char_lado} {texto.center(W - 4)} {char_lado}", "36", tema_ansi))
    print(_c(f"╚{borda}╝", "36", tema_ansi))


def _sep(char="─", tema_ansi=False):
    print(_c(char * W, "90", tema_ansi))


def _gerar_contexto_operacional():
    portos = [
        ("SANTOS", "SP"),
        ("ITAJAÍ", "SC"),
        ("PARANAGUÁ", "PR"),
        ("SUAPE", "PE"),
        ("PECÉM", "CE"),
        ("MANAUS", "AM"),
        ("VITÓRIA", "ES"),
        ("RIO DE JANEIRO", "RJ"),
        ("SALVADOR", "BA"),
        ("RIO GRANDE", "RS"),
    ]
    turnos = ["MATUTINO", "VESPERTINO", "NOTURNO"]
    fiscalizacoes = [
        "TRIAGEM ADUANEIRA DE RISCO",
        "OPERAÇÃO DE CONTRABANDO E DESCAMINHO",
        "FISCALIZAÇÃO DE CARGA PERIGOSA",
        "BLOCO DE INSPEÇÃO ALFANDEGÁRIA REFORÇADA",
    ]
    porto_nome, porto_uf = random.choice(portos)
    return {
        "porto_nome": porto_nome,
        "porto_uf": porto_uf,
        "turno": random.choice(turnos),
        "fiscalizacao": random.choice(fiscalizacoes),
    }


def _escolher_dificuldade():
    print("\n  Nível de dificuldade:")
    print("   [1] Treinamento  (mais tolerante)")
    print("   [2] Operacional  (padrão)")
    print("   [3] Crítico      (mais severo)")
    while True:
        escolha = input("\n  Escolha (1/2/3): ").strip()
        if escolha in DIFICULDADES:
            return DIFICULDADES[escolha]
        print("  Opção inválida.")


def _escolher_seed():
    raw = input("  Seed opcional (ENTER = aleatório): ").strip()
    if not raw:
        return None
    if raw.lstrip("-").isdigit():
        return int(raw)
    print("  Seed inválida. Usando aleatório.")
    return None


def _estado_inicial(nome, dificuldade_nome, seed):
    return {
        "nome": nome,
        "strikes": 0,
        "total": 0,
        "acertos": 0,
        "erros": 0,
        "reputacao": 50,
        "casos_graves": 0,
        "falsos_alarmes": 0,
        "eficiencia": 100,
        "dificuldade": dificuldade_nome,
        "seed": seed,
    }


def _chance_bonus_inteligencia(estado_jogador):
    if estado_jogador["reputacao"] < 75:
        return False
    chance = min(0.6, 0.20 + estado_jogador["casos_graves"] * 0.02)
    return random.random() < chance


def _hud_strikes(nome, strikes, max_strikes, estado_jogador, tema_ansi=False):
    restantes = max_strikes - strikes
    icones = "🟥" * strikes + "⬜" * max(0, restantes)
    _sep(tema_ansi=tema_ansi)
    print(f"  Inspetor: {nome:<16}  Advertências: {icones}  ({strikes}/{max_strikes})")
    print(f"  Conteineres: {estado_jogador['total']:<5} Acertos: {estado_jogador['acertos']:<5} Erros: {estado_jogador['erros']}")
    print(
        f"  Reputação: {estado_jogador['reputacao']:>3}/100  "
        f"Casos graves: {estado_jogador['casos_graves']:<3}  "
        f"Falsos alarmes: {estado_jogador['falsos_alarmes']:<3}  "
        f"Eficiência: {estado_jogador['eficiencia']:>3}%"
    )
    _sep(tema_ansi=tema_ansi)


def _exportar_relatorio(estado_jogador, contexto):
    REPORT_DIR.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = f"relatorio_{stamp}"
    relatorio = {
        "gerado_em": datetime.now().isoformat(timespec="seconds"),
        "porto": f"{contexto['porto_nome']} - {contexto['porto_uf']}",
        "turno": contexto["turno"],
        "fiscalizacao": contexto["fiscalizacao"],
        "estado_final": estado_jogador,
    }

    json_path = REPORT_DIR / f"{base}.json"
    csv_path = REPORT_DIR / f"{base}.csv"

    json_path.write_text(json.dumps(relatorio, ensure_ascii=False, indent=2), encoding="utf-8")
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["campo", "valor"])
        writer.writerow(["gerado_em", relatorio["gerado_em"]])
        writer.writerow(["porto", relatorio["porto"]])
        writer.writerow(["turno", relatorio["turno"]])
        writer.writerow(["fiscalizacao", relatorio["fiscalizacao"]])
        for k, v in estado_jogador.items():
            writer.writerow([k, v])

    print(f"\n  📄 Relatório exportado:")
    print(f"     - {json_path}")
    print(f"     - {csv_path}")


def _intro(tema_ansi=False):
    hoje = datetime.today().strftime("%d/%m/%Y")
    contexto = _gerar_contexto_operacional()

    _box([
        "",
        "E B C O  S Y S T E M S",
        "Empresa Brasileira de Controle Portuário",
        "Sistema de Inspeção e Rastreio de Cargas",
        "",
        f"DATA: {hoje}   TURNO: {contexto['turno']}",
        f"TERMINAL: PORTO DE {contexto['porto_nome']} — {contexto['porto_uf']}",
        f"MISSÃO: {contexto['fiscalizacao']}",
        "",
    ], tema_ansi=tema_ansi)

    input("\n  Pressione ENTER para continuar...")
    print()
    nome = _sanitizar_nome(input("  Antes de começar, qual é o seu nome, inspetor? "))
    dificuldade = _escolher_dificuldade()
    seed = _escolher_seed()
    if seed is not None:
        random.seed(seed)
        print(f"  Seed aplicada: {seed}")

    _sep(tema_ansi=tema_ansi)
    print(f"\n  Bem-vindo, Inspetor {nome}.")
    print(f"  Dificuldade: {dificuldade['nome']}")
    _sep(tema_ansi=tema_ansi)
    input("\n  Pressione ENTER para iniciar o turno...")
    return nome, contexto, dificuldade, seed


def _game_over(nome, strikes_total, contexto, tema_ansi=False):
    print()
    _box([
        "",
        "⛔   G A M E   O V E R   ⛔",
        "",
        f"Inspetor {nome}",
        f"{strikes_total} infrações graves registradas em prontuário.",
        "",
        "Você foi afastado com efeito imediato.",
        f"Porto de {contexto['porto_nome']} — {contexto['porto_uf']} ({contexto['turno'].lower()}).",
        "",
    ], tema_ansi=tema_ansi)
    print()


def main():
    tema_ansi = input("Tema ANSI colorido? (s/n): ").strip().lower() == "s"
    save = _carregar()
    contexto = None
    dificuldade = DIFICULDADES["2"]
    max_strikes = dificuldade["max_strikes"]

    if save:
        try:
            nome = _sanitizar_nome(save.get("nome", ""))
            if save.get("seed") is not None:
                random.seed(save["seed"])
            if save.get("dificuldade") in {d["nome"] for d in DIFICULDADES.values()}:
                dificuldade = next(d for d in DIFICULDADES.values() if d["nome"] == save["dificuldade"])
                max_strikes = dificuldade["max_strikes"]

            _sep(tema_ansi=tema_ansi)
            print("  💾 SAVE ENCONTRADO")
            print(f"  Inspetor    : {nome}")
            print(f"  Dificuldade : {save.get('dificuldade', 'Operacional')}")
            print(f"  Advertências: {save['strikes']}/{max_strikes}   Conteineres: {save['total']}   Acertos: {save['acertos']}")
            _sep(tema_ansi=tema_ansi)

            while True:
                resp = input("\n  Continuar partida salva? (s/n): ").strip().lower()
                if resp in ('s', 'n'):
                    break
                print("  Opção inválida.")

            if resp == "s":
                estado_jogador = dict(save)
                estado_jogador["nome"] = nome
                contexto = _gerar_contexto_operacional()
                print(f"\n  Bem-vindo de volta, Inspetor {nome}.\n")
            else:
                _deletar_save()
                nome, contexto, dificuldade, seed = _intro(tema_ansi=tema_ansi)
                max_strikes = dificuldade["max_strikes"]
                estado_jogador = _estado_inicial(nome, dificuldade["nome"], seed)
        except KeyError:
            print("\n  [AVISO] Dados do save estão incompletos. Iniciando nova partida.")
            _deletar_save()
            save = None

    if not save or contexto is None:
        nome, contexto, dificuldade, seed = _intro(tema_ansi=tema_ansi)
        max_strikes = dificuldade["max_strikes"]
        estado_jogador = _estado_inicial(nome, dificuldade["nome"], seed)

    primeiro = True
    salvo_status = "not_attempted"
    try:
        while True:
            if not primeiro:
                input(f"\n  [{nome}] Pressione ENTER para escanear o próximo conteiner...")
            primeiro = False

            c = gerar_conteiner(
                risco_escala=dificuldade["risco_escala"],
                suspeito_escala=dificuldade["suspeito_escala"],
            )
            alertas, suspeitos = simular_scanner(c)

            if _chance_bonus_inteligencia(estado_jogador) and suspeitos:
                dica = random.choice(suspeitos)
                alertas = alertas + [f"INTEL EBCO: rota com histórico ligado a '{dica}'."]
                print("\n  🛰 Inteligência prévia adicionou um alerta contextual ao scanner.")

            efeitos = tomar_decisao(
                c,
                alertas,
                suspeitos,
                estado_jogador,
                pressao_operacional=dificuldade["pressao_operacional"],
            )

            estado_jogador["total"] += 1
            if efeitos["ganhou_strike"]:
                estado_jogador["strikes"] += 1
                estado_jogador["erros"] += 1
            else:
                estado_jogador["acertos"] += 1

            salvo_status = "success" if _salvar(dict(estado_jogador)) else "failed"
            _hud_strikes(nome, estado_jogador["strikes"], max_strikes, estado_jogador, tema_ansi=tema_ansi)

            if estado_jogador["strikes"] >= max_strikes:
                _game_over(nome, estado_jogador["strikes"], contexto, tema_ansi=tema_ansi)
                _exportar_relatorio(estado_jogador, contexto)
                _deletar_save()
                break

            while True:
                continuar = input("  Deseja inspecionar o próximo conteiner? (s/n): ").strip().lower()
                if continuar in ('s', 'n'):
                    break
                print("  Opção inválida.")

            if continuar == "n":
                msg_salvo = "Progresso salvo." if salvo_status == "success" else "ATENÇÃO: Falha ao salvar o progresso."
                print(
                    f"\n  Turno {contexto['turno'].lower()} encerrado no Porto de "
                    f"{contexto['porto_nome']} — {contexto['porto_uf']}. "
                    f"Até amanhã, {nome}. {msg_salvo}\n"
                )
                _exportar_relatorio(estado_jogador, contexto)
                break
    except KeyboardInterrupt:
        print("\n\n  [SISTEMA INTERROMPIDO] Encerrando turno e exportando relatório...")
        _exportar_relatorio(estado_jogador, contexto)


if __name__ == "__main__":
    main()
