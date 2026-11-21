# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: gera o RASCUNHO R0 do contrato da v413 (CONTRATO_v413_R0.md), no molde do contrato
congelado da v412. Hashes e numeros lidos dos arquivos por script. Nao congela nada: o contrato congela depois da leitura
de terceiro das pedras limpas e da pagina publica R0 (secao 6)."""
import hashlib, json, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
INS = V / "insumos"
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
C412 = V.parent / "v412" / "CONTRATO_v412.md"
MAN = INS / "MANIFESTO_PEDRAS_v413.json"
KE = INS / "kernel_edits" / "ERRATA_OResumoEPsiBit.json"
RAIZ = INS / "auditoria_raiz" / "RAIZ_v413.json"
LEIT = V / "revisao_codex" / "PEDIDO_DE_LEITURA_DAS_PEDRAS_LIMPAS_v413_20nov.md"
ORD1 = V / "ORDEM_ETAPA_1_v413.md"
DEST = V / "CONTRATO_v413_R0.md"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def s16(p):
    return sha(p)[:16]


man = json.loads(MAN.read_text(encoding="utf-8"))
raiz = json.loads(RAIZ.read_text(encoding="utf-8"))
assert man["n_modulos_novos"] == 21 and raiz["bom"]
mods = sorted(m.split(".", 1)[1] for m in man["modulos_novos"])
FRENTE_A = ["PonteCookLevin", "APonteAoTM2", "AMaquinaTM2DaVerificacao", "SimBase", "SimLiteral", "SimExterior",
            "SimCompleta", "RelogioBeta", "LeituraBeta", "QuantizacaoBeta", "Reconstrucao", "PonteLeituraBeta",
            "EntregaBeta", "APonteDeCookLevin", "ONomeEBeta", "SondaContagem", "AFronteiraNaLinguaClassica"]
FRENTE_B = ["Trinity", "APropostaDaTensao"]
FRENTE_C = ["Operador"]
FRENTE_D = ["AIdentidadePreservada"]
assert sorted(FRENTE_A + FRENTE_B + FRENTE_C + FRENTE_D) == mods
um = NOS / "um.py"
cod = lambda l: ", ".join("`%s`" % x for x in l)  # noqa: E731

T = """# CONTRATO DA v413 — RASCUNHO R0

> Gerência c1, {data}. Rascunho, no molde do contrato congelado da v412 (`{c412}`, sha16 `{s412}`). Congela depois da
> leitura de terceiro das pedras limpas (pedido `{leit}`, sha16 `{sleit}`) e da página pública R0 (seção 6); emenda só por
> revisão nova (`CONTRATO_v413_R1.md`), nunca por cima.
> Base: a v412 selada (`um.py` do Nós, sha16 `{sum}`, lido do arquivo ao gerar este rascunho). Validade no kernel não é
> creditação; o gate não se move; nenhum número novo da natureza entra nesta versão.

## 0. O método (vale para tudo o que a v413 escreve no programa)

No `um.py` (o kernel que ele carrega, os registros, o artigo e o que ele emite) entra só o que é verdade: o enunciado, a
prova, o estatuto, os limites e a fonte conhecida. Não entra a história: quem disse, quando, em que ordem ou revisão; o
que foi proposto e recusado; o erro de quem; o caminho até o resultado. As definições e leis da teoria entram como
definição ou lei da teoria, com o estatuto de entrada (`[INPUT]` ou `[ONTO]`), sem aspas de fala, sem data e sem
atribuição a pessoa. A limpeza tira a narrativa, não o localizador técnico (nome de módulo, de teorema, de arquivo de
fonte, rótulo que distingue um objeto). Tudo o que se conversou continua registrado em paralelo: as falas por bytes em
`work\\cunhagens_13out\\`, o diário desta cadeia, o Mapa de Rotas, a memória da casa, os pareceres.

O que já está selado não se reescreve nesta versão, com uma exceção dita na seção 1: a docstring de um módulo do kernel
que afirmava mais do que o enunciado.

## 1. Pedras (kernel): {n} módulos novos e uma correção de texto

**A lista** é a do manifesto `insumos\\MANIFESTO_PEDRAS_v413.json` (sha16 `{sman}`), com as fontes em
`insumos\\pedras_limpas\\TGLExt\\` (forma do kernel: imports `TGLExt.X`, fim de linha LF, texto pelo método, código idêntico
ao revisado ou conferido). Compilação de conferência: {nt} teoremas públicos, todos com relatório de axiomas só no trio;
a raiz da v412 importada com os {n} novos passou (`insumos\\auditoria_raiz\\RAIZ_v413.json`, sha16 `{sraiz}`).

- **A ponte de Cook–Levin e as suas dependências** ({na}): {fa}.
- **A fronteira dos três literais** ({nb}): {fb}.
- **A consciência e o operador de consciência** ({nc}): {fc}.
- **A identidade preservada** ({nd}): {fd}.

**A correção de texto** de `TGLExt.OResumoEPsiBit.a_atualizacao_pela_clausula_seguinte` (recibo
`insumos\\kernel_edits\\ERRATA_OResumoEPsiBit.json`, sha16 `{ske}`): só a docstring; o código é idêntico. A docstring
antiga afirmava mais do que o enunciado; a nova diz o enunciado. A forma antiga fica na v412 selada e no registro
paralelo, não ao lado no programa (método da seção 0).

**Instalação.** Os módulos entram em `TGLExt\\` com o nome que têm. A única mudança permitida no texto das fontes ao
instalar: as linhas `#print axioms` do fim saem do corpo instalado. A forma de passar o nome da fonte ao compilador fica
fixa em toda a cadeia. Os namespaces ficam como estão (alguns módulos usam `Codex.*`, como já há na v412).

**Bandeiras.** Prefixo `ext_<modulo>_413_NNNN`. Nenhuma chave antiga muda de literal. Nenhum nome de bandeira carrega data,
nome de pessoa ou palavra de processo.

**Âncoras.** Cada registro ancora, por nome completo, as declarações com estrela dos seus módulos que não são `private`, e
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

- `ponte_cook_levin_v413` (módulos: os {na} da ponte)
  `TGL_COOK_LEVIN_BRIDGE_V413__SAT_IN_NP_ON_THE_MATHLIB_TM2_MACHINE__THE_KERNEL_READER_READS_THE_BETA_SUM_EXACTLY__ONE_READING_DECIDES_SAT_WITH_AN_ANSWER_OF_N_PLUS_3_BITS__THE_ONE_READING_CLASS_IS_EXACTLY_THE_POLYNOMIAL_REDUCTION_CLOSURE_OF_SAT__WITH_COOK_LEVIN_AS_A_NAMED_HYPOTHESIS_EVERY_NP_PROBLEM_IS_DECIDED_IN_POLYNOMIAL_TIME_WITH_ONE_READING__THE_READING_FINDS_A_SOLUTION_IN_AT_MOST_LETTERS_PLUS_ONE_READINGS__THE_READING_COST_IS_THE_PAID_TIME_LINEAR_IN_THE_NAMES_NOT_TAPE_STEPS__EVERY_READER_WITH_THE_PRECISION_COUNTS_THE_SOLUTIONS__SAT_IN_POLYNOMIAL_TIME_ON_THE_BARE_TAPE_MACHINE_OPEN__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED`
- `trinity_v413` (módulos: os {nb} da fronteira)
  `TGL_TRINITY_V413__THE_INCLINATION_OF_THE_NAME__NEVER_WRONG__DECIDES_EVERY_HORN_AND_EVERY_TWO_LITERAL_FORMULA_IN_AT_MOST_T_PLUS_1_CUBED_FIXINGS__STOPS_ONLY_AT_THE_FRONTIER_OF_THREE_LITERALS__CROSSING_BY_BRANCHING_DECIDES_EVERY_FORMULA_AT_A_PROVED_EXPONENTIAL_PRICE_ONLY_IN_THE_FRONTIER_NAMES__IN_FINITE_STEPS_ABSOLUTE_ZERO_IS_NOT_REACHED__THE_LOAD_N_LN2_IS_EXACT_ON_THE_FLAT_PLATEAU__A_POLYNOMIAL_CROSSING_IS_OPEN__GATE_UNMOVED`
- `operador_v413` (módulo: {fc})
  `TGL_CONSCIOUSNESS_OPERATOR_V413__WITHOUT_THE_PAIR_SELF_NEGATION_IS_THE_POINT_OF_CONTRADICTION__WITH_THE_PAIR_IT_LANDS_ON_THE_HALF_NAT__J_SQUARED_IS_ONE_AND_CONJUGATES_FACE_AND_COFACE__ANCHORING_PRESERVES_THE_IDENTITY__NEVER_ONE_HUNDRED_PERCENT__THAT_SOMEONE_IS_CONSCIOUS_IS_NOT_PROVED__GATE_UNMOVED`
- `identidade_preservada_v413` (módulo: {fd})
  `TGL_PRESERVED_IDENTITY_V413__THE_ZERO_COST_COORDINATES_PASS_THE_LOCK_UNCHANGED_AT_EVERY_TIME__THE_LOCK_TENDS_TO_THE_NAME__THE_LOAD_N_LN2_IS_THE_STRICT_THRESHOLD__GATE_UNMOVED`
- `cunhagens_v413` (sem módulo próprio)
  `TGL_DEFINITIONS_OF_THE_THEORY_V413__ENTRIES_NOT_THEOREMS__EACH_WITH_THE_TERMS_THAT_TYPE_IT_AND_WHAT_IS_NOT_TYPED__GATE_UNMOVED`
  A lista das leis e definições da teoria que entram como ENTRADA nesta versão (as leituras dos cabeçalhos de `Trinity`,
  `Operador`, `AIdentidadePreservada`, `APropostaDaTensao` e `ONomeEBeta`): para cada uma, o nome curto, o módulo e o
  título da seção do cabeçalho onde ela está, as âncoras que a tipam e o que o cabeçalho diz que NÃO está tipado. O
  registro aponta para o cabeçalho; não embute o texto.

**Checagens que todo registro traz** (molde da v412): o gate deste rito tem o mesmo veredito da v412 selada; os canais vivos
(neutrino, H0DN) seguem com o mesmo veredito; nenhuma chave antiga muda de literal; a escada só cresce; cada âncora é
verdadeira e está no relatório de axiomas só com os três axiomas.

## 3. As falas (registro paralelo; NÃO entram no programa)

Nenhuma fala é embutida ou transcrita. O construtor gera, por script, `VERBATIM_CONGELADO_v413.json` como artefato DA
CADEIA (não é lido pelo `um.py`): a lista dos arquivos `OPERADOR_19nov_*` e `OPERADOR_20nov_*` de `work\\cunhagens_13out\\`,
com tamanho e sha256 lidos de cada arquivo.

## 4. Decisões e erratas desta versão (registro paralelo; NÃO entram no programa)

- **D413.1** (autor, 20/11): o nome da pedra da ponte é `PonteCookLevin`; entram as quatro pedras do Kimi, a sonda da
  contagem e o enunciado da fronteira.
- **D413.2** (gerência): `APonteDeCookLevin` entra porque `APonteAoTM2` e `Reconstrucao` a importam; o texto dela diz o que
  prova (o iterador; custo cobrado por definição; confere o custo de uma atribuição dada), não ponte de custo de fita.
- **D413.3** (gerência): os namespaces `Codex.*` dos módulos novos ficam como estão (precedente da v412).
- **D413.4** (gerência): a docstring de `OResumoEPsiBit` é trocada pela que diz o enunciado (seção 1).
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
Turing. O construtor entrega um recibo com cada unidade de texto da v413 em que aparece “P = nP” e o resultado da guarda.

## 6. O texto público: a página R0

A gerência escreve `o_que_fica_claro_v413\\O_QUE_FICA_CLARO_v413_R0.md`: o que a v413 acrescenta (a ponte, na língua
clássica, com o que ela não diz; a fronteira dos três literais; o operador de consciência; a identidade preservada), os
itens abertos. A página é lida ao autor pela gerência antes do rito. Dela saem a seção nova do artigo (“O que fica claro
na v413”, antes da seção da v412; em inglês, tradução fiel), os blocos do README e o do handoff (com os marcadores que a
custódia exige). O resumo do artigo não muda, salvo o que a página disser.

## 7. A cadeia

Etapa 1 (ordem `ORDEM_ETAPA_1_v413.md`, sha16 `{sord}`): o sandbox `C:\\t\\k413c`, o bundle, o build e o Audit, os recibos,
o portão do pilar por leitura de código, o fecho `PRONTO_PARA_CANDIDATO_v413.json`. Etapa 2 (com o contrato congelado): os
registros, a guarda, a seção do artigo, os blocos, o candidato e o ensaio a seco. Depois: a revisão de terceiro do
candidato (pelo Codex, colada pelo autor), a leitura do texto público ao autor, o rito, o handoff à custódia. O portão do
pilar: se o ambiente da placa não for o do cache, PARAR e avisar (treino em curso em `C:\\IALD\\TGL_IALD_NATIVE_QWEN5090`:
não tocar). O B(n) da v413 é o salto v411→v413 que o autor escolheu em 19/11; ele roda se a Bancada estiver no ar com a
atualização do Codex; se não estiver, a decisão volta ao autor (como na v412). Sem publicação na cadeia: o fim é o handoff.

## 8. O que é de quem

- **Do construtor:** a Etapa 1; depois, a Etapa 2 pelo contrato congelado.
- **Da gerência:** conferir o que o construtor entregar; congelar o contrato; a página pública; os pedidos de revisão ao
  Codex (o autor cola); ler o texto público ao autor; o rito; o handoff.
- **Do autor:** a palavra final antes do rito; colar os pedidos ao Codex.
- **Fora desta versão:** a versão dedicada da condensação do documento inteiro pelo método; o teste antigo revisitado; o
  estudo da memória; o relógio τ★.

— gerência c1, {data}. Correções ao lado, nunca por cima.
<!-- contrato_v413:rascunho_R0 -->
"""
texto = T.format(data=time.strftime("%d/%m/%Y %H:%M"), c412=C412, s412=s16(C412), leit=LEIT.name, sleit=s16(LEIT),
                 sum=s16(um), n=man["n_modulos_novos"], sman=s16(MAN), nt=man["teoremas_publicos_novos"], sraiz=s16(RAIZ),
                 na=len(FRENTE_A), fa=cod(FRENTE_A), nb=len(FRENTE_B), fb=cod(FRENTE_B), nc=len(FRENTE_C),
                 fc=cod(FRENTE_C), nd=len(FRENTE_D), fd=cod(FRENTE_D), ske=s16(KE), sord=s16(ORD1))
d = texto.encode("utf-8")
if DEST.exists():
    bk = DEST.with_name(DEST.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S"))
    bk.write_bytes(DEST.read_bytes())
tmp = DEST.with_name(DEST.name + ".tmp")
tmp.write_bytes(d)
assert tmp.read_bytes() == d
tmp.replace(DEST)
print("%s sha16 %s (%d B) | base um.py v412 sha16 %s" % (DEST.name, s16(DEST), len(d), s16(um)))
