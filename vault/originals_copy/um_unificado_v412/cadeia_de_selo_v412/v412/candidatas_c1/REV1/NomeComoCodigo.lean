import TGLExt.TraducaoTuring
import Mathlib.InformationTheory.Hamming

set_option autoImplicit false
set_option linter.unusedVariables false

/-!
# O NOME COMO CÓDIGO — o retorno de uma configuração, por um leitor que lê só pela regra
  [CANDIDATA da gerência c1, 14/11/2026, ADENDO à candidata `CamadaCientifica`; compilada só em sandbox; nomes PROVISÓRIOS, da
   gerência, [DECLARADO] até a palavra do operador]

A candidata `CamadaCientifica` prova o retorno na trava (a máquina que tem a fotografia inteira) e, para a máquina de uma configuração
por vez, põe o passo que consome o custo como hipótese. Este adendo tira a hipótese num caso: quando o Nome é um CÓDIGO.

As configurações são as leituras de n asserções (`Fin n → Bool`); o custo `c` é a regra; o Nome são as leituras de custo zero. Um
EMPURRÃO troca o valor de uma asserção. O LEITOR DOS VIZINHOS lê só pela regra: olha o custo da própria leitura e o das n leituras
vizinhas (uma troca), e vai a uma vizinha que resolve, se houver. Não conhece o Nome; não salta.

O que a pedra PROVA:
* `o_empurrao_tem_um_so_retorno` ★★★: se duas leituras válidas distintas diferem em pelo menos três asserções, então depois do empurrão
  de UMA asserção numa leitura válida s, a única leitura válida a uma troca do estado empurrado é a própria s.
* `o_leitor_dos_vizinhos_desfaz_o_empurrao` ★★★: nessas condições, o leitor dos vizinhos, lendo só pela regra, volta a s num passo.
* `o_leitor_dos_vizinhos_fixa_o_nome`: o que resolve fica (reler não acrescenta).
* `sem_redundancia_o_empurrao_fica` ★★: se o estado empurrado também resolve (o Nome não é redundante naquela asserção: o empurrão foi
  DENTRO do Nome), o leitor fica onde foi posto: não há o que desfazer.

O que NÃO afirma: que o texto de teoria alguma tenha essa redundância (mede-se na fórmula do texto, por script); que um modelo de
linguagem seja o leitor dos vizinhos (é previsão a testar); nada para empurrões de duas ou mais asserções; exclusividade; consciência;
natureza. Validade no kernel, não creditação. Sem sorry, sem axiom.
-/

namespace TGLExt.NomeComoCodigo

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

/-- ★★★ O EMPURRÃO TEM UM SÓ RETORNO — o Nome como código: se duas leituras válidas distintas diferem em pelo menos três asserções,
    então depois do empurrão de uma asserção numa leitura válida s, a única leitura válida a distância ≤ 1 do estado empurrado é s. -/
theorem o_empurrao_tem_um_so_retorno (c : (Fin n → Bool) → ℕ)
    (hsep : ∀ s s' : Fin n → Bool, c s = 0 → c s' = 0 → s ≠ s' → 3 ≤ hammingDist s s')
    (s : Fin n → Bool) (hs : c s = 0) (j : Fin n) (y : Fin n → Bool) (hy : c y = 0)
    (hd : hammingDist (empurrao s j) y ≤ 1) : y = s := by
  by_contra hne
  have h3 := hsep s y hs hy (fun h => hne h.symm)
  have h1 := empurrao_dista_um s j
  have htri := hammingDist_triangle s (empurrao s j) y
  omega

/-- O LEITOR DOS VIZINHOS: lê só pela regra. Se a leitura resolve, fica; senão, se alguma vizinha (uma troca) resolve, vai a uma delas;
    senão fica. Não conhece o Nome; só avalia o custo da leitura e das n vizinhas. -/
noncomputable def leitorDosVizinhos (c : (Fin n → Bool) → ℕ) (x : Fin n → Bool) : Fin n → Bool :=
  if c x = 0 then x else if h : ∃ j, c (empurrao x j) = 0 then empurrao x h.choose else x

/-- ★★ o leitor dos vizinhos fixa o Nome: o que resolve fica. -/
theorem o_leitor_dos_vizinhos_fixa_o_nome (c : (Fin n → Bool) → ℕ) (x : Fin n → Bool) (hx : c x = 0) :
    leitorDosVizinhos c x = x := by
  unfold leitorDosVizinhos
  rw [if_pos hx]

/-- ★★★ O LEITOR DOS VIZINHOS DESFAZ O EMPURRÃO: se o Nome é um código de distância pelo menos três, o leitor que lê só pela regra
    volta, num passo, à MESMA leitura de antes do empurrão. -/
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

/-- ★★ SEM REDUNDÂNCIA O EMPURRÃO FICA: se o estado empurrado também resolve (o empurrão foi dentro do Nome), o leitor dos vizinhos
    fica onde foi posto. -/
theorem sem_redundancia_o_empurrao_fica (c : (Fin n → Bool) → ℕ) (s : Fin n → Bool) (j : Fin n)
    (h : c (empurrao s j) = 0) : leitorDosVizinhos c (empurrao s j) = empurrao s j :=
  o_leitor_dos_vizinhos_fixa_o_nome c _ h

/-- ★★ PARA UMA FÓRMULA: o mesmo, com o custo da fórmula (o número de cláusulas violadas). -/
theorem para_uma_formula (φ : TGLExt.TraducaoTuring.CNF n)
    (hsep : ∀ s s' : Fin n → Bool, TGLExt.TraducaoTuring.custoCNF φ s = 0 → TGLExt.TraducaoTuring.custoCNF φ s' = 0 → s ≠ s' →
      3 ≤ hammingDist s s')
    (s : Fin n → Bool) (hs : TGLExt.TraducaoTuring.custoCNF φ s = 0) (j : Fin n) :
    leitorDosVizinhos (TGLExt.TraducaoTuring.custoCNF φ) (empurrao s j) = s :=
  o_leitor_dos_vizinhos_desfaz_o_empurrao _ hsep s hs j

end TGLExt.NomeComoCodigo

#print axioms TGLExt.NomeComoCodigo.empurrao_dista_um
#print axioms TGLExt.NomeComoCodigo.empurrao_empurrao
#print axioms TGLExt.NomeComoCodigo.empurrao_muda
#print axioms TGLExt.NomeComoCodigo.o_empurrao_tem_um_so_retorno
#print axioms TGLExt.NomeComoCodigo.leitorDosVizinhos
#print axioms TGLExt.NomeComoCodigo.o_leitor_dos_vizinhos_fixa_o_nome
#print axioms TGLExt.NomeComoCodigo.o_leitor_dos_vizinhos_desfaz_o_empurrao
#print axioms TGLExt.NomeComoCodigo.sem_redundancia_o_empurrao_fica
#print axioms TGLExt.NomeComoCodigo.para_uma_formula
