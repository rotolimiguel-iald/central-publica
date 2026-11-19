
/-! ====================  SEÇÃO DO REVISOR (c1-terceiro, 14/11/2026) — exemplos e verificações sobre a candidata  ==================== -/

namespace TGLExt.NomeComoCodigo.Revisao
open TGLExt.NomeComoCodigo
open TGLExt.TraducaoTuring

/-! ### Item 2 — VACUIDADE: o código de repetição em Fin 3 → Bool -/

/-- custo do código de repetição: zero exatamente em 000 e 111, um nas outras seis leituras. -/
def rep3 : (Fin 3 → Bool) → ℕ := fun x => if x = (fun _ => false) ∨ x = (fun _ => true) then 0 else 1

theorem rep3_hsep : ∀ s s' : Fin 3 → Bool, rep3 s = 0 → rep3 s' = 0 → s ≠ s' → 3 ≤ hammingDist s s' := by
  decide

/-- o exemplo concreto: hsep NÃO é vazia, e o teorema dispara no código de repetição. -/
example (j : Fin 3) : leitorDosVizinhos rep3 (empurrao (fun _ => false) j) = (fun _ => false) :=
  o_leitor_dos_vizinhos_desfaz_o_empurrao rep3 rep3_hsep _ (by decide) j

example (j : Fin 3) : leitorDosVizinhos rep3 (empurrao (fun _ => true) j) = (fun _ => true) :=
  o_leitor_dos_vizinhos_desfaz_o_empurrao rep3 rep3_hsep _ (by decide) j

/-- o mesmo código, escrito como FÓRMULA CNF (x0→x1, x1→x2, x2→x0): o custo da fórmula é zero exatamente em 000 e 111. -/
def lit (i : Fin 3) (b : Bool) : Literal 3 := ⟨i, b⟩
def ciclo : CNF 3 := [[lit 0 false, lit 1 true], [lit 1 false, lit 2 true], [lit 2 false, lit 0 true]]

theorem ciclo_hsep : ∀ s s' : Fin 3 → Bool, custoCNF ciclo s = 0 → custoCNF ciclo s' = 0 → s ≠ s' → 3 ≤ hammingDist s s' := by
  decide

example (j : Fin 3) : leitorDosVizinhos (custoCNF ciclo) (empurrao (fun _ => false) j) = (fun _ => false) :=
  para_uma_formula ciclo ciclo_hsep _ (by decide) j

/-! ### Item 2 — hsep FALHA (distância 2): o que deixa de valer -/

/-- fórmula x0 = 0 ∧ (x1 ↔ x2): soluções 000 e 011, a distância 2. -/
def dois : CNF 3 := [[lit 0 false], [lit 1 false, lit 2 true], [lit 2 false, lit 1 true]]

theorem dois_hsep_falha : ¬ (∀ s s' : Fin 3 → Bool, custoCNF dois s = 0 → custoCNF dois s' = 0 → s ≠ s' → 3 ≤ hammingDist s s') := by
  decide

/-- a falha é de FATO, não de método: o estado 010 é o empurrão de 000 (asserção 1) E o empurrão de 011 (asserção 2); logo NENHUM leitor
    (função do estado, de qualquer espécie, com a regra ou sem ela) devolve os dois. -/
theorem nenhum_leitor_desfaz_a_distancia_dois (f : (Fin 3 → Bool) → (Fin 3 → Bool)) :
    ¬ (f (empurrao (fun _ => false) 1) = (fun _ => false) ∧ f (empurrao ![false, true, true] 2) = ![false, true, true]) := by
  have e : empurrao (fun _ : Fin 3 => false) 1 = empurrao ![false, true, true] 2 := by decide
  rintro ⟨h1, h2⟩
  rw [e] at h1
  have := h1.symm.trans h2
  revert this
  decide

/-- o enunciado que o teorema perde: com a distância 2, o estado 010 tem DUAS leituras válidas a uma troca (000 e 011) — a conclusão
    `y = s` de `o_empurrao_tem_um_so_retorno` é falsa. -/
theorem dois_duas_vizinhas_validas :
    custoCNF dois (fun _ => false) = 0 ∧ custoCNF dois ![false, true, true] = 0 ∧
    hammingDist (empurrao (fun _ : Fin 3 => false) 1) ![false, true, true] ≤ 1 ∧
    (![false, true, true] : Fin 3 → Bool) ≠ (fun _ => false) := by
  decide

/-! ### Item 2 — Nome com zero ou um ponto -/

/-- Nome vazio (custo 1 em toda parte): hsep vale por vacuidade, `hs` nunca é satisfeita, e o leitor é a identidade. -/
theorem nome_vazio_hsep (n : ℕ) :
    ∀ s s' : Fin n → Bool, (fun _ : Fin n → Bool => (1 : ℕ)) s = 0 → (fun _ : Fin n → Bool => (1 : ℕ)) s' = 0 → s ≠ s' → 3 ≤ hammingDist s s' :=
  fun s s' h _ _ => absurd h (by simp)

theorem nome_vazio_leitor_e_identidade (n : ℕ) (x : Fin n → Bool) : leitorDosVizinhos (fun _ : Fin n → Bool => (1 : ℕ)) x = x := by
  unfold leitorDosVizinhos
  rw [if_neg (by simp), dif_neg (by simp)]

/-- Nome de UM ponto x0: hsep vale por vacuidade, e o teorema afirma o retorno ao único ponto. -/
theorem nome_de_um_ponto (n : ℕ) (x0 : Fin n → Bool) (j : Fin n) :
    leitorDosVizinhos (fun x => if x = x0 then (0 : ℕ) else 1) (empurrao x0 j) = x0 := by
  refine o_leitor_dos_vizinhos_desfaz_o_empurrao _ ?_ x0 (by simp) j
  intro s s' hs hs' hne
  have h1 : s = x0 := by
    by_contra h; rw [if_neg h] at hs; exact absurd hs (by decide)
  have h2 : s' = x0 := by
    by_contra h; rw [if_neg h] at hs'; exact absurd hs' (by decide)
  exact absurd (h1.trans h2.symm) hne

/-! ### Item 3 — O LEITOR LÊ SÓ PELA REGRA? -/

theorem choose_congr' {n : ℕ} {p q : Fin n → Prop} (e : p = q) (hp : ∃ a, p a) (hq : ∃ a, q a) : hp.choose = hq.choose := by
  subst e; rfl

/-- LOCALIDADE: o leitor depende de `c` SÓ por duas coisas: se a própria leitura tem custo zero e quais das n vizinhas têm custo zero.
    (Não depende da grandeza do custo, nem de nenhum outro ponto, nem de hsep.) -/
theorem o_leitor_so_ve_o_zero_do_custo_na_leitura_e_nas_vizinhas {n : ℕ} (c c' : (Fin n → Bool) → ℕ) (x : Fin n → Bool)
    (h0 : c x = 0 ↔ c' x = 0) (hn : ∀ j, c (empurrao x j) = 0 ↔ c' (empurrao x j) = 0) :
    leitorDosVizinhos c x = leitorDosVizinhos c' x := by
  unfold leitorDosVizinhos
  by_cases hx : c x = 0
  · rw [if_pos hx, if_pos (h0.mp hx)]
  · have hx' : c' x ≠ 0 := fun h => hx (h0.mpr h)
    rw [if_neg hx, if_neg hx']
    by_cases hex : ∃ j, c (empurrao x j) = 0
    · have hex' : ∃ j, c' (empurrao x j) = 0 := hex.imp (fun j hj => (hn j).mp hj)
      rw [dif_pos hex, dif_pos hex']
      have e : (fun j => c (empurrao x j) = 0) = (fun j => c' (empurrao x j) = 0) := funext (fun j => propext (hn j))
      rw [choose_congr' e hex hex']
    · have hex' : ¬ ∃ j, c' (empurrao x j) = 0 := fun ⟨j, hj⟩ => hex ⟨j, (hn j).mpr hj⟩
      rw [dif_neg hex, dif_neg hex']

/-- corolário: o leitor só usa o VERIFICADOR (custo zero ou não), nunca a grandeza do custo. -/
theorem o_leitor_usa_so_o_verificador {n : ℕ} (c : (Fin n → Bool) → ℕ) (x : Fin n → Bool) :
    leitorDosVizinhos c x = leitorDosVizinhos (fun y => if c y = 0 then 0 else 1) x :=
  o_leitor_so_ve_o_zero_do_custo_na_leitura_e_nas_vizinhas _ _ x (by by_cases h : c x = 0 <;> simp [h])
    (fun j => by by_cases h : c (empurrao x j) = 0 <;> simp [h])

/-- DETERMINAÇÃO: sob hsep, o `Exists.choose` não escolhe nada às cegas: toda vizinha que resolve é a que o leitor escolhe. -/
theorem o_leitor_nao_escolhe_as_cegas {n : ℕ} (c : (Fin n → Bool) → ℕ)
    (hsep : ∀ s s' : Fin n → Bool, c s = 0 → c s' = 0 → s ≠ s' → 3 ≤ hammingDist s s')
    (x : Fin n → Bool) (hx : c x ≠ 0) (j : Fin n) (hj : c (empurrao x j) = 0) :
    leitorDosVizinhos c x = empurrao x j := by
  have hex : ∃ j', c (empurrao x j') = 0 := ⟨j, hj⟩
  unfold leitorDosVizinhos
  rw [if_neg hx, dif_pos hex]
  by_contra hne
  have h3 := hsep _ _ hex.choose_spec hj hne
  have d1 := empurrao_dista_um x hex.choose
  have d2 := empurrao_dista_um x j
  have htri := hammingDist_triangle (empurrao x hex.choose) x (empurrao x j)
  have hc := hammingDist_comm (empurrao x hex.choose) x
  omega

/-! ### Item 4(b) — o leitor FICA PARADO para sempre fora da vizinhança do Nome (e não é `LeitorDeUmaConfiguracao`) -/

/-- código de repetição em 4 bits: zero em 0000 e 1111; hsep vale (distância 4). -/
def rep4 : (Fin 4 → Bool) → ℕ := fun x => if x = (fun _ => false) ∨ x = (fun _ => true) then 0 else 1

theorem rep4_hsep : ∀ s s' : Fin 4 → Bool, rep4 s = 0 → rep4 s' = 0 → s ≠ s' → 3 ≤ hammingDist s s' := by
  decide

/-- 1100 está a distância 2 de 0000 e de 1111: nenhuma vizinha resolve; o leitor não sai do lugar, com custo 1 > 0. -/
theorem o_leitor_fica_parado_fora_da_vizinhanca :
    rep4 ![true, true, false, false] ≠ 0 ∧ leitorDosVizinhos rep4 ![true, true, false, false] = ![true, true, false, false] := by
  refine ⟨by decide, ?_⟩
  unfold leitorDosVizinhos
  rw [if_neg (by decide), dif_neg (by decide)]

/-- e portanto o passo NÃO consome o custo: a condição `consome` do tipo `LeitorDeUmaConfiguracao` da candidata principal falha. -/
theorem o_leitor_dos_vizinhos_nao_consome_o_custo :
    ¬ (∀ x : Fin 4 → Bool, rep4 x ≠ 0 → rep4 (leitorDosVizinhos rep4 x) < rep4 x) := by
  intro h
  have h1 := h ![true, true, false, false] o_leitor_fica_parado_fora_da_vizinhanca.1
  rw [o_leitor_fica_parado_fora_da_vizinhanca.2] at h1
  exact lt_irrefl _ h1

/-! ### Item 4(c) — uma fórmula com solução e uma variável que não aparece NUNCA tem hsep -/

/-- a fórmula vazia sobre 3 variáveis: toda leitura resolve; hsep falha. (O caso geral — variável livre — dá o mesmo: empurrar a variável
    livre de uma solução é outra solução, a distância 1.) -/
theorem formula_vazia_hsep_falha : ¬ (∀ s s' : Fin 3 → Bool, custoCNF ([] : CNF 3) s = 0 → custoCNF ([] : CNF 3) s' = 0 → s ≠ s' → 3 ≤ hammingDist s s') := by
  decide

end TGLExt.NomeComoCodigo.Revisao

#print axioms TGLExt.NomeComoCodigo.Revisao.rep3_hsep
#print axioms TGLExt.NomeComoCodigo.Revisao.ciclo_hsep
#print axioms TGLExt.NomeComoCodigo.Revisao.dois_hsep_falha
#print axioms TGLExt.NomeComoCodigo.Revisao.nenhum_leitor_desfaz_a_distancia_dois
#print axioms TGLExt.NomeComoCodigo.Revisao.dois_duas_vizinhas_validas
#print axioms TGLExt.NomeComoCodigo.Revisao.nome_vazio_hsep
#print axioms TGLExt.NomeComoCodigo.Revisao.nome_vazio_leitor_e_identidade
#print axioms TGLExt.NomeComoCodigo.Revisao.nome_de_um_ponto
#print axioms TGLExt.NomeComoCodigo.Revisao.o_leitor_so_ve_o_zero_do_custo_na_leitura_e_nas_vizinhas
#print axioms TGLExt.NomeComoCodigo.Revisao.o_leitor_usa_so_o_verificador
#print axioms TGLExt.NomeComoCodigo.Revisao.o_leitor_nao_escolhe_as_cegas
#print axioms TGLExt.NomeComoCodigo.Revisao.rep4_hsep
#print axioms TGLExt.NomeComoCodigo.Revisao.o_leitor_fica_parado_fora_da_vizinhanca
#print axioms TGLExt.NomeComoCodigo.Revisao.o_leitor_dos_vizinhos_nao_consome_o_custo
#print axioms TGLExt.NomeComoCodigo.Revisao.formula_vazia_hsep_falha
