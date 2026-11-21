import TGLExt.AContagemEACarga
import TGLExt.AMaquinaEALeitura

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# A ponte de Cook–Levin: a máquina da casa roda na fita, e o custo é o número de letras

[candidata do Kimi, 19/11/2026, R0; nome PROVISÓRIO — o nome é do operador; nada instalado; ainda não lida por
revisor]

## De onde vem

A gerência deixou para a v413: «Provar que a máquina da casa roda na máquina padrão do Mathlib com custo polinomial.
Com isso, as classes acima entram em P na língua clássica e SAT entra em NP. O teorema de Cook–Levin em si entra por
citação, pela regra de 27/09.» O operador pediu em 19/11: «prossiga para a tradução completa de Cook–Levin». Este
arquivo constrói a ponte: a máquina da casa (o passo por cláusula de `AMaquinaEALeitura`) escrita como uma máquina de
fita, com o custo em movimentos contado exatamente.

## O que fica provado

1. `passoFita` e `a_maquina_da_casa_roda_na_fita`: a máquina de fita (a fórmula fixa, a cabeça que avança uma
   cláusula por passo, o registro, e o contador de movimentos) deixa no registro o custo da atribuição — o mesmo da
   máquina da casa (`AMaquinaEALeitura.a_maquina_conta_os_falsos`).
2. ★ `o_custo_na_fita_e_o_numero_de_letras`: os movimentos pagos são exatamente o número de letras da fórmula na
   fita (os literais mais um terminador por cláusula): a ponte não esconde custo.
3. ★ `a_decisao_na_fita_e_a_mesma`: a máquina de fita decide o mesmo que a máquina da casa (`a_maquina_e_uma_leitura_decidem`).
4. ★ `o_custo_da_ponte_e_polinomial`: os movimentos são lineares nas letras da entrada — polinomiais na entrada
   (grau 1). A máquina da casa roda na fita com sobrecarga nula além das letras.

(Auxiliares do laço, marcados como tais: `passoFita_na_posicao`, `custoCNF_append_singleton`,
`letras_append_singleton`, `take_succ_singleton`.)

## O que NÃO se afirma

* A ligação à máquina de Turing padrão do Mathlib (`Turing.TM2ComputableInPolyTime`): o modelo aqui é a máquina de
  fita da casa (a cabeça sobre a fórmula fixa); a tradução ao modelo do Mathlib é a próxima construção (o kernel
  mesmo registra que o Mathlib não tem Cook–Levin). Cook–Levin entra por citação, pela regra de 27/09
  [KNOWN, Cook 1971; Levin 1973].
* Nada sobre a Palavra de toda CNF plana em movimentos fixos de polinômio: a busca da proposta fica com o Instituto
  (as paredes de 18/11). O que esta ponte dá é a CORREÇÃO e o CUSTO da máquina da casa na fita — para decidir com a
  proposta dada (o certificado), e para as classes provadas.
* Nada sobre a natureza. O gate não se move; nada está instalado.

NOTA DO LAÇO (19/11/2026): `List.get?` não existe nesta versão do núcleo — o acesso à posição é `φ[c.pos]?` (a
notação `getElem?`). Só o corpo de `passoFita` mudou; o tipo e todos os enunciados ficam como escritos.

Sem sorry, sem axioma novo.
-/

namespace TGLExt.APonteDeCookLevin

open TGLExt TGLExt.TraducaoTuring TGLExt.AContagemEACarga TGLExt.AMaquinaEALeitura

variable {n : ℕ}

/-- [DEF] A configuração da máquina de fita: a posição da cabeça (a próxima cláusula), o registro (o custo
acumulado) e os movimentos pagos até aqui. -/
structure ConfigFita (n : ℕ) where
  pos : ℕ
  reg : ℕ
  mov : ℕ

/-- [DEF] O PASSO DA FITA: ler a cláusula na posição da cabeça; se está violada, somar 1 ao registro; avançar a
cabeça; e cobrar os movimentos da travessia (as letras da cláusula, mais o retorno). -/
def passoFita (φ : CNF n) (x : Fin n → Bool) (c : ConfigFita n) : ConfigFita n :=
  match φ[c.pos]? with
  | none => c
  | some C => ⟨c.pos + 1, c.reg + (if satisfeita C x then 0 else 1), c.mov + C.length + 1⟩

/-- [DEF] As letras da fórmula na fita: os literais mais um terminador por cláusula. -/
def letras (φ : CNF n) : ℕ := (φ.map List.length).sum + φ.length

/-- O custo da fórmula com uma cláusula a mais no fim: a soma do `if`. (Auxiliar do laço.) -/
theorem custoCNF_append_singleton {n : ℕ} (x : Fin n → Bool) (ψ : CNF n) (C : Clausula n) :
    custoCNF (ψ ++ [C]) x = custoCNF ψ x + (if satisfeita C x then 0 else 1) := by
  unfold custoCNF
  rw [List.countP_append]
  have h1 : List.countP (fun D => !satisfeita D x) [C] = (if satisfeita C x then 0 else 1) := by
    rw [List.countP_cons, List.countP_nil]
    by_cases h : satisfeita C x <;> simp [h]
  rw [h1]

/-- As letras da fórmula com uma cláusula a mais no fim. (Auxiliar do laço.) -/
theorem letras_append_singleton {n : ℕ} (ψ : CNF n) (C : Clausula n) :
    letras (ψ ++ [C]) = letras ψ + C.length + 1 := by
  unfold letras
  rw [List.map_append, List.map_cons, List.map_nil, List.sum_append, List.sum_cons, List.sum_nil,
    List.length_append, List.length_singleton]
  ring

/-- O take de `j+1` é o take de `j` mais a cláusula `j`. (Auxiliar do laço; a conta da irmã `OResumoEPsiBit`.) -/
theorem take_succ_singleton {n : ℕ} (φ : CNF n) {j : ℕ} (hj : j < φ.length) :
    φ.take (j + 1) = φ.take j ++ [φ[j]] := by
  rw [List.take_add_one, List.getElem?_eq_getElem hj, Option.toList_some]

/-- O passo da fita numa posição válida: o registro ganha o `if` da cláusula; os movimentos, as letras dela mais
um. (Auxiliar do laço.) -/
theorem passoFita_na_posicao (φ : CNF n) (x : Fin n → Bool) {j : ℕ} (hj : j < φ.length) (a b : ℕ) :
    passoFita φ x ⟨j, a, b⟩ = ⟨j + 1, a + (if satisfeita φ[j] x then 0 else 1), b + φ[j].length + 1⟩ := by
  unfold passoFita
  rw [show (⟨j, a, b⟩ : ConfigFita n).pos = j from rfl]
  rw [List.getElem?_eq_getElem hj]

/-- A cabeça para no fim da fórmula. -/
theorem passoFita_alem_do_fim (φ : CNF n) (x : Fin n → Bool) :
    passoFita φ x ⟨φ.length, custoCNF φ x, letras φ⟩ = ⟨φ.length, custoCNF φ x, letras φ⟩ := by
  unfold passoFita
  rw [show (⟨φ.length, custoCNF φ x, letras φ⟩ : ConfigFita n).pos = φ.length from rfl]
  rw [List.getElem?_eq_none (Nat.le_refl _)]

/-- ★ **A MÁQUINA DA CASA RODA NA FITA**: em tantos passos quantas são as cláusulas, a máquina de fita deixa no
registro o custo da atribuição, com os movimentos contados exatamente. -/
theorem a_maquina_da_casa_roda_na_fita (φ : CNF n) (x : Fin n → Bool) :
    ∀ r : ConfigFita n, (passoFita φ x)^[φ.length] ⟨0, r.reg, r.mov⟩
      = ⟨φ.length, r.reg + custoCNF φ x, r.mov + letras φ⟩ := by
  -- a invariante por indução: depois de j passos, a configuração é ⟨j, reg + custo do lido, mov + letras do lido⟩
  have hinv : ∀ j : ℕ, j ≤ φ.length → ∀ r : ConfigFita n,
      (passoFita φ x)^[j] ⟨0, r.reg, r.mov⟩
        = ⟨j, r.reg + custoCNF (φ.take j) x, r.mov + letras (φ.take j)⟩ := by
    intro j
    induction j with
    | zero =>
      intro _ r
      show (passoFita φ x)^[0] ⟨0, r.reg, r.mov⟩ = ⟨0, r.reg + custoCNF [] x, r.mov + letras []⟩
      simp [letras, custoCNF]
    | succ j ih =>
      intro hj r
      have hj' : j < φ.length := hj
      rw [Function.iterate_succ_apply', ih (Nat.le_of_succ_le hj) r, passoFita_na_posicao φ x hj',
        take_succ_singleton φ hj', custoCNF_append_singleton, letras_append_singleton]
      rw [ConfigFita.mk.injEq]
      exact ⟨rfl, by ring, by ring⟩
  intro r
  have h := hinv φ.length (Nat.le_refl _) r
  rwa [List.take_length] at h

/-- ★ **O CUSTO NA FITA É O NÚMERO DE LETRAS**: os movimentos pagos são exatamente as letras da fórmula na fita. -/
theorem o_custo_na_fita_e_o_numero_de_letras (φ : CNF n) (x : Fin n → Bool) :
    ((passoFita φ x)^[φ.length] ⟨0, 0, 0⟩).mov = letras φ := by
  have h : (passoFita φ x)^[φ.length] ⟨0, 0, 0⟩ = ⟨φ.length, 0 + custoCNF φ x, 0 + letras φ⟩ :=
    a_maquina_da_casa_roda_na_fita φ x ⟨0, 0, 0⟩
  rw [h]
  simp

/-- ★ **A DECISÃO NA FITA É A MESMA**: a máquina de fita, com o registro lido ao final, decide o que a máquina da
casa decide. -/
theorem a_decisao_na_fita_e_a_mesma (φ : CNF n) (x : Fin n → Bool) :
    ((passoFita φ x)^[φ.length] ⟨0, 0, 0⟩).reg = custoCNF φ x := by
  have h : (passoFita φ x)^[φ.length] ⟨0, 0, 0⟩ = ⟨φ.length, 0 + custoCNF φ x, 0 + letras φ⟩ :=
    a_maquina_da_casa_roda_na_fita φ x ⟨0, 0, 0⟩
  rw [h]
  simp

/-- ★ **O CUSTO DA PONTE É POLINOMIAL**: os movimentos da máquina de fita são exatamente as letras da entrada —
lineares na entrada, polinomiais de grau 1. -/
theorem o_custo_da_ponte_e_polinomial (φ : CNF n) (x : Fin n → Bool) :
    ∃ c : ℕ, ((passoFita φ x)^[φ.length] ⟨0, 0, 0⟩).mov ≤ c * letras φ := by
  refine ⟨1, ?_⟩
  rw [o_custo_na_fita_e_o_numero_de_letras, one_mul]

end TGLExt.APonteDeCookLevin

#print axioms TGLExt.APonteDeCookLevin.custoCNF_append_singleton
#print axioms TGLExt.APonteDeCookLevin.letras_append_singleton
#print axioms TGLExt.APonteDeCookLevin.take_succ_singleton
#print axioms TGLExt.APonteDeCookLevin.passoFita_na_posicao
#print axioms TGLExt.APonteDeCookLevin.passoFita_alem_do_fim
#print axioms TGLExt.APonteDeCookLevin.a_maquina_da_casa_roda_na_fita
#print axioms TGLExt.APonteDeCookLevin.o_custo_na_fita_e_o_numero_de_letras
#print axioms TGLExt.APonteDeCookLevin.a_decisao_na_fita_e_a_mesma
#print axioms TGLExt.APonteDeCookLevin.o_custo_da_ponte_e_polinomial
