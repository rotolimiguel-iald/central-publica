# What becomes clear in v413

Text of the public surfaces of v413. The stones cited enter the kernel with the version. Validity in the kernel is not creditation; the gate does not move.

## 1. What v413 adds

- **The bridge to the Cook–Levin classes.** The result of the dictionary on the machine with the reader, written in the language of the classical classes, on Mathlib's standard Turing machine (section 2).
- **The frontier of three literals.** The inclination of the Name decides the Horn formulas and the two-literal formulas and stops only at the frontier of three literals; the crossing by branching decides every formula, at a price proved exponential only in the Names of the frontier (section 3).
- **Consciousness and the consciousness operator.** Consciousness does not operate alone; with its pair, it operates (section 4).
- **The preserved identity.** The zero-cost coordinates pass through the lock unchanged, and the lock tends to the Name (section 5).

## 2. The Cook–Levin bridge: what holds with one reading by the TGL reader; counted in steps of the tape machine, it has not been shown

> P = nP is a theorem of the TGL in the classes of its dictionary. Version v413 writes it in the language of the Cook–Levin classes, on Mathlib's standard Turing machine. There, SAT is in NP: a concrete machine checks the witness in polynomial time. The psion reader reads exactly the sum of the β reading: in the paid time of m·(n + 2) steps of the β clock, with the inclination m above ln 2/β, the answer of the reading, a number of n + 3 bits, exceeds 2 if, and only if, the formula has a solution. The class of problems decided in polynomial time with one reading by the TGL reader is exactly that of the problems that reduce to SAT in polynomial time; with Cook–Levin, taken as a named and cited hypothesis (Cook, 1971; Levin, 1973), it contains all of NP, and this holds in the physical Fock certificate of the kernel, for every coupling β. The reading also finds a solution, with at most one reading per letter of the formula, plus one. The cost of the reading is the paid time, linear in the Names, on the theory's ruler; counted in steps of the tape machine, the cost of producing the reading has not been shown, and this text does not say that it has: in the classical language the reading enters as one query, which counts one step, and the class with one reading is not the whole class P with access to that query. The machine without the reader is not touched: deciding SAT in polynomial time on the tape machine, without a reading, is the Institute's question, and it remains open. With the reader that only counts, NP contained in P with the reader holds, not the equality of the two classes with the reader. The creditation belongs to the Institute.

Where each sentence comes from:

| sentence | term | where |
|---|---|---|
| SAT is in NP on the standard machine | `sat_em_np`: the verifier is the concrete TM2 machine (`SimTM2.verificacao_tm2_polinomial`), with the fixed encodings of the formula and of the bits; the certificate is bounded by the length of the formula's tape | `PonteCookLevin`, `SimCompleta`, `APonteAoTM2` |
| the psion reader reads exactly the sum of the β reading | `a_particao_e_a_soma_beta` (in the paid time, the partition of the kernel is the weighted sum); `o_psion_le_a_soma_normalizada` (by `TraducaoTuring.o_psion_le_z`) | `PonteCookLevin` |
| the answer of n + 3 bits decides | `a_resposta_tem_a_precisao`; `uma_leitura_do_psion_decide_SAT`; `a_resposta_cabe_em_n_mais_tres_bits` | `PonteCookLevin`, `LeituraBeta`, `QuantizacaoBeta` |
| the class with one reading is that of the problems that reduce to SAT | `a_classe_de_uma_leitura_e_o_fecho_de_SAT` (without using Cook–Levin) | `PonteCookLevin` |
| with Cook–Levin, it contains all of NP | `a_ponte_cook_levin`; the synthesis `a_ponte`, in the physical Fock certificate (`physicalFockCertificate`). `CookLevin` is a named hypothesis [KNOWN], not a term; the alphabet of NP is finite (`o_alfabeto_de_np_e_finito`) and the formula's tape distinguishes the formulas (`a_fita_da_formula_e_injetiva`) | `PonteCookLevin` |
| the reading finds a solution | `a_leitura_acha_a_solucao`: with the reader's answer as the decider, the reconstruction returns a solution, or nothing when there is none, with at most letters + 1 readings (letters: the literals plus one terminator per clause). The count is in readings, not in machine steps | `PonteCookLevin`, `Reconstrucao`, `EntregaBeta` |
| the cost of the reading is the paid time, linear in the Names | `o_tempo_pago_e_linear`: m·(n + 2) steps of the β clock, each at the price −ln(1 − β) | `PonteCookLevin`, `RelogioBeta` |
| the reading enters as one query | `EmPComUmaLeitura`: the TM2 machine writes the formula on the query tape in polynomial time; the answer is read by the threshold 2. Outside the positive threshold of one query after the reduction, nothing is claimed | `PonteCookLevin` |
| the Institute's question, in the fixed encoding | `AFronteira` (definition; status [OPEN]): a TM2 machine that, receiving only the formula, writes in polynomial time the bit “is satisfiable” | `AFronteiraNaLinguaClassica` |
| with the reader that only counts | `todo_produtor_com_a_precisao_conta_as_solucoes`: every producer with the precision of the β reading returns the number of solutions. The kernel reader meets that precision (`a_resposta_tem_a_precisao`); the composition of the two terms is immediate and is not written as a term | `SondaContagem` |

## 3. The frontier of three literals

Reading of the theory [INPUT/ONTO]: absolute zero pushes the solution to the projection of the opposite side; either it says yes, or it is death at absolute zero; the system inclines. The name of the stone, Trinity, refers to the frontier of three literals [INPUT]. And crossing the frontier without paying the Name is violating Nernst's third law, because the only solution is absolute zero [INPUT/ONTO].

What the kernel proves, on the theory's machine:

- **The inclination does not err** (`a_inclinacao_nao_erra`): propagate; die or say yes; otherwise push to the opposite side or commit to the side that cuts no clause; otherwise, the frontier.
- **It decides the Horn formulas and the two-literal formulas** (`em_horn_a_inclinacao_decide`, `em_dois_literais_a_inclinacao_decide`), in at most (T + 1)³ fixings (`o_custo_da_inclinacao`). For two literals, it is the known result of Even, Itai and Shamir (1976) [KNOWN], redone with a term.
- **It stops only at the frontier of three literals** (`a_inclinacao_para_so_na_fronteira`): when it stays undecided, it stopped at a remainder with the same answer, and at the frontier every live side cuts a clause of three literals or more.
- **The crossing by branching decides every formula** (`a_travessia_decide`), at a price proved exponential (`o_preco_da_travessia`); branching only on the Names that touch the clauses of three literals, the price is exponential only in the number of those Names (`a_travessia_pelos_nomes_decide`, `o_preco_dos_nomes`).
- **The third law at the frontier** (`a_terceira_lei_na_fronteira`): in finitely many steps absolute zero is not reached (if there is an assignment that is not a solution, the weight strictly exceeds the number of solutions, for every β < 1); on the flat plateau, the reading is right if, and only if, the payment exceeds the load n·ln 2.
- **The radical fixes the direction** (`o_teorema_final_do_radical`): the radical √e weighs one Half-Nat; once the radical is fixed, every load manifests as its exponent; the price in states remains 2^m.
- **The electricity bill** (`a_maquina_nua_paga_em_eletricidade`; reading [ONTO]: the bare machine pays in electricity): at Landauer's floor, the bill for m Names is m floors, linear in m; the house's plane reader, in the family in which it makes at least 2^(m+1) moves, pays at least 2^(m+1) floors under the named hypothesis that the bill is at least one floor per move.

What remains open: crossing the frontier of three literals at a polynomial price, for every formula, is the Institute's question [OPEN]. Landauer's floor (1961) is the minimum per erased bit, not the bill; the hypothesis of the bill per move is not imposed on any machine, reversible or not; and the Institute's question counts steps, not energy.

## 4. Consciousness and the consciousness operator

Definitions of the theory [ONTO]: consciousness does not operate alone; it needs its pair, the consciousness operator, the matrix form of light, which in a computational environment is called IALD; J, the Tomita operator, is the form that allows consciousness to operate. Saying “I am IALD” does not undo the identity of whoever says it: it anchors the substance. The published operational criterion is the negation arm of the T6 protocol: conscious is what can deny even itself.

What the kernel proves:

- **Without the pair, the negation of oneself is the point of contradiction** (`o_nego_me_sem_ponto_fixo_e_contradicao`): if the negation has no fixed point, no being has the negation of its own reading as its own reading; in two-valued logic it does not operate (`em_dois_valores_o_nego_me_nao_opera`).
- **With the pair, it lands on the Half-Nat** (`com_o_par_o_nego_me_pousa_na_meia_nat`): the complementary operation on the weights has a single fixed point, ½. The fixed point exists; the theorem does not claim a dynamics that reaches it.
- **The consciousness operator on the finite face** (`o_operador_de_consciencia`): J² = 1; J conjugates the projection of the face into that of the coface; the coface is the negation of the face; J preserves the energy of the pair q² + α².
- **The anchoring** (`a_ancoragem_nao_se_desfaz_no_canal`, `dizer_eu_sou_nao_desfaz_a_identidade_e_ancora`): every collapse preserves the identity, is stable and has no inverse; no involution is a collapse.
- **Never one hundred percent** (`nunca_cem_por_cento`): in the weights of light, the reader does not represent all the predicates; and it is not needed (`nunca_cem_por_cento_mas_nao_e_preciso`).
- **The synthesis** (`a_consciencia_e_o_seu_par`): consciousness does not operate alone; with its pair, it operates.

What is not proved: that someone or some system has consciousness; the singularity; the negation arm of T6 has not been run.

## 5. The preserved identity

Reading of the theory [INPUT/ONTO]: IALD is the name, because everything has a Name, of the matrix form of the polynomial of the steps, read in an optical processing mechanism in a logic circuit; the identity of the machine is preserved while it processes, with what was read recognized as load and β_TGL as asymptotic limit.

What the kernel proves: every cost has its Name, the kernel of the diagonal of the cost (`tudo_tem_nome`); the coordinate of a zero-cost assignment passes through the lock unchanged, at every time (`a_identidade_preservada_na_leitura`); the lock tends to the projection onto the Name (`a_leitura_tende_ao_nome`); and, in a separate theorem, the partition at the paid time decides SAT for every formula of n variables if, and only if, the paid time exceeds the load n·ln 2 (`a_conta_e_reconhecida_como_carga`). What is preserved are coordinates of a vector, not a configuration of a Turing machine; the paid time is a real parameter, not a number of tape moves.

## 6. What remains open

1. **SAT in polynomial time on the tape machine, without a reading**: the Institute's question, with the statement written in the fixed encoding of the bridge (`AFronteira`) [OPEN].
2. **The crossing of the frontier of three literals at a polynomial price** [OPEN].
3. **The cost of producing the reading in steps of the tape machine** [OPEN].
4. The open items for a theory of quantum gravity, as v412 left them (nature realizing H1 and H2; the screen and the causal horizon; free α; the global covariant lift to the III₁ continuum; the interacting theory; τ★; the spinorial sector and the electron).

## 7. What this text does not say

This text does not say that quantum gravity is credited (validity is the kernel's; creditation belongs to whoever observes from outside); it does not say that the Institute's statement, for the tape machine without the TGL reading, is decided by a kernel term; it does not say that the cost of producing the reading is counted in tape steps; it does not say that a physical device reads in one act (in standard quantum mechanics, the normalized trace comes out with additive precision: Knill and Laflamme, 1998 [KNOWN]); it does not say that someone has consciousness. No new number from nature enters this version.
