# -*- coding: utf-8 -*-
# [DERIVADO v413, claude-construtor-v413] no molde de v412\gerar_preparacao_pronta_v412_r7.py (que fica intacto): o fecho da Etapa 2 da v413.
"""gerar_preparacao_pronta_v413.py -- o FECHO da Etapa 2 da v413 (do contrato ao candidato), pelo contrato congelado vigente (R2): le TODOS os recibos da etapa por arquivo (sha16 lido dos bytes), confere cada um
(cada checagem diz quantos itens examinou; zero e' falha), e grava PREPARACAO_v413_PRONTA.json (por temporario e troca, backup de bytes do anterior). Nada instala, nada roda o rito, nada toca o Nos.
O que segura o candidato (fechou False) e o que segura so' o selo (pendencia de decisao do autor ou da gerencia) ficam ditos em campos separados."""
import datetime, json, os, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_lib_v413 as L
import delta_v413 as DL

D = L.D
e = L.Exame("fecho_etapa2_v413")
R = lambda nome: L.ler_json(D / nome) if (D / nome).exists() else None
arq = lambda p: {"arquivo": str(Path(p).relative_to(D)) if str(p).startswith(str(D)) else str(p), "sha16": L.sha16_arq(p), "bytes": Path(p).stat().st_size} if Path(p).exists() else {"arquivo": str(p), "ausente": True}
assert L.MODO == "contrato", "o fecho e' do modo contrato"
# 1. os pinos de entrada (contrato R2 e a pagina R1; os insumos herdados)
ce = R("CONFERENCIA_ENTRADA_R2_ETAPA2_v413.json")
e.chk("os pinos do contrato R2 conferem (o contrato, a copia congelada, a pagina R1, o fecho da Etapa 1, o manifesto, as ancoras, o inventario)", bool(ce and ce["ok"]), len((ce or {}).get("linhas") or []), [x["arquivo"] for x in (ce or {}).get("linhas", []) if not x["ok"]])
pr = R("PRONTO_PARA_CANDIDATO_v413.json")
e.chk("a Etapa 1 fechou (o kernel dos 21 modulos e do modulo corrigido, a frio no k413c, todas as declaracoes no trio)", bool(pr and pr["etapa_1_fechou"] and pr["kernel_k413c"]["todas_no_trio"] and not pr["kernel_k413c"]["falhas"]), len((pr or {}).get("checagens") or []))
dc = R("DELTA_v413_CONFERIDO.json")
e.chk("o delta da v413 confere (versao, base, bundle, modulo corrigido, bandeiras, escada, registros, B(n) lido do delta do B(n), sandbox curto proprio)", bool(dc and dc["resumo"]["ok"]), (dc or {}).get("resumo", {}).get("n_checagens", 0))
# 2. registros, ancoras, verbatim
an = R("ANCORAS_ESCOLHIDAS_v413.json")
e.chk("as ancoras escolhidas pela regra do contrato: nenhum problema; nenhuma sem nome no relatorio de axiomas", bool(an and not an["problemas"] and an["ancoras_sem_nome_no_relatorio_de_axiomas"] == 0), (an or {}).get("n_ancoras_total", 0), (an or {}).get("problemas"))
rg = R("REGISTROS_v413_RECIBO.json")
e.chk("os seis registros (os cinco do contrato e o kh_n1_cobertura_v413): recibo verde", bool(rg and rg["ok"]), (rg or {}).get("resumo", {}).get("n_checagens", 0))
vb = R("VERBATIM_CONGELADO_v413.json")
e.chk("VERBATIM_CONGELADO_v413.json: as falas de 19 e 20/11 listadas por tamanho e sha256 (fora do programa)", bool(vb and vb["n"] > 0 and len(vb["arquivos"]) == vb["n"]), (vb or {}).get("n", 0))
# 3. a guarda, o texto publico, os marcadores
gf = R("GUARDA_FRASES_v413.json")
e.chk("a guarda herdada da v412: os controles herdados rodados contra as funcoes do um.py selado, iguais ao recibo da v412; os controles de P = nP sobre a pagina da v413", bool(gf and gf["ok"]),
      ((gf or {}).get("controles_herdados") or {}).get("n", 0) + ((gf or {}).get("controles_da_pagina_v413") or {}).get("n", 0))
gu = R("GUARDA_v413_UNIDADES.json")
e.chk("a travessia da guarda herdada (inteira, inclusive a F37b) sobre todos os textos novos, PT e EN: zero violacao; F43, premio, tautologia e historia limpos", bool(gu and gu["ok"]), (gu or {}).get("n_unidades_total", 0))
gp = R("GUARDA_v413_P_IGUAL_NP.json")
e.chk("o recibo das unidades com P = nP: todas limpas, cada uma com as duas marcas", bool(gp and gp["n_unidades"] > 0 and gp["n_limpas"] == gp["n_unidades"] and all(all(u["marcas"].values()) for u in gp["unidades"])), (gp or {}).get("n_unidades", 0))
tp = R("TEXTO_PUBLICO_v413.json"); tpl = R("TEXTO_PUBLICO_PDFLATEX_v413.json")
e.chk("a secao do artigo PT/EN montada da pagina R1 (a mesma estrutura, os mesmos termos entre crases, a travessia limpa) e compilada isolada com pdflatex", bool(tp and tp["fonte_pt"]["e_a_pagina_do_contrato"] and tp["estrutura_igual_nas_duas_linguas"] and tp["termos_iguais_nas_duas_linguas"]
      and all(v["ok"] for v in tp["travessia"].values()) and tpl and tpl["ok"]), (tp or {}).get("n_blocos", 0))
mh = R("MARCADORES_HERDADOS_v413.json")
e.chk("os marcadores herdados que a custodia exige: os 34, com o corpo do handoff selado da v412", bool(mh and mh["ok"] and mh["n_marcadores"] == 34), (mh or {}).get("n_marcadores", 0))
# 4. o candidato
cm = L.ler_json(DL.MANIFESTO_ARQ) if os.path.exists(DL.MANIFESTO_ARQ) else None
cand_ok = bool(cm and os.path.exists(DL.CANDIDATO_ARQ) and L.sha256_arq(DL.CANDIDATO_ARQ) == cm["sha256"] and os.path.getsize(DL.CANDIDATO_ARQ) == cm["bytes"] and cm["modo"] == "contrato" and cm["pagina"]["e_a_pagina_do_contrato"])
e.chk("o candidato em disco (fora de work\\) e' o do manifesto CANDIDATO_v413.json, gerado no modo contrato com a pagina do contrato", cand_ok, 1, [cm and cm.get("sha16"), DL.CANDIDATO_ARQ])
fj = L.ler_json(L.KD / "FLAGS_v413.json")
e.chk("a escada do candidato e' a medida no kernel (FLAGS_v413.json) e as bandeiras novas sao as 712", bool(cm and cm["escada"] == fj["escada"] and cm["n_bandeiras"] == fj["n_flags"] == len(fj["flags"])), 1, [cm and cm.get("escada"), fj["escada"]])
e.chk("o candidato traz o modulo corrigido SUBSTITUIDO (sha256 antes -> depois) e o par _V413_FONTES / _V413_VERBATINS2", bool(cm and cm["kernel"]["modulo_corrigido"]["substituido_no_dicionario_embutido"] and "K02_modulo_corrigido" in [p["id"] for p in cm["patches"]]), 1)
pp = R("PORTAO_DO_PILAR_CANDIDATO_v413.json")
e.chk("o portao do pilar no candidato: o fecho da chave do cache intocado (sha256 de cada nome igual ao do um.py selado)", bool(pp and pp["ok"] and pp["candidato"]["sha16"] == (cm or {}).get("sha16")), (pp or {}).get("n_nomes_do_fecho", 0))
en = R("ENSAIO_RESULTADO_v413.json")
e.chk("o ensaio a seco sobre ESTE candidato: tudo passou", bool(en and en.get("veredito") == "TUDO PASSOU" and en.get("candidato_sha16") == (cm or {}).get("sha16")), (en or {}).get("n_checagens_unidade", 0), (en or {}).get("veredito"))
gm = R("GUARDA_MATERIAL_PRIVADO_v413.json")
_expl = ((gm or {}).get("analise_por_nome_de_modulo") or {}).get("nomes_de_modulo_que_a_guarda_acusa") or {}
_so_nome = bool(gm and gm["com_material_privado"] and _expl and all(not v["arquivos_com_outro_acerto"] and v["arquivos_explicados_so_por_ele"] == len(gm["com_material_privado"]) for v in _expl.values()))
e.chk("a guarda de material privado (a da E03 da G1) rodou sobre os insumos pinados; limpo, ou todo acerto se explica so' por um nome de modulo desta versao (decisao do autor antes do selo)", bool(gm and (gm["limpo"] or _so_nome) and not gm["ilegiveis"]), (gm or {}).get("n_arquivos", 0),
      {"limpo": (gm or {}).get("limpo"), "n_com_acerto": len((gm or {}).get("com_material_privado") or []), "explicado_por": sorted(_expl)})
# (revisao de terceiro do candidato anterior) o recibo KH_N1 que o registro kh_n1_cobertura_v413 pina por sha256 nao foi regravado desde a revisao (B6): o sha16 lido do arquivo e' o que a revisao leu
REV_P = D / "revisao_candidato" / "REVISAO_CANDIDATO_v413.md"
REV_T = REV_P.read_bytes().decode("utf-8") if REV_P.exists() else ""
_kh_rev = re.search(r"KH_N1_v413\.json` com sha256 `([0-9a-f]{16})…`", REV_T)
e.chk("(revisao B6) kernel\\KH_N1_v413.json nao foi regravado: o sha16 lido do arquivo e' o que a revisao de terceiro leu, e o candidato o pina", bool(_kh_rev and L.sha16_arq(L.KH_N1_V413) == _kh_rev.group(1)), 1,
      [L.sha16_arq(L.KH_N1_V413), _kh_rev and _kh_rev.group(1)])


def _revisao():
    m_v = re.search(r"## Veredito: \*\*([A-Z_]+)\*\*", REV_T); m_c = re.search(r"sha256 `([0-9a-f]{16})…`", REV_T)
    return {"arquivo": arq(REV_P), "veredito": m_v and m_v.group(1), "candidato_revisado_sha16": m_c and m_c.group(1), "o_que_se_fez_com_cada_achado": {
        "M1": "nao_diz reescrito como o que NAO se afirma em todos os registros (os itens da creditacao e do numero novo da natureza; o recibo dos registros confere cada item); os registros so' tem texto em portugues; "
              "a secao 7 do artigo e o bloco nao_diz (PT/EN) sao prosa da pagina, com a polaridade certa, e ficam",
        "M2": "pendente: a decisao do autor sobre o termo privado, antes de instalar e rodar; o nome nao se renomeia; as formas exatas ficam no recibo da guarda privada e nas pendencias",
        "B1": "seis registros por especificacao (os cinco do contrato e a cobertura do relatorio de axiomas) no comentario da versao, no cabecalho do bloco v413, na docstring de _v413_rodar_specs (o cunhagens cobra o selo dos quatro registros com ancora) e no main",
        "B2": "chega a 2 ou mais / reaches 2 or more na secao do artigo e nos blocos, por ajuste com contagem exata sobre o texto lido (ajustes_revisao_v413.py); os arquivos da pagina e da traducao ficam intactos",
        "B3": "no registro da ponte: a hipotese da inclinacao m acima de ln 2/β no item da classe de uma leitura; (registros da v409/v412) no item de P = nP",
        "B4": "o extrator das entradas de cunhagens_v413 ignora nome de uma letra entre crases",
        "B5": "no manifesto: funcoes_identicas_a_base_salvo_literais_de_escada, com os literais de dado que mudam listados (patch e nome de topo)",
        "B6": "kernel\\KH_N1_v413.json intocado (checagem acima); a pre-condicao de sha256 no rito e' da Etapa 3",
        "B7": "redacao do contrato, da gerencia; o candidato nao muda",
        "B8": "sem defeito; fica dito",
        "B9": "o bloco entrega do handoff deixa de trazer a contagem da pasta da cadeia (quem montar o handoff conta na hora)",
        "B10": "nota no bloco entrega do handoff: as bandeiras ext_operador_413_* levam o nome do modulo Operador (o operador de consciencia)"}}


ok_cand = e.ok
pend_selo = []
if gm and not gm["limpo"]:
    _formas = sorted({f_ for v_ in _expl.values() for f_ in (v_.get("formas_que_a_guarda_acusa_sozinhas") or [])})   # so' as formas que a guarda acusa sozinhas (as outras caixas nao contam)
    pend_selo.append({"o_que": "a guarda de material privado da G1 (E03) acusa o nome de modulo %s nos insumos e no texto da v413 (todos os %d arquivos acusados se explicam so' por ele; contagem sem padrao); as formas exatas: %s"
                      % (", ".join(sorted(_expl)), len(gm["com_material_privado"]), ", ".join(_formas)),
                      "formas_exatas_do_nome": _formas,
                      "decisao": "do autor, ANTES de instalar e rodar o rito (revisao de terceiro, M2: o selo e' gravado pelo proprio rito, e renomear depois perderia o rito): isentar o termo, com a fala dele por bytes nomeando as formas exatas (TERMO_PRIVADO_ISENTO_v413.json), ou mudar o nome (o contrato proibe renomear sem a palavra dele; o construtor nao renomeia)",
                      "segura": "a instalacao, o rito, o selo e a publicacao; nao a revisao de terceiro",
                      "contagem_sobre_o_candidato": "[DECLARADO pela revisao de terceiro, nao refeito aqui] a revisao contou a guarda da G1 sobre o candidato anterior contra o um.py v412 (revisao_candidato\\r14_guarda_privada.py, so' numeros): com as duas formas isentas, os acertos do candidato igualam os da v412"})
out = {"contrato": "PREPARACAO_v413_PRONTA", "quando": datetime.datetime.now().isoformat(timespec="seconds"), "agente": "claude-construtor-v413 (Etapa 2 pelo contrato congelado), a servico da gerencia c1",
       "fechou": ok_cand, "estado": ("CANDIDATO REGERADO PELO CONTRATO R2 COM OS CONSERTOS DA REVISAO DE TERCEIRO DO CANDIDATO ANTERIOR (M1 e os BAIXOS que mudam texto) E ENSAIADO A SECO, NAO INSTALADO, RITO NAO RODADO; "
                                     "a decisao do autor sobre o termo privado (M2) segue pendente; a Etapa 3 NAO e' desta ordem" if ok_cand else "NAO FECHOU: ver checagens_do_fecho"),
       "revisao_de_terceiro": _revisao(),
       "checagens_do_fecho": e.linhas, "resumo_do_fecho": e.resumo(), "pendencias_antes_do_selo": pend_selo,
       "contrato_seguido": {"arquivo": L.CONTRATO.name, "sha16": L.sha16_arq(L.CONTRATO), "pagina": arq(L.PAGINA), "traducao_en": arq(L.PAGINA_EN)},
       "candidato": {"caminho": DL.CANDIDATO_ARQ, "sha16": (cm or {}).get("sha16"), "bytes": (cm or {}).get("bytes"), "manifesto": arq(DL.MANIFESTO_ARQ), "base_v412_sha16": (cm or {}).get("base_v412_sha16"), "n_patches": (cm or {}).get("n_patches"),
                     "patches": [p["id"] for p in (cm or {}).get("patches", []) if not p["id"].startswith("C12_")], "n_literais_expected_ladder": (cm or {}).get("expected_ladder_literais"), "escada": (cm or {}).get("escada"), "n_bandeiras": (cm or {}).get("n_bandeiras"),
                     "registros": (cm or {}).get("registros"), "modulo_corrigido": ((cm or {}).get("kernel") or {}).get("modulo_corrigido"), "gerador": arq(D / "gerar_candidato_v413.py")},
       "kernel": {"fecho_etapa_1": arq(D / "PRONTO_PARA_CANDIDATO_v413.json"), "linha_TOTAL": (pr or {}).get("kernel_k413c", {}).get("linha_TOTAL"), "linha_TOTAL_v412": (pr or {}).get("kernel_k413c", {}).get("linha_TOTAL_v412"),
                  "escada_de_bandeiras": fj["escada"], "n_bandeiras_novas": fj["n_flags"], "declaracoes_no_relatorio_de_axiomas": (pr or {}).get("kernel_k413c", {}).get("declaracoes_no_relatorio_de_axiomas")},
       "registros": {"recibo": arq(D / "REGISTROS_v413_RECIBO.json"), "n_ancoras_por_registro": {k: v["n_ancoras"] for k, v in ((rg or {}).get("registros") or {}).items()}, "n_checagens_por_registro": {k: v["n_checagens"] for k, v in ((rg or {}).get("registros") or {}).items()},
                     "n_ancoras_total": (rg or {}).get("n_ancoras_total"), "n_checagens_total": (rg or {}).get("n_checagens_total"), "ancoras_escolhidas": arq(D / "ANCORAS_ESCOLHIDAS_v413.json"), "modulos_sem_ancora": (an or {}).get("modulos_sem_ancora")},
       "guarda_de_frases": {"controles": arq(D / "GUARDA_FRASES_v413.json"), "controles_herdados": [((gf or {}).get("controles_herdados") or {}).get("n_ok"), ((gf or {}).get("controles_herdados") or {}).get("n")],
                            "controles_da_pagina_v413": [((gf or {}).get("controles_da_pagina_v413") or {}).get("n_ok"), ((gf or {}).get("controles_da_pagina_v413") or {}).get("n")], "unidades": arq(D / "GUARDA_v413_UNIDADES.json"),
                            "n_superficies": (gu or {}).get("n_superficies"), "n_unidades": (gu or {}).get("n_unidades_total"), "p_igual_np": arq(D / "GUARDA_v413_P_IGUAL_NP.json"), "n_unidades_com_p_igual_np": (gp or {}).get("n_unidades"),
                            "historia": ((gu or {}).get("historia") or {})},
       "texto_publico": {"secao": arq(D / "TEXTO_PUBLICO_v413.json"), "pdflatex": arq(D / "TEXTO_PUBLICO_PDFLATEX_v413.json"), "blocos": arq(D / "BLOCOS_TEXTO_PUBLICO_v413.json"), "marcadores_herdados": arq(D / "MARCADORES_HERDADOS_v413.json"),
                         "molde_dos_marcadores": arq(D / "MARCADORES_HERDADOS_PARA_O_HANDOFF_v413.md")},
       "verbatim_congelado": arq(D / "VERBATIM_CONGELADO_v413.json"), "portao_do_pilar_no_candidato": arq(D / "PORTAO_DO_PILAR_CANDIDATO_v413.json"),
       "guarda_de_material_privado": {"recibo": arq(D / "GUARDA_MATERIAL_PRIVADO_v413.json"), "limpo": (gm or {}).get("limpo"), "n_arquivos": (gm or {}).get("n_arquivos"), "n_com_acerto": len((gm or {}).get("com_material_privado") or []), "explicado_por_nome_de_modulo": sorted(_expl)},
       "ensaio_a_seco": {"recibo": arq(D / "ENSAIO_RESULTADO_v413.json"), "veredito": (en or {}).get("veredito"), "n_checagens_unidade": (en or {}).get("n_checagens_unidade"), "falhas": (en or {}).get("falhas_da_unidade")},
       "estado_em_disco": arq(L.ESTADO),
       "estatuto": "[REAL] medido no sandbox C:\\t\\k413c e nos recibos desta pasta; nada instalado no Nos; o rito nao rodou; validade no kernel nao e' creditacao; o gate nao se move"}
L.salvar_json(D / "PREPARACAO_v413_PRONTA.json", out)
print(json.dumps(e.resumo(), ensure_ascii=False), "| fechou:", ok_cand, "| pendencias antes do selo:", len(pend_selo))
for l in e.linhas:
    if not l["ok"]:
        print("FALHOU:", l["checagem"], "|", l["n_itens_examinados"], "|", str(l["detalhe"])[:300])
sys.exit(0 if ok_cand else 1)
