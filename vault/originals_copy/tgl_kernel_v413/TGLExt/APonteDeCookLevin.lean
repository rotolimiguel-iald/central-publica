import TGLExt.AContagemEACarga
import TGLExt.AMaquinaEALeitura

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# O iterador cláusula a cláusula: o registro dá o custo de uma atribuição, e o custo cobrado é o número de letras

## O modelo

O iterador trabalha sobre uma fórmula `φ` e uma atribuição `x` dadas. A cabeça avança uma cláusula por passo
(`passoFita`); o registro soma 1 quando a cláusula lida está violada; o contador `mov` soma o custo abstrato cobrado
por definição: o comprimento da cláusula mais 1 (os literais mais um terminador). Cada passo lê a cláusula pelo
índice e a avalia sobre `x` de uma vez: `mov` não é contagem demonstrada de movimentos de uma máquina de fita.

## O que fica provado

1. `passoFita` e `a_maquina_da_casa_roda_na_fita`: em tantos passos quantas são as cláusulas, a partir da posição
   `0`, o registro ganha o custo da atribuição, `custoCNF φ x` (o mesmo de
   `AMaquinaEALeitura.a_maquina_conta_os_falsos`), e o contador `mov` ganha `letras φ`.
2. ★ `o_custo_na_fita_e_o_numero_de_letras`: a partir de `⟨0, 0, 0⟩`, o custo cobrado é `letras φ` (os literais mais
   um terminador por cláusula).
3. ★ `a_decisao_na_fita_e_a_mesma`: a partir de `⟨0, 0, 0⟩`, o registro final é `custoCNF φ x`: verifica o custo de
   UMA atribuição dada (aceita se `reg = 0`); não decide se a fórmula tem solução. O teorema
   `TGLExt.AMaquinaEALeitura.a_maquina_e_uma_leitura_decidem` trata da leitura do zero sobre a entrada inteira na máquina
   levantada; é objeto distinto desta verificação da atribuição `x`.
4. ★ `o_custo_da_ponte_e_polinomial`: o enunciado é: para cada `φ` e `x` existe `c` com `mov ≤ c · letras φ`; a prova
   usa `c = 1` para todos.

(Auxiliares do laço, marcados como tais: `passoFita_na_posicao`, `custoCNF_append_singleton`,
`letras_append_singleton`, `take_succ_singleton`.)

## O que NÃO se afirma

* Que este módulo seja uma ponte de Cook–Levin, ou que o custo cobrado conte movimentos de uma máquina de fita. A
  verificação da testemunha na máquina padrão do Mathlib (`Turing.TM2ComputableInPolyTime`) está em outros módulos
  (`TGLExt.APonteAoTM2`, `TGLExt.SimTM2.verificacao_tm2_polinomial`); a ponte das classes, com Cook–Levin como
  hipótese nomeada (`PonteCookLevin.CookLevin`), está em `TGLExt.PonteCookLevin` [KNOWN, Cook 1971; Levin 1973].
* Nada sobre a Palavra de toda CNF plana em número polinomial de passos: a busca da atribuição fica com a pergunta do
  Instituto.
* Nada sobre a natureza. O gate não se move.

Sem sorry, sem axioma novo.
-/

namespace TGLExt.APonteDeCookLevin

open TGLExt TGLExt.TraducaoTuring TGLExt.AContagemEACarga TGLExt.AMaquinaEALeitura

variable {n : ℕ}

/-- [DEF] A configuração do iterador: a posição da cabeça (a próxima cláusula), o registro (o custo acumulado) e o
contador `mov` (o custo abstrato cobrado até aqui). -/
structure ConfigFita (n : ℕ) where
  pos : ℕ
  reg : ℕ
  mov : ℕ

/-- [DEF] O PASSO: ler a cláusula na posição da cabeça; se está violada, somar 1 ao registro; avançar a cabeça; e
somar a `mov` o comprimento da cláusula mais 1 (os literais mais o terminador): custo cobrado por definição, não
movimentos contados de uma máquina de fita. -/
def passoFita (φ : CNF n) (x : Fin n → Bool) (c : ConfigFita n) : ConfigFita n :=
  match φ[c.pos]? with
  | none => c
  | some C => ⟨c.pos + 1, c.reg + (if satisfeita C x then 0 else 1), c.mov + C.length + 1⟩

/-- [DEF] As letras da fórmula: os literais mais um terminador por cláusula. -/
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

/-- O take de `j+1` é o take de `j` mais a cláusula `j`. (Auxiliar do laço; a mesma conta de
`OResumoEPsiBit.take_succ_eq`.) -/
theorem take_succ_singleton {n : ℕ} (φ : CNF n) {j : ℕ} (hj : j < φ.length) :
    φ.take (j + 1) = φ.take j ++ [φ[j]] := by
  rw [List.take_add_one, List.getElem?_eq_getElem hj, Option.toList_some]

/-- O passo numa posição válida: o registro ganha o `if` da cláusula; o contador `mov`, o comprimento dela mais um.
(Auxiliar do laço.) -/
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

/-- ★ **O REGISTRO RECEBE O CUSTO DA ATRIBUIÇÃO**: em tantos passos quantas são as cláusulas, a partir da posição
`0`, o registro ganha `custoCNF φ x` e o contador `mov` ganha `letras φ` (a soma do custo cobrado em cada passo). -/
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

/-- ★ **O CUSTO COBRADO É O NÚMERO DE LETRAS**: a partir de `⟨0, 0, 0⟩`, depois de `φ.length` passos, `mov = letras φ`.
É o custo abstrato cobrado por definição em `passoFita`, não contagem de movimentos de uma máquina de fita. -/
theorem o_custo_na_fita_e_o_numero_de_letras (φ : CNF n) (x : Fin n → Bool) :
    ((passoFita φ x)^[φ.length] ⟨0, 0, 0⟩).mov = letras φ := by
  have h : (passoFita φ x)^[φ.length] ⟨0, 0, 0⟩ = ⟨φ.length, 0 + custoCNF φ x, 0 + letras φ⟩ :=
    a_maquina_da_casa_roda_na_fita φ x ⟨0, 0, 0⟩
  rw [h]
  simp

/-- ★ **O REGISTRO VERIFICA O CUSTO DE UMA ATRIBUIÇÃO**: a partir de `⟨0, 0, 0⟩`, depois de `φ.length` passos,
`reg = custoCNF φ x` para a atribuição `x` dada (aceita se `reg = 0`). Não decide se a fórmula tem solução. -/
theorem a_decisao_na_fita_e_a_mesma (φ : CNF n) (x : Fin n → Bool) :
    ((passoFita φ x)^[φ.length] ⟨0, 0, 0⟩).reg = custoCNF φ x := by
  have h : (passoFita φ x)^[φ.length] ⟨0, 0, 0⟩ = ⟨φ.length, 0 + custoCNF φ x, 0 + letras φ⟩ :=
    a_maquina_da_casa_roda_na_fita φ x ⟨0, 0, 0⟩
  rw [h]
  simp

/-- ★ **A COTA DO CUSTO COBRADO**: para cada `φ` e `x` existe `c` com `mov ≤ c · letras φ`; a prova usa `c = 1`
para todos (`o_custo_na_fita_e_o_numero_de_letras`). -/
theorem o_custo_da_ponte_e_polinomial (φ : CNF n) (x : Fin n → Bool) :
    ∃ c : ℕ, ((passoFita φ x)^[φ.length] ⟨0, 0, 0⟩).mov ≤ c * letras φ := by
  refine ⟨1, ?_⟩
  rw [o_custo_na_fita_e_o_numero_de_letras, one_mul]

end TGLExt.APonteDeCookLevin
