import random
import string
import json
from pathlib import Path

# ── Wordlists ─────────────────────────────────────────────────────────────────
TIPOS_CARGA = [
    "Eletronicos",
    "Roupas e Texteis",
    "Alimentos Secos",
    "Alimentos Refrigerados",
    "Maquinario Industrial",
    "Produtos Farmaceuticos",
    "Quimicos",
    "Materiais de Construcao",
    "Veiculos",
    "Bens de Consumo",
    "Materias-primas",
    "Combustiveis (granel)",
]

ITENS_POR_TIPO = {
    "Eletronicos": [
        "Teclado", "Mouse", "Monitor", "Celular", "Notebook",
        "Placa de Video", "Processador", "SSD", "Roteador", "Smartwatch",
    ],
    "Roupas e Texteis": [
        "Camisetas", "Calcas Jeans", "Tecido de Algodao", "Uniformes",
        "Calcados Esportivos", "Bolsas", "Cintos de Couro", "Meias",
    ],
    "Alimentos Secos": [
        "Arroz (sacos 50kg)", "Feijao", "Farinha de Trigo", "Acucar Refinado",
        "Cafe Torrado", "Milho em Grao", "Soja", "Cha a Granel",
    ],
    "Alimentos Refrigerados": [
        "Carne Bovina Congelada", "Frango Inteiro", "Peixe Eviscerado",
        "Queijo Maturado", "Manteiga", "Sorvete Industrial",
    ],
    "Maquinario Industrial": [
        "Compressor de Ar", "Torno Mecanico", "Soldadora Industrial",
        "Bomba Hidraulica", "Motor Eletrico", "Guindaste Portatil",
    ],
    "Produtos Farmaceuticos": [
        "Antibioticos (cx)", "Insulina Refrigerada", "Vacinas",
        "Equipamentos Medicos", "Reagentes Laboratoriais", "Soros",
    ],
    "Quimicos": [
        "Acido Cloridrico (bidao)", "Soda Caustica", "Etanol Industrial",
        "Resinas Epoxy", "Tintas e Solventes", "Fertilizantes NPK",
    ],
    "Materiais de Construcao": [
        "Cimento Portland", "Barras de Aco", "Telhas Ceramicas",
        "Vidros Temperados", "Madeira Serrada", "Tubos de PVC",
    ],
    "Veiculos": [
        "Automoveis Sedan", "Motocicletas", "Caminhonetes",
        "Onibus", "Tratores Agricolas", "Pecas de Motor",
    ],
    "Bens de Consumo": [
        "Brinquedos Plasticos", "Utensilios de Cozinha", "Moveis Desmontados",
        "Eletrodomesticos", "Artigos Esportivos", "Livros e Papelaria",
    ],
    "Materias-primas": [
        "Bobinas de Aco", "Lingotes de Aluminio", "Cobre em Fio",
        "Madeira Bruta", "Mineral de Ferro", "Borracha Natural",
    ],
    "Combustiveis (granel)": [
        "Petroleo Bruto", "Diesel S10", "Gasolina Comum",
        "GLP Liquefeito", "Etanol Hidratado", "Querosene de Aviacao",
    ],
}

ITENS_SUSPEITOS = [
    "Arma de Fogo (pistola)",
    "Arma de Fogo (fuzil)",
    "Municao em caixas",
    "Cocaina (pacotes)",
    "Heroina (embalada a vacuo)",
    "Metanfetamina",
    "Material Radioativo nao declarado",
    "Explosivos (detonadores)",
    "Dinheiro em especie (nao declarado)",
    "Cigarros contrabandeados",
    "Remedios falsificados",
    "Documentos falsos",
]

ITENS_ISCA = [
    ("Chumbo para Pesca (cx)", 290),
    ("Po de Talco Industrial (saco)", 270),
    ("Componentes de Liga Metalica (lacrado)", 310),
    ("Resina em Po (embalagem hermetica)", 260),
    ("Peças de Precisao em Aço Carbono", 320),
    ("Catalisadores Quimicos (bidao)", 340),
    ("Baterias de Lítio (palete)", 280),
    ("Polvora para Fogos Homologada (cx)", 200),
    ("Caixas Lacradas s/ Descricao", 150),
    ("Amostras Medicas Refrigeradas", 180),
    ("Material Eletronico Sigiloso (gov)", 120),
    ("Produtos Quimicos para Uso Agricola", 250),
]

NOMES_CAMUFLAGEM = [
    "Farinha Especial (saco)",
    "Tempero Importado (cx)",
    "Ferramenta Desmontada (lacrada)",
    "Peças Automotivas (uso geral)",
    "Suplemento Alimentar (palete)",
    "Material Ceramico Fino",
    "Componente Eletronico Frágil",
    "Produto Cosmetico a Granel",
    "Artesanato Regional (diverso)",
    "Peca Sobressalente (orig. autenticada)",
]

PAISES_ORIGEM = {
    "China":        ("Xangai", "CN", 2),
    "Estados Unidos":("Los Angeles", "US", 1),
    "Alemanha":     ("Hamburgo", "DE", 1),
    "Países Baixos":("Roterdã", "NL", 1),
    "Singapura":    ("Singapura", "SG", 1),
    "Coreia do Sul":("Busan", "KR", 1),
    "Japão":        ("Yokohama", "JP", 1),
    "Brasil":       ("Santos", "BR", 2),
    "Argentina":    ("Buenos Aires", "AR", 2),
    "Turquia":      ("Istambul", "TR", 3),
    "Índia":        ("Mumbai", "IN", 2),
    "Emirados Árabes":("Dubai", "AE", 2),
    "Nigéria":      ("Lagos", "NG", 4),
    "Rússia":       ("São Petersburgo", "RU", 4),
    "Venezuela":    ("Puerto Cabello", "VE", 5),
    "Irã":          ("Bandar Abbas", "IR", 5),
    "Colômbia":     ("Cartagena", "CO", 4),
    "Marrocos":     ("Casablanca", "MA", 3),
    "México":       ("Manzanillo", "MX", 3),
    "Malásia":      ("Port Klang", "MY", 2),
}

ARMADORES = ["MSCU", "MAEU", "TCKU", "HLXU", "OOLU", "CSNU", "EISU", "YMLU", "APHU", "TRHU", "HLBU"]

CHANCE_ITEM_SUSPEITO = 0.12
CHANCE_ISCA         = 0.18
CHANCE_CAMUFLAGEM   = 0.45

NARRATIVA_FRAGMENTOS = {
    "contexto_operacao": [
        {"ator": "Equipe de scanner", "local": "no pátio de triagem", "evidencia": "após nova varredura de densidade"},
        {"ator": "Fiscal de plantão", "local": "no gate de importação", "evidencia": "durante conferência de manifesto"},
        {"ator": "Centro de inteligência portuária", "local": "na doca secundária", "evidencia": "com base em alerta de rota"},
        {"ator": "Guarda portuária", "local": "na área alfandegada", "evidencia": "após cruzamento com imagens térmicas"},
    ],
    "metodo_ocultacao": [
        {"acao": "identificou fundo falso no assoalho", "evidencia": "com solda recente e parafusos fora do padrão", "tags": ["geral"]},
        {"acao": "localizou volumes misturados à carga declarada", "evidencia": "com lacres internos divergentes", "tags": ["geral"]},
        {"acao": "detectou tambores sem rastreabilidade", "evidencia": "com risco de dano ambiental", "tags": ["ambiental"]},
        {"acao": "encontrou caixas médicas sem cadeia fria comprovada", "evidencia": "com rotulagem sanitária inconsistente", "tags": ["farmaceutico"]},
    ],
    "reacao_equipe": [
        {"ator": "a Receita Federal", "acao": "reforçou o isolamento da área", "tags": ["geral"]},
        {"ator": "a Polícia Federal", "acao": "iniciou protocolo de custódia", "tags": ["geral"]},
        {"ator": "o IBAMA", "acao": "foi acionado para avaliação técnica imediata", "tags": ["ambiental"]},
        {"ator": "a ANVISA", "acao": "assumiu a verificação sanitária do lote", "tags": ["farmaceutico"]},
    ],
    "consequencia_legal": [
        {"consequencia": "com lavratura de auto de infração e retenção cautelar", "tags": ["geral"]},
        {"consequencia": "com abertura de inquérito e comunicação ao Ministério Público", "tags": ["geral"]},
        {"consequencia": "com processo administrativo ambiental e notificação do exportador", "tags": ["ambiental"]},
        {"consequencia": "com interdição sanitária e termo de recolhimento oficial", "tags": ["farmaceutico"]},
    ],
    "impacto_terminal": [
        {"consequencia": "gerando fila operacional no berço por até 2 horas"},
        {"consequencia": "aumentando a taxa de inspeção manual no turno"},
        {"consequencia": "bloqueando temporariamente a doca para perícia"},
        {"consequencia": "elevando o nível de alerta interno no terminal"},
    ],
}

def _digito_verificador(owner: str, serial: str) -> int:
    tabela = {c: i for i, c in enumerate("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")}
    valores = [tabela[c] * (2 ** i) for i, c in enumerate(owner + "U" + serial)]
    soma = sum(valores)
    return soma % 11 % 10

def gerar_id_conteiner() -> str:
    owner = random.choice(ARMADORES)
    serial = "".join(str(random.randint(0, 9)) for _ in range(6))
    digito = _digito_verificador(owner, serial)
    return f"{owner}U{serial}{digito}"
