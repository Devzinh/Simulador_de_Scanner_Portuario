# Simulador de Scanner Portuário (EBCO Systems)

Um simulador narrativo em Python baseado em texto onde você atua como um inspetor de cargas da EBCO Systems em diversos portos brasileiros. Seu trabalho é analisar manifestos de carga, ler o output de um scanner portuário e decidir o destino de cada conteiner. 

Erre três vezes e você estará demitido.

![Screenshots do Jogo (Opcional) - Substitua por uma imagem do seu terminal rodando o jogo]()

## 🛠️ Funcionalidades

- **Escaneamento Realista:** O scanner *nunca lhe diz o que é ilegal*. Ele reporta apenas anomalias de densidade (>300 kg/m³) e discrepâncias de peso. O jogador precisa cruzar os itens do manifesto com o peso e comportamento esperado.
- **Camuflagem Dinâmica:** Contrabandistas tentam enganar você misturando "Armas de Fogo" com "Farinha Especial", ou utilizando materiais que servem de isca para o scanner.
- **Inteligência Artificial de Decisão:** Sistema procedural que gera infinitos conteineres únicos. Nenhuma partida é igual a outra:
  - Dezenas de itens legítimos, suspeitos e camuflados.
  - Portos de origem globais com índices de risco (1 a 5).
  - Terminal de operação brasileiro pseudo-aleatório (Santos, Suape, Pecém, Manaus, etc).
- **Múltiplos Desfechos Policiais:** Baseado em procedimentos reais das polícias federais, IBAMA, ANVISA e Receita Federal. Você pode abrir IP (Inquérito Policial), efetuar prisões em flagrante, lacrar carga ou confiscar sob custódia do IML/COAF.
- **Sistema de Salvação (Save Game):** O jogo salva o estado do inspetor a cada conteiner. Se você fechar o terminal (ou forçar a saída com `Ctrl+C`), seu progresso até ali estará intacto para a próxima vez.

---

## 🏗️ Estrutura Arquitetural

O projeto foi dividido para ser modular e facilmente expansível:

- `main.py` — Ponto de entrada. Gerencia os menus interativos e a interface de terminal.
- `motor.py` — O "motor" pesado: lógica matemática do scanner de raio-X e montagem aleatória do conteiner.
- `eventos.py` — A espinha dorsal narrativa. Concentra todas as autoridades portuárias, as vistorias físicas e as dezenas de desfechos em cascata caso uma inspeção seja retida.
- `dados.py` — O banco de dados estático contendo wordlists de itens, portos, coeficientes de camuflagem e viaturas.
- `save.py` — Wrapper para leitura e gravação segura do arquivo `save_ebco.json`.

---

## 🚀 Como Jogar

1. Certifique-se de ter o Python (versão 3.10 ou superior) instalado no computador.
2. Clone o repositório ou baixe os arquivos.
3. No terminal (CMD, PowerShell ou Linux Shell), navegue até a pasta do projeto.
4. Rode as fileiras:

```bash
python main.py
```

O jogo será acionado no próprio terminal. Leia atentamente o peso das cargas e não deixe a pressa te gerar advertências ("strikes").

## ⚠️ Sobre o Ctrl+C
O jogo possui tratamento para Keyboard Interruptions. Se em qualquer tela você pressionar `Ctrl+C`, o simulador vai encerrar graciosamente, registrando seu último save, sem "sujar" o seu terminal de erros de compilação.

---

## 👩‍💻 Como Contribuir

- **Mais itens:** Adicione novas mercadorias no dicionário `ITENS_POR_TIPO` em `dados.py`.
- **Novas autoridades:** Se quiser incluir a Força Aérea ou Interpol, edite as constates `_EQUIPES` e `_UNIDADES_ACIONADAS` em `eventos.py`.
- Lembre-se que portos de destino/operação ficam dentro de `main.py`, enquanto origens de carga ficam em `dados.py`.

---
*Criado com fins didáticos para simulação de fluxo aduaneiro e tomada de decisão lógica.*
