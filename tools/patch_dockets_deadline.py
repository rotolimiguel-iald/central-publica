# -*- coding: utf-8 -*-
"""Patch the 15 non-ACOM docket.yaml files with the operator's deadline decision.

Operator decision (2026-07-09): the Paris window for the NEW ePCT deposit of the
15 non-ACOM patents is counted from the internal priority to ACOM (2025-12-05):
  - precautionary target: 2026-11-30 (last day of November)
  - FATAL: 2026-12-05
Alert level -> amarelo. Preserves all other lines/comments (line-oriented patch).
The ACOM docket (VIVO_DEPOSITADO_E_PAGO) is left untouched.
"""
import re
from pathlib import Path

PATENTS = Path(r"C:\IALD\Central de Patentes\patents")
ACOM = "BR102025026951-1_ACOM"

JANELA_BLOCK = (
    '# Janela de Paris para o NOVO ePCT (decisão do operador 09/07/2026):\n'
    '# contada da PRIORIDADE INTERNA ao ACOM (2025-12-05); mesma data p/ as 15.\n'
    'janela_paris_12m: "2026-12-05"                 # DATA FATAL do novo depósito ePCT [LEGAL]\n'
    'janela_paris_alvo_precaucional: "2026-11-30"   # alvo de trabalho (último dia de novembro)\n'
)


def patch(path: Path) -> int:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    out, changed = [], 0
    replaced_janela = False
    for ln in lines:
        stripped = ln.lstrip()
        if re.match(r'janela_paris_12m\s*:', stripped):
            out.append(JANELA_BLOCK)
            changed += 1
            replaced_janela = True
            continue
        if re.match(r'alert_level\s*:', stripped):
            out.append('alert_level: "amarelo"   # ~144 d até o alvo 30/11/2026; '
                        'prazo mais crítico do acervo (decisão do operador) [LEGAL]\n')
            changed += 1
            continue
        # recontextualize the abandoned-attempt framing (no "prescrito/histórico morto")
        if "PRESCRITO" in ln or "prescrito" in ln:
            ln = re.sub(
                r'#.*$',
                '# tentativa de protocolo 17/02/2026 (PCT/BR2026/050068-076) ABANDONADA '
                'DE PROPÓSITO — a substituir por novo depósito, não proteção perdida',
                ln)
            changed += 1
        out.append(ln)
    if not replaced_janela:
        return -1
    path.write_text("".join(out), encoding="utf-8")
    return changed


def main() -> None:
    total = 0
    for d in sorted(PATENTS.iterdir()):
        if not d.is_dir() or d.name == ACOM:
            continue
        dk = d / "docket.yaml"
        if not dk.exists():
            print(f"  [SKIP] sem docket: {d.name}")
            continue
        n = patch(dk)
        print(f"  {d.name}: {n} linhas alteradas")
        total += 1
    print(f"dockets não-ACOM patchados: {total} (esperado 15)")


if __name__ == "__main__":
    main()
