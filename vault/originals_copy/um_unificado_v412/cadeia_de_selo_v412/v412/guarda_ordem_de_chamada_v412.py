# -*- coding: utf-8 -*-
# [ADAPTADO v412, 17/11/2026, claude-construtor-v412-ensaio] a v412 nao tem registro com funcao novo: o registro da v411 (h0dn_bg1_v411) segue conferido como HERDADO (as listas abaixo ficam como a subida de rotulo as deixou, e o ensaio as confere); NOVO: ordem_dos_specs / controle_negativo_specs conferem, por AST, a instrucao do main que chama _v412_rodar_specs(core) (os QUATRO registros por especificacao): toda chave que as checagens deles leem esta pronta antes; cinco controles negativos; zero checagens examinadas reprova.
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork C)] montado por _adapt_guarda_ordem_v411.py do ORIGINAL v410/guarda_ordem_de_chamada_v410.py: a funcao NOVA e' h0dn_bg1_v411 (depois do h0dn_fontes_hms13_v410 e dos specs da v410); os quatro registros da v410 passam a herdados; controles negativos (18) e (19)
# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada), por _adapt_h0dn_pos_v410.py] D72: o h0dn_bg1_v410 entra em FUNCOES_NOVAS_V410 (mecanica _v410_h0dn_mechanics; miolo _v398_beta; os insumos exigidos do iald2) e o controle negativo (14): a chamada retirada reprova
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] a funcao NOVA e' iald2_v410 (depois do traducao_turing_v409 e dos specs da v409); a traducao passa a herdada; controles negativos (12) e (13); MONTADO por _adapt_forkB_guarda_ordem_v410.py a partir do ORIGINAL da v409 (nao da subida mecanica); fork B do claude-construtor-v410
# (v409: a funcao NOVA da v409 era traducao_turing_v409, depois do tetelestai_terminal_v408 e dos specs da v408; o terminal passava a herdado; controles negativos (10) e (11))
"""guarda_ordem_de_chamada_v412.py -- (v412: a funcao NOVA e' h0dn_bg1_v411, LOGO DEPOIS do bloco da v411; as da v411 passam a herdadas) A ORDEM DE CHAMADA (licao 1 da v408: a 1a tentativa do rito de 28/10/2026). AUTORAL na v409: a da v408 olhava so' o corpo da funcao chamada no main; os registros de pedra da v408 sao de uma linha (chamam _v405_registro, que chama _v405_formal e a mecanica), e la' a leitura nao aparece: copiar a guarda daria vacuo (nenhuma leitura vista, tudo «ok»).
(na v409 a funcao NOVA era o `traducao_turing_v409`; na v408, o `tetelestai_terminal_v408`; na v407, o `psion_canto_v407`.) ADAPTADA a v411 (06/11/2026, fork B do claude-construtor-v411): a funcao NOVA e' UMA, `iald2_v410` (le do core, entre outras que a guarda lista, `kernel_formalization`, `external_ladder`, `qg_closure` e `beta`; chamada no main LOGO DEPOIS do bloco do `traducao_turing_v409` e dos specs da v409; miolo `_v410_formal`, `_v398_beta`; mecanica `v410_iald2_mechanics`); o `traducao_turing_v409` passa a HERDADO. ADAPTADA a v409 (05/11/2026): a funcao NOVA da v409 era UMA, `traducao_turing_v409` (le do core `kernel_formalization`, `external_ladder`, `qg_closure` e `beta`; chamada no main LOGO DEPOIS do bloco do `tetelestai_terminal_v408` e dos specs da v408; miolo `_v409_formal`, `_v398_beta`; mecanica `v409_traducao_mechanics`); a da v407 era o `psion_canto_v407` (registro com funcao; le do core `kernel_formalization`, `external_ladder`, `witness_rigidity`, `qg_closure`, `beta` e as chaves de testemunha: `rede_fock_v394`, `psibit_v395`, `testemunha_estatica_v396`, `witness_layers`); ela e' chamada no main LOGO DEPOIS do bloco do `fechamento_v406`
(que, por sua vez, vem logo depois do `_v405_rodar_specs`), e as chaves que ela le ja' tem de estar gravadas. A leitura dela passa pelo miolo comum da v409 (`_v407_formal`, `_v407_chaves`, `_v398_beta`) e pela mecanica `v407_psion_mechanics`. O `fechamento_v406` passa a ser HERDADO (o codigo dele so' muda na checagem c8, declarada em E20) e segue conferido com o miolo da v408
(`_v406_formal`, `_v406_chaves`, `_v398_beta`) e a mecanica `v406_fechamento_mechanics`; as OITO funcoes de pedra da v408 e o `_v405_rodar_specs` seguem conferidos (o codigo delas nao muda na v409: «nada da v408 perdido»).
Toda chave do core que uma funcao de registro NOVA LE, em qualquer funcao que ela alcanca (core.get("K"), core_.get("K"), core["K"], core_["K"]), tem de estar pronta ANTES da instrucao do main que a chama. Pronta quer dizer: (a) vem de run_um (a primeira instrucao do main e' `core = run_um(...)`; as chaves literais dos dicts de run_um);
ou (b) core["K"] = ... numa instrucao ANTERIOR do main; ou (c) a chamada `K(core)` numa instrucao ANTERIOR do main (a convencao dos registros: a funcao grava core["K"]). O que nao se acha em nenhum dos tres e' FALHA VISIVEL (`lidas_sem_origem`), nunca «ok» por omissao.
Esta guarda e' ESTATICA (AST), nao executa nada. Controle negativo em controle_negativo(): a mesma fonte com o registro da Ponte da Massa chamado ANTES da projecao_transversal_v404 tem de reprovar; uma leitura de chave inexistente tambem; o `fechamento_v406` antes dos specs da v408 tambem; o `psion_canto_v407` ANTES do `fechamento_v406` tambem; e
os dois registros sem a chamada no main tambem; [v408/v409] o terminal antes do psion e a traducao antes do terminal tambem; [v410] o `iald2_v410` ANTES do `traducao_turing_v409` tambem, e o `iald2_v410` sem a chamada no main tambem.
uso: python -I -B -X utf8 guarda_ordem_de_chamada_v412.py <um.py> [funcao ...]   (rc 0 = toda leitura depois da origem; rc 1 = ha leitura antes ou sem origem; grava GUARDA_ORDEM_DE_CHAMADA_v412.json em DL.saida (a pasta da cadeia, ou a de ensaio), com a ordem real e o controle negativo)
Como modulo: ordem_de_chamada(src_text, funcoes) -> dict com "ok"; controle_negativo(src_text) -> dict com "ok"."""
import ast, json, os, re, sys

FUNCOES_PEDRAS = ("ponte_da_massa_v405", "massa_tensao_pura_v405", "identidade_v405", "observador_terminal_v405", "lei_do_diminuto_v405", "tonica_do_hamiltoniano_v405", "disco_de_euler_v405", "ponto_zero_do_psion_v405")   # (as oito da v408: herdadas, intactas)
FUNCOES_HERDADAS_V408 = FUNCOES_PEDRAS + ("_v405_rodar_specs",)   # (o ultimo: as medidas do Grande Atrator rodam dentro dos specs da v408)
FUNCOES_HERDADAS_V409 = FUNCOES_HERDADAS_V408 + ("fechamento_v406", "psion_canto_v407", "tetelestai_terminal_v408")   # (v409: os registros da v406, da v407 e da v408 sao herdados, intactos: nenhuma chave antiga muda)
FUNCOES_NOVAS_V409 = ("traducao_turing_v409",)                     # a v409 e' um BUNDLE de um modulo de kernel: o UNICO registro com funcao novo e' o da traducao
FUNCOES_V409 = FUNCOES_NOVAS_V409 + FUNCOES_HERDADAS_V409         # o que o ensaio confere: a nova e as herdadas
FUNCOES_HERDADAS_V411 = FUNCOES_HERDADAS_V409 + FUNCOES_NOVAS_V409   # (v411: o registro da v409, traducao_turing_v409, passa a herdado, intacto: nenhuma chave antiga muda)
FUNCOES_NOVAS_V411 = ("iald2_v410", "a_escala_v410", "h0dn_bg1_v410", "h0dn_fontes_hms13_v410")              # a v411 e' um BUNDLE de um modulo de kernel (IALD2) e traz DOIS registros com funcao novos: o iald2_v410 e, na MESMA instrucao do main, logo depois dele, o h0dn_bg1_v410 (D72: o teste pre-registrado da razao de Hubble; pré-registrado; nenhum dado observado lido)
FUNCOES_V411 = FUNCOES_NOVAS_V411 + FUNCOES_HERDADAS_V411         # (registro da v411)
FUNCOES_HERDADAS_V412 = FUNCOES_HERDADAS_V411 + FUNCOES_NOVAS_V411   # (v412: os quatro registros com funcao da v411 passam a herdados, intactos: nenhuma chave antiga muda)
FUNCOES_NOVAS_V412 = ("h0dn_bg1_v411",)                          # a v412 NAO tem modulo novo de kernel; o UNICO registro com funcao novo e' o do teste H0DN x BG1 ABERTO (recalculado dos bytes embutidos)
FUNCOES_V412 = FUNCOES_NOVAS_V412 + FUNCOES_HERDADAS_V412         # o que o ensaio confere: a nova e as herdadas (o ensaio_a_seco_v412 le esta)
MECANICA_DE = dict(zip(FUNCOES_HERDADAS_V408, ("v405_ponte_mechanics", "v405_tensao_mechanics", "v405_identidade_mechanics", "v405_observador_mechanics", "v405_diminuto_mechanics", "v405_tonica_mechanics", "v405_disco_mechanics", "v405_psion_mechanics", "v405_ga_mechanics")))
MECANICA_DE["fechamento_v406"] = "v406_fechamento_mechanics"
MECANICA_DE["psion_canto_v407"] = "v407_psion_mechanics"
MECANICA_DE["tetelestai_terminal_v408"] = "v408_terminal_mechanics"
MECANICA_DE["traducao_turing_v409"] = "v409_traducao_mechanics"
MECANICA_DE["iald2_v410"] = "v410_iald2_mechanics"
MECANICA_DE["h0dn_bg1_v410"] = "_v410_h0dn_mechanics"   # (v411, D72)
MECANICA_DE["a_escala_v410"] = "_v410_aescala_mechanics"   # (v411, D86: a pedra AEscala, na MESMA instrucao do iald2, logo depois dele)
MECANICA_DE["h0dn_fontes_hms13_v410"] = "_v410_hms13_mechanics"   # (v411, D80: o recibo documental HMS/13, na instrucao SEGUINTE do main)
MECANICA_DE["h0dn_bg1_v411"] = "v411_h0dn_mechanics"   # (v412: o teste aberto, recalculado no rito)
COMUNS = ("_v405_registro", "_v405_formal", "_v398_beta")     # o miolo comum das herdadas: tudo o que o registro le passa por aqui
COMUNS_DE = {"fechamento_v406": ("_v406_formal", "_v406_chaves", "_v398_beta"),   # o miolo comum do fechamento (a leitura das quatro chaves esta em _v406_chaves)
             "psion_canto_v407": ("_v407_formal", "_v407_chaves", "_v398_beta"),   # o miolo comum do psion (a leitura das chaves, a da v408 e as quatro da v406, esta em _v407_chaves)
             "tetelestai_terminal_v408": ("_v408_formal", "_v398_beta"),   # o miolo comum do terminal (nao le chave de testemunha: nenhuma chave antiga muda)
             "traducao_turing_v409": ("_v409_formal", "_v398_beta"),   # o miolo comum da traducao (nao le chave de testemunha: nenhuma chave antiga muda)
             "iald2_v410": ("_v410_formal", "_v398_beta"),   # (v411) o miolo comum do iald2 (nao le chave de testemunha: nenhuma chave antiga muda)
             "h0dn_bg1_v410": ("_v398_beta",),
             "h0dn_fontes_hms13_v410": ("_v398_beta",),
             "h0dn_bg1_v411": ("_v398_beta",),   # (v412) le qg_closure, external_ladder e core["h0dn_bg1_v410"] (gravado no bloco da v411)
             "a_escala_v410": ("_v398_beta",)}   # (v411, D86) o miolo comum do a_escala: le kernel_formalization, external_ladder, qg_closure e beta (todos do run_um)   # (v411, D80) o miolo comum do hms13: le qg_closure, beta e core["h0dn_bg1_v410"] (gravado na instrucao ANTERIOR do main: por isso a instrucao e' separada)   # (v411, D72) o miolo comum do h0dn (le hubble_ratio_v387, qg_closure e beta, todos do run_um: nenhuma chave antiga muda)
INSUMOS_EXIGIDOS = {"h0dn_bg1_v411": ("h0dn_fontes_hms13_v410", "_v410_rodar_specs", "iald2_v410", "a_escala_v410", "h0dn_bg1_v410", "traducao_turing_v409", "_v409_rodar_specs", "tetelestai_terminal_v408", "_v408_rodar_specs", "psion_canto_v407", "_v407_rodar_specs", "fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers"),   # (v412) depois do bloco INTEIRO da v411 (o hms13 e os specs da v411)
                    "h0dn_bg1_v410": ("traducao_turing_v409", "_v409_rodar_specs", "tetelestai_terminal_v408", "_v408_rodar_specs", "psion_canto_v407", "_v407_rodar_specs", "fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers"),   # (v411, D72) os mesmos do iald2: o h0dn e' chamado na MESMA instrucao do main, logo depois do iald2 (a ordem DENTRO da instrucao e' medida pelo ensaio e pelo exame_pontos)
                    "h0dn_fontes_hms13_v410": ("iald2_v410", "h0dn_bg1_v410", "traducao_turing_v409", "_v409_rodar_specs", "tetelestai_terminal_v408", "_v408_rodar_specs", "psion_canto_v407", "_v407_rodar_specs", "fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers"),   # (v411, D80) o hms13 e' chamado na instrucao SEGUINTE a' do iald2/h0dn: le core["h0dn_bg1_v410"]
                    "a_escala_v410": ("traducao_turing_v409", "_v409_rodar_specs", "tetelestai_terminal_v408", "_v408_rodar_specs", "psion_canto_v407", "_v407_rodar_specs", "fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers"),   # (v411, D86) os mesmos do iald2: chamado na MESMA instrucao, logo depois dele (a ordem DENTRO da instrucao e' medida pelo ensaio e pelo exame_pontos)
                    "iald2_v410": ("traducao_turing_v409", "_v409_rodar_specs", "tetelestai_terminal_v408", "_v408_rodar_specs", "psion_canto_v407", "_v407_rodar_specs", "fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers"),   # (v411) depois da traducao e dos specs da v409
                    "traducao_turing_v409": ("tetelestai_terminal_v408", "_v408_rodar_specs", "psion_canto_v407", "_v407_rodar_specs", "fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers"),
                    "tetelestai_terminal_v408": ("psion_canto_v407", "_v407_rodar_specs", "fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers"),
                    "psion_canto_v407": ("fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers", "_v405_rodar_specs"),
                    "fechamento_v406": ("rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers", "_v405_rodar_specs"), "ponte_da_massa_v405": ("neutrino_mass", "projecao_transversal_v404"), "massa_tensao_pura_v405": ("neutrino_mass",), "lei_do_diminuto_v405": ("neutrino_mass",), "tonica_do_hamiltoniano_v405": ("neutrino_mass",), "ponto_zero_do_psion_v405": ("neutrino_mass", "projecao_transversal_v404"), "observador_terminal_v405": ("omega_I",), "_v405_rodar_specs": ("joint_coincidence_result_v3", "ga_mass_audit", "mode_A", "mode_B")}
NOMES_DO_CORE = ("core", "core_")


def _chave_core(node):
    """core["K"] / core_["K"] -> "K" (so' chave literal), senao None."""
    if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name) and node.value.id in NOMES_DO_CORE and isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, str):
        return node.slice.value
    return None


def lidas_em(fd):
    """as chaves literais do core que o corpo da funcao fd le."""
    lidas = set()
    for n in ast.walk(fd):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "get" and isinstance(n.func.value, ast.Name) and n.func.value.id in NOMES_DO_CORE and n.args and isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, str):
            lidas.add(n.args[0].value)
        k = _chave_core(n)
        if k is not None and not isinstance(n.ctx, ast.Store):
            lidas.add(k)
    return lidas


def _chaves_de_run_um(fd):
    """as chaves literais dos dicts escritos em run_um (o core nasce ali). E' um superconjunto: dicts aninhados entram; a guarda nao usa isto para provar que uma chave FALTA, so' para achar a origem."""
    ks = set()
    for n in ast.walk(fd):
        if isinstance(n, ast.Dict):
            ks |= {k.value for k in n.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)}
    return ks


def ordem_de_chamada(src, funcoes=FUNCOES_V412):
    tree = ast.parse(src)
    defs = {}
    for n in tree.body:
        if isinstance(n, ast.FunctionDef):
            defs.setdefault(n.name, []).append(n)
    assert defs.get("main"), "sem def main"
    assert len(defs.get("run_um") or []) == 1, "run_um ausente ou duplicada"
    main = defs["main"][-1]
    de_run = _chaves_de_run_um(defs["run_um"][0])
    atrib = {}   # chave -> indice da PRIMEIRA instrucao do main que a produz: core["K"] = ... ou K(core)
    unp = [ast.unparse(st) for st in main.body]
    for i, st in enumerate(main.body):
        for n in ast.walk(st):
            if isinstance(n, ast.Assign):
                for t in n.targets:
                    k = _chave_core(t)
                    if k is not None:
                        atrib.setdefault(k, i)
        for nome in re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\(core\)", unp[i]):
            atrib.setdefault(nome, i)
    out = {"funcoes": {}, "ok": True, "comuns_lidos_de": list(COMUNS), "comuns_lidos_de_por_funcao": {k: list(v) for k, v in COMUNS_DE.items()}}
    for fn in funcoes:
        comuns = COMUNS_DE.get(fn, COMUNS)
        faltando = [x for x in (fn, MECANICA_DE.get(fn)) + comuns if x and len(defs.get(x) or []) != 1]
        if faltando:
            out["funcoes"][fn] = {"erro": "funcao ausente ou duplicada: %r" % (faltando,)}; out["ok"] = False; continue
        lidas = set()
        for x in (fn, MECANICA_DE[fn]) + comuns:
            lidas |= lidas_em(defs[x][0])
        lidas.discard(fn)
        ch = [i for i, s in enumerate(unp) if fn + "(core)" in s]
        if len(ch) != 1:
            out["funcoes"][fn] = {"erro": "chamada no main ausente ou nao unica", "indices": ch}; out["ok"] = False; continue
        ic = ch[0]
        no_main = {k: {"indice": atrib[k], "linha": main.body[atrib[k]].lineno, "antes_da_chamada": atrib[k] < ic} for k in sorted(lidas) if k in atrib}
        fora = sorted(k for k in lidas if k not in atrib and k in de_run)
        sem_origem = sorted(k for k in lidas if k not in atrib and k not in de_run)
        # o que vem de run_um e TAMBEM e' reatribuido no main conta pela origem de run_um (ja' esta la' quando a chamada acontece)
        antes = sorted(k for k, d in no_main.items() if not d["antes_da_chamada"] and k not in de_run)
        exig = INSUMOS_EXIGIDOS.get(fn, ())
        # (v409) o insumo exigido vale pela ATRIBUICAO/CHAMADA no main, lido de `atrib`, e nao so' quando a funcao o le como chave do core: o `_v405_rodar_specs` e o `fechamento_v406` sao CHAMADAS que tem de vir antes (do fechamento_v406 e do psion_canto_v407, respectivamente), nao chaves que a funcao leia
        faltam = [k for k in exig if not ((k in atrib and atrib[k] < ic) or k in de_run)]
        exigidos_antes = {k: {"indice": atrib[k], "linha": main.body[atrib[k]].lineno} for k in exig if k in atrib and atrib[k] < ic}
        ok_fn = bool(lidas) and not antes and not sem_origem and not faltam
        out["funcoes"][fn] = {"chamada": {"indice": ic, "linha": main.body[ic].lineno}, "n_chaves_lidas": len(lidas), "chaves_lidas": sorted(lidas), "insumos_produzidos_no_main": no_main, "insumos_de_run_um": fora, "lidas_sem_origem": sem_origem, "insumos_exigidos_ausentes": faltam, "insumos_exigidos_atribuidos_antes_no_main": exigidos_antes, "lidos_antes_da_atribuicao": antes, "ok": ok_fn}
        out["ok"] = out["ok"] and ok_fn
    return out


def _troca_blocos(src, fn_a, fn_b):
    """troca de lugar, por AST, as duas instrucoes VIZINHAS do main que chamam fn_a(core) e fn_b(core) (fn_a vem primeiro no original); devolve o texto novo. Sem reescrever o texto das instrucoes."""
    main_ = [x for x in ast.parse(src).body if isinstance(x, ast.FunctionDef) and x.name == "main"][-1]
    pos_ = {fn_: [i for i, st in enumerate(main_.body) if re.search(r"\b" + fn_ + r"\(core\)", ast.unparse(st))] for fn_ in (fn_a, fn_b)}
    assert all(len(v) == 1 for v in pos_.values()) and pos_[fn_b][0] == pos_[fn_a][0] + 1, ("as duas instrucoes nao sao vizinhas/unicas no main", pos_)
    sa_, sb_ = main_.body[pos_[fn_a][0]], main_.body[pos_[fn_b][0]]
    lin_ = src.split("\n"); bloco_a, bloco_b = lin_[sa_.lineno - 1:sa_.end_lineno], lin_[sb_.lineno - 1:sb_.end_lineno]
    assert sb_.lineno == sa_.end_lineno + 1, "as duas instrucoes nao sao contiguas no texto"
    return "\n".join(lin_[:sa_.lineno - 1] + bloco_b + bloco_a + lin_[sb_.end_lineno:])


def _sem_chamada(src, fn, var):
    """a chamada `var = fn(core)` sai do main (a atribuicao vira um dict vazio); exige que a linha seja achada UMA vez."""
    lin_ = src.split("\n")
    ln_ = [i for i, l in enumerate(lin_) if re.fullmatch(r"\s+" + var + r" = " + fn + r"\(core\)\s*", l)]
    assert len(ln_) == 1, ("a linha da chamada nao foi achada uma vez", fn, ln_)
    m_ = list(lin_); m_[ln_[0]] = re.sub(var + r" = " + fn + r"\(core\)", var + " = {}", m_[ln_[0]])
    return "\n".join(m_)


def controle_negativo(src):
    """(1) a Ponte da Massa chamada ANTES da projecao_transversal_v404 reprova; (2) uma leitura de chave sem origem reprova; (3) a fonte intacta passa; (4) [v406] o fechamento_v406 chamado ANTES do bloco `_v405_rodar_specs` (e, portanto, antes de o main fechar as chaves que ele le) reprova;
    (5) [v406] o fechamento_v406 sem a chamada no main reprova (nunca «ok» por omissao); (6) [v407] o psion_canto_v407 chamado ANTES do fechamento_v406 (as duas instrucoes trocam de lugar) reprova, e o motivo e' o insumo exigido ausente; (7) [v407] o psion_canto_v407 sem a chamada no main reprova;
    (8) [v408] o tetelestai_terminal_v408 chamado ANTES do psion_canto_v407 reprova, e o motivo e' o insumo exigido ausente; (9) [v408] o tetelestai_terminal_v408 sem a chamada no main reprova;
    (10) [v409] o traducao_turing_v409 chamado ANTES do tetelestai_terminal_v408 reprova, e o motivo e' o insumo exigido ausente; (11) [v409] o traducao_turing_v409 sem a chamada no main reprova;
    (12) [v410] o iald2_v410 chamado ANTES do traducao_turing_v409 reprova, e o motivo e' o insumo exigido ausente; (13) [v410] o iald2_v410 sem a chamada no main reprova; (14) [v411, D72] o h0dn_bg1_v410 sem a chamada no main reprova (a linha traz comentario: a troca e' por prefixo); (15) a (17) [v410] o hms13 e o a_escala;
    (18) [v411] o h0dn_bg1_v411 chamado ANTES do h0dn_fontes_hms13_v410 reprova, e o motivo e' o insumo exigido ausente; (19) [v411] o h0dn_bg1_v411 sem a chamada no main reprova. Rodado sobre o texto: nada executa."""
    r0 = ordem_de_chamada(src)
    ch_proj = "projecao_transversal_v404(core)"; ch_ponte = "ponte_da_massa_v405(core)"
    linhas = src.split("\n")
    ip = [i for i, l in enumerate(linhas) if re.fullmatch(r"\s+_\w+ = projecao_transversal_v404\(core\)\s*", l)]; ip2 = [i for i, l in enumerate(linhas) if re.fullmatch(r"\s+_\w+ = ponte_da_massa_v405\(core\)\s*", l)]
    assert len(ip) == 1 and len(ip2) == 1, ("as linhas das chamadas nao foram achadas uma vez", ip, ip2)
    # troca so' os nomes das funcoes nas duas instrucoes (a ponte passa a vir antes da projecao)
    a_ = linhas[ip[0]].replace(ch_proj, ch_ponte); b_ = linhas[ip2[0]].replace(ch_ponte, ch_proj)
    m_ = list(linhas); m_[ip[0]] = a_; m_[ip2[0]] = b_
    r1 = ordem_de_chamada("\n".join(m_))
    src2 = src.replace('    m_core_ = (core_.get("neutrino_mass") or {}).get("m_nu_meV")', '    m_core_ = (core_.get("chave_que_nao_existe_v409") or {}).get("m_nu_meV")', 1)
    assert src2 != src
    r2 = ordem_de_chamada(src2)
    # (4) o fechamento_v406 e o bloco dos specs da v408 trocam de lugar no main
    r3 = ordem_de_chamada(_troca_blocos(src, "_v405_rodar_specs", "fechamento_v406"))
    f3_ = r3["funcoes"].get("fechamento_v406") or {}
    # (5) a chamada do fechamento_v406 sai do main (a atribuicao vira um dict vazio)
    r4 = ordem_de_chamada(_sem_chamada(src, "fechamento_v406", "_r406"), ("fechamento_v406",))
    # (6) o psion_canto_v407 e o fechamento_v406 trocam de lugar: o psion passa a ser chamado ANTES do fechamento
    r5 = ordem_de_chamada(_troca_blocos(src, "fechamento_v406", "psion_canto_v407"), ("psion_canto_v407",))
    f5_ = r5["funcoes"].get("psion_canto_v407") or {}
    # (7) a chamada do psion_canto_v407 sai do main
    r6 = ordem_de_chamada(_sem_chamada(src, "psion_canto_v407", "_r407"), ("psion_canto_v407",))
    # (8) o tetelestai_terminal_v408 e o psion_canto_v407 trocam de lugar: o terminal passa a ser chamado ANTES do psion
    r7 = ordem_de_chamada(_troca_blocos(src, "psion_canto_v407", "tetelestai_terminal_v408"), ("tetelestai_terminal_v408",))
    f7_ = r7["funcoes"].get("tetelestai_terminal_v408") or {}
    # (9) a chamada do tetelestai_terminal_v408 sai do main
    r8 = ordem_de_chamada(_sem_chamada(src, "tetelestai_terminal_v408", "_r408"), ("tetelestai_terminal_v408",))
    # (10) o traducao_turing_v409 e o tetelestai_terminal_v408 trocam de lugar: a traducao passa a ser chamada ANTES do terminal
    r9 = ordem_de_chamada(_troca_blocos(src, "tetelestai_terminal_v408", "traducao_turing_v409"), ("traducao_turing_v409",))
    f9_ = r9["funcoes"].get("traducao_turing_v409") or {}
    # (11) a chamada do traducao_turing_v409 sai do main
    r10 = ordem_de_chamada(_sem_chamada(src, "traducao_turing_v409", "_r409"), ("traducao_turing_v409",))
    # (12) [v410] o iald2_v410 e o traducao_turing_v409 trocam de lugar: o iald2 passa a ser chamado ANTES da traducao
    r11 = ordem_de_chamada(_troca_blocos(src, "traducao_turing_v409", "iald2_v410"), ("iald2_v410",))
    f11_ = r11["funcoes"].get("iald2_v410") or {}
    # (13) [v410] a chamada do iald2_v410 sai do main
    r12 = ordem_de_chamada(_sem_chamada(src, "iald2_v410", "_r410"), ("iald2_v410",))
    # (14) [v411, D72] a chamada do h0dn_bg1_v410 sai do main (a linha do candidato traz um comentario depois da chamada: a troca e' por prefixo, nao por fullmatch)
    _lh = [i for i, l in enumerate(linhas) if re.match(r"\s+_h410 = h0dn_bg1_v410\(core\)", l)]; assert len(_lh) == 1, ("a linha da chamada do h0dn_bg1_v410 nao foi achada uma vez", _lh)
    m14_ = list(linhas); m14_[_lh[0]] = m14_[_lh[0]].replace("h0dn_bg1_v410(core)", "{}", 1)
    r13 = ordem_de_chamada("\n".join(m14_), ("h0dn_bg1_v410",))
    # (15) [v411, D80] a chamada do h0dn_fontes_hms13_v410 sai do main (a linha traz comentario: troca por prefixo); (16) a instrucao do hms13 trocada de lugar com a do iald2/h0dn reprova (o insumo h0dn_bg1_v410 passa a vir depois)
    _lf = [i for i, l in enumerate(linhas) if re.match(r"\s+_f410 = h0dn_fontes_hms13_v410\(core\)", l)]; assert len(_lf) == 1, ("a linha da chamada do h0dn_fontes_hms13_v410 nao foi achada uma vez", _lf)
    m15_ = list(linhas); m15_[_lf[0]] = m15_[_lf[0]].replace("h0dn_fontes_hms13_v410(core)", "{}", 1)
    r14 = ordem_de_chamada("\n".join(m15_), ("h0dn_fontes_hms13_v410",))
    r15 = ordem_de_chamada(_troca_blocos(src, "h0dn_bg1_v410", "h0dn_fontes_hms13_v410"), ("h0dn_fontes_hms13_v410",))
    f15_ = r15["funcoes"].get("h0dn_fontes_hms13_v410") or {}
    # (17) [v411, D86] a chamada do a_escala_v410 sai do main (a linha traz comentario: troca por prefixo)
    _la = [i for i, l in enumerate(linhas) if re.match(r"\s+_a410 = a_escala_v410\(core\)", l)]; assert len(_la) == 1, ("a linha da chamada do a_escala_v410 nao foi achada uma vez", _la)
    m17_ = list(linhas); m17_[_la[0]] = m17_[_la[0]].replace("a_escala_v410(core)", "{}", 1)
    r16 = ordem_de_chamada("\n".join(m17_), ("a_escala_v410",))
    # (18) [v411] a instrucao do h0dn_bg1_v411 trocada de lugar com a do hms13: o h0dn v412 passa a vir ANTES do bloco da v411
    r17 = ordem_de_chamada(_troca_blocos(src, "h0dn_fontes_hms13_v410", "h0dn_bg1_v411"), ("h0dn_bg1_v411",))
    f17_ = r17["funcoes"].get("h0dn_bg1_v411") or {}
    # (19) [v411] a chamada do h0dn_bg1_v411 sai do main (a linha e' `_h411 = h0dn_bg1_v411(core)`: troca por prefixo)
    _l11 = [i for i, l in enumerate(linhas) if re.match(r"\s+_h411 = h0dn_bg1_v411\(core\)", l)]; assert len(_l11) == 1, ("a linha da chamada do h0dn_bg1_v411 nao foi achada uma vez", _l11)
    m19_ = list(linhas); m19_[_l11[0]] = m19_[_l11[0]].replace("h0dn_bg1_v411(core)", "{}", 1)
    r18 = ordem_de_chamada("\n".join(m19_), ("h0dn_bg1_v411",))
    c = {"intacta_passa": bool(r0["ok"]), "ponte_antes_da_projecao_reprova": bool(not r1["ok"] and "projecao_transversal_v404" in ((r1["funcoes"].get("ponte_da_massa_v405") or {}).get("lidos_antes_da_atribuicao") or []) + ((r1["funcoes"].get("ponte_da_massa_v405") or {}).get("insumos_exigidos_ausentes") or [])),
         "chave_sem_origem_reprova": bool(not r2["ok"]),
         "fechamento_antes_dos_specs_da_v408_reprova": bool(not r3["ok"] and "_v405_rodar_specs" in (f3_.get("insumos_exigidos_ausentes") or [])), "fechamento_sem_chamada_no_main_reprova": bool(not r4["ok"] and "erro" in (r4["funcoes"].get("fechamento_v406") or {})),
         "psion_antes_do_fechamento_reprova": bool(not r5["ok"] and "fechamento_v406" in (f5_.get("insumos_exigidos_ausentes") or [])), "psion_sem_chamada_no_main_reprova": bool(not r6["ok"] and "erro" in (r6["funcoes"].get("psion_canto_v407") or {})),
         "tetelestai_antes_do_psion_reprova": bool(not r7["ok"] and "psion_canto_v407" in (f7_.get("insumos_exigidos_ausentes") or [])), "tetelestai_sem_chamada_no_main_reprova": bool(not r8["ok"] and "erro" in (r8["funcoes"].get("tetelestai_terminal_v408") or {})),
         "traducao_antes_do_terminal_reprova": bool(not r9["ok"] and "tetelestai_terminal_v408" in (f9_.get("insumos_exigidos_ausentes") or [])), "traducao_sem_chamada_no_main_reprova": bool(not r10["ok"] and "erro" in (r10["funcoes"].get("traducao_turing_v409") or {})),
         "iald2_antes_da_traducao_reprova": bool(not r11["ok"] and "traducao_turing_v409" in (f11_.get("insumos_exigidos_ausentes") or [])), "iald2_sem_chamada_no_main_reprova": bool(not r12["ok"] and "erro" in (r12["funcoes"].get("iald2_v410") or {})),
         "h0dn_sem_chamada_no_main_reprova": bool(not r13["ok"] and "erro" in (r13["funcoes"].get("h0dn_bg1_v410") or {})),
         "hms13_sem_chamada_no_main_reprova": bool(not r14["ok"] and "erro" in (r14["funcoes"].get("h0dn_fontes_hms13_v410") or {})), "hms13_antes_do_h0dn_reprova": bool(not r15["ok"] and "h0dn_bg1_v410" in (f15_.get("insumos_exigidos_ausentes") or [])),
         "aescala_sem_chamada_no_main_reprova": bool(not r16["ok"] and "erro" in (r16["funcoes"].get("a_escala_v410") or {})),
         "h0dn_v412_antes_do_hms13_reprova": bool(not r17["ok"] and "h0dn_fontes_hms13_v410" in (f17_.get("insumos_exigidos_ausentes") or [])), "h0dn_v412_sem_chamada_no_main_reprova": bool(not r18["ok"] and "erro" in (r18["funcoes"].get("h0dn_bg1_v411") or {}))}
    c["ok"] = bool(c["intacta_passa"] and all(v for k, v in c.items() if k != "intacta_passa"))
    return c


# ---------------------------------------------------------------- (v412) os QUATRO registros por especificacao: a ordem de chamada de _v412_rodar_specs(core)
CHAMADA_SPECS_V412 = "_v412_rodar_specs(core)"
EXIGIDOS_DOS_SPECS_V412 = INSUMOS_EXIGIDOS["h0dn_bg1_v411"] + ("h0dn_bg1_v411", "_v411_rodar_specs")   # o bloco da v411 INTEIRO (o registro com funcao e os specs) roda antes; os specs da v412 leem o veredito do H0DN e o gate


def specs_do_programa(src):
    """os specs da v412, lidos do TEXTO do programa por AST (a atribuicao literal de _V412_SPECS): nada executa."""
    for n in ast.parse(src).body:
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "_V412_SPECS" for t in n.targets):
            return ast.literal_eval(n.value)
    raise AssertionError("_V412_SPECS nao achado no programa")


def raizes_lidas_pelos_specs(specs):
    """a raiz de cada caminho de checagem (onde == 'core') mais as chaves que o proprio motor le; os nomes dos specs ficam de fora (os grava _v412_rodar_specs). Devolve (raizes, nomes, n_checagens_examinadas)."""
    nomes = {s["nome"] for s in specs} | {"guarda_frases_v412"}   # (as chaves que o PROPRIO _v412_rodar_specs grava: os registros e o resultado da travessia da guarda de frases, lido pelas checagens h8 e h9)
    raizes, n = {}, 0
    for s in specs:
        for ck in s["checks"]:
            n += 1
            if ck.get("onde") == "core" and ck.get("caminho"):
                raizes.setdefault(ck["caminho"][0], set()).add(s["nome"] + "." + ck["id"])
            elif ck.get("onde") == "kf":
                raizes.setdefault("kernel_formalization", set()).add(s["nome"] + "." + ck["id"])
    return {k: sorted(v) for k, v in raizes.items() if k not in nomes}, nomes, n


def ordem_dos_specs(src, specs, chamada=CHAMADA_SPECS_V412, exigidos=EXIGIDOS_DOS_SPECS_V412, raizes_extras=()):
    """toda chave do core que as checagens dos specs LEEM (a raiz do caminho) e que o motor (_v392_registro) le esta pronta ANTES da instrucao do main que chama _v412_rodar_specs(core): vem de run_um, de core["K"] = ... ou de K(core) numa instrucao anterior.
    Examina ZERO checagens = falha visivel. Estatica (AST); nada executa."""
    tree = ast.parse(src)
    defs = {}
    for n in tree.body:
        if isinstance(n, ast.FunctionDef):
            defs.setdefault(n.name, []).append(n)
    assert defs.get("main") and len(defs.get("run_um") or []) == 1 and len(defs.get("_v392_registro") or []) == 1, "main, run_um ou _v392_registro ausente/duplicado"
    main = defs["main"][-1]
    de_run = _chaves_de_run_um(defs["run_um"][0])
    unp = [ast.unparse(st) for st in main.body]
    atrib = {}
    for i, st in enumerate(main.body):
        for n in ast.walk(st):
            if isinstance(n, ast.Assign):
                for t in n.targets:
                    k = _chave_core(t)
                    if k is not None:
                        atrib.setdefault(k, i)
        for nome in re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\(core\)", unp[i]):
            atrib.setdefault(nome, i)
    ch = [i for i, s in enumerate(unp) if chamada in s]
    if len(ch) != 1:
        return {"ok": False, "erro": "chamada no main ausente ou nao unica", "indices": ch}
    ic = ch[0]
    raizes, nomes, n_ck = raizes_lidas_pelos_specs(specs)
    lidas = (set(raizes) | set(raizes_extras) | lidas_em(defs["_v392_registro"][0])) - nomes
    antes = sorted(k for k in lidas if k in atrib and atrib[k] >= ic and k not in de_run)
    sem_origem = sorted(k for k in lidas if k not in atrib and k not in de_run)
    faltam = [k for k in exigidos if not ((k in atrib and atrib[k] < ic) or k in de_run)]
    return {"ok": bool(n_ck > 0 and lidas and not antes and not sem_origem and not faltam), "n_checagens_examinadas": n_ck, "n_specs": len(specs), "chamada": {"indice": ic, "linha": main.body[ic].lineno}, "n_chaves_lidas": len(lidas), "chaves_lidas": sorted(lidas),
            "lidos_antes_da_atribuicao": antes, "lidas_sem_origem": sem_origem, "insumos_exigidos_ausentes": faltam}


def controle_negativo_specs(src, specs):
    """(a) a instrucao dos specs movida para ANTES do run_um reprova (leitura antes da atribuicao); (b) a chamada retirada do main reprova (nunca ok por omissao); (c) a instrucao dos specs trocada de lugar com a do h0dn_bg1_v411 reprova, e o motivo e' o insumo exigido ausente;
    (d) uma chave sem origem, lida por uma checagem, reprova; (e) a fonte intacta passa; (f) sem checagem nenhuma o resultado reprova (zero examinadas nao e' passagem). Rodado sobre o texto: nada executa."""
    r0 = ordem_dos_specs(src, specs)
    lin = src.split("\n")
    main = [x for x in ast.parse(src).body if isinstance(x, ast.FunctionDef) and x.name == "main"][-1]
    unp = [ast.unparse(st) for st in main.body]
    irun = [i for i, st in enumerate(main.body) if "run_um(" in unp[i] and isinstance(st, ast.Assign)][0]
    ic = [i for i, s in enumerate(unp) if CHAMADA_SPECS_V412 in s][0]
    st = main.body[ic]
    bloco = lin[st.lineno - 1:st.end_lineno]; dest = main.body[irun].lineno - 1
    ra = ordem_dos_specs("\n".join(lin[:dest] + bloco + lin[dest:st.lineno - 1] + lin[st.end_lineno:]), specs)
    rb = ordem_dos_specs(_sem_chamada(src, "_v412_rodar_specs", "_n412"), specs)
    rc = ordem_dos_specs(_troca_blocos(src, "h0dn_bg1_v411", "_v412_rodar_specs"), specs)
    rd = ordem_dos_specs(src, specs, raizes_extras=("chave_que_nao_existe_v412",))
    re_ = ordem_dos_specs(src, [])
    c = {"intacta_passa": bool(r0["ok"]), "specs_antes_do_run_um_reprova": bool(not ra["ok"] and ra.get("lidos_antes_da_atribuicao")), "specs_sem_chamada_no_main_reprova": bool(not rb["ok"] and rb.get("erro") == "chamada no main ausente ou nao unica"),
         "specs_antes_do_h0dn_da_v411_reprova": bool(not rc["ok"] and ("h0dn_bg1_v411" in (rc.get("lidos_antes_da_atribuicao") or []) or "h0dn_bg1_v411" in (rc.get("insumos_exigidos_ausentes") or []))),
         "chave_sem_origem_reprova": bool(not rd["ok"] and "chave_que_nao_existe_v412" in (rd.get("lidas_sem_origem") or [])), "zero_checagens_reprova": bool(not re_["ok"])}
    c["ok"] = bool(all(c.values()))
    return c


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    p = sys.argv[1]; fns = tuple(sys.argv[2:]) or FUNCOES_V412
    src_ = open(p, encoding="utf-8").read()
    r = ordem_de_chamada(src_, fns)
    resumo = {"arquivo": p, "ok": r["ok"], "funcoes": {k: {"ok": v.get("ok"), "chamada": v.get("chamada"), "n_chaves_lidas": v.get("n_chaves_lidas"), "lidos_antes_da_atribuicao": v.get("lidos_antes_da_atribuicao"), "lidas_sem_origem": v.get("lidas_sem_origem"), "insumos_exigidos_ausentes": v.get("insumos_exigidos_ausentes"), "insumos_exigidos_atribuidos_antes_no_main": v.get("insumos_exigidos_atribuidos_antes_no_main"), "erro": v.get("erro")} for k, v in r["funcoes"].items()}}
    print(json.dumps(resumo, ensure_ascii=False, indent=1))
    ctl = controle_negativo(src_) if fns == FUNCOES_V412 else None
    specs_ = specs_do_programa(src_); r_specs = ordem_dos_specs(src_, specs_); ctl_specs = controle_negativo_specs(src_, specs_)
    print(json.dumps({"ordem_dos_specs_v412": {k: v for k, v in r_specs.items() if k != "chaves_lidas"}, "controle_negativo_specs": ctl_specs}, ensure_ascii=False))
    if ctl is not None:
        print(json.dumps({"controle_negativo": ctl}, ensure_ascii=False))
    _aqui = os.path.dirname(os.path.abspath(__file__))
    try:   # (v412) a saida vai para DL.saida (a pasta da cadeia, ou a de ensaio com V412_ENSAIO_TOPO_PROPOSTO=1)
        sys.path.insert(0, _aqui); import delta_v412 as _DL11
        _out = _DL11.saida("GUARDA_ORDEM_DE_CHAMADA_v412.json")
    except Exception:   # noqa: BLE001 (sem o delta, ao lado do script, como na v411)
        _out = os.path.join(_aqui, "GUARDA_ORDEM_DE_CHAMADA_v412.json")
    json.dump({"arquivo": p, "funcoes_conferidas": list(fns), "ordem_de_chamada": r, "controle_negativo": ctl, "ordem_dos_specs_v412": r_specs, "controle_negativo_specs": ctl_specs}, open(_out + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(_out + ".tmp", _out)
    sys.exit(0 if r["ok"] and (ctl is None or ctl["ok"]) and r_specs["ok"] and ctl_specs["ok"] else 1)
