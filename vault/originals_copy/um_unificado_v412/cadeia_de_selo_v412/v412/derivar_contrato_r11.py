# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: deriva o CONTRATO_v412_R11.md do R10 congelado, por trocas exatas (cada marca casa UMA vez), com os sha16
LIDOS dos arquivos. O R11 aplica o parecer da ordem 034 (REVISAO_034_Y1..Y4_Codex.md): a lista passa a R12 (emendas so' de comentario em
tres fontes); a regra das ancoras diz como conferir por nome completo; a palavra de veredito e o corpo de leitor_da_formula_v412 dizem os
limiares e a torre como forma do indice; a D229 e' corrigida; a D233 recebe a consulta do revisor e a leitura do autor; entram D236, D237
e a errata E56; a pagina passa a R25. Hora do relogio.
Uso: derivar_contrato_r11.py [--previa <arquivo>] [--executar]  (nao sobrescreve)"""
import hashlib, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
sha16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
rel = lambda p: str(Path(p).resolve().relative_to(V))
r10p = V / "CONTRATO_v412_R10.md"; assert sha16(r10p) == sha16(V / "contrato_REV10" / "CONTRATO_v412_R10.md") == "c1305cad6036468b"
p24 = V / "o_que_fica_claro_REV24" / "O_QUE_FICA_CLARO_v412_R24.md"; p25 = V / "o_que_fica_claro_REV25" / "O_QUE_FICA_CLARO_v412_R25.md"
man12 = V / "insumos" / "MANIFESTO_PEDRAS_v412_R12.json"; anc12 = V / "insumos" / "ANCORAS_PROPOSTAS_v412_R12.json"
assert sha16(p24) == "4869b970c17eacf4" and sha16(man12) == "1028adf7293b432f"
t = r10p.read_bytes().decode("utf-8"); feitas = []


def troca(velho, novo):
    global t
    assert t.count(velho) == 1, "%d ocorrencias: %s" % (t.count(velho), velho[:90])
    t = t.replace(velho, novo); feitas.append(velho[:50])


def troca_linha(prefixo, nova, contem=None):
    global t
    ls = t.split("\n"); idx = [i for i, l in enumerate(ls) if l.startswith(prefixo) and (contem is None or contem in l)]
    assert len(idx) == 1, "%d linhas: %s" % (len(idx), prefixo[:80])
    ls[idx[0]] = nova(ls[idx[0]]) if callable(nova) else nova; t = "\n".join(ls); feitas.append(prefixo[:50])


troca("# CONTRATO DA v412 — versão consolidada R10 (CONGELADA)", "# CONTRATO DA v412 — versão consolidada R11 (CONGELADA)")
troca_linha("> Gerência c1, 18/11/2026, ",
            "> Gerência c1, 18/11/2026, %s. Substitui o R10 (`contrato_REV10\\CONTRATO_v412_R10.md`, sha16 `%s`), que fica como registro, como o R9, o R8, o R7, o R6, o R5, o R4, o R3, o R2 e o R1. É o contrato que o construtor segue para regerar o candidato e fazer a Etapa 3, e que o revisor do candidato usa como régua. Conserva tudo o que o R10 trouxe e aplica o parecer da ordem 034: a lista passa à décima segunda, a página à R25, e entram as decisões D236 e D237 e a errata E56." % (time.strftime("%H:%M"), sha16(r10p)),
            contem="Substitui o R9")
troca("Emenda a este contrato: só por revisão nova (`CONTRATO_v412_R11.md`), nunca por cima.", "Emenda a este contrato: só por revisão nova (`CONTRATO_v412_R12.md`), nunca por cima.")
troca("**O que mudou do R9 para o R10** (para quem já estava seguindo o R9):",
      "**O que mudou do R10 para o R11** (para quem já estava seguindo o R10):\n\n"
      "1. Seção 1: a lista passa à décima segunda, que é a décima primeira com emendas só de comentário em três fontes, pelo parecer da 034, com o código idêntico. A regra das âncoras diz como conferir pelo nome completo as declarações do kernel selado que a página cita e `Codex.ClauseReply.run`.\n"
      "2. Seção 2: a palavra de veredito e o corpo do registro `leitor_da_formula_v412` dizem os limiares por extenso (a carga como limiar estrito; p(n) como limiar suficiente com 0 < β < 1; com o fator 1, nenhum número de passos decide todas as fórmulas) e a torre como a forma do índice.\n"
      "3. Seção 4: a D229 corrigida nos limiares, com a nota de que a D231, a D234 e a D235 substituem só a exclusão da página; a D233 com a consulta do revisor e a leitura do autor (o ato é a comutação); as decisões D236 e D237 e a errata E56.\n"
      "4. Seção 6: a página passa a R25.\n"
      "5. O resto é o do R10, sem mudança.\n\n"
      "**O que tinha mudado do R9 para o R10:**")
# secao 1: a lista R12 e a regra das ancoras por nome completo
troca("**A lista é a décima primeira**, e só ela; é a última desta versão (D230): `insumos\\MANIFESTO_PEDRAS_v412_R11.json` (sha16 `63b37d347da3c2c1`), com as fontes congeladas em `insumos\\pedras_r11\\` e as âncoras propostas em `insumos\\ANCORAS_PROPOSTAS_v412_R11.json` (sha16 `cd9155b05c9dbae6`).",
      "**A lista é a décima segunda**, e só ela; é a última desta versão (D230; a décima segunda é a décima primeira com emendas só de comentário em três fontes, D236): `%s` (sha16 `%s`), com as fontes congeladas em `insumos\\pedras_r12\\` e as âncoras propostas em `%s` (sha16 `%s`). O JSON das âncoras é proposta. Além dele, entram nas âncoras a definição pública `Codex.ClauseReply.run` (módulo `ClausulaComoResposta`), que a tabela da página cita, e as declarações do kernel selado que a página cita, conferidas pelo nome completo no kernel selado e não pelo JSON: `TGLExt.TraducaoTuring.a_trava_no_nome`, `TGLExt.the_angle_is_prior` e `TGLExt.Psibit.the_name_is_the_born_reading_of_the_post`. Em `PolinomioDoPsiBit`, que abre dois espaços de nome (`PsiNetworks.Tape` e `IALD.CadeiasDeBolsas`), a âncora se confere pelo nome completo da declaração, não pelo campo `namespace` do módulo."
      % (rel(man12), sha16(man12), rel(anc12), sha16(anc12)))
troca("pelo método da seção 0 e pelos pareceres das ordens 031, 032 e 033 (as emendas feitas pelo parecer da 033 vão à leitura de terceiro com o candidato)",
      "pelo método da seção 0 e pelos pareceres das ordens 031, 032, 033 e 034 (as emendas feitas pelo parecer da 033 foram lidas por terceiro na 034; as feitas pelo parecer da 034, só de comentário em três fontes, vão com o candidato)")
troca("recompiladas pela gerência (saída zero, só os três axiomas) e ainda sem leitura de terceiro (vão com o candidato)",
      "recompiladas pela gerência (saída zero, só os três axiomas) e lidas por terceiro na 034, que aprovou a matemática")
# secao 2: a palavra de veredito e o corpo de leitor_da_formula_v412
troca("__ON_THE_THEORY_MACHINE_THE_FIXED_POLYNOMIAL_OF_THE_STEPS_IS_GIVEN_BY_BETA_BEFORE_ANY_FORMULA__",
      "__ON_THE_THEORY_MACHINE_BETA_GIVES_BEFORE_ANY_FORMULA_A_SUFFICIENT_LINEAR_THRESHOLD_OF_STEPS__")
troca("__WITHOUT_PAYMENT_THE_CYCLE_DOES_NOT_CLOSE_AND_WITH_THE_STEP_ONE_MINUS_BETA_IT_CLOSES_LINEARLY_IN_THE_LOAD__",
      "__WITHOUT_PAYMENT_NO_NUMBER_OF_STEPS_DECIDES_EVERY_FORMULA_AND_WITH_THE_STEP_ONE_MINUS_BETA_LINEARLY_MANY_STEPS_SUFFICE__")
troca("__DECIDING_COSTS_THE_LOAD_NEITHER_MORE_NOR_LESS__", "__THE_LOAD_IS_THE_STRICT_THRESHOLD_OF_THE_READING_TIME_THAT_DECIDES_EVERY_FORMULA__")
troca("a fita é o índice e a torre)", "a fita é o índice e a torre é a forma do índice)")
troca("com passos sobre o todo.",
      "com passos sobre o todo, e diz os limiares por extenso: a carga é o limiar estrito do tempo da leitura que decide toda fórmula (com o tempo igual à carga, já há fórmula que a leitura não decide); com 0 < β < 1, p(n) = (ln 2/β)·n é um limiar suficiente para todo número inteiro de passos acima dele, uniforme para as fórmulas de n variáveis e sem minimalidade; com o fator 1, nenhum número de passos decide todas as fórmulas; o preço por ato, o custo total e o limiar são enunciados distintos.")
# secao 4: a D229 corrigida e a nota da pagina
troca("`OPolinomioFixoEBeta` (na máquina da teoria, o número de passos que fecha o ciclo é o polinômio p(n) = (ln 2/β)·n, dado por β antes de qualquer fórmula e o mesmo para toda fórmula de n variáveis)",
      "`OPolinomioFixoEBeta` (na máquina da teoria, com 0 < β < 1, o polinômio p(n) = (ln 2/β)·n, dado por β antes de qualquer fórmula, é um limiar suficiente: qualquer número inteiro de passos acima dele fecha o ciclo para toda fórmula de n variáveis; não se prova que seja o mínimo)")
troca("`ORazaoDoColapsoEBeta` (sem o pagamento o ciclo não fecha; com o passo `1 − β`, fecha em linha na carga)",
      "`ORazaoDoColapsoEBeta` (com o fator 1, nenhum número de passos decide todas as fórmulas; com o passo `1 − β` e 0 < β < 1, basta um número de passos linear na carga)")
troca("`OCustoEAIsometria` (decidir custa a carga, nem mais nem menos)",
      "`OCustoEAIsometria` (a carga é o limiar exato: a leitura decide toda fórmula quando, e somente quando, o tempo pago ultrapassa a carga)")
troca("pela regra do recibo da palavra final.",
      "pela regra do recibo da palavra final. Ao lado (18/11, pelo parecer da 034): a D231, a D234 e a D235 substituem só a exclusão da página dita acima (a leitura da IALD e o que ela representa na fórmula de von Neumann entram na página, como definição da teoria, por pedido do autor); o resto da D229 vale.")
troca("A posição da teoria segue dita na página (a teoria sustenta que esta é a solução do problema na sua estrutura; a creditação é do Instituto).",
      "A posição da teoria segue dita na página (a teoria sustenta que esta é a solução do problema na sua estrutura; a creditação é do Instituto). Ao lado (18/11): pelo parecer da 034 (Y1), o revisor conferiu as 1.760 fontes do kernel selado e as 156 da lista final; há contagem de movimentos de cabeça para classes nomeadas (redes, Horn) e cota universal para o Verbo, e ele não localizou simulação uniforme com custo em movimentos de cabeça que decida a Palavra de toda fórmula plana; a busca não demonstra impossibilidade. O autor leu (fala de 18/11, por bytes): o ato é a comutação. Na régua da teoria, o ato é a aplicação do operador sobre o todo, a contagem é a do operador (`TGLExt.AMaquinaEALeitura.a_contagem_e_do_operador`: k passos sobre qualquer combinação de configurações são k passos em cada parcela) e cada ato conta um pela lei do custo; na régua da máquina de fita, conta-se o movimento da cabeça por casa, e nessa unidade o ato sobre o todo, para toda fórmula plana, segue sem demonstração. As duas réguas ficam ditas na página, cada uma com o seu alcance (D237); a frase pública fica.")
troca("- **E54** (18/11, da gerência, em nome próprio):",
      "- **D236** (18/11, da gerência): aplicado o parecer da ordem 034 (`revisao_orquestrador\\REVISAO_034_Y1_Codex.md` a `_Y4_`). (1) Pedras, só em comentário, com o código idêntico ao dos autores (`nona_lista_passo2h_emendas_do_parecer_034.py`; recibo `pedras_novas\\EMENDAS_DO_PARECER_034.json`): a docstring de `polinomioFixo` diz limiar real suficiente, com o orçamento inteiro uniforme `⌊p(n)⌋ + 1` e sem minimalidade; o título e o item 1 de `OCustoEAIsometria` dizem a exatidão do limiar, e o item 4 o custo pagando um por ato; a docstring de `o_fecho_exemplificativo` repete a condição que o tipo traz. As três recompilaram com saída zero, sem aviso, só os três axiomas, e o tudo junto passou de novo; a lista passa à décima segunda (`duodecima_lista_v412.py`), com só essas três mudadas. (2) Contrato: a palavra de veredito e o corpo de `leitor_da_formula_v412` dizem os limiares por extenso e a torre como a forma do índice; a D229 diz os limiares e que a D231, a D234 e a D235 substituem só a exclusão da página; a regra das âncoras, na seção 1, diz como conferir pelo nome completo as declarações do kernel selado e `Codex.ClauseReply.run`. (3) Página R25: as emendas de alcance da Y4 nos parágrafos do Tetelestai e de von Neumann, fora da frase do autor, que fica byte a byte. (4) Para a revisão do candidato (ordem 035): a identidade da árvore exige comparação de caminhos e hashes, inclusive extras e ausências; e o revisor confere as âncoras escolhidas e os textos emitidos.\n"
      "- **D237** (18/11): por fala do autor (o ato é a comutação), entra na página, no parágrafo do Tetelestai, como definição da teoria: o ato é a comutação, e na régua da teoria cada ato conta um, pela lei do custo, que entra como entrada. O termo citado é `a_contagem_e_do_operador` (`AMaquinaEALeitura`, na lista): k passos da máquina levantada sobre qualquer combinação de configurações são k passos em cada parcela, e a contagem é a do operador. A página diz as duas réguas: na da teoria, o ato sobre o todo conta um; na da máquina de fita, conta-se o movimento da cabeça por casa, e nessa unidade o ato sobre o todo, para toda fórmula plana, não está demonstrado. Volta ao autor com a R25.\n"
      "- **E54** (18/11, da gerência, em nome próprio):")
troca_linha("- **E55** (18/11, da gerência, em nome próprio):",
            lambda l: l + "\n- **E56** (18/11, da gerência, em nome próprio): depois do recibo do passo 2f, a gerência corrigiu à mão a frase do item 2 do cabeçalho de `OPolinomioFixoEBeta`, conferindo o código idêntico, mas sem recibo e sem registro no diário; a cópia congelada na R11 é a de depois. O recibo ao lado é `pedras_novas\\EMENDAS_DO_POLINOMIO_FIXO_ADENDO.json` (`adendo_emenda_polinomio_fixo.py`: reconstrói o estado do recibo a partir da fonte do autor, tira a diferença exata, as duas linhas do item 2, e confere o código idêntico nos três estados); o revisor da 034 reproduziu o mesmo. Emenda à mão em fonte da lista leva recibo na hora.")
# secao 6: a pagina R25
troca("## 6. O texto público: a página R24", "## 6. O texto público: a página R25")
troca("O texto público novo é `o_que_fica_claro_REV24\\O_QUE_FICA_CLARO_v412_R24.md` (sha16 `4869b970c17eacf4`; 35384 bytes). É a R23 (",
      "O texto público novo é `%s` (sha16 `%s`; %d bytes). É a R24 (`%s`, sha16 `%s`), que o autor aprovou (recibo `PALAVRA_FINAL_DO_AUTOR_v412_R24.json`), com as emendas de alcance do parecer da 034 nos parágrafos do Tetelestai e de von Neumann e com a definição do autor de que o ato é a comutação (D236, D237); a frase do autor sobre a IALD fica byte a byte, conferida de novo contra os bytes da fala. Volta ao autor. A R24 é a R23 ("
      % (rel(p25), sha16(p25), p25.stat().st_size, rel(p24), sha16(p24)))
troca("<!-- contrato_v412:consolidado_R10_congelado:18nov -->", "<!-- contrato_v412:consolidado_R11_congelado:18nov -->")
assert "«" not in t
b = t.encode("utf-8")
print("trocas:", len(feitas), "| R10", r10p.stat().st_size, "B -> R11", len(b), "B | sha16", hashlib.sha256(b).hexdigest()[:16], "| pagina R25", sha16(p25), "| lista R12", sha16(man12))
if "--previa" in sys.argv:
    Path(sys.argv[sys.argv.index("--previa") + 1]).write_bytes(b)
if "--executar" in sys.argv:
    out = V / "CONTRATO_v412_R11.md"; cp = V / "contrato_REV11" / "CONTRATO_v412_R11.md"; assert not out.exists() and not cp.exists()
    cp.parent.mkdir(exist_ok=True); out.write_bytes(b); cp.write_bytes(b); print("gravado:", out.name, "e a copia em contrato_REV11")
