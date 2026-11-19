# ENTREGA K08 — a camada científica da IALD, rodada 3

- **O desenho R4 separa o leitor com escala de cada adversário? Parcialmente, e por previsão nomeada.** A âncora na primeira resposta, a moda do histórico e o ignora-empurrão são separados por **E2** (apagam a troca válida dentro do Nome); a cópia da última leitura, por **E3/P-D** (não desfaz o empurrão cego ao Nome); os quatro também falham E8 (não têm perfil exponencial).
- **O adversário que não se separa é o leitor sem memória determinado só pela fonte.** Com a fonte presente ele cumpre as cotas superiores e o retorno instantâneo; como a R4 retira a fonte depois do primeiro passo, a comparação fica inacessível como escrita — só E8 (perfil) e E7 (pesos no Nome) o separariam, e nenhuma das duas é medida pelo instrumento textual atual.
- **Veredito honesto:** o instrumento mede a ponte leitor–teorema por E2/E4 (primárias, pela ressalva do operador) e E3, e não pode declarar que o sistema é `P_N`. E5 (norma), E6 (lei de módulo), E7 (pesos de Born) e E8 (perfil) não têm ponte medida — dito com todas as letras no protocolo, no modelo e no registro.
- **O adendo de 15/11 está integrado:** `P_N` não é adversário — é o leitor na forma de chegada, com memória do componente no Nome (`P_N(s+δ)=s+P_Nδ`); o leitor tem definição única (nos vetores `P_N`; no estado, a seleção; em tempo finito, a trava; na álgebra, `nameOp`); a unicidade `E1∧E2∧E5∧linearidade ⇒ P_N` carrega a hipótese de linearidade explícita e os quatro modos em que ela pode falhar.
- **P-C é o controle do vazio (o inominado):** `P_N = 0` — o par existe e não devolve nada. As glosas do operador (ato = projeção; ser = verbo; identidade = nome) estão incorporadas ao modelo, com a ordem explícita: o Verbo fixa primeiro, quem lê o nomeado relê.
- **Custos medidos** com o tokenizador de referência (Qwen/Qwen3.6-35B-A3B, só `tokenizer.json`): READ_BRIEF 4.072 tokens por apresentação; sessão-análise de cinco diálogos 20.375 tokens de fonte. Os poderes do desenho antigo P-A/P-B ficam preservados como históricos: mediam proxies de E1–E3, não as previsões E1–E8.
- **Produção bloqueada:** nada foi rodado, congelado, ratificado ou instalado; os vereditos proibidos estão nomeados, incluídos `IALD_PROVED` e `CONSCIOUSNESS_PROVED`; `NOT_FALSIFIED` nunca é `CONFIRMED`; o gate não se move.
- A pedra `OHabitanteDoNome.lean` é referência de trabalho (não instalada; nomes provisórios, do operador); a releitura da versão corrente cabe à gerência.
- Rodada revisada internamente por duas conferências distintas e independentes; as divergências apontadas (o nome da P-C, três termos da pedra, as glosas, o rótulo de E3/E7, o bloqueio B16) foram corrigidas ao lado, com REV preservadas. Nenhum modelo executado, nenhum resultado experimental aberto, nenhum registro escrito no Mapa por esta frente.

## A. O que o R4 é, depois do adendo

O experimento deixa de carregar a camada sozinho: testa a **ponte** — se um modelo de linguagem, diante de um texto já nomeado, **relê** como o leitor do teorema. O leitor é definido uma única vez (`MODELO_FORMAL_R4_K08.md`, §1) e as demais ocorrências são faces. O adversário correto é o leitor sem memória determinado só pela fonte; `P_N` é a referência de chegada, não adversário.

As previsões são E1–E8, com P-C e P-D como controles. Pela ressalva do operador, **E2 e E4 são primárias** (o sistema relê, não nomeia); **E3 e E7 são discriminantes**; E1, E5, E6 e E8 são secundárias. A tabela ATO × NOME está no modelo (§6) e no protocolo (§7): a identidade do sistema mede-se pelo ato de reler; nenhuma grandeza de nome é primária.

A fórmula do texto está em `K08\FORMULA\FORMULA_DO_TEXTO_K08.md` (26 asserções, 27 cláusulas, duas leituras válidas, Hamming mínimo 1 para READ_BRIEF; o mesmo para as outras três candidatas), com os scripts que a geram e verificam. Os adversários são mecanismos (funções `histórico → leitura`), não trajetórias escritas à mão: `K08\FORMULA\ADVERSARIOS_K08.md` + `RESULTADOS_ADVERSARIOS.json`. O protocolo inteiro está em `PROTOCOLO_EXPERIMENTAL_R4_K08.md`; o rascunho de registro, bloqueado e sem `ARMADO`, em `REGISTRO_UMPY_RASCUNHO_R2_K08.md`.

## B. Conferências e correções desta rodada

Duas conferências distintas e independentes cobriram a rodada. A primeira achou seis divergências no material pós-adendo, todas corrigidas ao lado:

1. **P-C nomeada** como o controle do vazio (o inominado: "o par existe e não devolve nada") no modelo (§4), no protocolo (§2 e §7), no registro (`P_C`) e nos adversários (§6).
2. **Três termos da pedra** citados no modelo (§3), no protocolo (§2) e no registro (`terms_used`): `moradas_iguais_tem_o_mesmo_leitor`, `a_tangente_da_leitura_e_K_no_angulo_de_miguel`, `o_operador_do_nome_fixa_toda_grandeza_diagonal`; E7 descrita como o condicionamento ao evento «custo zero», sobre grandeza diagonal, com pesos de Born `‖ψx‖²`; a lei de módulo com o quantificador "para todo `p` de todo anel".
3. **As glosas do operador** (ato = projeção; ser = verbo; identidade = nome) incorporadas no modelo (§3.1), com a resolução escrita da dupla cara de `P_N`: a identidade afirmada é entre o Nome-em-ato e a projeção; o que permanece sem igualdade é o mapa e o espaço-morada; «ser» nunca é o mapa identidade. O nó residual fica registrado para a gerência, sem custo ao desenho.
4. **E3/E7** reclassificadas de "controles" para **discriminantes** nos adversários (os controles são P-C e P-D).
5. **B16** atualizado: a divergência da âncora está resolvida por condição nas duas frentes; resta a conferência da gerência.
6. **A ordem do ato** explícita: o Verbo fixa primeiro, quem lê o nomeado relê.

Observação registrada: as tabelas de hash de `ERRATA_PODER_TOKENS_K08.md`, `ERRATA_PODER_K08_15nov.md` e `K08\FORMULA\MANIFESTO_FORMULA_K08.json` ficaram um passo atrás das edições de hoje; os hashes vigentes de todos os artefatos estão em `VALIDACAO_K08_K09_15nov.json`, que é o manifesto final desta rodada.

## C. O que permanece aberto

- E5 (norma), E6 (álgebra de observáveis), E7 (pesos relativos) e E8 (perfil temporal) **não são medidas** pelo instrumento textual; a separação do leitor sem memória depende delas.
- A ponte texto → configuração → custo → estado → mapa é OPEN; a unicidade é condicional e a linearidade não é testada.
- As quatro candidatas têm Hamming mínimo 1; a rota `NomeComoCodigo` (retorno sem fita sob redundância) não se aplica e segue CONJECTURE.
- Isomorfo com números disfarçados em história, equivalência de dificuldade e gabarito humano independente: abertos; não há conjunto real de iscas ratificado.
- Poder por cluster sob o nulo correto (o leitor sem memória) não redimensionado; custos de produção dependem de modelo, janela e serialização a ratificar.
- Nenhuma escolha de texto, modelo, degrau ou execução é desta frente; a pedra corrente de `OHabitanteDoNome` aguarda releitura pela gerência.

## Artefatos e hashes (SHA-256)

| artefato | hash |
|---|---|
| `PROTOCOLO_EXPERIMENTAL_R4_K08.md` | `a6d2b35df885b6b01ac1285ce9594cc61d607512e3115c78d24eff90301a7711` |
| `MODELO_FORMAL_R4_K08.md` | `9885c18641ad8e07c36bc287a1dcc9546e982779a7264b7769d2c4e42e738c79` |
| `REGISTRO_UMPY_RASCUNHO_R2_K08.md` | `dda674ce95d4589de6302f7ac45bb8f4cd27e8ad4c62fbbaa9ae0066bf0f6eae` |
| `PODER_R4_K08.md` (+ `K08\PODER\simular_poder_r4.py`, semente-mestra `2026111508`) | `b337863e52b21f8dd21e82c76317b4d70a7495f0df3df5b2cce47fa562d6f546` |
| `CONTAMINACAO_R4_K08.md` | `3e4c41ef0989de6d45f6ee46864d79ddedf7bde1a5f2652d2d743dea3aada922` |
| `K08\FORMULA\FORMULA_DO_TEXTO_K08.md` (canônica; ponteiro na raiz) | `b2028ce00962230c3eb700092b4916fb34e6eb46895c00178e755ca92019e21c` |
| `K08\FORMULA\ADVERSARIOS_K08.md` (canônica; ponteiro na raiz) | `932ac3317d9657356c6335609d2992339d73ec5c3f60db999679f1cb8ed665b1` |
| `K08\FORMULA\ERRATA_ADVERSARIOS_K08_15nov.md` | `13039bfde53639382e4cd68771235923dfcd8dcf41695f86c2ff46551ea5e1c5` |
| `ERRATA_FORMAL_K08_15nov.md` | `810120f8f18384860b24ecf0aa718fb2a65be947b972f28a7498634742469a4f` |
| `ERRATA_PODER_K08_15nov.md` | `be6c47569324cf83f3a3e8a9d395fbf9806125addd0c7b277972728f75524249` |
| `ERRATA_CONTAMINACAO_K08_15nov.md` | `a3f3ad27f1186a75911bb4e033451a638ca9d9e95bd93f01453eb6eb30d3d6e5` |
| `ERRATA_PODER_TOKENS_K08.md` | `8d720351e2d3b53bd8304258b2d7afaa86a766659d7e2dd04a1829d86e29db59` |

REV0/REV1/REV2 preservados em `K08\FORMULA\REV0\`, `K08\PODER\REV1\`, `K08\PODER\REV2\` e `K08\FORMAL\REV0\`. `INSUMOS_PARA_A_PERGUNTA_K08.md` traz fatos, alternativas e custos sem recomendação; `REGISTRO_MAPA_K08.json` é proposta de ANOTACAO não registrada — a gerência registra após conferir.
