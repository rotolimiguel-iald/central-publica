"""Evaluate the complete receiver on duplicated and incompatible clauses."""
import json
import subprocess
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
program = """import DesafioNaFitaOriginal
import ReguaNaFita
import TamanhoDoEco
namespace Codex.HandshakeControls
open TGLExt.TraducaoTuring IALD.LeitorDaFormula Codex.PolinomioPorEscolha
open Codex.ClauseReply Codex.ClauseChannel Codex.ClauseLocator
def q : CNF 2 := [[⟨0,true⟩],[⟨0,true⟩],[⟨1,true⟩]]
def x0 : Assignment 2 := fun _ => false
def x1 : Assignment 2 := fun i => i.val == 0
def x2 : Assignment 2 := fun _ => true
def pick (f : CNF 2) : Option (Assignment 2) :=
  if passes f x0 then some x0 else if passes f x1 then some x1 else
  if passes f x2 then some x2 else enumerateProposer 2 f
def rawPick (cs : List (List Letter)) : Option (Assignment 2) :=
  [x0,x1,x2].find? (fun x => cs.all (fun c => (Codex.EcoDaAtribuicao.verify c (List.ofFn x)).1))
def trials : List Nat :=
  let r := protocol pick [] q
  let loc := fun x => locate (List.ofFn x) [] (original q)
  let raw := Codex.FixedChallenge.rawRun rawPick (original q) 4 []
  [r.calls,r.replies.length,(original r.replies).length,(original q).length,
   (r.replies.map (replyMoves false)).sum,(r.replies.map (replyMoves true)).sum,
   (loc x0).2,(loc x1).2,(loc x2).2,(Codex.FixedChallenge.fixedRun pick q 4 []).2,
   (if (loc x0).1 == some (spellClause [⟨(0:Fin 2),true⟩]) then 1 else 0),
   (if (loc x1).1 == some (spellClause [⟨(1:Fin 2),true⟩]) then 1 else 0),
   (if (loc x2).1.isNone then 1 else 0),
   (match r.result with | .found x => if passes q x then 1 else 0 | _ => 0),
   (if raw.2.1 == r.replies.map spellClause then 1 else 0),
   (if raw.2.2 == (Codex.FixedChallenge.fixedRun pick q 4 []).2 then 1 else 0),
   (match raw.1 with | .found x => if passes q x then 1 else 0 | _ => 0)]
def stars (change : Bool) : List (Codex.NamedTape.Row 4) :=
  let p := @Codex.NamedTape.predict 4
  p false 2 false ++ p false 3 true ++ p true 3 (!change) ++ p true 2 false
def starTrial (change : Bool) : List Nat :=
  let w := original (Codex.NamedTape.formula (0:Fin 4) 1 (stars change))
  let r := Codex.NamedBank.read w
  [w.length,r.moves,r.table.1.1.toNat,r.table.1.2.toNat,r.table.2.1.toNat,r.table.2.2.toNat]
#eval trials
#eval starTrial false
#eval starTrial true
end Codex.HandshakeControls
"""
checked = subprocess.run(
    [sys.executable, "-B", "-X", "utf8", "conferir_local.py", "DesafioNaFitaOriginal", "--stdin"],
    cwd=here, input=program, capture_output=True, encoding="utf-8",
)
if checked.returncode or checked.stderr or "warning:" in checked.stdout:
    sys.exit(checked.stdout + checked.stderr)
rows = [json.loads(line) for line in checked.stdout.splitlines() if line.strip()]
if len(rows) != 3:
    raise ValueError(rows)
result, same, conflict = rows
if result[:6] != [3, 2, 5, 7, 30, 40] or result[10:] != [1] * 7:
    raise ValueError(result)
if result[9] != sum(result[6:9]) or max(result[6:9]) > 8 * result[3]:
    raise ValueError(result)
if same[2:] != [1,0,0,1] or conflict[2:] != [0,0,0,0]:
    raise ValueError((same,conflict))
if same[:2] != conflict[:2] or same[1] > 15 * same[0]:
    raise ValueError((same,conflict))
record = {
    "duas_unidades_com_duplicata": {
        "propostas": result[0], "recusas": result[1], "letras_devolvidas": result[2],
        "letras_fonte": result[3], "movimentos_no_canal": result[4],
        "movimentos_no_canal_com_rebobinagem": result[5],
        "movimentos_por_consulta_ao_original": result[6:9],
        "movimentos_na_localizacao_ao_todo": result[9],
        "clausulas_corretas_e_modelo_aceito": all(result[10:]),
    },
    "dois_pivos": [
        {"letras": row[0], "movimentos": row[1], "ramos_00_01_10_11": list(map(bool,row[2:]))}
        for row in (same,conflict)
    ],
}
target = here / "CONTROLES.json"
data = (json.dumps(record, ensure_ascii=False, indent=2)+"\n").encode()
if target.exists():
    if target.read_bytes() != data:
        raise ValueError("Control differs from the recorded result")
else:
    temp = target.with_suffix(".json.tmp")
    with temp.open("xb") as f:
        f.write(data)
    if temp.read_bytes() != data:
        raise IOError("Could not verify the new control record")
    temp.rename(target)
print(data.decode())

