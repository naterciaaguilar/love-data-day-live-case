# ============================================================
# NÍVEL 1 — Chatbot Simples
# Love Data Day UFMG — Dinâmica "Construindo Juntos"
#
# Conceito: system prompt + uma mensagem do usuário → resposta
# Sem memória: cada pergunta é tratada de forma independente.
# ============================================================

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import chamar_llm

# ──────────────────────────────────────────────────────────
#  TURMA DECIDE AQUI — preencha ao vivo com a turma!
# ──────────────────────────────────────────────────────────

NOME_ASSISTENTE = "???"   # Qual o nome do nosso assistente?
PERSONALIDADE   = "???"   # Como ele deve se comportar?
PUBLICO         = "???"   # Para quem ele fala: consumidor, entregador ou parceiro?
TOPICOS         = "???"   # Quais assuntos ele pode responder?

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
Se a pergunta fugir desses tópicos, redirecione o usuário gentilmente.
""".strip()


def chatbot_simples(pergunta: str) -> str:
    mensagens = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": pergunta},
    ]
    return chamar_llm(mensagens)


# ──────────────────────────────────────────────────────────
#  Loop interativo — rode com: python nivel1.py
# ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n🤖  {NOME_ASSISTENTE} online!  (digite 'sair' para encerrar)\n")
    print(f"   Público   : {PUBLICO}")
    print(f"   Tópicos   : {TOPICOS}")
    print(f"   Personalid: {PERSONALIDADE}\n")
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

        resposta = chatbot_simples(entrada)
        print(f"\n{NOME_ASSISTENTE}: {resposta}")
