# -*- coding: utf-8 -*-
# [DERIVADO v412 r7, claude-construtor-v412 (contrato R11)] copia de conferir_ancoras_propostas_v412_r5.py; trocas de texto exato com contagem registrada em DERIVACAO_R7_PIPELINE_v412.json (derivador: e7_02_derivar_kernel_v412.py). O original fica intacto.
# [DERIVADO v412 r5, claude-construtor-v412 (contrato R11)] reescrita de conferir_ancoras_propostas_v412_c4.py (que fica intacto) para a DECIMA SEGUNDA lista: o nome completo de cada declaracao NAO e' montado pelo prefixo do modulo.
"""conferir_ancoras_propostas_v412_r7.py -- so' LEITURA. Confere as ancoras que a gerencia PROPOS em insumos\\ANCORAS_PROPOSTAS_v412_R12.json (listas com_estrela, sem_estrela e listadas_em_print_axioms de cada modulo) contra o kernel do
sandbox ja' medido (kernel\\FLAGS_v412.json, do pos_build_kernel_v412_r7.py: a proveniencia das declaracoes publicas no relatorio de axiomas, e as linhas `#print axioms` de cada fonte, resolvidas no relatorio).
O NOME COMPLETO de cada declaracao sai do RELATORIO DE AXIOMAS, por um destes caminhos (o caminho fica dito em `via`), nunca por prefixo do modulo:
  print_axioms         -- a propria fonte lista a declaracao numa linha `#print axioms` (que traz o nome completo, ou o nome dentro do namespace da linha), e o pos_build achou esse nome no relatorio, com proveniencia no modulo;
  proveniencia         -- ha' UMA so' declaracao publica com proveniencia no modulo cujo nome e' o proposto ou termina em .<proposto>;
  namespace_do_insumo  -- ha' mais de uma candidata na proveniencia do modulo, e o namespace que o insumo da' para o modulo escolhe uma delas (desempate; o nome continua sendo um nome do relatorio);
e cada nome e' classificado: publica (serve de ancora: existe no relatorio, vem do modulo dito, tem bandeira), private (a fonte o declara `private`: nao serve de ancora por nome), ambiguo ou ausente (falhas visiveis).
Grava kernel\\ANCORAS_PROPOSTAS_CONFERIDAS_v412_R7.json. uso: C:\\Python314\\python.exe -B -X utf8 conferir_ancoras_propostas_v412_r7.py"""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
INS = os.path.join(HERE, "insumos")
AP = os.path.join(INS, "ANCORAS_PROPOSTAS_v412_R12.json")
MAN_P = os.path.join(INS, "MANIFESTO_PEDRAS_v412_R12.json")
PED = os.path.join(INS, "pedras_r12")
sha = lambda b: hashlib.sha256(b).hexdigest()
a = json.load(open(AP, encoding="utf-8"))
f = json.load(open(os.path.join(HERE, "kernel", "FLAGS_v412.json"), encoding="utf-8"))
pos = json.load(open(os.path.join(HERE, "kernel", "POS_BUILD_v412.json"), encoding="utf-8"))
assert pos.get("ok") is True, "o POS_BUILD_v412.json nao esta verde: nada a conferir"
prov = f["proveniencia_publicas"]; chave = {x[1]: x[0] for x in f["flags"]}
man_sha = sha(open(MAN_P, "rb").read())
pub_por_rel = {}
for k, v in prov.items():
    pub_por_rel.setdefault(v, []).append(k)
prints_por_mod = {}
for nome_res, d in f["ancoras"].items():
    prints_por_mod.setdefault(d["modulo"], []).append(d)
RX_DECL = r"^[ \t]*(?:@\[[^\]\n]*\][ \t]*\n?[ \t]*)*((?:(?:private|protected|noncomputable)[ \t]+)*)(?:theorem|lemma|def|abbrev|structure|inductive|instance)[ \t]+%s(?![\w'.])"


def classe_na_fonte(texto, nome_curto):
    return [m.group(1) for m in re.finditer(RX_DECL % re.escape(nome_curto), texto, re.M)]


fontes = {}
res = {}; cont = {"publica": 0, "private": 0, "ausente": 0, "ambiguo": 0}; vias = {}; ausentes = []; priv = []; ambiguos = []; conflito = []
por_lista = {}
n = 0
for reg, itens in a["registros"].items():
    for it in itens:
        ns = it.get("namespace"); mod = it.get("modulo"); rel = "TGLExt/%s.lean" % mod
        if mod not in fontes:
            fontes[mod] = open(os.path.join(PED, mod + ".lean"), encoding="utf-8").read()
        pubs = pub_por_rel.get(rel, [])
        prs = prints_por_mod.get("TGLExt." + mod, [])
        for lista in ("com_estrela", "sem_estrela", "listadas_em_print_axioms"):
            for nm in list(it.get(lista) or []):
                n += 1
                cp = sorted({d["resolvido"] for d in prs if d.get("resolvido") and (d["texto"].lstrip("@") == nm or d["texto"].endswith("." + nm) or d["resolvido"] == nm or d["resolvido"].endswith("." + nm))})
                cv = sorted(k for k in pubs if k == nm or k.endswith("." + nm))
                nome_audit = None; via = None; cl = None
                if len(cp) == 1 and (cp[0] in cv or not cv):
                    nome_audit, via = cp[0], "print_axioms"
                elif len(cv) == 1:
                    nome_audit, via = cv[0], "proveniencia"
                    if len(cp) == 1 and cp[0] != cv[0]:
                        conflito.append([reg, mod, nm, cp, cv])
                elif len(cv) > 1 or len(cp) > 1:
                    cands = sorted(set(cv) | set(cp))
                    q = (ns + "." + nm) if ns else nm
                    if q in cands:
                        nome_audit, via = q, "namespace_do_insumo"
                    else:
                        cl = "ambiguo"; ambiguos.append([reg, mod, nm, cands])
                else:
                    mods_ = classe_na_fonte(fontes[mod], nm.split(".")[-1])
                    if mods_ and all("private" in m_ for m_ in mods_):
                        cl = "private"; priv.append([reg, mod, nm])
                    else:
                        cl = "ausente"; ausentes.append([reg, mod, nm, mods_])
                if nome_audit:
                    ok_rel = prov.get(nome_audit) == rel
                    if not ok_rel:
                        cl = "ausente"; ausentes.append([reg, mod, nm, "o nome achado nao tem proveniencia no modulo: %s" % prov.get(nome_audit)]); nome_audit = None; via = None
                    else:
                        cl = "publica"
                cont[cl] += 1; por_lista.setdefault(lista, dict.fromkeys(cont, 0)); por_lista[lista][cl] += 1
                if via:
                    vias[via] = vias.get(via, 0) + 1
                res.setdefault(reg, []).append({"modulo": mod, "lista": lista, "nome_proposto": nm, "classe": cl, "via": via, "nome_no_audit": nome_audit,
                                                "bandeira_proposta": chave.get(nome_audit) if nome_audit else None,
                                                "no_trio": True if (nome_audit and pos.get("ok") is True) else None})   # (o pos_build confere que todo nome do relatorio de axiomas esta no trio)
n_pub_sem_bandeira = sum(1 for r in res.values() for x in r if x["classe"] == "publica" and not x["bandeira_proposta"])
sem_bandeira = [[x["modulo"], x["nome_no_audit"]] for r in res.values() for x in r if x["classe"] == "publica" and not x["bandeira_proposta"]]
rep = {"ancoras_propostas": AP, "sha256_das_propostas": sha(open(AP, "rb").read()), "manifesto": MAN_P, "sha256_do_manifesto": man_sha,
       "manifesto_da_proposta_igual_ao_atual": a.get("manifesto_sha256") == man_sha, "n_nomes_conferidos": n, "por_classe": cont, "por_lista_e_classe": por_lista, "por_via": vias,
       "n_publicas_sem_bandeira": n_pub_sem_bandeira, "publicas_sem_bandeira": sem_bandeira[:40],
       "private_na_fonte": {"n": len(priv), "nota": "declaracao `private` nao tem nome publico no relatorio (o nome leva o modulo): nao serve de ancora por nome; todas as declaracoes novas do relatorio estao no trio (POS_BUILD_v412.json)", "nomes": priv},
       "ausentes": ausentes, "ambiguos": ambiguos, "print_axioms_e_proveniencia_discordam": conflito, "por_registro": res,
       "nota": "o nome completo de cada declaracao sai do relatorio de axiomas do sandbox k412c (kernel\\FLAGS_v412.json: proveniencia das publicas e linhas #print axioms resolvidas), nunca do prefixo do modulo; a escolha das ancoras e' do contrato (e5_11)"}
out = os.path.join(HERE, "kernel", "ANCORAS_PROPOSTAS_CONFERIDAS_v412_R7.json")
if os.path.exists(out):
    os.replace(out, out + ".bak_anterior")
with open(out + ".tmp", "w", encoding="utf-8") as fh:
    fh.write(json.dumps(rep, ensure_ascii=False, indent=1))
os.replace(out + ".tmp", out)
print("nomes conferidos:", n, "| por classe:", cont, "| por via:", vias, "| private na fonte:", len(priv), "| ausentes:", len(ausentes), ausentes[:4], "| ambiguos:", len(ambiguos), ambiguos[:3],
      "| discordam:", len(conflito), "| manifesto da proposta == o atual:", rep["manifesto_da_proposta_igual_ao_atual"], "| publicas sem bandeira:", n_pub_sem_bandeira, sem_bandeira[:4])
sys.exit(0 if not ausentes and not ambiguos and not conflito else 1)
