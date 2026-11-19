# -*- coding: utf-8 -*-
# [ADAPTADO v412, 17/11/2026, claude-construtor-v412-ensaio] a v412 nao tem fala: nenhuma citacao entre aspas angulares nos textos novos; os rotulos herdados vem da v410 (_ROTULOS) e da v411 (ROTULOS_V411), lidos dos ARQUIVOS; escopo do um.py = os textos que a v412 escreve; arquivo examinado e' contado
# [AUTORAL v411, 12/11/2026, claude-construtor-v411, a servico da gerencia c1] REESCRITO para a v411 (o corpo da v410 subido por rotulo fica em conferir_citacoes_v411.py.bak_*_corpo_v410_bump e em bump\)
"""conferir_citacoes_v412.py -- confere que TODA citacao entre « » nos textos NOVOS da v412 e' VERBATIM de uma fala do operador: as 9 falas de 11 e 12/11 (VERBATIM_CONGELADO_v412.json, lidas por bytes) ou, se a
citacao for de fala anterior ja' selada, as falas embutidas na v411 (v411\\insumos\\cunhagens, lidas por bytes). Regra da casa: «» so' para fala verbatim do operador; frase da gerencia vai entre “ ”. Os textos novos:
delta_v412, registros_h0dn_v412, registros_v411, runtime_h0dn_v411, quadro_v412, gerar_candidato_v412 (o bloco do main, a linha UM_VERSION), os pysnips/os textos do pos-rito quando existirem, a proposta do topo do DESENHO
(5.1 b, entre “ ”: nao e' fala) e, se existir, o TOPO_RATIFICADO_v412.json; com --candidato, tambem o bloco v412 do candidato (v412_pins.py). Nao corrige texto: aponta. Grava conferir_citacoes_v412.json; rc 1 se alguma
citacao nao for verbatim. uso: python -B -X utf8 conferir_citacoes_v412.py [--candidato]"""
import glob, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v412 as DL  # noqa: E402
FALAS = {f_["nome"]: f_["text"] for f_ in DL.FALAS_V412}
ANT = {}
for p_ in glob.glob(os.path.join(DL.V411, "insumos", "cunhagens", "*.txt")):
    ANT[os.path.basename(p_)] = open(p_, "rb").read().decode("utf-8", "replace")
for p_ in glob.glob(os.path.join(DL.CUN, "OPERADOR_*_verbatim.txt")):   # (o acervo das falas do operador, so' leitura: uma citacao antiga reconhecida e' verbatim de um arquivo dele)
    ANT.setdefault(os.path.basename(p_), open(p_, "rb").read().decode("utf-8", "replace"))
_nrm = lambda s_: " ".join(str(s_).replace("\r\n", "\n").split())
# (escopo b, ORDEM da gerencia c1 de 12/11: a regra (g) da v411, portada) so' os arquivos de TEXTO do pos-rito; testes e harnesses ficam FORA da varredura, como na v411
ARQS_POS_RITO = [os.path.join("pos_rito", n_) for n_ in ("textos_v412.py", "registrar_mapa_v412.py", "fechar_v412.py", "leitura_v412.py", "superficies_v412.py", "textos_custodia_handoff_v412.py", "blocos_custodia_v412.py", "textos_v412_novo.pysnip")]
ARQS = ["delta_v412.py", "registros_v412.py", "textos_registros_v412.py", "runtime_v412_guarda.py", "gerar_candidato_v412.py", "TEXTO_PUBLICO_v412.json", "TOPO_RATIFICADO_v412_DERIVADO.json"]   # (escopo a, o do um.py: ESTRITO, as falas da lista congelada e as ja' seladas)
if "--candidato" in sys.argv and os.path.exists(DL.PINS_ARQ):   # (pedido do fork B: os pinos DA RODADA -- no ensaio do topo proposto, os do artefato de ensaio)
    ARQS.append(DL.PINS_ARQ)
_MARCA = "[A ADAPTAR v" + "412]"
NAO_ADAPTADOS = [a_ for a_ in ARQS if os.path.exists(os.path.join(HERE, a_)) and _MARCA in open(os.path.join(HERE, a_), "rb").read().decode("utf-8", "replace")]
ARQS = [a_ for a_ in ARQS if a_ not in NAO_ADAPTADOS]   # (o corpo ainda e' o da v411, subido por rotulo: a citacao dele se confere quando o arquivo for adaptado; a lista vai dita no JSON)
out = {"contrato": "CONFERIR_CITACOES_v412", "n_falas_v412": len(FALAS), "n_falas_anteriores": len(ANT), "arquivos": {}, "nao_verbatim": [], "nao_conferidos_corpo_da_v411_a_adaptar": NAO_ADAPTADOS}
for a_ in ARQS:
    p_ = a_ if os.path.isabs(a_) else os.path.join(HERE, a_)
    if not os.path.exists(p_):
        continue
    t_ = open(p_, "rb").read().decode("utf-8", "replace")
    cits_ = re.findall(r"«([^«»]{3,})»", t_)
    rel_ = []
    for c_ in cits_:
        cn_ = _nrm(c_)
        de_ = [n_ for n_, f_ in FALAS.items() if cn_ in _nrm(f_)] or [n_ for n_, f_ in ANT.items() if cn_ in _nrm(f_)]
        rel_.append({"citacao": c_[:120], "verbatim_de": de_[:2], "ok": bool(de_)})
        if not de_:
            out["nao_verbatim"].append({"arquivo": a_, "citacao": c_[:200]})
    out["arquivos"][a_] = {"n_citacoes": len(cits_), "n_ok": sum(1 for r_ in rel_ if r_["ok"]), "citacoes": rel_}
_prop = re.findall(r"^> (?:PT|EN) — “(.+)”$", DL._S5, re.M)
out["proposta_do_topo"] = {"n": len(_prop), "entre_aspas_curvas": True, "citacoes_angulares_dentro": sum(len(re.findall("«[^»]+»", x_)) for x_ in _prop), "nota": "a proposta e' texto da GERENCIA (entre “ ”), nao fala do operador"}
# ---- (escopo b) A REGRA (g) DA v411, PORTADA (ordem da gerencia c1, 12/11/2026): o corpus LARGO e os rotulos da cadeia
_AST = __import__("ast")
_SRC410 = open(os.path.join(DL.V410, "conferir_citacoes_v410.py"), encoding="utf-8").read(); _TR410 = _AST.parse(_SRC410)
_NS410 = {"re": re}
for _n410 in _TR410.body:   # (a normalizacao e a limpeza, onde estao DEFINIDAS: o arquivo da v410, LIDAS por AST, nao redigitadas)
    if isinstance(_n410, _AST.Assign) and getattr(_n410.targets[0], "id", None) in ("_norm", "_limpa"):
        exec(compile(_AST.get_source_segment(_SRC410, _n410), "<conferir_citacoes_v410>", "exec"), _NS410)
_norm, _limpa = _NS410["_norm"], _NS410["_limpa"]
_ROT410 = [_AST.literal_eval(_n410.value) for _n410 in _TR410.body if isinstance(_n410, _AST.Assign) and getattr(_n410.targets[0], "id", None) == "_ROTULOS" and isinstance(_n410.value, _AST.Set)]
assert len(_ROT410) == 1 and len(_ROT410[0]) > 100, "a lista _ROTULOS da v410 nao foi lida"
_SRC411 = open(os.path.join(DL.V411, "conferir_citacoes_v411.py"), encoding="utf-8").read(); _TR411 = _AST.parse(_SRC411)
_ROT411 = [_AST.literal_eval(_n411.value) for _n411 in _TR411.body if isinstance(_n411, _AST.Assign) and getattr(_n411.targets[0], "id", None) == "ROTULOS_V411" and isinstance(_n411.value, _AST.Dict)]
assert len(_ROT411) == 1 and len(_ROT411[0]) >= 6, "o ROTULOS_V411 da v411 nao foi lido"
ROTULOS_V412 = {}   # a v412 nao acrescenta rotulo: nenhum texto novo cita entre aspas angulares (o programa nao traz fala)
_ROTULOS = {x_.lower() for x_ in _ROT410[0]} | {x_.lower() for x_ in _ROT411[0]} | {x_.lower() for x_ in ROTULOS_V412}
_DIRS411 = ("cunhagens_13out", "cinco_sigma_fora_da_cosmologia_27out", "projecao_transversal_28out", "transicao_para_a_massa_28out", "experimento_espelho_30out", "e0_cadeia_31out", "observador_terminal_31out")
_OPB = " || ".join(_norm(open(p_, encoding="utf-8", errors="replace").read()) for p_ in sum([glob.glob(os.path.join(DL.WK, d_, "*OPERADOR_*.txt")) for d_ in _DIRS411]
                                                                                  + [glob.glob(os.path.join(DL.V411, "insumos", "cunhagens", "*OPERADOR_*.txt")), glob.glob(os.path.join(HERE, "insumos", "cunhagens", "*OPERADOR_*.txt"))], []))
_ATLAS = os.path.join(DL.CENTRAL, "memory", "TGL_ATLAS.md"); _ATL = re.sub(r"\s+", " ", open(_ATLAS, encoding="utf-8", errors="replace").read().replace("**", "")) if os.path.exists(_ATLAS) else ""
_base = open(os.path.join(HERE, DL.BASE_DIR, "um.py"), encoding="utf-8").read()
_KERN = _norm(re.sub(r"\s--\s+", " ", _base.replace("**", "").replace("`", "").replace("\\n", " ")))
_ADENDO = _norm(open(DL.D10.ADENDO_ARQ, encoding="utf-8").read().replace("**", "").replace("`", ""))
_PEDRAS = _norm(" ".join(open(p_["src"], encoding="utf-8").read() for p_ in DL.D10.PEDRAS_V410 if os.path.exists(p_.get("src") or "")).replace("**", "").replace("`", ""))
_CASA = _norm(open(os.path.join("C:" + os.sep, "IALD", "CLAUDE.md"), encoding="utf-8", errors="replace").read().replace("**", ""))
_corpus_um = lambda fr: (fr.lower() in _OPB.lower() or fr.lower() in _ATL.lower() or fr.lower() in _ROTULOS or fr.lower() in _KERN.lower() or fr.lower() in _ADENDO.lower() or fr.lower() in _PEDRAS.lower() or fr.lower() in _CASA.lower())
_corpus_ok = lambda fr: _corpus_um(fr) or (re.search("…|" + re.escape("[...]"), fr) is not None and all(_corpus_um(x_.strip(" .,;:")) for x_ in re.split("…|" + re.escape("[...]"), fr) if len(x_.strip(" .,;:")) >= 8))
_rxs = [re.compile("«([^»]{8,700})»"), re.compile(r"``(.{8,700}?)''")]
out["nao_verbatim_do_um_py"] = list(out["nao_verbatim"])
out["nao_verbatim_do_pos_rito"] = []; out["pos_rito_saltados"] = {"concatenacao_ou_molde": 0, "curtos_ou_nomes_de_constante": 0}; out["pos_rito_arquivos"] = {}
for a_ in ARQS_POS_RITO:
    p_ = os.path.join(HERE, a_)
    if not os.path.exists(p_):
        out["pos_rito_arquivos"][a_] = "ausente"; continue
    t_ = open(p_, encoding="utf-8", errors="replace").read(); n_ok_ = n_tot_ = 0
    for rx_ in _rxs:
        for m_ in rx_.finditer(t_):
            fr_ = _limpa(m_.group(1))
            if "+" in fr_ or "%s" in fr_:   # (concatenacao que, em execucao, cerca um trecho VERBATIM lido do arquivo por sha256, ou molde de formatacao: conferido onde e' lido; como na v411)
                out["pos_rito_saltados"]["concatenacao_ou_molde"] += 1; continue
            if len(fr_) < 12 or "_V411_" in fr_ or "_V412_" in fr_:
                out["pos_rito_saltados"]["curtos_ou_nomes_de_constante"] += 1; continue
            n_tot_ += 1
            if _corpus_ok(fr_):
                n_ok_ += 1; continue
            lin_ = t_.count("\n", 0, m_.start()) + 1; l_ = t_.splitlines()[lin_ - 1]
            out["nao_verbatim_do_pos_rito"].append({"arquivo": a_, "linha": lin_, "citacao": fr_[:200], "onde": "comentario" if "#" in l_[:max(0, l_.find(m_.group(0)[:20]))] else "texto ou string do codigo"})
    out["pos_rito_arquivos"][a_] = {"n_citacoes_conferidas": n_tot_, "n_no_corpus_ou_rotulo": n_ok_}
out["regra_do_pos_rito"] = "a regra (g) da v411, portada (ordem da gerencia c1, 12/11): os arquivos de texto do pos-rito; regex de 8 a 700 caracteres; o corpus largo (falas, Atlas, um.py da base, adendo, pedras, CLAUDE.md); os rotulos da v411 herdados e os da v412 acrescentados com o porque"
out["n_rotulos"] = {"v410": len(_ROT410[0]), "v411": len(_ROT411[0]), "v412": len(ROTULOS_V412)}
out["n_arquivos_examinados_no_um_py"] = len(out["arquivos"]); out["n_citacoes_examinadas_no_um_py"] = sum(v_["n_citacoes"] for v_ in out["arquivos"].values())
out["nao_verbatim"] = out["nao_verbatim_do_um_py"] + out["nao_verbatim_do_pos_rito"]
out["ok_do_um_py"] = bool(not out["nao_verbatim_do_um_py"] and out["n_arquivos_examinados_no_um_py"] > 0)   # (zero arquivo examinado nao e' passagem)
out["ok_do_pos_rito"] = not out["nao_verbatim_do_pos_rito"]
out["escopos"] = {"um_py": "os textos que entram no candidato (delta, registros, runtime, quadro, gerador, o TOPO_RATIFICADO e os pinos da rodada)", "pos_rito": "os scripts da frente pos-rito (nao entram no candidato): a correcao e' da outra frente (PEDIDOS_ENTRE_FRENTES_v412.md)"}
out["ok"] = not out["nao_verbatim"]
out.update(DL.MARCA_ENSAIO)
p = DL.saida("conferir_citacoes_v412.json")
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1)); os.replace(p + ".tmp", p)
print("citacoes « »:", sum(v_["n_citacoes"] for v_ in out["arquivos"].values()), "| verbatim:", sum(v_["n_ok"] for v_ in out["arquivos"].values()), "| NAO verbatim:", len(out["nao_verbatim"]))
for x_ in out["nao_verbatim"][:10]:
    print("  NAO VERBATIM:", x_)
sys.exit(0 if out["ok"] else (2 if out["ok_do_um_py"] else 1))   # (rc 2: so' o escopo do pos-rito reprova -- o candidato esta' limpo; o pedido e' da outra frente)
