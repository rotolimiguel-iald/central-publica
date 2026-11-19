# -*- coding: utf-8 -*-
"""conferir_ancoras_propostas_v412.py -- (claude-construtor-v412, 17/11/2026) so' LEITURA: confere as ancoras que a gerencia PROPOS em insumos\\ANCORAS_PROPOSTAS_v412.json (gravado as 05:25,
depois da ordem) contra o kernel do sandbox ja' medido: cada nome (namespace + nome) existe no axiom_report do Audit (kernel\\FLAGS_v412.json: proveniencia das publicas), vem do modulo dito, tem
bandeira proposta e esta' no trio. Nao escolhe ancora nenhuma (isso e' do contrato, Etapa 2). Grava kernel\\ANCORAS_PROPOSTAS_CONFERIDAS_v412.json.
uso: C:\\Python314\\python.exe -B -X utf8 conferir_ancoras_propostas_v412.py"""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
AP = os.path.join(HERE, "insumos", "ANCORAS_PROPOSTAS_v412.json")
a = json.load(open(AP, encoding="utf-8"))
f = json.load(open(os.path.join(HERE, "kernel", "FLAGS_v412.json"), encoding="utf-8"))
prov = f["proveniencia_publicas"]; chave = {x[1]: x[0] for x in f["flags"]}
man_sha = hashlib.sha256(open(os.path.join(HERE, "insumos", "MANIFESTO_PEDRAS_v412.json"), "rb").read()).hexdigest()
res = {}; faltam = []; n = 0
for reg, itens in a["registros"].items():
    for it in itens:
        ns = it.get("namespace"); mod = it.get("modulo")
        rel = "TGLExt/%s.lean" % mod
        for lista in ("com_estrela", "sem_estrela"):
            for nm in list(it.get(lista) or []):
                n += 1
                q = nm if (ns and nm.startswith(ns + ".")) else ((ns + "." + nm) if ns else nm)
                ok = q in prov and prov[q] == rel
                sufixo = None
                if not ok:   # o nome pode morar num namespace interno do modulo (ex.: LeitorDeUmaConfiguracao): procura-se pelo sufixo, so' entre as publicas do mesmo modulo
                    cands = [k for k, v in prov.items() if v == rel and k.endswith("." + nm)]
                    sufixo = cands if cands else None
                res.setdefault(reg, []).append({"lista": lista, "nome": q, "existe_no_audit_e_vem_do_modulo": ok, "bandeira_proposta": chave.get(q),
                                                "achado_por_sufixo_no_mesmo_modulo": sufixo, "bandeira_do_sufixo": [chave.get(c) for c in sufixo] if sufixo else None})
                if not ok and not (sufixo and len(sufixo) == 1):
                    faltam.append([reg, mod, q, sufixo])
import re  # noqa: E402
privadas = []
for reg_, mod_, q_, s_ in faltam:
    t_ = open(os.path.join(HERE, "insumos", "pedras", mod_ + ".lean"), encoding="utf-8").read()
    if re.search(r"^\s*private\s+(?:theorem|lemma|def)\s+" + re.escape(q_.split(".")[-1]) + r"\b", t_, re.M):
        privadas.append(q_)
rep_priv = {"faltam_que_sao_private_na_fonte": len(privadas), "nota_private": "declaracao `private` nao tem nome publico no Audit (o nome leva o modulo): nao serve de ancora por nome; todas no trio pelo POS_BUILD"}
rep = {**rep_priv, "ancoras_propostas": AP, "sha256": hashlib.sha256(open(AP, "rb").read()).hexdigest(), "manifesto_da_proposta_igual_ao_atual": a.get("manifesto_sha256") == man_sha,
       "n_nomes_conferidos": n, "n_faltam": len(faltam), "faltam": faltam[:50], "por_registro": res,
       "nota": "conferencia por nome contra o Audit do sandbox k412c (todos os nomes do Audit estao no trio: POS_BUILD_v412); a escolha das ancoras e' do contrato"}
out = os.path.join(HERE, "kernel", "ANCORAS_PROPOSTAS_CONFERIDAS_v412.json")
open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(rep, ensure_ascii=False, indent=1)); os.replace(out + ".tmp", out)
print("nomes conferidos:", n, "| faltam:", len(faltam), faltam[:5], "| manifesto igual:", rep["manifesto_da_proposta_igual_ao_atual"])
