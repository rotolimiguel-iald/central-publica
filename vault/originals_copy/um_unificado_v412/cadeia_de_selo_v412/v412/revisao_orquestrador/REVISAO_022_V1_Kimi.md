APROVADO_COM_RESSALVAS

# REVISÃO 022 — V1 — revisor Kimi

Unidade: candidata `MinimoFuncionalDeEnergia` (R1), revisão do que a gerência produziu na noite de 16/11 para fechar a v412.
Fonte revista: `candidatas_c1\REV22\MinimoFuncionalDeEnergia.lean` — sha256 `6918426af123402583adbecbaf0ae0352b27735965dc466c81318488f40bf414` (sha16 `6918426af1234025`, como na ordem), idêntica byte a byte à fonte viva `candidatas_c1\MinimoFuncionalDeEnergia.lean` de onde o log da gerência foi gerado (diff vazio).
Revisão distinta, formada por mim: não li `REVISAO_022_*_Codex*.md` nem parecer nenhum sobre esta unidade; li o meu `REVISAO_018_U7_Kimi.md` (R0), que as emendas dizem responder. Trabalho em `revisao_orquestrador\V1_Kimi\`. Não executei a ORDEM 021 (em espera).
[DECLARADO por mim até a gerência conferir na fonte.]

## Achados

### ALTO
Nenhum.

### MÉDIO
Nenhum.

### BAIXO

**B1 — O exemplo-parêntese «c ≡ 1 num ponto só» comporta uma leitura falsa.**
`MinimoFuncionalDeEnergia.lean:54` — «Sem ela, o único minimizador é o vetor nulo (com `c ≡ 1` num ponto só, a energia vale 1 em todo estado de norma 1)». A única leitura verdadeira é a do espaço de UM ponto com `c ≡ 1` (aí `E(v) = ‖v‖² = 1` nos estados de norma 1). Mas «num ponto só» também se lê como «`c = 1` em apenas um ponto de um `X` maior» — e nessa leitura a frase é falsa: os pontos com `c = 0` dão energia zero a estados de norma 1 neles suportados. A constância marcada por «`c ≡ 1`» força a primeira leitura, mas só depois de reler.
Conserto: trocar por «com `|X| = 1` e `c ≡ 1`» ou «no espaço de um ponto, com `c ≡ 1`».

## Respostas às perguntas da ordem

**1. Cada teorema novo diz o que a docstring diz — sim, os seis.** Recompilei em cópia própria (log no fim); `#print axioms` um a um; enunciado contra docstring:

- `a_energia_zero_fora_do_vetor_nulo_exige_custo_zero` (:215; doc :213-214): `(hv : v ≠ 0) → re⟪v, opDaInstancia c v⟫ = 0 → ∃ x, c x = 0`. É exatamente a docstring. ✓
- `a_penalidade_dos_vinculos_e_o_operador_do_custo` (:264; doc :262-263): sob `∀ j x, cj j x ≤ 1` — os «vínculos de custo 0 ou 1» da docstring —, `penalty (fun j => opDaInstancia (cj j)) = opDaInstancia (fun x => ∑ j, cj j x)`. ✓ A hipótese binária é necessária e está usada: a prova fecha coordenada a coordenada por `d² = d` (`Nat.le_one_iff_eq_zero_or_eq_one`, :278-280); para vínculo de custo 2, `D†D` daria 4 ≠ 2. A docstring não promete mais que o binário.
- `o_custo_da_formula_e_a_soma_das_ocorrencias` (:288; doc :287): `custoCNF φ x = ∑ j : Fin φ.length, custoDaOcorrencia φ j x`. ✓ Os dois lados contam ocorrências com multiplicidade (`countP` de um lado, `Fin φ.length` do outro): cláusula repetida conta de novo nos dois, como a docstring de `custoDaOcorrencia` (:282-283) declara.
- `o_operador_do_custo_da_formula_e_a_penalidade_das_clausulas` (:306; doc :304-305): `opDaInstancia (custoCNF φ) = penalty (fun j : Fin φ.length => opDaInstancia (custoDaOcorrencia φ j))` — o lema geral instanciado nos vínculos das ocorrências, via o teorema da soma. ✓
- `a_seletora_da_formula_e_a_seletora_apofatica` (:315; doc :314): `seletora (custoCNF φ) = -penalty (...)`. «Termo a termo» é literal: o lado direito É o termo `-penalty D` de `TheEquationOfTruth` — o mesmo que aparece em `selector_nonpos` (kernel :103-104), cuja docstring é «A seletora apofatica A_C = −H». ✓
- `o_nome_da_formula_e_a_intersecao_dos_nucleos` (:322; doc :320-321): `(opDaInstancia (custoCNF φ)).ker = ⨅ j, (opDaInstancia (custoDaOcorrencia φ j)).ker`, por `ker_penalty` (kernel :66-79 — cuja docstring é «uma violacao nao compensa outra», a frase que a docstring da candidata repete). ✓

**2. A ponte é a que faltava, e a escolha por ocorrência não esvazia — é a única que a torna verdadeira.** Argumento, não impressão:
(i) A igualdade liga objetos definidos independentemente no kernel: `opDaInstancia (custoCNF φ)` (a diagonal do custo SAT, `TraducaoTuring` :116-117 e :1049) e `penalty D` (a forma `Σ D†D`, `TheEquationOfTruth` :51-52). Não é definição disfarçada: `custoDaOcorrencia` é def nova, mas o que a liga a `custoCNF` é teorema provado por indução na lista (:288-302, com o `add_comm` final mostrando que não é defeq), e o que a liga à `penalty` é teorema provado por extensão na base ortonormal com o passo `d² = d`.
(ii) A indexação por OCORRÊNCIA (`Fin φ.length`) é forçada pela semântica de `custoCNF` (`List.countP`, que conta com multiplicidade, kernel :1049). Com índice por cláusula sem repetição, a igualdade seria FALSA para fórmula com cláusula repetida: o custo conta duas vezes, a penalty contaria uma. A escolha que esvaziaria seria a contrária.
(iii) O conteúdo é o declarado e não mais: para vínculos 0/1, `D_j` é a projeção diagonal das atribuições que violam a cláusula `j`, `D†D = D`, e `Σ D†D = Σ D` é a diagonal do número de violações. O «O que NÃO se afirma» (:82-85) continua a excluir a identificação com a bancada 80_/92_/128_ — agora com a frase correta: «a forma `A_C = −Σ D†D` é agora a mesma por teorema, a identificação entre as duas realizações não é construída».
(iv) É o lema que o meu B2 da U7 pediu (`opDaInstancia (fun y => ∑ j, cj j y) = penalty …`), com a hipótese binária que o meu esboço não escrevia e que é matematicamente exigida — a R1 é mais precisa que o meu conserto proposto.

**3. O cabeçalho atende às três baixas do meu U7 e às duas médias citadas do Codex, sem dizer mais que os termos.**
- Kimi B1 (glosa do referente): :17-20 — «A fala não nomeia arquivo nenhum: é a gerência que lê “o leitor que pousa e retorna” como o leitor da candidata `CamadaCientifica`, por ser ela a que prova o pouso e o retorno.» A glosa saiu da voz do operador e está assinada pela gerência. ATENDIDA.
- Kimi B2 (lacuna interna `opDaInstancia = penalty` não nomeada): fechada por construção (itens 7 e 8) — mais forte que o conserto proposto, que pedia o lema OU uma frase; o que resta fora (bancada) segue declarado (:82-84). ATENDIDA. (Quanto a «que os dois apontaram como passo faltante», :10: pela minha parte confere, B2 do meu U7; a parte do Codex não conferi — não leio o parecer dele.)
- Kimi B3 (pré-ponte binária subdeclarada): :32-35 nomeia as duas peças com os nomes certos — conferi: `a_trava_binaria_e_o_fluxo_do_axioma` (`CamadaCientifica` :254-255: `trava c t v = axiomFlow P t v` para `c ≤ 1`) e `axiomFlow_eq_exp` (`TheAxiomAndTheFalseWitness` :161-163: `NormedSpace.exp ((-t) • (1 - P)) = axiomFlow P t`) — e restabelece o que é próprio: «o caso geral (custo natural qualquer), a forma de gerador (a derivada), os fatos de energia e a ponte». ATENDIDA.
- Codex M1 (trava linear vs. órbita normalizada): LINEAR em maiúsculas no item 1 (:42, «antes de qualquer normalização»); «Como ler» (:72-77) atribui o retorno à trava SEGUIDA da normalização (`a_trava_pousa_e_volta` — conferi: é a trava renormalizada, `(‖trava …‖)⁻¹ • trava …`, `CamadaCientifica` :482-493); «O que NÃO se afirma» (:85) nega que a trajetória normalizada tenha o A_C por gerador. ATENDIDA.
- Codex M2 (operador/funcional/valor mínimo/minimizadores): :39-40 separam os quatro objetos antes dos itens. ATENDIDA.
- Sem sobreleitura: a afirmação de ausência (:22-23) foi reconferida por mim hoje — 0 ocorrências de `truthFlow`, `EquationOfTruth`, `NormedSpace.exp` em `TraducaoTuring.lean` e `AEscala.lean` (sandbox k411c) e em `CamadaCientifica.lean` (candidatas_c1). Legenda de ★ honesta: os dois ★ novos (itens 7 e 8) são os de conteúdo próprio; os corolários novos (`a_energia_zero_…`, a soma, a seletora da fórmula, a interseção) vão sem ★. Os verbetes do Atlas citados (:25, :58) são os mesmos que conferi na R0, um termo por vez; as frases que os citam não mudaram, exceto a atualização correta do item da ponte.

**4. A frase da derivada da trajetória normalizada está certa e bem marcada.** :74-75. Refiz a conta: para `φ(s) = e^{−sH}ψ` e `χ = φ/‖φ‖`, `dχ/ds = −Hχ + re⟨χ,Hχ⟩χ` ao longo de toda a trajetória (em `s = 0` com `‖ψ‖ = 1` é a fórmula escrita); como aqui `H = opDaInstancia c` é auto-adjunto (`opDaInstancia_autoadjunto`, kernel :132-133), `⟨χ,Hχ⟩ ∈ ℝ` e o `re` cai fora — a forma `−Hψ + ⟨ψ,Hψ⟩ψ` é exata no contexto. A marca «[DERIVED; conta feita pelo revisor Codex; não é termo deste arquivo]» diz o que a frase é: fato derivado, fora dos termos deste arquivo — e o «O que NÃO se afirma» (:85) trava a conclusão certa (a trajetória normalizada NÃO tem o A_C por gerador). A atribuição da conta ao Codex não conferi (não leio os pareceres dele); a conta e a marcação, sim.

## O que conferi (lista)

1. Hashes: REV22 e fonte viva `candidatas_c1\` — sha256 `6918426af1234025…bf414` nas duas, diff vazio entre elas. Recibo `RESULTADO_MinimoFuncionalDeEnergia.json` com o mesmo sha256, RC 0, 17 teoremas, `todos_so_o_trio`, `sorryAx: false`, defs `seletora` + `custoDaOcorrencia` — tudo batendo com a minha recompilação.
2. Recompilação em cópia própria: fonte e `compilar_candidata.ps1` copiados para `V1_Kimi\`; `lean.exe` 4.31.0 (commit 68218e876d2a38b1985b8590fff244a83c321783) sobre os `.olean` de `C:\t\k411c\final` (build/lib/lean + packages), sem lake, sem tocar nas pastas da gerência. RC 0, 82 s; a saída contém SOMENTE as respostas dos 17 `#print axioms`, todas `[propext, Classical.choice, Quot.sound]`; zero avisos, zero erros. Log: `V1_Kimi\build\MinimoFuncionalDeEnergia.log` (INICIO 2026-11-16 19:42:06, FIM 19:43:28, sha da fonte registrado igual). Conteúdo idêntico ao log da gerência (`candidatas_c1\build\MinimoFuncionalDeEnergia.log`, INICIO 19:13:55, FIM 19:14:25, RC 0) — só muda a janela de tempo.
3. Fonte sem `sorry`/`admit`/`axiom`/`native_decide`/`implemented_by`/`extern` fora do comentário da linha 89 («Sem sorry, sem axioma novo.»). 17 teoremas e 2 defs contados na fonte — bate com o recibo.
4. Enunciados do kernel lidos na fonte do sandbox: `penalty`, `re_inner_penalty`, `ker_penalty`, `isSelfAdjoint_penalty`, `selector_nonpos`, `truthFlow`, `T`, `hasDerivAt_flow_apply`, `T_apply_eigen`, `flowTendsToFamily_of_finiteDimensional` (`TheEquationOfTruth` :51-52, :60-63, :66-79, :95-100, :103-106, :178, :181, :375-378, :420-428, :432); `opDaInstancia`, `opDaInstancia_ofLp`, `opDaInstancia_single`, `opDaInstancia_autoadjunto`, `solucao_por_coordenadas`, `trava`, `trava_ofLp`, `travaOp`, `travaOp_apply`, `Literal`, `Clausula`, `CNF`, `satisfeita`, `custoCNF`, `custoCNF_cons` (`TraducaoTuring` :116-139, :237-259, :472-477, :982-987, :1034-1055).
5. Cruzamentos com `CamadaCientifica`: `a_trava_binaria_e_o_fluxo_do_axioma` (:254-269) e `a_trava_pousa_e_volta` (:482-497, a trava renormalizada); e `axiomFlow_eq_exp` (`TheAxiomAndTheFalseWitness` :161-163).
6. Ausência afirmada no cabeçalho reconferida: os três termos × os três artefatos = 0 ocorrências.
7. Diff R0→R1 na íntegra: cabeçalho retrabalhado nos pontos das cinco ressalvas, mais os seis teoremas novos, a def `custoDaOcorrencia` e os seis `#print axioms` correspondentes; os 11 teoremas da R0 e suas provas, intocados. O «o que mudou» declarado pela gerência bate com o diff.
8. Atlas: não reabri; os dois verbetes citados (`A_C (funcional-Amor)`, pedra 80_; `A_C — anatomia (128_)`) foram conferidos por mim na R0, um termo por vez, e as frases do cabeçalho que os citam são as mesmas.

Nada instalado, nada a provedor remoto, kernel lido e não tocado; nenhuma pasta `REV*` editada; o `.olean` gerado ficou só em `V1_Kimi\build\`.
