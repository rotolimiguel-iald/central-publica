# -*- coding: utf-8 -*-
"""e3_patch_exame_v412.py -- adapta exame_pontos_v412.py (backup .bak_20261117_antes_do_patch_e3, feito antes): (1) a instrucao do main que chama _v412_rodar_specs(core) fica DEPOIS da do h0dn_bg1_v411 (heranca) e IMEDIATAMENTE antes de emit_figures
(a posicao do h0dn deixa de ser a ultima); (2) o PONTO NOVO (4j): os quatro registros por especificacao no ponto de chamada real; (3) os registros da v412 entram na lista dos recriados pelo bloco. Idempotente (para se o ponto novo ja' esta). Script da cadeia."""
import hashlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "exame_pontos_v412.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
if "ponto_specs_v412" in s:
    print("ja' adaptado"); sys.exit(0)


def troca(old, new, n=1):
    global s
    assert s.count(old) == n, (old[:100], s.count(old))
    s = s.replace(old, new)


troca("list(um._V411_NOMES_REGISTROS):   # (v409:", "list(um._V411_NOMES_REGISTROS) + list(um._V412_NOMES_REGISTROS):   # (v412: + os quatro registros por especificacao) (v409:")
troca('ih11 = [i for i, s_ in enumerate(unp) if "h0dn_bg1_v411(core)" in s_]', 'ih11 = [i for i, s_ in enumerate(unp) if "h0dn_bg1_v411(core)" in s_]\niv12 = [i for i, s_ in enumerate(unp) if "_v412_rodar_specs(core)" in s_]   # (v412) os quatro registros por especificacao: a instrucao seguinte a do h0dn_bg1_v411, imediatamente antes de emit_figures')
troca("and len(ih11) == 1 and ih11[0] == ihm[0] + 1 and ih11[0] + 1 == i1, (", "and len(ih11) == 1 and ih11[0] == ihm[0] + 1 and len(iv12) == 1 and iv12[0] == ih11[0] + 1 and iv12[0] + 1 == i1, (")
troca("[h0dn_bg1_v411, specs v412] -> emit_figures nao e' a das instrucoes do main\", ifch, ipc, itt, itu, iia, ihm, ih11, i1)", "[h0dn_bg1_v411 (HERDADO), specs v411] -> [specs v412] -> emit_figures nao e' a das instrucoes do main\", ifch, ipc, itt, itu, iia, ihm, ih11, iv12, i1)")
troca("ih11 = ih11[0]", "ih11 = ih11[0]; iv12 = iv12[0]")
troca('"logo_antes_do_emit_figures": ih11 + 1 == i1,', '"logo_antes_da_instrucao_dos_specs_da_v412": ih11 + 1 == iv12 and iv12 + 1 == i1,')
troca('not p11.get("logo_antes_do_emit_figures")', 'not p11.get("logo_antes_da_instrucao_dos_specs_da_v412")')
ancora = 'out["core." + DL.FECHO_REGISTRO] = {"all_verified": h11.get("all_verified"), "verdict": str(h11.get("verdict"))[:300], "falhas": R["ponto_h0dn_v412"]["mecanica"]["falhos"]}'
novo = ancora + '''
# (4j) [v412] o PONTO DE CHAMADA REAL dos quatro registros por especificacao (executado dentro do bloco acima): a instrucao do main LOGO DEPOIS da do h0dn_bg1_v411 (o bloco da v411 inteiro ja' rodou) e IMEDIATAMENTE antes de emit_figures; o motor e' o da v392
#      (nenhum registro com funcao novo); o veredito e' a palavra do CONTRATO (lida pelo delta); o numero de checagens e' o do spec (zero nao passa); nenhuma chave antiga mudada pelo bloco
_pv12 = {}
for _n12 in DL.REGISTROS_SPEC_V412:
    _r12 = core.get(_n12) or {}; _s12 = [s_ for s_ in um._V412_SPECS if s_["nome"] == _n12][0]
    _pv12[_n12] = {"all_verified": _r12.get("all_verified"), "verdict": _r12.get("verdict"), "palavra_do_contrato": DL.PALAVRAS_DE_VEREDITO[_n12], "n_checks": len(_r12.get("checks") or []), "n_checks_do_spec": len(_s12["checks"]),
                   "checks_falhos": [str(c_.get("descricao"))[:80] for c_ in (_r12.get("checks") or []) if not c_.get("ok")][:4], "kernel": _r12.get("kernel"), "does_not_gate_core": _r12.get("does_not_gate_core")}
    out["core." + _n12] = {"all_verified": _r12.get("all_verified"), "verdict": str(_r12.get("verdict"))[:300], "falhas": _pv12[_n12]["checks_falhos"]}
R["ponto_specs_v412"] = {"indice_no_main": iv12, "linha": main.body[iv12].lineno, "logo_depois_da_instrucao_do_h0dn_da_v411": iv12 == ih11 + 1, "logo_antes_do_emit_figures": iv12 + 1 == i1, "dentro_do_bloco_executado": i0 <= iv12 < i1,
                         "chama_so_os_specs_da_v412": "h0dn_bg1_v411(core)" not in unp[iv12] and "_v411_rodar_specs(core)" not in unp[iv12], "n_registros": len(_pv12), "registros": _pv12}'''
troca(ancora, novo)
troca('if R["troca_dita_v412"]["ok"] is not True: falsos.append("troca_dita_v412")', '''pv12_ = R["ponto_specs_v412"]   # (4j) o ponto NOVO da v412: os quatro registros por especificacao
if (not pv12_["logo_depois_da_instrucao_do_h0dn_da_v411"] or not pv12_["logo_antes_do_emit_figures"] or not pv12_["dentro_do_bloco_executado"] or not pv12_["chama_so_os_specs_da_v412"] or pv12_["n_registros"] != 4
        or any(v_["all_verified"] is not True or v_["verdict"] != v_["palavra_do_contrato"] or v_["n_checks"] != v_["n_checks_do_spec"] or v_["n_checks"] <= 0 or v_["checks_falhos"] or v_["does_not_gate_core"] is not True for v_ in pv12_["registros"].values())): falsos.append("ponto_specs_v412")
if R["troca_dita_v412"]["ok"] is not True: falsos.append("troca_dita_v412")''')
i = s.index("# [A ADAPTAR v412] SUBIDA"); j = s.index("\n", i)
s = s[:i] + "# [ADAPTADO v412, 17/11/2026, claude-construtor-v412-ensaio] a instrucao dos specs da v412 (_v412_rodar_specs) vem depois da do h0dn_bg1_v411 (herdado) e imediatamente antes de emit_figures; ponto novo (4j) dos quatro registros por especificacao; os registros da v412 entram nos recriados pelo bloco; o manifesto de diagnostico por variavel de ambiente (so' no ensaio de diagnostico)" + s[j:]
tmp = P + ".tmp"
open(tmp, "wb").write(s.encode("utf-8")); assert os.path.getsize(tmp) > len(raw)
os.replace(tmp, P)
print("exame_pontos_v412.py adaptado:", hashlib.sha256(open(P, "rb").read()).hexdigest()[:16])
