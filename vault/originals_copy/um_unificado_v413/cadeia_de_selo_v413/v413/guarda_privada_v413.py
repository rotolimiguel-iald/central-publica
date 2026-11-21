# -*- coding: utf-8 -*-
"""guarda_privada_v413.py -- a GUARDA DE MATERIAL PRIVADO da custodia, ANTES do selo (Etapa 3 da v413, 20/11/2026; licao da v412: a guarda so' rodava na
custodia, depois do selo, e o conserto custou decisao do autor). Roda a MESMA contagem da G1 (custodia_g1.espelho_pares.carregar_marcadores_privados e
guarda_conta; a mesma regra do E03: um artefato novo nao pode ter MAIS ocorrencias que o seu par no espelho, o the_boundary com a v412 publicada; os
nomes isentos so' por decisao do operador da versao, decisoes\\TERMO_PRIVADO_ISENTO_v413.json, conferida como a G1 confere) sobre:
  --fase pre (antes do rito): o candidato (--candidato, ou o do ESPERADOS_v413.json), as fontes novas e a corrigida do sandbox k413c com a raiz, e
                              --core <arquivo> se houver um core de ensaio da Etapa 2;
  --fase pos (depois do rito, antes do handoff): o um.py, o core, o selo, o sidecar, os textos e os artigos, o manifesto do kernel, as capturas, o stdout
                              da v413, as fontes novas e a corrigida no Nos com a raiz, e os dois diffs da v413.
NUNCA imprime nem grava padrao nenhum: so' contagens; para um artefato barrado, os NUMEROS de ordem dos marcadores que cresceram (termo da casa n /
marcador privado n), como a custodia ja' os nomeia. Recibo GUARDA_PRIVADA_v413_<fase>.json nesta pasta. Saida 0 so' com zero termos novos; com termo
novo, saida 1: a decisao e' do autor (o termo sai antes do selo, ou a fala dele por bytes, com os nomes exatos, vai na entrega).
ENSAIO (--ensaio): o controle positivo (o um.py da v412 de base_v412 contra o do espelho: zero) e o negativo (o mesmo um.py contra um par vazio: tem de
barrar), sem saber nem gravar qual termo; recibo em etapa3\\ENSAIO_GUARDA_PRIVADA_v413.json."""
import hashlib, json, os, re, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
CEN = Path(r"C:\IALD\Central de Patentes"); sys.path.insert(0, str(CEN / "tools"))
from custodia_g1 import espelho_pares as EP  # noqa: E402
from custodia_g1.caminhos import Caminhos  # noqa: E402
V = Path(__file__).resolve().parent; C = Caminhos({}); ESPD = C.ESP; NOS = C.NOS; SB = Path(r"C:\t\k413c\final")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
arg = lambda k: (sys.argv[sys.argv.index(k) + 1] if k in sys.argv and sys.argv.index(k) + 1 < len(sys.argv) else None)


def isentos_v413():
    p = C.G1 / "decisoes" / "TERMO_PRIVADO_ISENTO_v413.json"
    if not p.is_file():
        return ()
    d = json.loads(p.read_text(encoding="utf-8")); vb = Path(str(d.get("ordem", "")))
    vb = vb if vb.is_absolute() else C.CEN / vb
    assert d.get("versao") == "v413" and vb.is_file() and sha(vb) == d.get("ordem_sha256"), "a decisao de nomes isentos da v413 nao confere (versao ou fala por sha256)"
    nomes = tuple(d.get("nomes_exatos") or ()); assert nomes and all(isinstance(s, str) and len(s) >= 12 for s in nomes), "nomes isentos vazios ou curtos"
    return nomes


def por_marcador(p, pats, isen):
    t = Path(p).read_bytes().decode("utf-8", "replace") if Path(p).is_file() else ""
    for s in isen:
        t = t.replace(s, " ")
    return [len(g.findall(t)) for g in pats]


def varrer(pares, priv, isen):
    pats = list(EP.GUARDA) + list(priv); n_casa = len(EP.GUARDA); out = []
    for nome, src, dst, tipo in pares:
        nn = EP.guarda_conta(src, priv, isen)
        nv = EP.guarda_conta(dst, priv, isen) if dst is not None and Path(dst).is_file() else 0
        assert nn is not None, ("leitura falhou (fail-closed)", nome)
        x = {"artefato": nome, "tipo": tipo, "fonte": str(src), "par_no_espelho": str(dst) if dst else None, "par_existe": bool(dst is not None and Path(dst).is_file()),
             "ocorrencias_novo": nn, "ocorrencias_espelho": nv or 0, "barrado": bool(nn and nn > (nv or 0))}
        if x["barrado"]:
            a, b = por_marcador(src, pats, isen), por_marcador(dst, pats, isen) if x["par_existe"] else [0] * len(pats)
            x["cresceram"] = [("termo da casa %d" % (i + 1)) if i < n_casa else ("marcador privado %d" % (i - n_casa + 1)) for i in range(len(pats)) if a[i] > b[i]]
        out.append(x)
    return out


def pares_pre():
    ESP = json.loads((V / "ESPERADOS_v413.json").read_text(encoding="utf-8")) if (V / "ESPERADOS_v413.json").is_file() else {}
    cand = arg("--candidato") or ((ESP.get("candidato") or {}).get("caminho"))
    assert cand and Path(cand).is_file(), "sem o candidato: passe --candidato <caminho> (ou rode o esperados_v413_foco.py antes)"
    KN = json.loads((V / "kernel_modulos_novos_v413.json").read_text(encoding="utf-8"))
    P = [("um.py (candidato)", Path(cand), ESPD / "um.py", "SELADO")]
    for rel in sorted(KN["novos"]) + sorted(KN["kernel_corrigido"]) + ["TGLExt.lean"]:
        P.append(("kernel " + rel, SB / Path(*rel.split("/")), ESPD / "Lean" / "tgl_kernel" / Path(*rel.split("/")), "KERNEL"))
    if arg("--core"):
        P.append(("um_absoluto.json (core de ensaio)", Path(arg("--core")), ESPD / "um_absoluto.json", "SELADO"))
    return P


def pares_pos():
    selo = json.loads((NOS / "um_absoluto_selo.json").read_text(encoding="utf-8")); assert selo.get("um_version") == "v413", "o Nos nao esta' na v413: a fase pos e' depois do rito"
    P = []
    for nome in selo["sha256"]:
        sub = EP.DESTINO_SELADOS.get(nome); P.append((nome, NOS / nome, (ESPD / sub / nome) if sub else (ESPD / nome), "SELADO"))
    for nome in ("um_absoluto_selo.json", "um_absoluto_selo_acom.json", "um_absoluto_pt.txt", "um_absoluto_en.txt"):
        P.append((nome, NOS / nome, ESPD / nome, "DECLARADO"))
    for p in sorted(NOS.glob("tgl_kernel_*capture*.txt")):
        if ".bak_" not in p.name:
            P.append((p.name, p, ESPD / "rodadas" / p.name, "CAPTURA"))
    P.append(("rodada_v413_stdout.txt", NOS / "rodada_v413_stdout.txt", ESPD / "rodadas" / "rodada_v413_stdout.txt", "STDOUT"))
    KN = json.loads((V / "kernel_modulos_novos_v413.json").read_text(encoding="utf-8"))
    for rel in sorted(KN["novos"]) + sorted(KN["kernel_corrigido"]) + ["TGLExt.lean"]:
        P.append(("kernel " + rel, NOS / "tgl_kernel" / Path(*rel.split("/")), ESPD / "Lean" / "tgl_kernel" / Path(*rel.split("/")), "KERNEL"))
    for n in ("DIFF_v412_v413.diff", "DIFF_KERNEL_v413.txt"):
        P.append((n, V / n, ESPD / "diferencas_v413" / n, "DIFF"))
    return P


priv = EP.carregar_marcadores_privados(); isen = isentos_v413()
if "--ensaio" in sys.argv:
    base = V / "base_v412" / "um.py"; assert sha(base) == sha(ESPD / "um.py"), "o um.py de base_v412 nao e' o do espelho (o controle positivo pede os mesmos bytes)"
    pos = varrer([("um.py da v412 (base) contra o espelho", base, ESPD / "um.py", "SELADO")], priv, isen)
    neg = varrer([("um.py da v412 (base) contra um par vazio", base, None, "SELADO")], priv, isen)
    ok = (not pos[0]["barrado"]) and neg[0]["barrado"] and neg[0]["ocorrencias_novo"] == pos[0]["ocorrencias_espelho"] > 0
    rec = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "ensaio": True, "ok": ok, "positivo": pos, "negativo": neg, "n_termos_da_casa": len(EP.GUARDA), "n_marcadores_privados": len(priv),
           "isentos_v413": len(isen), "nota": "so' contagens; nenhum padrao lido aqui foi impresso ou gravado"}
    (V / "etapa3" / "ENSAIO_GUARDA_PRIVADA_v413.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    print("ENSAIO DA GUARDA PRIVADA:", "COMO ESPERADO" if ok else "FORA DO ESPERADO", "| positivo: %d contra %d (barrado=%s) | negativo: %d contra par vazio (barrado=%s)" % (
        pos[0]["ocorrencias_novo"], pos[0]["ocorrencias_espelho"], pos[0]["barrado"], neg[0]["ocorrencias_novo"], neg[0]["barrado"]))
    sys.exit(0 if ok else 1)
fase = arg("--fase") or "pre"; assert fase in ("pre", "pos"), "--fase pre|pos"
res = varrer(pares_pre() if fase == "pre" else pares_pos(), priv, isen)
barr = [x for x in res if x["barrado"]]
rec = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "fase": fase, "espelho": str(ESPD), "n_artefatos": len(res), "termos_novos": len(barr), "excesso_total": sum(x["ocorrencias_novo"] - x["ocorrencias_espelho"] for x in barr),
       "barrados": barr, "artefatos": res, "n_termos_da_casa": len(EP.GUARDA), "n_marcadores_privados": len(priv), "isentos_v413": len(isen),
       "regra": "a do E03 da G1 (espelho._ap_e03): ocorrencias_novo > ocorrencias_espelho barra; so' contagens, nenhum padrao impresso ou gravado"}
out = V / ("GUARDA_PRIVADA_v413_%s.json" % fase)
if out.exists():
    out.with_name(out.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(out.read_bytes())
tmp = out.with_name(out.name + ".tmp"); tmp.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8"); tmp.replace(out)
print("GUARDA PRIVADA v413 (%s): %d artefatos | termos novos: %d%s | recibo %s" % (fase, len(res), len(barr), (" -> " + "; ".join("%s (%s)" % (x["artefato"], ", ".join(x["cresceram"])) for x in barr)) if barr else "", out.name))
sys.exit(0 if not barr else 1)
