import random
from dados import (
    TIPOS_CARGA, PAISES_ORIGEM, ITENS_SUSPEITOS, NOMES_CAMUFLAGEM, 
    ITENS_ISCA, ITENS_POR_TIPO, CHANCE_ITEM_SUSPEITO, CHANCE_CAMUFLAGEM, 
    CHANCE_ISCA, gerar_id_conteiner
)
def gerar_conteiner():
    tipo_carga = random.choice(TIPOS_CARGA)
    pais = random.choice(list(PAISES_ORIGEM.keys()))
    porto, iso, risco = PAISES_ORIGEM[pais]

    itens_escaneados = []
    for _ in range(random.randint(12, 22)):
        roll = random.random()
        if roll < CHANCE_ITEM_SUSPEITO:
            nome_real = random.choice(ITENS_SUSPEITOS)
            if random.random() < CHANCE_CAMUFLAGEM:
                nome_exibido = random.choice(NOMES_CAMUFLAGEM)
            else:
                nome_exibido = nome_real
            densidade = random.randint(150, 500)
            suspeito = True
        elif roll < CHANCE_ITEM_SUSPEITO + CHANCE_ISCA:
            nome_exibido, densidade_base = random.choice(ITENS_ISCA)
            densidade = densidade_base + random.randint(-30, 30)
            suspeito = False
        else:
            nome_exibido = random.choice(ITENS_POR_TIPO[tipo_carga])
            densidade = random.randint(10, 120) + random.randint(0, 80)
            suspeito = False
        itens_escaneados.append({"item": nome_exibido, "densidade": densidade, "suspeito": suspeito})

    novo_id = gerar_id_conteiner()
    if not isinstance(novo_id, str) or not novo_id.strip():
        raise RuntimeError("gerar_id_conteiner gerou um ID vazio ou inválido.")
    
    return {
        "id": novo_id,
        "peso_declarado": random.randint(1000, 10000),
        "tipo_carga": tipo_carga,
        "pais": pais,
        "porto": porto,
        "iso": iso,
        "risco_pais": risco,
        "itens_escaneados": itens_escaneados,
    }


# ── Scanner ────────────────────────────────────────────────────────────────────
def simular_scanner(c):
    risco_label = {1: "BAIXO", 2: "MODERADO", 3: "ELEVADO", 4: "ALTO", 5: "CRÍTICO"}
    print(f"\n{'='*58}")
    print(f"  SCANNER PORTUÁRIO — {c['id']}")
    print(f"{'='*58}")
    print(f"  Tipo de carga  : {c['tipo_carga']}")
    print(f"  Origem         : {c['pais']} [{c['iso']}] — Porto: {c['porto']}")
    print(f"  Risco do país  : {risco_label[c['risco_pais']]} ({c['risco_pais']}/5)")
    print(f"  Peso declarado : {c['peso_declarado']} kg")
    print(f"{'─'*58}")

    alertas = []
    suspeitos_encontrados = []

    peso_real = sum(i["densidade"] for i in c["itens_escaneados"])
    diferenca = abs(peso_real - c["peso_declarado"])

    print("  Itens detectados pelo scanner:")
    for idx, item in enumerate(c["itens_escaneados"], 1):
        print(f"   {idx}. {item['item']} (densidade: {item['densidade']} kg/m³)")
        if item["suspeito"]:
            suspeitos_encontrados.append(item["item"])

    print(f"{'─'*58}")
    print(f"  Peso estimado pelo scanner: {peso_real} kg")

    if diferenca > (c["peso_declarado"] * 0.05):
        alertas.append("Discrepância de peso detectada entre manifesto e aferição física")
    
    itens_densos = sum(1 for item in c["itens_escaneados"] if item["densidade"] > 300)
    if itens_densos > 0:
        alertas.append(f"Aviso estrutural: {itens_densos} assinatura(s) de densidade atípica (>300 kg/m³)")
        
    if c["risco_pais"] >= 4:
        alertas.append(f"Regra de inteligência: Origem classificada como risco {risco_label[c['risco_pais']]}")

    return alertas, suspeitos_encontrados
