# -*- coding: utf-8 -*-
"""Etapa 2 da v413: o conflito da pagina pinada com a guarda herdada, medido, e a PROPOSTA de uma pagina R1 (nao e' a pagina do contrato; so' a gerencia a adota, por contrato R2).
O conflito: a primeira frase do bloco de citacao da secao 2 da pagina pinada traz, no MESMO trecho, “P = nP” e “Turing”, sem o qualificador relativo ao leitor nem negacao/limite; a obrigacao LOCAL F37b da guarda herdada
(_v409_guarda_frases, que a _v412_guarda_frases herda e que o contrato da v412 manteve: “a obrigacao local da v409, F37b, NAO sai”) a recusa. A guarda nao se relaxa e a pagina nao se edita aqui.
A proposta: UMA troca de pontuacao na pagina (“, e a v413 o escreve” -> “. A v413 o escreve”), que poe “P = nP” e “Turing” em trechos diferentes, sem mudar palavra de conteudo; na traducao EN, a mesma troca.
Este script: (1) mede o conflito com a guarda selada (a funcao, a linha no um.py selado, o que ela exige); (2) grava proposta_pagina_R1\\ com a pagina e a traducao propostas (troca de texto exato, contagem 1);
(3) confere que a guarda passa sobre a unidade da proposta; (4) grava PROPOSTA_PAGINA_R1_v413.json."""
import difflib, json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_lib_v413 as L
import base_um_v412 as B

NS = B.carregar(["_v412_guarda_frases"])
B.chamar_resolvendo(NS, "_v412_guarda_frases", "aquecimento")
g12 = NS["_v412_guarda_frases"]
T = B.texto()
linha_f37b = [i + 1 for i, l in enumerate(T.split("\n")) if '"F37b_p_igual_np_e_turing_juntos_sem_o_qualificador_no_mesmo_trecho"' in l]
linha_def_v409 = [i + 1 for i, l in enumerate(T.split("\n")) if l.startswith("def _v409_guarda_frases(")]
TROCAS = {"pt": ("nas classes do seu dicionário, e a v413 o escreve", "nas classes do seu dicionário. A v413 o escreve"),
          "en": ("in the classes of its dictionary, and v413 writes it", "in the classes of its dictionary. Version v413 writes it")}
ORIG = {"pt": L.PAGINA_CONTRATO, "en": L.D / (L.PAGINA_CONTRATO.stem + "_EN.md")}
DEST = {"pt": L.PROPOSTA_DIR / "O_QUE_FICA_CLARO_v413_R1_PROPOSTA.md", "en": L.PROPOSTA_DIR / "O_QUE_FICA_CLARO_v413_R1_PROPOSTA_EN.md"}
import registros_v413 as RG   # (o desembrulhador da pagina; com o modo contrato, a pagina do contrato)

rec = {"o_que_e": __doc__.split("Este script:")[0].strip(), "pagina_do_contrato": {"arquivo": str(L.PAGINA_CONTRATO.relative_to(L.D)), "sha16": L.sha16_arq(L.PAGINA_CONTRATO)},
       "guarda": {"funcao": "_v412_guarda_frases -> _v409_guarda_frases (F37b)", "um_py_selado_sha16": L.sha16_arq(L.D / "base_v412" / "um.py"), "linha_da_regra_F37b_no_um_py_selado_LF": linha_f37b,
                  "linha_do_def_v409_guarda_frases": linha_def_v409,
                  "o_que_exige": "no MESMO trecho (o texto partido por . ; | quebra de linha aspas), onde aparecem “P = nP” e “Turing”, o qualificador “relativo ao leitor” (EN “relative to the reader”) ou uma negacao/limite (“ não ”, “ nunca ”, “ nem ”, “ fica fora”, EN “ not ”, “ never ”, “ stays outside”, “n't”)",
                  "o_que_nao_se_faz": "a guarda nao se relaxa; a pagina pinada nao se edita; nenhuma palavra de conteudo se inventa"}, "linguas": {}}
ok = True
for lg in ("pt", "en"):
    src = ORIG[lg].read_bytes().decode("utf-8")
    velho, novo = TROCAS[lg]
    c = src.count(velho)
    assert c == 1, ("a troca proposta nao casa uma vez", lg, c)
    prop = src.replace(velho, novo)
    q_orig = re.findall(r"^> (.+)$", RG.desembrulhar(src), re.M)
    q_prop = re.findall(r"^> (.+)$", RG.desembrulhar(prop), re.M)
    assert len(q_orig) == 1 and len(q_prop) == 1
    v_o = [x[0] for x in g12(q_orig[0])]
    v_p = [x[0] for x in g12(q_prop[0])]
    L.salvar_bytes(DEST[lg], prop.encode("utf-8"))
    diff = list(difflib.unified_diff(src.splitlines(), prop.splitlines(), lineterm="", n=0))
    rec["linguas"][lg] = {"original": str(ORIG[lg].relative_to(L.D)), "original_sha16": L.sha16_arq(ORIG[lg]), "proposta": str(DEST[lg].relative_to(L.D)), "proposta_sha16": L.sha16_arq(DEST[lg]),
                          "troca": {"velho": velho, "novo": novo, "ocorrencias": c}, "diff": diff, "guarda_no_paragrafo_original": v_o, "guarda_no_paragrafo_proposto": v_p}
    ok = ok and bool(v_o) and not v_p
rec["conflito_medido"] = all(rec["linguas"][lg]["guarda_no_paragrafo_original"] for lg in ("pt", "en"))
rec["proposta_passa_na_guarda"] = all(not rec["linguas"][lg]["guarda_no_paragrafo_proposto"] for lg in ("pt", "en"))
rec["estatuto"] = "PROPOSTA: nao e' a pagina do contrato; adota-la e' ato da gerencia (pagina R1 e contrato R2); o modo proposta da cadeia (V413_PAGINA_PROPOSTA=1) a usa so' para exercitar o candidato ate' o fim"
L.salvar_json(L.D / "PROPOSTA_PAGINA_R1_v413.json", rec)
print(json.dumps({lg: {"original": rec["linguas"][lg]["guarda_no_paragrafo_original"], "proposta": rec["linguas"][lg]["guarda_no_paragrafo_proposto"]} for lg in ("pt", "en")}, ensure_ascii=False))
print("linha da F37b no um.py selado:", linha_f37b, "| conflito medido:", rec["conflito_medido"], "| proposta passa:", rec["proposta_passa_na_guarda"])
sys.exit(0 if ok else 1)
