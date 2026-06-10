# ============================================================
# NÍVEL 3 — Chatbot com Tool (Function Calling)
# Love Data Day UFMG — Dinâmica "Construindo Juntos"
#
# Diferença do Nível 2:
#   ✅ O modelo pode "chamar funções" do nosso código.
#   ✅ Quando precisa de uma informação externa, ele emite um
#      tool_call e aguarda o resultado antes de responder.
#   ✅ A turma vota qual tool implementar!
# ============================================================

import json
from config import chamar_llm, chamar_llm_com_tools

# ──────────────────────────────────────────────────────────
#  TURMA DECIDE AQUI — mesmos valores dos níveis anteriores
# ──────────────────────────────────────────────────────────

NOME_ASSISTENTE = "???"
PERSONALIDADE   = "???"
PUBLICO         = "???"
TOPICOS         = "???"

# ── Sugestões (descomente se a turma travar) ──────────────
# NOME_ASSISTENTE = "Tobias"
# PERSONALIDADE   = "animado, usa emojis e linguagem descontraída"
# PUBLICO         = "consumidores do iFood"
# TOPICOS         = "rastreamento de pedidos, cancelamentos e cupons de desconto"
# ─────────────────────────────────────────────────────────


SYSTEM_PROMPT = f"""
Você é {NOME_ASSISTENTE}, assistente virtual do iFood para {PUBLICO}.
Personalidade: {PERSONALIDADE}.
Responda apenas sobre: {TOPICOS}.
Use as tools disponíveis quando precisar consultar informações específicas.
""".strip()

historico: list = []


# ══════════════════════════════════════════════════════════
#  TURMA VOTA AQUI — qual tool implementar?
#
#  Troque o valor de OPCAO_TOOL conforme a votação:
#    "A" → Consultar status de pedido
#    "B" → Consultar cardápio de restaurante
#    "C" → Calcular tempo estimado de entrega
#    "D" → Validar cupom de desconto
# ══════════════════════════════════════════════════════════

OPCAO_TOOL = "A"   # TURMA DECIDE: "A", "B", "C" ou "D"


# ------------------------------------------------------------------
# OPÇÃO A — Status de Pedido
# ------------------------------------------------------------------
def _tool_status_pedido(parametro: str) -> str:
    """Retorna o status de um pedido pelo ID."""
    dados = {
        "12345": "Em preparo 🍳 — seu restaurante está cozinhando o pedido.",
        "67890": "A caminho 🛵 — entregador Marcos está indo até você (8 min).",
        "11111": "Entregue ✅ — pedido entregue às 19h42.",
        "99999": "Cancelado ❌ — pedido cancelado a pedido do cliente.",
    }
    return dados.get(parametro, f"Pedido #{parametro} não encontrado. Verifique o número.")

_TOOL_DEF_A = {
    "type": "function",
    "function": {
        "name": "tool_escolhida",
        "description": "Consulta o status atual de um pedido iFood pelo número do pedido.",
        "parameters": {
            "type": "object",
            "properties": {
                "parametro": {
                    "type": "string",
                    "description": "Número (ID) do pedido a ser consultado.",
                },
            },
            "required": ["parametro"],
        },
    },
}


# ------------------------------------------------------------------
# OPÇÃO B — Cardápio de Restaurante
# ------------------------------------------------------------------
def _tool_cardapio(parametro: str) -> str:
    """Retorna itens em destaque do cardápio de um restaurante."""
    dados = {
        "pizza express": "🍕 Destaques: Margherita R$39, Calabresa R$42, Quatro Queijos R$45.",
        "burger king":   "🍔 Destaques: Whopper R$28, BK Duplo R$33, Chicken Crispy R$25.",
        "sushi yama":    "🍣 Destaques: Combo 30 peças R$89, Temaki Salmão R$29, Uramaki R$35.",
        "mcdonalds":     "🍟 Destaques: Big Mac R$26, McChicken R$22, McCombo R$35.",
    }
    chave = parametro.lower().strip()
    return dados.get(chave, f"Restaurante '{parametro}' não encontrado no catálogo.")

_TOOL_DEF_B = {
    "type": "function",
    "function": {
        "name": "tool_escolhida",
        "description": "Consulta os itens em destaque do cardápio de um restaurante parceiro iFood.",
        "parameters": {
            "type": "object",
            "properties": {
                "parametro": {
                    "type": "string",
                    "description": "Nome do restaurante a ser consultado.",
                },
            },
            "required": ["parametro"],
        },
    },
}


# ------------------------------------------------------------------
# OPÇÃO C — Tempo Estimado de Entrega
# ------------------------------------------------------------------
def _tool_tempo_entrega(parametro: str) -> str:
    """Retorna o tempo estimado de entrega para um bairro/região."""
    dados = {
        "pampulha":       "⏱️ Pampulha: estimativa de 25–35 minutos.",
        "savassi":        "⏱️ Savassi: estimativa de 15–20 minutos (muitos entregadores na região).",
        "contagem":       "⏱️ Contagem: estimativa de 40–55 minutos.",
        "centro":         "⏱️ Centro: estimativa de 20–30 minutos.",
        "buritis":        "⏱️ Buritis: estimativa de 30–40 minutos.",
    }
    chave = parametro.lower().strip()
    return dados.get(chave, f"Região '{parametro}' sem dados de estimativa disponíveis no momento.")

_TOOL_DEF_C = {
    "type": "function",
    "function": {
        "name": "tool_escolhida",
        "description": "Estima o tempo médio de entrega do iFood para um bairro ou região.",
        "parameters": {
            "type": "object",
            "properties": {
                "parametro": {
                    "type": "string",
                    "description": "Nome do bairro ou região para estimar o tempo de entrega.",
                },
            },
            "required": ["parametro"],
        },
    },
}


# ------------------------------------------------------------------
# OPÇÃO D — Validar Cupom de Desconto
# ------------------------------------------------------------------
def _tool_cupom(parametro: str) -> str:
    """Valida um cupom de desconto e retorna as condições."""
    dados = {
        "UFMG10":    "✅ Cupom válido! 10% de desconto em pedidos acima de R$30. Validade: 30/06/2026.",
        "PRIMEIRAENTREGA": "✅ Cupom válido! Entrega grátis no primeiro pedido. Sem pedido mínimo.",
        "BLACKFRIDAY": "❌ Cupom expirado. Promoção encerrada em 29/11/2025.",
        "FRETE0":     "✅ Cupom válido! Frete grátis em pedidos acima de R$50. Validade: 15/06/2026.",
    }
    chave = parametro.upper().strip()
    return dados.get(chave, f"Cupom '{parametro}' não encontrado ou inválido.")

_TOOL_DEF_D = {
    "type": "function",
    "function": {
        "name": "tool_escolhida",
        "description": "Valida um cupom de desconto iFood e retorna as condições de uso.",
        "parameters": {
            "type": "object",
            "properties": {
                "parametro": {
                    "type": "string",
                    "description": "Código do cupom de desconto a ser validado.",
                },
            },
            "required": ["parametro"],
        },
    },
}


# ------------------------------------------------------------------
# Seletor de tool conforme voto da turma
# ------------------------------------------------------------------
_OPCOES = {
    "A": (_tool_status_pedido, _TOOL_DEF_A,
          "Consultar status de pedido (ex: 12345, 67890)"),
    "B": (_tool_cardapio,      _TOOL_DEF_B,
          "Consultar cardápio (ex: pizza express, mcdonalds)"),
    "C": (_tool_tempo_entrega, _TOOL_DEF_C,
          "Tempo de entrega (ex: pampulha, savassi, centro)"),
    "D": (_tool_cupom,         _TOOL_DEF_D,
          "Validar cupom (ex: UFMG10, PRIMEIRAENTREGA, FRETE0)"),
}

if OPCAO_TOOL not in _OPCOES:
    raise ValueError(f"OPCAO_TOOL deve ser 'A', 'B', 'C' ou 'D'. Recebido: '{OPCAO_TOOL}'")

tool_escolhida_fn, TOOL_DEF, DICA_EXEMPLO = _OPCOES[OPCAO_TOOL]
TOOLS = [TOOL_DEF]


# ------------------------------------------------------------------
# Função principal do chatbot com tool
# ------------------------------------------------------------------
def chatbot_com_tool(pergunta: str) -> str:
    global historico

    historico.append({"role": "user", "content": pergunta})
    mensagens = [{"role": "system", "content": SYSTEM_PROMPT}] + historico

    # 1ª chamada: o modelo decide se aciona a tool ou responde direto
    msg = chamar_llm_com_tools(mensagens, TOOLS)

    if msg.get("tool_calls"):
        tc     = msg["tool_calls"][0]
        args   = json.loads(tc["function"]["arguments"])
        result = tool_escolhida_fn(args["parametro"])

        print(f"\n   🔧 Tool acionada : {tc['function']['name']}({args})")
        print(f"   📦 Resultado     : {result}\n")

        # Adiciona a resposta do modelo + resultado da tool ao contexto
        mensagens.append(msg)
        mensagens.append({
            "role": "tool",
            "tool_call_id": tc["id"],
            "content": result,
        })

        # 2ª chamada: o modelo formula a resposta final com o resultado
        resposta_final = chamar_llm(mensagens)
        historico.append({"role": "assistant", "content": resposta_final})
        return resposta_final

    # Modelo respondeu direto, sem acionar tool
    resposta_direta = msg.get("content", "")
    historico.append({"role": "assistant", "content": resposta_direta})
    return resposta_direta


def limpar_memoria() -> None:
    global historico
    historico = []
    print("🗑️  Memória apagada! Nova conversa iniciada.\n")


# ──────────────────────────────────────────────────────────
#  Loop interativo — rode com: python nivel3.py
# ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    nome_opcao = {
        "A": "Status de Pedido",
        "B": "Cardápio de Restaurante",
        "C": "Tempo de Entrega",
        "D": "Validação de Cupom",
    }[OPCAO_TOOL]

    print(f"\n🤖  {NOME_ASSISTENTE} online com tool!  (digite 'sair' para encerrar)\n")
    print(f"   Tool ativa: Opção {OPCAO_TOOL} — {nome_opcao}")
    print(f"   💡 Tente  : '{DICA_EXEMPLO}'")
    print(f"   Comandos  : 'limpar' apaga o histórico | 'sair' encerra")
    print("-" * 55)

    while True:
        try:
            entrada = input(f"\nVocê [{len(historico)//2 + 1}]: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando...")
            break

        if entrada.lower() in ("sair", "exit", "quit"):
            print("Até logo! 👋")
            break
        if entrada.lower() == "limpar":
            limpar_memoria()
            continue
        if not entrada:
            continue

        resposta = chatbot_com_tool(entrada)
        print(f"\n{NOME_ASSISTENTE}: {resposta}")
