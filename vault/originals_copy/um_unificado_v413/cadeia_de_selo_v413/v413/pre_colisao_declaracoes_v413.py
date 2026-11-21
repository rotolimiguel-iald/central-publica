# -*- coding: utf-8 -*-
# [DERIVADO v413, claude-construtor-v413 (Etapa 1, 20/11/2026)] copia de C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\pre_colisao_declaracoes_v412_r7.py; trocas de texto exato com contagem registrada em DERIVACAO_ETAPA1_v413.json (derivador: derivar_scripts_etapa1_v413.py) e subida dos rotulos de versao (v412->v413, v411->v412); o molde fica intacto.
# [DERIVADO v412 r7, claude-construtor-v412 (contrato R11)] copia de pre_colisao_declaracoes_v412_r5.py; trocas de texto exato com contagem registrada em DERIVACAO_R7_PIPELINE_v412.json (derivador: e7_02_derivar_kernel_v412.py). O original fica intacto.
# [DERIVADO v412 r5, 18/11/2026, claude-construtor-v412 (contrato R11)] copia de pre_colisao_declaracoes_v412_c4.py para a DECIMA SEGUNDA lista de pedras (insumos\MANIFESTO_PEDRAS_v412_R12.json, insumos\pedras_r12; 153 modulos); e5_02_derivar_scripts_r7_v412.py (trocas de texto exato com contagem registrada).
# [DERIVADO v412 c4, 17/11/2026, claude-construtor-v412 (contrato R4)] copia de pre_colisao_declaracoes_v412_r3.py para a DECIMA SEGUNDA lista de pedras (insumos\MANIFESTO_PEDRAS_v412_R12.json, insumos\pedras_r12; 42 modulos); e4_02_derivar_scripts_c4_v412.py (trocas de texto exato com contagem registrada).
# [DERIVADO v412 r3, 17/11/2026, claude-construtor-v412 (continuacao 2)] copia de pre_colisao_declaracoes_v412_r2.py para a DECIMA SEGUNDA lista de pedras (insumos\MANIFESTO_PEDRAS_v412_R12.json, insumos\pedras_r12); derivar_scripts_r3_v412.py (trocas de texto exato com contagem conferida).
# [DERIVADO v412 r2, 17/11/2026, claude-construtor-v412] copia de pre_colisao_declaracoes_v412.py para a DECIMA SEGUNDA lista (40 modulos); grava kernel\PRE_COLISAO_v412_R7.json (o da Etapa 1 fica). Os nomes do kernel vem do audit.log da v411.
"""pre_colisao_declaracoes_v413.py -- (claude-construtor-v412, 17/11/2026) PRE-CONFERENCIA de colisao de NOMES DE DECLARACAO, antes de instalar os modulos novos no sandbox.
[v413] le o manifesto da v413 (modulos_novos; as pedras limpas em insumos\\pedras_limpas\\TGLExt) e confere tambem o modulo que a v413 corrige so' no texto (kernel_corrigido):
os nomes que ele declara tem de estar todos no kernel atual (a correcao nao cria nem tira declaracao).
Le, por expressao regular sobre as fontes congeladas (insumos\\pedras_limpas\\TGLExt, sha256 conferido contra o manifesto), os nomes declarados (theorem, lemma, def, abbrev, structure, inductive,
class, instance com nome, opaque, axiom), qualificados pela pilha de `namespace`; as declaracoes `private` ficam fora (o nome delas leva o modulo). Compara:
 (a) com os nomes do kernel atual (as linhas TGL_DECL_SOURCE do log do Audit da v412, que e' o kernel do k412c byte a byte), por nome exato e por prefixo de estrutura;
 (b) entre os proprios modulos novos (dois modulos que nao se importam podem declarar o mesmo nome: so' a raiz, que importa os dois, o veria).
E' uma pre-conferencia por texto: o juiz definitivo e' o build da raiz no sandbox (o Lean recusa ambiente com nome repetido). Grava kernel\\PRE_COLISAO_v413.json. Sai 1 se houver colisao.
uso: C:\\Python314\\python.exe -B -X utf8 pre_colisao_declaracoes_v413.py"""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
PK = os.path.dirname(os.path.abspath(__file__))
MAN = json.load(open(os.path.join(PK, "insumos", "MANIFESTO_PEDRAS_v413.json"), encoding="utf-8"))
PED = os.path.join(PK, "insumos", "pedras_limpas", "TGLExt")
KC = {k_: v_ for k_, v_ in (MAN.get("kernel_corrigido") or {}).items()}
AUD = os.path.join(os.path.dirname(PK), "v412", "kernel", "audit.log")
OUT = os.path.join(PK, "kernel", "PRE_COLISAO_v413.json")
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
for k_, m in MAN["modulos_novos"].items():
    nome_ = k_.split(".", 1)[1]
    b = open(os.path.join(PED, nome_ + ".lean"), "rb").read()
    if hashlib.sha256(b).hexdigest() != m["sha256_pedra_limpa"]:
        sha_ruim.append(nome_)
    por_mod[nome_] = nomes_da_fonte(b.decode("utf-8"))
# o modulo corrigido so' no texto: os nomes que ele declara tem de ser EXATAMENTE os que o kernel ja tem dele (nada novo, nada some)
corr_rep = {}
for k_, v_ in KC.items():
    b = open(v_["saida"], "rb").read()
    if hashlib.sha256(b).hexdigest() != v_["sha256_saida"]:
        sha_ruim.append(k_)
    ns_ = sorted({q for q, kw in nomes_da_fonte(b.decode("utf-8"))})
    ausentes_ = [q for q in ns_ if q not in existentes]
    corr_rep[k_] = {"n_nomes_lidos": len(ns_), "nomes_que_o_kernel_nao_tem": ausentes_, "ok": not ausentes_}
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
       "kernel_corrigido": corr_rep, "kernel_corrigido_ok": all(v_["ok"] for v_ in corr_rep.values()) and len(corr_rep) == len(KC),
       "colisao_com_o_kernel_nome_exato": col_kernel, "colisao_com_o_kernel_prefixo_de_estrutura": col_prefixo, "colisao_entre_os_modulos_da_lista": col_entre,
       "nota": "pre-conferencia por texto (expressao regular sobre as fontes, sem comentarios); o juiz definitivo e' o build da raiz no sandbox"}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
_b = json.dumps(rep, ensure_ascii=False, indent=1).encode("utf-8")
if os.path.exists(OUT):   # [v413] backup de BYTES antes de regravar a saida (o molde gravava por cima)
    _bk = OUT + ".bak_" + __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S"); open(_bk, "wb").write(open(OUT, "rb").read()); assert open(_bk, "rb").read() == open(OUT, "rb").read()
open(OUT + ".tmp", "wb").write(_b); assert os.path.getsize(OUT + ".tmp") == len(_b); os.replace(OUT + ".tmp", OUT)
print(json.dumps({k: v for k, v in rep.items() if k != "n_nomes_lidos_por_modulo"}, ensure_ascii=False, indent=1)[:4000])
sys.exit(1 if (col_kernel or col_prefixo or col_entre or sha_ruim or not rep["kernel_corrigido_ok"]) else 0)
