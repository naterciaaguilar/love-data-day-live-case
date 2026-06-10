# Roteiro para o Professor
### Love Data Day UFMG — Dinâmica "Construindo Juntos"

---

## Nível 1 — Chatbot Simples (`nivel1.py`)

**Conceito:** system prompt + pergunta → resposta. Sem memória entre turnos.

**Ao vivo com a turma:**
1. Abra `nivel1.py` no editor
2. Peça para a turma preencher as 4 variáveis:
   - `NOME_ASSISTENTE` — nome do bot
   - `PERSONALIDADE` — tom de voz
   - `PUBLICO` — para quem ele fala
   - `TOPICOS` — o que ele pode responder
3. Rode: `python nivel1.py`
4. Mostre que **perguntas fora do tópico são redirecionadas**
5. Mostre que ele **não lembra** de turnos anteriores

**Pergunta para turma:** *"Façam duas perguntas seguidas onde a segunda depende da primeira. O que acontece?"*

---

## Nível 2 — Chatbot com Memória (`nivel2.py`)

**Conceito:** acumulamos o histórico em uma lista e enviamos tudo para o modelo a cada turno.

**Ao vivo com a turma:**
1. Abra `nivel2.py` e compare com `nivel1.py`
2. Mostre a lista `historico` e a função `chatbot_com_memoria`
3. Pergunte: *"O que acontece se não salvarmos a resposta do assistente no histórico?"*
4. Rode: `python nivel2.py`
5. Teste uma conversa com referências ao contexto anterior
6. Use o comando `limpar` para mostrar o reset do histórico
7. Mostre o contador `[📝 Histórico: N mensagens]` crescendo

**Ponto de discussão:** *"Qual o limite dessa abordagem? O que acontece com conversas muito longas?"* *(context window, custo por token)*

---

## Nível 3 — Chatbot com Tool (`nivel3.py`)

**Conceito:** o modelo pode chamar funções do nosso código para buscar dados externos.

**Votação na tela (projete as opções):**

| Opção | Tool | Exemplo de uso |
|-------|------|----------------|
| **A** | Status de pedido | "Qual o status do pedido 12345?" |
| **B** | Cardápio de restaurante | "O que tem no cardápio do Pizza Express?" |
| **C** | Tempo de entrega | "Quanto tempo demora para entregar na Pampulha?" |
| **D** | Validar cupom | "O cupom UFMG10 é válido?" |

**Ao vivo com a turma:**
1. Abra `nivel3.py` e mostre a estrutura de `TOOLS` (JSON Schema)
2. A turma vota → troque o valor de `OPCAO_TOOL` para `"A"`, `"B"`, `"C"` ou `"D"`
3. Rode: `python nivel3.py`
4. Faça uma pergunta que **acione a tool** → mostre os logs `🔧 Tool acionada` e `📦 Resultado`
5. Faça uma pergunta que **não precise da tool** → o modelo responde direto
6. Explique o fluxo de duas chamadas: decidir → executar → formular resposta

**Ponto de discussão:** *"Como o modelo sabe quando usar a tool? Que informação no JSON Schema o orienta?"* *(campo `description`)*

---

## Dados de teste prontos (Nível 3)

| Opção A — Pedidos | Opção B — Restaurantes |
|---|---|
| `12345` → Em preparo | `pizza express` → Margherita, Calabresa |
| `67890` → A caminho | `burger king` → Whopper, BK Duplo |
| `11111` → Entregue | `sushi yama` → Combo 30 peças |
| `99999` → Cancelado | `mcdonalds` → Big Mac, McChicken |

| Opção C — Bairros BH | Opção D — Cupons |
|---|---|
| `pampulha` → 25–35 min | `UFMG10` → 10% off (válido) |
| `savassi` → 15–20 min | `PRIMEIRAENTREGA` → frete grátis |
| `contagem` → 40–55 min | `BLACKFRIDAY` → expirado |
| `centro` → 20–30 min | `FRETE0` → frete grátis acima R$50 |
