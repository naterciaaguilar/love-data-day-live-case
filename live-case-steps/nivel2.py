# ============================================================
# NÍVEL 2 — Chatbot com Memória
# Love Data Day UFMG — Dinâmica "Construindo Juntos"
#
# Diferença do Nível 1:
#   ✅ Mantemos o 'historico' de mensagens entre as perguntas.
#   ✅ A cada turno, enviamos TUDO: system + histórico + nova pergunta.
#   ✅ O modelo "lembra" do que foi dito antes.
# ============================================================

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import chamar_llm

# ──────────────────────────────────────────────────────────
#  TURMA DECIDE AQUI — mesmos valores do Nível 1
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
Se a pergunta fugir desses tópicos, redirecione o usuário gentilmente.
""".strip()


# ──────────────────────────────────────────────────────────
#  MEMÓRIA: lista que acumula o histórico da conversa
# ──────────────────────────────────────────────────────────
historico: list = []


def chatbot_com_memoria(pergunta: str) -> str:
    global historico

    # 1. Adiciona a pergunta do usuário ao histórico
    historico.append({"role": "user", "content": pergunta})

    # 2. Monta as mensagens: system fixo + todo o histórico
    mensagens = [{"role": "system", "content": SYSTEM_PROMPT}] + historico

    # 3. Chama o modelo com o contexto completo
    resposta = chamar_llm(mensagens)

    # 4. TURMA DECIDE AQUI — o que fazer com a resposta?
    #    Dica: precisamos salvar ela no histórico também!
    historico.append({"role": "assistant", "content": resposta})

    return resposta


def limpar_memoria() -> None:
    """Apaga o histórico para começar uma nova conversa."""
    global historico
    historico = []
    print("🗑️  Memória apagada! Nova conversa iniciada.\n")


# ──────────────────────────────────────────────────────────
#  Loop interativo — rode com: python nivel2.py
#  Comandos especiais: 'limpar' apaga o histórico, 'sair' encerra.
# ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n🤖  {NOME_ASSISTENTE} online com memória!  (digite 'sair' para encerrar)\n")
    print(f"   Público   : {PUBLICO}")
    print(f"   Tópicos   : {TOPICOS}")
    print(f"   💡 Dica   : tente se referir a algo dito antes — ele vai lembrar!\n")
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

        resposta = chatbot_com_memoria(entrada)
        print(f"\n{NOME_ASSISTENTE}: {resposta}")
        print(f"\n   [📝 Histórico: {len(historico)} mensagens acumuladas]")
