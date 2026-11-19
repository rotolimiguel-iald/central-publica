# -*- coding: utf-8 -*-
"""fazer_transicao_etapa2.py -- (claude-construtor-v412, Etapa 2, contrato R4) compoe acom_construtor_v412/transicao_etapa2.json (o q e o p da transicao ACOM do fecho do candidato) com numeros e sha256 LIDOS dos artefatos.
Depois: C:/Python314/python.exe -X utf8 ../acom_init_construtor_v412.py --transicao transicao_etapa2.json (usa a SUA referencia, faz get e transition com a revisao lida)."""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(H)
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
pr = os.path.join(P, "PREPARACAO_v412_PRONTA.json"); en = os.path.join(P, "ENSAIO_RESULTADO_v412.json")
d = json.load(open(pr, encoding="utf-8")); c = d["candidato"]; k = d["kernel"]; g = d["guarda_de_frases"]; e = d["ensaio_a_seco"]
texto = ("Etapa 2 da v412 fechada pelo construtor (contrato R4, sha16 %s): candidato %s (%s bytes; base v411 %s) gerado e NAO instalado; kernel da setima lista (%s modulos) no sandbox, TOTAL decl %s thm %s fora do trio %s, escada %s -> %s; "
         "quatro registros por especificacao; guarda de frases pela travessia: controles %s de %s, %s superficies, %s unidades, todas limpas; ensaio a seco: %s (%s de %s checagens de unidade); portao do pilar no candidato: %s. "
         "Nao feito: bateria pre-selo e scripts de rito/custodia. Rito nao rodou.") % (d["contrato_seguido"]["sha16"], c["sha16"], c["bytes"], c["base_v411_sha16"], k["n_modulos"], k["linha_TOTAL"]["decl"], k["linha_TOTAL"]["thm"], k["linha_TOTAL"]["fora_do_trio"],
                                                                                  d["escada"]["antes_v411"], d["escada"]["depois_candidato"], g["controles"]["n_ok"], g["controles"]["n"], g["travessia"]["n_superficies"], g["travessia"]["n_unidades_total"], e["veredito"], e["n_ok"], e["n_checagens_unidade"],
                                                                                  d["portao_do_pilar_no_candidato"]["ok"])
out = {"event_id": "construtor-v412-etapa2-candidato-r4-17nov",
       "changes": {"records": [{"id": "construtor-v412-etapa2", "kind": "fact", "statute": "REAL", "text": texto,
                                "sources": [{"kind": "artifact", "ref": pr.replace("\\", "/") + "#sha256:" + sha(pr)}, {"kind": "artifact", "ref": en.replace("\\", "/") + "#sha256:" + sha(en)}]}],
                   "flow": {"phase": "preparacao_v412__etapa2_candidato_pronto__parado", "next_action": "gerencia: revisao de terceiro do candidato; decidir os pontos do fecho; adaptar rito e custodia; rito depois da aprovacao"}}}
op = os.path.join(H, "transicao_etapa2.json")
open(op, "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
print(op, "sha16", sha(op)[:16])
