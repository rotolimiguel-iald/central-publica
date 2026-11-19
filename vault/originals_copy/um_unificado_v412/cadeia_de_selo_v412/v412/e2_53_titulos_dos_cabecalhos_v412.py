"""titulo (linha '# ...') ou primeira frase do cabecalho de cada modulo da quinta lista (para o 'diz' dos registros), e a presenca de '## O que NAO se afirma'."""
import json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
from e2_lib_v412 import D, salvar_json, sha16_arq, ler_json
F = D / "insumos" / "pedras_r7"
MAN = ler_json(D / "insumos" / "MANIFESTO_PEDRAS_v412_R7.json")
out = {}
for p in sorted(F.glob("*.lean")):
    t = p.read_bytes().decode("utf-8")
    m = re.search(r"/-!(.*?)-/", t, re.S)
    h = m.group(1) if m else ""
    tit = None
    mt = re.search(r"(?m)^# (.+)$", h)
    if mt:
        tit = mt.group(1).strip()
    else:
        s = re.sub(r"\s+", " ", h).strip()
        tit = (s.split(". ")[0] + ".") if s else None
    nao = re.search(r"(?m)^#{2,3} (O que .*N[ÃA]O .*|.*N[ÃA]O se afirma.*)$", h)
    out[p.stem] = {"titulo": tit, "tem_secao_nao_afirma": bool(nao), "secao_nao": nao.group(1) if nao else None, "tem_cabecalho": bool(m)}
for k, v in out.items():
    print("%-30s | %s | nao=%s | %s" % (k, "cab" if v["tem_cabecalho"] else "SEM", v["secao_nao"], (v["titulo"] or "")[:110]))
salvar_json(D / "TITULOS_DOS_CABECALHOS_v412.json", {"sha16_manifesto": sha16_arq(D / "insumos" / "MANIFESTO_PEDRAS_v412_R7.json"), "modulos": out})
