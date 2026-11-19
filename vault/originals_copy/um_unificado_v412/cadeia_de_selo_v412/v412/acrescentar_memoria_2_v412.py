# -*- coding: utf-8 -*-
"""acrescentar_memoria_2_v412.py -- (gerencia c1, 19/11/2026) o apontador do topico licoes-custodia-v412-g1-19nov no MEMORY_2.md (o MEMORY.md esta'
no limite e pinado: nao recebe linha). Backup de BYTES antes, temporario, conferencia de que cresceu; recusa se o apontador ja' existe."""
import sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
M = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory")
p = M / "MEMORY_2.md"; t = M / "licoes-custodia-v412-g1-19nov.md"
assert t.is_file(), "o topico nao existe"
MARCA = "<!-- indice_19nov_v412_selada -->"
LINHA = ("- **[v412 SELADA E O QUE A G1 EXIGE (19/11)](licoes-custodia-v412-g1-19nov.md)** — selo `60f00e9818f71b73`, `um.py` `3e741dcaa58ef2b8`; "
         "handoff no molde da G1; três emendas AO LADO mantidas pela custódia; **o B(n) não rodou: decisão do autor** (a dispensa da guarda foi recusada)")
a = p.read_bytes(); assert MARCA.encode() not in a, "o apontador ja' existe"
bk = p.with_name(p.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")); bk.write_bytes(a); assert bk.read_bytes() == a
fim = b"\r\n" if a.count(b"\r\n") > a.count(b"\n") / 2 else b"\n"
novo = a.rstrip(b"\r\n") + fim + fim + ("%s\n%s" % (MARCA, LINHA)).replace("\n", fim.decode()).encode("utf-8") + fim
tmp = p.with_name(p.name + ".tmp_c1"); tmp.write_bytes(novo); assert tmp.stat().st_size == len(novo); tmp.replace(p); assert p.stat().st_size > len(a)
print("MEMORY_2.md: apontador acrescentado | backup", bk.name, "|", len(a), "->", p.stat().st_size, "B")
