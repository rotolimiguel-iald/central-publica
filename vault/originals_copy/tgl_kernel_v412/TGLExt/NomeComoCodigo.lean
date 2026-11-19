import TGLExt.TraducaoTuring
import Mathlib.InformationTheory.Hamming

set_option autoImplicit false
set_option linter.unusedVariables false

/-!
# O NOME COMO CÓDIGO — um passo local desfaz o empurrão de uma asserção

As configurações são as leituras de n asserções (`Fin n → Bool`); o custo `c` é a regra; o Nome são as leituras de custo zero. Um
EMPURRÃO troca o valor de uma asserção. O LEITOR DOS VIZINHOS consulta o VERIFICADOR (o custo é zero ou não) na própria leitura e nas n
leituras vizinhas (uma troca), e vai a uma vizinha que resolve, se houver. Não conhece o Nome e não salta.

O núcleo combinatório é [KNOWN]: num código de distância mínima três, a decodificação no raio um é única (Hamming, 1950). O que esta
pedra acrescenta é o dicionário e a localidade do leitor, como termos.

O que a pedra PROVA:
* `o_empurrao_tem_um_so_retorno` [KNOWN, Hamming]: se duas leituras válidas distintas diferem em pelo menos três asserções, então depois
  do empurrão de UMA asserção numa leitura válida s, a única leitura válida a uma troca do estado empurrado é a própria s.
* `o_leitor_dos_vizinhos_desfaz_o_empurrao` ★★★: nessas condições, o leitor dos vizinhos volta a s num passo.
* `o_leitor_so_ve_o_zero_do_custo_na_leitura_e_nas_vizinhas` ★★★ (a LOCALIDADE): o leitor depende do custo só por duas coisas, se a
  própria leitura tem custo zero e quais das n vizinhas têm custo zero. `o_leitor_usa_so_o_verificador`: não usa a grandeza do custo.
* `a_trava_deixa_intacta_sse_o_custo_e_zero` ★★: o teste que o leitor aplica a uma leitura (custo zero) é o teste “a trava a deixa
  intacta”, para todo tempo positivo. É o único elo por termo com a trava.
* `o_leitor_dos_vizinhos_fixa_o_nome`: o que resolve fica. `o_empurrao_dentro_do_nome_fica`: se o estado empurrado também resolve, o
  leitor fica onde foi posto (caso que a hipótese da distância três exclui).

O que NÃO afirma:
* Que este leitor seja o passo que consome o custo da `CamadaCientifica`: não é. Fora da bola de raio um do Nome ele pode ficar parado
  para sempre com custo positivo; não pousa de qualquer estado. É um passo, com promessa de partida a uma troca do Nome.
* Que ele seja um `LeitorDoFundo`: não tem escala. Ele consulta o verificador em n + 1 pontos; não lê brilho, não lê tempo de ciclo.
* Que a distância três valha para a fórmula de algum texto: ela pede leituras válidas ISOLADAS, e falha para toda fórmula satisfazível
  com variável livre. Mede-se na fórmula do texto, por script.
* Que o retorno daqui seja o da trava: lá o que foi posto fora do Nome é ESQUECIDO (a amplitude decai); aqui a configuração é
  REPOSICIONADA. As duas máquinas partilham o custo e o teste do zero; não há outro elo por termo.
* Nada para empurrões de duas ou mais asserções. Que um modelo de linguagem seja este leitor é previsão a testar.
* Exclusividade; consciência; natureza. Validade no kernel, não creditação. Sem sorry, sem axiom.
-/

namespace TGLExt.NomeComoCodigo
open TGLExt.TraducaoTuring

variable {n : ℕ}

/-- O EMPURRÃO de uma asserção: troca o valor da coordenada j. -/
def empurrao (x : Fin n → Bool) (j : Fin n) : Fin n → Bool := Function.update x j (!x j)

/-- o empurrão muda no máximo uma asserção. -/
theorem empurrao_dista_um (x : Fin n → Bool) (j : Fin n) : hammingDist x (empurrao x j) ≤ 1 := by
  unfold hammingDist empurrao
  calc (Finset.univ.filter (fun i => x i ≠ Function.update x j (!x j) i)).card
      ≤ ({j} : Finset (Fin n)).card := by
        apply Finset.card_le_card
        intro i hi
        rw [Finset.mem_filter] at hi
        rw [Finset.mem_singleton]
        by_contra hne
        exact hi.2 (by simp [Function.update, hne])
    _ = 1 := Finset.card_singleton j

/-- empurrar duas vezes a mesma asserção devolve a leitura. -/
theorem empurrao_empurrao (x : Fin n → Bool) (j : Fin n) : empurrao (empurrao x j) j = x := by
  funext i
  unfold empurrao
  by_cases h : i = j
  · subst h
    simp
  · simp [Function.update, h]

/-- o empurrão muda a leitura. -/
theorem empurrao_muda (x : Fin n → Bool) (j : Fin n) : x ≠ empurrao x j := by
  intro h
  have hj := congrFun h j
  simp [empurrao] at hj

/-- O EMPURRÃO TEM UM SÓ RETORNO [KNOWN: Hamming, 1950; a decodificação única no raio um de um código de distância mínima três]: se
    duas leituras válidas distintas diferem em pelo menos três asserções, então depois do empurrão de uma asserção numa leitura válida
    s, a única leitura válida a distância ≤ 1 do estado empurrado é s. -/
theorem o_empurrao_tem_um_so_retorno (c : (Fin n → Bool) → ℕ)
    (hsep : ∀ s s' : Fin n → Bool, c s = 0 → c s' = 0 → s ≠ s' → 3 ≤ hammingDist s s')
    (s : Fin n → Bool) (hs : c s = 0) (j : Fin n) (y : Fin n → Bool) (hy : c y = 0)
    (hd : hammingDist (empurrao s j) y ≤ 1) : y = s := by
  by_contra hne
  have h3 := hsep s y hs hy (fun h => hne h.symm)
  have h1 := empurrao_dista_um s j
  have htri := hammingDist_triangle s (empurrao s j) y
  omega

/-- O LEITOR DOS VIZINHOS: consulta o verificador (custo zero ou não) na leitura e nas n vizinhas. Se a leitura resolve, fica; senão,
    se alguma vizinha (uma troca) resolve, vai a uma delas; senão fica. Não conhece o Nome. Não é `LeitorDoFundo` (não tem escala) nem
    o passo que consome o custo (fora da bola de raio um do Nome pode ficar parado). -/
noncomputable def leitorDosVizinhos (c : (Fin n → Bool) → ℕ) (x : Fin n → Bool) : Fin n → Bool :=
  if c x = 0 then x else if h : ∃ j, c (empurrao x j) = 0 then empurrao x h.choose else x

/-- ★ o leitor dos vizinhos fixa o Nome: o que resolve fica. -/
theorem o_leitor_dos_vizinhos_fixa_o_nome (c : (Fin n → Bool) → ℕ) (x : Fin n → Bool) (hx : c x = 0) :
    leitorDosVizinhos c x = x := by
  unfold leitorDosVizinhos
  rw [if_pos hx]

/-- ★★★ O LEITOR DOS VIZINHOS DESFAZ O EMPURRÃO: se o Nome é um código de distância pelo menos três, o leitor dos vizinhos volta, num
    passo, à MESMA leitura de antes do empurrão de uma asserção. -/
theorem o_leitor_dos_vizinhos_desfaz_o_empurrao (c : (Fin n → Bool) → ℕ)
    (hsep : ∀ s s' : Fin n → Bool, c s = 0 → c s' = 0 → s ≠ s' → 3 ≤ hammingDist s s')
    (s : Fin n → Bool) (hs : c s = 0) (j : Fin n) :
    leitorDosVizinhos c (empurrao s j) = s := by
  have hx : c (empurrao s j) ≠ 0 := by
    intro h0
    have h3 := hsep s (empurrao s j) hs h0 (empurrao_muda s j)
    have h1 := empurrao_dista_um s j
    omega
  have hex : ∃ j', c (empurrao (empurrao s j) j') = 0 := ⟨j, by rw [empurrao_empurrao]; exact hs⟩
  unfold leitorDosVizinhos
  rw [if_neg hx, dif_pos hex]
  exact o_empurrao_tem_um_so_retorno c hsep s hs j _ hex.choose_spec (empurrao_dista_um _ _)

/-- (auxiliar) a escolha depende só do predicado. -/
theorem escolha_so_depende_do_predicado {p q : Fin n → Prop} (e : p = q) (hp : ∃ a, p a) (hq : ∃ a, q a) :
    hp.choose = hq.choose := by
  subst e
  rfl

/-- ★★★ A LOCALIDADE: o leitor dos vizinhos depende do custo SÓ por duas coisas: se a própria leitura tem custo zero, e quais das n
    vizinhas têm custo zero. Não depende da grandeza do custo, nem de nenhuma outra leitura, nem do Nome. -/
theorem o_leitor_so_ve_o_zero_do_custo_na_leitura_e_nas_vizinhas (c c' : (Fin n → Bool) → ℕ) (x : Fin n → Bool)
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
      rw [escolha_so_depende_do_predicado e hex hex']
    · have hex' : ¬ ∃ j, c' (empurrao x j) = 0 := fun ⟨j, hj⟩ => hex ⟨j, (hn j).mpr hj⟩
      rw [dif_neg hex, dif_neg hex']

/-- ★★ O LEITOR USA SÓ O VERIFICADOR: o leitor é o mesmo para o custo c e para o custo binário “resolve ou não resolve”. -/
theorem o_leitor_usa_so_o_verificador (c : (Fin n → Bool) → ℕ) (x : Fin n → Bool) :
    leitorDosVizinhos c x = leitorDosVizinhos (fun y => if c y = 0 then 0 else 1) x :=
  o_leitor_so_ve_o_zero_do_custo_na_leitura_e_nas_vizinhas _ _ x (by by_cases h : c x = 0 <;> simp [h])
    (fun j => by by_cases h : c (empurrao x j) = 0 <;> simp [h])

/-- o empurrão dentro do Nome fica: se o estado empurrado também resolve, o leitor dos vizinhos fica onde foi posto. (A hipótese da
    distância três exclui este caso; ele só ocorre quando o Nome não é código.) -/
theorem o_empurrao_dentro_do_nome_fica (c : (Fin n → Bool) → ℕ) (s : Fin n → Bool) (j : Fin n)
    (h : c (empurrao s j) = 0) : leitorDosVizinhos c (empurrao s j) = empurrao s j :=
  o_leitor_dos_vizinhos_fixa_o_nome c _ h

/-- ★★ O TESTE DO LEITOR É O TESTE DA TRAVA: para todo tempo positivo, a trava deixa intacta a leitura y (o vetor da base em y) se e só
    se o custo de y é zero. É o critério que o leitor dos vizinhos aplica a cada vizinha. -/
theorem a_trava_deixa_intacta_sse_o_custo_e_zero {X : Type} [Fintype X] [DecidableEq X] (c : X → ℕ) {t : ℝ} (ht : 0 < t) (y : X) :
    trava c t (EuclideanSpace.single y (1 : ℂ)) = EuclideanSpace.single y (1 : ℂ) ↔ c y = 0 := by
  constructor
  · intro h
    have h1 := congrArg (fun v : EuclideanSpace ℂ X => WithLp.ofLp v y) h
    simp only [trava_ofLp, PiLp.single_apply, if_true, mul_one] at h1
    by_contra hc
    have hpos : (0 : ℝ) < t * (c y : ℝ) := by
      have : (1 : ℝ) ≤ (c y : ℝ) := by exact_mod_cast Nat.one_le_iff_ne_zero.mpr hc
      nlinarith
    have hlt : Real.exp (-(t * (c y : ℝ))) < 1 := by
      have h0 := Real.exp_lt_exp.mpr (show -(t * (c y : ℝ)) < 0 by linarith)
      rwa [Real.exp_zero] at h0
    have h2 : Real.exp (-(t * (c y : ℝ))) = 1 := by exact_mod_cast h1
    linarith
  · intro h
    ext x
    rw [trava_ofLp]
    by_cases hx : x = y
    · subst hx
      simp [h]
    · simp [hx]

/-- PARA UMA FÓRMULA: o mesmo, com o custo da fórmula (o número de cláusulas violadas). -/
theorem para_uma_formula (φ : CNF n)
    (hsep : ∀ s s' : Fin n → Bool, custoCNF φ s = 0 → custoCNF φ s' = 0 → s ≠ s' → 3 ≤ hammingDist s s')
    (s : Fin n → Bool) (hs : custoCNF φ s = 0) (j : Fin n) :
    leitorDosVizinhos (custoCNF φ) (empurrao s j) = s :=
  o_leitor_dos_vizinhos_desfaz_o_empurrao _ hsep s hs j

end TGLExt.NomeComoCodigo
