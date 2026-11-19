# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: deriva o CONTRATO_v412_R5.md do R4 congelado, por trocas exatas (cada marca casa UMA vez), com os
numeros e os sha16 LIDOS dos arquivos: o manifesto e as ancoras da lista vigente, a pagina vigente, o R4. Hora do relogio.
Uso: derivar_contrato_r5.py <manifesto.json> <ancoras.json> <pagina.md> [--executar]
Sem --executar so' ensaia (mostra tamanho e as trocas). Com --executar grava CONTRATO_v412_R5.md e a copia em contrato_REV5\\; nao
sobrescreve. A pagina passada tem de ser a VIGENTE (lida por terceiro e com a palavra do autor sobre a frase): o script nao sabe disso;
quem roda responde por isso."""
import hashlib, json, re, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
p_man, p_anc, p_pag = (Path(a) for a in sys.argv[1:4]); EXEC = "--executar" in sys.argv
sha16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
rel = lambda p: str(Path(p).resolve().relative_to(V))
man = json.loads(p_man.read_text(encoding="utf-8")); mods = man["modulos"]
A = [m["modulo"] for m in mods if m.get("frente") == "A"]; B = [m["modulo"] for m in mods if m.get("frente") == "B"]; C = [m["modulo"] for m in mods if m.get("frente") == "C"]
assert len(A) + len(B) + len(C) == man["n_modulos"] == len(mods), (len(A), len(B), len(C), man["n_modulos"])
por = {q: sum(1 for m in mods if m.get("frente") == "C" and m["de_quem"] == q) for q in ("gerencia", "Kimi", "Codex")}
ns = {}
for m in mods:
    if m.get("frente") == "C":
        for n in m["namespaces"]:
            ns.setdefault(n.split(".")[0], set()).add(m["modulo"])
r4p = V / "CONTRATO_v412_R4.md"; t = r4p.read_bytes().decode("utf-8"); assert sha16(r4p) == sha16(V / "contrato_REV4" / "CONTRATO_v412_R4.md")
pag_nome = p_pag.stem.split("_")[-1] if not p_pag.stem.endswith("PROPOSTA") else p_pag.stem.split("_")[-2] + " (PROPOSTA)"
feitas = []


def troca(velho, novo, n=1):
    global t
    assert t.count(velho) == n, "%d ocorrencias (esperava %d): %s" % (t.count(velho), n, velho[:80])
    t = t.replace(velho, novo); feitas.append(velho[:60])


def troca_linha(prefixo, nova):
    global t
    ls = t.split("\n"); idx = [i for i, l in enumerate(ls) if l.startswith(prefixo)]
    assert len(idx) == 1, "%d linhas com o prefixo: %s" % (len(idx), prefixo[:80])
    ls[idx[0]] = nova; t = "\n".join(ls); feitas.append(prefixo[:60])


lista = "nona" if p_man.name.endswith("_R9.json") else "décima"
troca("# CONTRATO DA v412 — versão consolidada R4 (CONGELADA)", "# CONTRATO DA v412 — versão consolidada R5 (CONGELADA)")
troca_linha("> Gerência c1, 17/11/2026, 17:19. Substitui o R3",
            "> Gerência c1, 18/11/2026, %s. Substitui o R4 (`contrato_REV4\\CONTRATO_v412_R4.md`, sha16 `%s`), que fica como registro, como o R3, o R2 e o R1. É o contrato que o construtor segue para regerar o candidato e fazer a Etapa 3, e que o revisor do candidato usa como régua. Conserva tudo o que o R4 trouxe e acrescenta: a %s lista de pedras (as duas da oitava e as %d do leitor da fórmula), um registro novo, a página %s e as respostas aos pontos que o construtor deixou no fecho da Etapa 2." % (time.strftime("%H:%M"), sha16(r4p), lista, len(C), pag_nome))
troca("Emenda a este contrato: só por revisão nova (`CONTRATO_v412_R5.md`), nunca por cima.", "Emenda a este contrato: só por revisão nova (`CONTRATO_v412_R6.md`), nunca por cima.")
troca("**O que mudou do R3 para o R4** (para quem já estava seguindo o R3):",
      """**O que mudou do R4 para o R5** (para quem já estava seguindo o R4):

1. Seção 1: a lista é a %s, com %d módulos: os 42 da sétima, as duas pedras da oitava (`OPassoEOFim`, `OPsibitEACompressao`, na frente A) e %d módulos novos numa frente nova, a C (o leitor da fórmula). A regra das âncoras ganha o recuo pelos `#print axioms`. Os identificadores das fontes não se renomeiam.
2. Seção 2: um registro novo, `leitor_da_formula_v412`; o veredito de `iald_camada_cientifica_v412` troca um trecho por três; os registros passam a cinco.
3. Seção 3: o artefato das falas vai até os arquivos de 18/11.
4. Seção 4: as decisões D222 a D226 e a errata E54.
5. Seção 6: a página passa a %s (um item novo na seção 1; o bloco do leitor da fórmula na seção 2; a última frase do parágrafo de citação da seção 2).
6. Seção 8: o construtor regera o candidato pela lista nova e faz a Etapa 3.
7. O resto é o do R4, sem mudança.

**O que tinha mudado do R3 para o R4:**""" % (lista, len(mods), len(C), pag_nome))
troca("## 1. Pedras (kernel): 42 módulos novos", "## 1. Pedras (kernel): %d módulos novos" % len(mods))
troca_linha("**A lista é a sétima**, e só ela:",
            "**A lista é a %s**, e só ela: `%s` (sha16 `%s`), com as fontes congeladas em `insumos\\pedras_r%s\\` e as âncoras propostas em `%s` (sha16 `%s`). São os 42 módulos da sétima lista, sem mudança; as duas pedras da oitava, `OPassoEOFim` e `OPsibitEACompressao`, lidas por terceiro; e %d módulos novos do leitor da fórmula (campo `novas_em_relacao_a_oitava_lista` do manifesto), de três autores (%d da gerência, %d do Kimi, %d do Codex). Nos %d novos o código fora de comentários é idêntico ao da fonte de cada autor (campo `fonte_revista_sha256`); a gerência só ajustou comentários, pelo método da seção 0 e pelos pareceres das ordens 031 e 032 (as últimas emendas, feitas pelo parecer da 032, vão à leitura de terceiro com o candidato). Uma das pedras da gerência, `OSeparadorNoPercurso`, foi escrita em resposta ao parecer da 031 e aprovada no da 032. Duas pedras do Kimi, `AClausulaExemplificativa` e `AFitaEOIndice`, entraram por ordem do autor depois do corte: a gerência as recompilou (saída zero, três axiomas) e ajustou os cabeçalhos pelo método, e elas ainda não foram lidas por terceiro (vão com o candidato). Cada log de compilação é da fonte congelada. Uma raiz que importa o kernel inteiro e os %d módulos compila sem erro (campo `tudo_junto` do manifesto): não há nome de declaração repetido. `Token2` importa também o módulo selado `TGLExt.Token`."
            % (lista, rel(p_man), sha16(p_man), "9" if lista == "nona" else "10", rel(p_anc), sha16(p_anc), len(C), por["gerencia"], por["Kimi"], por["Codex"], len(C), len(mods)))
troca("Frente A (a camada científica), 15 módulos: ", "Frente A (a camada científica), %d módulos: " % len(A))
troca("`AEsperancaEOIf`, `Token2`, `AMaquina`.", "`AEsperancaEOIf`, `Token2`, `AMaquina`, `OPassoEOFim`, `OPsibitEACompressao`.")
assert set(A) == {"CamadaCientifica", "MinimoFuncionalDeEnergia", "OLeitorEALei", "AContagemEACarga", "AMaquinaEALeitura", "OPassoEORetorno", "OHabitanteDoNome", "NomeComoCodigo", "CopiadorEImpostor", "OTempoEACauda", "AFitaEACauda", "AMedidaEOIf", "AEsperancaEOIf", "Token2", "AMaquina", "OPassoEOFim", "OPsibitEACompressao"}, sorted(A)
assert len(B) == 27
troca("Em caso de dúvida sobre a frente ou a autoria de um módulo, vale o manifesto, não esta lista.",
      "Frente C (o leitor da fórmula), %d módulos: os do campo `novas_em_relacao_a_oitava_lista` do manifesto (os que têm `frente` igual a `C`). Conservam os espaços de nome que os autores lhes deram (%s) e os nomes das declarações; duas são sondas, com nome de arquivo em minúsculas.\n\nEm caso de dúvida sobre a frente ou a autoria de um módulo, vale o manifesto, não esta lista."
      % (len(C), ", ".join("`%s.*` em %d" % (k, len(v)) for k, v in sorted(ns.items(), key=lambda kv: -len(kv[1])))))
troca("Nenhuma outra edição das fontes é autorizada, por motivo algum:", "Nenhuma outra edição das fontes é autorizada, por motivo algum, e nenhum identificador (espaço de nome, nome de declaração, nome de módulo) é renomeado:")
troca("o construtor lista as escolhidas num recibo para a gerência conferir.", "nos módulos sem estrela que a página não cita e cujo cabeçalho não dá resultado principal, ancora as declarações que o próprio módulo lista nas suas linhas `#print axioms` (campo `listadas_em_print_axioms` do insumo das âncoras); o construtor lista as escolhidas num recibo para a gerência conferir.")
troca("__WHETHER_A_LETTER_PROCEDURE_WITH_POLYNOMIAL_STEPS_EXISTS_FOR_EVERY_FORMULA_IS_OPEN_AND_NOT_TAUTOLOGICAL",
      "__THE_STEP_ONE_MINUS_BETA_CLOSES_THE_CYCLE_IN_LINEARLY_MANY_STEPS_ON_THE_WHOLE_AND_THE_NAME_STAYS_WHOLE__THE_BINARY_PAIR_WORD_AND_VERB_ANSWERS_FOR_EVERY_FORMULA_ABOVE_THE_LOAD__A_LETTER_PROCEDURE_WITH_ONE_FIXED_POLYNOMIAL_FOR_EVERY_FORMULA_NOT_SHOWN_AND_NOT_TAUTOLOGICAL")
troca("Módulos: os 15 da frente A. Alcance dos seis trechos novos da sexta lista:", "Módulos: os %d da frente A. Alcance dos dois trechos das pedras da oitava lista: o passo é o fator `1 − β` com `β` parâmetro real entre 0 e 1 (a identificação com o β da teoria é entrada); o número de passos que fecha o ciclo é linear no número de variáveis e cada passo age sobre o todo, logo não é contagem de letras; o par binário é a Palavra (há solução) e o Verbo (a soma lida ainda desce), lidos com o tempo pago acima da carga, e é a compressão da LEITURA, não a compressão a partir das letras da fórmula. Alcance dos seis trechos da sexta lista:" % len(A))
troca("e a pergunta do Instituto segue em aberto e não é tautológica. Alcance de três outros trechos",
      "e um procedimento de letras com um polinômio fixo para toda fórmula não está demonstrado, e a pergunta não é tautológica (o que se sabe da contagem por letra está no registro `leitor_da_formula_v412`). Alcance de três outros trechos")
troca("- `matematica_que_restava_v412`\n",
      """- `leitor_da_formula_v412`
  `TGL_FORMULA_READER_V412__GROUPING_THE_READ_SUM_BY_THE_FRONTIER_LOSES_NOTHING__EVERY_WALK_FROM_THE_ONLY_READ_TO_THE_ONLY_UNREAD_HAS_A_VERTEX_ON_THE_FRONTIER__THE_READING_RULE_IS_FIXED_AND_IS_EQUALITY__THE_CLAUSE_IS_EXEMPLARY_ONE_FITTING_LITERAL_SUFFICES__EVERY_POSITION_OF_THE_TAPE_MUST_BE_READ_AND_THE_SAME_NAME_CARRIES_THE_SAME_VALUE__WORD_AND_VERB_ARE_THE_TWO_BITS_OF_THE_FORMULA__THE_STATE_IS_THE_TABLE_AND_THE_CURVE_IS_ITS_PROJECTION__THE_TABLE_TRANSITION_HOLDS_FOR_EVERY_FORMULA_GIVEN_THE_TWO_FRONTIERS__THE_WHOLE_NAME_PER_BRANCH_HAS_AN_UPDATE_LAW_FOR_EVERY_CLAUSE__BRANCHES_JOIN_ON_EQUAL_CONTENT_OF_THE_SHARED_NAMES__A_REFUSAL_RETURNS_A_VIOLATED_CLAUSE_AND_THERE_ARE_AT_MOST_AS_MANY_REFUSALS_AS_CLAUSES__ONE_FIXED_POLYNOMIAL_FOR_NAMED_CLASSES_OF_FORMULAS_EACH_WITH_ITS_OWN_MACHINE_AND_WRITING__THE_VERB_OF_ANY_FORMULA_IN_LINEARLY_MANY_STEPS_OF_A_TWO_STACK_MACHINE__EACH_EXAMINED_REPRESENTATION_HAS_A_PROVED_LIMIT__GENERATING_THE_BLOCK_INDICATORS_UNIFORMLY_WOULD_DECIDE_SATISFIABILITY__ONE_FIXED_POLYNOMIAL_FOR_THE_WORD_OF_EVERY_FLAT_FORMULA_NOT_SHOWN__THE_COMPRESSION_AS_THE_PSIBIT_IS_A_DEFINITION_OF_THE_THEORY_NOT_A_KERNEL_TERM__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED`
  Módulos: os %d da frente C. O corpo diz, por extenso e só com o que tem âncora: as classes nomeadas e a cota de cada uma, com a unidade do enunciado (transições, passos ou movimentos) e a hipótese de cada teorema, como na tabela da seção 2 da página; que cada limite é do leitor ou da representação que o teorema examina, e não cota para todo procedimento; que as definições da teoria (a compressão é o PsiBit; o separador é o piso da leitura; a curva é a releitura; a recusa com conteúdo; a verdade é o contorno; a fita é o índice e a torre) entram como entrada; e que o polinômio fixo para a Palavra de toda fórmula plana não está demonstrado. Este registro não usa a expressão “P = nP”.
- `matematica_que_restava_v412`
""" % len(C))
troca("lista dos arquivos `OPERADOR_13nov_*` a `OPERADOR_17nov_*`", "lista dos arquivos `OPERADOR_13nov_*` a `OPERADOR_18nov_*`")
troca("- **D205/D212** (o parágrafo de P = nP): o texto vigente é o da seção 2 da página R13 (seção 6 deste contrato).", "- **D205/D212** (o parágrafo de P = nP): o texto vigente é o da seção 2 da página vigente (seção 6 deste contrato).")
troca("- **D213/D217** (pedras): a lista é a quinta (seção 1).", "- **D213/D217** (pedras): a lista é a vigente (seção 1).")
troca("- **Leitura vigente de uma fala de 17/11:**",
      """- **D222** (18/11): por ordem do autor entra tudo na v412: as fontes novas do leitor da fórmula, de três autores, entram nesta versão, e não na seguinte. O corte é o das onze pastas fechadas até as 16:05 de 18/11; por ordem expressa do autor entram também as duas pedras que o Kimi escreveu depois (`AClausulaExemplificativa`, `AFitaEOIndice`); o que for escrito depois disso abre a versão seguinte. Entra ainda a pedra `OSeparadorNoPercurso`, da gerência, que responde a um achado do revisor (o lema do caminho concluía menos do que os textos diziam); a versão R1 que o autor da pedra `AFronteiraEOUnicoPortao` escreveu para o mesmo achado fica como alternativa examinada, fora da lista (parecer `revisao_orquestrador\\REVISAO_032_V1_Codex.md`).
- **D223** (18/11): o autor aceitou os nomes: os módulos entram com os nomes que os autores deram, e os identificadores do código ficam como estão.
- **D224** (18/11, da gerência): respostas aos pontos que o construtor deixou no fecho da Etapa 2 (`PREPARACAO_v412_PRONTA.json`, campo `decisoes_e_pontos_para_a_gerencia`). (1) Aceito o patch de DADO no literal `escada` do contrato do teste H0DN, junto dos literais `expected_ladder`, pelo precedente das versões anteriores; o relatório diz o valor antigo e o novo. (2) Não há pino exato de cobertura do kernel para a árvore nova nesta versão; o da v411 fica como piso, e o ensaio continua cobrando as entradas do hash formal. (3) Os identificadores `r1`, `r2`, `r3` das checagens do registro `cunhagens_v412` são trocados por nomes sem a forma de número de revisão (o construtor escolhe; por exemplo `selo_camada`, `selo_matematica`, `selo_parede`, e `selo_leitor` para o registro novo), já que o candidato é regerado. (4) Aceito o topo versionado. (5) Aceita a regra das âncoras com o recuo pelos `#print axioms`, agora dita na seção 1. (6) A página é a da seção 6. (7) `VERBATIM_CONGELADO_v412.json` segue fora do programa e fora da varredura dos insumos pinados; não se publica nem se copia para fora da casa.
- **D225** (18/11): o registro novo `leitor_da_formula_v412` (seção 2) e os dois trechos de veredito das pedras da oitava lista.
- **D226** (18/11): a frase da página sobre a pergunta do Instituto (seção 6) abre com a forma que o autor escolheu entre as duas propostas (“A resposta da teoria à pergunta do Instituto é o PsiBit”); o revisor recomendou a outra; a escolha é do autor. A frase afirma a resposta da teoria e diz o que os teoremas não cobrem.
- **E54** (18/11, da gerência, em nome próprio): a gerência rodou por engano um script de estado do construtor, que regravou um bloco de `ETAPA_2_ESTADO_v412.json`; os bytes da cópia anterior foram repostos e conferidos por hash; o arquivo errado ficou ao lado. Num registro do diário, um número não medido foi corrigido ao lado.
- **Leitura vigente de uma fala de 17/11:**""")
troca("(a) cada um dos quatro registros da seção 2, como checagem obrigatória;", "(a) cada um dos cinco registros da seção 2, como checagem obrigatória;")
troca("(4) o título da seção 2 da página R13 passa;", "(4) o título da seção 2 da página vigente passa;")
troca("## 6. O texto público: a página R13", "## 6. O texto público: a página %s" % pag_nome)
troca_linha("O texto público novo é `o_que_fica_claro_REV13\\O_QUE_FICA_CLARO_v412_R13.md`",
            "O texto público novo é `%s` (sha16 `%s`; %d bytes). É a R14 (a R13 com a emenda do parecer `revisao_orquestrador\\REVISAO_030_T3_Codex.md`) com três mudanças: um item novo na seção 1 (“O leitor da fórmula”); um bloco novo na seção 2, com o mesmo título, a tabela termo a termo e um parágrafo de fecho; e a última frase do parágrafo de citação da seção 2, que afirma a resposta da teoria (o PsiBit) e diz que o polinômio fixo em letras está provado para classes de fórmulas e não está demonstrado para a fórmula plana arbitrária. As seções 3 a 6 são as de antes. O bloco novo e a frase foram lidos por terceiro duas vezes (pareceres `revisao_orquestrador\\REVISAO_031_U3_Codex.md` e `REVISAO_032_V3_Codex.md`) e emendados linha a linha; a redação depois das emendas do segundo parecer, e as duas linhas da tabela acrescentadas por último (a cláusula exemplificativa; a fita e o índice), ainda não foram lidas por terceiro: vão com a revisão do candidato. Cada termo citado na tabela do bloco é teorema em algum módulo da própria linha (conferido por script ao montar a página)."
            % (rel(p_pag), sha16(p_pag), p_pag.stat().st_size))
troca("a adaptação dos scripts da cadeia ao conjunto de 40 módulos; a bateria pré-selo com o recibo do kernel da quinta lista; o gerador e o CANDIDATO; o ensaio a seco; o portão do pilar no candidato. Para no fecho do candidato que o molde da v411 usa.",
      "os cinco registros; a adaptação dos scripts da cadeia ao conjunto de %d módulos; o kernel da lista vigente no `k412c`; o gerador e o CANDIDATO regerado; o ensaio a seco; o portão do pilar no candidato. Para no fecho do candidato que o molde da v411 usa.\n- **Do construtor (Etapa 3, depois de a revisão do candidato aprovar):** adaptar de verdade, um a um, os scripts de rito, instalação, custódia e pós-rito que hoje trazem a marca `[A ADAPTAR v412]` (a marca só sai do script adaptado e ensaiado); a bateria pré-selo com o recibo do kernel da lista vigente." % len(mods))
troca("— gerência c1, 17/11/2026. Correções ao lado, nunca por cima.\n<!-- contrato_v412:consolidado_R4_congelado:17nov -->", "— gerência c1, 18/11/2026. Correções ao lado, nunca por cima.\n<!-- contrato_v412:consolidado_R5_congelado:18nov -->")
for proibido in ("«", "leitura do operador"):
    assert proibido not in t, proibido
b = t.encode("utf-8")
print("trocas:", len(feitas), "| frente A", len(A), "| B", len(B), "| C", len(C), por, "| espacos de nome da frente C:", {k: len(v) for k, v in ns.items()})
print("R4", r4p.stat().st_size, "B -> R5", len(b), "B | sha16", hashlib.sha256(b).hexdigest()[:16], "| pagina:", rel(p_pag), sha16(p_pag))
if "--previa" in sys.argv:
    Path(sys.argv[sys.argv.index("--previa") + 1]).write_bytes(b)
if EXEC:
    assert "PROPOSTA" not in p_pag.name, "a pagina passada e' proposta, nao a vigente"
    out = V / "CONTRATO_v412_R5.md"; cp = V / "contrato_REV5" / "CONTRATO_v412_R5.md"; assert not out.exists() and not cp.exists()
    cp.parent.mkdir(exist_ok=True); out.write_bytes(b); cp.write_bytes(b); print("gravado:", out.name, "e a copia em contrato_REV5")
