"""R5: monta a traducao EN da pagina R18 (O_QUE_FICA_CLARO_v412_R18_EN.md) a partir da EN da R13 (arquivo do R4, que fica intacto). As diferencas da R13 para a R18 (medidas por e5_20_diff_r13_r18_v412.py) sao:
um item novo na secao 1; tres mudancas dentro do paragrafo de citacao da secao 2; uma linha da primeira tabela; e o bloco novo “O leitor da formula” (dois paragrafos, a tabela de 30 linhas e o paragrafo de fecho).
Traducao fiel: mesma estrutura, mesmos termos entre crases na mesma ordem, nomes de termos e de modulos intactos. Confere a estrutura e os termos contra a pagina R18 antes de gravar. Escrita por temporario; backup de bytes."""
import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e5_lib_v412 as L
import texto_publico_v412 as TP0   # (so' a funcao blocos, para comparar a estrutura; o conversor da v412 r5 e' texto_publico_v412_r5.py)

SRC = L.D / "O_QUE_FICA_CLARO_v412_R13_EN.md"
DST = L.D / "O_QUE_FICA_CLARO_v412_R18_EN.md"
en = SRC.read_bytes().decode("utf-8").split("\n")
pt = L.PAGINA.read_bytes().decode("utf-8")

ITEM_9 = ("- **The reader of the formula.** The PsiBit is read directly from the clauses. The summary of the reading is a table over the frontier between the part read and the part still to be read, and grouping the read sum by the frontier loses nothing; "
          "the rule for reading the letter is fixed, equality; the state is the table, and the curve of the read sum is its projection. For classes of formulas, each with its own machine and its own writing, the reading closes on the tape within a fixed polynomial in the number of letters; "
          "for the arbitrary flat formula, that polynomial has not been shown (section 2).")
TROCAS_PARAGRAFO = [
    ("it checks, a single time, the proof of the law for every formula, without receiving any formula or assignment;", "it checks, at once and for every formula, the proof of the cost under the adopted law, without receiving any formula or assignment;"),
    ("Counted letter by letter on the tape machine of the Institute's statement, the same result has not been shown, and this text does not say that it has: the question of the Institute, whether there is a letter procedure with a polynomial number of steps for every formula, is not tautological and remains open.",
     "The answer of the theory to the question of the Institute is the PsiBit: the reader of the pair, which comes directly from the formula. Counted letter by letter on the tape machine of the Institute's statement, the same result has not been shown for every formula, and this text does not say that it has: "
     "the fixed polynomial in letters is proved for classes of formulas, each with its own machine and its own writing (series-parallel networks with the junctions written in the input, chains of fixed width, formulas in which the two restrictions of the first variable are Horn, "
     "binary chains in the promised order, binary clauses that begin with one of two pivots), and for the arbitrary flat formula it is what the theorems themselves leave open."),
]
TROCA_LINHA_36 = ("[KNOWN] formulas with two variables per clause are decided in polynomial time by the letter machine |",
                  "[KNOWN] formulas with at most two literals per clause are decided in polynomial time by the letter machine (Aspvall, Plass and Tarjan, 1979, Information Processing Letters 8(3), 121–123) |")
P48 = ("**The reader of the formula.** Definition of the theory: the compression comes directly from the formula, and it is the PsiBit; the reading of the binary pair by the PsiBit is the original compression, the reader itself; the reading rule is a single one, the equals sign. "
       "The kernel types the part of this that fits in a term. Read clause by clause, the formula leaves as state a table over the frontier, the variables that the part read still shares with the part still to be read. "
       "Grouping the read sum by the frontier loses nothing: the whole sum adds, in each cell, the products of the weight read by the weight still to be read over the complete assignments that fall in it; the plain sum of the cells of the table gives the read sum of the prefix. "
       "Every walk from a variable that is only read to a variable that is only still to be read has a vertex on the frontier: it separates the graph of the formula. The rule for reading the letter is equality to what is put, and it does not depend on the formula. "
       "The two bits of the formula are the Word (there is a solution) and the Verb (the read sum still descends); in formulas of one variable, each one alone confuses formulas that the other distinguishes. "
       "Two distinct tables can have the same sum and never the same content: the prefixes x and not-x have the same curve for every time and opposite answers after the same clause; the state is the table, the curve is its projection. "
       "Given the two frontiers, the next table comes from the previous one and from the clause that enters, by a rule that holds for every formula. Fixing a label applies the same choice to all its occurrences, and the Word of the formula is the disjunction of the Words of the two branches. "
       "Two blocks join when there is a compatible witness on each side, the two with the same values on the names they share, and at least one of them satisfies the part of the new clause that falls to it. The refusal of a proposal returns an occurrence of the violated clause, and that refusal is reused.")
P50 = "In the table, each row has its own machine, its own writing and its own unit (transitions, steps or displacements); L is the length of the input in the writing of the row."
TABELA = [
    "| what is stated | term | where |",
    "|---|---|---|",
    "| the summary only sees the frontier, and grouping by it loses nothing | `o_resumo_so_ve_a_fronteira`: the summary is constant on each cell of the frontier. `a_leitura_pela_fronteira_e_exata`: the whole read sum adds, in each cell, the products of the weight read by the weight still to be read over the complete assignments of the cell. `total_projection`: the sum of the cells gives the read sum of the prefix, in any number of variables. The table has 2 to the size of the frontier cells (`a_fronteira_tem_duas_elevado_as_celulas`), including when the frontier is the set of all the variables | `OResumoEPsiBit`, `ProjecaoDaFronteira` |",
    "| every walk from the only read to the only still to be read has a vertex on the frontier | `o_percurso_atravessa_a_fronteira`, with the walk given as an explicit list. It is not proved that the frontier is the smallest separator, nor the only one. `a_fronteira_e_o_unico_portao` concludes only that, the chain existing, the frontier is not empty | `OSeparadorNoPercurso`, `AFronteiraEOUnicoPortao` |",
    "| the reading rule is fixed and is equality; Word and Verb | `a_regra_e_unica_e_anterior`: the rule does not have the formula as input (the term does not compare competing rules). `a_palavra_e_lida_pela_soma`: with the time paid above n·ln 2. `a_descida_e_positiva_sse_ha_o_que_ler`: for every time, the descent is positive if and only if there is an assignment of nonzero cost. `o_par_e_necessario_e_suficiente_na_formula`: the two controls, in formulas of one variable | `OPsiBitDaFormula` |",
    "| the clause is exemplary: one literal that fits suffices | `a_clausula_e_exemplificativa`: the clause holds if and only if some literal holds. `o_caput_nao_esgota_a_variavel`: the literal only reads its own variable. `a_verdade_e_lida_no_contorno` and `a_leitura_nao_e_cem_por_cento_em_tempo_finito`: the lock of the cost tends to the projection onto the solutions and, there being amplitude outside them, does not reach it in finite time | `AClausulaExemplificativa` |",
    "| the tape is the index: every position has to be read, and the same name carries the same value | `quem_nao_visita_nao_le`: a reader blind to one position gives the same answer to two tapes with opposite answers; it is the bound of reading the whole input. `sat_formulaDa` and `a_coreferencia_obriga_o_transporte`: in a family of two unit clauses on the same variable, there is a solution if and only if the two positions read agree | `AFitaEOIndice` |",
    "| same curve, distinct contents | `mesma_curva_para_todo_tempo`; `palavras_opostas_depois_da_mesma_clausula`; `a_fronteira_distingue_os_prefixos` (the cells differ for nonzero time); `a_curva_identifica_o_que_o_resumo_distingue`. It is the example of one variable | `ACurvaEAEstado` |",
    "| the transition of the table holds for every formula | `transition`: at every cut before the end and for every time, the next table is the previous one advanced by the clause that enters, given the old frontier and the new one. The identity gives no bound on construction or on time | `TransicaoDaFronteira` |",
    "| the fixed label preserves the correlation | `word_split`: the Word is the disjunction of the Words of the two restrictions. It does not give, by itself, the cost of evaluating the branches | `RestricaoGlobal` |",
    "| the whole Name per branch, when the clause enters | `marked_clause_law`: the prefix with the new clause is compatible with the marks if and only if some literal of it is compatible with the prefix (it holds for the empty clause and for any list of marks). `whole_name_after_clause`: with a positive number of steps and β between 0 and 1 | `AtualizaONome` |",
    "| two blocks join by the content of the shared names | `semantic_handshake`: with the common names covered by the labels or by the marks, the formula with the new clause is compatible if and only if there is a certified witness on each side, the two equal on the labels, and at least one satisfies its part of the clause. Two equal echoes can fail together | `HandshakeDoNome` |",
    "| the refusal returns the violated clause | `inspect_some`: the refusal returns an occurrence of a violated clause of the block that answers. `reuses_clause`: it holds for every assignment that coincides on the variables of the clause. `reply_bounds` and `call_bound`: for a block of m clauses, at most m returns and m + 1 calls to an exact proposer, whose time is still to be measured | `ARecusaTemConteudo`, `ClausulaComoResposta` |",
    "| series-parallel networks, with the junctions written in the input: at most L² + 1 transitions | `fixed_polynomial_for_networks`: a machine with one tape and one head, the same for every network | `PolinomioDoPsiBit` |",
    "| chains of bags of fixed width: L + 1 steps | `fixed_width_psibit`. The control depends on the width; it is not a uniform machine when the width is part of the input | `PolinomioDoPsiBit` |",
    "| formulas in which the two restrictions of the first variable are Horn: a quadratic bound in L | `fixed_zero_two_horn`: the displacements add up to at most 27L + 16 + 4(L + 1)(3L + 2). It does not include finding a pivot that works | `CircuitoNaFita` |",
    "| the class of the sign profile: at most 7L movements, in two passes | `seven_movements_per_letter`: the bound holds for every tape. `word_exact`: the output is the Word when every variable, other than the pivot, that appears with both signs also appears in a unit clause | `SegundaLeitura` |",
    "| binary chain in the promised order (each new end has not yet occurred; the parities of the addresses alternate): the correlation between the ends fits in four bits and comes from the letters in exactly L displacements | `one_head`: L displacements in L + 1 transitions. `closed_path`: the four values between the ends in L displacements, including the clause that links the two ends. The ordering and the recognition of the class on arbitrary inputs are not counted | `CadeiaNaFita`, `DuasPontasLivres` |",
    "| binary clauses in which the first literal is one of two pivots (the one at address zero and another) and the second is a name outside the two: the four branches in exactly 7L + 8T movements, T being the number of address marks | `exact_movements`: four passes, with the returns. `branch_exact`: each branch answers whether there is an assignment with those two values. The free names may repeat | `ReguaNaFita` |",
    "| a family of 6k + 14 letters: the search by literals makes at least 2 to the k checks; another reader reads the same family in exactly 66k + 166 movements | `delayed_letters`; `delayed_checks`; `exact_delayed_moves`. They are counts of different readers and of different operations | `CustoDaBuscaLiteral`, `LeitorDeReuso` |",
    "| the Verb of any formula: at most 3L + 1 steps | `universal_verb_tape`: a two-stack machine, with unary addresses. It is the Verb, not the Word | `VerboNaFita` |",
    "| the transport of the inscription in two bits per letter: 6L displacements, adding transmission and reception | `any_cnf_transport` (8L with the rewinding of the channel). The reconstruction delivers the inscription; the Word requires further reading | `TransporteDaInscricao` |",
    "| limit: the explicit list of rows of the table exceeds every polynomial in a family | `no_uniform_row_polynomial` | `CustoDaTabela` |",
    "| limit: every complete execution of the plan of branches taken from the syntax exceeds every polynomial in a coupled family | `exceeds_each_polynomial` | `LimiteDoLeitor` |",
    "| limit: the projections alone do not update | `no_profile_update`: with at least one variable, there is no function that, from the profile of projections of the prefix and the whole clause, gives the next profile for every prefix and every clause | `LimiteDasProjecoes` |",
    "| limit: conjunctive records that represent exactly the solutions of k disjoint pairs require at least 2 to the k records | `any_exact_cube_layer` | `LimiteDoReuso` |",
    "| limit: covering exactly, with k affine labels, the conjunction of n clauses of two positive literals on disjoint pairs requires 3ⁿ ≤ k·2ⁿ | `cover_lower_bound` | `CoberturaAfin` |",
    "| limit: a key of b bits, exact for every prefix and for every continuation that fixes the w free labels, has b ≥ 2 to the w | `binary_key_bound`. The formulas that realize arbitrary relations can be long: it is not a bound in the length L | `CapacidadeDosRotulos` |",
    "| limit: the key in dense phase exceeds every polynomial in a family | `charged_lower`: the path of the head to the digit that decides. `no_fixed_dense_budget`: that floor exceeds every polynomial in the length of the source | `CustoDaFaseDensa` |",
    "| limit: a register of p bits, exact for every continuation of every formula in n variables, has p ≥ 2ⁿ | `o_nome_exato_pede_dois_a_n_bits`. It is a floor of space in the worst case, in n; it estimates neither time nor the length L | `AParedeDoNome` |",
    "| the reduction: every formula embeds, in at most 5L + 15 actions of reading and writing, into an instance of two blocks with a bridge, compatible if and only if the original is | `linear_embedding`. `genuinely_shared` and `packet_decides` link the bridge to the indicators of the blocks. Whoever generated those indicators uniformly, from the input, would decide whether the formula has a solution; the cost of that generation is not bounded | `ClausulaNoSeparador` |",
    "| has not been shown | open: a single executable machine that decides the Word of every flat formula in movements bounded by a fixed polynomial in the number of letters. Identities between tables, limits of one reader and finite controls do not give that result | — |",
]
P85 = ("Each limit above is of the reader or of the representation that the theorem examines; none is a bound for every procedure. That the compression is the PsiBit, that the separator is the floor of the reading, that the curve is the rereading, "
       "that the refusal is a name with content, that the truth is the contour and that the tape is the index and the tower are definitions of the theory, which enter as input.")
assert len(TABELA) == 32

# as posicoes na EN da R13 (as mesmas linhas da R13 em portugues: 77 linhas nas duas)
assert len(en) == 77, len(en)
assert en[8].startswith("- **") and en[7].startswith("- **"), (en[7][:40], en[8][:40])
assert en[12].startswith("> P = nP is a theorem of the TGL in the classes of its dictionary.")
assert en[35].startswith("| counted letter by letter, the house procedure costs the whole |")
assert en[44].startswith("**") and en[45] == "", (en[44][:50], repr(en[45]))
par = en[12]
for velho, novo in TROCAS_PARAGRAFO:
    assert par.count(velho) == 1, velho[:60]
    par = par.replace(velho, novo)
l36 = en[35]
assert l36.count(TROCA_LINHA_36[0]) == 1
l36 = l36.replace(*TROCA_LINHA_36)
out = list(en)
out[45:45] = ["", P48, "", P50, ""] + TABELA + ["", P85]
out[35] = l36
out[12] = par
out[8:8] = [ITEM_9]
txt = "\n".join(out)
# a estrutura e os termos, contra a pagina R18
bpt, ben = TP0.blocos(pt), TP0.blocos(txt)
est = lambda bl: [(t, (len(v) if isinstance(v, list) else (len(v[1]) if t == "table" else 1))) for t, v in bl]
assert est(bpt) == est(ben), ("a traducao nao tem a mesma estrutura da pagina", [(a, b) for a, b in zip(est(bpt), est(ben)) if a != b][:5], len(bpt), len(ben))
cod_pt, cod_en = re.findall(r"`([^`]+)`", pt), re.findall(r"`([^`]+)`", txt)
assert cod_pt == cod_en, ("os termos entre crases diferem", [(a, b) for a, b in zip(cod_pt, cod_en) if a != b][:5], len(cod_pt), len(cod_en))
assert len(txt.split("\n")) == len(pt.split("\n")), (len(txt.split("\n")), len(pt.split("\n")))
# numeros e formulas iguais, linha a linha (os algarismos e os simbolos matematicos nao se traduzem)
num = lambda s: re.findall(r"\d+|[≤≥ⁿ²·]", re.sub(r"`[^`]+`", "", s))
dif_num = [(i + 1, num(a), num(b)) for i, (a, b) in enumerate(zip(pt.split("\n"), txt.split("\n"))) if num(a) != num(b)]
print("linhas com numeros/simbolos diferentes entre PT e EN:", len(dif_num), dif_num[:6])
L.salvar_bytes(DST, txt.encode("utf-8"))
print("gravado", DST, DST.stat().st_size, L.sha16_arq(DST), "| blocos", len(ben), "| termos entre crases", len(cod_en), "| linhas", len(out))
