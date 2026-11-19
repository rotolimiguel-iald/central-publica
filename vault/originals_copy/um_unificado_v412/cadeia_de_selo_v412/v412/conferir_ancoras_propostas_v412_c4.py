# -*- coding: utf-8 -*-
# [DERIVADO v412 c4, 17/11/2026, claude-construtor-v412 (contrato R4)] copia de conferir_ancoras_propostas_v412_r3.py para a SETIMA lista de pedras (insumos\MANIFESTO_PEDRAS_v412_R7.json, insumos\pedras_r7; 42 modulos); e4_02_derivar_scripts_c4_v412.py (trocas de texto exato com contagem registrada).
# [DERIVADO v412 r3, 17/11/2026, claude-construtor-v412 (continuacao 2)] copia de conferir_ancoras_propostas_v412_r2.py para a SETIMA lista de pedras (insumos\MANIFESTO_PEDRAS_v412_R7.json, insumos\pedras_r7); derivar_scripts_r3_v412.py (trocas de texto exato com contagem conferida).
"""conferir_ancoras_propostas_v412_c4.py -- (claude-construtor-v412, complemento da Etapa 1, 17/11/2026) so' LEITURA. Copia ampliada de conferir_ancoras_propostas_v412.py para a SETIMA lista:
confere as ancoras que a gerencia PROPOS em insumos\\ANCORAS_PROPOSTAS_v412_R7.json contra o kernel do sandbox ja' medido (kernel\\FLAGS_v412.json, gerado pelo pos_build_kernel_v412_c4.py:
proveniencia das declaracoes publicas no Audit). Cada nome (namespace + nome) e' classificado em UMA classe:
  publica      -- existe no axiom_report do Audit, vem do modulo dito, no trio, e tem bandeira proposta (serve de ancora por nome);
  por_sufixo   -- nao bate com namespace+nome mas ha' UMA so' publica do mesmo modulo que termina em .nome (namespace interno do modulo); serve de ancora com o nome completo que o Audit tem;
  private      -- a fonte congelada declara o nome como `private`: o Audit o guarda como _private.<modulo>.<n>.<nome>; NAO serve de ancora por nome;
  ausente      -- nem publica nem private (nao deveria existir; se houver, e' falha visivel).
Nao escolhe ancora nenhuma (isso e' do contrato, Etapa 2). Grava kernel\\ANCORAS_PROPOSTAS_CONFERIDAS_v412_R4.json (o da Etapa 1 fica).
uso: C:\\Python314\\python.exe -B -X utf8 conferir_ancoras_propostas_v412_c4.py"""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
INS = os.path.join(HERE, "insumos")
AP = os.path.join(INS, "ANCORAS_PROPOSTAS_v412_R7.json")
MAN_P = os.path.join(INS, "MANIFESTO_PEDRAS_v412_R7.json")
PED = os.path.join(INS, "pedras_r7")
TRIO = {"propext", "Classical.choice", "Quot.sound"}
sha = lambda b: hashlib.sha256(b).hexdigest()
a = json.load(open(AP, encoding="utf-8"))
f = json.load(open(os.path.join(HERE, "kernel", "FLAGS_v412.json"), encoding="utf-8"))
pos = json.load(open(os.path.join(HERE, "kernel", "POS_BUILD_v412.json"), encoding="utf-8"))
assert pos.get("ok") is True, "o POS_BUILD_v412.json nao esta verde: nada a conferir"
prov = f["proveniencia_publicas"]; chave = {x[1]: x[0] for x in f["flags"]}
man_sha = sha(open(MAN_P, "rb").read())
RX_DECL = r"^[ \t]*(?:@\[[^\]\n]*\][ \t]*\n?[ \t]*)*((?:(?:private|protected|noncomputable)[ \t]+)*)(?:theorem|lemma|def)[ \t]+%s(?![\w'.])"


def classe_na_fonte(texto, nome_curto):
    """[modificadores de cada declaracao com esse nome curto na fonte] (so' theorem/lemma/def)."""
    return [m.group(1) for m in re.finditer(RX_DECL % re.escape(nome_curto), texto, re.M)]


fontes = {}
res = {}; cont = {"publica": 0, "por_sufixo": 0, "private": 0, "ausente": 0}; ausentes = []; priv = []; ambiguos = []
por_estrela = {"com_estrela": dict(cont), "sem_estrela": dict(cont)}
n = 0
for reg, itens in a["registros"].items():
    for it in itens:
        ns = it.get("namespace"); mod = it.get("modulo"); rel = "TGLExt/%s.lean" % mod
        if mod not in fontes:
            fontes[mod] = open(os.path.join(PED, mod + ".lean"), encoding="utf-8").read()
        for lista in ("com_estrela", "sem_estrela"):
            for nm in list(it.get(lista) or []):
                n += 1
                q = nm if (ns and nm.startswith(ns + ".")) else ((ns + "." + nm) if ns else nm)
                sufixo = None
                if q in prov and prov[q] == rel:
                    cl = "publica"; nome_audit = q
                else:
                    cands = [k for k, v in prov.items() if v == rel and (k == nm or k.endswith("." + nm))]
                    if len(cands) == 1:
                        cl = "por_sufixo"; nome_audit = cands[0]; sufixo = cands
                    elif len(cands) > 1:
                        cl = "ausente"; nome_audit = None; sufixo = cands; ambiguos.append([reg, mod, nm, cands])
                    else:
                        mods = classe_na_fonte(fontes[mod], nm.split(".")[-1])
                        if mods and all("private" in m_ for m_ in mods):
                            cl = "private"; nome_audit = None; priv.append([reg, mod, nm])
                        else:
                            cl = "ausente"; nome_audit = None; ausentes.append([reg, mod, q, mods])
                cont[cl] += 1; por_estrela[lista][cl] += 1
                res.setdefault(reg, []).append({"modulo": mod, "lista": lista, "nome_proposto": q, "classe": cl, "nome_no_audit": nome_audit,
                                                "bandeira_proposta": chave.get(nome_audit) if nome_audit else None,
                                                "no_trio": True if (nome_audit and pos.get("ok") is True) else None})   # (o pos_build confere que todo nome do axiom_report esta no trio)
n_pub_sem_bandeira = sum(1 for r in res.values() for x in r if x["classe"] in ("publica", "por_sufixo") and not x["bandeira_proposta"])
rep = {"ancoras_propostas": AP, "sha256_das_propostas": sha(open(AP, "rb").read()), "manifesto": MAN_P, "sha256_do_manifesto": man_sha,
       "manifesto_da_proposta_igual_ao_atual": a.get("manifesto_sha256") == man_sha, "n_nomes_conferidos": n, "por_classe": cont, "por_classe_e_estrela": por_estrela,
       "n_publicas_ou_por_sufixo_sem_bandeira": n_pub_sem_bandeira,
       "private_na_fonte": {"n": len(priv), "nota": "declaracao `private` nao tem nome publico no Audit (o nome leva o modulo): nao serve de ancora por nome; todas as declaracoes novas do Audit estao no trio (POS_BUILD_v412.json)", "nomes": priv},
       "ausentes": ausentes, "ambiguos": ambiguos, "por_registro": res,
       "nota": "conferencia por nome contra o Audit do sandbox k412c (kernel\\FLAGS_v412.json, proveniencia das publicas); a escolha das ancoras e' do contrato"}
out = os.path.join(HERE, "kernel", "ANCORAS_PROPOSTAS_CONFERIDAS_v412_R4.json")
if os.path.exists(out):
    os.replace(out, out + ".bak_anterior")
with open(out + ".tmp", "w", encoding="utf-8") as fh:
    fh.write(json.dumps(rep, ensure_ascii=False, indent=1))
os.replace(out + ".tmp", out)
print("nomes conferidos:", n, "| por classe:", cont, "| private na fonte:", len(priv), "| ausentes:", len(ausentes), ausentes[:3], "| ambiguos:", len(ambiguos),
      "| manifesto da proposta == o atual:", rep["manifesto_da_proposta_igual_ao_atual"], "| sem bandeira:", n_pub_sem_bandeira)
sys.exit(0 if not ausentes and not ambiguos else 1)
