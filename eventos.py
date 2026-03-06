# -*- coding: utf-8 -*-
import random
from dados import ITENS_SUSPEITOS, NARRATIVA_FRAGMENTOS

_EQUIPE_PADRAO = [
    ("Equipe Alfa", "Receita Federal — Setor de Scanner Avançado"),
    ("Equipe Bravo", "Polícia Federal — DENARC / Narcóticos"),
    ("Equipe Charlie", "IBAMA — Divisão de Fauna e Carga Ambiental"),
    ("Equipe Delta", "ANVISA — Vigilância Sanitária Portuária"),
    ("Equipe Echo", "Guarda Portuária (GPort) — Patrulha de Cais"),
    ("Equipe Foxtrot", "Receita Federal + Cão Farejador K-9"),
    ("Equipe Golf", "Força Nacional — Missão GLO Porto de Santos"),
]

_UNIDADES_ACIONADAS = [
    ("DRF", "Delegacia da Receita Federal"),
    ("DRACO", "Delegacia de Repressão ao Crime Organizado"),
    ("DENARC", "Polícia Federal — Divisão de Narcóticos"),
    ("GOE-PF", "Grupamento de Operações Especiais — PF"),
    ("COIPORT", "Coordenação de Inteligência Portuária"),
    ("GPort", "Guarda Portuária — Ronda Tática de Cais"),
    ("CIPOE", "Companhia de Inteligência Portuária — Exército"),
]

_HISTORICO_NARRATIVA = {}


def _tags_coerencia(itens):
    texto = " ".join(i.lower() for i in (itens or []))
    tags = {"geral"}
    if any(k in texto for k in ["radioativo", "quim", "fertiliz", "ambient"]):
        tags.add("ambiental")
    if any(k in texto for k in ["remed", "vacina", "insulina", "farm", "sanit"]):
        tags.add("farmaceutico")
    return tags


def _escolher_fragmento(c, categoria, tags=None):
    opcoes = NARRATIVA_FRAGMENTOS.get(categoria) or []
    if tags:
        preferencia = None
        if "ambiental" in tags:
            preferencia = "ambiental"
        elif "farmaceutico" in tags:
            preferencia = "farmaceutico"

        if preferencia:
            especificas = [o for o in opcoes if preferencia in o.get("tags", [])]
            if especificas:
                opcoes = especificas

        filtradas = [o for o in opcoes if not o.get("tags") or any(t in tags for t in o["tags"])]
    else:
        filtradas = list(opcoes)
    pool = filtradas or opcoes
    if not pool:
        return {}

    partida = c.get("id", "_default") if isinstance(c, dict) else "_default"
    historico = _HISTORICO_NARRATIVA.setdefault(partida, {})
    ultimo = historico.get(categoria)
    candidatas = [o for o in pool if o != ultimo]
    escolhido = random.choice(candidatas or pool)
    historico[categoria] = escolhido
    return escolhido


def _montar_narrativa(c, itens_base):
    tags = _tags_coerencia(itens_base)
    contexto = _escolher_fragmento(c, "contexto_operacao")
    ocultacao = _escolher_fragmento(c, "metodo_ocultacao", tags)
    reacao = _escolher_fragmento(c, "reacao_equipe", tags)
    legal = _escolher_fragmento(c, "consequencia_legal", tags)
    impacto = _escolher_fragmento(c, "impacto_terminal")

    blocos = []
    if contexto:
        blocos.append(
            f"{contexto.get('ator', 'A equipe')} {contexto.get('evidencia', 'durante a vistoria')} {contexto.get('local', 'no terminal')}"
        )
    if ocultacao:
        blocos.append(
            f"{ocultacao.get('acao', 'identificou inconsistências')} {ocultacao.get('evidencia', 'com indícios materiais')}"
        )
    if reacao:
        blocos.append(f"Na sequência, {reacao.get('ator', 'a equipe de resposta')} {reacao.get('acao', 'foi mobilizada')}")
    if legal:
        blocos.append(f"A ocorrência seguiu {legal.get('consequencia', 'com registro administrativo')}")
    if impacto:
        blocos.append(f"{impacto.get('consequencia', 'sem impacto operacional relevante')}")

    if not blocos:
        return "Fiscalização registrou ocorrência com encaminhamento padrão."
    return ". ".join(blocos[:5]) + "."


def _equipe_coerente(itens):
    tags = _tags_coerencia(itens)
    if "ambiental" in tags:
        return "Equipe Charlie", "IBAMA — Divisão de Fauna e Carga Ambiental"
    if "farmaceutico" in tags:
        return "Equipe Delta", "ANVISA — Vigilância Sanitária Portuária"
    return random.choice(_EQUIPE_PADRAO)


def _inspecao_positiva(c, achou):
    qtd_presos = random.randint(0, 3)
    peso_kg = random.randint(5, 800)
    cenario = _montar_narrativa(c, achou)

    print(f"\n  🚨 IRREGULARIDADES CONFIRMADAS — {cenario.upper()}")
    print("     Itens encontrados fisicamente:")
    for item in achou:
        print(f"       • {item} (~{peso_kg} kg)")
    if qtd_presos:
        print(f"\n     {qtd_presos} operador(es) do terminal detido(s) no pátio.")

    print("\n  Próxima ação:")
    print("   [1] Acionar Polícia Federal para prisão em flagrante")
    print("   [2] Emitir Auto de Infração e lacrar para perícia")
    print("   [3] Transferir carga à Receita Federal para destruição controlada")
    print("   [4] Abrir Inquérito Policial e liberar tripulação sob monitoramento")
    while True:
        acao = input("\n  Sua decisão (1/2/3/4): ").strip()
        if acao == "1":
            print(f"\n  🚓 PF acionada. Flagrante lavrado — {max(qtd_presos,1)} preso(s).")
            print(f"     Conteiner {c['id']} recolhido como corpo de delito.")
            print("     Operação registrada no sistema COAF.\n")
            break
        if acao == "2":
            valor_multa = random.randint(50, 500) * 1000
            print(f"\n  📄 Auto de Infração emitido — multa estimada: R$ {valor_multa:,}.")
            print(f"     Conteiner {c['id']} lacrado. Perícia forense convocada (ETA 24–48h).\n")
            break
        if acao == "3":
            print("\n  🔬 Carga encaminhada à Receita Federal para destruição.")
            print(f"     Processo administrativo {c['id']}-RF aberto. Armador notificado.\n")
            break
        if acao == "4":
            print(f"\n  🗂️ Inquérito Policial Federal aberto — nº {random.randint(100,999)}/2026-SR/SP.")
            print("     Tripulação liberada com tornozeleira. Passaportes retidos.\n")
            break
        print("  Opção inválida.")


def _inspecao_negativa(c):
    razao = _montar_narrativa(c, [])
    print("\n  ✅ INSPEÇÃO CONCLUÍDA — SEM IRREGULARIDADES.")
    print(f"     {razao}")

    print("\n  Encaminhamento:")
    print("   [1] Liberar imediatamente após vistoria")
    print("   [2] Solicitar segunda inspeção por outra equipe")
    print("   [3] Liberar, mas registrar alerta para rastreio de rota")
    while True:
        acao = input("\n  Sua decisão (1/2/3): ").strip()
        if acao == "1":
            print(f"\n  ✅ Conteiner {c['id']} LIBERADO após vistoria.\n")
            break
        if acao == "2":
            print("\n  🔄 Segunda inspeção solicitada — aguardando equipe disponível.")
            print(f"     Conteiner {c['id']} permanece no pátio de retenção.\n")
            break
        if acao == "3":
            print(f"\n  📡 Conteiner {c['id']} liberado com alerta de monitoramento.")
            print("     Sistema SisComex notificado — rastreio ativo até destino final.\n")
            break
        print("  Opção inválida.")


def _resultado_inspecao_fisica(c, suspeitos_encontrados):
    codigo, orgao = _equipe_coerente(suspeitos_encontrados)
    print(f"\n{'─'*58}")
    print("  🔍 RESULTADO DA INSPEÇÃO FÍSICA")
    print(f"  {codigo} — {orgao}")
    print(f"  Faixa de risco: {faixa.upper()} ({risco}/5)")
    print(f"  {narrativa}")
    print(f"{'─'*58}")
    base_confirmar = 0.68 if suspeitos_encontrados else 0.16
    chance_confirmar = _clamp(base_confirmar + (0.18 * risco_mod), 0.10, 0.92)
    if random.random() < chance_confirmar:
        achou = suspeitos_encontrados or [random.choice(ITENS_SUSPEITOS)]
        _inspecao_positiva(c, achou)
    else:
        _inspecao_negativa(c)


def _flagrante_positivo(c, suspeitos_encontrados, unidade_sigla):
    alvo = suspeitos_encontrados or [random.choice(ITENS_SUSPEITOS)]
    detidos = random.randint(1, 5)
    peso_kg = random.randint(10, 1200)

    cenario = _montar_narrativa(c, alvo)
    print(f"\n  🔴 FLAGRANTE CONFIRMADO — {cenario}")
    print("\n     Itens apreendidos:")
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
            print("     Perícia do IML agendada para as próximas 6h.\n")
            break
        if acao == "2":
            num_ip = random.randint(100, 999)
            print(f"\n  🗂️ Inquérito Federal nº {num_ip}/2026-SR/SP aberto.")
            print("     Custódia transferida à PF. Advogados notificados.\n")
            break
        if acao == "3":
            print("\n  ⚖ Ministério Público acionado — pedido de prisão preventiva.")
            print("     Audiência de custódia marcada para as próximas 24h.\n")
            break
        if acao == "4":
            print("\n  🏦 COAF notificado — investigação de lavagem iniciada.")
            print("     Contas bancárias dos envolvidos bloqueadas preventivamente.\n")
            break
        print("  Opção inválida.")
    return False
def _flagrante_negativo(c, suspeitos_encontrados):
    razao = _montar_narrativa(c, suspeitos_encontrados)
    print("\n  ⚠ UNIDADE NO LOCAL — SEM PRISÕES.")
    print(f"     {razao}")
    ganhou_strike = not suspeitos_encontrados
    if ganhou_strike:
        print("\n  ⛔ FALSO ALARME REGISTRADO EM PRONTUÁRIO.")
        print("     Nenhum indício real justificava acionamento imediato.")
        print("     Comandante de pátio foi notificado do erro.\n")

    print("  Próximo passo:")
    print("   [1] Liberar conteiner — sem base para retenção adicional")
    print("   [2] Manter retido e solicitar reforço de segunda unidade")
    print("   [3] Liberar, mas registrar no SisComex para rastreio de rota")
    while True:
        acao = input("\n  Sua decisão (1/2/3): ").strip()
        if acao == "1":
            print(f"\n  ✅ Conteiner {c['id']} LIBERADO pela unidade no local.\n")
            break
        if acao == "2":
            print("\n  🔒 Reforço solicitado. Segunda unidade a caminho.")
            print(f"     Conteiner {c['id']} em quarentena no pátio de retenção.\n")
            break
        if acao == "3":
            print("\n  📡 Liberado com rastreio ativo. SisComex notificado.")
            print("     Alerta gerado para o porto de destino.\n")
            break
        print("  Opção inválida.")
    return ganhou_strike
def _desfecho_autoridades(c, suspeitos_encontrados):
    sigla, nome_completo = random.choice(_UNIDADES_ACIONADAS)
    risco = c.get("risco_pais", 1)
    faixa, narrativa = _narrativa_risco(risco)
    risco_mod = (risco - 1) / 4
    print(f"\n{'─'*58}")
    print("  🚔 AUTORIDADES ACIONADAS")
    print(f"  Unidade: {sigla} — {nome_completo}")
    print(f"  Faixa de risco: {faixa.upper()} ({risco}/5)")
    print(f"  {narrativa}")
    print(f"{'─'*58}")
    base_flagrante = 0.70 if suspeitos_encontrados else 0.22
    chance_flagrante = _clamp(base_flagrante + (0.20 * risco_mod), 0.15, 0.95)
    if random.random() < chance_flagrante:
        return _flagrante_positivo(c, suspeitos_encontrados, sigla)
    return _flagrante_negativo(c, suspeitos_encontrados)


def tomar_decisao(c, alertas, suspeitos_encontrados):
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
        if escolha == "1":
            print(f"\n  ✅ Conteiner {c['id']} LIBERADO.")
            print("     Autorizado pelo fiscal para seguir ao destino.")
            if suspeitos_encontrados and random.random() < 0.65:
                print(f"\n  ⛔ AUDITORIA POSTERIOR — Conteiner {c['id']} interceptado.")
                print("     Irregularidades confirmadas após rastreio de rota.")
                print("     Erro de liberação registrado em seu prontuário.")
                return True
            print()
            return False
        if escolha == "2":
            print(f"\n  🔒 Conteiner {c['id']} RETIDO.")
            print("     Aguardando inspeção física pela equipe de fiscalização.")
            _resultado_inspecao_fisica(c, suspeitos_encontrados)
            return False
        if escolha == "3":
            print(f"\n  🚔 Conteiner {c['id']} — AUTORIDADES ACIONADAS.")
            return _desfecho_autoridades(c, suspeitos_encontrados)
        print("  Opção inválida. Escolha 1, 2 ou 3.")
