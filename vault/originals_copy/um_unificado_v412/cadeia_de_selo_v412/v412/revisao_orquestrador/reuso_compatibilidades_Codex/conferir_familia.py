"""Read evaluated counters from the compiled Lean modules on the original tapes."""
from pathlib import Path
import json
import subprocess
import sys

root = Path(__file__).resolve().parent
program = """
import LeitorDeReuso
import ObrigacoesJaSatisfeitas
import DespachoDeReuso

open Codex.LiteralSearchCost Codex.PolinomioPorEscolha

#eval show IO Unit from do
  for k in ([0, 1, 2, 5, 10] : List Nat) do
    let p := delayed k
    let w := original p
    let guardMoves := Codex.CertifiedRead.headMovements w
    let newMoves := Codex.ReuseReader.movements w
    let bits := Codex.ReuseReader.read w
    let checks0 := (traced p [⟨0,false⟩]).2
    let checks1 := (traced p [⟨0,true⟩]).2
    let rows := Codex.BranchCache.initial 4
    let tries := Codex.BranchCache.attempts p rows
    let ext := Codex.CoverCache.extensions p rows
    let probes := Codex.CoverCache.membershipBudget p rows
    let dispatch := Codex.ReuseDispatch.physicalMoves w
    IO.println s!"{k}|{w.length}|{checks0}|{checks1}|{guardMoves}|{newMoves}|{bits.1}|{bits.2}|{tries}|{ext}|{probes}|{dispatch}"
"""
process = subprocess.run(
    [sys.executable, "-B", "-X", "utf8", str(root / "conferir_local.py"),
     "LeitorDeReuso", "--stdin"],
    input=program.encode(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    cwd=root, check=False)
out = process.stdout.decode("utf-8")
if process.returncode:
    raise SystemExit(out)
rows = []
for line in out.splitlines():
    parts = line.split("|")
    if len(parts) != 12 or parts[6:8] != ["true", "true"]:
        raise ValueError(line)
    k, length, old_no, old_yes, guard, moves = map(int, parts[:6])
    attempted, extended, probes, dispatch = map(int, parts[8:])
    assert length == 6*k+14 and min(old_no, old_yes) >= 2**k
    assert moves == 66*k+166 and guard == 30*k+74
    assert dispatch == (guard if k == 0 else guard+length+moves)
    assert k < 2 or attempted == 6*k+8
    assert k == 0 or (extended == 12 and probes == 4*k+8)
    rows.append(dict(k=k, letras=length, folhas_ramo_0=old_no, folhas_ramo_1=old_yes,
                     movimentos_guarda=guard, movimentos_leitor_reuso=moves,
                     movimentos_despachante=dispatch,
                     ramos=[True, True], extensoes_da_camada_simples=attempted,
                     extensoes_com_certificados=extended, teto_consultas_de_pertinencia=probes))
if [row["k"] for row in rows] != [0, 1, 2, 5, 10]:
    raise ValueError("Unexpected set of input sizes")
print(json.dumps(rows, indent=2))

