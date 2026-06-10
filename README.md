# Love Data Day UFMG — Dinâmica "Construindo Juntos"
### Chatbot em Camadas: do Zero ao Function Calling

---

## Estrutura do Projeto

```
love-data-day-live-case/
├── scaffold.py               ← Esqueleto completo para os alunos preencherem
├── config.py                 ← Cliente LLM compartilhado (+ modo offline)
├── requirements.txt
├── .env.example
├── README.md
└── live-case-steps/          ← Dinâmicas ao vivo (um arquivo por nível)
    ├── nivel1.py             ←   Nível 1: Chatbot Simples
    ├── nivel2.py             ←   Nível 2: Chatbot com Memória
    └── nivel3.py             ←   Nível 3: Chatbot com Tool (Function Calling)
```

**`scaffold.py`** — arquivo único com os três níveis em estrutura esqueleto. Os campos marcados com `"???"` ficam em branco para o aluno preencher. Basta trocar `NIVEL = 1` para `2` ou `3` para executar cada etapa.

**`live-case-steps/`** — versão completa de cada nível, usada pelo professor durante a apresentação ao vivo.

---

## Setup (fazer antes da aula)

```bash
# 1. Criar e ativar um ambiente virtual isolado
python3 -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows

# 2. Instalar dependências dentro do venv
pip install -r requirements.txt

# 3. Criar arquivo de configuração
cp .env.example .env

# 4. Editar o .env com sua chave OpenAI
#    OPENAI_API_KEY=sk-...
#    USE_MOCK=false
```

> Sempre que abrir um novo terminal para rodar os scripts, lembre de ativar o venv primeiro (`source .venv/bin/activate`).

**Sem internet no dia?** Defina `USE_MOCK=true` no `.env`.
As respostas serão simuladas localmente — ideal para demonstrar o fluxo sem depender de API.

---

## Modo Offline

Defina `USE_MOCK=true` no `.env` para ativar respostas simuladas:

```
USE_MOCK=true
```

O mock responde `"[MOCK] Recebi: '...' — modo offline ativo."` e no Nível 3 simula um `tool_call` para demonstrar o fluxo completo sem API.

---

## Dependências

```
requests>=2.31.0
python-dotenv>=1.0.0
urllib3<2
```
