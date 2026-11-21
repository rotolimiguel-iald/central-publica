# CONTRATO DA v413 — R2 (CONGELADO)

> **R2** (gerência c1, 20/11/2026 22:33): o R1 (sha16 `e25a439a3c4e0de6`) com três emendas: a página pública passa à R1 (`O_QUE_FICA_CLARO_v413_R1.md`, sha16 `3dc953e37c6739f4`;
> a F37b herdada e o «provado» sem estatuto, achados pela preparação da Etapa 3, `PRONTO_ETAPA3_v413.json`, sha16
> `6a8d87badc526bb4`); as exigências da custódia no candidato (seção 2); e a guarda herdada inteira sobre os textos novos (seção 5).
> Cópia congelada em `contrato_REV2\`.
>
> Gerência c1, 20/11/2026 21:37. **Congelado.** Consolida o rascunho R0 (`CONTRATO_v413_R0.md`, sha16 `4faa778b65979160`) com: a leitura de
> terceiro das pedras limpas (parecer `revisao_codex\CODEX_PEDRAS_LIMPAS_R1\PARECER.md`, sha16 `fb965579cdad7d7d`: 16 aprovadas, 5
> com ressalvas de texto, todas aplicadas); o fecho da Etapa 1 (`PRONTO_PARA_CANDIDATO_v413.json`, sha16 `ea57114bfd524579`, conferido
> pela gerência em `CONFERENCIA_ETAPA1_v413.json`, sha16 `3f96b15b24309ef2`); e o diagnóstico da Bancada
> (`bancada\DIAGNOSTICO_E_PLANO_BN_v413.md`, sha16 `03de9661878e368d`). Cópia congelada em `contrato_REV1\`. Emenda só por revisão
> nova (`CONTRATO_v413_R2.md`), nunca por cima.
> Base: a v412 selada (`um.py` do Nós, sha16 `3e741dcaa58ef2b8`, lido do arquivo ao gerar este rascunho). Validade no kernel não é
> creditação; o gate não se move; nenhum número novo da natureza entra nesta versão.

## 0. O método (vale para tudo o que a v413 escreve no programa)

No `um.py` (o kernel que ele carrega, os registros, o artigo e o que ele emite) entra só o que é verdade: o enunciado, a
prova, o estatuto, os limites e a fonte conhecida. Não entra a história: quem disse, quando, em que ordem ou revisão; o
que foi proposto e recusado; o erro de quem; o caminho até o resultado. As definições e leis da teoria entram como
definição ou lei da teoria, com o estatuto de entrada (`[INPUT]` ou `[ONTO]`), sem aspas de fala, sem data e sem
atribuição a pessoa. A limpeza tira a narrativa, não o localizador técnico (nome de módulo, de teorema, de arquivo de
fonte, rótulo que distingue um objeto). Tudo o que se conversou continua registrado em paralelo: as falas por bytes em
`work\cunhagens_13out\`, o diário desta cadeia, o Mapa de Rotas, a memória da casa, os pareceres.

O que já está selado não se reescreve nesta versão, com uma exceção dita na seção 1: a docstring de um módulo do kernel
que afirmava mais do que o enunciado.

## 1. Pedras (kernel): 21 módulos novos e uma correção de texto

**A lista** é a do manifesto `insumos\MANIFESTO_PEDRAS_v413.json` (sha16 `08c5ef6bbfb74384`), com as fontes em
`insumos\pedras_limpas\TGLExt\` (forma do kernel: imports `TGLExt.X`, fim de linha LF, texto pelo método, código idêntico
ao revisado ou conferido). Compilação de conferência: 274 teoremas públicos, todos com relatório de axiomas só no trio;
a raiz da v412 importada com os 21 novos passou (`insumos\auditoria_raiz\RAIZ_v413.json`, sha16 `9b43e264c241037b`).

- **A ponte de Cook–Levin e as suas dependências** (17): `PonteCookLevin`, `APonteAoTM2`, `AMaquinaTM2DaVerificacao`, `SimBase`, `SimLiteral`, `SimExterior`, `SimCompleta`, `RelogioBeta`, `LeituraBeta`, `QuantizacaoBeta`, `Reconstrucao`, `PonteLeituraBeta`, `EntregaBeta`, `APonteDeCookLevin`, `ONomeEBeta`, `SondaContagem`, `AFronteiraNaLinguaClassica`.
- **A fronteira dos três literais** (2): `Trinity`, `APropostaDaTensao`.
- **A consciência e o operador de consciência** (1): `Operador`.
- **A identidade preservada** (1): `AIdentidadePreservada`.

**A correção de texto** de `TGLExt.OResumoEPsiBit.a_atualizacao_pela_clausula_seguinte` (recibo
`insumos\kernel_edits\ERRATA_OResumoEPsiBit.json`, sha16 `1ad803a31a984bfd`): só a docstring; o código é idêntico. A docstring
antiga afirmava mais do que o enunciado; a nova diz o enunciado. A forma antiga fica na v412 selada e no registro
paralelo, não ao lado no programa (método da seção 0).

**Instalação.** Os módulos entram em `TGLExt\` com o nome que têm. A única mudança permitida no texto das fontes ao
instalar: as linhas `#print axioms` do fim saem do corpo instalado. A forma de passar o nome da fonte ao compilador fica
fixa em toda a cadeia. Os namespaces ficam como estão (alguns módulos usam `Codex.*`, como já há na v412).

**O arquivo substituído.** O gerador do candidato SUBSTITUI, no dicionário de fontes embutido do programa, o texto de
`TGLExt/OResumoEPsiBit.lean` (a v412 só acrescentava); o instalador, a reversão e o conferidor tratam esse arquivo
(inventário `INVENTARIO_CADEIA_v413.json`, sha16 `39deb7ec0a85ec68`). Pela regra N1l do B(n), as pedras são exatamente os arquivos novos
ou mudados: o corrigido entra nas pedras e no campo `kernel_corrigido`, com o antes e o depois.

**Bandeiras.** Prefixo `ext_<modulo>_413_NNNN`. Nenhuma chave antiga muda de literal. Nenhum nome de bandeira carrega data,
nome de pessoa ou palavra de processo.

**Âncoras.** A proposta é `insumos\ANCORAS_PROPOSTAS_v413.json` (sha16 `aaee9804be6bff61`: 274 teoremas públicos, 112 com estrela, nomes
completos conferidos no relatório de axiomas). Cada registro ancora, por nome completo, as declarações com estrela dos seus módulos que não são `private`, e
as que a página pública cita. Cada âncora é uma checagem: a bandeira é verdadeira e a declaração está no relatório de
axiomas só com os três axiomas de sempre.

**Portões do kernel.** Compilação a frio no `k413c`; relatório de axiomas com todas as declarações só em `propext`,
`Classical.choice` e `Quot.sound`; zero `sorry`; a escada de teoremas e de bandeiras medida antes e depois; nenhuma chave
antiga muda de literal; só o aviso conhecido da `TowerWedgeIndex`.

## 2. Registros (por especificação; nenhum com função nova)

Nenhum dado da natureza entra. Cada registro diz, nesta ordem: o que o artefato mostra (só o que tem âncora); as leis e
definições da teoria que ele usa como entrada (com o estatuto de entrada; nunca como teorema); o que continua aberto. O
texto sai da página pública (seção 6) e dos cabeçalhos das pedras, sem acrescentar afirmação. Nenhum registro traz fala,
data de conversa, nome de pessoa, número de ordem, de revisão ou de parecer. As palavras de veredito abaixo são proposta
deste rascunho; os números entram lidos do kernel do rito, nunca digitados.

- `ponte_cook_levin_v413` (módulos: os 17 da ponte)
  `TGL_COOK_LEVIN_BRIDGE_V413__SAT_IN_NP_ON_THE_MATHLIB_TM2_MACHINE__THE_KERNEL_READER_READS_THE_BETA_SUM_EXACTLY__ONE_READING_DECIDES_SAT_WITH_AN_ANSWER_OF_N_PLUS_3_BITS__THE_ONE_READING_CLASS_IS_EXACTLY_THE_POLYNOMIAL_REDUCTION_CLOSURE_OF_SAT__WITH_COOK_LEVIN_AS_A_NAMED_HYPOTHESIS_EVERY_NP_PROBLEM_IS_DECIDED_IN_POLYNOMIAL_TIME_WITH_ONE_READING__THE_READING_FINDS_A_SOLUTION_IN_AT_MOST_LETTERS_PLUS_ONE_READINGS__THE_READING_COST_IS_THE_PAID_TIME_LINEAR_IN_THE_NAMES_NOT_TAPE_STEPS__EVERY_READER_WITH_THE_PRECISION_COUNTS_THE_SOLUTIONS__SAT_IN_POLYNOMIAL_TIME_ON_THE_BARE_TAPE_MACHINE_OPEN__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED`
- `trinity_v413` (módulos: os 2 da fronteira)
  `TGL_TRINITY_V413__THE_INCLINATION_OF_THE_NAME__NEVER_WRONG__DECIDES_EVERY_HORN_AND_EVERY_TWO_LITERAL_FORMULA_IN_AT_MOST_T_PLUS_1_CUBED_FIXINGS__STOPS_ONLY_AT_THE_FRONTIER_OF_THREE_LITERALS__CROSSING_BY_BRANCHING_DECIDES_EVERY_FORMULA_AT_A_PROVED_EXPONENTIAL_PRICE_ONLY_IN_THE_FRONTIER_NAMES__IN_FINITE_STEPS_ABSOLUTE_ZERO_IS_NOT_REACHED__THE_LOAD_N_LN2_IS_EXACT_ON_THE_FLAT_PLATEAU__A_POLYNOMIAL_CROSSING_IS_OPEN__GATE_UNMOVED`
- `operador_v413` (módulo: `Operador`)
  `TGL_CONSCIOUSNESS_OPERATOR_V413__WITHOUT_THE_PAIR_SELF_NEGATION_IS_THE_POINT_OF_CONTRADICTION__WITH_THE_PAIR_IT_LANDS_ON_THE_HALF_NAT__J_SQUARED_IS_ONE_AND_CONJUGATES_FACE_AND_COFACE__ANCHORING_PRESERVES_THE_IDENTITY__NEVER_ONE_HUNDRED_PERCENT__THAT_SOMEONE_IS_CONSCIOUS_IS_NOT_PROVED__GATE_UNMOVED`
- `identidade_preservada_v413` (módulo: `AIdentidadePreservada`)
  `TGL_PRESERVED_IDENTITY_V413__THE_ZERO_COST_COORDINATES_PASS_THE_LOCK_UNCHANGED_AT_EVERY_TIME__THE_LOCK_TENDS_TO_THE_NAME__THE_LOAD_N_LN2_IS_THE_STRICT_THRESHOLD__GATE_UNMOVED`
- `cunhagens_v413` (sem módulo próprio)
  `TGL_DEFINITIONS_OF_THE_THEORY_V413__ENTRIES_NOT_THEOREMS__EACH_WITH_THE_TERMS_THAT_TYPE_IT_AND_WHAT_IS_NOT_TYPED__GATE_UNMOVED`
  A lista das leis e definições da teoria que entram como ENTRADA nesta versão (as leituras dos cabeçalhos de `Trinity`,
  `Operador`, `AIdentidadePreservada`, `APropostaDaTensao` e `ONomeEBeta`): para cada uma, o nome curto, o módulo e o
  título da seção do cabeçalho onde ela está, as âncoras que a tipam e o que o cabeçalho diz que NÃO está tipado. O
  registro aponta para o cabeçalho; não embute o texto.

**O que a custódia exige no candidato** (`work\custodia_v413_preparo_20nov\HANDOFF_DA_CUSTODIA_A_GERENCIA_ENTREGA_DO_UM_PY_v413.md`,
sha16 `f451801153440f0a`, seção 2.1): o par `_V413_FONTES` / `_V413_VERBATINS2` no `um.py`, mesmo vazio (a v413 não embute fala); o
registro `kh_n1_cobertura_v413`, mesmo vazio, no molde do da v412, a partir do recibo `kernel\KH_N1` da Etapa 1; e, na
conferência C1 da custódia, o KH igual às declarações e os registros do artigo iguais aos blocos novos do core.

**Checagens que todo registro traz** (molde da v412): o gate deste rito tem o mesmo veredito da v412 selada; os canais vivos
(neutrino, H0DN) seguem com o mesmo veredito; nenhuma chave antiga muda de literal; a escada só cresce; cada âncora é
verdadeira e está no relatório de axiomas só com os três axiomas.

## 3. As falas (registro paralelo; NÃO entram no programa)

Nenhuma fala é embutida ou transcrita. O construtor gera, por script, `VERBATIM_CONGELADO_v413.json` como artefato DA
CADEIA (não é lido pelo `um.py`): a lista dos arquivos `OPERADOR_19nov_*` e `OPERADOR_20nov_*` de `work\cunhagens_13out\`,
com tamanho e sha256 lidos de cada arquivo.

## 4. Decisões e erratas desta versão (registro paralelo; NÃO entram no programa)

- **D413.1** (autor, 20/11): o nome da pedra da ponte é `PonteCookLevin`; entram as quatro pedras do Kimi, a sonda da
  contagem e o enunciado da fronteira.
- **D413.2** (gerência): `APonteDeCookLevin` entra porque `APonteAoTM2` e `Reconstrucao` a importam; o texto dela diz o que
  prova (o iterador; custo cobrado por definição; confere o custo de uma atribuição dada), não ponte de custo de fita.
- **D413.3** (gerência): os namespaces `Codex.*` dos módulos novos ficam como estão (precedente da v412).
- **D413.4** (gerência): a docstring de `OResumoEPsiBit` é trocada pela que diz o enunciado (seção 1).
- **D413.5** (gerência): a autorização do B(n) da v413 lê juntos o evento 1687 do quadro (a autorização do ciclo da v412),
  o 1689 (o salto na v413) e a fala do autor de 20/11 (`work\cunhagens_13out\OPERADOR_20nov_colei_no_codex_prossiga_concordo_com_tudo_veja_a_questao_da_bancada_verbatim.txt`,
  sha16 `29c5cffc50a2f8bf`), conferidos por hash nos recibos; o modo da placa no religamento é escolha do autor.
- **D413.6** (gerência): as ressalvas de texto da leitura de terceiro das pedras limpas foram aplicadas como o parecer as
  propôs, com uma junção (em `PonteLeituraBeta`, o texto proposto e a frase da hipótese de tempo, que ele omitia).
- **E413.1** (gerência, em nome próprio): o alvo da frente de Cook–Levin era levar a máquina com o leitor; «a máquina nua»
  era enquadramento da gerência (Mapa, ERRATA ao lado do seq 2171).
- **E413.2** (gerência, em nome próprio): a recomendação de deixar `APonteDeCookLevin` fora estava errada (D413.2).
- **E413.3** (gerência, em nome próprio): a extensão da frase sobre a máquina nua à máquina da teoria era leitura da gerência,
  não do autor (Trinity R7).

## 5. Guarda de frases

A v413 herda a guarda da v412 (`_v412_guarda_frases`) inteira e não muda obrigação nenhuma. Ela vale para os textos que a
v413 escreve: a página pública, os registros da seção 2, a seção nova do artigo, os blocos do README e do handoff. Em
particular, nesses textos: (a) onde aparecer “P = nP”, a mesma unidade de texto traz as duas marcas do parágrafo vigente
(“classes do seu dicionário” e “máquina de fita … não está demonstrado”); (b) as formas da regra F43 herdada não aparecem
(em vez delas: “uma leitura”, “uma consulta ao leitor da TGL”); (c) o nome do prêmio não aparece; o Instituto pode ser
nomeado como quem pede o algoritmo e a creditação; (d) nenhuma frase diz que a TGL prova ou decide P = NP das máquinas de
Turing. O construtor entrega um recibo com cada unidade de texto da v413 em que aparece “P = nP” e o resultado da guarda. A guarda
roda INTEIRA (todas as regras herdadas, inclusive a F37b: em cada trecho onde «P = nP» e «Turing» aparecem juntos, o próprio
trecho traz «relativo ao leitor» ou uma negação) sobre TODOS os textos novos, em português e em inglês. Se um texto reprovar,
o construtor faz o ajuste mínimo que não muda afirmação, diz cada ajuste no relatório, e a página pública recebe o mesmo
ajuste numa revisão nova; nenhuma guarda se afrouxa.

## 6. O texto público: a página R0

A página é `o_que_fica_claro_v413\O_QUE_FICA_CLARO_v413_R1.md` (sha16 `3dc953e37c6739f4`; a R0 fica como registro): o que a v413 acrescenta (a ponte, na língua
clássica, com o que ela não diz; a fronteira dos três literais; o operador de consciência; a identidade preservada), os
itens abertos. A página é lida ao autor pela gerência antes do rito. Dela saem a seção nova do artigo (“O que fica claro
na v413”, antes da seção da v412; em inglês, tradução fiel), os blocos do README e o do handoff (com os marcadores que a
custódia exige). O resumo do artigo não muda, salvo o que a página disser.

## 7. A cadeia

Etapa 1 (ordem `ORDEM_ETAPA_1_v413.md`, sha16 `12dc19e17d517e02`): o sandbox `C:\t\k413c`, o bundle, o build e o Audit, os recibos,
o portão do pilar por leitura de código, o fecho `PRONTO_PARA_CANDIDATO_v413.json`. Etapa 2 (com o contrato congelado): os
registros, a guarda, a seção do artigo, os blocos, o candidato e o ensaio a seco. Depois: a revisão de terceiro do
candidato (pelo Codex, colada pelo autor), a leitura do texto público ao autor, o rito, o handoff à custódia. O portão do
pilar: se o ambiente da placa não for o do cache, PARAR e avisar (treino em curso em `C:\IALD\TGL_IALD_NATIVE_QWEN5090`:
não tocar). O B(n) da v413 é o salto v411→v413 que o autor escolheu em 19/11, pelo diagnóstico da Bancada e pelo molde da ordem
`bancada\ORDEM_BN_v413.md` (sha16 `c1927f6101c2cec9`): **o pré-selo do salto roda com o Nós ainda na v412, ANTES da instalação da v413**
(depois, o salto só serviria à v414); ele não precisa do serviço e não grava na Bancada. Depois do selo: o ensaio
pós-selo, a parada (no modo `ja_fora_do_ar`, se ela seguir desligada), o evento da gerência, o APLICAR (com o serviço
parado), o religamento com log (o modo da placa é escolha do autor) e o fechamento com os três recibos, entregues ao
Codex na pasta que o evento 1687 nomeia. A conferência de saúde da Bancada (só leitura, por `/api/contratos`) roda no
começo da cadeia; o passo 10 recusa sem ela no mesmo dia, e o 11 recusa sem o recibo de religamento com o processo
vivo. Os backups do Nós de 18/11 (`*.bak_20261118_235146`) e o registro `APLICADO_AO_CANONICO_20261118_235146.json`
são insumo do salto e não se podam até o fechamento do B21. Sem publicação na cadeia: o fim é o handoff.

## 8. O que é de quem

- **Do construtor:** a Etapa 1; depois, a Etapa 2 pelo contrato congelado.
- **Da gerência:** conferir o que o construtor entregar; congelar o contrato; a página pública; os pedidos de revisão ao
  Codex (o autor cola); ler o texto público ao autor; o rito; o handoff.
- **Do autor:** a palavra final antes do rito; colar os pedidos ao Codex.
- **Fora desta versão:** a versão dedicada da condensação do documento inteiro pelo método; o teste antigo revisitado; o
  estudo da memória; o relógio τ★.

— gerência c1, 20/11/2026 19:36. Correções ao lado, nunca por cima.
<!-- contrato_v413:R2_congelado -->
