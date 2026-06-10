# ============================================================
# config.py — Configurações e cliente LLM compartilhado
# Love Data Day UFMG — Dinâmica "Construindo Juntos"
# ============================================================

import os
import json
import requests

# Carrega variáveis do arquivo .env, se existir
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # sem python-dotenv, usa os.environ diretamente

API_URL = "https://api.openai.com/v1/chat/completions"
MODELO  = "gpt-4o-mini"

# USE_MOCK=true no .env ativa respostas simuladas (sem internet)
USE_MOCK = os.getenv("USE_MOCK", "false").lower() == "true"


# ------------------------------------------------------------------
# Modo offline: respostas simuladas para quando não há internet
# ------------------------------------------------------------------
def _mock_llm(mensagens: list) -> str:
    ultima = next(
        (m["content"] for m in reversed(mensagens) if m.get("role") == "user"),
        "..."
    )
    trecho = ultima[:60] + ("..." if len(ultima) > 60 else "")
    return f"[MOCK] Recebi: '{trecho}' — modo offline ativo. Defina USE_MOCK=false para usar a API real."


def _mock_msg_com_tool(mensagens: list) -> dict:
    """Simula uma resposta com tool_call para demonstração offline."""
    # Parâmetros mock fixos por tool, para garantir um retorno válido
    _mock_params = {
        "tool_status_pedido": "12345",
        "tool_cardapio":      "pizza express",
        "tool_tempo_entrega": "pampulha",
        "tool_cupom":         "UFMG10",
    }
    ultima = next(
        (m["content"] for m in reversed(mensagens) if m.get("role") == "user"),
        "12345"
    )
    # Tenta usar o último token como parâmetro; cai no default "12345"
    parametro = ultima.split()[-1] if ultima.split()[-1].isalnum() else "12345"
    return {
        "role": "assistant",
        "content": None,
        "tool_calls": [{
            "id": "mock_tc_001",
            "type": "function",
            "function": {
                "name": "tool_escolhida",
                "arguments": json.dumps({"parametro": parametro}),
            },
        }],
    }


# ------------------------------------------------------------------
# Chamadas reais à API
# ------------------------------------------------------------------
def _get_headers() -> dict:
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError(
            "⚠️  OPENAI_API_KEY não encontrada.\n"
            "   Crie um arquivo .env com: OPENAI_API_KEY=sk-...\n"
            "   Ou defina USE_MOCK=true para modo offline."
        )
    return {"Authorization": f"Bearer {api_key}"}


def chamar_llm(mensagens: list) -> str:
    """Envia mensagens ao modelo e retorna o texto de resposta."""
    if USE_MOCK:
        return _mock_llm(mensagens)

    payload  = {"model": MODELO, "messages": mensagens, "temperature": 0.7}
    resposta = requests.post(API_URL, headers=_get_headers(), json=payload)
    resposta.raise_for_status()
    return resposta.json()["choices"][0]["message"]["content"]


def chamar_llm_com_tools(mensagens: list, tools: list) -> dict:
    """
    Envia mensagens + definições de tools.
    Retorna o objeto 'message' completo — pode conter tool_calls.
    """
    if USE_MOCK:
        return _mock_msg_com_tool(mensagens)

    payload  = {
        "model": MODELO,
        "messages": mensagens,
        "tools": tools,
        "tool_choice": "auto",
    }
    resposta = requests.post(API_URL, headers=_get_headers(), json=payload)
    resposta.raise_for_status()
    return resposta.json()["choices"][0]["message"]
