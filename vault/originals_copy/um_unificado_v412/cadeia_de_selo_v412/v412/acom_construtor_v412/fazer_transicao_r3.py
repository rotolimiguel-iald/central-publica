# -*- coding: utf-8 -*-
"""fazer_transicao_r3.py -- (claude-construtor-v412, continuacao 2, 17/11/2026) compoe acom_construtor_v412/transicao_r3.json (o q e o p da transicao ACOM do fecho R3) com numeros e sha256 LIDOS dos
artefatos. Depois: C:/Python314/python.exe -X utf8 ../acom_init_construtor_v412.py --transicao transicao_r3.json (usa a SUA referencia, faz get e transition com a revisao lida)."""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(H)
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
pr = os.path.join(P, "PRONTO_PARA_CANDIDATO_v412_R3.json"); rc = os.path.join(P, "kernel", "KERNEL_RECIBO_v412.json")
d = json.load(open(pr, encoding="utf-8")); k = d["kernel_k412c"]; c = d["comparacao_com_o_r2"]; t = k["linha_TOTAL"]
texto = ("Continuacao 2 do complemento da Etapa 1 da v412 fechada pelo construtor: o sandbox C:/t/k412c/final passou da quarta para a quinta lista de pedras (manifesto R5, sha16 %s; 40 modulos; 6 emendados so em comentarios e docstrings, codigo igual por dois metodos); "
         "%d de %d compilaram (rc 0); TOTAL decl %d thm %d fora do trio %d; escada %s; %d bandeiras novas; chaves das bandeiras identicas as do R2: %s; ancoras propostas %s; igual ao R2 em tudo medido; um.py do Nos sha16 %s intacto, nenhum modulo do manifesto no kernel do Nos. "
         "Nada instalado no Nos; rito nao rodou; sem candidato.") % (d["manifesto"]["sha16"], k["modulos_compilados_rc0"], k["n_modulos"], t["decl"], t["thm"], t["fora_do_trio"], k["escada_de_teoremas_e_bandeiras"], k["n_bandeiras_novas"],
                                                                       c["chaves_das_bandeiras_identicas"], d["ancoras_propostas"]["por_classe"], d["nos_intacto"]["conteudo"]["um_py_sha16"])
out = {"event_id": "construtor-v412-r3-quinta-lista-17nov",
       "changes": {"records": [{"id": "construtor-v412-r3", "kind": "fact", "statute": "REAL", "text": texto,
                                "sources": [{"kind": "artifact", "ref": pr.replace("\\", "/") + "#sha256:" + sha(pr)}, {"kind": "artifact", "ref": rc.replace("\\", "/") + "#sha256:" + sha(rc)}]}],
                   "flow": {"phase": "preparacao_v412__r3_quinta_lista_fechada__parado", "next_action": "gerencia: congelar o DESENHO e o contrato, prefixos das bandeiras, consertar a checagem vazia do pos_build; Etapa 2 por novo construtor"}}}
op = os.path.join(H, "transicao_r3.json")
open(op, "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
print(op, "sha16", sha(op)[:16])
