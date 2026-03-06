import random
from dados import ITENS_SUSPEITOS

_EQUIPES = [
    ("Equipe Alfa",   "Receita Federal — Setor de Scanner Avançado"),
    ("Equipe Bravo",  "Polícia Federal — DENARC / Narcóticos"),
    ("Equipe Charlie", "IBAMA — Divisão de Fauna e Carga Ambiental"),
    ("Equipe Delta",  "ANVISA — Vigilância Sanitária Portuária"),
    ("Equipe Echo",   "Guarda Portuária (GPort) — Patrulha de Cais"),
    ("Equipe Foxtrot", "Receita Federal + Cão Farejador K-9"),
    ("Equipe Golf",   "Força Nacional — Missão GLO Porto de Santos"),
]


def _efeitos_base():
    return {
        "ganhou_strike": False,
        "reputacao": 0,
        "casos_graves": 0,
        "falsos_alarmes": 0,
        "eficiencia": 0,
        "risco_interno": 0,
        "bonus_inteligencia": 0,
    }


def _merge_efeitos(*efeitos):
    final = _efeitos_base()
    for efeito in efeitos:
        for k, v in efeito.items():
            if k == "ganhou_strike":
                final[k] = final[k] or bool(v)
            else:
                final[k] += v
    return final


def _inspecao_positiva(c, achou):
    """Equipe encontrou irregularidade — escolha de como encaminhar."""
    qtd_presos = random.randint(0, 3)
    peso_kg = random.randint(5, 800)

    cenario = random.choice([
        "drogas ocultas em fundo falso do conteiner",
        "carga real diverge totalmente do manifesto declarado",
        "componentes de armas desmontados entre itens legítimos",
        "material radiológico em recipiente não identificado",
        "dinheiro não declarado embalado a vácuo entre mercadorias",
        "produto contrabandeado com nota fiscal de outro exportador",
    ])

    print(f"\n  🚨 IRREGULARIDADES CONFIRMADAS — {cenario.upper()}")
    print(f"     Itens encontrados fisicamente:")
    for item in achou:
        print(f"       • {item} (~{peso_kg} kg)")
    if qtd_presos:
        print(f"\n     {qtd_presos} operador(es) do terminal detido(s) no pátio.")

    print(f"\n  Próxima ação:")
    print("   [1] Acionar Polícia Federal para prisão em flagrante")
    print("   [2] Emitir Auto de Infração e lacrar para perícia")
    print("   [3] Transferir carga à Receita Federal para destruição controlada")
    print("   [4] Abrir Inquérito Policial e liberar tripulação sob monitoramento")

    while True:
        acao = input("\n  Sua decisão (1/2/3/4): ").strip()
        if acao == "1":
            print(f"\n  🚔 PF acionada. Flagrante lavrado — {max(qtd_presos,1)} preso(s).")
            print(f"     Conteiner {c['id']} recolhido como corpo de delito.")
            print(f"     Operação registrada no sistema COAF.\n")
            return {"reputacao": 7, "casos_graves": 1, "eficiencia": 3, "risco_interno": -2}
        if acao == "2":
            valor_multa = random.randint(50, 500) * 1000
            print(f"\n  📋 Auto de Infração emitido — multa estimada: R$ {valor_multa:,}.")
            print(f"     Conteiner {c['id']} lacrado. Perícia forense convocada (ETA 24–48h).\n")
            return {"reputacao": 5, "casos_graves": 1, "eficiencia": 2, "risco_interno": -1}
        if acao == "3":
            print(f"\n  🔬 Carga encaminhada à Receita Federal para destruição.")
            print(f"     Processo administrativo {c['id']}-RF aberto. Armador notificado.\n")
            return {"reputacao": 6, "casos_graves": 1, "eficiencia": 2, "risco_interno": -1}
        if acao == "4":
            print(f"\n  🕵 Inquérito Policial Federal aberto — nº {random.randint(100,999)}/2026-SR/SP.")
            print(f"     Tripulação liberada com tornozeleira. Passaportes retidos.\n")
            return {"reputacao": 3, "casos_graves": 1, "eficiencia": 1, "risco_interno": 0}
        print("  Opção inválida.")


def _inspecao_negativa(c):
    """Equipe não encontrou nada — escolha de encaminhamento."""
    razao = random.choice([
        "Manifesto de carga confere com itens encontrados fisicamente.",
        "Cão farejador K-9 não alertou para nenhuma substância ilícita.",
        "Densidade elevada justificada: equipamentos de aço inox homologados.",
        "Documentação alfandegária validada pela Receita Federal — NF-e regular.",
        "Itens de aparência suspeita são amostras com registro ANVISA.",
        "Segunda medição de densidade dentro dos parâmetros — falso positivo do scanner.",
        "Carga inspecionada item a item — nenhuma irregularidade física encontrada.",
    ])
    print(f"\n  ✅ INSPEÇÃO CONCLUÍDA — SEM IRREGULARIDADES.")
    print(f"     {razao}")

    print(f"\n  Encaminhamento:")
    print("   [1] Liberar imediatamente após vistoria")
    print("   [2] Solicitar segunda inspeção por outra equipe")
    print("   [3] Liberar, mas registrar alerta para rastreio de rota")

    while True:
        acao = input("\n  Sua decisão (1/2/3): ").strip()
        if acao == "1":
            print(f"\n  ✅ Conteiner {c['id']} LIBERADO após vistoria.\n")
            return {"reputacao": -1, "falsos_alarmes": 1, "eficiencia": -1, "risco_interno": 1}
        if acao == "2":
            print(f"\n  🔄 Segunda inspeção solicitada — aguardando equipe disponível.")
            print(f"     Conteiner {c['id']} permanece no pátio de retenção.\n")
            return {"reputacao": -2, "falsos_alarmes": 1, "eficiencia": -2, "risco_interno": 2}
        if acao == "3":
            print(f"\n  📡 Conteiner {c['id']} liberado com alerta de monitoramento.")
            print(f"     Sistema SisComex notificado — rastreio ativo até destino final.\n")
            return {"reputacao": 0, "falsos_alarmes": 1, "eficiencia": -1, "risco_interno": 1}
        print("  Opção inválida.")


def _resultado_inspecao_fisica(c, suspeitos_encontrados):
    codigo, orgao = random.choice(_EQUIPES)
    print(f"\n{'─'*58}")
    print(f"  🔍 RESULTADO DA INSPEÇÃO FÍSICA")
    print(f"  {codigo} — {orgao}")
    print(f"{'─'*58}")

    chance_confirmar = 0.72 if suspeitos_encontrados else 0.12
    if random.random() < chance_confirmar:
        achou = suspeitos_encontrados or [random.choice(ITENS_SUSPEITOS)]
        return _inspecao_positiva(c, achou)
    return _inspecao_negativa(c)


_UNIDADES_ACIONADAS = [
    ("DRF", "Delegacia da Receita Federal"),
    ("DRACO", "Delegacia de Repressão ao Crime Organizado"),
    ("DENARC", "Polícia Federal — Divisão de Narcóticos"),
    ("GOE-PF", "Grupamento de Operações Especiais — PF"),
    ("COIPORT", "Coordenação de Inteligência Portuária"),
    ("GPort", "Guarda Portuária — Ronda Tática de Cais"),
    ("CIPOE", "Companhia de Inteligência Portuária — Exército"),
]


def _flagrante_positivo(c, suspeitos_encontrados, unidade_sigla):
    alvo = suspeitos_encontrados or [random.choice(ITENS_SUSPEITOS)]
    detidos = random.randint(1, 5)
    peso_kg = random.randint(10, 1200)

    cenarios = [
        "Operadores do terminal tentaram remover os itens durante abordagem.",
        "Carga encontrada em compartimento oculto no assoalho do conteiner.",
        "Dois veículos de fuga interceptados na saída do terminal.",
        "Operação coordenada com Marinha — embarcação de apoio abordada no canal.",
        "Suspeitos identificados por câmeras de vigilância do porto horas antes.",
        "Itens embalados com supressor de odor — cão K-9 alertou mesmo assim.",
    ]
    print(f"\n  🔴 FLAGRANTE CONFIRMADO — {random.choice(cenarios)}")
    print(f"\n     Itens apreendidos:")
    for item in alvo:
        print(f"       • {item} (~{peso_kg} kg)")
    print(f"\n     {detidos} suspeito(s) detido(s). Conteiner {c['id']} lacrado.")

    print(f"\n  Encaminhamento ({unidade_sigla}):")
    print("   [1] Lavrar flagrante e encaminhar ao IML para perícia")
    print("   [2] Transferir à Polícia Federal para inquérito federal")
    print("   [3] Acionar Ministério Público — solicitar prisão preventiva")
    print("   [4] Comunicar COAF — suspeita de lavagem de dinheiro")

    while True:
        acao = input("\n  Sua decisão (1/2/3/4): ").strip()
        if acao == "1":
            print(f"\n  📋 Flagrante lavrado. {detidos} preso(s) — Centro de Detenção Provisória.")
            print(f"     Perícia do IML agendada para as próximas 6h.\n")
            return {"reputacao": 8, "casos_graves": 1, "eficiencia": 4, "risco_interno": -2}
        if acao == "2":
            num_ip = random.randint(100, 999)
            print(f"\n  🕵 Inquérito Federal nº {num_ip}/2026-SR/SP aberto.")
            print(f"     Custódia transferida à PF. Advogados notificados.\n")
            return {"reputacao": 6, "casos_graves": 1, "eficiencia": 3, "risco_interno": -1}
        if acao == "3":
            print(f"\n  ⚖ Ministério Público acionado — pedido de prisão preventiva.")
            print(f"     Audiência de custódia marcada para as próximas 24h.\n")
            return {"reputacao": 7, "casos_graves": 1, "eficiencia": 3, "risco_interno": -1}
        if acao == "4":
            print(f"\n  💰 COAF notificado — investigação de lavagem iniciada.")
            print(f"     Contas bancárias dos envolvidos bloqueadas preventivamente.\n")
            return {"reputacao": 5, "casos_graves": 1, "eficiencia": 2, "risco_interno": 0}
        print("  Opção inválida.")


def _flagrante_negativo(c, suspeitos_encontrados):
    razao = random.choice([
        "Suspeitos avistados fugiram para área não inspecionada antes da chegada.",
        "Documentação apresentada no local passou em validação digital imediata.",
        "Cão farejador K-9 não alertou para nenhum dos itens do conteiner.",
        "Densidade anômala explicada: contrapesos de chumbo homologados para exportação.",
        "Responsável pelo embarque apresentou autorização ministerial vigente.",
        "Itens sinalizados pelo scanner estavam dentro da lista de isenção alfandegária.",
    ])
    print(f"\n  ⚠ UNIDADE NO LOCAL — SEM PRISÕES.")
    print(f"     {razao}")

    ganhou_strike = not suspeitos_encontrados
    if ganhou_strike:
        print(f"\n  ⛔ FALSO ALARME REGISTRADO EM PRONTUÁRIO.")
        print(f"     Nenhum indício real justificava acionamento imediato.")
        print(f"     Comandante de pátio foi notificado do erro.\n")

    print(f"  Próximo passo:")
    print("   [1] Liberar conteiner — sem base para retenção adicional")
    print("   [2] Manter retido e solicitar reforço de segunda unidade")
    print("   [3] Liberar, mas registrar no SisComex para rastreio de rota")

    while True:
        acao = input("\n  Sua decisão (1/2/3): ").strip()
        if acao == "1":
            print(f"\n  ✅ Conteiner {c['id']} LIBERADO pela unidade no local.\n")
            return {"ganhou_strike": ganhou_strike, "reputacao": -4 if ganhou_strike else -1,
                    "falsos_alarmes": 1, "eficiencia": -3 if ganhou_strike else -1, "risco_interno": 3 if ganhou_strike else 1}
        if acao == "2":
            print(f"\n  🔒 Reforço solicitado. Segunda unidade a caminho.")
            print(f"     Conteiner {c['id']} em quarentena no pátio de retenção.\n")
            return {"ganhou_strike": ganhou_strike, "reputacao": -3 if ganhou_strike else -1,
                    "falsos_alarmes": 1, "eficiencia": -2, "risco_interno": 2 if ganhou_strike else 1}
        if acao == "3":
            print(f"\n  📡 Liberado com rastreio ativo. SisComex notificado.")
            print(f"     Alerta gerado para o porto de destino.\n")
            return {"ganhou_strike": ganhou_strike, "reputacao": -2 if ganhou_strike else 0,
                    "falsos_alarmes": 1, "eficiencia": -1, "risco_interno": 2 if ganhou_strike else 1}
        print("  Opção inválida.")


def _desfecho_autoridades(c, suspeitos_encontrados):
    sigla, nome_completo = random.choice(_UNIDADES_ACIONADAS)
    print(f"\n{'─'*58}")
    print(f"  🚔 AUTORIDADES ACIONADAS")
    print(f"  Unidade: {sigla} — {nome_completo}")
    print(f"{'─'*58}")

    chance_flagrante = 0.75 if suspeitos_encontrados else 0.20
    if random.random() < chance_flagrante:
        return _flagrante_positivo(c, suspeitos_encontrados, sigla)
    return _flagrante_negativo(c, suspeitos_encontrados)


def _aplicar_efeitos(estado_jogador, efeitos):
    estado_jogador["reputacao"] = max(0, min(100, estado_jogador["reputacao"] + efeitos["reputacao"]))
    estado_jogador["casos_graves"] = max(0, estado_jogador["casos_graves"] + efeitos["casos_graves"])
    estado_jogador["falsos_alarmes"] = max(0, estado_jogador["falsos_alarmes"] + efeitos["falsos_alarmes"])
    estado_jogador["eficiencia"] = max(0, min(100, estado_jogador["eficiencia"] + efeitos["eficiencia"]))


def _efeitos_emergentes(estado_jogador):
    efeitos = _efeitos_base()

    if estado_jogador["reputacao"] <= 30:
        chance_auditoria = min(0.75, 0.25 + estado_jogador["falsos_alarmes"] * 0.04)
        if random.random() < chance_auditoria:
            print("\n  🧾 AUDITORIA INTERNA EXTRAORDINÁRIA ABERTA.")
            print("     Reputação baixa elevou o nível de escrutínio do seu turno.")
            efeitos["reputacao"] -= 2
            efeitos["eficiencia"] -= 1
            efeitos["risco_interno"] += 2
            if random.random() < 0.35:
                print("     ⛔ Não conformidade processual encontrada: advertência formal aplicada.")
                efeitos["ganhou_strike"] = True

    if estado_jogador["reputacao"] >= 75:
        chance_bonus = min(0.7, 0.25 + estado_jogador["casos_graves"] * 0.03)
        if random.random() < chance_bonus:
            print("\n  🛰 BÔNUS DE INTELIGÊNCIA LIBERADO.")
            print("     Você recebeu dossiês antecipados de risco para os próximos lotes.")
            efeitos["bonus_inteligencia"] += 1
            efeitos["eficiencia"] += 1

    return efeitos


# ── Decisão inicial do fiscal ──────────────────────────────────────────────────
def tomar_decisao(c, alertas, suspeitos_encontrados, estado_jogador):
    if alertas:
        print("\n  🚨 ALERTAS DO SCANNER:")
        for a in alertas:
            print(f"     • {a}")
    else:
        print("\n  ✅ Nenhuma irregularidade técnica reportada.")

    print("\n  Decisão do fiscal:")
    print("   [1] Liberar conteiner")
    print("   [2] Reter para inspeção física")
    print("   [3] Acionar autoridades imediatamente (suspeita grave)")

    while True:
        escolha = input("\n  Digite sua escolha (1/2/3): ").strip()

        efeitos = _efeitos_base()

        if escolha == "1":
            print(f"\n  ✅ Conteiner {c['id']} LIBERADO.")
            print(f"     Autorizado pelo fiscal para seguir ao destino.")
            efeitos["eficiencia"] += 1
            if suspeitos_encontrados and random.random() < 0.65:
                print(f"\n  ⛔ AUDITORIA POSTERIOR — Conteiner {c['id']} interceptado.")
                print(f"     Irregularidades confirmadas após rastreio de rota.")
                print(f"     Erro de liberação registrado em seu prontuário.")
                efeitos = _merge_efeitos(
                    efeitos,
                    {"ganhou_strike": True, "reputacao": -8, "casos_graves": 1, "eficiencia": -4, "risco_interno": 3},
                )
            else:
                efeitos["reputacao"] += 1
            print()
        elif escolha == "2":
            print(f"\n  🔒 Conteiner {c['id']} RETIDO.")
            print(f"     Aguardando inspeção física pela equipe de fiscalização.")
            efeitos = _merge_efeitos(efeitos, _resultado_inspecao_fisica(c, suspeitos_encontrados))
        elif escolha == "3":
            print(f"\n  🚔 Conteiner {c['id']} — AUTORIDADES ACIONADAS.")
            efeitos = _merge_efeitos(efeitos, _desfecho_autoridades(c, suspeitos_encontrados))
        else:
            print("  Opção inválida. Escolha 1, 2 ou 3.")
            continue

        efeitos = _merge_efeitos(efeitos, _efeitos_emergentes(estado_jogador))
        _aplicar_efeitos(estado_jogador, efeitos)
        return efeitos


# ── UI helpers ───────────────────────────────────────────────────────────────
