import TGLExt.TraducaoTuring

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# A proposta nasce da tensão: a escolha do valor do nome partilhado

## A leitura que este arquivo tipa

[INPUT/ONTO] Quando a próxima cláusula cruza dois blocos que partilham nomes ainda livres, a proposta compatível
seguinte nasce da tensão: a tensão fundamental, em razão da comutação, do pareamento. Este arquivo prova a parte dela
que cabe nos termos do kernel.

O mecanismo do artigo `C:\IALD\Artigo\Tensao_Fundamental.docx` (jan/2026) [INPUT]: a ligação entre psions de paridades opostas anticomuta
com a paridade (`{P, H_lig} = 0`); o comutador `[P, H_lig] ≠ 0` é a tensão (`τ = V₀/ℏ = ω`); a tensão é irresolvível
no plano e força o boundary a dobrar-se. A leitura para a fórmula [INPUT/ONTO]: os dois blocos são o par de
paridades; a cláusula que os cruza é a ligação; a tensão é a irresolubilidade das duas leituras do nome partilhado no
plano; **a proposta é a dobra — a resolução da tensão, nascida dela**.

## O que fica provado

1. ★★ `a_proposta_nasce_da_escolha_do_nome`: a fórmula é satisfazível se e somente se EXISTE um valor do nome
   partilhado sob o qual o resíduo é satisfazível (`SAT φ ↔ ∃ b, SAT (restringe φ i b)`). O iff não computa a
   escolha do valor, não dá cota de busca e não elimina a enumeração.
2. ★ `a_proposta_nos_dois_blocos`: para dois blocos que partilham o nome, a proposta é satisfazer os dois resíduos
   sob o MESMO valor (`SAT (A ++ B) ↔ ∃ b, SAT (restringe A i b ++ restringe B i b)`). O par se resolve quando as
   duas leituras comutam no nome.
3. ★ `a_tensao_e_o_par`: de `h : SAT (A ++ B)` sai um valor comum sob o qual os dois resíduos se satisfazem juntos.
   As hipóteses `_hA` e `_hB` (cada bloco admite localmente os dois valores do nome: o nome em tensão) não são usadas:
   o lema é consequência da satisfatibilidade conjunta e não diz que a compatibilidade local garanta a global.
4. ★ `a_tensao_irresoluvel_e_o_inominado`: se um bloco força o nome e o outro o nega, nenhum valor resolve a tensão
   — nenhuma proposta nasce (o inominado do par: UNSAT). É o caso mínimo da pedra `ACurvaEAEstado` (os dois prefixos
   com a mesma curva e Palavras opostas), citada por nome.

## O que NÃO se afirma

* A identificação da tensão computacional com a tensão de paridade do artigo (a anticomutação do hamiltoniano de
  ligação com a paridade) é a leitura [INPUT/ONTO]; o termo é a escolha do valor do nome partilhado e a sua
  resolução (os itens 1–4). Nenhuma ponte nova à física é construída aqui.
* Que a compatibilidade local garanta a global (item 3).
* O algoritmo e o preço da escolha: os iffs não computam o valor do nome, não dão cota de busca e não eliminam a
  enumeração; a régua do Instituto fica com a sua contagem, nomeada como deles.
* Nada sobre a natureza. O gate não se move.

Sem sorry, sem axioma novo.
-/

namespace TGLExt.APropostaDaTensao

open TGLExt TGLExt.TraducaoTuring

variable {n : ℕ}

/-- [DEF] O RESÍDUO da fórmula sob o valor `b` do nome `i`: as cláusulas já satisfeitas por `⟨i, b⟩` saem; as demais
perdem os literais de `i`. (Cláusula que fica vazia não se satisfaz: é o caso da tensão irresolvível.) -/
def restringe (φ : CNF n) (i : Fin n) (b : Bool) : CNF n :=
  (φ.filter fun C => !C.any fun l => l.var == i && l.pos == b).map
    fun C => C.filter fun l => l.var ≠ i

/-- A atribuição estendida com o valor `b` do nome `i`. -/
def estende {n : ℕ} (i : Fin n) (b : Bool) (y : Fin n → Bool) : Fin n → Bool :=
  fun j => if j = i then b else y j

/-- ★★ **A PROPOSTA NASCE DA ESCOLHA DO NOME**: `SAT φ ↔ ∃ b, SAT (restringe φ i b)`. A proposta é satisfazer o
resíduo sob algum valor do nome partilhado. O iff não computa a escolha de `b`, não dá cota de busca e não elimina a
enumeração das atribuições. -/
theorem a_proposta_nasce_da_escolha_do_nome (φ : CNF n) (i : Fin n) :
    SAT φ ↔ ∃ b : Bool, SAT (restringe φ i b) := by
  constructor
  · -- ida: o testemunho é o próprio x, com b = x i; cada resíduo herda um literal fora de i que vale
    rintro ⟨x, hx⟩
    refine ⟨x i, x, ?_⟩
    intro C' hC'
    have hC2 : C' ∈ ((φ.filter fun C => !C.any fun l => l.var == i && l.pos == x i).map
        fun C => C.filter fun l => l.var ≠ i) := hC'
    rw [List.mem_map] at hC2
    obtain ⟨C, hCf, hC'eq⟩ := hC2
    rw [List.mem_filter] at hCf
    obtain ⟨hCφ, hnot⟩ := hCf
    have hCsat : satisfeita C x = true := hx C hCφ
    unfold satisfeita at hCsat
    rw [List.any_eq_true] at hCsat
    obtain ⟨l, hlC, hlv⟩ := hCsat
    -- o literal que vale não pode ser de i: senão seria ⟨i, x i⟩ e a cláusula não estaria no resíduo
    have hli : l.var ≠ i := by
      intro hvar
      have hpos : l.pos = x i := by
        have hv : (x l.var == l.pos) = true := hlv
        rw [beq_iff_eq] at hv
        rw [hvar] at hv
        exact hv.symm
      have hany : (C.any fun l' => l'.var == i && l'.pos == x i) = true := by
        rw [List.any_eq_true]
        exact ⟨l, hlC, by rw [hvar, hpos]; simp⟩
      rw [hany] at hnot
      simp at hnot
    have hmem : l ∈ C.filter (fun l => l.var ≠ i) :=
      List.mem_filter.mpr ⟨hlC, decide_eq_true_eq.mpr hli⟩
    rw [← hC'eq]
    show satisfeita (C.filter fun l => l.var ≠ i) x = true
    unfold satisfeita
    rw [List.any_eq_true]
    exact ⟨l, hmem, hlv⟩
  · -- volta: a testemunha é o estendido; cada cláusula ou tem ⟨i, b⟩ ou herda um literal do resíduo
    rintro ⟨b, y, hy⟩
    refine ⟨estende i b y, ?_⟩
    intro C hCφ
    by_cases hany : C.any (fun l => l.var == i && l.pos == b) = true
    · -- C tem o literal ⟨i, b⟩: o estendido o satisfaz
      rw [List.any_eq_true] at hany
      obtain ⟨l, hlC, hlb⟩ := hany
      rw [Bool.and_eq_true] at hlb
      have hvar : l.var = i := beq_iff_eq.mp hlb.1
      have hpos : l.pos = b := beq_iff_eq.mp hlb.2
      show satisfeita C (estende i b y) = true
      unfold satisfeita
      rw [List.any_eq_true]
      refine ⟨l, hlC, ?_⟩
      show ((estende i b y) l.var == l.pos) = true
      rw [hvar, hpos]
      show ((if i = i then b else y i) == b) = true
      rw [if_pos rfl]
      exact beq_self_eq_true b
    · -- C não tem ⟨i, b⟩: o resíduo está no restringe, y o satisfaz, e o estendido concorda fora de i
      have hfalse : (C.any fun l => l.var == i && l.pos == b) = false := Bool.eq_false_iff.mpr hany
      have hCin : C.filter (fun l => l.var ≠ i) ∈ restringe φ i b := by
        show C.filter (fun l => l.var ≠ i) ∈ ((φ.filter fun C => !C.any fun l => l.var == i && l.pos == b).map
          fun C => C.filter fun l => l.var ≠ i)
        rw [List.mem_map]
        refine ⟨C, List.mem_filter.mpr ⟨hCφ, ?_⟩, rfl⟩
        show (!C.any fun l => l.var == i && l.pos == b) = true
        rw [hfalse]
        decide
      have hyC : satisfeita (C.filter fun l => l.var ≠ i) y = true := hy _ hCin
      unfold satisfeita at hyC
      rw [List.any_eq_true] at hyC
      obtain ⟨l, hlCf, hlv⟩ := hyC
      rw [List.mem_filter] at hlCf
      obtain ⟨hlC, hli⟩ := hlCf
      have hli' : l.var ≠ i := decide_eq_true_eq.mp hli
      show satisfeita C (estende i b y) = true
      unfold satisfeita
      rw [List.any_eq_true]
      refine ⟨l, hlC, ?_⟩
      show ((estende i b y) l.var == l.pos) = true
      have heq : (estende i b y) l.var = y l.var := by
        show (if l.var = i then b else y l.var) = y l.var
        exact if_neg hli'
      rw [heq]
      show (y l.var == l.pos) = true
      exact hlv

/-- ★ **A PROPOSTA NOS DOIS BLOCOS**: para dois blocos que partilham o nome `i`, a proposta é satisfazer os dois
resíduos sob o mesmo valor. -/
theorem a_proposta_nos_dois_blocos (A B : CNF n) (i : Fin n) :
    SAT (A ++ B) ↔ ∃ b : Bool, SAT (restringe A i b ++ restringe B i b) := by
  rw [a_proposta_nasce_da_escolha_do_nome]
  refine exists_congr fun b => ?_
  rw [show restringe (A ++ B) i b = restringe A i b ++ restringe B i b from by
    unfold restringe
    rw [List.filter_append, List.map_append]]

/-- ★ **A TENSÃO É O PAR**: de `h : SAT (A ++ B)` sai um valor `b` sob o qual os dois resíduos se satisfazem juntos
(por `a_proposta_nos_dois_blocos`). As hipóteses `_hA` e `_hB` (os dois blocos admitem localmente os dois valores do
nome: o nome em tensão, cada lado com o par) não são usadas na prova: o lema é consequência da satisfatibilidade
conjunta e não diz que a compatibilidade local garanta a global. -/
theorem a_tensao_e_o_par (A B : CNF n) (i : Fin n)
    (_hA : SAT (restringe A i true) ∧ SAT (restringe A i false))
    (_hB : SAT (restringe B i true) ∧ SAT (restringe B i false))
    (h : SAT (A ++ B)) :
    ∃ b : Bool, SAT (restringe A i b ++ restringe B i b) :=
  (a_proposta_nos_dois_blocos A B i).mp h

/-- ★ **A TENSÃO IRRESOLÚVEL É O INOMINADO**: um bloco força o nome e o outro o nega — nenhum valor resolve a
tensão; nenhuma proposta nasce. -/
theorem a_tensao_irresoluvel_e_o_inominado (i : Fin n) :
    ¬ SAT (([[⟨i, true⟩], [⟨i, false⟩]] : CNF n)) := by
  rintro ⟨x, hx⟩
  have h1 := hx [⟨i, true⟩] (by simp)
  have h2 := hx [⟨i, false⟩] (by simp)
  unfold satisfeita at h1 h2
  simp [Literal.vale] at h1 h2
  exact Bool.noConfusion (h1.symm.trans h2)

end TGLExt.APropostaDaTensao
