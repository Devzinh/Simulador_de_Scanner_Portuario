# -*- coding: utf-8 -*-
import random
from dados import ITENS_SUSPEITOS


def icon(nome):
    """Retorna ícones estáveis para mensagens de terminal."""
    icones = {
        "pf": "👮",
        "auto_infracao": "🧾",
        "inquerito": "📁",
        "monitoramento": "📡",
        "coaf": "🏦",
    }
    return icones.get(nome, "[!]")


_EQUIPES = [
    ("Equipe Alfa",   "Receita Federal — Setor de Scanner Avançado"),
    ("Equipe Bravo",  "Polícia Federal — DENARC / Narcóticos"),
    ("Equipe Charlie","IBAMA — Divisão de Fauna e Carga Ambiental"),
    ("Equipe Delta",  "ANVISA — Vigilância Sanitária Portuária"),
    ("Equipe Echo",   "Guarda Portuária (GPort) — Patrulha de Cais"),
    ("Equipe Foxtrot","Receita Federal + Cão Farejador K-9"),
    ("Equipe Golf",   "Força Nacional — Missão GLO Porto de Santos"),
]
def _clamp(valor, minimo, maximo):
    return max(minimo, min(maximo, valor))
def _narrativa_risco(risco):
    if risco <= 1:
        return "baixo", "Origem de baixo risco: operação orientada por conferência documental."
    if risco == 2:
        return "moderado", "Origem de risco moderado: inspeção com foco em inconsistências pontuais."
    if risco in (3, 4):
        return "alto", "Origem de risco alto: protocolos reforçados e tolerância reduzida a desvios."
    return "crítico", "Origem crítica: ação de inteligência prioriza confirmação imediata e cadeia de custódia rígida."
def _inspecao_positiva(c, achou):
    """Equipe encontrou irregularidade — escolha de como encaminhar."""
    qtd_presos = random.randint(0, 3)
    peso_kg    = random.randint(5, 800)
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
        try:
            acao = input("\n  Sua decisão (1/2/3/4): ").strip()
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        
        if acao == "1":
            print(f"\n  {icon('pf')} PF acionada. Flagrante lavrado — {max(qtd_presos,1)} preso(s).")
            print(f"     Conteiner {c['id']} recolhido como corpo de delito.")
            print(f"     Operação registrada no sistema COAF.\n")
            break
        elif acao == "2":
            valor_multa = random.randint(50, 500) * 1000
            print(f"\n  {icon('auto_infracao')} Auto de Infração emitido — multa estimada: R$ {valor_multa:,}.")
            print(f"     Conteiner {c['id']} lacrado. Perícia forense convocada (ETA 24–48h).\n")
            break
        elif acao == "3":
            print(f"\n  🔬 Carga encaminhada à Receita Federal para destruição.")
            print(f"     Processo administrativo {c['id']}-RF aberto. Armador notificado.\n")
            break
        elif acao == "4":
            print(f"\n  {icon('inquerito')} Inquérito Policial Federal aberto — nº {random.randint(100,999)}/2026-SR/SP.")
            print(f"     Tripulação liberada com tornozeleira. Passaportes retidos.\n")
            break
        else:
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
        try:
            acao = input("\n  Sua decisão (1/2/3): ").strip()
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        if acao == "1":
            print(f"\n  ✅ Conteiner {c['id']} LIBERADO após vistoria.\n")
            break
        elif acao == "2":
            print(f"\n  🔄 Segunda inspeção solicitada — aguardando equipe disponível.")
            print(f"     Conteiner {c['id']} permanece no pátio de retenção.\n")
            break
        elif acao == "3":
            print(f"\n  {icon('monitoramento')} Conteiner {c['id']} liberado com alerta de monitoramento.")
            print(f"     Sistema SisComex notificado — rastreio ativo até destino final.\n")
            break
        else:
            print("  Opção inválida.")
def _resultado_inspecao_fisica(c, suspeitos_encontrados):
    codigo, orgao = random.choice(_EQUIPES)
    risco = c.get("risco_pais", 1)
    faixa, narrativa = _narrativa_risco(risco)
    risco_mod = (risco - 1) / 4
    print(f"\n{'─'*58}")
    print(f"  🔍 RESULTADO DA INSPEÇÃO FÍSICA")
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
# ── Acionamento imediato de autoridades — banco de desfechos ──────────────────
_UNIDADES_ACIONADAS = [
    ("DRF",     "Delegacia da Receita Federal"),
    ("DRACO",   "Delegacia de Repressão ao Crime Organizado"),
    ("DENARC",  "Polícia Federal — Divisão de Narcóticos"),
    ("GOE-PF",  "Grupamento de Operações Especiais — PF"),
    ("COIPORT", "Coordenação de Inteligência Portuária"),
    ("GPort",   "Guarda Portuária — Ronda Tática de Cais"),
    ("CIPOE",   "Companhia de Inteligência Portuária — Exército"),
]
def _flagrante_positivo(c, suspeitos_encontrados, unidade_sigla):
    alvo   = suspeitos_encontrados or [random.choice(ITENS_SUSPEITOS)]
    detidos = random.randint(1, 5)
    peso_kg = random.randint(10, 1200)
    cenarios = [
        f"Operadores do terminal tentaram remover os itens durante abordagem.",
        f"Carga encontrada em compartimento oculto no assoalho do conteiner.",
        f"Dois veículos de fuga interceptados na saída do terminal.",
        f"Operação coordenada com Marinha — embarcação de apoio abordada no canal.",
        f"Suspeitos identificados por câmeras de vigilância do porto horas antes.",
        f"Itens embalados com supressor de odor — cão K-9 alertou mesmo assim.",
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
        try:
            acao = input("\n  Sua decisão (1/2/3/4): ").strip()
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        if acao == "1":
            print(f"\n  📋 Flagrante lavrado. {detidos} preso(s) — Centro de Detenção Provisória.")
            print(f"     Perícia do IML agendada para as próximas 6h.\n")
            break
        elif acao == "2":
            num_ip = random.randint(100, 999)
            print(f"\n  {icon('inquerito')} Inquérito Federal nº {num_ip}/2026-SR/SP aberto.")
            print(f"     Custódia transferida à PF. Advogados notificados.\n")
            break
        elif acao == "3":
            print(f"\n  ⚖ Ministério Público acionado — pedido de prisão preventiva.")
            print(f"     Audiência de custódia marcada para as próximas 24h.\n")
            break
        elif acao == "4":
            print(f"\n  {icon('coaf')} COAF notificado — investigação de lavagem iniciada.")
            print(f"     Contas bancárias dos envolvidos bloqueadas preventivamente.\n")
            break
        else:
            print("  Opção inválida.")
    return False
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
        try:
            acao = input("\n  Sua decisão (1/2/3): ").strip()
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        if acao == "1":
            print(f"\n  ✅ Conteiner {c['id']} LIBERADO pela unidade no local.\n")
            break
        elif acao == "2":
            print(f"\n  🔒 Reforço solicitado. Segunda unidade a caminho.")
            print(f"     Conteiner {c['id']} em quarentena no pátio de retenção.\n")
            break
        elif acao == "3":
            print(f"\n  📡 Liberado com rastreio ativo. SisComex notificado.")
            print(f"     Alerta gerado para o porto de destino.\n")
            break
        else:
            print("  Opção inválida.")
    return ganhou_strike
def _desfecho_autoridades(c, suspeitos_encontrados):
    sigla, nome_completo = random.choice(_UNIDADES_ACIONADAS)
    risco = c.get("risco_pais", 1)
    faixa, narrativa = _narrativa_risco(risco)
    risco_mod = (risco - 1) / 4
    print(f"\n{'─'*58}")
    print(f"  🚔 AUTORIDADES ACIONADAS")
    print(f"  Unidade: {sigla} — {nome_completo}")
    print(f"  Faixa de risco: {faixa.upper()} ({risco}/5)")
    print(f"  {narrativa}")
    print(f"{'─'*58}")
    base_flagrante = 0.70 if suspeitos_encontrados else 0.22
    chance_flagrante = _clamp(base_flagrante + (0.20 * risco_mod), 0.15, 0.95)
    if random.random() < chance_flagrante:
        return _flagrante_positivo(c, suspeitos_encontrados, sigla)
    else:
        return _flagrante_negativo(c, suspeitos_encontrados)
# ── Decisão inicial do fiscal ──────────────────────────────────────────────────
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
        try:
            escolha = input("\n  Digite sua escolha (1/2/3): ").strip()
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        if escolha == "1":
            print(f"\n  ✅ Conteiner {c['id']} LIBERADO.")
            print(f"     Autorizado pelo fiscal para seguir ao destino.")
            if suspeitos_encontrados and random.random() < 0.65:
                print(f"\n  ⛔ AUDITORIA POSTERIOR — Conteiner {c['id']} interceptado.")
                print(f"     Irregularidades confirmadas após rastreio de rota.")
                print(f"     Erro de liberação registrado em seu prontuário.")
                return True
            print()
            return False
        elif escolha == "2":
            print(f"\n  🔒 Conteiner {c['id']} RETIDO.")
            print(f"     Aguardando inspeção física pela equipe de fiscalização.")
            _resultado_inspecao_fisica(c, suspeitos_encontrados)
            return False
        elif escolha == "3":
            print(f"\n  🚔 Conteiner {c['id']} — AUTORIDADES ACIONADAS.")
            ganhou = _desfecho_autoridades(c, suspeitos_encontrados)
            return ganhou
        else:
            print("  Opção inválida. Escolha 1, 2 ou 3.")
# ── UI helpers ───────────────────────────────────────────────────────────────
