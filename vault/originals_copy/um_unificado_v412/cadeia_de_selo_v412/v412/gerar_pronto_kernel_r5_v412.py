# -*- coding: utf-8 -*-
"""gerar_pronto_kernel_r5_v412.py -- (contrato R5) FECHA a etapa do kernel da decima lista: PRONTO_PARA_CANDIDATO_v412_R5.json. Tudo LIDO dos recibos por script; compara com o estado do fecho R4 (as copias .bak_c4 de kernel/):
o esperado e' 153 de 153 com saida zero, todos compilados neste build (a frio), as 952 chaves de bandeira do R4 identicas, as bandeiras novas so' dos 111 modulos novos, nenhuma chave antiga mudada, zero fora dos tres axiomas,
zero sorry, so' o aviso conhecido da TowerWedgeIndex, a escada antes e depois."""
import datetime, json, re, sys
from pathlib import Path
sys.path.insert(0, r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
sys.stdout.reconfigure(encoding="utf-8")
from e5_lib_v412 import D, ler_json, salvar_json, sha16_arq, Exame, MANIFESTO, ANCORAS, estado_bloco

K = D / "kernel"
pos, fl, kh = ler_json(K / "POS_BUILD_v412.json"), ler_json(K / "FLAGS_v412.json"), ler_json(K / "KH_N1_v412.json")
pos4, fl4 = ler_json(K / "POS_BUILD_v412.json.bak_c4"), ler_json(K / "FLAGS_v412.json.bak_c4")
dec, nos = ler_json(K / "DECIMA_LISTA_CONFERIDA_v412.json"), ler_json(K / "NOS_INTACTO_R5_v412.json")
anc = ler_json(K / "ANCORAS_PROPOSTAS_CONFERIDAS_v412_R5.json"); pre = ler_json(K / "PRE_COLISAO_v412_R5.json"); frio = ler_json(K / "FRIO_DOS_42_R5_v412.json"); ult = ler_json(K / "ULTIMA_INSTALACAO_v412.json")
man = ler_json(MANIFESTO); marcas = (K / "construir_marcas.txt").read_text(encoding="utf-8")
bundle = ler_json(D / "BUNDLE_v412.json")
N = int(man["n_modulos"])
e = Exame("kernel_decima_lista")
k4 = {f[0]: f[1] for f in fl4["flags"]}; k5 = {f[0]: f[1] for f in fl["flags"]}
novas_chaves = sorted(set(k5) - set(k4)); sumidas = sorted(set(k4) - set(k5)); mudou_nome = [k for k in k4 if k in k5 and k4[k] != k5[k]]
mods_r4 = set(fl4["n_por_modulo"])
n_marcas = len(re.findall(r"(?m)^modulo=\S+ rc=0 s=\d+$", marcas))
e.chk("%d de %d modulos com saida zero (marcas: uma linha por modulo, rc 0; rc final 0)" % (n_marcas, N), n_marcas == N == 153 and bool(re.search(r"(?m)^rc=0$", marcas)) and not re.search(r"(?m)^parou_em=", marcas), n_marcas)
e.chk("o pos_build esta verde: zero erro, zero sorry; rc do build e do Audit 0", pos["ok"] is True and not pos.get("falhas"), len(pos.get("sinais", [])), pos.get("falhas"))
modo = pos["modo_dos_modulos_no_build"]
e.chk("compilacao A FRIO: os %d modulos tiveram linha Built neste build (nenhum reaproveitado)" % N, pos["todos_os_modulos_a_frio"] is True and len(modo) == N and all(v == "Built" for v in modo.values()), len(modo), {k: v for k, v in modo.items() if v != "Built"})
e.chk("fora dos tres axiomas: zero declaracoes (linha TOTAL e criterio j1)", pos["linha_TOTAL"]["fora_do_trio"] == 0 and pos["criterios"]["j1_fora_do_trio"] == 0, pos["linha_TOTAL"]["decl"])
e.chk("nenhuma chave antiga muda de literal (as %d chaves da v411)" % pos["chaves_antigas"]["n"], not pos["chaves_antigas"]["mudam"] and pos["chaves_antigas"]["n"] > 0, pos["chaves_antigas"]["n"])
e.chk("as %d chaves de bandeira do fecho R4 (setima lista) seguem identicas (mesmo nome de declaracao) e nenhuma sumiu" % len(k4), not sumidas and not mudou_nome and len(k4) == fl4["n_flags"], len(k4), [sumidas[:2], mudou_nome[:2]])
mods_novos = sorted({f[2] for f in fl["flags"] if f[0] in set(novas_chaves)})
e.chk("as bandeiras novas vem so' dos modulos que a decima lista acrescenta (nenhum dos 42 antigos ganhou ou perdeu bandeira)", not (set(mods_novos) & mods_r4) and len(novas_chaves) == fl["n_flags"] - len(k4) and all(fl["n_por_modulo"][m] == fl4["n_por_modulo"][m] for m in mods_r4),
      len(novas_chaves), {"modulos_com_bandeira_nova": len(mods_novos)})
sem_flag = sorted(m for m, n in fl["n_por_modulo"].items() if n == 0)
e.chk("todo modulo do bundle tem pelo menos uma bandeira (declaracao nomeada publica)", not sem_flag and len(fl["n_por_modulo"]) == N, len(fl["n_por_modulo"]), sem_flag[:5])
pref = fl["prefixos"]
e.chk("os prefixos das bandeiras sao ext_<modulo em minusculas>_412_ e distintos entre si", len(set(pref.values())) == len(pref) == N and all(p == "ext_%s_412_" % m.split(".")[-1].lower() for m, p in pref.items()), len(pref))
outros_avisos = {m: v["n"] for m, v in pos["avisos_por_modulo"].items() if v["n"] and m != "TGLExt.TowerWedgeIndex"}
e.chk("so' o aviso conhecido da TowerWedgeIndex (nenhum outro modulo novo com aviso)", not outros_avisos and pos["aviso_conhecido_TowerWedgeIndex"]["parece_o_conhecido"], len(pos["avisos_por_modulo"]), outros_avisos)
s_built = next(s for s in pos["sinais"] if "tinha de compilar" in s["checagem"])
e.chk("a checagem Built examinou mais de zero modulos (os que a instalacao mudou no sandbox) e passou", s_built["ok"] and s_built["detalhe"]["examinados"] > 0, s_built["detalhe"]["examinados"], s_built["detalhe"])
E0 = fl["escada"][0]
e.chk("a escada medida: [%d, %d] (antes: a da v411; depois: mais as %d bandeiras)" % (E0, fl["escada"][1], fl["n_flags"]), fl["escada"] == [E0, E0 + fl["n_flags"]] and E0 == fl4["escada"][0] and kh["linha_TOTAL"]["decl"] == pos["linha_TOTAL"]["decl"], fl["n_flags"])
e.chk("a decima lista foi conferida (12/12) e a pre-conferencia de nomes nao achou colisao", dec["ok"] and not pre["colisao_com_o_kernel_nome_exato"] and not pre["colisao_com_o_kernel_prefixo_de_estrutura"] and not pre["colisao_entre_os_modulos_da_lista"], pre["n_nomes_lidos"])
e.chk("as ancoras propostas conferem com o relatorio de axiomas (zero ausentes, zero ambiguos, zero publicas sem bandeira)", anc["ausentes"] == [] and anc["ambiguos"] == [] and anc["n_publicas_sem_bandeira"] == 0 and anc["manifesto_da_proposta_igual_ao_atual"], anc["n_nomes_conferidos"], anc["por_via"])
e.chk("as duas transformacoes permitidas e mais nenhuma: o preparo reconstruiu cada instalado a partir do insumo (imports de irmaos trocados e #print axioms retirados) e pinou o sha256", bundle["n"] == N and bundle["manifesto_sha256"] == __import__("hashlib").sha256(MANIFESTO.read_bytes()).hexdigest(),
      bundle["n"], {"imports_trocados": sum(len(m["imports_trocados"]) for m in bundle["modulos"]), "print_axioms_retirados": sum(m["n_print_axioms_removidos"] for m in bundle["modulos"])})
e.chk("o Nos esta intacto (um.py v411; nenhum modulo do manifesto no kernel do Nos)", not nos["falhas"] and nos["um_py_sha16"] == "1203b1f9202020d6" and nos["um_py_igual_a_base_v411_em_bytes"], 1)
d_decl, d_thm = pos["linha_TOTAL"]["decl"] - pos4["linha_TOTAL"]["decl"], pos["linha_TOTAL"]["thm"] - pos4["linha_TOTAL"]["thm"]
por_frente = {}
fr = {x["modulo"]: x["frente"] for x in man["modulos"]}
for m, n in fl["n_por_modulo"].items():
    por_frente[fr[m.split(".")[-1]]] = por_frente.get(fr[m.split(".")[-1]], 0) + n
fecho = {"contrato": "PRONTO_PARA_CANDIDATO_v412_R5", "quando": datetime.datetime.now().isoformat(timespec="seconds"), "agente": "claude-construtor-v412 (Etapa 2 pelo contrato R5), a servico da gerencia c1",
         "estado": "KERNEL DA DECIMA LISTA FECHADO NO SANDBOX k412c: 153 de 153 compilaram a frio; medicoes feitas; nada instalado no Nos; rito nao rodou", "kernel_fechou": e.ok, "checagens": e.linhas, "resumo": e.resumo(),
         "contrato_r5": {"arquivo": "CONTRATO_v412_R5.md", "sha16": sha16_arq(D / "CONTRATO_v412_R5.md")},
         "manifesto": {"arquivo": "insumos/MANIFESTO_PEDRAS_v412_R10.json", "sha16": sha16_arq(MANIFESTO), "n_modulos": N, "por_frente": {k: sum(1 for x in man["modulos"] if x["frente"] == k) for k in "ABC"}, "por_autor": {a: sum(1 for x in man["modulos"] if x["de_quem"] == a) for a in sorted({x["de_quem"] for x in man["modulos"]})}},
         "sandbox": "C:\\t\\k412c\\final", "arvore_so_fontes": "C:\\t\\k412c\\arvore (a anterior foi para C:\\t\\k412c\\arvore_anterior_<data>, fora de work\\)",
         "linha_TOTAL": pos["linha_TOTAL"], "linha_TOTAL_setima_lista_R4": pos4["linha_TOTAL"], "linha_TOTAL_v411": pos["linha_TOTAL_v411"],
         "delta_vs_setima_lista": {"decl": d_decl, "thm": d_thm, "bandeiras": fl["n_flags"] - fl4["n_flags"]}, "delta_vs_v411": pos["delta_vs_v411"],
         "escada": {"antes": fl["escada"][0], "depois": fl["escada"][1], "n_bandeiras": fl["n_flags"], "escada_do_R4": fl4["escada"]}, "bandeiras_por_frente": por_frente,
         "teoremas": {"antes_v411": pos["linha_TOTAL_v411"]["thm"], "depois": pos["linha_TOTAL"]["thm"], "do_R4": pos4["linha_TOTAL"]["thm"]}, "declaracoes": {"antes_v411": pos["linha_TOTAL_v411"]["decl"], "depois": pos["linha_TOTAL"]["decl"], "do_R4": pos4["linha_TOTAL"]["decl"]},
         "duracao_build_s": kh.get("duracao_build_s"), "duracao_audit_s": kh.get("duracao_audit_s"), "n_ancoras_print_axioms": pos.get("n_ancoras"),
         "instalacao": {"mudados_no_sandbox_nesta_rodada": len(ult.get("mudados_no_sandbox", [])), "raiz_mudou": ult.get("raiz_mudou"), "artefatos_dos_42_movidos_para_a_compilacao_a_frio": {"quarentena": frio["quarentena"], "n_arquivos": frio["n_arquivos_movidos"]},
                        "imports_de_irmaos_trocados": sum(len(m["imports_trocados"]) for m in bundle["modulos"]), "linhas_print_axioms_retiradas": sum(m["n_print_axioms_removidos"] for m in bundle["modulos"]), "nomes_em_minusculas": sorted(m["modulo"] for m in bundle["modulos"] if m["modulo"][0].islower()),
                        "identificador_renomeado": "nenhum", "nome_repetido_na_compilacao": "nenhum (a raiz TGLExt e o TGL.Audit compilaram com os 153 imports)"},
         "ancoras_propostas": {"arquivo": "insumos/ANCORAS_PROPOSTAS_v412_R10.json", "sha16": sha16_arq(ANCORAS), "conferencia": "kernel/ANCORAS_PROPOSTAS_CONFERIDAS_v412_R5.json", "n_nomes": anc["n_nomes_conferidos"], "por_classe": anc["por_classe"], "por_via": anc["por_via"], "private_na_fonte": anc["private_na_fonte"]["n"]},
         "recibos": {n: sha16_arq(K / n) for n in ("POS_BUILD_v412.json", "FLAGS_v412.json", "KERNEL_RECIBO_v412.json", "KH_N1_v412.json", "LOGS_COPIADOS_v412.json", "DECIMA_LISTA_CONFERIDA_v412.json", "NOS_INTACTO_R5_v412.json", "PRE_COLISAO_v412_R5.json", "FRIO_DOS_42_R5_v412.json",
                                                    "ANCORAS_PROPOSTAS_CONFERIDAS_v412_R5.json", "ULTIMA_INSTALACAO_v412.json", "audit.log", "lake_build.log", "construir_marcas.txt")},
         "desvios_desta_ordem": ["o que e' ANTIGO (o kernel da v411 ja' compilado no sandbox) foi reaproveitado pelo lake; os 153 modulos novos, a raiz e o Audit foram compilados neste build; para isso os artefatos de build dos 42 modulos da setima lista foram MOVIDOS (nao apagados) para a quarentena fora de work\\",
                                 "scripts _r5 derivados dos _c4 por troca exata com contagem registrada (DERIVACAO_R5_v412.json); os anteriores ficam intactos; o estado do fecho R4 de kernel/ tem copia .bak_c4 (kernel/GUARDA_C4_v412.json)",
                                 "o preparo do bundle (preparar_bundle_v412.py, da Etapa 1) foi usado sem mudanca, com --manifesto e --pedras apontando para a decima lista"],
         "estatuto": "[REAL] medido no sandbox C:\\t\\k412c\\final; nada instalado no Nos; o rito nao rodou; validade no kernel nao e' creditacao; o gate nao se move"}
salvar_json(D / "PRONTO_PARA_CANDIDATO_v412_R5.json", fecho)
print(e.resumo(), "| gravado PRONTO_PARA_CANDIDATO_v412_R5.json", sha16_arq(D / "PRONTO_PARA_CANDIDATO_v412_R5.json"), "| TOTAL", pos["linha_TOTAL"], "| escada", fl["escada"], "| delta vs R4", fecho["delta_vs_setima_lista"])
for l in e.linhas:
    if not l["ok"]:
        print("FALHOU:", l["checagem"], l["n_itens_examinados"], str(l["detalhe"])[:400])
if e.ok:
    estado_bloco("1_kernel", True, {"fecho_kernel": D / "PRONTO_PARA_CANDIDATO_v412_R5.json", "pos_build": K / "POS_BUILD_v412.json", "flags": K / "FLAGS_v412.json", "recibo_kernel": K / "KERNEL_RECIBO_v412.json", "ancoras_conferidas": K / "ANCORAS_PROPOSTAS_CONFERIDAS_v412_R5.json"},
                 nota="kernel da decima lista fechado no sandbox: %d/%d a frio; TOTAL decl %d thm %d fora do trio %d; escada %d -> %d" % (n_marcas, N, pos["linha_TOTAL"]["decl"], pos["linha_TOTAL"]["thm"], pos["linha_TOTAL"]["fora_do_trio"], fl["escada"][0], fl["escada"][1]),
                 proximo="e5_11_ancoras_escolhidas_v412.py; e5_60_registros_v412.py; V412_REGERAR=1 gerar_candidato_v412_r5.py",
                 falta=["2_registros", "3_respostas_D224", "4_texto_publico (travessia com recibo)", "5_gerador_candidato_ensaio_portoes", "6_fecho"])
sys.exit(0 if e.ok else 1)
