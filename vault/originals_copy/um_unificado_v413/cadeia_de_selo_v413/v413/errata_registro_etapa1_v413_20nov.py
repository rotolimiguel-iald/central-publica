# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026, ERRATA AO LADO em nome proprio: o registro da Etapa 1 (Mapa seq 2211; ACOM d352) gravou
"None" na escada, nas bandeiras novas e nas declaracoes, porque o script leu chaves de topo e os numeros estao em blocos
aninhados do PRONTO_PARA_CANDIDATO_v413.json. Le os tres numeros por busca recursiva no recibo e registra (1) ERRATA no
Mapa corrigindo o 2211 e (2) um registro de correcao na ACOM. O registro original fica."""
import hashlib, json, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"
V = Path(__file__).resolve().parent
PRONTO = V / "PRONTO_PARA_CANDIDATO_v413.json"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def acha(o, chave):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == chave:
                return v
            x = acha(v, chave)
            if x is not None:
                return x
    elif isinstance(o, list):
        for v in o:
            x = acha(v, chave)
            if x is not None:
                return x
    return None


pr = json.loads(PRONTO.read_text(encoding="utf-8"))
esc = acha(pr, "escada_de_teoremas_e_bandeiras")
nb = acha(pr, "n_bandeiras_novas")
dec = acha(pr, "declaracoes_no_relatorio_de_axiomas")
assert esc and nb and dec, (esc, nb, dec)
print("(0) lidos do PRONTO (sha16 %s): escada %s | bandeiras novas %s | declaracoes %s" % (sha(PRONTO)[:16], esc, nb, dec))
err = {
    "tipo": "ERRATA", "rota_id": "cadeia.preparacao_v413", "corrige": 2211, "dominio": "CADEIA",
    "titulo": "ERRATA AO LADO (gerencia c1, em nome proprio): os tres numeros da Etapa 1 da v413 que o registro 2211 gravou como None",
    "resultado": ("O registro 2211 leu chaves de topo do PRONTO_PARA_CANDIDATO_v413.json e gravou None. Os numeros, lidos por "
                  "busca recursiva no mesmo recibo (sha16 %s): escada de teoremas e bandeiras %s; %s bandeiras novas; %s "
                  "declaracoes no relatorio de axiomas. O resto do 2211 vale como esta'.") % (sha(PRONTO)[:16], esc, nb, dec),
    "veredito": "ERRATA_DOS_TRES_NUMEROS_DA_ETAPA_1__LIDOS_DO_RECIBO_POR_BUSCA_RECURSIVA",
    "estatuto": "REAL (lidos do recibo por script)",
    "status": "EXAMINADA", "olhou_dados": False,
    "onde": str(V), "artefatos": [str(PRONTO)],
    "nota": "o registro original fica; correcao ao lado",
}
pj = V / "mapa_errata_etapa1_v413_20nov.json"
pj.write_text(json.dumps(err, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([PY, "-B", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem",
                    "gerencia-c1 (claude-code, sessao 6da8f00d)"], capture_output=True, stdin=subprocess.DEVNULL, timeout=180)
out = r.stdout.decode("utf-8", "replace")
assert r.returncode == 0, out[:800] + r.stderr.decode("utf-8", "replace")[:800]
print("(1) Mapa ERRATA %s" % out[out.find('"seq"'):][:14])

REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"


def acom(req):
    rr = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"],
                        input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True, timeout=180)
    return rr.returncode, rr.stdout


rc, o = acom({"operation": "project", "reference": REF})
proj = json.loads(o.decode("utf-8"))
assert proj.get("ok") is True
rev = acha(proj, "revision")
req = {"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"},
       "expected_revision": rev, "event_id": "c1-20nov-d353-errata-numeros-etapa1",
       "changes": {"records": [
           {"id": "c1-20nov-d353-errata-numeros-etapa1", "kind": "fact", "statute": "REAL",
            "text": ("CORRECAO AO LADO (gerencia c1, em nome proprio) do registro c1-20nov-d352-etapa1-v413-fechada: onde ele diz "
                     "\"escada None, None bandeiras novas; None declaracoes\", leia-se, lido do recibo por busca recursiva: escada "
                     "%s; %s bandeiras novas; %s declaracoes no relatorio de axiomas, todas no trio.") % (esc, nb, dec),
            "sources": [{"kind": "artifact", "ref": "%s#sha256:%s" % (PRONTO, sha(PRONTO))}]}]}}
rc, ot = acom(req)
(V / "acom_c1_20261120_d353_transition.receipt.json").write_bytes(ot)
t = ot.decode("utf-8", "replace")
print("(2) ACOM rev %s | rc %d | ok %s | %s" % (rev, rc, '"ok": true' in t, t[t.find('"revision"'):][:20]))
assert '"ok": true' in t
