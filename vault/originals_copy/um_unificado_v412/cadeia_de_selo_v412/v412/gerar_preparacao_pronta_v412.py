# -*- coding: utf-8 -*-
"""gerar_preparacao_pronta_v412.py -- (claude-construtor-v412, Etapa 2, contrato R4) o FECHO do candidato: PREPARACAO_v412_PRONTA.json (o nome que o molde da v411 da ao 'candidato pronto para a revisao'). Tudo LIDO dos artefatos por script
(sha16, numeros, resultados); a prosa so' no que e' dito como pendencia, desvio ou decisao. Nao instala, nao roda o rito."""
import datetime, glob, hashlib, json, os, re, sys
from pathlib import Path
sys.path.insert(0, r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
sys.stdout.reconfigure(encoding="utf-8")
from e2_lib_v412 import D, ler_json, salvar_json, sha16_arq

K = D / "kernel"
j = lambda p: ler_json(p) if Path(p).exists() else None
s16 = lambda p: sha16_arq(p) if Path(p).exists() else None
cand = j(D / "CANDIDATO_v412.json")
pos = j(K / "POS_BUILD_v412.json")
fl = j(K / "FLAGS_v412.json")
ant = j(D / "PRONTO_PARA_CANDIDATO_v412_R3.json")
ens = j(D / "ENSAIO_RESULTADO_v412.json")
gf = j(D / "GUARDA_FRASES_v412.json")
gu = j(D / "GUARDA_v412_UNIDADES.json")
pil = j(D / "PORTAO_DO_PILAR_CANDIDATO_v412.json")
priv = j(D / "GUARDA_MATERIAL_PRIVADO_v412.json")
reg = j(D / "REGISTROS_v412_RECIBO.json")
anc = j(D / "ANCORAS_ESCOLHIDAS_v412.json")
nos = j(K / "NOS_INTACTO_C4_v412.json")
setima = j(K / "SETIMA_LISTA_CONFERIDA_v412.json")
builtc = j(K / "BUILT_CHECAGEM_CORRIGIDA_R4_v412.json")
man = j(D / "insumos" / "MANIFESTO_PEDRAS_v412_R7.json")
pilar_ok = pil and pil.get("ok")
r3_tot = (ant or {}).get("kernel_k412c", {}).get("linha_TOTAL")
pos_tot = (pos or {}).get("linha_TOTAL")
n_por_mod = (fl or {}).get("n_por_modulo", {})
novos = {m: n_por_mod.get("TGLExt." + m) for m in ("Token2", "AMaquina")}
fecho = {
    "contrato": "PREPARACAO_v412_PRONTA", "quando": datetime.datetime.now().isoformat(timespec="seconds"), "agente": "claude-construtor-v412 (Etapa 2), a servico da gerencia c1",
    "estado": "CANDIDATO GERADO E ENSAIADO A SECO, NAO INSTALADO, RITO NAO RODADO; para aqui, para a revisao de terceiro e as decisoes da gerencia",
    "contrato_seguido": {"arquivo": "CONTRATO_v412_R4.md", "sha16": s16(D / "CONTRATO_v412_R4.md"), "copia_congelada_igual": hashlib.sha256((D / "CONTRATO_v412_R4.md").read_bytes()).hexdigest() == hashlib.sha256((D / "contrato_REV4" / "CONTRATO_v412_R4.md").read_bytes()).hexdigest()},
    "candidato": {"arquivo": "um_v412_candidato.py", "caminho": str(D / "um_v412_candidato.py"), "sha16": (cand or {}).get("sha16"), "bytes": (cand or {}).get("bytes"), "base_v411_sha16": (cand or {}).get("base_v411_sha16"), "manifesto": "CANDIDATO_v412.json",
                  "manifesto_sha16": s16(D / "CANDIDATO_v412.json"), "n_patches": (cand or {}).get("n_patches"), "patches": [p["id"] for p in (cand or {}).get("patches", []) if not p["id"].startswith("C12_expected")], "n_literais_expected_ladder": (cand or {}).get("expected_ladder_literais")},
    "escada": {"antes_v411": (cand or {}).get("escada", [None, None])[0], "depois_candidato": (cand or {}).get("escada", [None, None])[1], "bandeiras_novas": (cand or {}).get("n_bandeiras"), "kernel_medido": (pos or {}).get("escada"), "igual": ((cand or {}).get("escada") == (pos or {}).get("escada"))},
    "kernel": {"sandbox": "C:\\t\\k412c\\final", "n_modulos": (man or {}).get("n_modulos"), "lista": "setima (insumos\\MANIFESTO_PEDRAS_v412_R7.json)", "manifesto_sha16": s16(D / "insumos" / "MANIFESTO_PEDRAS_v412_R7.json"), "setima_lista_conferida": {"ok": (setima or {}).get("ok"), "resumo": (setima or {}).get("resumo")},
               "pos_build_ok": (pos or {}).get("ok"), "linha_TOTAL": pos_tot, "linha_TOTAL_v411": (pos or {}).get("linha_TOTAL_v411"), "delta_vs_v411": (pos or {}).get("delta_vs_v411"), "linha_TOTAL_quinta_lista_R3": r3_tot,
               "delta_vs_quinta_lista": ({"decl": pos_tot["decl"] - r3_tot["decl"], "thm": pos_tot["thm"] - r3_tot["thm"]} if (pos_tot and r3_tot) else None), "declaracoes_dos_dois_modulos_novos": novos,
               "fora_do_trio": (pos_tot or {}).get("fora_do_trio"), "avisos_fora_o_conhecido": (pos or {}).get("avisos_por_modulo") and {m: v.get("n") for m, v in pos["avisos_por_modulo"].items() if v.get("n") and m != "TGLExt.TowerWedgeIndex"},
               "chaves_antigas_mudam": ((pos or {}).get("chaves_antigas") or {}).get("mudam"), "checagem_built_corrigida": {"ok": (builtc or {}).get("ok"), "n_exigidos_examinados": (builtc or {}).get("n_exigidos_examinados")},
               "nos_intacto": {"ok": bool(nos) and not nos.get("conteudo", nos).get("falhas", ["?"]) if nos else None, "um_py_sha16": (nos or {}).get("conteudo", nos or {}).get("um_py_sha16")}},
    "registros": {"nomes": (cand or {}).get("registros"), "recibo": "REGISTROS_v412_RECIBO.json", "recibo_ok": (reg or {}).get("ok"), "por_registro": (reg or {}).get("registros"), "n_ancoras_total": (anc or {}).get("n_ancoras_total"),
                  "ancoras_escolhidas": {"recibo": "ANCORAS_ESCOLHIDAS_v412.json", "sha16": s16(D / "ANCORAS_ESCOLHIDAS_v412.json"), "n_por_registro": {r: v["n_ancoras"] for r, v in (anc or {}).get("registros", {}).items()}}},
    "guarda_de_frases": {"controles": {"n": (gf or {}).get("n_controles"), "n_ok": (gf or {}).get("n_ok"), "numerados": (gf or {}).get("controles_numerados")}, "recibo_controles": "GUARDA_FRASES_v412.json", "fonte_sha16": s16(D / "runtime_v412_guarda.py"),
                         "travessia": {"recibo": "GUARDA_v412_UNIDADES.json", "ok": (gu or {}).get("ok"), "n_superficies": (gu or {}).get("n_superficies"), "n_unidades_total": (gu or {}).get("n_unidades_total"),
                                       "n_unidades_com_p_igual_np_ou_fluidos": len((gu or {}).get("unidades_com_p_igual_np_ou_fluidos", []))},
                         "verificador_de_historia": (gu or {}).get("historia"), "formas_da_F43_nos_textos_emitidos": (gu or {}).get("f43", {}).get("achados"), "marcadores_herdados": {k: v for k, v in ((gu or {}).get("marcadores_herdados") or {}).items() if k in ("n", "diferem")}},
    "portao_do_pilar_no_candidato": {"ok": pilar_ok, "resumo": (pil or {}).get("resumo"), "recibo": "PORTAO_DO_PILAR_CANDIDATO_v412.json", "n_nomes_do_fecho": (pil or {}).get("n_nomes_do_fecho"), "falta_antes_do_rito": (pil or {}).get("falta_antes_do_rito")},
    "guarda_de_material_privado": {"limpo": (priv or {}).get("limpo"), "n_arquivos": (priv or {}).get("n_arquivos"), "com_material_privado": (priv or {}).get("com_material_privado"), "recibo": "GUARDA_MATERIAL_PRIVADO_v412.json"},
    "ensaio_a_seco": ens and {"veredito": ens["real"].get("veredito"), "rc": (ens["real"].get("saida") or {}).get("rc"), "n_checagens_unidade": ens["real"].get("n_checagens_unidade"), "n_ok": ens["real"].get("n_ok"), "n_falhas": ens["real"].get("n_falhas"),
                              "candidato_sha16": ens["real"].get("sha16_do_candidato"), "escada": ens["real"].get("escada"), "chaves_novas_no_core": ens["real"].get("chaves_novas_no_core"), "componentes": ens["real"].get("componentes"),
                              "examinou": {k: v for k, v in (ens["real"].get("v412_examinou") or {}).items() if k != "guarda_de_frases"}} or None,
    "ensaio_a_seco_arquivo": "ENSAIO_RESULTADO_v412.json", "ensaio_sha16": s16(D / "ENSAIO_RESULTADO_v412.json"),
    "verbatim_congelado": {"arquivo": "VERBATIM_CONGELADO_v412.json", "sha16": s16(D / "VERBATIM_CONGELADO_v412.json"), "n": (j(D / "VERBATIM_CONGELADO_v412.json") or {}).get("n")},
    "resumo_troca_de_pnp": (cand or {}).get("resumo_troca_de_pnp"),
    "decisoes_e_pontos_para_a_gerencia": [
        "patch de DADO no literal 'escada' de _V411_H0DN_CONTRACT (baseline), junto dos 30 literais 'expected_ladder': sem ele o registro herdado h0dn_bg1_v411 (funcao selada, c15) recusa porque a escada do rito deixou de ser 12308 (achado do ensaio a seco; com o patch, 500/500)",
        "o contrato nao tem kh_n1_cobertura_v412: a arvore nova do kernel nao tem pino exato (kh_n1_cobertura_v411 virou piso nos checks h2/h3/h6/h8; cunhagens_v411 u6 virou piso e u44 pina a raiz nova); o ensaio cobra as entradas do hash formal por conta propria",
        "os ids r1, r2, r3 do registro cunhagens_v412 (checagens do selo dos tres outros registros) casam o padrao de numero de revisao do verificador de historia; sao identificadores de checagem, nao prosa; renomear exige regerar o candidato e repetir o ensaio",
        "o resumo: _V411_TOPO e _v411_topo_texto ficam como estao; a v412 tem _V412_TOPO e _v412_topo_texto (copia por AST com o paragrafo de P = nP passando pela travessia); o paragrafo novo vem da pagina R13",
        "ancoras: regra do contrato operacionalizada em ANCORAS_ESCOLHIDAS_v412.json (estrela; pagina; cabecalho; recuo pelos #print axioms da fonte para os modulos sem estrela, pagina nem cabecalho): a gerencia confere o recibo",
        "a pagina REV14 apareceu na pasta depois do R4 congelado; esta entrega segue o R4 e a R13",
        "VERBATIM_CONGELADO_v412.json (artefato da cadeia, fora do programa; lista nomes, tamanhos e sha256 dos arquivos OPERADOR_13nov a 17nov): a guarda de material privado acha 2 ocorrencias de marcador privado NOS NOMES de arquivos; por isso ele nao entra na varredura dos insumos pinados (nao e' insumo do candidato) e nao deve ser publicado ou copiado para fora da casa sem copia limpa",
    ],
    "nao_feito_ou_pendente": [
        "bateria pre-selo (B(n) da Bancada) e os scripts da cadeia de rito, instalacao, custodia e pos_rito seguem marcados [A ADAPTAR v412] e NAO foram adaptados nem rodados (a Bancada so' seria lida por GET); os blocos de texto do README, do estado atual e do handoff foram montados como artefato (BLOCOS_TEXTO_PUBLICO_v412.json) e passaram pela travessia, mas os scripts pos_rito que os emitem apos o rito nao foram adaptados",
        "portao do pilar antes do rito: conferir que o ambiente da placa e' o do cache (ato da gerencia; ha treino em curso, que nao foi tocado)",
        "a revisao de terceiro, o congelamento da pagina final, a palavra do autor, a tarefa agendada, o rito e a custodia sao da gerencia",
    ],
    "refeito_por_causa_do_R2_R3_R4": [
        "R2: guarda de frases refeita (a travessia, a unidade, as duas obrigacoes herdadas pelo nome inteiro, a regra dos fluidos por frase com formas em ingles, 21 controles com recibo); checagem da guarda em cada registro; cunhagens sem falas; resumo versionado; 34 marcadores herdados conferidos por bytes",
        "R3: sexta lista e novos modulos (Token2, AMaquina): sandbox levado a 42 modulos, medicoes refeitas, ancoras, registros (15 modulos na frente A), gerador, candidato (o R1 guardado), ensaio a seco e portoes refeitos; pagina R11 na secao do artigo, no resumo e nos blocos",
        "R4: setima lista (so' o cabecalho de Token2 mudou), palavras de veredito do R4, pagina R13 (traducao EN refeita), a tese da tautologia fora de todo texto novo (so' a negacao dela, que a pagina traz)",
    ],
    "texto_publico": {"pagina_pt": "o_que_fica_claro_REV13/O_QUE_FICA_CLARO_v412_R13.md", "pagina_pt_sha16": s16(D / "o_que_fica_claro_REV13" / "O_QUE_FICA_CLARO_v412_R13.md"), "traducao_en": "O_QUE_FICA_CLARO_v412_R13_EN.md", "traducao_en_sha16": s16(D / "O_QUE_FICA_CLARO_v412_R13_EN.md"),
                      "secao_do_artigo": "TEXTO_PUBLICO_v412.json", "secao_sha16": s16(D / "TEXTO_PUBLICO_v412.json"), "blocos": "BLOCOS_TEXTO_PUBLICO_v412.json", "blocos_sha16": s16(D / "BLOCOS_TEXTO_PUBLICO_v412.json")},
    "estatuto": "[REAL] medido no sandbox C:\\t\\k412c\\final e nos recibos desta pasta; nada instalado no Nos; o rito nao rodou; validade no kernel nao e' creditacao; o gate nao se move",
}
salvar_json(D / "PREPARACAO_v412_PRONTA.json", fecho)
print("gravado PREPARACAO_v412_PRONTA.json", s16(D / "PREPARACAO_v412_PRONTA.json"))
