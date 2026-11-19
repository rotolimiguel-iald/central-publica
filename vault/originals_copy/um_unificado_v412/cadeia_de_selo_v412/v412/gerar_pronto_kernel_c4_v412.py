# -*- coding: utf-8 -*-
"""gerar_pronto_kernel_c4_v412.py -- (contrato R4) FECHA a etapa do kernel da setima lista: PRONTO_PARA_CANDIDATO_v412_R4.json e TAMANHOS_CRIADOS_v412_R4.json. Tudo LIDO dos recibos por script; compara com o estado do R3 (as copias .bak_r3 de kernel/):
o esperado e' 42 de 42 com saida zero, declaracoes/teoremas/bandeiras crescendo so' pelo que Token2 e AMaquina trazem, nenhuma chave antiga mudada, zero fora do trio, so' o aviso conhecido."""
import datetime, hashlib, json, os, sys
from pathlib import Path
sys.path.insert(0, r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
sys.stdout.reconfigure(encoding="utf-8")
from e2_lib_v412 import D, ler_json, salvar_json, sha16_arq, Exame

K = D / "kernel"
pos, fl, kh = ler_json(K / "POS_BUILD_v412.json"), ler_json(K / "FLAGS_v412.json"), ler_json(K / "KH_N1_v412.json")
pos3, fl3 = ler_json(K / "POS_BUILD_v412.json.bak_r3"), ler_json(K / "FLAGS_v412.json.bak_r3")
r3 = ler_json(D / "PRONTO_PARA_CANDIDATO_v412_R3.json")
set_l, nos = ler_json(K / "SETIMA_LISTA_CONFERIDA_v412.json"), ler_json(K / "NOS_INTACTO_C4_v412.json")
anc = ler_json(K / "ANCORAS_PROPOSTAS_CONFERIDAS_v412_R4.json"); built = ler_json(K / "BUILT_CHECAGEM_CORRIGIDA_R4_v412.json")
man = ler_json(D / "insumos" / "MANIFESTO_PEDRAS_v412_R7.json"); marcas = (K / "construir_marcas.txt").read_text(encoding="utf-8")
e = Exame("kernel_setima_lista")
k3 = {f[0]: f[1] for f in fl3["flags"]}; k4 = {f[0]: f[1] for f in fl["flags"]}
novas_chaves = sorted(set(k4) - set(k3)); sumidas = sorted(set(k3) - set(k4)); mudou_nome = [k for k in k3 if k in k4 and k3[k] != k4[k]]
e.chk("42 de 42 modulos com saida zero (marcas: uma linha por modulo, rc 0)", marcas.count("rc=0 s=") == 42 and "rc=0\nfim" in marcas.replace("\r", ""), 42)
e.chk("zero erro, zero sorry; rc do build e do Audit 0", pos["ok"] is True and not pos.get("falhas"), len(pos.get("sinais", [])), pos.get("falhas"))
e.chk("fora dos tres axiomas: zero declaracoes (linha TOTAL e criterio j1)", pos["linha_TOTAL"]["fora_do_trio"] == 0 and pos["criterios"]["j1_fora_do_trio"] == 0, pos["linha_TOTAL"]["decl"])
e.chk("nenhuma chave antiga muda de literal (as %d chaves da v411)" % pos["chaves_antigas"]["n"], not pos["chaves_antigas"]["mudam"] and pos["chaves_antigas"]["n"] > 0, pos["chaves_antigas"]["n"])
e.chk("as 903 chaves de bandeira do R3 seguem identicas (mesmo nome de declaracao) e nenhuma sumiu", not sumidas and not mudou_nome and len(k3) == 903, len(k3), [sumidas[:2], mudou_nome[:2]])
mods_novos = sorted({fl["flags"][i][2] for i in range(len(fl["flags"])) if fl["flags"][i][0] in novas_chaves})
e.chk("as bandeiras novas vem so' de Token2 e AMaquina", mods_novos == ["TGLExt.AMaquina", "TGLExt.Token2"] and len(novas_chaves) == fl["n_flags"] - 903, len(novas_chaves), mods_novos)
d_decl, d_thm = pos["linha_TOTAL"]["decl"] - pos3["linha_TOTAL"]["decl"], pos["linha_TOTAL"]["thm"] - pos3["linha_TOTAL"]["thm"]
e.chk("o crescimento de declaracoes e teoremas sobre o R3 e' so' dos dois modulos novos (n por modulo: Token2 e AMaquina; os outros 40 iguais ao R3)", all(fl["n_por_modulo"][m] == fl3["n_por_modulo"][m] for m in fl3["n_por_modulo"]) and d_decl > 0, len(fl["n_por_modulo"]), {"decl": d_decl, "thm": d_thm, "Token2": fl["n_por_modulo"]["TGLExt.Token2"], "AMaquina": fl["n_por_modulo"]["TGLExt.AMaquina"]})
e.chk("so' o aviso conhecido da TowerWedgeIndex (nenhum outro modulo com aviso)", not {m: v["n"] for m, v in pos["avisos_por_modulo"].items() if v["n"] and m != "TGLExt.TowerWedgeIndex"} and pos["aviso_conhecido_TowerWedgeIndex"]["parece_o_conhecido"], len(pos["avisos_por_modulo"]))
e.chk("a checagem Built corrigida examinou mais de zero modulos (os dois novos) e os controles passaram", built["ok"] is True and pos and any(s["detalhe"] and s["detalhe"].get("examinados", 0) > 0 for s in pos["sinais"] if "tinha de compilar" in s["checagem"]), 2)
e.chk("a escada medida e' a do candidato: [12308, %d]" % fl["escada"][1], fl["escada"] == [12308, 12308 + fl["n_flags"]] and kh["linha_TOTAL"]["decl"] == pos["linha_TOTAL"]["decl"], fl["n_flags"])
e.chk("a setima lista foi conferida (9/9) e as ancoras propostas conferem (zero ausentes, zero ambiguos)", set_l["ok"] and anc["ausentes"] == [] and anc["ambiguos"] == [] and anc["n_publicas_ou_por_sufixo_sem_bandeira"] == 0, anc["n_nomes_conferidos"])
e.chk("o Nos esta intacto (um.py v411; nenhum modulo do manifesto no kernel do Nos)", not nos.get("conteudo", nos)["falhas"] and nos.get("conteudo", nos)["um_py_sha16"] == "1203b1f9202020d6", 1)
fecho = {"contrato": "PRONTO_PARA_CANDIDATO_v412_R4", "quando": datetime.datetime.now().isoformat(timespec="seconds"), "agente": "claude-construtor-v412 (Etapa 2, contrato R4), a servico da gerencia c1",
         "estado": "KERNEL DA SETIMA LISTA FECHADO NO SANDBOX k412c: 42 de 42 compilaram; medicoes feitas; nada instalado no Nos; rito nao rodou", "kernel_fechou": e.ok, "checagens": e.linhas, "resumo": e.resumo(),
         "contrato_r4": {"arquivo": "CONTRATO_v412_R4.md", "sha16": sha16_arq(D / "CONTRATO_v412_R4.md")}, "manifesto": {"arquivo": "insumos/MANIFESTO_PEDRAS_v412_R7.json", "sha16": sha16_arq(D / "insumos" / "MANIFESTO_PEDRAS_v412_R7.json"), "n_modulos": man["n_modulos"],
                                                                                                                       "novas_em_relacao_a_quinta_lista": man["novas_em_relacao_a_quinta_lista"], "mudaram_da_sexta_lista": man["mudaram_da_sexta_lista"]},
         "sandbox": "C:\\t\\k412c\\final", "linha_TOTAL": pos["linha_TOTAL"], "linha_TOTAL_quinta_lista": pos3["linha_TOTAL"], "linha_TOTAL_v411": pos["linha_TOTAL_v411"], "delta_vs_quinta_lista": {"decl": d_decl, "thm": d_thm, "bandeiras": fl["n_flags"] - 903},
         "delta_vs_v411": pos["delta_vs_v411"], "escada": fl["escada"], "n_bandeiras": fl["n_flags"], "n_por_modulo_dos_novos": {m: fl["n_por_modulo"][m] for m in ("TGLExt.Token2", "TGLExt.AMaquina")}, "duracao_build_s": kh.get("duracao_build_s"), "duracao_audit_s": kh.get("duracao_audit_s"),
         "ancoras_propostas": {"arquivo": "insumos/ANCORAS_PROPOSTAS_v412_R7.json", "sha16": sha16_arq(D / "insumos" / "ANCORAS_PROPOSTAS_v412_R7.json"), "conferencia": "kernel/ANCORAS_PROPOSTAS_CONFERIDAS_v412_R4.json", "n_nomes": anc["n_nomes_conferidos"], "por_classe": anc["por_classe"]},
         "recibos": {n: sha16_arq(K / n) for n in ("POS_BUILD_v412.json", "FLAGS_v412.json", "KERNEL_RECIBO_v412.json", "KH_N1_v412.json", "LOGS_COPIADOS_v412.json", "SETIMA_LISTA_CONFERIDA_v412.json", "NOS_INTACTO_C4_v412.json", "BUILT_CHECAGEM_CORRIGIDA_R4_v412.json", "audit.log", "lake_build.log")},
         "desvios_desta_ordem": ["o build foi INCREMENTAL: so' Token2 e AMaquina (e a raiz e o Audit) foram compilados nesta rodada; os outros 40 estavam em dia para o lake (compilados e medidos na rodada anterior, mesmas fontes por sha256); o rito do Nos compila tudo a frio",
                                 "scripts _c4 derivados dos _r3 (e do pos_build _r4 com a checagem Built corrigida) por troca exata com contagem registrada (DERIVACAO_C4_v412.json); os _r2, _r3 e _r4 ficam intactos", "o estado do R3 de kernel/ tem copia .bak_r3 (kernel/GUARDA_R3_v412.json)"],
         "estatuto": "[REAL] medido no sandbox C:\\t\\k412c\\final; nada instalado no Nos; o rito nao rodou; validade no kernel nao e' creditacao; o gate nao se move"}
salvar_json(D / "PRONTO_PARA_CANDIDATO_v412_R4.json", fecho)
print(e.resumo(), "| gravado PRONTO_PARA_CANDIDATO_v412_R4.json", sha16_arq(D / "PRONTO_PARA_CANDIDATO_v412_R4.json"))
for l in e.linhas:
    if not l["ok"]:
        print("FALHOU:", l["checagem"], l["n_itens_examinados"], str(l["detalhe"])[:300])
sys.exit(0 if e.ok else 1)
