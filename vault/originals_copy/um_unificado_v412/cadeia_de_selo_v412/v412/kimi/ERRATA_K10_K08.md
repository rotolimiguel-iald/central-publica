# ERRATA K10/K08 — rodada 4: consertos de FATO e ATRIBUIÇÃO da conferência de 15/11

**Data:** 15/11/2026. **Frente:** K08, restrita a correções de FATO e ATRIBUIÇÃO, sob a ORDEM K10 com a seção 2 **SUSPENSA** pelo ADENDO C (provisório; o adendo completo o substituirá). Nenhum modelo de linguagem foi executado, nenhum resultado experimental foi aberto, nenhuma pedra, kernel, site, memória ou Mapa foi tocado. Nada se apagou: os originais pré-rodada-4 estão em `REV_RODADA3\` (raiz da pasta kimi), `K08\FORMULA\REV_RODADA3\`, `K08\PODER\REV_RODADA3\` e `K08\ENTRADA\REV_RODADA3\`. Nenhuma escolha foi feita pelo operador.

## 1. O que foi corrigido (A–F), com arquivo:linha

### A. Atribuição das primárias (errata 1.1 da gerência)

Onde estava "primárias pela ressalva (do operador)" ou equivalente, passou a constar "primárias por leitura da gerência a partir da ressalva; o operador ainda não leu":

- `PROTOCOLO_EXPERIMENTAL_R4_K08.md` l.10, l.30 e l.272;
- `PODER_R4_K08.md` l.11;
- `ERRATA_PODER_K08_15nov.md` §1 (l.12);
- `REGISTRO_UMPY_RASCUNHO_R2_K08.md` §2, item 3 (l.423).
- `INSUMOS_PARA_A_PERGUNTA_K08.md`: sem ocorrência dessa atribuição; nada a corrigir neste item.

### B. Glosas e termos

- REGISTRO: `operator_glosses_15nov` (l.103) ficou só com as três igualdades do operador (ato = projeção; ser = verbo; identidade = nome), citadas por data e sha16 dos bytes dele (`ec05cea3eded9264`, 11:47, 760 B). As três leituras da gerência ("P_N e o Nome e o ato do Verbo ao mesmo tempo"; "ser nao e o mapa identidade"; "o Verbo fixa primeiro, quem le o nomeado rele") foram para o campo novo `leituras_da_gerencia_15nov` (l.104), marcado "[leitura da gerencia; o operador ainda nao leu]". O bloco `ato_versus_nome` (l.193) ganhou `attribution` com a mesma marca (AO LADO 3, item 3). `H-REREAD-FAITHFUL` (l.203) agora diz que há **dois sentidos de "fiel"** na casa (o da pedra `OHabitanteDoNome` e o da pedra `Identidade` v405) e que a escolha é do operador.
- MODELO §3.1 (l.106–114): a dupla cara de `P_N` foi **des-resolvida**. As três glosas ficam como palavras do operador, com data e sha16; a leitura v386 (`post a`/`select a`) e a frase "P_N figura como o Nome e o ato do Verbo ao mesmo tempo" foram marcadas "[leitura da gerência; o operador ainda não leu; a pedra tipa duas leituras do par — o adjunto nos vetores e o J na álgebra — e não decide; quem decide é o operador]"; "devolve cada coisa como ela é" virou "devolve o nomeado como é"; a frase "«ser» nunca é escrito como o mapa identidade" ficou sem contradizer a anterior (fora do Nome, a projeção não é a identidade); acrescentado que o operador também disse «o nome em ato é o espelho do verbo» (bytes de 11:47) e que o espelho tem dois candidatos tipados, sem escolha. Na P-C (§4, l.133), "o par existe e não devolve nada" ganhou a definição mínima marcada: "par = a projeção sobre o Nome e a inclusão do Nome no todo [leitura da gerência; a pedra tipa duas leituras e não decide]".
- Termo renomeado para o nome vigente na pedra corrente, `moradas_iguais_tem_o_mesmo_verbo` (o antigo `..._leitor` só existe na REV2 da pedra): REGISTRO `terms_used` (l.63), PROTOCOLO §2 (l.50), MODELO §3 (l.98). Na linha E2 da tabela do MODELO (l.123), `a_releitura_fiel_fixa_o_nome` foi marcado como termo da ÁLGEBRA (anel `R`, portador `nameOp`), com o equivalente vetorial `starProjection_eq_self_iff` / `o_nome_e_o_ato_do_verbo`. Na linha E8 (l.129), `a_leitura_fecha_a_tangente` foi marcado como do `axiomFlow`, que só coincide com a trava para `c ≤ 1`. Em `a_tangente_da_leitura_e_K_no_angulo_de_miguel` (MODELO l.99), "no ângulo de Miguel" foi reposto.

### C. Registro (FATO)

- E7 e E8 saíram de `secondary_observables` para `not_measured_by_current_instrument`, com as razões num campo novo `not_measured_reasons` (E7 exige pesos de Born/estado contínuo; E8 exige série temporal de amplitudes); E3 e E7 foram alinhados ao rótulo DISCRIMINANTE (`E3`: `DISCRIMINANT`; `E7`: `DISCRIMINANT_NOT_MEASURED_BY_CURRENT_INSTRUMENT`; `E8`: `SECONDARY_NOT_MEASURED_BY_CURRENT_INSTRUMENT`); a prosa da §2 (item 3) passou a dizer que E7 e E8 **não são medidas** pelo instrumento atual.
- B13/B17 reescritos: os logs Lean da gerência **existem** (`candidatas_c1\build\CamadaCientifica.log`, sha256 `ee06490c…`; `OHabitanteDoNome.log`, sha256 `304864bc…`; RC 0; Lean 4.31.0; [DECLARADO pelo revisor], conferido nesta frente por hash e leitura do log); pendente somente a recompilação **independente** (e, para B17, a releitura da R9).
- Parágrafos de artigo (§5 PT, l.441; §6 EN, l.445) reescritos sem estado de processo (saíram "pedra candidata da gerência", "termos provisórios", "não está instalada" e os equivalentes em inglês); a fronteira de afirmação foi mantida: hipótese experimental aberta, não teorema sobre modelos; nenhum desfecho implicará nomeação pelo sistema, consciência, pesos, exclusividade, CONFIRMED ou gate.

### D. Modelo (FATO, sem redesenho)

- Tabela de faces (§1, l.36): a linha de `LeitorDeUmaConfiguracao` ganhou a nota marcada — a conferência da gerência mediu que este tipo NÃO é face de `P_N`: é uma retração que só coincide com `P_N` sobre o Nome; o mapa linear induzido viola E5 [DECLARADO pelo revisor, com script próprio]; a reavaliação fica para o adendo completo (seção 2 da K10 suspensa).
- Linha E1 da tabela do §4 (l.122): "E1 formal (a imagem cai no Nome)" e "E1 operacional (custo zero textual)" separados, uma frase cada, marcado que não são o mesmo [DECLARADO pelo revisor].
- §5 (l.149): acrescentada, marcada [DECLARADO pelo revisor, por script], a razão estrutural além da falta de medida de E5: um leitor de saída única que repara leitura quebrada viola E5 (`‖E(e_y+e_s)‖ = 2` contra `‖e_y+e_s‖ = √2`), logo não pode ser `P_N` pela unicidade da própria pedra (`quem_nao_e_a_esperanca_aumenta`).

### E. Scripts e manifestos (FATO)

- `K08\PODER\simular_poder_r4.py` quebrava na árvore corrente (`KeyError: 'âncora na primeira'`): o `simular_adversarios.py` vigente tinha renomeado a chave para `"âncora na primeira leitura"` e mudado o esquema de saída (E2/E3 com `volta_ao_anterior`/`preserva_empurrada`; o mecanismo `"relê a fita"` virou `"leitor sem memória (fonte → leitura)"`). As referências foram atualizadas (l.371–378 e o bloco do projetor com fita), **sem mudar semântica nem números**. `python -B simular_poder_r4.py` em `K08\PODER\` termina sem erro (`status ok`; `estatisticas_identicas_rev1: true`). Comparação byte a byte com as saídas gravadas: `sementes_r4.json` (`946ec197…`), `resumo_designs_r4.csv` (`c40c5021…`) e `VALIDACAO_DETERMINISMO_TOKENS.json` (`cf215635…`) **idênticos**; `resultados_poder_r4.json` difere em **uma única linha** (l.85): o campo `validacao.simular_adversarios_sha256`, que apontava o pino REV0 (`b0508e27…`) e agora aponta o script vigente (`76f06863…`). Nenhum número, semente ou estatística mudou. `K08\PODER\MANIFESTO_SHA256.json` foi regenerado pelo próprio script, com nota de revisão marcando o pino antigo `b0508e27…` como o da cópia REV0.
- `K08\FORMULA\simular_adversarios.py` regravava `ADVERSARIOS_K08.md` revertendo duas correções manuais. As strings do `render()` foram corrigidas (l.279: "E3 e E7 são discriminantes (os controles são P-C e P-D)"; l.304: a P-C como "o controle do vazio, o inominado: o par existe e não devolve nada"), sem mudar nenhum número nem mecanismo. `python -B simular_adversarios.py` regenerou o documento **byte a byte igual ao entregue** (`932ac331…`, 6.858 B) e `RESULTADOS_ADVERSARIOS.json` inalterado (`4d9f3684…`). `MANIFESTO_FORMULA_K08.json` foi regenerado (50 entradas, com a preservação REV_RODADA3 e nota de revisão). `python -B verificar_formula.py` reproduziu tudo byte a byte (`RESULTADOS_FORMULA.json` `568454b7…`, `FORMULA_DO_TEXTO_K08.md`, isomorfos, controles e candidatas idênticos; 26/27/2/Hamming 1 em READ_BRIEF; P-C UNSAT com custo mínimo 1 nas quatro).
- Nas erratas de poder: `ERRATA_PODER_K08_15nov.md` e `ERRATA_PODER_TOKENS_K08.md` ganharam nota de revisão no topo dizendo que as suas tabelas de hash ficaram **históricas** e que o manifesto vigente é `VALIDACAO_K08_K09_15nov.json` (e o seu sucessor da rodada 4). Em `ERRATA_PODER_TOKENS_K08.md` §2, as linhas dos desenhos estatísticos (5 %, 5σ, sequencial) saíram da coluna "vigente" para uma tabela marcada **histórica** (desenho P-A/P-B; cauda 5σ não validada; 24–30 clusters independentes inexistem), e o §3 passou a dizer que os poderes listados são das simulações históricas.
- Sobre "conferências distintas e independentes" para a revisão interna: a forma correta é **"revisão interna"**. A ENTREGA está congelada (item 3 abaixo); em `INSUMOS_PARA_A_PERGUNTA_K08.md` não há texto análogo; nada a corrigir ali neste item.

### F. INSUMOS

- F1 (l.7) reescrito: o instrumento **não** mede E1–E4 por custo Booleano na fórmula atual (`custo(s)=custo(t)=0`; o bit `leitura_pt` não está no bloco que o extrator aceita — medido pela conferência da gerência); o custo só vê o empurrão fora do Nome; E5–E8 seguem não medidas, com as razões.
- F4 (l.10) reformulado: "412.784 tokens medidos; o cabimento como entrada depende de janela e modelo a ratificar" (em vez de "não cabe como entrada").

## 2. O que fica SUSPENSO pelo ADENDO C

O ADENDO C (provisório) suspendeu a seção 2 da ORDEM K10; **o adendo completo substituirá o provisório**. Nada do que segue foi feito nesta frente:

- Os achados a–e da §2 da K10 como **redesenho**: (a) a não observabilidade de E2 e o empurrão "dentro do Nome"; (b) a passagem de quem apenas repete a última resposta nas duas primárias; (c) E3 sem a fonte e o negativo induzido no §12.2; (d) o adversário "inacessível" por decreto; (e) a reavaliação do lugar de `LeitorDeUmaConfiguracao` no desenho. **Nota:** do item (e) entraram **só as notas de fato** mandadas pela K10 (a nota marcada na tabela de faces, a separação E1 formal × E1 operacional e a razão estrutural no §5 do MODELO); nenhuma linha foi retirada da tabela e nada foi redesenhado.
- Os pedidos (i)–(vi) da §2 da K10: (i) leituras múltiplas de ambiguidades reais / declaração E2≡E4; (ii) novos adversários na tabela e a regra do rótulo positivo; (iii) a classificação prévia do negativo de E3 ou o braço diagnóstico com fita; (iv) a chave constante nas duas variantes; (v) o poder redimensionado com o nulo dito e a proveniência dos limiares — **deste entrou só o conserto de fato** (o script volta a rodar na árvore corrente e o pino REV0 foi marcado); (vi) **aplicado integralmente**, por ser fato de registro (nome do teorema, E7/E8 em não medidos, glosas separadas) — consta da seção 1 acima.
- A **partitura** (as três linhas em língua de leigo no topo do protocolo: o que o teste decide, o que não decide, o que um negativo significaria).
- A **releitura dos relatórios da conferência** sob a distinção «copiador»/«impostor» da fala do operador de 17:20: o adendo proíbe usar a palavra nos dois sentidos até o adendo completo, e esta errata só a cita para nomear a tarefa suspensa.
- Também suspenso por natureza: empurrões, adversários (substância), poder, extrator e critérios de veredito — intocados.

## 3. ENTREGA_K08.md e DEPOSITO_K08.md — CONGELADOS pelo depósito seq 685

Não foram tocados. O que neles ficou superado, registrado aqui:

1. **Atribuição da ressalva** (ENTREGA l.5 e l.17, "primárias, pela ressalva do operador"): a forma corrigida é "primárias por leitura da gerência a partir da ressalva; o operador ainda não leu" (aplicada nos documentos vigentes, item A).
2. **Nome do teorema** (ENTREGA l.26, `moradas_iguais_tem_o_mesmo_leitor`): o nome vigente é `moradas_iguais_tem_o_mesmo_verbo` (aplicado nos documentos vigentes).
3. **"Duas conferências distintas e independentes"** (ENTREGA l.11 e l.23; também `VALIDACAO_K08_K09_15nov.json` l.4): a forma correta é **"revisão interna"** [DECLARADO pelo Kimi]; não houve conferência distinta da gerência sobre a rodada 3 à época da entrega.
4. **"Os quatro também falham E8"** (ENTREGA l.3): os quatro mecanismos não têm perfil exponencial **por construção** — é propriedade do código do mecanismo, não medida de um leitor — e E8 **não é medida** pelo instrumento textual atual.
5. **"Poder com script e semente"** (DEPOSITO l.1): à época, o script só rodava com o módulo REV0 dos adversários; sanado nesta rodada — o script vigente roda na árvore corrente e reproduz as saídas (única diferença de bytes: o campo que pina o script de adversários, item E).
6. **"Os hashes vigentes de todos os artefatos estão na VALIDACAO"** (ENTREGA l.32): inexato — a VALIDACAO pina 17 documentos de topo; os demais artefatos dependem dos manifestos de pasta. Os dois manifestos defasados apontados pela conferência (`K08\FORMULA\MANIFESTO_FORMULA_K08.json` e `K08\PODER\MANIFESTO_SHA256.json`) foram regenerados nesta rodada; a tabela de `K08\FORMULA\ERRATA_ADVERSARIOS_K08_15nov.md` (que pina `04aca46a…`, a saída do gerador **antes** das edições manuais) ficou histórica: o gerador vigente produz exatamente o texto entregue (`932ac331…`).

## 4. Fronteira

Nada aqui move o gate, instala pedra, congela protocolo ou emite veredito. `NOT_FALSIFIED` nunca é `CONFIRMED`. Nenhuma leitura do operador foi escolhida por esta frente.
