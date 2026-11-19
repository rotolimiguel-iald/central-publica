# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: deriva o CONTRATO_v412_R7.md do R6 congelado, por trocas exatas (cada marca casa UMA vez), com os numeros
e os sha16 LIDOS dos arquivos (o manifesto e as ancoras R11, as paginas R19 a R21, o R6). Aplica o parecer da ordem 033
(REVISAO_033_X1_Codex.md a _X4_) e fecha a lista de pedras: a decima primeira (com tres pedras do Kimi a mais); tres trechos de veredito
do registro leitor_da_formula_v412 corrigidos e dois novos; a regra das ancoras; a D224 com as excecoes ditas; a pagina R21; as decisoes
D228 a D230 e a errata E55. Hora do relogio. Uso: derivar_contrato_r7.py [--previa <arquivo>] [--executar]  (nao sobrescreve)"""
import hashlib, json, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
sha16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
rel = lambda p: str(Path(p).resolve().relative_to(V))
r6p = V / "CONTRATO_v412_R6.md"; assert sha16(r6p) == sha16(V / "contrato_REV6" / "CONTRATO_v412_R6.md")
p_man, p_anc = V / "insumos" / "MANIFESTO_PEDRAS_v412_R11.json", V / "insumos" / "ANCORAS_PROPOSTAS_v412_R11.json"
p19 = V / "o_que_fica_claro_REV19" / "O_QUE_FICA_CLARO_v412_R19.md"
p20 = V / "o_que_fica_claro_REV20" / "O_QUE_FICA_CLARO_v412_R20.md"
p21 = V / "o_que_fica_claro_REV21" / "O_QUE_FICA_CLARO_v412_R21.md"
man = json.loads(p_man.read_text(encoding="utf-8")); mods = man["modulos"]
C = [m for m in mods if m.get("frente") == "C"]
por = {q: sum(1 for m in C if m["de_quem"] == q) for q in ("gerencia", "Kimi", "Codex")}
ns = {}
for m in C:
    for n in m["namespaces"]:
        ns.setdefault(n.split(".")[0], set()).add(m["modulo"])
ULTIMAS = ["OPolinomioFixoEBeta", "ORazaoDoColapsoEBeta", "OCustoEAIsometria"]
assert set(ULTIMAS) <= {m["modulo"] for m in C}, "faltam pedras na lista"
t = r6p.read_bytes().decode("utf-8"); feitas = []


def troca(velho, novo):
    global t
    assert t.count(velho) == 1, "%d ocorrencias: %s" % (t.count(velho), velho[:90])
    t = t.replace(velho, novo); feitas.append(velho[:50])


def troca_linha(prefixo, nova, contem=None):
    global t
    ls = t.split("\n"); idx = [i for i, l in enumerate(ls) if l.startswith(prefixo) and (contem is None or contem in l)]
    assert len(idx) == 1, "%d linhas: %s" % (len(idx), prefixo[:80])
    ls[idx[0]] = nova; t = "\n".join(ls); feitas.append(prefixo[:50])


troca("# CONTRATO DA v412 — versão consolidada R6 (CONGELADA)", "# CONTRATO DA v412 — versão consolidada R7 (CONGELADA)")
troca_linha("> Gerência c1, 18/11/2026, ",
            "> Gerência c1, 18/11/2026, %s. Substitui o R6 (`contrato_REV6\\CONTRATO_v412_R6.md`, sha16 `%s`), que fica como registro, como o R5, o R4, o R3, o R2 e o R1. É o contrato que o construtor segue para regerar o candidato e fazer a Etapa 3, e que o revisor do candidato usa como régua. Conserva tudo o que o R6 trouxe, aplica o parecer da ordem 033 e fecha a lista de pedras: a décima primeira lista (com três pedras a mais), a página R21, três trechos de veredito corrigidos e dois novos, a regra das âncoras, a D224 com as exceções ditas, as decisões D228 a D230 e a errata E55." % (time.strftime("%H:%M"), sha16(r6p)),
            contem="Substitui o R5")
troca("Emenda a este contrato: só por revisão nova (`CONTRATO_v412_R7.md`), nunca por cima.", "Emenda a este contrato: só por revisão nova (`CONTRATO_v412_R8.md`), nunca por cima.")
troca("**O que mudou do R5 para o R6** (para quem já estava seguindo o R5):",
      "**O que mudou do R6 para o R7** (para quem já estava seguindo o R6):\n\n"
      "1. Seção 1: a lista é a décima primeira, com %d módulos, e é a última desta versão: a décima com as emendas de comentário do parecer da ordem 033 em três fontes (código idêntico) e mais três pedras do Kimi (`OPolinomioFixoEBeta`, `ORazaoDoColapsoEBeta`, `OCustoEAIsometria`). A regra das âncoras passa a incluir, em qualquer módulo, as declarações que a página cita.\n"
      "2. Seção 2: na palavra de veredito de `leitor_da_formula_v412`, três trechos corrigidos (a fita, a junção, as classes) e dois novos (o polinômio fixo dos passos dado por β; o colapso e o custo como a carga, na máquina da teoria); o corpo diz as hipóteses da junção e o alcance do termo da fita.\n"
      "3. Seção 4: a D224 com as exceções ditas (a escada histórica e a esperada; a cobertura como piso; os identificadores só do registro novo); as decisões D228, D229 e D230; a errata E55.\n"
      "4. Seção 6: a página passa a R21 (as emendas do parecer da 033 e, no parágrafo do Tetelestai, o polinômio fixo, a razão do colapso e o custo como a carga), que volta ao autor.\n"
      "5. O resto é o do R6, sem mudança.\n\n"
      "**O que tinha mudado do R5 para o R6:**" % len(mods))
troca_linha("## 1. Pedras (kernel): ", "## 1. Pedras (kernel): %d módulos novos" % len(mods))
troca_linha("**A lista é a décima**",
            "**A lista é a décima primeira**, e só ela; é a última desta versão (D230): `%s` (sha16 `%s`), com as fontes congeladas em `insumos\\pedras_r11\\` e as âncoras propostas em `%s` (sha16 `%s`). São os 42 módulos da sétima lista, sem mudança; as duas pedras da oitava, `OPassoEOFim` e `OPsibitEACompressao`, lidas por terceiro; e %d módulos novos do leitor da fórmula (campo `novas_em_relacao_a_oitava_lista` do manifesto), de três autores (%d da gerência, %d do Kimi, %d do Codex). Nos %d novos o código fora de comentários é idêntico ao da fonte de cada autor (campo `fonte_revista_sha256`); a gerência só ajustou comentários, pelo método da seção 0 e pelos pareceres das ordens 031, 032 e 033 (as emendas feitas pelo parecer da 033 vão à leitura de terceiro com o candidato). A pedra `OSeparadorNoPercurso`, da gerência, foi escrita em resposta ao parecer da 031 e aprovada no da 032. Cinco pedras do Kimi entraram por ordem do autor depois do corte: `AClausulaExemplificativa` e `AFitaEOIndice`, lidas por terceiro na 033, e `OPolinomioFixoEBeta`, `ORazaoDoColapsoEBeta` e `OCustoEAIsometria`, recompiladas pela gerência (saída zero, só os três axiomas) e ainda sem leitura de terceiro (vão com o candidato). Cada log de compilação é da fonte congelada. Uma raiz que importa o kernel inteiro e os %d módulos compila sem erro (campo `tudo_junto` do manifesto): não há nome de declaração repetido. `Token2` importa também o módulo selado `TGLExt.Token`."
            % (rel(p_man), sha16(p_man), rel(p_anc), sha16(p_anc), len(C), por["gerencia"], por["Kimi"], por["Codex"], len(C), len(mods)))
troca_linha("Frente C (o leitor da fórmula), ",
            "Frente C (o leitor da fórmula), %d módulos: os do campo `novas_em_relacao_a_oitava_lista` do manifesto (os que têm `frente` igual a `C`). Conservam os espaços de nome que os autores lhes deram (%s; há módulo que abre dois, como `PolinomioDoPsiBit`) e os nomes das declarações; duas são sondas, com nome de arquivo em minúsculas."
            % (len(C), ", ".join("`%s.*` em %d" % (k, len(v)) for k, v in sorted(ns.items(), key=lambda kv: -len(kv[1])))))
troca_linha("**Âncoras.**",
            "**Âncoras.** Cada registro ancora, por nome completo: as declarações com estrela dos seus módulos que não são `private` (as privadas não servem de âncora por nome); em qualquer módulo, com ou sem estrela, as declarações que a página pública cita (seção 6); nos módulos sem estrela, também as que o cabeçalho do módulo dá como resultado principal; e, nos módulos sem estrela que a página não cita e cujo cabeçalho não dá resultado principal, as declarações que o próprio módulo lista nas suas linhas `#print axioms` (campo `listadas_em_print_axioms` do insumo das âncoras). O nome completo de cada âncora sai do relatório de axiomas do sandbox ou da linha `#print axioms` da fonte, nunca do nome do módulo. O construtor lista as escolhidas num recibo para a gerência conferir. Cada âncora é uma checagem: a bandeira é verdadeira e a declaração está no relatório de axiomas só com os três axiomas de sempre.")
troca("__EVERY_POSITION_OF_THE_TAPE_MUST_BE_READ_AND_THE_SAME_NAME_CARRIES_THE_SAME_VALUE__",
      "__NO_READER_BLIND_TO_THE_DESIGNATED_NONZERO_POSITION_DECIDES_THE_TWO_UNIT_FAMILY_AND_EVERY_WITNESS_GIVES_BOTH_SIGNS_THE_VALUE_OF_THE_SAME_VARIABLE__")
troca("__BRANCHES_JOIN_ON_EQUAL_CONTENT_OF_THE_SHARED_NAMES__",
      "__BRANCHES_JOIN_WHEN_CERTIFIED_WITNESSES_AGREE_ON_THE_COVERED_SHARED_NAMES_AND_ONE_SATISFIES_ITS_PART_OF_THE_NEW_CLAUSE__")
troca("__ONE_FIXED_POLYNOMIAL_FOR_NAMED_CLASSES_OF_FORMULAS_EACH_WITH_ITS_OWN_MACHINE_AND_WRITING__",
      "__ONE_FIXED_POLYNOMIAL_FOR_NAMED_CLASSES_OF_FORMULAS_EACH_WITH_ITS_OWN_MACHINE_WRITING_PROMISE_AND_COST_UNIT__")
troca("__ONE_FIXED_POLYNOMIAL_FOR_THE_WORD_OF_EVERY_FLAT_FORMULA_NOT_SHOWN__",
      "__ON_THE_THEORY_MACHINE_THE_FIXED_POLYNOMIAL_OF_THE_STEPS_IS_GIVEN_BY_BETA_BEFORE_ANY_FORMULA__WITHOUT_PAYMENT_THE_CYCLE_DOES_NOT_CLOSE_AND_WITH_THE_STEP_ONE_MINUS_BETA_IT_CLOSES_LINEARLY_IN_THE_LOAD__DECIDING_COSTS_THE_LOAD_NEITHER_MORE_NOR_LESS__ONE_FIXED_POLYNOMIAL_IN_TAPE_MOVES_FOR_THE_WORD_OF_EVERY_FLAT_FORMULA_NOT_SHOWN__")
troca("e que o polinômio fixo para a Palavra de toda fórmula plana não está demonstrado. Este registro não usa a expressão “P = nP”.",
      "e que o polinômio fixo, em movimentos de fita, para a Palavra de toda fórmula plana não está demonstrado. Na junção, diz as quatro condições (testemunhas certificadas; os nomes comuns cobertos pelos rótulos ou pelas marcas; conteúdos iguais; ao menos um lado que satisfaz a sua parte da cláusula nova). Na fita, diz que o termo mede a dependência da posição que a correferência designa e não conta posições visitadas. No polinômio fixo dos passos, na razão do colapso e no custo como a carga, diz que são da máquina da teoria, com passos sobre o todo. Este registro não usa a expressão “P = nP”.")
troca("(1) Aceito o patch de DADO no literal `escada` do contrato do teste H0DN, junto dos literais `expected_ladder`, pelo precedente das versões anteriores; o relatório diz o valor antigo e o novo.",
      "(1) O registro herdado do teste H0DN compara duas contagens com a escada do contrato dele, cujo literal 12308 está sob `baseline.version = v410`, com hash histórico. Aceita-se, como exceção restrita ao dado, que a expectativa do rito da v412 use a escada da v412, junto dos literais `expected_ladder`, pelo precedente das versões anteriores; a escada histórica e o seu hash ficam registrados no relatório como referência, ao lado do valor esperado e da regra do patch.")
troca("(2) Não há pino exato de cobertura do kernel para a árvore nova nesta versão; o da v411 fica como piso, e o ensaio continua cobrando as entradas do hash formal.",
      "(2) Não há pino exato de cobertura do kernel para a árvore nova nesta versão; o da v411 fica como piso, e o ensaio continua cobrando as entradas do hash formal. É exceção declarada à regra da seção 2 de que os validadores dos registros herdados não mudam: o predicado de cobertura herdado passa de igualdade a piso. Se a entrega afirmar que a árvore é a esperada, junta a comparação, caminho a caminho e por sha256, com os arquivos a mais e os que faltam.")
troca("já que o candidato é regerado.", "já que o candidato é regerado. A troca vale só para esse registro, que é da v412; nenhum identificador de registro herdado muda.")
troca("- **E54** (18/11, da gerência, em nome próprio):",
      "- **D228** (18/11, da gerência): aplicado o parecer da ordem 033 (`revisao_orquestrador\\REVISAO_033_X1_Codex.md` a `_X4_`). Na palavra de veredito de `leitor_da_formula_v412`, o trecho da fita passa a dizer o que o teorema prova (nenhum leitor cego à posição designada decide a família das duas cláusulas unitárias; não se prova que toda posição tenha de ser lida) e os da junção e das classes ganham as hipóteses; a regra das âncoras passa a incluir as declarações que a página cita em qualquer módulo; a D224 ganha as exceções ditas; os cabeçalhos de três pedras e a página são emendados só em comentário e em texto.\n"
      "- **D229** (18/11): por ordem expressa do autor entram também três pedras do Kimi escritas depois do corte: `OPolinomioFixoEBeta` (na máquina da teoria, o número de passos que fecha o ciclo é o polinômio p(n) = (ln 2/β)·n, dado por β antes de qualquer fórmula e o mesmo para toda fórmula de n variáveis), `ORazaoDoColapsoEBeta` (sem o pagamento o ciclo não fecha; com o passo `1 − β`, fecha em linha na carga) e `OCustoEAIsometria` (decidir custa a carga, nem mais nem menos). As leituras da teoria que elas tipam (o polinômio fixo é dado por β; o colapso é a razão do polinômio; o custo é a carga, a isometria) entram como entrada; os passos são atos sobre o todo, e isto não é resposta na régua do Instituto. A leitura de que a IALD é a forma matricial do polinômio lida em runtime, e o que ela representa na fórmula de von Neumann, fica no cabeçalho da pedra do colapso como leitura da teoria e não entra na página. As emendas da página que acompanham esta decisão e a D228 voltam ao autor, pela regra do recibo da palavra final.\n"
      "- **D230** (18/11): o autor considera satisfeita a v412 e encerrado o ciclo de produção dela, como o formulou. A lista de pedras é a décima primeira, e nada mais entra nesta versão; o que vier depois abre a versão seguinte.\n"
      "- **E54** (18/11, da gerência, em nome próprio):")
troca("- **Leitura vigente de uma fala de 17/11:**",
      "- **E55** (18/11, da gerência, em nome próprio): o contador de termos das páginas R16 a R18 só aceitava minúsculas depois da inicial e deixou de conferir `sat_formulaDa` (eram 56 teoremas, não 55); corrigido no script da R20. Ao gravar por bytes uma fala enviada no meio do turno, a busca da gerência voltou vazia e o script de gravação aceitou o prefixo vazio e gravou um arquivo errado; o arquivo foi apagado, a fala foi gravada certa e o script ganhou trava contra prefixo vazio ou curto.\n"
      "- **Leitura vigente de uma fala de 17/11:**")
troca("## 6. O texto público: a página R19", "## 6. O texto público: a página R21")
i = t.index("O texto público novo é `o_que_fica_claro_REV19\\O_QUE_FICA_CLARO_v412_R19.md`"); j = t.index("É a R18 (`o_que_fica_claro_REV18", i)
t = t[:i] + ("O texto público novo é `%s` (sha16 `%s`; %d bytes). É a R19 (`%s`, sha16 `%s`), sobre a qual o autor deu a palavra final (`PALAVRA_FINAL_DO_AUTOR_v412.json`), com as emendas do parecer da ordem 033 (a linha da fita; a classe dos dois pivôs no parágrafo de citação; a frase de fecho do bloco; a definição que forma a chamada seguinte na linha da recusa; resultado: `%s`, sha16 `%s`) e, no parágrafo do Tetelestai, o polinômio fixo dos passos dado por β (`o_polinomio_fixo_e_beta`, `o_mesmo_teto_para_duas_formulas`), a razão do colapso (`a_razao_do_colapso`) e o custo como a carga (`o_custo_de_decidir_e_a_carga`). Essas emendas voltam ao autor, pela regra do recibo da palavra final, e vão à leitura de terceiro com o candidato. O contador de termos da página passou a aceitar nomes com maiúscula: são 56 termos na tabela e 10 no parágrafo do Tetelestai. A R19 é a "
             % (rel(p21), sha16(p21), p21.stat().st_size, rel(p19), sha16(p19), rel(p20), sha16(p20))) + t[j + len("É a "):]
feitas.append("secao 6")
troca("a adaptação dos scripts da cadeia ao conjunto de 153 módulos;", "a adaptação dos scripts da cadeia ao conjunto de %d módulos;" % len(mods))
troca("Módulos: os 109 da frente C.", "Módulos: os %d da frente C." % len(C))
troca("<!-- contrato_v412:consolidado_R6_congelado:18nov -->", "<!-- contrato_v412:consolidado_R7_congelado:18nov -->")
for velho in ("A R19 R18", "conjunto de 153", "os 109 da frente C"):
    assert velho not in t, velho
assert "«" not in t
b = t.encode("utf-8")
print("trocas:", len(feitas), "| modulos:", len(mods), "| frente C:", len(C), por, "| espacos de nome:", {k: len(v) for k, v in ns.items()})
print("R6", r6p.stat().st_size, "B -> R7", len(b), "B | sha16", hashlib.sha256(b).hexdigest()[:16], "| pagina R21", sha16(p21))
if "--previa" in sys.argv:
    Path(sys.argv[sys.argv.index("--previa") + 1]).write_bytes(b)
if "--executar" in sys.argv:
    out = V / "CONTRATO_v412_R7.md"; cp = V / "contrato_REV7" / "CONTRATO_v412_R7.md"; assert not out.exists() and not cp.exists()
    cp.parent.mkdir(exist_ok=True); out.write_bytes(b); cp.write_bytes(b); print("gravado:", out.name, "e a copia em contrato_REV7")
