# [DERIVADO v412 r7, claude-construtor-v412 (contrato R11)] copia de e5_12_titulos_dos_cabecalhos_v412.py; trocas de texto exato com contagem registrada em DERIVACAO_R7_PIPELINE_v412.json (derivador: e7_04_derivar_texto_v412.py). O original fica intacto.
"""R5: titulo (linha '# ...') ou primeira frase do cabecalho de cada modulo da DECIMA SEGUNDA lista, a presenca de secao 'O que NAO se afirma', e as secoes do cabecalho cujo titulo diz que o arquivo TIPA uma letra, lei, leitura ou definicao.
Grava TITULOS_DOS_CABECALHOS_v412.json (com backup de bytes do anterior). So' leitura das fontes congeladas."""
import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
from e7_lib_v412 import D, salvar_json, sha16_arq, ler_json, PEDRAS, MANIFESTO
MAN = ler_json(MANIFESTO)
out = {}; tipa = {}
for x in MAN["modulos"]:
    p = PEDRAS / (x["modulo"] + ".lean")
    t = p.read_bytes().decode("utf-8")
    m = re.search(r"/-!(.*?)-/", t, re.S)
    h = m.group(1) if m else ""
    mt = re.search(r"(?m)^# (.+)$", h)
    if mt:
        tit = mt.group(1).strip()
    else:
        s = re.sub(r"\s+", " ", h).strip()
        tit = (s.split(". ")[0] + ".") if s else None
    nao = re.search(r"(?m)^#{2,3} (O que .*N[ÃA]O .*|.*N[ÃA]O se afirma.*)$", h)
    secs_tipa = [s_.strip() for s_ in re.findall(r"(?m)^## (.*\btipa\b.*)$", h)]
    out[x["modulo"]] = {"titulo": tit, "tem_secao_nao_afirma": bool(nao), "secao_nao": nao.group(1) if nao else None, "tem_cabecalho": bool(m), "secoes_tipa": secs_tipa, "frente": x["frente"]}
    if secs_tipa:
        tipa[x["modulo"]] = secs_tipa
sem = [k for k, v in out.items() if not v["tem_cabecalho"]]
print("modulos:", len(out), "| sem cabecalho /-! -/:", len(sem), sem[:30])
print("modulos com secao que tipa:", len(tipa))
for k, v in tipa.items():
    print("   %-28s %s | %s" % (k, out[k]["frente"], v))
for k in ("OPassoEOFim", "OPsibitEACompressao"):
    t = (PEDRAS / (k + ".lean")).read_bytes().decode("utf-8")
    print("\n=====", k); print(re.search(r"/-!(.*?)-/", t, re.S).group(1)[:6000])
salvar_json(D / "TITULOS_DOS_CABECALHOS_v412.json", {"sha16_manifesto": sha16_arq(MANIFESTO), "lista": "duodecima (insumos/pedras_r12)", "modulos": out})
