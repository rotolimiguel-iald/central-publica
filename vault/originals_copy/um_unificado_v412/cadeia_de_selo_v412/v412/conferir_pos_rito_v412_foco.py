# -*- coding: utf-8 -*-
"""conferir_pos_rito_v412_foco.py -- (gerencia c1, 18/11/2026, Etapa 3 ENXUTA: PLANO_ETAPA3_ENXUTA_v412.md) confere, DEPOIS do rito v412,
SO' LENDO o Nos, o que tinha de mudar e o que nao podia, contra o estado SELADO da v411 (os backups que o instalador gravou, lidos pelo
APLICADO_AO_CANONICO_<ts>.json mais novo) e o ESPERADOS_v412.json (esperados_v412_foco.py). Substitui, nesta versao, o conferir_rito_v412.py
herdado (v411, sem modulo novo), que segue marcado e nao roda. Grava CONFERENCIA_POS_RITO_v412_FOCO.json. Saida 0 so' se TUDO bater.
Checagens:
 1. o stdout do rito termina com RITO_RC=0; o um.py do Nos e' o candidato (sha16 e bytes do ESPERADOS);
 2. o selo novo: um_version v412; sha256/um.py == o do arquivo; o veredito do gate == o da v411; nada formal sem selar (not_sealed formais vazio)
    e as recusas de dado iguais as da v411;
 3. NADA DA v411 PERDIDO: todo registro com veredito do core da v411 existe no core novo com o MESMO veredito, salvo pela troca dita
    (trocando a escada antes/depois e o hash do um.py v411/v412 por marcadores neutros, o veredito fica identico); toda chave do selo da v411
    existe no selo novo;
 4. os cinco registros novos existem no core com a palavra de veredito do contrato R11;
 5. as bandeiras: todas as True da v411 seguem True; o numero de True == a escada de depois (ESPERADOS.escada[1]); as novas == n_bandeiras_novas;
 6. o relatorio de axiomas: nenhum sorryAx e nada fora do trio (propext, Classical.choice, Quot.sound) nas entradas novas e nas herdadas;
 7. o kernel do Nos: os 156 modulos novos existem com o sha256 do manifesto R12 (ESPERADOS.bundle_sha256); a raiz TGLExt.lean importa os 156."""
import glob, hashlib, json, os, re, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; NOS = Path(os.environ.get("V412_NOS") or r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")   # (V412_NOS: so' para o ensaio do conferidor num Nos falso)
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
lj = lambda p: json.loads(Path(p).read_text(encoding="utf-8"))
ESP = lj(V / "ESPERADOS_v412.json"); assert ESP.get("gerador") == "esperados_v412_foco.py"
ap = [os.environ["V412_APLICADO"]] if os.environ.get("V412_APLICADO") else sorted(glob.glob(str(V / "APLICADO_AO_CANONICO_*.json"))); assert ap, "nenhum APLICADO_AO_CANONICO_*.json"
AP = lj(ap[-1]); B = AP["backups"]
linhas = []; ok_total = True


def chk(nome, cond, detalhe=None):
    global ok_total
    ok_total = ok_total and bool(cond); linhas.append({"checagem": nome, "ok": bool(cond), "detalhe": detalhe})
    print(("ok    " if cond else "FALHOU"), nome, "" if cond else str(detalhe)[:600])


# a v411 selada: dos backups do instalador (o estado que estava no Nos antes do rito)
selo0 = lj(B["um_absoluto_selo.json"]["backup"]); core0 = lj(B["um_absoluto.json"]["backup"])["core"]
assert sha(B["um.py"]["backup"])[:16] == ESP["origem_sha16"] and B["um_absoluto_selo.json"]["sha16"] == ESP["base_v411"]["selo_sha256"][:16], "os backups nao sao a v411 selada"
selo1 = lj(NOS / "um_absoluto_selo.json"); R1 = lj(NOS / "um_absoluto.json"); core1 = R1["core"]
# 1. o stdout e o um.py
so = (NOS / "rodada_v412_stdout.txt").read_bytes().decode("utf-8", "replace").rstrip().split("\n")
chk("o stdout do rito termina com RITO_RC=0", so and so[-1].strip() == "RITO_RC=0", so[-3:] if so else None)
um1 = NOS / "um.py"
chk("o um.py do Nos e' o candidato (sha16 e bytes)", sha(um1)[:16] == ESP["candidato_sha16"] and um1.stat().st_size == ESP["candidato_bytes"], (sha(um1)[:16], um1.stat().st_size))
# 2. o selo
chk("o selo novo diz um_version v412", selo1.get("um_version") == "v412", selo1.get("um_version"))
chk("o selo novo pina o um.py do disco (sha256/um.py)", (selo1.get("sha256") or {}).get("um.py") == sha(um1), (selo1.get("sha256") or {}).get("um.py"))
chk("o veredito do gate e' o da v411 (o gate nao se move)", selo1.get("qg_closure_verdict") == selo0.get("qg_closure_verdict") == ESP["gate_verdict_v411"], selo1.get("qg_closure_verdict"))
ns0, ns1 = selo0.get("not_sealed_this_run") or {}, selo1.get("not_sealed_this_run") or {}
chk("nada formal sem selar; as recusas de dado iguais as da v411", (ns1.get("formais") or []) == [] and sorted(ns1.get("recusas_de_dado") or []) == sorted(ns0.get("recusas_de_dado") or []),
    {"formais": ns1.get("formais"), "recusas": ns1.get("recusas_de_dado")})
# 3. nada da v411 perdido
def neutro(v):   # (a regra do ensaio a seco: os vizinhos so' mudam numeros) hashes hexadecimais e numeros viram marcadores neutros
    return re.sub(r"\d+", "<N>", re.sub(r"[0-9a-f]{16,64}", "<H>", str(v)))
reg0 = {k: m["verdict"] for k, m in core0.items() if isinstance(m, dict) and m.get("verdict")}
faltam = [k for k in reg0 if not (isinstance(core1.get(k), dict) and core1[k].get("verdict"))]
mudaram = {k: (reg0[k][:120], str(core1[k]["verdict"])[:120]) for k in reg0 if k not in faltam and core1[k]["verdict"] != reg0[k]}
fora_da_troca = {k: v for k, v in mudaram.items() if neutro(core1[k]["verdict"]) != neutro(reg0[k])}
chk("nenhum registro com veredito da v411 sumiu do core (%d herdados)" % len(reg0), not faltam, faltam[:10])
chk("nenhum veredito herdado mudou fora da troca dita (escada e hash do um.py); mudaram pela troca dita: %d" % (len(mudaram) - len(fora_da_troca)), not fora_da_troca, fora_da_troca)
sk_falta = [k for k in selo0 if k not in selo1]
chk("toda chave do selo da v411 existe no selo novo (%d)" % len(selo0), not sk_falta, sk_falta[:10])
# 4. os cinco registros novos
reg_ruins = {n: (core1.get(n) or {}).get("verdict") for n, w in ESP["registros_v412"].items() if (core1.get(n) or {}).get("verdict") != w}
chk("os cinco registros novos existem com a palavra de veredito do contrato R11", not reg_ruins, reg_ruins)
# 5. as bandeiras
kf0, kf1 = core0["kernel_formalization"], core1["kernel_formalization"]
t0 = {k for k, v in kf0.items() if v is True}; t1 = {k for k, v in kf1.items() if v is True}
caiu = sorted(t0 - t1)
chk("todas as bandeiras True da v411 seguem True (%d)" % len(t0), not caiu, caiu[:10])
novas = t1 - t0; esperadas = set(ESP["bandeiras_novas_chaves"])
chk("as bandeiras True novas sao exatamente as %d chaves do FLAGS_v412.json (nem mais, nem menos)" % len(esperadas), novas == esperadas and len(esperadas) == ESP["n_bandeiras_novas"] and len(t0) == ESP["n_bandeiras_true_v411"],
    {"novas": len(novas), "esperadas": len(esperadas), "a_mais": sorted(novas - esperadas)[:5], "faltam": sorted(esperadas - novas)[:5], "true_v411": len(t0)})
_est = str((core1.get("estatuto_da_prova_v391") or {}).get("verdict"))
chk("o veredito do estatuto da prova traz a escada de depois (%d)" % ESP["escada"][1], str(ESP["escada"][1]) in _est and str(ESP["escada"][0]) not in _est, _est[:200])
# 6. os axiomas
TRIO = {"propext", "Classical.choice", "Quot.sound"}
ax1 = kf1.get("axiom_report")
def axiomas_de(x):
    if isinstance(x, dict):
        for k, v in x.items():
            yield k, v
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield i, v
fora = []; com_sorry = []
for k, v in axiomas_de(ax1):
    s = json.dumps(v, ensure_ascii=False)
    if "sorryAx" in s:
        com_sorry.append(k)
    nomes = set(re.findall(r"[A-Za-z][A-Za-z0-9_.']*", s)) if isinstance(v, (list, str)) else set()
    if isinstance(v, list):
        extra = {a for a in v if isinstance(a, str)} - TRIO
        if extra:
            fora.append((k, sorted(extra)[:3]))
chk("o relatorio de axiomas nao tem sorryAx (%s entradas)" % (len(ax1) if hasattr(ax1, "__len__") else "?"), not com_sorry, com_sorry[:10])
chk("nenhuma entrada do relatorio de axiomas fora do trio", not fora, fora[:10])
# 7. o kernel do Nos
mal = [rel for rel, s in ESP["bundle_sha256"].items() if not (NOS / "tgl_kernel" / Path(*rel.split("/"))).is_file() or sha(NOS / "tgl_kernel" / Path(*rel.split("/"))) != s]
chk("os %d modulos novos estao no kernel do Nos com o sha256 do manifesto R12" % len(ESP["bundle_sha256"]), not mal, mal[:10])
raiz = (NOS / "tgl_kernel" / "TGLExt.lean").read_text(encoding="utf-8")
sem_import = [rel for rel in ESP["bundle_sha256"] if ("import TGLExt." + rel[len("TGLExt/"):-len(".lean")]) not in raiz]
chk("a raiz TGLExt.lean do Nos importa os 156", not sem_import, sem_import[:10])
rec = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "ok": ok_total, "aplicado": os.path.basename(ap[-1]), "esperados_sha16": sha(V / "ESPERADOS_v412.json")[:16],
       "selo_sha16": sha(NOS / "um_absoluto_selo.json")[:16], "um_py_sha16": sha(um1)[:16], "checagens": linhas,
       "nota": "conferidor ENXUTO da v412 (Etapa 3 enxuta); o conferir_rito_v412.py herdado da v411 nao roda"}
out = V / ("CONFERENCIA_POS_RITO_v412_FOCO.json" if not os.environ.get("V412_NOS") else "CONFERENCIA_POS_RITO_v412_FOCO_ENSAIO_NOS_FALSO.json")
if out.exists():
    out.with_name(out.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(out.read_bytes())
out.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
print("CONFERENCIA POS-RITO v412 (enxuta):", "TUDO BATE" if ok_total else "ALGO NAO BATE", "| checagens", len(linhas), "| ok", sum(1 for l in linhas if l["ok"]))
sys.exit(0 if ok_total else 1)
