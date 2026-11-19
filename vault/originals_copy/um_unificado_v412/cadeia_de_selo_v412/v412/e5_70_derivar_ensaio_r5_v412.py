# -*- coding: utf-8 -*-
"""e5_70_derivar_ensaio_r5_v412.py -- FASE 1 do ensaio a seco do contrato R5 (claude-construtor-v412-ensaio-r5). Re-rodavel: toda correcao futura do ENSAIO entra como troca nova nas listas abaixo, nunca como edicao a mao das copias.
Deriva, SEM rodar nada do candidato e sem tocar o Nos:
  ensaio_a_seco_v412_r5.py (do ensaio_a_seco_v412.py, que fica intacto), os oito auxiliares _r5 que o ensaio importa ou chama (todos importam delta_v412), e3_topo_derivado_v412_r5.py e e5_71_resultado_ensaio_v412.py.
Cada troca e' de TEXTO EXATO com o minimo de ocorrencias exigido; o derivador comum (e5_deriv_v412.derivar) registra o achado em DERIVACAO_R5_PIPELINE_v412.json e confere que o destino compila.
Nenhum numero de modulos, de registros, de bandeiras, de ancoras ou de superficies e' digitado nas trocas: tudo e' lido do contrato, do manifesto, dos recibos ou de um._V412_SPECS em tempo de rodada.
Grava ENSAIO_R5_ESTADO_v412.json (arquivos e sha16 lidos dos arquivos, as trocas de conteudo e a causa de cada uma, as referencias residuais medidas por grep, o que fica por decidir e o comando da fase 2)."""
import datetime, hashlib, json, os, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
from e5_deriv_v412 import D, MODS_R5, derivar

EU = "e5_70_derivar_ensaio_r5_v412.py"
sha = lambda b: hashlib.sha256(b).hexdigest()
AUX = ["guarda_ordem_de_chamada_v412", "exame_pontos_v412", "simular_arvore_do_nos_v412", "guardas_estaticas_bancada_v412", "conferir_citacoes_v412", "topo_com_resultado_v412", "guarda_conversa_v412", "quadro_v397"]
MODS = MODS_R5 + AUX   # toda linha de import e todo nome de arquivo .py destes modulos passa a apontar para a copia _r5 (nunca a palavra solta)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# trocas de CONTEUDO do ensaio: (id, velho, novo, minimo de ocorrencias, porque). As trocas de import saem do derivador comum e nao entram aqui.
CONT = [
    ("A1", '''and len(_N12) == 4 and _N12[-1] == "cunhagens_v412"''',
     '''and _N12 == ["iald_camada_cientifica_v412", "leitor_da_formula_v412", "matematica_que_restava_v412", "parede_do_teste_cego_v412", "cunhagens_v412"] and len(set(_N12)) == len(_N12)''', 1,
     "o R5 tem CINCO registros por especificacao, na ordem do contrato (o leitor_da_formula_v412 e' novo); a contagem fixa de quatro cai, a ordem e os nomes sao cobrados"),
    ("A2", '''bool(all(_tudo12.values()) and len(_tudo12) == 4)''', '''bool(all(_tudo12.values()) and len(_tudo12) == len(_N12))''', 1, "a contagem dos registros que selam e' a dos registros do spec, lida de um._V412_NOMES_REGISTROS"),
    ("B1", '''_modA12, _modB12 = re.findall(r"`(\\w+)`", _mA.group(2)), re.findall(r"`(\\w+)`", _mB.group(2))''',
     '''_modA12, _modB12 = re.findall(r"`(\\w+)`", _mA.group(2)), re.findall(r"`(\\w+)`", _mB.group(2))
_mC = re.search(r"Frente C \\(o leitor da fórmula\\), (\\d+) m[óo]dulos", _CT12); _MAN12 = json.load(open(DL.MANIFESTO_ARQ_PEDRAS, encoding="utf-8"))["modulos"]
_frentes12 = {f_: sorted(e_["modulo"] for e_ in _MAN12 if e_["frente"] == f_) for f_ in ("A", "B", "C")}; _modC12 = list(_frentes12["C"])   # (R5: o contrato traz a LISTA das frentes A e B e so' a CONTAGEM da C; os nomes da C saem do campo `frente` do manifesto; A e B tambem sao cruzadas com o manifesto)
assert _mC and len(_MAN12) == sum(len(v_) for v_ in _frentes12.values()), "frente C nao achada no contrato, ou ha' modulo do manifesto fora das tres frentes"''', 1,
     "a frente C (109 modulos) nao tem lista no contrato R5, so' a contagem; a lista vem do manifesto (campo frente) e o ensaio confere a contagem do contrato contra ela; A e B ganham o cruzamento com o manifesto"),
    ("B2", '''for n_, mods_ in (("iald_camada_cientifica_v412", _modA12), ("matematica_que_restava_v412", _modB12)):''',
     '''for n_, mods_ in (("iald_camada_cientifica_v412", _modA12), ("leitor_da_formula_v412", _modC12), ("matematica_que_restava_v412", _modB12)):''', 1,
     "o leitor_da_formula_v412 e' o terceiro registro com ancora: as ancoras, as bandeiras e as declaracoes dele sao recalculadas como as dos outros dois"),
    ("B3", '''and _num12["iald_camada_cientifica_v412"]["n_ancoras"] + _num12["matematica_que_restava_v412"]["n_ancoras"] == _ANC12["n_ancoras_total"]''',
     '''and sum(v_["n_ancoras"] for v_ in _num12.values() if isinstance(v_, dict)) == _ANC12["n_ancoras_total"] and len([1 for v_ in _num12.values() if isinstance(v_, dict)]) == len(_frentes12)''', 1,
     "o total de ancoras do recibo e' a soma dos TRES registros com ancora (A, C, B), nao de dois; o numero de registros somados e' cobrado contra o de frentes do manifesto"),
    ("B4", '''and len(_modA12) == int(_mA.group(1)) and len(_modB12) == int(_mB.group(1)) and int(_mA.group(1)) + int(_mB.group(1)) == DL.N_BUNDLE == len(DL.BUNDLE_RELS) and set(_modA12 + _modB12) == {m_.split("/")[-1][:-5] for m_ in DL.BUNDLE_RELS} and len(_modA12 + _modB12) == len(set(_modA12 + _modB12)) > 0)''',
     '''and len(_modA12) == int(_mA.group(1)) and len(_modB12) == int(_mB.group(1)) and len(_modC12) == int(_mC.group(1)) and sorted(_modA12) == _frentes12["A"] and sorted(_modB12) == _frentes12["B"]
                                                                                  and int(_mA.group(1)) + int(_mB.group(1)) + int(_mC.group(1)) == DL.N_BUNDLE == len(DL.BUNDLE_RELS) == DL.N_MODULOS_DO_MANIFESTO and set(_modA12 + _modB12 + _modC12) == {m_.split("/")[-1][:-5] for m_ in DL.BUNDLE_RELS} and len(_modA12 + _modB12 + _modC12) == len(set(_modA12 + _modB12 + _modC12)) > 0)''', 1,
     "as tres frentes somam o bundle inteiro (153 no R5, lido do manifesto e do contrato; o R4 tinha 15 + 27 = 42), sem repeticao, e cada modulo do bundle e' de uma frente"),
    ("F1", '''_r_sem3 = um._v392_registro(dict(_sp_cn12, sem_guarda=True), dict(c, **{"parede_do_teste_cego_v412": dict(c["parede_do_teste_cego_v412"], all_verified=False)}))''',
     '''_selos12 = {ck_["id"]: ck_["caminho"][0] for ck_ in _sp_cn12["checks"] if ck_["id"].startswith("selo_")}   # (R5: o cunhagens_v412 cobra o selo de CADA um dos outros quatro registros, por um id proprio -- selo_camada, selo_leitor, selo_matematica, selo_parede --, sem forma de numero de revisao)
_r_sem12 = {i_: um._v392_registro(dict(_sp_cn12, sem_guarda=True), dict(c, **{r_: dict(c[r_], all_verified=False)})) for i_, r_ in _selos12.items()}   # (o selo de cada um dos outros registros tirado, um por vez: o cunhagens_v412 tem de recusar nos quatro casos)''', 1,
     "os ids das checagens do selo deixaram de ser r1, r2, r3 e o cunhagens cobra QUATRO selos; o ensaio tira o selo de cada registro, um por vez, e exige a recusa pelo id certo (o R4 tirava so' o da parede)"),
    ("F2", '''"cunhagens_cobra_o_selo_dos_outros_tres": bool(_r_sem3["all_verified"] is False and "CHECK_r3" in _r_sem3["verdict"]),''',
     '''"cunhagens_cobra_o_selo_dos_outros_quatro": bool(sorted(_selos12.values()) == sorted(n_ for n_ in _N12 if n_ != "cunhagens_v412") and len(_r_sem12) == len(_selos12) > 0 and all(r_["all_verified"] is False and ("CHECK_" + i_) in r_["verdict"] for i_, r_ in _r_sem12.items())), "n_selos_cobrados": len(_selos12),''', 1,
     "o conjunto dos registros cobrados e' exatamente o dos outros quatro, e cada selo retirado e' recusado com o id da propria checagem no veredito"),
    ("F3", '''for k_, v_ in _lig12.items() if k_ != "n_entradas")''', '''for k_, v_ in _lig12.items() if k_ not in ("n_entradas", "n_selos_cobrados"))''', 1, "o novo campo numerico do dicionario da ligacao nao e' booleano: sai do `all`, como o n_entradas, e entra no JSON"),
    ("F4", '''U["v412_a_ligacao_entre_os_registros_cunhagens_cobra_o_selo_dos_outros_tres_a_parede_e_as_entradas"]''', '''U["v412_a_ligacao_entre_os_registros_cunhagens_cobra_o_selo_dos_outros_quatro_a_parede_e_as_entradas"]''', 1, "o nome da checagem diz a verdade (quatro selos)"),
    ("G1", '''and len(_tr12) == 8 and all(_igual_recibo12.values()) and all(_no_core12.values()) and len(_no_core12) == 4''',
     '''and set(_tr12) == {"registro:" + n_ for n_ in _N12} | {p_ + ":" + l_ for p_ in ("artigo", "resumo") for l_ in ("pt", "en")} and all(_igual_recibo12.values()) and all(_no_core12.values()) and set(_no_core12) == set(_N12)''', 1,
     "as superficies da travessia refeita aqui sao os cinco registros mais o artigo e o resumo em PT e EN (nao oito, nao quatro): comparadas por NOME, lidos de _N12"),
    ("G2", '''_ru12["n_superficies"] == len(_ru12["superficies"]) >= 14''',
     '''_ru12["n_superficies"] == len(_ru12["superficies"]) > 0 and set(_ru12["superficies"]) == set(_tr12) | {p_ + ":" + l_ for p_ in ("readme", "estado_atual", "handoff") for l_ in ("pt", "en")}''', 1,
     "o recibo GUARDA_v412_UNIDADES.json passa de 14 para 15 superficies; em vez de trocar um piso por outro, o ensaio cobra os NOMES: as da travessia daqui mais o readme, o estado_atual e o handoff em PT e EN"),
    ("H1", '''        if "/checks[" in p_ and p_.endswith("/id"):
            _ids_fora12.append(p_); return
        _un12.append((p_, o_))''', '''        _un12.append((p_, o_))''', 1,
     "no R4 os ids de checagem (r1, r2, r3) tinham forma de numero de revisao e eram tirados da prosa; no R5 nenhum id tem (o gerador recusa), entao o ensaio os EXAMINA como qualquer texto e a excecao some"),
    ("H2", '''_ids_fora12 = []   # (os identificadores de checagem -- r1, r2, r3 -- sao nome de campo do spec, nao prosa: o padrao R<digito> do verificador os tomaria por numero de revisao; ficam FORA da prosa examinada e contados aqui)''',
     '''_ids_fora12 = []   # (R5: fica VAZIA de proposito -- os ids de checagem sao examinados como prosa --; o que o verificador tira da prosa agora sao os identificadores do kernel com ponto, contados em n_identificadores_do_kernel_fora_da_prosa)''', 1, "o comentario diz a regra nova"),
    ("H3", '''_vh12["n_unidades_examinadas"] > 1000 and _vh12a["ok"]''', '''_vh12["n_unidades_examinadas"] > 1000 and _vh12["n_identificadores_do_kernel_fora_da_prosa"] > 0 and not _ids_fora12 and _vh12a["ok"]''', 1,
     "zero identificador do kernel tirado da prosa seria o verificador sem a lista (FLAGS_v412.json ausente): os nomes `Codex.*` etc. voltariam a casar a palavra de modelo; o ensaio exige que o verificador tenha tirado mais de zero (e o resultado diz quantos)"),
    ("H4", '''"historia_de_conversa": {"ids_de_checagem_fora_da_prosa": len(_ids_fora12), ''', '''"historia_de_conversa": {"ids_de_checagem_fora_da_prosa": len(_ids_fora12), "identificadores_do_kernel_fora_da_prosa": _vh12["n_identificadores_do_kernel_fora_da_prosa"], ''', 1, "o resultado registra quantos identificadores do kernel o verificador tirou da prosa"),
    ("O1", '''U["v412_ordem_de_chamada_dos_quatro_specs_medida_por_ast_depois_do_bloco_da_v411_e_antes_de_emit_figures_com_cinco_controles_negativos"]''', '''U["v412_ordem_de_chamada_dos_cinco_specs_medida_por_ast_depois_do_bloco_da_v411_e_antes_de_emit_figures_com_cinco_controles_negativos"]''', 1, "o nome da checagem diz a verdade (cinco specs)"),
    ("O2", '''_op12["n_specs"] == len(um._V412_NOMES_REGISTROS) == 4 and _logo12''', '''_op12["n_specs"] == len(um._V412_NOMES_REGISTROS) == len(DL.REGISTROS_SPEC_V412) and _logo12''', 1, "a contagem de specs da ordem de chamada e' a de DL.REGISTROS_SPEC_V412, nao um 4 digitado"),
    ("V1", '''v["n_registros_retirados"] != 4 or v["n_linhas_do_quadro_de_vereditos_retiradas"] != 4 or''', '''v["n_registros_retirados"] != len(V412R) or v["n_linhas_do_quadro_de_vereditos_retiradas"] != len(V412R) or''', 1,
     "a variante do artigo sem os registros da v412 retira UMA linha do quadro por registro: cinco, lidos de V412R (a chave guarda_frases_v412 nao tem linha no quadro, como no R4)"),
    ("V2", '''any(int(a_) - int(b_) == 4 for a_, b_ in zip(_cont12[0], _cont12[1]) if a_ != b_)''', '''any(int(a_) - int(b_) == len(V412R) for a_, b_ in zip(_cont12[0], _cont12[1]) if a_ != b_)''', 1, "a contagem de chaves do quadro cai pelo numero de registros retirados (V412R), nao por 4"),
    ("V3", '''igual_ao_completo_menos_as_quatro_linhas_e_a_contagem''', '''igual_ao_completo_menos_as_linhas_dos_registros_e_a_contagem''', 2, "o nome do campo diz a verdade (uma linha por registro)"),
    ("V4", '''n_linhas_diferentes_alem_das_quatro''', '''n_linhas_diferentes_alem_das_dos_registros''', 1, "idem"),
    # texto dos comentarios e das docstrings das partes tocadas (o codigo ao lado ja' muda; a frase do comentario nao pode seguir dizendo quatro)
    ("C1", '''# (6r) [v412] OS QUATRO REGISTROS POR ESPECIFICACAO (iald_camada_cientifica_v412, matematica_que_restava_v412, parede_do_teste_cego_v412, cunhagens_v412)''',
     '''# (6r) [v412, contrato R5] OS CINCO REGISTROS POR ESPECIFICACAO (iald_camada_cientifica_v412, leitor_da_formula_v412, matematica_que_restava_v412, parede_do_teste_cego_v412, cunhagens_v412)''', 1, "comentario do bloco"),
    ("C2", '''o texto dos 40 modulos embutidos''', '''o texto dos modulos embutidos''', 1, "comentario do bloco"),
    ("C3", '''as quatro funcoes EMBUTIDAS (a guarda sobre UMA unidade, a divisao em unidades, a divisao do TeX, a travessia) sao as da cadeia, funcao por funcao''', '''as quatro funcoes EMBUTIDAS (a guarda sobre UMA unidade, a divisao em unidades, a divisao do TeX, a travessia; sao quatro funcoes, nao quatro registros) sao as da cadeia, funcao por funcao''', 1, "o quatro das funcoes continua certo; o comentario diz que nao e' o dos registros"),
    ("C4", '''# --- (g) a guarda de frases da v412 (contrato R4, secao 5)''', '''# --- (g) a guarda de frases da v412 (contrato R5, secao 5)''', 1, "comentario do bloco"),
    ("C5", '''# --- (h) nenhum texto novo traz historia de conversa (o verificador da cadeia, com o autoteste): os quatro registros inteiros,''', '''# --- (h) nenhum texto novo traz historia de conversa (o verificador da cadeia, com o autoteste): os cinco registros inteiros,''', 1, "comentario do bloco"),
    ("C6", '''# (v412) a VARIANTE sem os quatro registros por especificacao da v412:''', '''# (v412) a VARIANTE sem os registros por especificacao da v412 (cinco no R5):''', 1, "comentario do bloco"),
    ("C7", '''menos as QUATRO linhas do quadro de vereditos e a contagem de chaves (N menos quatro)''', '''menos as linhas do quadro de vereditos dos registros (uma por registro) e a contagem de chaves (N menos o numero de registros)''', 1, "comentario do bloco"),
    ("C8", '''(V412R) e a chave nova do core, o resultado da travessia da guarda de frases (V412N): os quatro por especificacao''', '''(V412R) e a chave nova do core, o resultado da travessia da guarda de frases (V412N): os cinco por especificacao (contrato R5)''', 1, "comentario da linha dos nomes novos"),
    ("C9", '''# --- (f) a ligacao entre os registros: o cunhagens_v412 cobra o selo dos outros tres;''', '''# --- (f) a ligacao entre os registros: o cunhagens_v412 cobra o selo dos outros quatro;''', 1, "comentario do bloco"),
    ("S1", '''all(((seal.get("registros_v412") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V412_NOMES_REGISTROS) and len(seal.get("registros_v412") or {}) == 4)''',
     '''all(((seal.get("registros_v412") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V412_NOMES_REGISTROS) and len(seal.get("registros_v412") or {}) == len(um._V412_NOMES_REGISTROS))''', 1,
     "o resumo do selo traz UM item por registro novo da v412 (cinco no R5): a contagem e' a de um._V412_NOMES_REGISTROS, nao um 4 digitado (achado por grep dos `== 4` do ensaio)"),
    ("C10", '''# (5b-v412) A ORDEM DE CHAMADA DOS QUATRO REGISTROS POR ESPECIFICACAO (_v412_rodar_specs)''', '''# (5b-v412) A ORDEM DE CHAMADA DOS CINCO REGISTROS POR ESPECIFICACAO (_v412_rodar_specs)''', 1, "comentario do bloco"),
    ("C11", '''o cunhagens_v412 vem por ultimo (cobra o selo dos outros tres); examina TODAS''', '''o cunhagens_v412 vem por ultimo (cobra o selo dos outros quatro); examina TODAS''', 1, "comentario do bloco"),
    ("C12", '''os QUATRO registros por especificacao da v412 no ponto de chamada real''', '''os registros por especificacao da v412 (cinco no contrato R5) no ponto de chamada real''', 1, "docstring"),
]
CONT_AUX_TEXTO = {
    "guarda_ordem_de_chamada_v412": [
        ("T1", '''(os QUATRO registros por especificacao): toda chave''', '''(os cinco registros por especificacao no R5): toda chave''', 1, "comentario do cabecalho"),
        ("T2", '''(v412) os QUATRO registros por especificacao: a ordem de chamada''', '''(v412, R5) os CINCO registros por especificacao: a ordem de chamada''', 1, "comentario de secao")],
    "simular_arvore_do_nos_v412": [
        ("T3", '''quatro registros da v412 e os herdados selam''', '''cinco registros da v412 (contrato R5) e os herdados selam''', 1, "comentario do cabecalho"),
        ("T4", '''(v412: os quatro registros por especificacao DEPOIS''', '''(v412, R5: os cinco registros por especificacao DEPOIS''', 1, "comentario da instrucao"),
        ("T5", '''os quatro registros da v412 entram depois dos da v411''', '''os cinco registros da v412 (contrato R5) entram depois dos da v411''', 1, "comentario do cabecalho")],
}
CONT_EXAME = [
    ("E3", '''ponto novo (4j) dos quatro registros por especificacao''', '''ponto novo (4j) dos cinco registros por especificacao (R5)''', 1, "comentario do cabecalho"),
    ("E4", '''(v412: + os quatro registros por especificacao)''', '''(v412, R5: + os cinco registros por especificacao)''', 1, "comentario"),
    ("E5", '''(v412) os quatro registros por especificacao: a instrucao seguinte''', '''(v412, R5) os cinco registros por especificacao: a instrucao seguinte''', 1, "comentario"),
    ("E6", '''(4j) o ponto NOVO da v412: os quatro registros por especificacao''', '''(4j) o ponto NOVO da v412: os cinco registros por especificacao''', 1, "comentario"),
    ("E1", '''or pv12_["n_registros"] != 4''', '''or pv12_["n_registros"] != len(DL.REGISTROS_SPEC_V412)''', 1, "o ponto de chamada real confere os registros do spec (cinco no R5), lidos de DL.REGISTROS_SPEC_V412"),
    ("E2", '''# (4j) [v412] o PONTO DE CHAMADA REAL dos quatro registros por especificacao''', '''# (4j) [v412, contrato R5] o PONTO DE CHAMADA REAL dos cinco registros por especificacao''', 1, "comentario do bloco"),
]
CONT_RESULTADO = [
    ("R1", '''(contrato R4; o resultado do R1 fica em ENSAIO_RESULTADO_v412.json.bak_r1)''', '''(contrato R5, ensaio_a_seco_v412_r5.py; o resultado do R4 fica na copia .bak_<data> que este script faz antes de regravar)''', 1, "docstring"),
    ("R2", '''r"C:\\t\\k412c\\ensaio_adapt\\r4_run1.txt"''', '''r"C:\\t\\k412c\\ensaio_adapt\\r5_run1.txt"''', 1, "a saida da rodada do R5 vai para r5_run*.txt (as do R4 ficam como estao)"),
    ("R3", '''(ensaio_a_seco_v412.py, montado do original da v411 por e3_ensaio_adaptar_v412.py) sobre o candidato do contrato R4"''', '''(ensaio_a_seco_v412_r5.py, derivado do ensaio do R4 por e5_70_derivar_ensaio_r5_v412.py) sobre o candidato do contrato R5"''', 1, "o que o arquivo diz que e'"),
    ("R4", '''open(OUT + ".tmp", "wb").write(b); assert os.path.getsize(OUT + ".tmp") == len(b)''',
     '''if os.path.exists(OUT) and open(OUT, "rb").read() != b:   # (backup de bytes do resultado anterior antes de regravar)
    _bk = OUT + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(_bk, "wb").write(open(OUT, "rb").read()); assert open(_bk, "rb").read() == open(OUT, "rb").read()
open(OUT + ".tmp", "wb").write(b); assert os.path.getsize(OUT + ".tmp") == len(b)''', 1, "regra do backup imediato: o resultado do R4 nao se perde"),
    ("R5", '''shutil.copyfile(SAIDA, os.path.join(HERE, "ENSAIO_SAIDA_v412.txt"))''',
     '''_SD = os.path.join(HERE, "ENSAIO_SAIDA_v412.txt")
if os.path.exists(_SD) and open(_SD, "rb").read() != open(SAIDA, "rb").read():
    _bk = _SD + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(_bk, "wb").write(open(_SD, "rb").read()); assert open(_bk, "rb").read() == open(_SD, "rb").read()
shutil.copyfile(SAIDA, _SD)''', 1, "idem para a saida do R4"),
]

ARQUIVOS = []   # (origem, destino) na ordem em que foram derivados
reg = {}


def der(origem, destino, trocas, imports=True):
    r = derivar(origem, destino, [(v, n, m) for _i, v, n, m, _p in trocas], EU, imports=imports, mods=MODS)
    ARQUIVOS.append((origem, destino)); reg[destino] = r
    return r


for a in AUX:
    tr = CONT_EXAME if a == "exame_pontos_v412" else CONT_AUX_TEXTO.get(a, [])
    der(a + ".py", a + "_r5.py", tr)
der("e3_topo_derivado_v412.py", "e3_topo_derivado_v412_r5.py", [], imports=False)
der("e3_resultado_ensaio_v412.py", "e5_71_resultado_ensaio_v412.py", CONT_RESULTADO, imports=False)
der("ensaio_a_seco_v412.py", "ensaio_a_seco_v412_r5.py", CONT)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# o que sobrou, medido por grep nas copias (nunca declarado de memoria)
PADROES = {
    "delta_v412_sem_r5": r"\bdelta_v412\b(?!_r5)",
    "contrato_R4": r"CONTRATO_v412_R4",
    "R13_REV13": r"\bR13\b|\bREV13\b",
    "manifesto_R7": r"MANIFESTO_PEDRAS_v412_R7",
    "pedras_r7": r"pedras_r7",
    "quatro_registros": r"(?i)\bquatro\b[^\n]{0,40}\bregistros?\b|\bregistros?\b[^\n]{0,40}\bquatro\b|os quatro por especifica|\bQUATRO registros",
    "igual_a_4": r"(==|!=) ?4\b",
    "n_42": r"\b42\b",
    "ids_r1_r2_r3": r"\"r[123]\"|\br[123]\b(?=[\"' ,:)])|CHECK_r3",
    "quatro_linhas_do_quadro": r"(?i)quatro linhas|dos_quatro_specs|outros_tres|outros tres",
}
resid = {}
for _o, dest in ARQUIVOS:
    t = (D / dest).read_bytes().decode("utf-8").split("\n")
    r = {}
    for nome, rx in PADROES.items():
        ach = []
        for i, l in enumerate(t, 1):
            if i == 1:
                continue   # o cabecalho do derivador cita os nomes do original
            for m in re.finditer(rx, l):
                antes = l[:m.start()]
                ach.append({"linha": i, "depois_de_um_cerquilha_na_linha": "#" in antes, "trecho": l[max(0, m.start() - 50):m.end() + 50]})
                break
        if ach:
            r[nome] = ach
    resid[dest] = r

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def sha16_arq(p):
    return sha(Path(p).read_bytes())[:16]


estado = {
    "o_que_e": "estado da FASE 1 do ensaio a seco do contrato R5 (adaptacao estatica; o ensaio NAO foi rodado; nenhum recibo do R4 foi tocado)",
    "agente": "claude-construtor-v412-ensaio-r5 (a servico do claude-construtor-v412)",
    "quando": datetime.datetime.now().isoformat(timespec="seconds"),
    "derivador": EU,
    "arquivos": {dest: {"origem": o, "origem_sha16": sha16_arq(D / o), "destino_sha16": sha16_arq(D / dest), "destino_bytes": (D / dest).stat().st_size, "n_trocas_total": len(reg[dest]["trocas"]),
                        "n_trocas_de_conteudo": {"ensaio_a_seco_v412_r5.py": len(CONT), "exame_pontos_v412_r5.py": len(CONT_EXAME), "e5_71_resultado_ensaio_v412.py": len(CONT_RESULTADO), **{k + "_r5.py": len(v) for k, v in CONT_AUX_TEXTO.items()}}.get(dest, 0)} for o, dest in ARQUIVOS},
    "trocas_de_import_do_ensaio": reg["ensaio_a_seco_v412_r5.py"]["trocas"][:len(reg["ensaio_a_seco_v412_r5.py"]["trocas"]) - len(CONT)],   # (as de import vem primeiro; depois as de conteudo)
    "trocas_de_conteudo": {"ensaio_a_seco_v412_r5.py": [{"id": i, "porque": p, "ocorrencias_achadas": None} for i, v, n, m, p in CONT],
                           "exame_pontos_v412_r5.py": [{"id": i, "porque": p} for i, v, n, m, p in CONT_EXAME], **{k + "_r5.py": [{"id": i, "porque": p} for i, v, n, m, p in v_] for k, v_ in CONT_AUX_TEXTO.items()}, "e5_71_resultado_ensaio_v412.py": [{"id": i, "porque": p} for i, v, n, m, p in CONT_RESULTADO]},
    "referencias_residuais_medidas_por_grep": resid,
    "sem_copia_de_proposito": {"runtime_v412_guarda.py": "a fonte da guarda embutida nao mudou (contrato R5)", "topo_v412.py": "nao mudou", "base_um_v411.py": "nao mudou", "acom_conferencias_v412.py": "nao importa nenhum modulo da cadeia v412; nao mudou"},
}
# a contagem de ocorrencias de cada troca de conteudo, lida do registro do derivador
oc = {}
for t in reg["ensaio_a_seco_v412_r5.py"]["trocas"]:
    oc[t["velho"]] = t["ocorrencias"]
for it in estado["trocas_de_conteudo"]["ensaio_a_seco_v412_r5.py"]:
    v = [x for x in CONT if x[0] == it["id"]][0][1]
    it["ocorrencias_achadas"] = oc.get(v[:160])
estado["comando_da_fase_2"] = [
    "(1) conferir que o candidato novo e os recibos do build estao no lugar: um_v412_candidato.py, CANDIDATO_v412.json, v412_pins.py, FORMAL_MAP_v412.json, GUARDA_FRASES_v412.json, GUARDA_v412_UNIDADES.json, REGISTROS_v412_RECIBO.json, ANCORAS_ESCOLHIDAS_v412.json, TEXTO_PUBLICO_v412.json, BLOCOS_TEXTO_PUBLICO_v412.json, kernel\\FLAGS_v412.json, kernel\\POS_BUILD_v412.json, BUNDLE_v412.json, kernel_modulos_novos_v412.json",
    "(2) C:\\Python314\\python.exe -B -X utf8 \"C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v412\\e3_topo_derivado_v412_r5.py\"   (rederiva TOPO_RATIFICADO_v412_DERIVADO.json do CANDIDATO_v412.json novo)",
    "(3) cd \"C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v412\" ; C:\\Python314\\python.exe -B -X utf8 ensaio_a_seco_v412_r5.py > C:\\t\\k412c\\ensaio_adapt\\r5_run1.txt 2>&1 ; echo rc=$?   (sem -I; ~40 min; em segundo plano; a saida de rodada vai para C:\\t\\k412c\\ensaio_adapt)",
    "(4) C:\\Python314\\python.exe -B -X utf8 e5_71_resultado_ensaio_v412.py C:\\t\\k412c\\ensaio_adapt\\r5_run1.txt   (grava ENSAIO_RESULTADO_v412.json e copia a saida para ENSAIO_SAIDA_v412.txt, com backup dos do R4)",
]
estado["os_residuos_acima_sao"] = "comentarios e docstrings HERDADOS de v403 a v411 (os quatro registros com funcao da v403, da v410, da v411; QUATRO linhas do .md; o cabecalho historico do R4), igualdades a 4 de blocos HERDADOS (erratas, medidas, insumos do H0DN, bundles da v408), o `r2` e o `R2` de versoes antigas (variaveis e rotulos de D99), e o `delta_v412` de duas citacoes em comentario/docstring (conferir_citacoes l.7; quadro_v397 l.13): nenhum e' codigo vivo do R5. O que era codigo vivo do R4 e' o que as trocas de conteudo tratam (ver trocas_de_conteudo)."
estado["checagens_do_R4_que_mudaram_de_sentido_no_R5"] = [
    "A exigencia 'sao quatro registros' (len == 4) virou a lista de cinco nomes na ordem do contrato (A1); nada foi relaxado: ficou mais estrita (nomes e ordem).",
    "(f) o cunhagens_v412 cobrava o selo dos 'outros tres' pelo id r3 (so' o da parede era tirado); no R5 sao quatro ids proprios e o ensaio tira o selo de cada um, um por vez (F1 a F3).",
    "(h) os ids de checagem eram tirados da prosa por terem forma de numero de revisao; no R5 nenhum tem, e o ensaio os examina (H1); o que o verificador tira da prosa agora (identificadores do kernel com ponto) e' contado e exigido > 0 (H3, H4).",
    "(g) o piso 'superficies >= 14' virou igualdade de NOMES (as da travessia mais readme, estado_atual e handoff em PT e EN): 15 no R5, sem digitar o 15 (G1, G2).",
    "(6r) 15 + 27 = 42 modulos lidos do contrato: agora A + B + C, com a C lida do manifesto (so' a contagem esta no contrato) e A e B cruzadas com o manifesto; soma cobrada contra o bundle e DL.N_MODULOS_DO_MANIFESTO (B1 a B4).",
    "o resumo do selo (`seal['registros_v412']`) tinha `len == 4` escondido na checagem do selo; achado por grep e corrigido para o numero de registros do spec (S1).",
]
estado["por_decidir_e_so_se_prova_na_fase_2"] = [
    "tudo o que depende do candidato novo: as ancoras do leitor_da_formula_v412 recalculadas, o numero de identificadores do kernel tirados da prosa (> 0), os titulos `\\subsection*{N. ...}` do bloco novo 'O leitor da fórmula' em ordem numerica (a checagem secoes_numeradas_em_ordem le a numeracao do texto novo), o tamanho dos titulos em _H12 (>= 5), o marcador 'classes do seu dicionário' no resumo novo (conferido por mim no TEXTO_PUBLICO_v412.json de hoje: presente em PT e EN).",
    "conferir_citacoes_v412_r5 varre, por nome de arquivo, as copias _r5 de delta, registros, textos_registros e gerador, mas NAO varre texto_publico_v412_r5.py nem guarda_frases_v412_r5.py (o TEXTO_PUBLICO_v412.json ja' entra); acrescentar e' decisao da gerencia (nao fiz: nao mudo o escopo de uma checagem sem ordem).",
    "os arquivos de saida mantem os NOMES do R4 (ensaio_a_seco_v412.json, conferir_citacoes_v412.json, GUARDAS_ESTATICAS_BANCADA_v412.json, ENSAIO_RESULTADO_v412.json, ENSAIO_SAIDA_v412.txt): o e5_71 faz backup de bytes do RESULTADO e da SAIDA; os outros tres sao regravados pelo ensaio, entao o passo (0) do comando os guarda antes. SIMULACAO_ARVORE_NOS_<sha16> e EXAME_PONTOS_<sha16> levam o hash do candidato (nao colidem).",
    "tempo: o R4 levou ~39 min; o R5 tem ~3x mais checagens negadas (o leitor_da_formula_v412 traz uma checagem de bandeira e uma de declaracao por ancora): esperar mais.",
]
estado["comando_da_fase_2"].insert(0, "(0) backup de bytes dos tres JSON que o ensaio regrava: para f in ensaio_a_seco_v412.json conferir_citacoes_v412.json GUARDAS_ESTATICAS_BANCADA_v412.json: cp $f $f.bak_r4_<AAAAMMDD_HHMMSS> (na pasta da cadeia)")
b = json.dumps(estado, ensure_ascii=False, indent=1).encode("utf-8")
p = D / "ENSAIO_R5_ESTADO_v412.json"
if p.exists() and p.read_bytes() != b:
    bk = Path(str(p) + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")); bk.write_bytes(p.read_bytes()); assert bk.read_bytes() == p.read_bytes()
tmp = Path(str(p) + ".tmp"); tmp.write_bytes(b); assert tmp.stat().st_size == len(b); os.replace(tmp, p)
print("gravado", p.name, len(b), "bytes sha16", sha(b)[:16])
for dest, r in resid.items():
    print(" residuos em", dest, {k: len(v) for k, v in r.items()})
