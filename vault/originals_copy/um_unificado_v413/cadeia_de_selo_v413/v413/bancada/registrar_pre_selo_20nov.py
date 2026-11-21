# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: registra o pre-selo do salto v411->v413 RODADO (com o Nos ainda na v412, antes da instalacao):
(1) Mapa: RESULTADO na rota bancada.bn_v413.salto_v411_v413_20nov; (2) ACOM transition; (3) marca o passo 4 do plano.
Numeros lidos da saida e dos recibos."""
import hashlib, json, re, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"
B = Path(__file__).resolve().parent
V = B.parent
OUT = V / "bateria_pre_selo" / "bn_pre_selo_out_v413.txt"
PINO = V / "PINO_RECIBO_PRE_SELO_v413.json"
PRE = V / "PRECONDICOES_BN_v413.json"
PINOS = V / "PINOS_BN_v413.json"
REV = B / "REVISAO_INDEPENDENTE_BN_v413.md"
PR = B / "PRONTO_BN_v413.json"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def s16(p):
    return sha(p)[:16]


for p in (OUT, PINO, PRE, PINOS, REV, PR):
    assert p.exists(), p
o = OUT.read_text(encoding="utf-8", errors="replace")
assert ("REPINADA_B21__SALTO_v411_v412__ENSAIO__NADA_GRAVADO_NA_BANCADA" in o and "producao_intacta=True" in o
        and "UTILIZAVEL_DO_PINO=True" in o and "RC_LIMPAR=0" in o and "NENHUMA FALHA" in o)
m = re.search(r'"condicoes_ok": "(\d+/\d+)"', o)
cond = m.group(1) if m else "?"
print("(0) pre-selo: veredito exato do salto | conferencia pelo esboco %s | pino %s | PINOS %s" % (cond, s16(PINO), s16(PINOS)))
res = {"tipo": "RESULTADO", "rota_id": "bancada.bn_v413.salto_v411_v413_20nov", "dominio": "BANCADA",
       "titulo": "o pre-selo do salto v411->v413 RODADO com o Nos ainda na v412, antes da instalacao: REPINADA_B21__SALTO_v411_v412__ENSAIO",
       "resultado": ("Revisao independente unica do molde: APROVADO_COM_RESSALVAS, sem ALTO (%s, sha16 %s); os 13 BAIXOS e M1/M3/M4 "
                     "aplicados pelo construtor (95/95 hermeticos; PRONTO %s). Pre-selo real (rodar_bn_pre_selo_v413.sh): veredito "
                     "REPINADA_B21__SALTO_v411_v412__ENSAIO__NADA_GRAVADO_NA_BANCADA; conferencia pelo esboco %s; bateria da v412 "
                     "BATERIA_PASSA; producao_intacta True (a Bancada so' foi lida); pino do recibo %s utilizavel; PINOS_BN_v413 %s "
                     "com 7 pendentes que dependem do candidato (o diff_e_pinos com --delta antes do APLICAR); p00: 23 ok, 0 falha.") % (
           REV.name, s16(REV), s16(PR), cond, s16(PINO), s16(PINOS)),
       "veredito": "PRE_SELO_DO_SALTO_v411_v413_RODADO_ANTES_DA_INSTALACAO__PRODUCAO_INTACTA__PINO_UTILIZAVEL__PENDENTES_DO_CANDIDATO",
       "estatuto": "REAL (saida da rodada e recibos)", "status": "EM_CURSO", "olhou_dados": False,
       "defeito": "um teste da bateria nao executado (14: 13 passa, 1 nao executado); os pinos do candidato pendentes ate' a Etapa 2",
       "nao_refazer": "nao refazer o pre-selo: o pino serve ao pos-selo da v413; a janela fecha quando a v413 for instalada",
       "proximo_passo": "depois do candidato: diff_e_pinos_bn_v413.py --delta <delta da v413> ate' pendentes vazio; depois do selo: ensaio a seco do pos-selo, e o pos-selo real (10 a 11, religamento em modo cpu)",
       "onde": str(V / "bateria_pre_selo"), "artefatos": [str(OUT), str(PINO), str(PRE), str(PINOS), str(REV), str(PR)],
       "refs": ["cadeia.preparacao_v413"], "nota": "ordem do operador da noite de 20/11 (bytes) cobre a execucao; partitura registrada antes de rodar"}
pj = B / "mapa_resultado_pre_selo_20nov.json"
pj.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([PY, "-B", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem",
                    "gerencia-c1 (claude-code, sessao 6da8f00d)"], capture_output=True, stdin=subprocess.DEVNULL, timeout=180)
out = r.stdout.decode("utf-8", "replace")
assert r.returncode == 0, out[:800] + r.stderr.decode("utf-8", "replace")[:800]
print("(1) Mapa %s" % out[out.find('"seq"'):][:14])
REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"


def acom(req):
    rr = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"],
                        input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True, timeout=180)
    return rr.returncode, rr.stdout


def acha(x, k):
    if isinstance(x, dict):
        for kk, vv in x.items():
            if kk == k:
                return vv
            y = acha(vv, k)
            if y is not None:
                return y
    elif isinstance(x, list):
        for vv in x:
            y = acha(vv, k)
            if y is not None:
                return y
    return None


rc, oo = acom({"operation": "project", "reference": REF})
rev = acha(json.loads(oo.decode("utf-8")), "revision")
req = {"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": rev,
       "event_id": "c1-20nov-d355-pre-selo-do-salto",
       "changes": {"records": [{"id": "c1-20nov-d355-pre-selo-do-salto", "kind": "fact", "statute": "REAL",
                                "text": ("Pre-selo do salto v411->v413 rodado com o Nos na v412, antes da instalacao: veredito "
                                         "REPINADA_B21__SALTO_v411_v412__ENSAIO__NADA_GRAVADO_NA_BANCADA, conferencia %s, "
                                         "producao intacta, pino utilizavel; 7 pinos pendentes do candidato.") % cond,
                                "sources": [{"kind": "artifact", "ref": "%s#sha256:%s" % (p, sha(p))} for p in (OUT, PINO, PINOS)]}]}}
rc, ot = acom(req)
t = ot.decode("utf-8", "replace")
print("(2) ACOM rev %s | ok %s | %s" % (rev, '"ok": true' in t, t[t.find('"revision"'):][:20]))
assert '"ok": true' in t
r = subprocess.run([PY, "-X", "utf8", str(V / "marcar_plano.py"), "4", "pre-selo rodado: REPINADA_B21__SALTO_v411_v412__ENSAIO, %s, producao intacta; pino %s" % (cond, s16(PINO))],
                   capture_output=True, stdin=subprocess.DEVNULL)
print("(3)", r.stdout.decode("utf-8", "replace").strip())
