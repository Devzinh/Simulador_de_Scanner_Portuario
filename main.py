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
    contexto = _gerar_contexto_operacional()
    porto_nome = contexto["porto_nome"]
    porto_uf = contexto["porto_uf"]
    turno = contexto["turno"]
    fiscalizacao = contexto["fiscalizacao"]
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



def _hud_strikes(nome, strikes, max_strikes, total, acertos, erros):
    restantes = max_strikes - strikes
    icones = "🟥" * strikes + "⬜" * restantes
    _sep()
    print(f"  Inspetor: {nome:<16}  Advertências: {icones}  ({strikes}/{max_strikes})")
    print(f"  Conteineres: {total:<5} Acertos: {acertos:<5} Erros: {erros}")
    _sep()


def main():
    max_strikes = 3
    save = _carregar()

    if save:
        try:
            print()
            _sep()
            print(f"  💾 SAVE ENCONTRADO")
            print(f"  Inspetor    : {save['nome']}")
            print(f"  Advertências: {save['strikes']}/{max_strikes}   "
                  f"Conteineres: {save['total']}   Acertos: {save['acertos']}")
            _sep()
            
            while True:
                resp = input("\n  Continuar partida salva? (s/n): ").strip().lower()
                if resp in ('s', 'n'):
                    break
                print("  Opção inválida. Digite 's' para SIM ou 'n' para NÃO.")

            if resp == "s":
                nome    = save["nome"]
                strikes = save["strikes"]
                total   = save["total"]
                acertos = save["acertos"]
                erros   = save["erros"]
                contexto = {
                    "porto_nome": save.get("porto_nome"),
                    "porto_uf": save.get("porto_uf"),
                    "turno": save.get("turno"),
                    "fiscalizacao": save.get("fiscalizacao"),
                }
                if not all(contexto.values()):
                    contexto = _gerar_contexto_operacional()
                print(f"\n  Bem-vindo de volta, Inspetor {nome}.\n")
            else:
                _deletar_save()
                nome, contexto = _intro()
                strikes = total = acertos = erros = 0
        except KeyError:
            print("\n  [AVISO] Dados do save estão incompletos. Iniciando nova partida.")
            _deletar_save()
            save = None

    if not save:
        nome, contexto = _intro()
        strikes = total = acertos = erros = 0

    primeiro = True
    try:
        while True:
            if not primeiro:
                input(f"\n  [{nome}] Pressione ENTER para escanear o próximo conteiner...")
            primeiro = False
            c = gerar_conteiner()
            alertas, suspeitos = simular_scanner(c)
            ganhou_strike = tomar_decisao(c, alertas, suspeitos)

            total += 1
            if ganhou_strike:
                strikes += 1
                erros   += 1
            else:
                acertos += 1

            _salvar({
                "nome": nome,
                "strikes": strikes,
                "total": total,
                "acertos": acertos,
                "erros": erros,
                "porto_nome": contexto["porto_nome"],
                "porto_uf": contexto["porto_uf"],
                "turno": contexto["turno"],
                "fiscalizacao": contexto["fiscalizacao"],
            })
            _hud_strikes(nome, strikes, max_strikes, total, acertos, erros)

            if strikes >= max_strikes:
                _game_over(nome, strikes, contexto)
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
