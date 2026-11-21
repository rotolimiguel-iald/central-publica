# -*- coding: utf-8 -*-
"""conferir_mds_v413.py -- gerencia c1, 21/11/2026: confere que os .md (e os textos declarados) que o um.py v413 e o pos-rito regeneram
APONTAM a v413 e INCORPORAM as derivacoes novas (ordem do operador da noite de 20/11, bytes sha16 792f126a797e24eb: «regenerar corretamente os
md's todos apontando a v413 e incorporando as novas derivações corretamente»). So' le; nada grava fora do recibo. Tudo lido (ESPERADOS, selo,
delta); nenhum numero digitado.
Por arquivo do Nos:
  um_absoluto_forma_canonica.md  carimbo «Versão v413» com o sha16 do um.py; cada registro novo da v413 na lista de vereditos, com all_verified=True;
                                 a linha final «versao v413»; reescrito depois do inicio do rito.
  um_absoluto_manifest.md        carimbo «Versão v413» com o sha16; os 21 modulos novos citados; reescrito depois do inicio do rito.
  um_absoluto_pt.txt / _en.txt   o titulo da secao nova (PT «O que fica claro na v413»; EN do delta) e os 21 modulos citados.
  A_PROVA_DA_QG_TGL_arvore.md    (depois do passo 3 do pos-rito) o titulo «(v413)»; sem ele, PENDENTE (nao falha antes do passo 3).
Uso: conferir_mds_v413.py [--exigir-arvore]   (saida 0 so' com tudo OK; recibo CONFERENCIA_MDS_v413.json na pasta da cadeia)"""
import hashlib, json, os, re, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent.parent
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
ESP = json.loads((V / "ESPERADOS_v413.json").read_text(encoding="utf-8"))
SELO = json.loads((NOS / "um_absoluto_selo.json").read_text(encoding="utf-8"))
U16 = ESP["candidato_sha16"]
REGS = sorted(ESP["registros_v413"])
NOMES = sorted(os.path.splitext(os.path.basename(x))[0] for x in ESP["bundle_sha256"])
dt = (V / "delta_v413.py").read_text(encoding="utf-8")
m = re.search(r'TITULO_SECAO_V413 = \{"pt": [^,]+, "en": "([^"]+)"\}', dt)
TIT = {"pt": "O que fica claro na v413", "en": m.group(1) if m else None}
EXIGIR_ARV = "--exigir-arvore" in sys.argv
APL = sorted(V.glob("APLICADO_AO_CANONICO_*.json"))
t0 = time.mktime(time.strptime(json.loads(APL[-1].read_text(encoding="utf-8"))["ts"], "%Y%m%d_%H%M%S")) if APL else 0
res, ok = {}, True


def ler(n):
    p = NOS / n
    return (p.read_text(encoding="utf-8", errors="replace"), p.stat().st_mtime, hashlib.sha256(p.read_bytes()).hexdigest()[:16]) if p.is_file() else (None, 0, None)


def checa(arq, nome, cond, det=""):
    global ok
    res.setdefault(arq, []).append({"checagem": nome, "ok": bool(cond), "detalhe": det})
    if not cond:
        ok = False


assert SELO.get("um_version") == "v413" and SELO["sha256"]["um.py"][:16] == U16, "o selo do Nos nao e' a v413 com o um.py pinado: confiro so' depois do rito"
carimbo = "> **Versão v413**"
for arq in ("um_absoluto_forma_canonica.md", "um_absoluto_manifest.md"):
    t, mt, h = ler(arq)
    checa(arq, "existe", t is not None)
    if t is None:
        continue
    l3 = "\n".join(t.split("\n")[:4])
    checa(arq, "carimbo da v413 no topo", carimbo in l3 and U16 in l3, l3[:200])
    checa(arq, "sem carimbo de outra versao no topo", not re.search(r"\*\*Versão v(?!413)\d+\*\*", l3))
    checa(arq, "reescrito depois da instalacao", mt > t0, time.strftime("%d/%m %H:%M", time.localtime(mt)))
    res[arq].append({"sha16": h})
t, mt, h = ler("um_absoluto_forma_canonica.md")
if t:
    for r in REGS:
        linha = [x for x in t.split("\n") if x.startswith("- `%s`:" % r)]
        checa("um_absoluto_forma_canonica.md", "registro %s na lista de vereditos, verificado" % r,
              len(linha) == 1 and ESP["registros_v413"][r] in linha[0] and "[all_verified=True]" in linha[0], (linha[0][:160] if linha else "AUSENTE"))
    checa("um_absoluto_forma_canonica.md", "linha final com a versao v413", "versao v413; rodada %s" % SELO["timestamp"] in t)
t, mt, h = ler("um_absoluto_manifest.md")
if t:
    falt = [n for n in NOMES if n not in t]
    checa("um_absoluto_manifest.md", "os %d modulos novos citados" % len(NOMES), not falt, "faltam: %s" % falt[:8])
for arq, lang in (("um_absoluto_pt.txt", "pt"), ("um_absoluto_en.txt", "en")):
    t, mt, h = ler(arq)
    checa(arq, "existe", t is not None)
    if t is None:
        continue
    checa(arq, "titulo da secao nova (%s)" % TIT[lang], bool(TIT[lang]) and TIT[lang] in t)
    falt = [n for n in NOMES if n not in t]
    checa(arq, "os %d modulos novos citados" % len(NOMES), not falt, "faltam: %s" % falt[:8])
    checa(arq, "reescrito depois da instalacao", mt > t0, time.strftime("%d/%m %H:%M", time.localtime(mt)))
    res[arq].append({"sha16": h})
t, mt, h = ler("A_PROVA_DA_QG_TGL_arvore.md")
tit = t.split("\n")[0] if t else ""
if "(v413)" in tit:
    checa("A_PROVA_DA_QG_TGL_arvore.md", "titulo (v413)", True, tit[:120])
    res["A_PROVA_DA_QG_TGL_arvore.md"].append({"sha16": h})
elif EXIGIR_ARV:
    checa("A_PROVA_DA_QG_TGL_arvore.md", "titulo (v413)", False, tit[:120])
else:
    res["A_PROVA_DA_QG_TGL_arvore.md"] = [{"checagem": "titulo (v413)", "ok": None, "detalhe": "PENDENTE: o passo 3 do pos-rito regera a arvore (%s)" % tit[:80]}]
rec = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "por": "pos_rito\\conferir_mds_v413.py", "ok": ok, "um_py_sha16": U16, "selo_ts": SELO["timestamp"],
       "registros_v413": REGS, "n_modulos_novos": len(NOMES), "titulos": TIT, "arquivos": res}
b = json.dumps(rec, ensure_ascii=False, indent=1).encode("utf-8")
out = V / "CONFERENCIA_MDS_v413.json"
tmp = out.with_name(out.name + ".tmp")
tmp.write_bytes(b)
assert tmp.read_bytes() == b
tmp.replace(out)
for arq, cs in res.items():
    for c in cs:
        if "checagem" in c:
            print("%-6s %-32s %s %s" % ({True: "OK", False: "FALHA", None: "PEND"}[c["ok"]], arq[:32], c["checagem"], ("| " + c["detalhe"][:90]) if c.get("detalhe") and c["ok"] is not True else ""))
print("CONFERENCIA_MDS_v413.json | %s" % ("TUDO OK" if ok else "HA FALHA"))
sys.exit(0 if ok else 1)
