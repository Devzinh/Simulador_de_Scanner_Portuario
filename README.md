# 🚢 Simulador de Scanner Portuário — EBCO Systems

<p align="center">
  <strong>Um jogo narrativo em terminal onde cada decisão aduaneira muda sua carreira.</strong>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img alt="Status" src="https://img.shields.io/badge/status-jog%C3%A1vel-22c55e?style=for-the-badge">
  <img alt="Interface" src="https://img.shields.io/badge/interface-terminal-111827?style=for-the-badge">
  <img alt="Licença" src="https://img.shields.io/badge/licen%C3%A7a-educacional-f59e0b?style=for-the-badge">
</p>

---

## 🎬 O que é este projeto?

No **Simulador de Scanner Portuário**, você assume o papel de um(a) inspetor(a) da **EBCO Systems** em operações de fiscalização de carga.

Seu trabalho é:
- ler os dados técnicos de scanner (densidade/peso/rota),
- identificar sinais de risco sem “resposta pronta”,
- decidir entre **liberar**, **reter** ou **acionar autoridades**.

> ⚠️ **Regra crítica**: o scanner não diz “isso é ilegal”. Ele só mostra sinais técnicos.
> A interpretação é toda sua.

Erre demais e sua reputação cai. Com **3 strikes**, você é afastado(a).

---

## ✨ Destaques de gameplay

- 🔎 **Scanner semi-realista**: alerta por densidade atípica e discrepância de peso.
- 🎭 **Camuflagem dinâmica**: itens suspeitos podem aparecer disfarçados.
- 🌍 **Risco por origem**: país/rota alteram probabilidades do motor.
- 🧠 **Sistema emergente**: auditorias e bônus de inteligência conforme desempenho.
- 🚔 **Múltiplos desfechos operacionais**: inspeção física, flagrante, encaminhamento legal.
- 💾 **Save robusto com integridade (HMAC)**: evita adulteração do progresso.

---

## 🧱 Arquitetura (visão rápida)

```text
main.py
  ├─ fluxo principal, interface e HUD
  ├─ chama motor.py para gerar/escanear conteiner
  ├─ chama eventos.py para decisões e consequências
  └─ persiste estado via save.py

motor.py
  ├─ geração procedural do conteiner
  └─ simulação do scanner e alertas técnicos

eventos.py
  ├─ árvore de decisões (liberar/reter/acionar)
  ├─ narrativas e desfechos (inspeção/flagrante)
  └─ aplicação de efeitos (reputação, eficiência, strikes)

dados.py
  ├─ catálogos de itens e países
  ├─ probabilidades base do jogo
  └─ fragmentos narrativos + geração de ID de conteiner

save.py
  ├─ sanitização de entrada
  ├─ assinatura HMAC do payload
  └─ leitura/escrita segura de save_ebco.json
```

---

## 🔁 Loop de jogo (como a rodada funciona)

1. O motor gera um contêiner com origem, tipo de carga, itens e pesos.
2. O scanner imprime sinais técnicos e possíveis alertas.
3. Você decide:
   - `[1]` Liberar,
   - `[2]` Reter para inspeção,
   - `[3]` Acionar autoridades.
4. O sistema resolve consequências e atualiza métricas:
   - `strikes`, `acertos/erros`, `reputação`, `casos_graves`, `falsos_alarmes`, `eficiência`.
5. O estado é salvo automaticamente ao final do ciclo.

---

## 🚀 Como executar

### Pré-requisitos
- Python **3.10+**

### Rodando localmente

```bash
python main.py
```

Pronto. O jogo roda 100% no terminal.

---

## 🎮 Controles e decisões

Durante o jogo, as escolhas são feitas por teclado (inputs numéricos e confirmações `s/n`).

- **[1] Liberar** → pode render eficiência, mas existe risco de auditoria posterior.
- **[2] Reter** → aumenta cautela, porém pode gerar falso alarme.
- **[3] Acionar autoridades** → ação forte, com chance de flagrante ou desgaste operacional.

💡 **Dica de estratégia**: use o conjunto completo de sinais (peso, densidade, origem e coerência narrativa dos itens), não apenas um alerta isolado.

---

## 💾 Save game e segurança

O progresso é salvo em `save_ebco.json` e assinado por HMAC usando chave local (`.ebco_key`).

Isso oferece:
- detecção de save adulterado,
- escrita atômica com arquivo temporário,
- migração com defaults para campos novos,
- sanitização do nome do jogador.

---

## 🧪 Balanceamento e customização

Se quiser ajustar dificuldade/conteúdo:

- `dados.py`
  - `CHANCE_ITEM_SUSPEITO`
  - `CHANCE_ISCA`
  - `CHANCE_CAMUFLAGEM`
  - listas de itens e países
- `eventos.py`
  - pesos de consequência (reputação/eficiência/strikes)
  - fluxos narrativos e opções de encaminhamento
- `motor.py`
  - lógica de risco por origem e discrepância de peso

---

## 🗂️ Estrutura do projeto

```text
.
├── main.py      # entrada e loop principal
├── motor.py     # geração procedural + scanner
├── eventos.py   # decisões, narrativas e efeitos
├── dados.py     # datasets e probabilidades
├── save.py      # persistência segura do progresso
└── README.md
```

---

## 🧭 Sugestões de evolução

- [ ] Adicionar testes automatizados para funções puras de motor/eventos.
- [ ] Criar modo “seed fixa” para depuração de partidas.
- [ ] Exportar relatório final do turno em JSON/CSV.
- [ ] Implementar níveis de dificuldade (Treinamento, Operacional, Crítico).
- [ ] Melhorar UX com paleta ANSI opcional e tema de cores.

---

## 🤝 Contribuição

Contribuições são bem-vindas para:
- novos itens e rotas,
- novos cenários narrativos,
- novos órgãos/equipes de fiscalização,
- melhorias de equilíbrio e progressão.

---

## 📌 Observações

Este projeto foi criado com foco didático/simulativo para exercitar lógica de decisão sob incerteza em contexto aduaneiro.

Se quiser, posso também montar uma versão do README com **GIF do terminal** (asciinema + preview em SVG/GIF) para deixá-lo ainda mais “animado” visualmente.
