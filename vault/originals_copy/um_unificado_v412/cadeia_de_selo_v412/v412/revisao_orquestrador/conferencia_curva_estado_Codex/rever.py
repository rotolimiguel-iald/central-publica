"""Recheck the two new Kimi sources and the independent generalization."""
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
previous = here.parent / "psibit_polinomio_por_letra_Codex"
sys.path.insert(0, str(previous))
import conferir

module = sys.argv[1]
kimi_modules = {"AFronteiraEOUnicoPortao", "ACurvaEAEstado"}
if module not in kimi_modules | {"ProjecaoDaFronteira"}:
    raise SystemExit("Módulo desconhecido")
if module in kimi_modules:
    source = module + ".lean"
    if (here / source).read_bytes() != (conferir.V412 / "candidatas_kimi" / source).read_bytes():
        raise SystemExit("Cópia diferente da fonte do Kimi")
conferir.ROOT = here
conferir.PREVIOUS = previous
raise SystemExit(0 if conferir.check(module) else 1)
