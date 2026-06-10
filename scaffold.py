# ============================================================
# scaffold.py — Esqueleto Completo do Case
# Love Data Day UFMG — Dinâmica "Construindo Juntos"
#
# Este arquivo contém a estrutura dos três níveis do chatbot.
# Preencha os campos marcados com "???" para completar o exercício.
#
# Para rodar:
#   pip install -r requirements.txt
#   cp .env.example .env   # adicione sua OPENAI_API_KEY
#   python scaffold.py
#
# Sem internet? Defina USE_MOCK=true no .env
# ============================================================

import os
import json
import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

API_URL  = "https://api.openai.com/v1/chat/completions"
MODELO   = "gpt-4o-mini"
USE_MOCK = os.getenv("USE_MOCK", "false").lower() == "true"


# ──────────────────────────────────────────────────────────
# Cliente LLM
# ──────────────────────────────────────────────────────────

def chamar_llm(mensagens: list) -> str:
    if USE_MOCK:
        ultima = next((m["content"] for m in reversed(mensagens) if m["role"] == "user"), "...")
        return f"[MOCK] Recebi: '{ultima[:60]}' — modo offline ativo."

    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("⚠️  Defina OPENAI_API_KEY no arquivo .env")

    headers  = {"Authorization": f"Bearer {api_key}"}
    payload  = {"model": MODELO, "messages": mensagens, "temperature": 0.7}
    resposta = requests.post(API_URL, headers=headers, json=payload)
    resposta.raise_for_status()
    return resposta.json()["choices"][0]["message"]["content"]


def chamar_llm_com_tools(mensagens: list, tools: list) -> dict:
    if USE_MOCK:
        ultima = next((m["content"] for m in reversed(mensagens) if m["role"] == "user"), "123")
        return {
            "content": None,
            "tool_calls": [{
                "id": "mock_tc_001",
                "type": "function",
                "function": {
                    "name": "minha_tool",
                    "arguments": json.dumps({"parametro": ultima.split()[-1]}),
                },
            }],
        }

    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("⚠️  Defina OPENAI_API_KEY no arquivo .env")

    headers  = {"Authorization": f"Bearer {api_key}"}
    payload  = {"model": MODELO, "messages": mensagens, "tools": tools, "tool_choice": "auto"}
    resposta = requests.post(API_URL, headers=headers, json=payload)
    resposta.raise_for_status()
    return resposta.json()["choices"][0]["message"]


# ══════════════════════════════════════════════════════════
# CONFIGURAÇÃO DO ASSISTENTE
# Preencha as variáveis abaixo antes de rodar qualquer nível.
# ══════════════════════════════════════════════════════════

NOME_ASSISTENTE = "???"   # Ex: "Tobias"
PERSONALIDADE   = "???"   # Ex: "animado, usa emojis e linguagem descontraída"
PUBLICO         = "???"   # Ex: "consumidores do iFood"
TOPICOS         = "???"   # Ex: "rastreamento de pedidos, cancelamentos e cupons"

SYSTEM_PROMPT = f"""
Você é {NOME_ASSISTENTE}, assistente virtual do iFood para {PUBLICO}.
Personalidade: {PERSONALIDADE}.
Responda apenas sobre: {TOPICOS}.
Se a pergunta fugir desses tópicos, redirecione o usuário gentilmente.
""".strip()


# ══════════════════════════════════════════════════════════
# NÍVEL 1 — Chatbot Simples
#
# Conceito: uma pergunta → uma resposta, sem contexto anterior.
# O model recebe apenas o system prompt + a mensagem atual.
# ══════════════════════════════════════════════════════════

def chatbot_simples(pergunta: str) -> str:
    mensagens = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": pergunta},
    ]
    return chamar_llm(mensagens)


# ══════════════════════════════════════════════════════════
# NÍVEL 2 — Chatbot com Memória
#
# Conceito: acumulamos todas as mensagens em 'historico' e
# enviamos o contexto completo a cada novo turno.
# O model "lembra" o que foi dito antes.
# ══════════════════════════════════════════════════════════

historico: list = []


def chatbot_com_memoria(pergunta: str) -> str:
    global historico

    # 1. Registra a pergunta do usuário
    historico.append({"role": "user", "content": pergunta})

    # 2. Monta: system fixo + histórico completo
    mensagens = [{"role": "system", "content": SYSTEM_PROMPT}] + historico

    # 3. Chama o modelo
    resposta = chamar_llm(mensagens)

    # 4. Registra a resposta do assistente para os próximos turnos
    historico.append({"role": "assistant", "content": resposta})

    return resposta


# ══════════════════════════════════════════════════════════
# NÍVEL 3 — Chatbot com Tool (Function Calling)
#
# Conceito: o model pode "chamar" uma função do nosso código
# para buscar dados externos antes de formular a resposta.
#
# Preencha:
#   minha_tool()  → lógica da função (o que ela retorna?)
#   TOOLS         → descrição JSON Schema para o modelo
# ══════════════════════════════════════════════════════════

def minha_tool(parametro: str) -> str:
    """O que essa função faz? Preencha os dados abaixo."""
    dados = {
        "???": "???",   # chave: valor de retorno
        "???": "???",   # adicione mais entradas conforme necessário
    }
    return dados.get(parametro, "Informação não encontrada.")


TOOLS = [{
    "type": "function",
    "function": {
        "name": "minha_tool",
        "description": "???",   # Descreva o que a função faz (o modelo lê isso para decidir quando usá-la)
        "parameters": {
            "type": "object",
            "properties": {
                "parametro": {
                    "type": "string",
                    "description": "???",   # Descreva o que o parâmetro representa
                },
            },
            "required": ["parametro"],
        },
    },
}]


def chatbot_com_tool(pergunta: str) -> str:
    mensagens = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": pergunta},
    ]

    # 1ª chamada: o modelo decide se usa a tool ou responde direto
    msg = chamar_llm_com_tools(mensagens, TOOLS)

    if msg.get("tool_calls"):
        tc     = msg["tool_calls"][0]
        args   = json.loads(tc["function"]["arguments"])
        result = minha_tool(args["parametro"])

        print(f"\n   🔧 Tool acionada : {tc['function']['name']}({args})")
        print(f"   📦 Resultado     : {result}\n")

        # Adiciona a chamada + resultado ao contexto
        mensagens.append(msg)
        mensagens.append({
            "role": "tool",
            "tool_call_id": tc["id"],
            "content": result,
        })

        # 2ª chamada: modelo formula a resposta com o resultado em mãos
        return chamar_llm(mensagens)

    return msg.get("content", "")


# ══════════════════════════════════════════════════════════
# ESCOLHA O NÍVEL PARA RODAR
# Troque o valor de NIVEL para 1, 2 ou 3.
# ══════════════════════════════════════════════════════════

NIVEL = 1   # 1 → simples | 2 → com memória | 3 → com tool

_FUNCOES = {
    1: chatbot_simples,
    2: chatbot_com_memoria,
    3: chatbot_com_tool,
}

_NOMES = {
    1: "Nível 1 — Chatbot Simples",
    2: "Nível 2 — Chatbot com Memória",
    3: "Nível 3 — Chatbot com Tool",
}

if __name__ == "__main__":
    if NIVEL not in _FUNCOES:
        raise ValueError(f"NIVEL deve ser 1, 2 ou 3. Recebido: {NIVEL}")

    chatbot = _FUNCOES[NIVEL]

    print(f"\n🤖  {NOME_ASSISTENTE} online!  [{_NOMES[NIVEL]}]")
    print(f"   (digite 'sair' para encerrar)\n")
    print("-" * 55)

    while True:
        try:
            entrada = input("\nVocê: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando...")
            break

        if entrada.lower() in ("sair", "exit", "quit"):
            print("Até logo! 👋")
            break
        if not entrada:
            continue

        resposta = chatbot(entrada)
        print(f"\n{NOME_ASSISTENTE}: {resposta}")
