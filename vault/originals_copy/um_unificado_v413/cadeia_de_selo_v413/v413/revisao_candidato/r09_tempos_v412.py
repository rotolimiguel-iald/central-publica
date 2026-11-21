# r09 -- os tempos do rito da v412 (SO LEITURA): da materializacao do kernel ao veredito do kernel, e do autoteste do fail-closed.
import json, os, sys
from datetime import datetime

P = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\rodada_v412_stdout_tempos.jsonl"
MARCAS = ["[kernel embutido] materializado", "lake build: True", "TGL_KERNEL_STAGE1_VERIFIED", "AUTOTESTE DO FAIL-CLOSED", "com sorry injetado", "restaurado da fonte", "FAIL_CLOSED_SELFTEST_PASSED"]


def main():
    linhas = []
    with open(P, "r", encoding="utf-8") as fh:
        for l in fh:
            try:
                linhas.append(json.loads(l))
            except Exception:
                pass
    print("n registros:", len(linhas), "chaves:", list(linhas[0].keys()) if linhas else None)
    t0 = None
    for i, r in enumerate(linhas):
        txt = str(r.get("linha") or r.get("texto") or "")
        for m in MARCAS:
            if m in txt:
                h = r.get("hora_utc") or r.get("t")
                print(i, h, txt[:120])
    print("primeira:", linhas[0].get("hora_utc"), " ultima:", linhas[-2].get("hora_utc") if len(linhas) > 1 else None)


if __name__ == "__main__":
    main()
