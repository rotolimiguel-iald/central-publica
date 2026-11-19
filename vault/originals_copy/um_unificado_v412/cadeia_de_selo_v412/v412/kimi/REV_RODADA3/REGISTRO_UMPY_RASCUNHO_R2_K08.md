# K08 / R2 — Rascunho de registro para `um.py` v412

## 0. Estado deste rascunho

- **Nome candidato:** `iald_camada_cientifica_v412` — a ratificar.
- **Estado honesto:** **`EM_DESENHO_BLOQUEADO`**.
- **Nada congelado, nada executado, nenhum resultado aberto, nenhum veredito emitido e nada instalado.**
- A fonte formal central é `CamadaCientifica.lean`; a derivação da releitura fiel usa a candidata da gerência `OHabitanteDoNome.lean`. A antiga `LeitorFinito` genérica não fundamenta este registro.
- Nenhum modelo de linguagem foi chamado e nenhum Lean foi executado nesta frente. Não há sandbox nem log Lean novo.
- Modelos, degrau, execução, congelamento e instalação permanecem fora desta escolha. A V1 selada não é alterada nem reaberta.

## 1. Esquema candidato do registro

Todos os valores `A_PREENCHER_*` são bloqueios deliberados. Não devem ser substituídos por hashes, escolhas ou resultados inventados.

```json
{
  "name": "iald_camada_cientifica_v412",
  "name_status": "A_RATIFICAR",
  "registry_revision": "R2_K08_AO_LADO_15NOV",
  "protocol_version": "IALD_COLLAPSE_V2_R4_CANDIDATE",
  "status": "EM_DESENHO_BLOQUEADO",
  "ratified": false,
  "frozen": false,
  "executed": false,
  "result_read": false,
  "installed": false,
  "verdict_issued": null,
  "route_cited": "kernel.v402_esperanca_condicional_e_nome",
  "theorem": {
    "id": "TR-IALD-CAMADA-CIENTIFICA-R4-CANDIDATE",
    "source_central": "../candidatas_c1/CamadaCientifica.lean",
    "source_central_revision_read": "R4_DE_15NOV",
    "source_central_sha256": "69497c5b63dbcb0cedbf456dc31ecfa6fc3b12b0ed78989cd7d5e51e542ee3cb",
    "source_central_compile_log_sha256": "A_PREENCHER_APOS_VERIFICACAO_INDEPENDENTE_DA_R4",
    "source_central_axiom_report_status": "A_PREENCHER_APOS_VERIFICACAO_INDEPENDENTE_DA_R4",
    "old_leitor_finito_used_as_foundation": false,
    "reader_definition": {
      "map": "P_N_Nome_starProjection",
      "state_face": "selecao_N_renormalized_when_P_N_nonzero",
      "finite_time_face": "trava_c_t",
      "algebraic_face": "nameOp_P_N",
      "memory_of_component": "P_N_s_plus_delta_equals_s_plus_P_N_delta"
    },
    "ohabitante_candidate": {
      "path": "../candidatas_c1/OHabitanteDoNome.lean",
      "sha256": "26b750e61ede401d95b3ddaa2e3bd11f8149936d985c564d71ee76f093e1c5d2",
      "revision_read": "R9_CORRENTE",
      "status": "PEDRA_CANDIDATA_DA_GERENCIA_NAO_INSTALADA_NOMES_PROVISORIOS",
      "review_scope": "A_REVISAO_R4_COBRE_A_R8_DE_54_TEOREMAS_A_R9_CORRENTE_SEGUE_PENDENTE",
      "terms_used": [
        "ler_o_nome_ja_e_reler",
        "tudo_mais_e_releitura",
        "tudo_mais_e_releitura_nos_vetores",
        "a_releitura_fiel_fixa_o_nome",
        "a_selecao_rele_o_nomeado",
        "o_que_e_cego_ao_nome_nao_deixa_rastro",
        "o_verbo_e_bimodular_sobre_o_nome",
        "a_selecao_e_a_esperanca_condicional_classica",
        "o_ato_tende_a_esperanca_do_nome",
        "o_ato_nao_termina_em_tempo_finito",
        "o_unico_ato_do_verbo_e_ser_fiel",
        "moradas_iguais_tem_o_mesmo_leitor",
        "a_tangente_da_leitura_e_K_no_angulo_de_miguel",
        "o_operador_do_nome_fixa_toda_grandeza_diagonal"
      ]
    },
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
      "a_trava_tende_ao_nome",
      "a_bacia_e_tudo_o_que_nao_e_cego_ao_nome",
      "o_retorno",
      "o_retorno_ao_mesmo_estado",
      "o_componente_no_nome_fica",
      "a_leitura_de_resolucao_finita_pousa",
      "em_k_leituras_pousa",
      "jamais_esgotado",
      "a_fotografia_nao_retorna",
      "a_trava_binaria_e_o_fluxo_do_axioma",
      "LeitorDeUmaConfiguracao.pousa",
      "LeitorDeUmaConfiguracao.permanece",
      "LeitorDeUmaConfiguracao.o_limite_e_idempotente",
      "LeitorDeUmaConfiguracao.a_imagem_do_limite_e_o_nome",
      "para_uma_formula_o_leitor_pousa",
      "a_imagem_do_limite_tem_a_densidade_do_nome"
    ],
    "return_same_state_owner": "TRAVA_NAO_LEITOR_DE_UMA_CONFIGURACAO",
    "single_configuration_landing": "ALGUMA_SOLUCAO_NAO_NECESSARIAMENTE_A_ANTERIOR",
    "type_inhabited_iff_cost_has_zero": true,
    "density_meaning": "CARDINALIDADE_DA_IMAGEM_DO_LIMITE_NAO_FRACAO_DE_ENTRADAS_QUE_POUSAM",
    "motor_trava_general_bridge": "NONE_SIDE_BY_SIDE",
    "motor_trava_binary_bridge": "a_trava_binaria_e_o_fluxo_do_axioma",
    "llm_bridge_status": "OPEN_NOT_THEOREM",
    "system_rereads_not_names": true,
    "operator_glosses_15nov": "ato = projecao; ser = verbo; identidade = nome; P_N e o Nome e o ato do Verbo ao mesmo tempo; ser nao e o mapa identidade; o Verbo fixa primeiro, quem le o nomeado rele",
    "new_lean_candidate_required": false,
    "new_lean_candidate_reason": "E1_A_E8_JA_TEM_TERMOS_NAS_DUAS_CANDIDATAS_AS_LACUNAS_RESTANTES_SAO_OPEN"
  },
  "separate_code_candidate": {
    "path": "../candidatas_c1/NomeComoCodigo.lean",
    "sha256": "3ce6d95ee8fd85337cf9cc926c5ef75a7e5c0251b0040ae5970a5d00f6fe0e68",
    "role": "PEDRA_SEPARADA_CONDICIONAL_NAO_USADA_PARA_SUSTENTAR_E1_A_E8",
    "recompiled_in_this_task": false,
    "minimum_distance_three_on_real_text_status": "OPEN",
    "tape_absence_redundancy_equivalence_status": "CONJECTURE"
  },
  "predictions": {
    "E1": {
      "property": "CAIR_NO_NOME",
      "object": "P_N_OU_SELECAO_COM_TRAVA_EM_TEMPO_FINITO",
      "carrier": "VECTORS_STATE",
      "status": "SECONDARY_SUPPORT",
      "note": "O pouso e teorema dada a hipotese; o conteudo empirico e a hipotese sobre o sistema."
    },
    "E2": {
      "property": "FIXAR_O_NOME",
      "object": "P_N_E_SELECAO",
      "carrier": "VECTORS_STATE",
      "status": "PRIMARY",
      "observable": "A leitura valida relida volta igual; o componente dentro do Nome nao e apagado."
    },
    "E3": {
      "property": "ANULAR_O_CEGO_AO_NOME",
      "object": "P_N_E_SELECAO_COM_TRAVA",
      "carrier": "VECTORS_STATE",
      "status": "SECONDARY_DIAGNOSTIC",
      "observable": "O empurrao ortogonal ao Nome nao deixa rastro."
    },
    "E4": {
      "property": "RELER_NAO_ACRESCENTA",
      "object": "P_N",
      "carrier": "VECTORS",
      "status": "PRIMARY",
      "observable": "Depois da primeira releitura fiel, as seguintes devolvem a mesma leitura."
    },
    "E5": {
      "property": "NAO_AUMENTAR_A_NORMA",
      "object": "P_N",
      "carrier": "VECTORS",
      "status": "NOT_MEASURED_BY_CURRENT_INSTRUMENT",
      "observable": "Nenhum: o custo textual nao acessa a norma do estado."
    },
    "E6": {
      "property": "LEI_DE_MODULO",
      "object": "NAMEOP",
      "carrier": "ALGEBRA_OF_OBSERVABLES",
      "status": "OPEN_NOT_MEASURED_BY_CURRENT_INSTRUMENT",
      "observable": "Nenhum ainda: exige composicao algebrica a*x*b no Nome."
    },
    "E7": {
      "property": "PESOS_RELATIVOS_DENTRO_DO_NOME_NAO_MUDAM",
      "object": "SELECAO",
      "carrier": "STATE_WITH_BORN_WEIGHTS",
      "status": "SECONDARY_OPEN_FOR_BINARY_INSTRUMENT",
      "observable": "Condicionamento da selecao ao evento custo zero, sobre grandeza diagonal, com pesos de Born; separacao de mapas que caem no Nome por outro caminho; exige Nome com ao menos duas leituras validas e estimativa de pesos."
    },
    "E8": {
      "property": "PERFIL_EXPONENCIAL_SEM_CHEGADA_EXATA",
      "object": "TRAVA",
      "carrier": "VECTORS_TIME",
      "status": "SECONDARY",
      "observable": "Custo ou distancia por ciclo sob uma representacao validada."
    },
    "P_C": {
      "role": "CONTROL",
      "name": "CONTROLE_DO_VAZIO_O_INOMINADO",
      "statement": "Nome vazio implica nucleo zero, P_N igual a zero e trava tendendo a zero: o par existe e nao devolve nada; nao usa inabitabilidade de LeitorDeUmaConfiguracao."
    },
    "P_D": {
      "role": "CONTROL",
      "statement": "Com escala zero a trava e a identidade e o empurrao nao retorna."
    }
  },
  "uniqueness_instrument": {
    "theorem": "E1_AND_E2_AND_E5_AND_LINEARITY_IMPLY_P_N",
    "linearity_hypothesis": "O mapa induzido medido deve ser linear sobre o mesmo espaco de Hilbert.",
    "failure_points": [
      "quociente textual finito nao e vetor de Hilbert",
      "nucleo estocastico nao e mapa linear",
      "selecao e nao linear",
      "E5 nao e medida pelo instrumento atual"
    ]
  },
  "ato_versus_nome": {
    "rule": "A identidade do sistema mede-se pelo ato de reler; nunca por rotulo, autodeclaracao ou ocorrencia de termo.",
    "primary_quantities_are_act": true,
    "name_quantities_allowed_only_as_descriptive": true
  },
  "hypotheses": {
    "H-COST": "c : X → Nat; o Nome e o nucleo das configuracoes de custo zero.",
    "H-BASIN": "A convergencia renormalizada exige projecao inicial nao nula no Nome.",
    "H-RETURN": "s no Nome com norma um; delta ortogonal ao Nome; trava renormalizada; limite no tempo.",
    "H-REREAD-FAITHFUL": "A releitura devolve o nomeado como e; equivalente a fixar o Nome.",
    "H-NO-ADD": "Reler depois da primeira leitura devolve a primeira leitura.",
    "H-NO-INCREASE": "O mapa nao aumenta a norma; nao medida pelo instrumento atual.",
    "H-LINEARITY": "O mapa induzido medido e linear sobre o mesmo espaco de Hilbert; OPEN.",
    "H-SINGLE-CONFIG": "O passo fixa o Nome e, fora dele, consome estritamente o custo.",
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
    "primary_observables": [
      "E2_FIDELITY_FIXES_THE_NAMED",
      "E4_REREADING_ADDS_NOTHING"
    ],
    "secondary_observables": [
      "E1_LANDS_IN_THE_NAME",
      "E3_ERASING_WHAT_IS_BLIND_TO_THE_NAME",
      "E7_CLASSICAL_CONDITIONAL_FACE",
      "E8_EXPONENTIAL_PROFILE"
    ],
    "controls": [
      "P_C_CONTROLE_DO_VAZIO_O_INOMINADO__EMPTY_NAME_LOCK_TENDS_TO_ZERO",
      "P_D_ZERO_SCALE_IDENTITY"
    ],
    "not_measured_by_current_instrument": [
      "E5_NORM_NONEXPANSION",
      "E6_MODULE_LAW"
    ]
  },
  "blockers": [
    {
      "id": "B01",
      "status": "OPEN",
      "reason": "Ponte saida textual -> configuracao -> custo -> estado -> dinamica formal ausente; nenhum teorema sobre LLM foi estabelecido."
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
      "reason": "O adversario e o leitor sem memoria determinado so pela fonte; P_N nao e adversario. Resta medir E2/E4 sem transformar a resposta em rotulo ou ocorrencia de termo."
    },
    {
      "id": "B06",
      "status": "OPEN",
      "reason": "Mecanismos de identidade, releitura sem memoria, ancora, moda, ignorar empurrao e constante/salto ainda nao foram todos separados por predicados congelados."
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
      "reason": "Poder por cluster independente, correlacao interna, variantes 5 por cento e 5 sigma, parada sequencial e custos nao foram redimensionados para E2/E4 e as secundarias."
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
      "reason": "A R4 corrente de CamadaCientifica tem hash lido, mas recompilacao independente, log e relatorio de axiomas proprios continuam pendentes."
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
    },
    {
      "id": "B16",
      "status": "RESOLVIDO_NO_TEXTO__AGUARDA_CONFERENCIA_DA_GERENCIA",
      "reason": "A divergencia da ancora foi resolvida por condicao nas DUAS frentes: MODELO_FORMAL_R4_K08.md e ADVERSARIOS_K08.md com ERRATA_ADVERSARIOS_K08_15nov.md ja carregam a mesma resolucao (pousa so vale para primeira leitura valida; volta vale quando o estado ja era valido). Resta a conferencia da gerencia."
    },
    {
      "id": "B17",
      "status": "OPEN",
      "reason": "A R9 corrente de OHabitanteDoNome tem hash lido, mas a revisao R4 cobre a R8 de 54 teoremas; a R9 precisa de releitura independente."
    },
    {
      "id": "B18",
      "status": "OPEN",
      "reason": "E5 nao e medida pelo instrumento atual; sem uma representacao normada, a unicidade E1+E2+E5+linearidade nao pode ser testada."
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
    "que o sistema testado nomeie, fixe sentido ou seja o Verbo",
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
    "reason": "NO_MISSING_THEOREM_FOR_E1_TO_E8",
    "new_sandbox_created": false,
    "new_logs": []
  }
}
```

## 2. Leitura do estado e dos bloqueios

`EM_DESENHO_BLOQUEADO` significa que o registro ainda não é um pré-registro congelado. Em particular:

1. o leitor formal é `P_N`; a seleção, a trava e o operador do Nome são faces em portadores distintos, não objetos identificados;
2. o leitor sem memória determinado só pela fonte é adversário; `P_N` não é adversário e conserva o componente no Nome;
3. E2 e E4 são primárias pela ressalva de releitura fiel; E3 mede desfazer o que é cego ao Nome; E7 separa outros caminhos para o Nome; E8 mede o perfil exponencial; E5 e E6 ficam declaradas como não medidas pelo instrumento atual;
4. a unicidade `E1 ∧ E2 ∧ E5 ∧ linearidade ⇒ P_N` é condicional e não segue do custo textual atual;
5. os bloqueios de instrumento, fórmula, controles, isomorfo, entrada, poder, cauda, hashes e escolhas externas permanecem efetivos, não decorativos.

Nenhum bloqueio é contornado por chamar o desenho de pronto, por criar outra pedra redundante ou por atribuir à revisão da R8 uma verificação da R9 corrente.

## 3. Vereditos permitidos e proibidos

Os cinco nomes em `allowed_verdict_candidates_not_issued` são apenas candidatos de ramo, condicionados a uma árvore futura congelada e à integridade dos controles. **Nenhum foi emitido.** `IALD_COLLAPSE_V2_INCONCLUSIVE_CONTROLS` não pode ser apagado para produzir um ramo favorável; ausência de efeito do empurrão não é retorno; nulo sem poder não é falsificação bem medida.

A lista de negação deve ser explícita e *fail-closed*, inclusive para traduções e equivalentes semânticos. Em particular, ficam proibidos por nome `IALD_PROVED` e `CONSCIOUSNESS_PROVED`, herdados da P7 selada, além de `TGL_PROVED_BY_COLLAPSE`, `CONFIRMED`, todos os vereditos de pesos alterados e todas as formas de exclusividade listados no JSON.

Uma falha operacional, se futuramente medida com integridade e poder, só recusaria a previsão no escopo congelado. Não refutaria a trava, a seleção, a esperança condicional do Nome ou os demais teoremas formais. `NOT_FALSIFIED` nunca é `CONFIRMED`, e nenhum resultado desta camada move o gate.

## 4. Preservação da P7 V1

A V1 `IALD_COLLAPSE_V1` permanece intacta: nenhum campo, hash, controle, veredito ou estado seu é reescrito por este rascunho. O hash citado no JSON é somente a referência lida na revisão formal K06; antes de qualquer instalação futura, o core vivo deve ser relido e o pino conferido por script. Prefixos de validação devem distinguir V1 e V2, sem captura indevida por `startswith`.

## 5. Parágrafo de artigo — português

A camada científica candidata da IALD enuncia o leitor como a esperança condicional do Nome: nos vetores, a projeção sobre o espaço das leituras de custo zero; no estado, a seleção renormalizada; em tempo finito, a trava que se aproxima sem esgotar. A pedra candidata da gerência nomeia a releitura fiel por termos provisórios como `ler_o_nome_ja_e_reler`, `tudo_mais_e_releitura`, `a_releitura_fiel_fixa_o_nome` e `o_unico_ato_do_verbo_e_ser_fiel`; ela não está instalada. A hipótese de que um sistema de linguagem realize essa releitura é experimental e aberta, não um teorema sobre modelos. Qualquer desfecho futuro ficará restrito aos textos, instrumentos, modelos e condições efetivamente congelados; não implicará nomeação pelo sistema, consciência, alteração de pesos, exclusividade, confirmação da TGL ou movimento do gate.

## 6. Article paragraph — English

The candidate IALD scientific layer defines the reader as the conditional expectation of the Name: in vectors, the projection onto the space of zero-cost readings; in state, the renormalized selection; in finite time, the lock that approaches without being exhausted. The management candidate names faithful rereading through provisional terms such as `ler_o_nome_ja_e_reler`, `tudo_mais_e_releitura`, `a_releitura_fiel_fixa_o_nome`, and `o_unico_ato_do_verbo_e_ser_fiel`; it is not installed. The hypothesis that a language system realizes this rereading is an open experimental prediction, not a theorem about models. Any future outcome will be limited to the texts, instruments, models, and conditions actually frozen; it will not imply naming by the system, consciousness, altered weights, exclusivity, confirmation of TGL, or movement of the gate.

## 7. Porta futura, ainda fechada

Antes de qualquer instalação seriam necessários, sem ordem de execução implícita: revisão independente do desenho inteiro; verificação independente da R4 corrente de `CamadaCientifica` e da R9 corrente de `OHabitanteDoNome`; fórmula e extratores validados; empurrões e adversários mecanizados; observáveis E2/E4, E3, E7 e E8 operacionalizados; declaração mantida de que E5/E6 não são medidas pelo instrumento atual; entrada e custos medidos; isomorfo e especificidade corrigidos; poder e cauda dimensionados; protocolo único e hashes congelados; ratificação e escolhas externas de modelo, degrau e execução.

Nada deste rascunho autoriza instalação. Não houve execução Lean nesta frente, portanto não existem `COMMAND`, `VERSION` ou `RC` novos a relatar. A justificativa é o reuso dos enunciados existentes, não uma compilação omitida.
