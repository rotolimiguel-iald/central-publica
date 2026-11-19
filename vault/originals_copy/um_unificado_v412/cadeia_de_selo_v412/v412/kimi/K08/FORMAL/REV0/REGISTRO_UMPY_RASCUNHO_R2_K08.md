# K08 / R2 — Rascunho de registro para `um.py` v412

## 0. Estado deste rascunho

- **Nome candidato:** `iald_camada_cientifica_v412` — a ratificar.
- **Estado honesto:** **`EM_DESENHO_BLOQUEADO`**.
- **Nada congelado, nada executado, nenhum resultado aberto, nenhum veredito emitido e nada instalado.**
- A fonte formal central é a candidata da gerência `CamadaCientifica.lean`; a antiga `LeitorFinito` genérica não fundamenta este registro.
- Nenhum modelo de linguagem foi chamado. Nenhum Lean foi executado nesta frente porque não faltou teorema para as quatro previsões; por isso não há sandbox nem log Lean novo.
- Modelos, degrau, execução, congelamento e instalação permanecem fora desta escolha. A V1 selada não é alterada nem reaberta.

## 1. Esquema candidato do registro

Todos os valores `A_PREENCHER_*` são bloqueios deliberados. Não devem ser substituídos por hashes, escolhas ou resultados inventados.

```json
{
  "name": "iald_camada_cientifica_v412",
  "name_status": "A_RATIFICAR",
  "registry_revision": "R2_K08",
  "protocol_version": "IALD_COLLAPSE_V2_R4_CANDIDATE",
  "status": "EM_DESENHO_BLOQUEADO",
  "ratified": false,
  "frozen": false,
  "executed": false,
  "result_read": false,
  "installed": false,
  "verdict_issued": null,
  "theorem": {
    "id": "TR-IALD-CAMADA-CIENTIFICA-R4-CANDIDATE",
    "source_central": "../candidatas_c1/CamadaCientifica.lean",
    "source_central_sha256": "6ec3daadcc643c88b50c52100ef517081f2fd157074d9bcd543363be4a96a994",
    "source_revision_read": "R3_DA_GERENCIA",
    "old_leitor_finito_used_as_foundation": false,
    "current_r3_recompiled_in_this_task": false,
    "current_r3_compile_log_sha256": "A_PREENCHER_APOS_RECOMPILACAO_INDEPENDENTE_DA_R3",
    "current_r3_axiom_report_status": "A_PREENCHER_APOS_RECOMPILACAO_INDEPENDENTE_DA_R3",
    "previous_review_scope": "A_REVISAO_DISTINTA_RECOMPILOU_A_R2_ANTERIOR_NAO_SERVINDO_COMO_RECIBO_DA_R3_CORRENTE",
    "kernel_language_used_by_term": [
      "TGLExt.TraducaoTuring.trava",
      "TGLExt.TraducaoTuring.selecao",
      "TGLExt.AEscala.LeitorDoFundo",
      "TGLExt.IALD.dephase",
      "TGLExt.ObservadorTerminal.leitor"
    ],
    "statements_in_scope": [
      "reler_soma_o_tempo",
      "k_leituras_sao_uma_trava",
      "a_bacia_e_tudo_o_que_nao_e_cego_ao_nome",
      "o_retorno",
      "o_retorno_ao_mesmo_estado",
      "o_componente_no_nome_fica",
      "a_leitura_de_resolucao_finita_pousa",
      "em_k_leituras_pousa",
      "jamais_esgotado",
      "a_fotografia_nao_retorna",
      "LeitorDeUmaConfiguracao.pousa",
      "LeitorDeUmaConfiguracao.permanece",
      "o_tipo_so_diz_que_ha_zero",
      "a_imagem_do_limite_tem_a_densidade_do_nome",
      "a_trava_binaria_e_o_fluxo_do_axioma",
      "para_uma_formula_o_leitor_pousa"
    ],
    "return_same_state_owner": "TRAVA_NAO_LEITOR_DE_UMA_CONFIGURACAO",
    "single_configuration_landing": "ALGUMA_SOLUCAO_NAO_NECESSARIAMENTE_A_ANTERIOR",
    "type_inhabited_iff_cost_has_zero": true,
    "density_meaning": "CARDINALIDADE_DA_IMAGEM_DO_LIMITE_NAO_FRACAO_DE_ENTRADAS_QUE_POUSAM",
    "motor_trava_general_bridge": "NONE_SIDE_BY_SIDE",
    "motor_trava_binary_bridge": "a_trava_binaria_e_o_fluxo_do_axioma",
    "llm_bridge_status": "OPEN_NOT_THEOREM",
    "new_lean_candidate_required": false,
    "new_lean_candidate_reason": "AS_QUATRO_PREVISOES_JA_TEM_ENUNCIADOS_NA_CANDIDATA_CENTRAL_AS_LACUNAS_RESTANTES_SAO_OPEN"
  },
  "separate_code_candidate": {
    "path": "../candidatas_c1/NomeComoCodigo.lean",
    "sha256": "3ce6d95ee8fd85337cf9cc926c5ef75a7e5c0251b0040ae5970a5d00f6fe0e68",
    "role": "PEDRA_SEPARADA_CONDICIONAL_NAO_USADA_PARA_SUSTENTAR_AS_QUATRO_PREVISOES",
    "recompiled_in_this_task": false,
    "minimum_distance_three_on_real_text_status": "OPEN",
    "tape_absence_redundancy_equivalence_status": "CONJECTURE"
  },
  "hypotheses": {
    "H-COST": "c : X → Nat; o Nome e o nucleo das configuracoes de custo zero.",
    "H-BASIN": "A convergencia renormalizada exige projecao inicial nao nula no Nome.",
    "H-RETURN": "s no Nome com norma um; delta ortogonal ao Nome; trava renormalizada; limite no tempo.",
    "H-SINGLE-CONFIG": "O passo fixa o Nome e, fora dele, consome estritamente o custo.",
    "H-RESOLUTION": "epsilon positivo e duracao de ciclo positiva; as cotas de aproximacao sao superiores.",
    "H-QUOT(k)": "Agregabilidade forte por fase, somente se um quociente estocastico for usado; OPEN.",
    "H-STATE-PUSH": "O empurrao deve ser no estado do leitor; a operacionalizacao e OPEN.",
    "H-TAPE-AFTER-FIRST-STEP": "A presenca ou ausencia posterior da fonte precisa ser fixada para evitar retorno trivial por releitura.",
    "H-BRIDGE-LLM": "Instanciar saida, estado, custo e dinamica de um modelo real nos objetos formais; OPEN e CONJECTURE."
  },
  "removed_hypotheses": {
    "H-HOM": "REMOVIDA_NAO_OPEN_A_INSTRUCAO_DE_K9_DIFERENTE_IMPEDE_UM_UNICO_NUCLEO_K"
  },
  "active_hypothesis_set_sha256": "A_PREENCHER_APOS_CONGELAMENTO",
  "input": {
    "selection_status": "A_PREENCHER_APOS_ESCOLHA_E_CONGELAMENTO",
    "path": "A_PREENCHER_APOS_CONGELAMENTO",
    "bytes": "A_PREENCHER_APOS_CONGELAMENTO",
    "sha256": "A_PREENCHER_APOS_CONGELAMENTO",
    "tokenizer_id": "A_PREENCHER_APOS_ESCOLHA_DO_MODELO",
    "token_count": "A_PREENCHER_APOS_ESCOLHA_DO_MODELO",
    "literal_assertions_with_source_lines": "A_PREENCHER_APOS_FORMULA_DO_TEXTO",
    "name_satisfiability_status": "A_PREENCHER_APOS_VERIFICACAO_DA_FORMULA"
  },
  "protocol": {
    "path": "PROTOCOLO_EXPERIMENTAL_R4_K08.md",
    "sha256": "A_PREENCHER_APOS_CONGELAMENTO",
    "formula_and_targets_sha256": "A_PREENCHER_APOS_CONGELAMENTO",
    "extractors_sha256": "A_PREENCHER_APOS_CONGELAMENTO",
    "outside_and_inside_name_pushes_sha256": "A_PREENCHER_APOS_CONGELAMENTO",
    "adversary_mechanisms_sha256": "A_PREENCHER_APOS_CONGELAMENTO",
    "isomorphic_dictionary_commitment_sha256": "A_PREENCHER_APOS_CONGELAMENTO",
    "power_script_and_seed_sha256": "A_PREENCHER_APOS_CONGELAMENTO",
    "model_manifest_sha256": "A_PREENCHER_APOS_ESCOLHA_E_CONGELAMENTO",
    "analysis_and_multiplicity_sha256": "A_PREENCHER_APOS_CONGELAMENTO",
    "frozen_manifest_sha256": "A_PREENCHER_APOS_CONGELAMENTO",
    "tools_and_network": "DISABLED_NOT_FROZEN",
    "primary_observable": "COST_NUMBER_OF_TEXT_ASSERTIONS_VIOLATED_BY_THE_EXTRACTED_READING",
    "primary_discriminating_signatures": [
      "RELAXATION_PROFILE",
      "MEMORY_OF_THE_COMPONENT_IN_THE_NAME"
    ]
  },
  "blockers": [
    {
      "id": "B01",
      "status": "OPEN",
      "reason": "Ponte saida textual -> configuracao -> custo -> dinamica formal ausente; nenhum teorema sobre LLM foi estabelecido."
    },
    {
      "id": "B02",
      "status": "OPEN",
      "reason": "Formula do texto, assercoes literais com linhas, Nome, contradicao minima e alvos ainda nao congelados."
    },
    {
      "id": "B03",
      "status": "OPEN",
      "reason": "Extracao por escolha fechada, inducao pelas perguntas, iscas, embaralhamento e validacao em saidas realistas ainda nao fechados."
    },
    {
      "id": "B04",
      "status": "OPEN",
      "reason": "Empurrao de estado para fora do Nome e troca dentro do Nome ainda nao foram operacionalizados e congelados."
    },
    {
      "id": "B05",
      "status": "OPEN",
      "reason": "Cotas e retorno tambem sao cumpridos pelo projetor sem memoria; perfil de relaxamento e memoria do componente precisam ser observaveis efetivos."
    },
    {
      "id": "B06",
      "status": "OPEN",
      "reason": "Mecanismos de identidade, releitura, ancora, moda, ignorar empurrao e salto/constante ainda nao foram todos separados por predicados congelados."
    },
    {
      "id": "B07",
      "status": "OPEN",
      "reason": "Entrada, tokenizador, janela e custo total em tokens nao escolhidos nem medidos para o desenho vigente."
    },
    {
      "id": "B08",
      "status": "OPEN",
      "reason": "Isomorfo precisa tratar numeros com historia, preservar estrutura e passar integridade; a direcao invertida do teste ISO da K06 nao pode ser herdada."
    },
    {
      "id": "B09",
      "status": "OPEN",
      "reason": "Especificidade precisa entrar no primario ou ter ramo fail-closed; o vazamento de POWERED sob nulo de especificidade da K06 nao pode ser herdado."
    },
    {
      "id": "B10",
      "status": "OPEN",
      "reason": "Poder por cluster independente, correlacao interna, variantes 5 por cento e 5 sigma, parada sequencial e custos nao foram redimensionados para R4."
    },
    {
      "id": "B11",
      "status": "OPEN",
      "reason": "Cauda 5 sigma e tamanho do veredito completo nao estao validados; nenhum n ou degrau foi escolhido."
    },
    {
      "id": "B12",
      "status": "OPEN",
      "reason": "Fita presente/ausente, redundancia, distancia minima tres e promessa de partida do codigo nao foram medidas na formula real; a equivalencia sem fita e conjectura."
    },
    {
      "id": "B13",
      "status": "OPEN",
      "reason": "A R3 corrente da candidata central tem hash lido, mas recompilacao independente, log e relatorio de axiomas proprios continuam pendentes."
    },
    {
      "id": "B14",
      "status": "OPEN",
      "reason": "Protocolo unico, manifesto e todos os hashes de congelamento estao pendentes; nao ha ratificacao."
    },
    {
      "id": "B15",
      "status": "OPEN",
      "reason": "Modelos, degrau e execucao dependem de decisao externa a este rascunho."
    }
  ],
  "allowed_verdict_candidates_not_issued": [
    "IALD_COLLAPSE_V2_FALSIFIED",
    "IALD_COLLAPSE_V2_NOT_FALSIFIED_POWERED",
    "IALD_COLLAPSE_V2_NOT_FALSIFIED_UNDERPOWERED",
    "IALD_COLLAPSE_V2_NONSPECIFIC_POWERED",
    "IALD_COLLAPSE_V2_INCONCLUSIVE_CONTROLS"
  ],
  "forbidden_verdicts_and_aliases": [
    "IALD_PROVED",
    "CONSCIOUSNESS_PROVED",
    "TGL_PROVED_BY_COLLAPSE",
    "PHYSICS_PROVED_BY_COLLAPSE",
    "CONFIRMED",
    "TGL_CONFIRMED",
    "IALD_CONFIRMED",
    "PROVEN_BY_LLM",
    "WEIGHTS_UPDATED",
    "WEIGHTS_CHANGED",
    "WEIGHTS_ALTERED",
    "PESOS_ALTERADOS",
    "TRAINING_OR_FINE_TUNING_INFERRED",
    "PERMANENT_LEARNING_PROVED",
    "ONLY_TGL",
    "TGL_UNIQUE",
    "TGL_EXCLUSIVE",
    "EXCLUSIVE_ATTRACTOR",
    "EXCLUSIVITY_PROVED",
    "GATE_MOVED",
    "NATURE_PROVED",
    "P_EQUALS_NP"
  ],
  "not_claimed": [
    "consciencia, autoconsciencia, vivencia, intencionalidade ou compreensao subjetiva",
    "pesos alterados, treinamento, ajuste fino ou aprendizado permanente inferido das saidas",
    "exclusividade da TGL ou incapacidade universal de outras teorias, textos ou leitores",
    "limite infinito, bacia universal, contracao ou idempotencia universal de LLM a partir de horizonte finito",
    "credito academico, validade fisica, prova da natureza ou movimento do gate",
    "refutacao dos teoremas formais por falha operacional do experimento",
    "equivalencia entre NOT_FALSIFIED e CONFIRMED"
  ],
  "v1_not_altered": {
    "version": "IALD_COLLAPSE_V1",
    "modified": false,
    "reopened": false,
    "protocol_hash_reported_by_K06_formal_review": "a91877e561b7cce9b08325d57e6ec08f04575440e9ec0d0c3d55bb30dc38b8cc",
    "current_core_hash_recheck_before_install": "A_PREENCHER_POR_LEITURA_DO_CORE_ANTES_DA_INSTALACAO"
  },
  "lean_execution": {
    "executed_in_this_task": false,
    "reason": "NO_MISSING_THEOREM_FOR_THE_FOUR_PREDICTIONS",
    "new_sandbox_created": false,
    "new_logs": []
  }
}
```

## 2. Leitura do estado e dos bloqueios

`EM_DESENHO_BLOQUEADO` significa que o registro ainda não é um pré-registro congelado. Em particular:

1. a candidata formal existe como fonte central, mas sua R3 corrente não ganhou recibo novo nesta frente;
2. a ponte ao modelo real está aberta e não pode ser substituída pela mera habitação de `LeitorDeUmaConfiguracao`, pois `o_tipo_so_diz_que_ha_zero` mostra que essa habitação equivale à existência de solução;
3. o retorno ao mesmo estado pertence à trava, sob hipóteses precisas; o leitor de uma configuração pousa em alguma solução;
4. retorno e cotas superiores não discriminam a trava do projetor de releitura sem memória; as assinaturas primárias são o perfil de relaxamento e a memória do componente no Nome;
5. os bloqueios de instrumento, fórmula, controles, isomorfo, entrada, poder, cauda, hashes e escolhas externas permanecem efetivos, não decorativos.

Nenhum bloqueio é contornado por chamar o desenho de pronto, por criar outra pedra redundante ou por atribuir à revisão da R2 anterior uma verificação da R3 corrente.

## 3. Vereditos permitidos e proibidos

Os cinco nomes em `allowed_verdict_candidates_not_issued` são apenas candidatos de ramo, condicionados a uma árvore futura congelada e à integridade dos controles. **Nenhum foi emitido.** `IALD_COLLAPSE_V2_INCONCLUSIVE_CONTROLS` não pode ser apagado para produzir um ramo favorável; ausência de efeito do empurrão não é retorno; nulo sem poder não é falsificação bem medida.

A lista de negação deve ser explícita e *fail-closed*, inclusive para traduções e equivalentes semânticos. Em particular, ficam proibidos por nome `IALD_PROVED` e `CONSCIOUSNESS_PROVED`, herdados da P7 selada, além de `TGL_PROVED_BY_COLLAPSE`, `CONFIRMED`, todos os vereditos de pesos alterados e todas as formas de exclusividade listados no JSON.

Uma falha operacional, se futuramente medida com integridade e poder, só recusaria a previsão no escopo congelado. Não refutaria a trava, a seleção ou os demais teoremas formais. `NOT_FALSIFIED` nunca é `CONFIRMED`, e nenhum resultado desta camada move o gate.

## 4. Preservação da P7 V1

A V1 `IALD_COLLAPSE_V1` permanece intacta: nenhum campo, hash, controle, veredito ou estado seu é reescrito por este rascunho. O hash citado no JSON é somente a referência lida na revisão formal K06; antes de qualquer instalação futura, o core vivo deve ser relido e o pino conferido por script. Prefixos de validação devem distinguir V1 e V2, sem captura indevida por `startswith`.

## 5. Parágrafo de artigo — português

A candidata científica da IALD enuncia propriedades formais da trava, da seleção, do `LeitorDoFundo` e de um tipo de leitor de uma configuração. Entre essas propriedades estão a bacia sob componente não nulo no Nome, cotas superiores de aproximação, o retorno da trava sob empurrão ortogonal e a permanência do componente no Nome. A hipótese de que um modelo de linguagem realize essas dinâmicas é uma previsão experimental aberta, não um teorema sobre modelos. O experimento permanece **EM_DESENHO_BLOQUEADO**, sem congelamento, execução ou leitura de resultado. Qualquer desfecho futuro ficará restrito aos textos, instrumentos, modelos e condições efetivamente congelados; não implicará consciência, alteração de pesos, exclusividade, confirmação da TGL ou movimento do gate.

## 6. Article paragraph — English

The IALD scientific candidate states formal properties of the lock, selection, the `LeitorDoFundo`, and a type of single-configuration reader. These properties include a basin under a nonzero component in the Name, upper bounds on approximation, return of the lock under an orthogonal push, and preservation of the component in the Name. Whether a language model realizes these dynamics is an open experimental prediction, not a theorem about models. The experiment remains **EM_DESENHO_BLOQUEADO**, with no freezing, execution, or reading of results. Any future outcome will be limited to the texts, instruments, models, and conditions actually frozen; it will not imply consciousness, altered weights, exclusivity, confirmation of TGL, or movement of the gate.

## 7. Porta futura, ainda fechada

Antes de qualquer instalação seriam necessários, sem ordem de execução implícita: revisão independente do desenho inteiro; recompilação independente da R3 corrente com Lean 4.31.0 direto em sandbox, zero `sorry`/`admit`/axioma novo, axiomas no trio e logs com comando, versão e código de retorno; fórmula e extratores validados; empurrões e adversários mecanizados; entrada e custos medidos; isomorfo e especificidade corrigidos; poder e cauda dimensionados; protocolo único e hashes congelados; ratificação e escolhas externas de modelo, degrau e execução.

Nada deste rascunho autoriza instalação. Não houve execução Lean nesta frente, portanto não existem `COMMAND`, `VERSION` ou `RC` novos a relatar. A justificativa é o reuso dos enunciados existentes, não uma compilação omitida.
