# -*- coding: utf-8 -*-
"""gerencia c1, 21/11/2026: os scripts da Etapa 3 foram escritos com o contrato R1 e a pagina R0; o vigente e' o contrato R2
(94982ebbc29d81b8) com a pagina R1 (3dc953e37c6739f4). Troca, por texto exato e com contagem, nos quatro scripts que leem ou
citam o contrato e a pagina. Backup de bytes ao lado; escrita por temporario. As palavras de veredito sao as mesmas no R1 e no
R2 (conferido aqui: o bloco da secao 2 com as palavras e' igual nos dois)."""
import hashlib, re, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
TS = time.strftime("%Y%m%d_%H%M%S")
R1, R2 = (V / "CONTRATO_v413_R1.md").read_text(encoding="utf-8"), (V / "CONTRATO_v413_R2.md").read_text(encoding="utf-8")
pal = lambda t: re.findall(r"`(TGL_[A-Z0-9_]+)`", t)  # noqa: E731
assert pal(R1) == pal(R2) and len(pal(R2)) >= 5, "as palavras de veredito mudaram entre R1 e R2"
TROCAS = {
    "montar_handoff_e_linhagem_v413.py": [("O_QUE_FICA_CLARO_v413_R0.md", "O_QUE_FICA_CLARO_v413_R1.md"),
                                          ("CONTRATO_v413_R1.md", "CONTRATO_v413_R2.md"),
                                          ("p\\u00fablica R0", "p\\u00fablica R1"), ("contrato R1", "contrato R2")],
    "esperados_v413_foco.py": [("CONTRATO_v413_R1.md", "CONTRATO_v413_R2.md"), ("contrato_REV1", "contrato_REV2"),
                               ("contrato R1", "contrato R2")],
    "conferir_pos_rito_v413_foco.py": [("contrato R1", "contrato R2"), ("CONTRATO_v413_R1.md", "CONTRATO_v413_R2.md")],
    "pos_rito/adaptar_arvore_da_prova_v413.py": [("CONTRATO_v413_R1.md", "CONTRATO_v413_R2.md")],
}
for nome, trocas in TROCAS.items():
    f = V / nome
    b = f.read_bytes()
    crlf = b"\r\n" in b
    t = b.decode("utf-8").replace("\r\n", "\n")
    cont = {}
    for a, z in trocas:
        cont[a] = t.count(a)
        t = t.replace(a, z)
    novo = (t.replace("\n", "\r\n") if crlf else t).encode("utf-8")
    if novo == b:
        print("%-42s sem mudanca" % nome)
        continue
    bk = f.with_name(f.name + ".bak_" + TS + "_r2")
    bk.write_bytes(b)
    tmp = f.with_name(f.name + ".tmp")
    tmp.write_bytes(novo)
    assert tmp.read_bytes() == novo
    tmp.replace(f)
    print("%-42s %s | sha16 %s" % (nome, ", ".join("%s x%d" % (k[:24], v) for k, v in cont.items()),
                                   hashlib.sha256(novo).hexdigest()[:16]))
