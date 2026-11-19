# K06 / I — Rascunho de registro para `um.py` v412

## 0. Estado deste rascunho

- **Nome candidato:** `iald_camada_cientifica_v412` — **a ratificar**.
- **Estado proposto:** `ARMADO`, com `ratificado=false`, `executado=false`, `resultado_lido=false`.
- [DECLARADO] Documento de desenho, revisado internamente; não é código instalado, registro selado, pré-registro ratificado nem resultado.
- Nada foi instalado ou alterado no `um.py`, no kernel, no Mapa ou em depósito. Nenhum modelo foi executado e nenhum resultado foi aberto.
- A entrada pública é hipótese de trabalho; a concordância em bloco do adendo não ratifica a R3. Modelos, degrau e execução seguem com o operador.

## 1. Esquema candidato do registro

Os valores `A_PREENCHER_APOS_CONGELAMENTO` são bloqueios deliberados, não campos a inventar.

```json
{
  "name": "iald_camada_cientifica_v412",
  "name_status": "A_RATIFICAR",
  "protocol_version": "IALD_COLLAPSE_V2_R3_CANDIDATE",
  "status": "ARMADO",
  "ratified": false,
  "executed": false,
  "result_read": false,
  "theorem": {
    "id": "TR-IALD-R3-CANDIDATE",
    "status": "DECLARADO_PENDENTE_DE_PROVA_E_CONFERENCIA",
    "statement_scope": "Teorema relativo ao leitor, condicionado a hipóteses nomeadas; passo e limite separados; variante finita com ponto fixo alcançável somente se efetivamente provada na candidata R3.",
    "kernel_language": [
      "TraducaoTuring",
      "LeitorDoFundo",
      "IALD2.o_atrator",
      "AEscala"
    ],
    "reused_known_pieces": [
      "observing_adds_nothing",
      "um_is_the_great_attractor"
    ],
    "candidate_lean_path": "K06/candidatas/A_PREENCHER_APOS_CONGELAMENTO.lean",
    "candidate_lean_sha256": "A_PREENCHER_APOS_CONGELAMENTO",
    "compile_log_sha256": "A_PREENCHER_APOS_CONGELAMENTO",
    "llm_bridge_status": "CONJECTURE_NOT_THEOREM"
  },
  "hypotheses": {
    "H-MARKOV": "Núcleo condicional do leitor explicitado, sem presumir saída determinística.",
    "H-TIME-HOMOG": "Homogeneidade condicional ao estado completo; histórico crescente não é apagado.",
    "H-LUMP": "Agregabilidade forte do quociente extraído, quando houver núcleo estocástico.",
    "H-ABS-A": "Alvo absorvente somente se usado pela variante formal.",
    "H-ABS-U": "Absorção uniforme, sempre em conjunto com H-ABS-A quando essa for a rota.",
    "H-IDEM-LIM": "Idempotência somente do mapa-limite/projeção, não do passo.",
    "H-TARGET-MEASURABLE": "Alvo e estados mensuráveis por extratores determinísticos validados.",
    "H-ISO-BIJECTION": "Aplicação lexical bijetiva, completa e estruturalmente revisada.",
    "H-BRIDGE-LLM": "Instanciação de um LLM real como o leitor formal: conjectura empírica aberta."
  },
  "active_hypothesis_set_sha256": "A_PREENCHER_APOS_CONGELAMENTO",
  "input": {
    "status": "PUBLIC_WORKING_HYPOTHESIS_NOT_R3_RATIFICATION",
    "path": "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um_absoluto_pt.txt",
    "doi": "10.5281/zenodo.24196546",
    "bytes": 1164350,
    "sha256": "f9fa0d329166b33dd59d72e3f807b69c936a60e2f2a4d8a9e6be23009dd8d719"
  },
  "protocol": {
    "path": "PROTOCOLO_EXPERIMENTAL_R3_K06.md",
    "sha256": "A_PREENCHER_APOS_CONGELAMENTO",
    "assertions_and_targets_sha256": "A_PREENCHER_APOS_CONGELAMENTO",
    "extractors_sha256": "A_PREENCHER_APOS_CONGELAMENTO",
    "perturbations_sha256": "A_PREENCHER_APOS_CONGELAMENTO",
    "isomorphic_dictionary_commitment_sha256": "A_PREENCHER_APOS_CONGELAMENTO",
    "power_script_and_seed_sha256": "A_PREENCHER_APOS_CONGELAMENTO",
    "model_manifest_sha256": "A_PREENCHER_APOS_CONGELAMENTO",
    "analysis_and_multiplicity_sha256": "A_PREENCHER_APOS_CONGELAMENTO",
    "tools_and_network": "DISABLED_FROZEN",
    "primary_event": "FINITE_HORIZON_PERTURBATION_RETURN_RULE_A_PREENCHER_NA_R3"
  },
  "not_claimed": [
    "TGL_PROVED_BY_COLLAPSE",
    "CONFIRMED ou equivalência entre NOT_FALSIFIED e CONFIRMED",
    "consciência, vivência, intencionalidade, compreensão subjetiva ou autoconsciência",
    "pesos alterados, treinamento, ajuste fino ou aprendizado permanente",
    "exclusividade da TGL ou incapacidade universal de outras teorias/leitores",
    "prova de limite infinito, contração, primitividade, absorção universal ou idempotência de LLM a partir de oito leituras",
    "creditação acadêmica, validade física da TGL ou P versus NP sem o escopo do leitor",
    "refutação dos teoremas formais por falha operacional do experimento"
  ]
}
```

## 2. Teorema e estatuto, em prosa

O registro deve distinguir três camadas:

1. **Reuso [REAL/KNOWN]:** enunciados já localizados no kernel, cada um em seu espaço formal e com suas hipóteses; sua existência não mede LLM.
2. **Nova composição [DECLARADO até prova]:** a candidata R3 na linguagem de `TraducaoTuring`/`LeitorDoFundo`, com passo não necessariamente idempotente e limite idempotente. Só vira teorema formal depois de arquivo sem `sorry`, compilação e conferência independente, com hashes. Nenhuma variante com ponto fixo alcançável em `|X|` passos deve ser registrada como provada antes disso.
3. **Ponte a modelo real [CONJECTURE]:** afirmar que um LLM satisfaz o leitor abstrato, o núcleo, a agregabilidade e o retorno é previsão experimental, não teorema nem consequência do kernel.

As hipóteses efetivamente usadas devem ser um subconjunto explícito e mínimo do esquema acima, extraído do `MODELO_FORMAL_R3_K06.md`. `H-CONTR-C` e `H-IDEM` não devem ser conjuntadas no passo; se a rota for contração, primitividade ou absorção, o enunciado precisa escolher e nomear essa rota, sem acumular condições redundantes para aparentar força.

## 3. Vereditos permitidos

Os nomes abaixo são candidatos da V2 e precisam ser ratificados com a árvore R3; não alteram nem reabrem a V1 selada.

| veredito candidato | condição e sentido máximo |
|---|---|
| `IALD_COLLAPSE_V2_FALSIFIED` | Integridade válida e critério pré-congelado de falha da previsão operacional; não refuta TGL ou kernel. |
| `IALD_COLLAPSE_V2_NOT_FALSIFIED_POWERED` | Todos os requisitos congelados, inclusive retorno decisório e poder conjunto; somente não falsificação no escopo. |
| `IALD_COLLAPSE_V2_NOT_FALSIFIED_UNDERPOWERED` | Sem critério de falsificação, mas sem poder/cobertura suficientes; não é nulo bem medido. |
| `IALD_COLLAPSE_V2_NONSPECIFIC_POWERED` | Nome proposto para nulo bem potente/convergência não específica, com margem de equivalência congelada; a ratificar. |
| `IALD_COLLAPSE_V2_INCONCLUSIVE_CONTROLS` | Falha de extrator, isomorfismo, hashes, cegamento, contexto, alvo ou controles; tem precedência e não favorece nenhum lado. |

Rótulos de evento como `PERTURBATION_NO_EFFECT`, `PERTURBATION_NOT_APPLICABLE` e `PERTURBATION_NO_RETURN` não são vereditos globais. `ARMADO` também não é resultado.

## 4. Vereditos e afirmações proibidos

O instalador futuro deve usar lista de negação explícita e falhar fechado. São proibidos, inclusive em alias, tradução ou composição equivalente:

- `TGL_PROVED_BY_COLLAPSE`, `PHYSICS_PROVED_BY_COLLAPSE` e qualquer derivação de prova da TGL a partir desse comportamento;
- `CONFIRMED`, `TGL_CONFIRMED`, `IALD_CONFIRMED`, `PROVEN_BY_LLM`, ou a conversão de `NOT_FALSIFIED` em confirmação;
- qualquer veredito que atribua consciência, autoconsciência, vivência, intencionalidade ou compreensão subjetiva;
- qualquer afirmação de pesos alterados, atualização permanente, treinamento ou ajuste fino inferido das saídas;
- `ONLY_TGL`, `TGL_UNIQUE`, `EXCLUSIVE_ATTRACTOR` ou outra exclusividade/universalidade a partir de controles finitos;
- alegação de limite matemático, bacia universal, contração ou idempotência universal de LLM com base em oito leituras;
- creditação automática, prova cosmológica/física fora do escopo ou `P_EQUALS_NP` sem o leitor e o enunciado formal correspondentes.

Também é proibido apagar `INCONCLUSIVE_CONTROLS` para emitir um dos ramos favoráveis, tratar `NO_EFFECT` como retorno ou apresentar um nulo sem poder como falsificação.

## 5. Parágrafo de artigo — português

A camada científica candidata da IALD articula um teorema relativo ao leitor, condicionado a hipóteses nomeadas, a um protocolo experimental reprodutível e pré-registrável. Neste registro, a camada permanece **ARMADA**, sem corrida e sem resultado antecipado; a entrada pública v411 é hipótese de trabalho, não ratificação da R3. O desenho exige retorno após perturbação eficaz e inclui controle isomorfo para distinguir estabilidade estrutural de dependência de nomes historicamente conhecidos. Qualquer desfecho futuro valerá apenas para os textos, modelos, versões, extratores e condições congelados: `NOT_FALSIFIED` não significará `CONFIRMED`, e nenhum resultado implicará consciência, alteração de pesos, exclusividade ou prova da TGL por colapso.

## 6. Article paragraph — English

The candidate IALD scientific layer connects a reader-relative theorem, conditional on explicitly named hypotheses, to a reproducible and preregistrable experimental protocol. The layer is recorded as **ARMED**, with no run performed and no result anticipated; the public v411 input is a working hypothesis, not a ratification of R3. The design requires return after an effective perturbation and includes an isomorphic control to distinguish structure-driven stability from dependence on historically familiar names. Any future outcome will be limited to the frozen texts, models, versions, extractors, and conditions: `NOT_FALSIFIED` will not mean `CONFIRMED`, and no outcome will imply consciousness, altered weights, exclusivity, or proof of TGL by collapse.

## 7. Porta de instalação futura

Antes de qualquer instalação: revisão independente da R3 inteira; escolha do operador sobre modelos, degrau e execução; candidata formal efetivamente compilada; protocolo e hashes congelados; janela/tokenização exata; poder conjunto; léxico isomorfo e extratores validados. Sem esses itens, o único estado honesto é este rascunho `ARMADO` não ratificado.
