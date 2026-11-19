# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: so' leitura. Confere o material da ordem 033 ao Codex antes de escreve-la:
(1) para os 4 modulos emendados pelo parecer da 032 e os 2 do Kimi que entraram por ultimo, a copia congelada em insumos\\pedras_r10 e'
igual, por bytes, 'a copia de trabalho de pedras_novas; (2) o codigo (fora de comentarios e docstrings) e' identico ao da fonte do autor
(pedras_novas\\origem); (3) para os 4 emendados, a copia que o revisor leu na 032 (pedras_novas\\REV_032\\depois) difere da congelada so'
em comentario; (4) a pagina R18 contem a R17 menos as linhas acrescentadas. Imprime os sha16."""
import hashlib, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; N = V / "pedras_novas"; R10 = V / "insumos" / "pedras_r10"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]


def sem_comentarios(t):
    out, i, n, prof = [], 0, len(t), 0
    while i < n:
        if t.startswith("/-", i):
            prof += 1; i += 2; continue
        if prof and t.startswith("-/", i):
            prof -= 1; i += 2; continue
        if prof:
            i += 1; continue
        if t.startswith("--", i):
            while i < n and t[i] != "\n":
                i += 1
            continue
        out.append(t[i]); i += 1
    return "\n".join(l.rstrip() for l in "".join(out).split("\n") if l.strip())


EMEND_032 = ["OResumoEPsiBit", "OPsiBitDaFormula", "AFronteiraEOUnicoPortao", "ACurvaEAEstado"]
KIMI_ULTIMAS = ["AClausulaExemplificativa", "AFitaEOIndice"]
n = 0
for m in EMEND_032 + KIMI_ULTIMAS:
    r10, trab, orig = R10 / (m + ".lean"), N / (m + ".lean"), N / "origem" / (m + ".lean")
    assert r10.read_bytes() == trab.read_bytes(), "congelada difere da de trabalho: " + m
    assert sem_comentarios(r10.read_text(encoding="utf-8")) == sem_comentarios(orig.read_text(encoding="utf-8")), "codigo difere do autor: " + m
    linha = "%-26s congelada %s | autor %s | codigo identico" % (m, sha(r10), sha(orig))
    if m in EMEND_032:
        d = N / "REV_032" / "depois" / (m + ".lean")
        assert d.read_bytes() != r10.read_bytes(), "nada mudou desde a 032: " + m
        assert sem_comentarios(d.read_text(encoding="utf-8")) == sem_comentarios(r10.read_text(encoding="utf-8"))
        linha += " | lida na 032 %s (difere so' em comentario)" % sha(d)
    print(linha); n += 1
r16 = V / "o_que_fica_claro_REV16" / "O_QUE_FICA_CLARO_v412_R16_PROPOSTA_frase_A.md"
r17 = V / "o_que_fica_claro_REV17" / "O_QUE_FICA_CLARO_v412_R17.md"
r18 = V / "o_que_fica_claro_REV18" / "O_QUE_FICA_CLARO_v412_R18.md"
l17 = set(r17.read_text(encoding="utf-8").split("\n")); l18 = r18.read_text(encoding="utf-8").split("\n")
novas = [l for l in l18 if l not in l17]
print("pagina: R16A %s | R17 %s | R18 %s | linhas da R18 que nao estao na R17: %d" % (sha(r16), sha(r17), sha(r18), len(novas)))
for l in novas:
    print("   +", l[:110])
assert n == 6 and len(novas) >= 2
print("contrato R5 %s | manifesto R10 %s" % (sha(V / "CONTRATO_v412_R5.md"), sha(V / "insumos" / "MANIFESTO_PEDRAS_v412_R10.json")))
print("CONFERE")
