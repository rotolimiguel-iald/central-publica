import TGLExt.RelacaoFronteira

/-! Contador do leitor de fronteira. Uma visita a literal, coordenada, linha, célula
do saco ou célula-alvo vale uma unidade. Preparar os domínios, obter bits por índice,
copiar endereços e mover a cabeça de uma máquina de fita têm custos separados. -/
namespace IALD.TrabalhoPorCorte

open TGLExt.TraducaoTuring IALD.RelacaoFronteira

/-- Com stop=true, procura um sucesso. Com stop=false, procura uma falha.
A resposta e o contador compartilham a mesma visita, com curto-circuito real. -/
def checkList {α : Type} (stop : Bool) (visit : α → Bool × Nat) : List α → Bool × Nat
  | [] => (!stop, 0)
  | x :: xs =>
    let a := visit x
    if a.1 == stop then (stop, 1+a.2)
    else let b := checkList stop visit xs; (b.1, 1+a.2+b.2)

private theorem check_any {α : Type} (v : α → Bool × Nat) (xs : List α) :
    (checkList true v xs).1 = xs.any (fun x => (v x).1) := by
  induction xs with
  | nil => rfl
  | cons x xs ih => cases h : (v x).1 <;> simp [checkList, h, ih]

private theorem check_all {α : Type} (v : α → Bool × Nat) (xs : List α) :
    (checkList false v xs).1 = xs.all (fun x => (v x).1) := by
  induction xs with
  | nil => rfl
  | cons x xs ih => cases h : (v x).1 <;> simp [checkList, h, ih]

private theorem check_le {α : Type} (stop : Bool) (v : α → Bool × Nat) (k : Nat)
    (h : ∀ x, (v x).2 ≤ k) (xs : List α) :
    (checkList stop v xs).2 ≤ xs.length * (1+k) := by
  induction xs with
  | nil => simp [checkList]
  | cons x xs ih =>
    have hx := h x
    simp only [checkList, List.length_cons, Nat.add_mul, Nat.one_mul]
    split <;> simp only <;> omega

def measuredAgree {n} (s : Finset (Fin n)) (x y : Assignment n) :=
  checkList false (fun i => (x i == y i, 0)) (keys s)

def measuredLookup {n} (s : Finset (Fin n)) (rows : List (Assignment n)) (z : Assignment n) :=
  checkList true (fun y => measuredAgree s y z) rows

def measuredClause {n} (c : Clausula n) (z : Assignment n) :=
  checkList true (fun l => (l.vale z, 0)) c

def checkContext {n} (s t : Finset (Fin n)) (c : Clausula n)
    (rows : List (Assignment n)) (u z : Assignment n) : Bool × Nat :=
  let a := measuredLookup s rows z
  let b := measuredClause c z
  let d := measuredAgree t z u
  (a.1 && b.1 && d.1, a.2+b.2+d.2)

def measuredCell {n} (s t : Finset (Fin n)) (c : Clausula n)
    (rows : List (Assignment n)) (u : Assignment n) :=
  checkList true (checkContext s t c rows u) (cells (bag s t c))

def selectRows {α : Type} (v : α → Bool × Nat) : List α → List α × Nat
  | [] => ([],0)
  | x :: xs =>
    let a := v x
    let b := selectRows v xs
    (if a.1 then x :: b.1 else b.1, 1+a.2+b.2)

private theorem select_spec {α : Type} (v : α → Bool × Nat) (xs : List α) :
    (selectRows v xs).1 = xs.filter (fun x => (v x).1) := by
  induction xs with
  | nil => rfl
  | cons x xs ih => cases h : (v x).1 <;> simp [selectRows, h, ih]

private theorem select_le {α : Type} (v : α → Bool × Nat) (k : Nat)
    (h : ∀ x, (v x).2 ≤ k) (xs : List α) :
    (selectRows v xs).2 ≤ xs.length * (1+k) := by
  induction xs with
  | nil => simp [selectRows]
  | cons x xs ih =>
    have hx := h x
    simp only [selectRows, List.length_cons, Nat.add_mul, Nat.one_mul]
    omega

def measuredAdvance {n} (s t : Finset (Fin n)) (c : Clausula n) (rows : List (Assignment n)) :=
  selectRows (measuredCell s t c rows) (cells t)

theorem same_rows {n} (s t : Finset (Fin n)) (c : Clausula n) (rows : List (Assignment n)) :
    (measuredAdvance s t c rows).1 = advance s t c rows := by
  simp [measuredAdvance, select_spec, advance, measuredCell, checkContext, measuredLookup,
    measuredClause, measuredAgree, check_any, check_all, lookup, agrees, satisfeita]

private theorem keys_size {n} (s : Finset (Fin n)) : (keys s).length = s.card := by
  have nd : (keys s).Nodup := (List.nodup_finRange n).filter _
  have hs : (keys s).toFinset = s := by ext; simp
  exact (List.toFinset_card_of_nodup nd).symm.trans (congrArg Finset.card hs)

private theorem cost_agree {n} (s : Finset (Fin n)) (x y : Assignment n) :
    (measuredAgree s x y).2 ≤ s.card := by
  simpa [measuredAgree, keys_size] using check_le false
    (fun i => (x i == y i, 0)) 0 (fun _ => Nat.le_refl _) (keys s)

private theorem cost_lookup {n} (s : Finset (Fin n)) (rows : List (Assignment n)) (x : Assignment n) :
    (measuredLookup s rows x).2 ≤ rows.length * (1+s.card) :=
  check_le true _ _ (fun y => cost_agree s y x) _

private theorem cost_clause {n} (c : Clausula n) (x : Assignment n) :
    (measuredClause c x).2 ≤ c.length := by
  simpa [measuredClause] using check_le true
    (fun l : Literal n => (l.vale x, 0)) 0 (fun _ => Nat.le_refl _) c

theorem paid_visits {n} (s t : Finset (Fin n)) (c : Clausula n) (rows : List (Assignment n)) :
    (measuredAdvance s t c rows).2 ≤
    2 ^ t.card * (1 + 2 ^ (bag s t c).card *
      (1 + (rows.length * (1+s.card) + c.length + t.card))) := by
  let k := rows.length * (1+s.card) + c.length + t.card
  have inner (u z : Assignment n) : (checkContext s t c rows u z).2 ≤ k :=
    Nat.add_le_add (Nat.add_le_add (cost_lookup s rows z) (cost_clause c z)) (cost_agree t z u)
  have mid (u : Assignment n) : (measuredCell s t c rows u).2 ≤ 2 ^ (bag s t c).card * (1+k) := by
    simpa only [measuredCell,cells_length] using check_le true _ k (inner u) (cells (bag s t c))
  simpa only [measuredAdvance,cells_length,k] using select_le _ _ mid (cells t)

def polynomial (L P : Nat) : Nat :=
  P * (1 + P * (1 + (P*(1+L) + L + L)))

theorem bounded_width_cost {n} (s t : Finset (Fin n)) (c : Clausula n)
    (rows : List (Assignment n)) (L P : Nat)
    (hrows : rows.length ≤ P) (ht : 2^t.card ≤ P) (hb : 2^(bag s t c).card ≤ P)
    (hs : s.card ≤ L) (hc : c.length ≤ L) (hn : t.card ≤ L) :
    (measuredAdvance s t c rows).2 ≤ polynomial L P :=
  (paid_visits s t c rows).trans
    (Nat.mul_le_mul ht (Nat.add_le_add_left (Nat.mul_le_mul hb
      (Nat.add_le_add_left (Nat.add_le_add (Nat.add_le_add
        (Nat.mul_le_mul hrows (Nat.add_le_add_left hs 1)) hc) hn) 1)) 1))

/-- Contador encadeado, sem consultar a especificação semântica da Palavra. -/
def measuredScan {n} (p : CNF n) (rows : List (Assignment n)) :
    CNF n → List (Assignment n) × Nat
  | [] => (rows,0)
  | c :: rest =>
    let a := measuredAdvance (boundary p (c :: rest)) (boundary (p ++ [c]) rest) c rows
    let b := measuredScan (p ++ [c]) a.1 rest
    (b.1,a.2+b.2)

theorem measuredScan_spec {n} (p r : CNF n) (rows : List (Assignment n)) :
    (measuredScan p rows r).1 = scan p rows r := by
  induction r generalizing p rows with
  | nil => rfl
  | cons c r ih => simp [measuredScan, scan, ih, same_rows]

theorem measured_word {n} (f : CNF n) (s : ℝ) (hs : (n:ℝ)*Real.log 2 < s) :
    lookup ∅ (measuredScan [] [zero] f).1 zero = true ↔
    TGLExt.OPsibitEACompressao.palavra (custoCNF f) s := by
  rw [measuredScan_spec]
  exact read_word f s hs

/-- Hipóteses inteiramente sintáticas em cada corte. Nenhuma menciona o
veredito, a execução do leitor ou o número de visitas efetuadas. -/
def geometry {n} (p : CNF n) (L P : Nat) : CNF n → Prop
  | [] => True
  | c :: rest =>
    let s := boundary p (c :: rest)
    let t := boundary (p ++ [c]) rest
    2^t.card ≤ P ∧ 2^(bag s t c).card ≤ P ∧ s.card ≤ L ∧ c.length ≤ L ∧
      t.card ≤ L ∧ geometry (p ++ [c]) L P rest

theorem scan_cost {n} (p r : CNF n) (rows : List (Assignment n)) (L P : Nat)
    (hrows : rows.length ≤ P) (hgeom : geometry p L P r) :
    (measuredScan p rows r).1.length ≤ P ∧
    (measuredScan p rows r).2 ≤ r.length * polynomial L P := by
  induction r generalizing p rows with
  | nil => exact ⟨hrows, Nat.zero_le _⟩
  | cons c r ih =>
    let s := boundary p (c :: r)
    let t := boundary (p ++ [c]) r
    obtain ⟨ht,hb,hs,hc,hn,hr⟩ := hgeom
    have hnext : (measuredAdvance s t c rows).1.length ≤ P := by
      rw [same_rows]
      exact (advance_length s t c rows).trans ht
    have hstep := bounded_width_cost s t c rows L P hrows ht hb hs hc hn
    have tail := ih (p ++ [c]) _ hnext hr
    refine ⟨tail.1,?_⟩
    change (measuredAdvance s t c rows).2 +
      (measuredScan (p ++ [c]) (measuredAdvance s t c rows).1 r).2 ≤ _
    simpa only [List.length_cons, Nat.add_mul, Nat.one_mul, Nat.add_comm (polynomial L P)] using
      Nat.add_le_add hstep tail.2

def measuredRead {n} (f : CNF n) : Bool × Nat :=
  let a := measuredScan [] [zero] f
  let b := measuredLookup ∅ a.1 zero
  (b.1, a.2+b.2)

theorem measuredRead_spec {n} (f : CNF n) (s : ℝ) (hs : (n:ℝ)*Real.log 2 < s) :
    (measuredRead f).1 = true ↔ TGLExt.OPsibitEACompressao.palavra (custoCNF f) s := by
  simpa [measuredRead, measuredLookup, measuredAgree, check_any, check_all,
    lookup, agrees] using measured_word f s hs

theorem total_visits {n} (f : CNF n) (L P : Nat) (hp : 1 ≤ P) (hg : geometry [] L P f) :
    (measuredRead f).2 ≤ f.length * polynomial L P + P := by
  obtain ⟨hrows,hwork⟩ := scan_cost [] f [zero] L P hp hg
  have hend := cost_lookup (∅ : Finset (Fin n)) (measuredScan [] [zero] f).1 zero
  simp only [Finset.card_empty, Nat.add_zero, Nat.mul_one] at hend
  exact Nat.add_le_add hwork (hend.trans hrows)

end IALD.TrabalhoPorCorte
