"""Evaluate finite controls in the pinned Lean environment."""
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
program = """
import UmaChaveAngular
import PrecisaoDaChave
import TransporteDaInscricao
open Codex.PolinomioPorEscolha Codex.OrthantRelation Codex.SinglePhase

def examples (i : Nat) : Codex.ChainTape.Row × List Codex.ChainTape.Row :=
  if i=0 then ((false,true),[(true,false)]) else ((true,true),[(false,false)])
def formula := Codex.ChainTape.ladder (n:=3) examples 2 (by decide)
def combined := join (twoVarKey equalityCNF) (twoVarKey inequalityCNF)
#eval show IO Unit from do
  let measured := turn (phaseTag combined) + 2 + (1/64 : ℚ)
  let states := List.finRange 16
  let fees := (original (formula ++ Codex.ChainTape.unit (2 : Fin 3) true)).length
  let bits := Codex.ChainTape.reader (original (formula ++ Codex.ChainTape.unit (2 : Fin 3) true))
  let rawtag := keyOf ((original formula).foldl Codex.ChainTape.see (Codex.ChainTape.clean Codex.ChainTape.freshKey))
  IO.println s!"chain|{fees}|{bits.1}|{bits.2}|{rawtag.val}|{(phaseTag combined).val}|{(slice measured).val}"
  let good := states.all (fun t => slice (turn t - 3 - 1/64) == t && slice (turn t + 2 + 1/64) == t)
  IO.println s!"sectors|{states.length}|{good}"
  for n in ([1,3,7,15] : List Nat) do
    let f := Codex.DenseAngle.source n true
    let g := Codex.DenseAngle.source n false
    IO.println s!"dense|{n+1}|{(original f).length}|{(original g).length}|{2^(n+1)}"
"""
proc = subprocess.run(
    [sys.executable, "-B", "-X", "utf8", str(root / "conferir_local.py"),
     "UmaChaveAngular", "--stdin"], input=program.encode(), cwd=root,
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
out = proc.stdout.decode("utf-8")
if proc.returncode:
    raise SystemExit(out)
lines = out.splitlines()
assert lines[:2] == ["chain|24|true|false|6|6|6","sectors|16|true"], lines
dense = []
for line in lines[2:]:
    name, w, a, b, digits = line.split("|")
    w, a, b, digits = map(int, (w, a, b, digits))
    assert name == "dense" and a == b == w*(w-1)//2+2*w+2 and digits == 2**w
    dense.append({"variaveis":w, "letras_de_cada_CNF":a, "digitos_na_chave_densa":digits})
assert [d["variaveis"] for d in dense] == [2,4,8,16]
print(json.dumps({"stdout":lines, "cadeia":{"letras":24,"ramos":[True,False],"setor_antes_da_unidade":6},
                  "setores_testados_em_dois_desvios":16,"denso":dense}, ensure_ascii=False, indent=2))
