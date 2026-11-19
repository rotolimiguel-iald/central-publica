VEREDITO REV20 `OLeitorEALei.lean`: **APROVADO** | VEREDITO REV21 `BoostEDissipador.lean`: **APROVADO_COM_RESSALVAS**

# REVISÃO 022 — Unidade V3 (Kimi, revisor distinto)

Data: 16/11/2026. Revisor: Kimi (V3), sem leitura de pareceres alheios nem do trabalho do Codex sobre estas candidatas.
Objetos (sha16 conferidos por bytes contra a ordem):

- `candidatas_c1\REV20\OLeitorEALei.lean` — sha256 `e8097c78307b6c18371538901a24b3fd10a7328bfaec3a6ad5654fc473ebb953` (sha16 `e8097c78307b6c18` ✓), 6 teoremas.
- `candidatas_c1\REV21\BoostEDissipador.lean` — sha256 `69765f7fc002c37c03625e6c28148235cf65052b05193335d0f8e3601cf7a1c7` (sha16 `69765f7fc002c37c` ✓), 11 teoremas.

Método: cópias próprias em `revisao_orquestrador\V3_Kimi\copias\{REV20,REV21}\` (sha16 idênticos após cópia); recompilação com `lean.exe` da toolchain `leanprover/lean4:v4.31.0` (a do projeto), `LEAN_PATH` sobre os `.olean` de `C:\t\k411c\final` (`final\.lake\build\lib\lean` + pacotes mathlib/batteries/Qq/aesop/importGraph/plausible/proofwidgets/LeanSearchClient). Sem `lake build`. Nada editado nas pastas `REV*`. Fatos marcados [DECLARADO] aguardam conferência da gerência na fonte.

---

## 1. Recompilação

### REV20 (`V3_Kimi\copias\REV20\rev20_out.txt`, `rev20_err.txt`)
Exit 0 em 73 s. **stderr vazio: zero avisos, zero erros.** stdout:

```
'TGLExt.OLeitorEALei.a_lei_na_clausula' depends on axioms: [propext, Classical.choice, Quot.sound]
'TGLExt.OLeitorEALei.o_custo_e_o_numero_de_falsos' depends on axioms: [propext, Quot.sound]
'TGLExt.OLeitorEALei.o_nome_e_onde_a_lei_da_verdadeiro' depends on axioms: [propext, Classical.choice, Quot.sound]
'TGLExt.OLeitorEALei.sat_e_existir_onde_a_lei_da_verdadeiro' depends on axioms: [propext, Classical.choice, Quot.sound]
'TGLExt.OLeitorEALei.o_operador_do_custo_conta_os_falsos' depends on axioms: [propext, Classical.choice, Quot.sound]
'TGLExt.OLeitorEALei.o_leitor_decai_por_falso' depends on axioms: [propext, Classical.choice, Quot.sound]
```

### REV21 (`V3_Kimi\copias\REV21\rev21_out.txt`, `rev21_err.txt`)
Exit 0 em 64 s. **stderr vazio: zero avisos, zero erros.** stdout: os 11 teoremas, cada um com `[propext, Classical.choice, Quot.sound]`.

### Leitura dos axiomas
Só os três axiomas padrão do Mathlib em todos os 17 teoremas; nenhum `sorryAx`, nenhum axioma declarado no arquivo. A varredura de `sorry`/`admit`/`axiom` nos fontes só encontra a frase do cabeçalho "Sem sorry, sem axioma novo". A cláusula do cabeçalho **confere** nas duas.

---

## 2. Enunciado contra docstring, um a um

### REV20 — 6/6 conferem

1. `a_lei_na_clausula` (REV20:68-72) — docstring: "VERDADEIRO (1) sse a cláusula vale, FALSO (0) sse não vale". Enunciado: o par de iffs exato. Como `bit` e `truthValue 1 ·` só produzem 0/1, a dicotomia é completa. **Não é vazio nem trivial por definição** (exige caso a caso sobre `satisfeita C x`). Confere.
2. `o_custo_e_o_numero_de_falsos` (REV20:74-88) — `custoCNF φ x = Σ (1 − leiNaClausula C x)`. Reescrita genuína de `countP` (TraducaoTuring.lean:1049) por indução; não é definição. Confere.
3. `o_nome_e_onde_a_lei_da_verdadeiro` (REV20:90-98) — `custoCNF φ x = 0 ↔ ∀ C ∈ φ, leiNaClausula C x = 1`, via `custoCNF_zero_sse` (TraducaoTuring.lean:1057) + item 1. Confere; a docstring matemática é exata (o título "O NOME É ONDE…" é o vocabulário do operador, declarado como tal no cabeçalho, linha 8).
4. `sat_e_existir_onde_a_lei_da_verdadeiro` (REV20:100-109) — `SAT φ ↔ ∃ x, ∀ C ∈ φ, leiNaClausula C x = 1`. É a definição de `SAT` (TraducaoTuring.lean:1064) reescrita pelo item 1 — passo quase direto, mas a docstring o declara com honestidade ("É o existencial da própria definição da classe NP [KNOWN], escrito sobre a lei"). Confere; não vende mais do que é.
5. `o_operador_do_custo_conta_os_falsos` (REV20:111-115) — `opDaInstancia_single` (TraducaoTuring.lean:123) com o custo reescrito pelo item 2. O cabeçalho (linha 33-35) declara que o item 5 é "leitura de definições e de lemas do kernel" — sem inflação. Confere.
6. `o_leitor_decai_por_falso` (REV20:117-122) — `trava_ofLp` (TraducaoTuring.lean:476) com o item 2; `e^{−s}` elevado ao número de falsos = `exp(−(s·k))`, que é o termo provado. Confere.

Nenhum teorema vazio, nenhum verdadeiro-por-definição vendido como resultado, nenhum enfeite.

### REV21 — 11/11 conferem (contas refeitas pelo revisor)

1. `a_forma_de_minkowski_e_o_determinante` (REV21:77-83) — `det !![t+z, x−iy; x+iy, t−z] = t²−z²−(x²+y²)`. Refeita a conta: exato. "O sinal de menos sai do determinante; não é posto" — correto: `herm4` (REV21:73-75) não contém sinal. Confere.
2. `a_forma_e_preservada_por_determinante_um` (REV21:85-87) — `det(A X Aᴴ) = det A · det X · conj(det A)`; com `det A = 1` fecha. Vale para todo `X` (mais geral que hermitiano). Cabeçalho o classifica como "lema de determinantes" — honesto. Confere.
3. `a_anatomia_do_gerador_da_face` (REV21:91-95) — `−(1−P) = −½·𝟙 + ½·(2P−1)`: álgebra pura, sem hipóteses sobre `P`, como a docstring declara ("Vale para toda matriz P"). Confere.
4. `o_gerador_de_boost_tem_quadrado_um` (REV21:97-104) — `(2P−1)² = 4P²−4P+1 = 1` sob `P*P = P`. Confere.
5. `o_gerador_de_boost_tem_traco_zero` (REV21:106-109) — `tr(2P−1) = 2·1 − 2 = 0` sob `tr P = 1` (em 2×2 `tr 𝟙 = 2`). Confere.
6. `a_rotacao_e_menos_i_vezes_o_boost` (REV21:126-128) — conjunção de três `rfl`. **É verdadeiro por definição**, e a docstring o declara: "(por definição)". Não é vendido como resultado no corpo; ver achado R21-3 sobre a ★ do cabeçalho.
7. `os_boosts_fecham_com_o_sinal_de_lorentz` (REV21:130-134) — `[Kx,Ky] = (i/2)σz` via `pauli_xy`/`pauli_yx` (SitePauliObservables.lean:178,184) e `−Jz = (i/2)σz`. Refeita a conta: exato, o sinal de Lorentz é o enunciado. Confere.
8. `as_rotacoes_fecham_com_o_sinal_oposto` (REV21:136-143) — `[Jx,Jy] = (−i)²[Kx,Ky] = −(−Jz) = Jz`. Confere.
9. `o_fluxo_do_lock_e_dilatacao_vezes_boost` (REV21:147-175) — refeita a conta: `e^{−s/2}cosh(s/2) = (1+e^{−s})/2`, `e^{−s/2}sinh(s/2) = (1−e^{−s})/2`, logo RHS = `e^{−s}·𝟙 + (1−e^{−s})·P = P + e^{−s}(1−P) = axiomFlow P s` (TheAxiomAndTheFalseWitness.lean:104). A igualdade é exata para **toda** matriz `P`. Confere — com ressalva de leitura no cabeçalho (achado R21-1).
10. `o_fluxo_do_lock_no_nome_do_eixo_z` (REV21:180-185) — `nomeZ = diag(1,0)` ⇒ fluxo = `diag(1, e^{−s})`. Confere.
11. `o_fluxo_do_lock_preserva_a_forma_a_menos_da_dilatacao` (REV21:187-195) — `det(F X Fᴴ) = det F · conj(det F) · det X = (e^{−s})²·det X`, com `F` real diagonal. Confere.

---

## 3. Alcance dos cabeçalhos

### REV20
Afirma: a lei lida cláusula a cláusula, o custo como contagem de falsos, o existencial de SAT sobre a lei, e os dois lemas operador/trava reescritos. **Não** afirma: a contagem do ato de leitura em passos da TM do Mathlib (`TM2ComputableInPolyTime`), as identificações sem termo (matemática=psíon, par=lógica, projeção=física, nome=TGL — exatamente o restante do verbatim), nada sobre a natureza. A frase "É nesse sentido, e só nele, que este arquivo dá face de kernel à frase de que o leitor é a matemática" delimita o alcance com precisão. **Nenhuma frase deixa entender mais do que os termos provam.**

### REV21
Afirma, no alcance da face 2×2: o determinante como forma, a anatomia do gerador, os dois fechamentos de comutador, o fluxo como dilatação × forma hiperbólica, e a preservação da forma a menos da dilatação. **Não** afirma: o mapa 2×2→4×4 para os boosts da representação definidora (v63), os três vínculos como os três boosts, termos de salto, positividade completa, o contínuo, nada sobre a natureza. Bloco da literatura marcado "[KNOWN; citado de memória, a conferir na fonte]" — honesto. Duas frases pedem ajuste (achados R21-1 e R21-2 abaixo).

---

## 4. Voz do operador × voz da gerência; citações

Aspas angulares (« »): **não há nenhuma ocorrência nas duas candidatas** (varredura sem resultado); as referências são por prefixo de nome de arquivo. Os dois arquivos de cunhagem existem e têm exatamente uma linha cada.

- REV20 linhas 13-16 → `OPERADOR_16nov_na_lingua_de_turing_o_leitor_e_a_matematica_..._verbatim.txt` (1 linha). A paráfrase confere: "na língua de turing o leitor é a matemática", "não há matemática sem o espelhamento lógico da identidade preservada". A fórmula `{[1=1=VERDADEIRO][1=0=FALSO]}` (REV20 linha 14) **confere byte a byte** com o verbatim. A omissão do superlativo "QUE é a lei mais importante da física" não distorce. **Voz correta: o que é atribuído ao operador está por bytes na fala dele.**
- REV21 linhas 13-16 → `OPERADOR_16nov_a_forma_de_minkowski_e_os_geradores_de_boost_nao_sao_os_operadores_de_lindblad_..._verbatim.txt` (1 linha). A pergunta "Ele perguntou se não são os operadores de Lindblad" confere com o verbatim ("…não são os operadores de lindblad?"). **Voz da pergunta correta.** Porém a frase anterior — "a gerência disse ao operador que … entram por definição, escritos à mão" — **não está por bytes no arquivo citado** (que contém só a pergunta e "de resto concordo com tudo"); ver achado R21-2. Não há inversão de voz (nada da gerência posto na boca do operador).

---

## 5. Achados por gravidade

### REV20 — nenhum achado com peso de ressalva

- **[INFORMATIVA] REV20 — `OLeitorEALei.lean:100-109`** — `sat_e_existir_onde_a_lei_da_verdadeiro` é a definição de `SAT` reescrita pelo item 1; conteúdo matemático mínimo. A docstring já o declara ("É o existencial da própria definição da classe NP [KNOWN], escrito sobre a lei"), logo não há inflação. Conserto: nenhum necessário; registrado para o orquestrador calibrar a ★.

### REV21 — duas ressalvas baixas (texto do cabeçalho), uma informativa

- **[BAIXA] REV21 — `BoostEDissipador.lean:39-40` (cabeçalho, item 5)** — "O fluxo sem salto do lock é uma dilatação `e^{−s/2}` vezes **a exponencial do gerador de boost**." A igualdade provada (REV21:148-175) vale para toda matriz `P`; já a leitura de `cosh(s/2)·𝟙 + senh(s/2)·(2P−1)` como exponencial `exp((s/2)(2P−1))` exige `(2P−1)² = 1`, i.e., `P` idempotente — hipótese **ausente do enunciado** do teorema 9 (disponível via REV21:98 quando posta). O termo prova a forma hiperbólica; a frase estende meio passo além. Conserto: "…vezes `cosh(s/2)·𝟙 + senh(s/2)·(2P−1)` — que, para `P` idempotente (quadrado um, item 3), é a exponencial do gerador de boost".
- **[BAIXA] REV21 — `BoostEDissipador.lean:13-16` (cabeçalho)** — "Em 16/11/2026 **a gerência disse ao operador que** … a forma de Minkowski (o sinal de menos) e os geradores de boost entram por definição, escritos à mão." O arquivo de cunhagem citado nas linhas 15-16 contém apenas a pergunta do operador e "de resto concordo com tudo"; a afirmação atribuída à gerência não tem respaldo por bytes nesse arquivo [DECLARADO pela gerência — a conferir na fonte da fala da gerência]. Conserto: citar também a cunhagem da gerência com a afirmação, ou marcar a frase como contexto declarado.
- **[INFORMATIVA] REV21 — `BoostEDissipador.lean:35-37` e `126-128`** — `a_rotacao_e_menos_i_vezes_o_boost` é três `rfl`; a docstring é honesta ("(por definição)"), mas o cabeçalho o agrupa sob a ★ do item 4 junto com os dois fechamentos, que têm conteúdo. Conserto opcional: separar a ★ ("★ os_boosts…, as_rotacoes…; a_rotacao… por definição").
- **[INFORMATIVA] REV21 — `BoostEDissipador.lean:25`** — "a anatomia do `A_C` no Atlas (face `−(1 − P)`, núcleo `−½·𝟙`)": referência ao Atlas não verificada nesta revisão [DECLARADO pela gerência]; o termo provado neste arquivo é só a decomposição algébrica (REV21:93-95).

---

## 6. Lista do conferido, com logs

| Item | Resultado | Evidência |
|---|---|---|
| sha16 REV20 / REV21 | conferem com a ordem | hash próprio, §abertura |
| Recompilação REV20 | exit 0, 73 s, stderr vazio | `V3_Kimi\copias\REV20\rev20_out.txt`, `rev20_err.txt` |
| Recompilação REV21 | exit 0, 64 s, stderr vazio | `V3_Kimi\copias\REV21\rev21_out.txt`, `rev21_err.txt` |
| Axiomas dos 17 teoremas | só `propext, Classical.choice, Quot.sound`; sem `sorryAx` | logs acima |
| `sorry`/`admit`/`axiom` nos fontes | ausentes | varredura grep (§1) |
| Lemas do kernel usados | `truthValue`(:24), `truthValue_table`(:26-28), `custoCNF`(:1049), `custoCNF_cons`(:1051), `custoCNF_zero_sse`(:1057), `SAT`(:1064), `opDaInstancia_single`(:123), `trava_ofLp`(:476), `axiomFlow`(:104), `pauli_xy`(:178), `pauli_yx`(:184) — todos existem com os enunciados usados | leitura de `C:\t\k411c\final\TGLExt\{TheEquationOfTruth,TraducaoTuring,TheAxiomAndTheFalseWitness,SitePauliObservables}.lean` |
| Enunciado × docstring | 6/6 e 11/11 conferem; contas de REV21 refeitas à mão | §2 |
| Aspas angulares | nenhuma nas duas candidatas | varredura grep (§4) |
| Cunhagem REV20 | verbatim confere; fórmula da lei byte a byte; voz do operador correta | `cunhagens_13out\OPERADOR_16nov_na_lingua_de_turing_..._verbatim.txt` (1 linha) |
| Cunhagem REV21 | pergunta do operador confere; fala prévia da gerência sem bytes no arquivo citado [DECLARADO] | `cunhagens_13out\OPERADOR_16nov_a_forma_de_minkowski_..._verbatim.txt` (1 linha) |

Ferramenta: `lean.exe` 4.31.0 (`leanprover--lean4---v4.31.0`), sem `lake build`; LEAN_PATH sobre `C:\t\k411c\final`. Cópias e logs em `revisao_orquestrador\V3_Kimi\copias\`. Nenhuma escrita fora da pasta de trabalho do revisor e deste relatório.
