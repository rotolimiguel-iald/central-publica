# -*- coding: utf-8 -*-
"""pre_colisao_declaracoes_v412.py -- (claude-construtor-v412, 17/11/2026) PRE-CONFERENCIA de colisao de NOMES DE DECLARACAO, antes de instalar os 34 modulos no sandbox.
Le, por expressao regular sobre as fontes congeladas (insumos\\pedras, sha256 conferido contra o manifesto), os nomes declarados (theorem, lemma, def, abbrev, structure, inductive,
class, instance com nome, opaque, axiom), qualificados pela pilha de `namespace`; as declaracoes `private` ficam fora (o nome delas leva o modulo). Compara:
 (a) com os 34300 nomes do kernel atual (as linhas TGL_DECL_SOURCE do log do Audit da v411, que e' o kernel do k411c byte a byte), por nome exato e por prefixo de estrutura;
 (b) entre os proprios 34 modulos (dois modulos que nao se importam podem declarar o mesmo nome: so' a raiz, que importa os dois, o veria).
E' uma pre-conferencia por texto: o juiz definitivo e' o build da raiz no sandbox (o Lean recusa ambiente com nome repetido). Grava kernel\\PRE_COLISAO_v412.json. Sai 1 se houver colisao.
uso: C:\\Python314\\python.exe -B -X utf8 pre_colisao_declaracoes_v412.py"""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
PK = os.path.dirname(os.path.abspath(__file__))
MAN = json.load(open(os.path.join(PK, "insumos", "MANIFESTO_PEDRAS_v412.json"), encoding="utf-8"))
PED = os.path.join(PK, "insumos", "pedras")
AUD = os.path.join(os.path.dirname(PK), "v411", "kernel", "audit.log")
OUT = os.path.join(PK, "kernel", "PRE_COLISAO_v412.json")
RX_DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)*((?:private|protected|noncomputable|partial|unsafe|nonrec)\s+)*(theorem|lemma|def|abbrev|structure|inductive|class|instance|opaque|axiom)\s+([^\s:({\[]+)", re.M)


def sem_comentarios(t):
    t = re.sub(r"/-.*?-/", lambda m: "\n" * m.group(0).count("\n"), t, flags=re.S)
    return re.sub(r"--[^\n]*", "", t)


def nomes_da_fonte(t):
    t = sem_comentarios(t)
    pilha = []; out = []
    for ln in t.split("\n"):
        s = ln.strip()
        m = re.match(r"^namespace\s+(\S+)", s)
        if m:
            pilha.append(m.group(1)); continue
        m = re.match(r"^end\s+(\S+)", s)
        if m and pilha and pilha[-1] == m.group(1):
            pilha.pop(); continue
        m = RX_DECL.match(s)
        if m:
            mods, kw, nome = m.group(1) or "", m.group(2), m.group(3)
            if "private" in mods or (kw == "instance" and nome in ("where", ":=")):
                continue
            if nome.startswith("_root_."):
                q = nome[len("_root_."):]
            else:
                q = ".".join(pilha + [nome]) if pilha else nome
            out.append((q, kw))
    return out


existentes = set()
for ln in open(AUD, "rb").read().decode("utf-8").splitlines():
    if ln.startswith("TGL_DECL_SOURCE\t"):
        existentes.add(ln.split("\t")[1])
por_mod = {}; sha_ruim = []
for m in MAN["modulos"]:
    b = open(os.path.join(PED, m["modulo"] + ".lean"), "rb").read()
    if hashlib.sha256(b).hexdigest() != m["sha256"]:
        sha_ruim.append(m["modulo"])
    por_mod[m["modulo"]] = nomes_da_fonte(b.decode("utf-8"))
col_kernel = []; col_prefixo = []
for mod, L in por_mod.items():
    for q, kw in L:
        if q in existentes:
            col_kernel.append([mod, q, kw])
        elif kw in ("structure", "class", "inductive") and any(e.startswith(q + ".") for e in existentes):
            col_prefixo.append([mod, q, kw])
dono = {}
col_entre = []
for mod, L in por_mod.items():
    for q, kw in L:
        if q in dono and dono[q] != mod:
            col_entre.append([dono[q], mod, q])
        dono.setdefault(q, mod)
rep = {"fonte_dos_nomes_do_kernel": AUD, "n_nomes_do_kernel": len(existentes), "sha256_fora_do_manifesto": sha_ruim,
       "n_nomes_lidos_por_modulo": {k: len(v) for k, v in por_mod.items()}, "n_nomes_lidos": sum(len(v) for v in por_mod.values()),
       "colisao_com_o_kernel_nome_exato": col_kernel, "colisao_com_o_kernel_prefixo_de_estrutura": col_prefixo, "colisao_entre_os_34": col_entre,
       "nota": "pre-conferencia por texto (expressao regular sobre as fontes, sem comentarios); o juiz definitivo e' o build da raiz no sandbox"}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT + ".tmp", "w", encoding="utf-8").write(json.dumps(rep, ensure_ascii=False, indent=1)); os.replace(OUT + ".tmp", OUT)
print(json.dumps({k: v for k, v in rep.items() if k != "n_nomes_lidos_por_modulo"}, ensure_ascii=False, indent=1)[:4000])
sys.exit(1 if (col_kernel or col_prefixo or col_entre or sha_ruim) else 0)
