import TGLExt.PolinomioPorEscolha

/- Compilação a partir dos caracteres da CNF original. Uma cabeça de entrada
   avança, uma de saída escreve, e duas cabeças auxiliares unárias se deslocam
   a partir de uma borda fixa. Nenhum passo copia um natural: os endereços
   passam de uma cabeça à outra por movimentos unitários. Cada cláusula
   retém sua primeira cabeça positiva, ou nenhuma se ela só tem negativos. -/
namespace IALD.CompilaHornNaFita
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula Codex.HornCross Codex.CrossSelectors
open Codex.PolinomioPorEscolha (Letter spell spellClause original weight)
open Codex.SparseHornTape (Sym arg args line program)
variable {n : Nat}

inductive Phase where | scan | need | save | skip | issue | halt
deriving DecidableEq, Repr

structure Cfg where
  mode : Phase
  input : List Letter
  out : List Sym
  cur : Nat
  has : Bool
  saved : Nat

def step (c : Cfg) : Cfg := match c.mode with
  | .halt => c
  | .scan => match c.input with
    | [] => {c with mode:=.halt}
    | .tick :: t => {c with input:=t,cur:=c.cur+1}
    | .sign false :: t => {c with mode:=.need,input:=t}
    | .sign true :: t =>
      if c.has then {c with mode:=.skip,input:=t} else {c with mode:=.save,input:=t,has:=true}
    | .delimiter :: t =>
      if c.has then {c with mode:=.issue,input:=t}
      else {c with input:=t,out:=.deny::c.out}
  | .need => match c.cur with
    | 0 => {c with mode:=.scan,out:=.need::c.out}
    | k+1 => {c with cur:=k,out:=.tick::c.out}
  | .save => match c.cur with
    | 0 => {c with mode:=.scan}
    | k+1 => {c with cur:=k,saved:=c.saved+1}
  | .skip => match c.cur with
    | 0 => {c with mode:=.scan}
    | k+1 => {c with cur:=k}
  | .issue => match c.saved with
    | 0 => {c with mode:=.scan,has:=false,out:=.setBit::c.out}
    | k+1 => {c with saved:=k,out:=.tick::c.out}

def run : Nat → Cfg → Cfg
  | 0,c => c
  | k+1,c => run k (step c)

theorem run_add (k j : Nat) (s : Cfg) : run (k+j) s = run j (run k s) := by
  induction k generalizing s with
  | zero => simp [run]
  | succ k ih => rw [Nat.succ_add]; exact ih _
theorem one (s : Cfg) : run 1 s = step s := rfl

def ready (ip : List Letter) (out : List Sym) (h : Option Nat) : Cfg :=
  ⟨.scan,ip,out,0,h.isSome,h.getD 0⟩

theorem ticks (k j : Nat) (ip : List Letter) (out : List Sym) (b : Bool) (z : Nat) :
    run k ⟨.scan,List.replicate k .tick ++ ip,out,j,b,z⟩ = ⟨.scan,ip,out,j+k,b,z⟩ := by
  induction k generalizing j with
  | zero => rfl
  | succ k ih =>
    rw [List.replicate_succ]
    change run k ⟨.scan,List.replicate k .tick ++ ip,out,j+1,b,z⟩ = _
    rw [ih,show j+1+k=j+(k+1) by omega]

theorem need_trace (k : Nat) (ip : List Letter) (out : List Sym) (b : Bool) (z : Nat) :
    run (k+1) ⟨.need,ip,out,k,b,z⟩ =
      ⟨.scan,ip,.need :: (List.replicate k .tick ++ out),0,b,z⟩ := by
  induction k generalizing out with
  | zero => rfl
  | succ k ih =>
    change run (k+1) ⟨.need,ip,.tick::out,k,b,z⟩ = _
    rw [ih,List.replicate_succ']; simp only [List.append_assoc,List.singleton_append]

theorem save_trace (k z : Nat) (ip : List Letter) (out : List Sym) :
    run (k+1) ⟨.save,ip,out,k,true,z⟩ = ⟨.scan,ip,out,0,true,z+k⟩ := by
  induction k generalizing z with
  | zero => rfl
  | succ k ih =>
    change run (k+1) ⟨.save,ip,out,k,true,z+1⟩ = _
    rw [ih,show z+1+k=z+(k+1) by omega]

theorem skip_trace (k z : Nat) (ip : List Letter) (out : List Sym) :
    run (k+1) ⟨.skip,ip,out,k,true,z⟩ = ⟨.scan,ip,out,0,true,z⟩ := by
  induction k with | zero => rfl | succ k ih => exact ih

theorem issue_trace (z : Nat) (ip : List Letter) (out : List Sym) :
    run (z+1) ⟨.issue,ip,out,0,true,z⟩ =
      ready ip (.setBit :: (List.replicate z .tick ++ out)) none := by
  induction z generalizing out with
  | zero => rfl
  | succ z ih =>
    change run (z+1) ⟨.issue,ip,.tick::out,0,true,z⟩ = _
    rw [ih,List.replicate_succ']; simp only [List.append_assoc,List.singleton_append]

def selectLit (h : Option Nat) (l : Literal n) : Option Nat :=
  if l.pos then h.or (some l.var.val) else h
def bodyLit (l : Literal n) : List Sym := if l.pos then [] else arg l.var .need

theorem read_lit (l : Literal n) (ip : List Letter) (out : List Sym) (h : Option Nat) :
    run (2*(spell l).length) (ready (spell l ++ ip) out h) =
       ready ip ((bodyLit l).reverse ++ out) (selectLit h l) := by
  obtain ⟨i,b⟩ := l
  have size : 2*(spell (⟨i,b⟩ : Literal n)).length = i.val + (1+(i.val+1)) := by
    simp [spell]; omega
  rw [size,run_add]
  simp only [ready,spell,List.append_assoc,List.singleton_append,ticks,Nat.zero_add]
  rw [run_add 1 (i.val+1),one]
  cases b <;> cases h <;>
    simp [step,need_trace,skip_trace,save_trace,selectLit,bodyLit,arg]

theorem read_lits (cs : Clausula n) (ip : List Letter) (out : List Sym) (h : Option Nat) :
    run (2*(cs.flatMap spell).length) (ready (cs.flatMap spell ++ ip) out h) =
      ready ip ((cs.flatMap bodyLit).reverse ++ out) (cs.foldl selectLit h) := by
  induction cs generalizing h out with
  | nil => rfl
  | cons l cs ih =>
    simp only [List.flatMap_cons,List.length_append,Nat.mul_add,List.append_assoc,
      List.reverse_append,List.foldl_cons]
    rw [run_add,read_lit,ih]

theorem body_eq (c : Clausula n) : c.flatMap bodyLit = args (names c false) := by
  induction c with
  | nil => rfl
  | cons l c ih =>
    rcases l with ⟨i,b⟩
    cases b <;> simp [bodyLit,names,args] at ih ⊢ <;> exact ih

def chosen (c : Clausula n) : Rule n := ⟨names c false,(names c true).head?⟩

theorem select_eq (c : Clausula n) (h : Option Nat) :
    c.foldl selectLit h = h.or ((chosen c).head.map Fin.val) := by
  induction c generalizing h with
  | nil => cases h <;> rfl
  | cons l c ih =>
    rcases l with ⟨i,b⟩
    cases b <;> cases h <;>
      simp [selectLit,List.foldl_cons,ih,chosen,names]

def term : Option Nat → List Sym
  | none => [.deny]
  | some k => List.replicate k .tick ++ [.setBit]

def termTime : Option Nat → Nat
  | none => 1
  | some k => k+2

theorem delimiter (h : Option Nat) (ip : List Letter) (out : List Sym) :
    run (termTime h) (ready (.delimiter :: ip) out h) = ready ip ((term h).reverse ++ out) none := by
  cases h with
  | none => rfl
  | some k =>
    change run (k+1) ⟨.issue,ip,out,0,true,k⟩ = _
    rw [issue_trace]
    simp [term]

theorem line_term (r : Rule n) :
    line r = args r.body ++ term (r.head.map Fin.val) := by
  obtain ⟨xs,h⟩ := r
  cases h <;> rfl

def clauseTime (c : Clausula n) :=
  2*(c.flatMap spell).length + termTime ((chosen c).head.map Fin.val)

theorem read_clause (c : Clausula n) (ip : List Letter) (out : List Sym) :
    run (clauseTime c) (ready (spellClause c ++ ip) out none) =
      ready ip ((line (chosen c)).reverse ++ out) none := by
  simp only [clauseTime,spellClause,List.append_assoc,List.singleton_append]
  rw [run_add,read_lits,select_eq]
  change run _ (ready _ _ ((chosen c).head.map Fin.val)) = _
  rw [delimiter,line_term,List.reverse_append,List.append_assoc,body_eq]
  rfl

def totalTime (p : CNF n) := (p.map clauseTime).sum

theorem compile (p : CNF n) (ip : List Letter) (out : List Sym) :
    run (totalTime p) (ready (original p ++ ip) out none) =
      ready ip ((program (p.map chosen)).reverse ++ out) none := by
  induction p generalizing out with
  | nil => rfl
  | cons c p ih =>
    change run (clauseTime c + totalTime p) (ready ((spellClause c ++ original p) ++ ip) out none) = _
    rw [List.append_assoc,run_add,read_clause,ih]
    change _ = ready ip ((line (chosen c) ++ program (p.map chosen)).reverse ++ out) none
    rw [List.reverse_append,List.append_assoc]

theorem chosen_mem (c : Clausula n) : chosen c ∈ alternatives c := by
  unfold chosen alternatives
  cases e : names c true <;> simp

theorem term_bound (c : Clausula n) :
    termTime ((chosen c).head.map Fin.val) ≤ (c.flatMap spell).length+2 := by
  have part := Codex.PolinomioPorEscolha.sign_partition c
  unfold chosen
  cases h : names c true with
  | nil => simp [termTime]
  | cons i is =>
    have hi : i ∈ names c true := by simp [h]
    have mem := Codex.PolinomioPorEscolha.weight_member (names c true) i hi
    change i.val+2 ≤ _
    omega

theorem time_bound (p : CNF n) : totalTime p ≤ 3*(original p).length := by
  induction p with
  | nil => rfl
  | cons c p ih =>
    have t := term_bound c
    change 2*(c.flatMap spell).length + termTime ((chosen c).head.map Fin.val) + totalTime p ≤
      3*((spellClause c) ++ original p).length
    simp only [spellClause,List.length_append,List.length_cons,List.length_nil]
    omega

/-- Soma dos deslocamentos de entrada, saída e ambas as cabeças auxiliares.
    O comprimento das listas e as diferenças são medidores, não operações do controle. -/
def moves (s t : Cfg) :=
  Nat.dist s.input.length t.input.length + Nat.dist s.out.length t.out.length +
    Nat.dist s.cur t.cur + Nat.dist s.saved t.saved

def travel : Nat → Cfg → Nat | 0,_ => 0 | k+1,c => moves c (step c) + travel k (step c)

theorem one_step (c : Cfg) : moves c (step c) ≤ 2 := by
  rcases c with ⟨m,ip,o,i,b,j⟩
  cases m with
  | halt => simp [step,moves]
  | need => cases i <;> simp [step,moves,Nat.dist]
  | save => cases i <;> simp [step,moves,Nat.dist]
  | skip => cases i <;> simp [step,moves,Nat.dist]
  | issue => cases j <;> simp [step,moves,Nat.dist]
  | scan =>
    cases ip with
    | nil => simp [step,moves]
    | cons a ip => cases a with
      | tick => simp [step,moves,Nat.dist]
      | sign v => cases v <;> cases b <;> simp [step,moves,Nat.dist]
      | delimiter => cases b <;> simp [step,moves,Nat.dist]

theorem travel_bound (k : Nat) (c : Cfg) : travel k c ≤ 2*k := by
  induction k generalizing c with
  | zero => rfl
  | succ k ih =>
    change moves c (step c) + travel k (step c) ≤ _
    have := one_step c
    have := ih (step c)
    omega

def IsHorn (p : CNF n) := ∀ c ∈ p, (names c true).length ≤ 1

theorem unique_alternative (c : Clausula n) (h : (names c true).length ≤ 1) :
    alternatives c = [chosen c] := by
  unfold chosen alternatives
  cases e : names c true with
  | nil => rfl
  | cons i is =>
    cases is with
    | nil => rfl
    | cons j js => simp [e] at h

theorem horn_select (p : CNF n) (h : IsHorn p) : programs p = [p.map chosen] := by
  induction p with
  | nil => rfl
  | cons c p ih =>
    have hc := unique_alternative c (h _ List.mem_cons_self)
    have hp := ih (fun d hd => h d (List.mem_cons_of_mem _ hd))
    simp [programs,hc,hp]

theorem semantic (p : CNF n) (h : IsHorn p) :
    palavraDaFormula ((p.map chosen).map asClause) = palavraDaFormula p := by
  have sig := selector_word p
  rw [horn_select p h] at sig
  rw [← horn_word]
  change checkProgram (p.map chosen) = palavraDaFormula p
  cases e : checkProgram (p.map chosen) <;> simpa [scan,e] using sig

/-- A máquina começa com os símbolos de p e quatro cabeças em suas bordas.
    O resultado da fita de saída, lida na ordem de escrita, é o programa Horn.
    O limite vale também fora da classe, mas lá se escolhe apenas um candidato. -/
theorem physical_compilation (p : CNF n) :
    let c := ready (original p) [] none
    let L := (original p).length
    ∃ T ≤ 3*L+1, travel T c ≤ 2*(3*L+1) ∧ (run T c).mode = .halt ∧
      (run T c).out.reverse = program (p.map chosen) := by
  refine ⟨totalTime p+1,Nat.add_le_add_right (time_bound p) 1,?_,?_,?_⟩
  · exact (travel_bound _ _).trans (Nat.mul_le_mul_left _ (Nat.add_le_add_right (time_bound p) 1))
  · have h := compile p [] []
    simp only [List.append_nil] at h
    rw [run_add, h,one]; rfl
  · have h := compile p [] []
    simp only [List.append_nil] at h
    rw [run_add,h,one]
    simp [ready,step]

/-- Na troca de controle, a cabeça permanece à direita do último símbolo.
    A próxima máquina precisa realmente rebobinar a fita que acabou de receber. -/
def dock (c : Cfg) : Codex.SparseHornTape.Cfg := ⟨.back,true,false,false,c.out,[],0,∅⟩

/-- Composição dos três traços, partindo da CNF bruta Horn: compila, rebobina,
    verifica. O orçamento inclui uma transição adicional de troca de controle. -/
theorem flat_horn_stages (p : CNF n) (horn : IsHorn p) :
    let g := ready (original p) [] none
    let L := (original p).length
    ∃ K R V, K+1+R+V ≤ 4*L+3+Codex.PolinomioPorEscolha.budget L ∧
      (run K g).mode = .halt ∧
      Codex.SparseHornTape.run R (dock (run K g)) = Codex.SparseHornTape.start (p.map chosen) ∅ ∧
      (Codex.SparseHornTape.run (R+V) (dock (run K g))).mode = .halt (palavraDaFormula p) ∧
      travel K g + Codex.SparseHornTape.travel (R+V) (dock (run K g)) ≤
        2*(4*L+3+Codex.PolinomioPorEscolha.budget L) := by
  let g := ready (original p) [] none
  let q := p.map chosen
  let L := (original p).length
  obtain ⟨K,hK,cm,done,output⟩ := physical_compilation p
  have rev : (run K g).out = (program q).reverse := by
    simpa [g,q] using congrArg List.reverse output
  have back : Codex.SparseHornTape.run ((program q).length+1) (dock (run K g)) =
      Codex.SparseHornTape.start q ∅ := by
    unfold dock
    rw [rev]
    have h := Codex.SparseHornTape.back_trace (program q).reverse [] (∅ : Finset Nat) true false false
    simpa [Codex.SparseHornTape.start,Codex.SparseHornTape.written] using h
  have mem : q ∈ programs p := by rw [horn_select p horn]; simp [q]
  have len := Codex.PolinomioPorEscolha.selected_length p q mem
  have bd := Codex.PolinomioPorEscolha.budget_le _ _ len
  obtain ⟨V,ht,_,hv⟩ := Codex.SparseHornTape.sparse_horn_tape q
  have vb : V ≤ Codex.PolinomioPorEscolha.budget L := ht.trans bd
  have kb : K ≤ 3*L+1 := hK
  have wb : (program q).length ≤ L := len
  have all : K+1+((program q).length+1)+V ≤ 4*L+3+Codex.PolinomioPorEscolha.budget L := by omega
  refine ⟨K,(program q).length+1,V,all,done,back,?_,?_⟩
  · rw [Codex.SparseHornTape.run_add,back,hv,semantic p horn]
  · have left := travel_bound K g
    have right := Codex.SparseHornTape.travel_bound ((program q).length+1+V) (dock (run K g))
    change travel K g + Codex.SparseHornTape.travel ((program q).length+1+V) (dock (run K g)) ≤
      2*(4*L+3+Codex.PolinomioPorEscolha.budget L)
    omega

end IALD.CompilaHornNaFita
