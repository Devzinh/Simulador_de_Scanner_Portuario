import random
from motor import gerar_conteiner, simular_scanner
from eventos import tomar_decisao
from save import _salvar, _carregar, _deletar_save

W = 62


def _box(linhas, char_topo="═", char_lado="║"):
    borda = char_topo * (W - 2)
    print(f"╔{borda}╗")
    for linha in linhas:
        texto = linha[:W - 4]
        print(f"{char_lado} {texto.center(W - 4)} {char_lado}")
    print(f"╚{borda}╝")


def _sep(char="─"):
    print(char * W)


def _titulo(texto):
    print(f"\n  ┌{'─' * (W - 4)}┐")
    print(f"  │ {texto:<{W-5}}│")
    print(f"  └{'─' * (W - 4)}┘")


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


# ── Loop principal ─────────────────────────────────────────────────────────────
def _intro():
    import datetime
    hoje = datetime.date.today().strftime("%d/%m/%Y")
    PORTOS = [
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
    TURNOS = ["MATUTINO", "VESPERTINO", "NOTURNO"]
    porto_nome, porto_uf = random.choice(PORTOS)
    turno = random.choice(TURNOS)
    _box([
        "",
        "E B C O  S Y S T E M S",
        "Empresa Brasileira de Controle Portuário",
        "Sistema de Inspeção e Rastreio de Cargas",
        "",
        f"DATA: {hoje}   TURNO: {turno}",
        f"TERMINAL: PORTO DE {porto_nome} — {porto_uf}",
        f"MISSÃO: {fiscalizacao}",
        "",
    ])

    input("\n  Pressione ENTER para continuar...")
    print()
    nome = input("  Antes de começar, qual é o seu nome, inspetor? ").strip() or "Inspetor"
    print()
    _sep()
    print(f"""
  Bem-vindo, Inspetor {nome}.

  Você foi designado para o Terminal de Escaneamento do Porto
  de {porto_nome} — {porto_uf}, em turno {turno.lower()}.

  A operação ativa desta rodada é: {fiscalizacao}.

  Seu trabalho é analisar os dados do scanner e decidir:

    [1]  Liberar o conteiner para seguir ao destino
    [2]  Reter para inspeção física pela equipe de campo
    [3]  Acionar autoridades imediatamente

  O scanner mostra itens e densidades — mas NÃO identifica
  o que é ilegal. Esse julgamento é inteiramente seu.

  Erros ficam registrados. Três infrações = demissão.
""")
    _sep()
    print()
    input("  Pressione ENTER para iniciar o turno...")
    print()
    return nome, contexto


def _game_over(nome, strikes_total, contexto):
    porto_nome = contexto["porto_nome"]
    porto_uf = contexto["porto_uf"]
    turno = contexto["turno"]
    print()
    _box([
        "",
        "⛔   G A M E   O V E R   ⛔",
        "",
        f"Inspetor {nome}",
        f"{strikes_total} infrações graves registradas em prontuário.",
        "",
        "A EBCO não pode manter um fiscal cujos erros",
        f"colocam em risco o Porto de {porto_nome} — {porto_uf}.",
        f"Escala crítica comprometida no turno {turno.lower()}.",
        "",
        "Você foi afastado com efeito imediato.",
        "Processo administrativo disciplinar aberto.",
        "",
    ])
    print()


def _hud_strikes(nome, strikes, max_strikes, total, acertos, erros, estado_jogador):
    restantes = max_strikes - strikes
    icones = "🟥" * strikes + "⬜" * restantes
    _sep()
    print(f"  Inspetor: {nome:<16}  Advertências: {icones}  ({strikes}/{max_strikes})")
    print(f"  Conteineres: {total:<5} Acertos: {acertos:<5} Erros: {erros}")
    print(
        f"  Reputação: {estado_jogador['reputacao']:>3}/100  "
        f"Casos graves: {estado_jogador['casos_graves']:<3}  "
        f"Falsos alarmes: {estado_jogador['falsos_alarmes']:<3}  "
        f"Eficiência: {estado_jogador['eficiencia']:>3}%"
    )
    _sep()


def _estado_inicial(nome):
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
    }


def _chance_bonus_inteligencia(estado_jogador):
    if estado_jogador["reputacao"] < 75:
        return False
    chance = min(0.6, 0.20 + estado_jogador["casos_graves"] * 0.02)
    return random.random() < chance


def main():
    max_strikes = 3
    save = _carregar()

    if save:
        try:
            print()
            _sep()
            print(f"  💾 SAVE ENCONTRADO")
            print(f"  Inspetor    : {save['nome']}")
            print(f"  Advertências: {save['strikes']}/{max_strikes}   Conteineres: {save['total']}   Acertos: {save['acertos']}")
            print(
                f"  Reputação   : {save['reputacao']}/100   "
                f"Casos graves: {save['casos_graves']}   "
                f"Falsos alarmes: {save['falsos_alarmes']}   "
                f"Eficiência: {save['eficiencia']}%"
            )
            _sep()

            while True:
                resp = input("\n  Continuar partida salva? (s/n): ").strip().lower()
                if resp in ('s', 'n'):
                    break
                print("  Opção inválida. Digite 's' para SIM ou 'n' para NÃO.")

            if resp == "s":
                estado_jogador = dict(save)
                nome = estado_jogador["nome"]
                print(f"\n  Bem-vindo de volta, Inspetor {nome}.\n")
            else:
                _deletar_save()
                nome = _intro()
                estado_jogador = _estado_inicial(nome)
        except KeyError:
            print("\n  [AVISO] Dados do save estão incompletos. Iniciando nova partida.")
            _deletar_save()
            save = None

    if not save:
        nome = _intro()
        estado_jogador = _estado_inicial(nome)

    primeiro = True
    try:
        while True:
            if not primeiro:
                input(f"\n  [{nome}] Pressione ENTER para escanear o próximo conteiner...")
            primeiro = False

            c = gerar_conteiner()
            alertas, suspeitos = simular_scanner(c)

            if _chance_bonus_inteligencia(estado_jogador) and suspeitos:
                dica = random.choice(suspeitos)
                alertas = alertas + [f"INTEL EBCO: rota com histórico ligado a '{dica}'."]
                print("\n  🛰 Inteligência prévia adicionou um alerta contextual ao scanner.")

            efeitos = tomar_decisao(c, alertas, suspeitos, estado_jogador)

            estado_jogador["total"] += 1
            if efeitos["ganhou_strike"]:
                estado_jogador["strikes"] += 1
                estado_jogador["erros"] += 1
            else:
                estado_jogador["acertos"] += 1

            _salvar(dict(estado_jogador))
            _hud_strikes(
                nome,
                estado_jogador["strikes"],
                max_strikes,
                estado_jogador["total"],
                estado_jogador["acertos"],
                estado_jogador["erros"],
                estado_jogador,
            )

            if estado_jogador["strikes"] >= max_strikes:
                _game_over(nome, estado_jogador["strikes"])
                _deletar_save()
                break

            while True:
                continuar = input("  Deseja inspecionar o próximo conteiner? (s/n): ").strip().lower()
                if continuar in ('s', 'n'):
                    break
                print("  Opção inválida. Digite 's' para SIM ou 'n' para NÃO.")

            if continuar == "n":
                print(
                    f"\n  Turno {contexto['turno'].lower()} encerrado no Porto de "
                    f"{contexto['porto_nome']} — {contexto['porto_uf']}. "
                    f"Até amanhã, {nome}. Progresso salvo.\n"
                )
                break
    except KeyboardInterrupt:
        print(
            f"\n\n  [SISTEMA INTERROMPIDO] Turno {contexto['turno'].lower()} "
            f"encerrado à força no Porto de {contexto['porto_nome']} — "
            f"{contexto['porto_uf']}. Até logo, {nome}. Progresso salvo.\n"
        )


if __name__ == "__main__":
    main()
