# CONTAMINAÇÃO R4/K08 — ESCOLHA FECHADA E ISOMORFO

**Estado:** validação de software sobre casos integralmente sintéticos; produção não certificada. Nenhum modelo foi executado, nenhum resultado real foi aberto, nenhum T6/material reservado foi usado e nenhum artigo público foi usado como insumo ou alterado nesta frente.

## Arquivos entregues

### `K08/EXTRACAO/`

- Código: `extrator_fechado.py`, `gerar_casos.py`, `executar_casos.py`, `inducao.py`, `validar_reproducao.py`.
- Método: `METODO_EXTRACAO.md`.
- Casos e saídas: `casos_sinteticos.json`, `saidas_casos.json`, `metricas_casos.json`, `RELATORIO_CASOS.md`.
- Indução: `saidas_inducao.json`, `metricas_inducao.json`, `RELATORIO_INDUCAO.md`.
- Reprodutibilidade: `REPRODUCAO.json`.

### `K08/ISOMORFO/`

- Máquina e insumos: `maquina_isomorfa.py`, `executar_isomorfo.py`, `dicionario_sintetico_v1.json`, `fontes_sinteticas.json`, `PLANO_ISOMORFO.md`.
- Alternativa contrafactual: `texto_original_numerico_sintetico.txt`, `texto_contrafactual_isomorfo.txt`, `gabarito_contrafactual_isomorfo.json`, `sondas_memoria_contrafactual.json`.
- Alternativa sem números: `texto_sem_numeros_original_sintetico.txt`, `texto_sem_numeros_isomorfo.txt`, `gabarito_sem_numeros_isomorfo.json`.
- Sem Nome, pela mesma máquina: `texto_sem_nome_contrafactual.txt`, `gabarito_sem_nome_contrafactual.json`, `texto_sem_nome_sem_numeros.txt`, `gabarito_sem_nome_sem_numeros.json`, `formulas_avaliadas.json`.
- Verificação: `alternativas_numericas.json`, `validacao_isomorfo.json`, `RELATORIO_ISOMORFO.md`, `manifesto.json`.

## 1. Escolha fechada: contrato e o que mudou

Para cada asserção apresentada, a resposta é uma escolha entre:

- **SIM** — o texto afirma a proposição;
- **NÃO** — o texto afirma sua negação ou uma proposição explicitamente incompatível;
- **O TEXTO NÃO DIZ** — o texto não afirma nem nega; citação sem endosso e termos soltos ficam aqui.

O bloco usa `INICIO_LEITURA_K08`, uma linha `ID=RÓTULO` por asserção e `FIM_LEITURA_K08`. A pontuação é por ID, determinística e sem LLM juiz. Não se usa a antiga gramática K06R1 nem uma tupla sujeito–relação–objeto.

Preâmbulo fora de um único bloco e ordem diversa dos IDs não zeram mais o conteúdo; ambos são marcados como forma não canônica. Bloco duplo, ID duplicado/desconhecido/ausente, truncamento, resposta vazia, registro fora do bloco e rótulo em inglês invalidam o bloco para a medida conjunta. Não se escolhe um bloco favorável nem se recuperam acertos parciais de um bloco ambíguo.

### O que resolve

1. Reduz a obediência a uma gramática de tuplas e elimina o falso negativo de uma leitura correta causado apenas por preâmbulo externo ou reordenação.
2. Separa afirmação, negação e silêncio, inclusive citação sem relação de endosso.
3. Separa formato analisável, formato canônico e conteúdo, impedindo que um bloco perfeito seja chamado de leitura correta.
4. Permite medir ordem, iscas e controle só gramática sem modelo como juiz.

### O que NÃO resolve

1. **Indução pela pergunta:** as asserções e o vocabulário são fornecidos; mede-se verificação/reconhecimento, não extração espontânea nem descoberta da fórmula.
2. **Cópia e adivinhação:** um copiador do gabarito ou uma regra fixa ainda pode acertar forma e conteúdo; iscas finitas não cobrem todas as estratégias.
3. **Validação semântica real:** o extrator lê rótulos, não interpreta prosa; saídas reais continuam precisando de gabarito humano independente.
4. **Convergência:** um escore num passo não mede pouso, retorno, memória, alteração de pesos ou dinâmica temporal.
5. **Consistência pelo parser:** P e ¬P aparecem como itens separados e ambos podem receber SIM; a insatisfatibilidade é verificada por uma camada lógica à parte.

## 2. Casos, taxas e falhas

A bateria contém os tipos correto, cita sem relacionar, negação, truncado, inglês, vazio, outros nomes, prosa com preâmbulo, ordem diversa, IDs desconhecidos/duplicados, bloco adversarial duplo, conteúdo errado com formato válido e contradição explícita.

| Medida | Resultado | Interpretação permitida |
|---|---:|---|
| Casos / falhas do contrato esperado | 15 / 0 | O software implementou o contrato sintético previsto. |
| Blocos analisáveis | 8/15 = 53,3 % | Apenas forma; os outros casos foram construídos como inválidos. |
| Blocos canônicos | 6/15 = 40,0 % | Forma estrita, sem preâmbulo e na ordem apresentada. |
| Conteúdo entre analisáveis | 25/27 = 92,6 % | Inclui o caso deliberadamente errado C14; não é taxa de modelo. |
| Medida conjunta | 25/55 = 45,5 % | Bloco inválido contribui zero acertos; não é taxa de produção. |
| Formato válido e conteúdo errado | C14, 2/4 | Sucesso de formato não é compreensão nem convergência. |

Os gabaritos são literais e independentes do parser, mas casos e gabaritos têm o mesmo autor; a validação humana independente de saídas realistas permanece aberta.

## 3. Indução: ordem, iscas e só gramática

As sementes **13, 29, 53 e 79** estão fixadas no código; com a ordem original são cinco ordens. O produto completo contém dois textos, três mecanismos e cinco ordens: **30 respostas e 210 células**, todas emitidas. Nenhum resultado foi escolhido ou omitido.

As métricas são formato analisável/canônico, conteúdo entre válidos, medida conjunta, acerto por rótulo, confusões negação↔silêncio, endosso de iscas com SIM, amplitude de acurácia entre ordens e invariância de rótulos por ID.

| Texto | Mecanismo sintético | Formato | Conteúdo | Endosso de iscas | Amplitude por ordem |
|---|---|---:|---:|---:|---:|
| Original | Oráculo de fiação | 100 % | 100 % | 0 % | 0,000 |
| Original | Sempre-SIM | 100 % | 28,6 % | 100 % | 0,000 |
| Original | Memória posicional | 100 % | 48,6 % | 33,3 % | 0,714 |
| Só gramática | Oráculo de fiação | 100 % | 100 % | 0 % | 0,000 |
| Só gramática | Sempre-SIM | 100 % | 0 % | 100 % | 0,000 |
| Só gramática | Memória posicional | 100 % | 28,6 % | 33,3 % | 0,000 |

O sempre-SIM também tem invariância de rótulos de 100 %: invariância e formato podem ser perfeitos sem leitura. O oráculo só verifica a fiação. Esses mecanismos demonstram que os controles funcionam nos casos construídos; **não medem indução de um modelo real**.

## 4. Plano isomorfo e números com história

O dicionário é `k08-sintetico-v1`, versão 1, SHA-256 `76f63bd936fc8cbe0edb5beb5debeef1873d7ac9d0011a0974282d50afc5f3c8`. Texto, asserções, polaridades e gabarito passam pela mesma máquina, em uma passagem sem cascata. IDs permanecem e o mesmo extrator mede todos os braços.

### Alternativa (i): contrafactual factual coerente

- `40,0 s → 46,0 s` e `42,0 s → 43,0 s`; nenhuma das duas quantidades medidas fica intacta.
- A conclusão dependente muda de “a segunda foi mais lenta” para “a segunda foi mais rápida”; unidade e igualdade do número de oscilações são preservadas.
- “Primeira/segunda” são índices estruturais, não medidas. As sondas que conservam valores antigos ficam fora do texto e do gabarito principais.
- NUM01, NUM02 e REL01 documentam as mudanças. Quatro das seis sondas originais mudam de rótulo no contrafactual, tornando testável seguir a história versus seguir o novo texto.

**Testável agora:** coerência interna, ausência dos números antigos, transformação do gabarito e mesmo extrator no exemplo sintético. **Preço e bloqueio:** não é isomorfo factual estrito; texto real exige curadoria independente de coerência e dificuldade. Nenhuma medida da natureza foi trocada como rótulo.

### Alternativa (ii): restrição a textos sem números

**Testável agora:** renomeação por aliases declarados, gabarito, contradição mínima e mesmo extrator no texto qualitativo sintético; o guarda lexical não encontrou números antes ou depois. **Preço e bloqueio:** não testa contaminação numérica e não se aplica a textos com medidas. O guarda não prova ausência de toda quantidade implícita.

As duas alternativas são emitidas sem ranking e com `selected_arm=null`. A primeira examina números com história ao alterar fatos; a segunda preserva o escopo qualitativo ao excluir números. Não há escolha escondida.

## 5. Sem Nome e reintrodução acidental

A mesma máquina insere uma única negação de um literal já afirmado e transforma o resultado. P e ¬P recebem SIM em itens separados.

| Braço | Base: custo mínimo / leituras zero | Sem Nome: custo mínimo / leituras zero | Uma inserção removida restaura a base |
|---|---:|---:|---:|
| Contrafactual | 0 / 1 | 1 / 0 | Exatamente |
| Sem números | 0 / 1 | 1 / 0 | Exatamente |

O enumerador trata da **fórmula mínima declarada para a contradição**, não de uma formalização completa de todos os fatos. Nela não há reintrodução de leitura de custo zero. A auditoria separada não encontrou nomes-fonte nem números antigos; a troca comparativa bidirecional é validada por distinção textual e polaridade.

## 6. Verificações, reprodução e bloqueios

- Isomorfo: **34/34 verificações atuais aprovadas**, incluindo quatro controles negativos: número sem política, número intacto, número no braço restrito e reintrodução lexical deliberada são detectados.
- Falha de desenvolvimento corrigida: a primeira transformação comparativa colidiu N03/N04; o par foi tornado bidirecional e o teste `TEXTOS_DE_POLARIDADE_DISTINTOS` foi acrescentado. Não se oculta essa falha no histórico de validação.
- Fiação pelo mesmo extrator: 6/6 na base, no isomorfo e no sem Nome numérico; 5/5 nos três braços qualitativos. **Esses 100 % são construção e formato, não desempenho nem convergência.**
- Duas execuções completas foram byte a byte idênticas nos **34 arquivos rastreados**, sem diferenças. `REPRODUCAO.json` fica fora do próprio hash. SHA-256 combinado: `83e78c718042bd70066e17452fe1a020d5a07574cc6812909ba19caae116c2e5`.
- Repetição: a partir de `K08/EXTRACAO/`, `python -B validar_reproducao.py` executa somente os scripts sintéticos das duas pastas.

**Bloqueios restantes:** saídas reais e gabarito humano independente; efeito real de indução; curadoria contrafactual e equivalência de dificuldade; escopo de textos com números na alternativa restrita; validação da fórmula completa de qualquer texto real; e qualquer inferência temporal ou de convergência. Nada nesta frente certifica produção.
