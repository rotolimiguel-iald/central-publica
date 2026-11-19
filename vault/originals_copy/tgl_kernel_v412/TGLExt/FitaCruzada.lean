import TGLExt.PontePalavraVerbo

/- Fita única, cabeça única, alfabeto fixo. A sintaxe retangular de entrada
   contém as unidades negativas e as ocorrências positivas. Cada ida percorre
   todas as variáveis e lê a próxima cláusula. O retorno passa célula por célula.
   A coluna sentinela (sempre proibida e vazia) distingue cláusulas vazias
   mesmo em zero variáveis. -/
namespace IALD.FitaCruzada
open TGLExt.TraducaoTuring IALD.LeitorDaFormula

abbrev Bits (n : Nat) := Fin n → Bool

def positive {n} (r : Bits n) : Clausula n :=
  ((List.finRange n).filter r).map (fun i => ⟨i,true⟩)

def formula {n} (blocked : Bits n) (rows : List (Bits n)) : CNF n :=
  ((List.finRange n).filter blocked).map (fun i => [⟨i,false⟩]) ++ rows.map positive

def available {n} (blocked r : Bits n) : Bool :=
  (List.finRange n).any (fun i => !blocked i && r i)

theorem sat_spec {n} (blocked : Bits n) (rows : List (Bits n)) :
    rows.all (available blocked) = true ↔ SAT (formula blocked rows) := by
  have pos (r x : Bits n) : satisfeita (positive r) x = true ↔
      ∃ i, r i = true ∧ x i = true := by
    simp [satisfeita,positive,List.any_eq_true,Literal.vale]
  have units (x : Bits n) : passes (formula blocked rows) x = true ↔
      (∀ i, blocked i = true → x i = false) ∧
        (∀ r ∈ rows, ∃ i, r i = true ∧ x i = true) := by
    simp [passes,formula,List.all_eq_true,satisfeita,Literal.vale] at *
    constructor
    · rintro ⟨u,h⟩
      exact ⟨fun i hb => (u i).resolve_left (by simp [hb]),fun r hr => (pos r x).mp (h r hr)⟩
    · rintro ⟨u,h⟩
      refine ⟨?_,fun r hr => (pos r x).mpr (h r hr)⟩
      intro i
      cases e : blocked i with
      | false => exact Or.inl rfl
      | true => exact Or.inr (u i e)
  have av (r : Bits n) : available blocked r = true ↔
      ∃ i, blocked i = false ∧ r i = true := by
    simp [available,List.any_eq_true]
  rw [sat_iff,List.all_eq_true]
  constructor
  · intro h
    refine ⟨fun i => !blocked i,(units _).mpr ⟨?_,?_⟩⟩
    · intro i hi; simp [hi]
    · intro r hr
      obtain ⟨i,free,yes⟩ := (av _).mp (h r hr)
      exact ⟨i,yes,by simp [free]⟩
  · rintro ⟨x,hx⟩ r hr
    obtain ⟨pins,clauses⟩ := (units _).mp hx
    obtain ⟨i,yes,h⟩ := clauses r hr
    refine (av _).mpr ⟨i,?_,yes⟩
    cases b : blocked i with
    | false => rfl
    | true => have z := pins i b; simp [z] at h

inductive Cell where
  | head (blocked : Bool)
  | fresh (occurs : Bool)
  | spent
  | close
deriving DecidableEq, Repr

inductive Mode where | idle | take (blocked : Bool) | used
deriving DecidableEq, Repr

structure Registers where
  mode : Mode
  seen : Bool
  hit : Bool
deriving DecidableEq, Repr

def localRead (s : Registers) : Cell → Registers × Cell
  | .head b => (⟨.take b,s.seen,s.hit⟩,.head b)
  | .close => (⟨.idle,s.seen,s.hit⟩,.close)
  | .spent => (s,.spent)
  | .fresh v => match s.mode with
    | .take b => (⟨.used,true,s.hit || (!b && v)⟩,.spent)
    | _ => (s,.fresh v)

def sweep (s : Registers) : List Cell → Registers × List Cell
  | [] => (s,[])
  | c::cs =>
    let v := localRead s c
    let tail := sweep v.1 cs
    (tail.1,v.2::tail.2)

theorem sweep_append (a b : List Cell) (s : Registers) :
    sweep s (a ++ b) =
      ((sweep (sweep s a).1 b).1,(sweep s a).2 ++ (sweep (sweep s a).1 b).2) := by
  induction a generalizing s with
  | nil => rfl
  | cons a as ih => simp [sweep,ih]

theorem sweep_length (cs : List Cell) (s : Registers) : (sweep s cs).2.length = cs.length := by
  induction cs generalizing s with
  | nil => rfl
  | cons c cs ih => simp [sweep,ih]

theorem spent_run (k : Nat) (s : Registers) :
    sweep s (List.replicate k .spent) = (s,List.replicate k .spent) := by
  induction k with
  | zero => rfl
  | succ k ih => simp [List.replicate_succ,sweep,localRead,ih]

theorem used_run (xs : List Bool) (v a : Bool) :
    sweep ⟨.used,v,a⟩ (xs.map .fresh) = (⟨.used,v,a⟩,xs.map .fresh) := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simp [sweep,localRead,ih]

def block (b : Bool) (k : Nat) (xs : List Bool) : List Cell :=
  .head b :: (List.replicate k .spent ++ (xs.map .fresh ++ [.close]))

theorem block_take (b r : Bool) (k : Nat) (xs : List Bool) (s : Registers) :
    sweep s (block b k (r::xs)) =
      (⟨.idle,true,s.hit || (!b && r)⟩,block b (k+1) xs) := by
  simp [block,List.replicate_succ',sweep_append,spent_run,used_run,sweep,localRead,List.append_assoc]

theorem block_empty (b : Bool) (k : Nat) (s : Registers) :
    sweep s (block b k []) = (⟨.idle,s.seen,s.hit⟩,block b k []) := by
  simp [block,sweep_append,spent_run,sweep,localRead]

def columns {n} (blocked : Bits n) (k : Nat) (rows : List (Bits n))
    (ids : List (Fin n)) : List Cell :=
  ids.flatMap (fun i => block (blocked i) k (rows.map (fun r => r i)))

def tape {n} (blocked : Bits n) (k : Nat) (rows : List (Bits n)) : List Cell :=
  block true k (rows.map (fun _ => false)) ++ columns blocked k rows (List.finRange n)

theorem cols_cons {n} (b : Bits n) (k : Nat) (rs : List (Bits n)) (i : Fin n) (is : List (Fin n)) :
    columns b k rs (i::is) = block (b i) k (rs.map (fun r => r i)) ++ columns b k rs is := rfl

theorem cols_take {n} (blocked r : Bits n) (k : Nat) (rows : List (Bits n))
    (ids : List (Fin n)) (a : Bool) :
    sweep ⟨.idle,true,a⟩ (columns blocked k (r::rows) ids) =
      (⟨.idle,true,a || ids.any (fun i => !blocked i && r i)⟩,columns blocked (k+1) rows ids) := by
  induction ids generalizing a with
  | nil => simp [columns,sweep]
  | cons i ids ih =>
    simp only [cols_cons,List.map_cons,List.any_cons,sweep_append,block_take,ih,Bool.or_assoc]

theorem cols_empty {n} (blocked : Bits n) (k : Nat) (ids : List (Fin n)) (s a : Bool) :
    sweep ⟨.idle,s,a⟩ (columns blocked k [] ids) =
       (⟨.idle,s,a⟩,columns blocked k [] ids) := by
  induction ids with
  | nil => rfl
  | cons i ids ih =>
    simp only [cols_cons,List.map_nil,sweep_append,block_empty,ih]

def zero : Registers := ⟨.idle,false,false⟩

theorem round_take {n} (blocked r : Bits n) (k : Nat) (rows : List (Bits n)) :
    sweep zero (tape blocked k (r::rows)) =
       (⟨.idle,true,available blocked r⟩,tape blocked (k+1) rows) := by
  simp [tape,sweep_append,block_take,zero,cols_take,available]

theorem round_empty {n} (blocked : Bits n) (k : Nat) :
    sweep zero (tape blocked k []) = (zero,tape blocked k []) := by
  simp [tape,sweep_append,block_empty,cols_empty,zero]

/-- A posição da cabeça é o início da lista à direita. A lista esquerda está
    invertida. Só a célula corrente muda, e cada passo atravessa no máximo uma
    célula. As duas bordas da fita finita têm delimitadores distinguíveis. -/
inductive Machine where
  | read (good : Bool) (reg : Registers) (left right : List Cell)
  | rewind (good : Bool) (left right : List Cell)
  | halt (answer : Bool)
deriving DecidableEq, Repr

def step : Machine → Machine
  | .read good reg left (c::cs) =>
    let v := localRead reg c
    .read good v.1 (v.2::left) cs
  | .read good reg left [] =>
    if reg.seen then .rewind (good && reg.hit) left [] else .halt good
  | .rewind good (c::cs) right => .rewind good cs (c::right)
  | .rewind good [] right => .read good zero [] right
  | .halt ans => .halt ans

def execute : Nat → Machine → Machine
  | 0,s => s
  | n+1,s => execute n (step s)

theorem execute_add (a b : Nat) (s : Machine) : execute (a+b) s = execute b (execute a s) := by
  induction a generalizing s with
  | zero => simp [execute]
  | succ a ih => rw [Nat.succ_add]; exact ih _

theorem right_steps (pre rest left : List Cell) (g : Bool) (s : Registers) :
    execute pre.length (.read g s left (pre++rest)) =
      .read g (sweep s pre).1 ((sweep s pre).2.reverse ++ left) rest := by
  induction pre generalizing s left with
  | nil => rfl
  | cons c cs ih =>
    simp only [List.length_cons,List.cons_append,execute,step,sweep,List.reverse_cons,
      List.append_assoc]
    exact ih _ _

theorem left_steps (left right : List Cell) (g : Bool) :
    execute left.length (.rewind g left right) = .rewind g [] (left.reverse ++ right) := by
  induction left generalizing right with
  | nil => rfl
  | cons c cs ih =>
    simp only [List.length_cons,execute,step,List.reverse_cons,List.append_assoc,List.singleton_append]
    exact ih _

theorem full_round {inp out : List Cell} {bit g : Bool}
    (h : sweep zero inp = (⟨.idle,true,bit⟩,out)) :
    execute (2*inp.length+2) (.read g zero [] inp) = .read (g && bit) zero [] out := by
  have len : out.length = inp.length := by simpa [h] using sweep_length inp zero
  have right := right_steps inp [] [] g zero
  simp only [List.append_nil,h] at right
  have left := left_steps out.reverse [] (g && bit)
  simp only [List.length_reverse,List.reverse_reverse,List.append_nil] at left
  rw [show 2*inp.length+2 = (inp.length+1)+(out.length+1) by omega, execute_add]
  rw [execute_add inp.length 1,right]
  change execute (out.length+1) (.rewind (g && bit) out.reverse []) = _
  rw [execute_add out.length 1,left]
  rfl

def time (L m : Nat) := m*(2*L+2)+(L+1)

theorem exact_steps {n} (blocked : Bits n) (k : Nat) (rows : List (Bits n)) (g : Bool) :
    execute (time (tape blocked k rows).length rows.length) (.read g zero [] (tape blocked k rows)) =
      .halt (g && rows.all (available blocked)) := by
  induction rows generalizing k g with
  | nil =>
    have h := right_steps (tape blocked k []) [] [] g zero
    simp only [List.append_nil,round_empty] at h
    simp only [time,List.length_nil,Nat.zero_mul,Nat.zero_add,List.all_nil,Bool.and_true]
    rw [execute_add _ 1,h]; rfl
  | cons r rows ih =>
    have h := round_take blocked r k rows
    have len : (tape blocked (k+1) rows).length = (tape blocked k (r::rows)).length := by
      simpa only [h] using sweep_length (tape blocked k (r::rows)) zero
    rw [show time (tape blocked k (r::rows)).length (r::rows).length =
      (2*(tape blocked k (r::rows)).length+2)+time (tape blocked (k+1) rows).length rows.length by
        rw [len]; simp [time,Nat.succ_mul]; omega,
      execute_add,full_round h,ih]
    simp [Bool.and_assoc]

theorem row_count_le_length {n} (b : Bits n) (rs : List (Bits n)) :
    rs.length ≤ (tape b 0 rs).length := by
  simp [tape,block]; omega

theorem tape_length {n} (b : Bits n) (k : Nat) (rs : List (Bits n)) :
    (tape b k rs).length = (n+1)*(k+rs.length+2) := by
  have len (p : Bool) (xs : List Bool) : (block p k xs).length = k+xs.length+2 := by
    simp [block]; omega
  have cols (is : List (Fin n)) : (columns b k rs is).length = is.length*(k+rs.length+2) := by
    induction is with
    | nil => simp [columns]
    | cons i is ih =>
      simp only [cols_cons,List.length_append,len,List.length_map,ih,List.length_cons,Nat.succ_mul]
      omega
  simp only [tape,List.length_append,len,List.length_map,cols,List.length_finRange,Nat.succ_mul]
  omega

/-- Limite físico sobre as transições na própria fita com delimitadores. -/
theorem physical_word {n} (b : Bits n) (rs : List (Bits n)) (t : ℝ)
    (ht : (n:ℝ)*Real.log 2 < t) :
    ∃ steps ans, steps ≤ 2*((tape b 0 rs).length+1)^2 + ((tape b 0 rs).length+1) ∧
      execute steps (.read true zero [] (tape b 0 rs)) = .halt ans ∧
      (ans = true ↔ TGLExt.OPsibitEACompressao.palavra (custoCNF (formula b rs)) t) := by
  let L := (tape b 0 rs).length
  refine ⟨time L rs.length,rs.all (available b),?_,?_,(sat_spec b rs).trans
    (TGLExt.OPsibitEACompressao.a_palavra_decide _ ht _)⟩
  · have hm : rs.length ≤ L+1 := Nat.le_trans (row_count_le_length b rs) (Nat.le_succ L)
    have h := Nat.mul_le_mul_right (2*L+2) hm
    dsimp [time]
    change _ ≤ 2*(L+1)^2+(L+1)
    nlinarith
  · simpa [L] using exact_steps b 0 rs true

end IALD.FitaCruzada
