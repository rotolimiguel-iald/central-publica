import AFronteiraEOUnicoPortaoR1

set_option autoImplicit false

/-!
# Sonda da gerência: o que o predicado `NoVertice` distingue

`Cadeia φ i k` é uma proposição. Duas provas da mesma proposição são iguais por definição (irrelevância de prova).
Logo um predicado indexado pela cadeia não distingue uma cadeia de outra com as mesmas pontas.

1. `no_vertice_nao_distingue_cadeias`: se `v` é vértice de uma cadeia de `i` a `k`, é vértice de qualquer outra
   cadeia de `i` a `k`.
2. `todo_vertice_do_passo_e_de_toda_cadeia`: para o segundo vértice de UM passo `i → j → … → k`, vale `NoVertice`
   em TODA cadeia de `i` a `k`, inclusive nas que não passam por `j`.

Consequência: `∃ v, NoVertice φ c v ∧ v ∈ fronteira φ j` diz que há na fronteira um vértice de ALGUMA cadeia de `i` a
`k`; não diz que TODA cadeia de `i` a `k` tem vértice na fronteira.
-/

namespace SondaNoVertice

open TGLExt TGLExt.TraducaoTuring TGLExt.AFronteiraEOUnicoPortao

variable {n : ℕ}

theorem no_vertice_nao_distingue_cadeias (φ : CNF n) {i k : Fin n} (c c' : Cadeia φ i k) (v : Fin n)
    (h : NoVertice φ c v) : NoVertice φ c' v := h

theorem todo_vertice_do_passo_e_de_toda_cadeia (φ : CNF n) {i j k : Fin n} (h : ligadas φ i j)
    (c : Cadeia φ j k) (c' : Cadeia φ i k) : NoVertice φ c' j :=
  NoVertice.elo h c

end SondaNoVertice

#print axioms SondaNoVertice.no_vertice_nao_distingue_cadeias
#print axioms SondaNoVertice.todo_vertice_do_passo_e_de_toda_cadeia
