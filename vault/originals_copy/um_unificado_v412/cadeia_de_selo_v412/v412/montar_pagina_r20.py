# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: a pagina R20 = a R19 emendada pelo parecer da ordem 033 (REVISAO_033_X1_Codex.md, _X2_, _X4_): a linha da
fita (o teorema mede a dependencia da posicao designada; nao obriga a ler toda posicao nem da' cota de leitura); a classe dos dois
pivos no paragrafo de citacao; a frase de fecho do bloco (a torre e' a forma do indice); a definicao que forma a chamada seguinte na
linha da recusa; e, no paragrafo do Tetelestai, o polinomio fixo dos passos dado por beta (OPolinomioFixoEBeta). Trocas exatas.
Confere, linha a linha da tabela, cada termo como theorem/lemma num modulo da propria linha, agora tambem os nomes com maiuscula
(o contador da R16 a R18 pulava `sat_formulaDa`); confere os termos do paragrafo do Tetelestai e a definicao citada.
Com --executar grava o_que_fica_claro_REV20\\O_QUE_FICA_CLARO_v412_R20.md (nao sobrescreve)."""
import hashlib, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; N = V / "pedras_novas"
t = (V / "o_que_fica_claro_REV19" / "O_QUE_FICA_CLARO_v412_R19.md").read_bytes().decode("utf-8")
TROCAS = [
 ("| a fita é o índice: toda posição tem de ser lida, e o mesmo nome leva o mesmo valor | `quem_nao_visita_nao_le`: um leitor cego a uma posição dá a mesma resposta a duas fitas de respostas opostas; é a cota de ler a entrada inteira. `sat_formulaDa` e `a_coreferencia_obriga_o_transporte`: numa família de duas cláusulas unitárias sobre a mesma variável, há solução se e só se as duas posições lidas concordam | `AFitaEOIndice` |",
  "| a fita é o índice: a resposta depende da posição que a correferência designa, e o mesmo nome leva o mesmo valor | `quem_nao_visita_nao_le`: para p ≠ 0, um leitor insensível ao sinal em p confunde duas fitas desta família de duas cláusulas unitárias. `sat_formulaDa`: há solução se e só se f(0) = f(p); `a_coreferencia_obriga_o_transporte`: então toda testemunha atribui esse valor à variável 0. O termo não conta posições visitadas | `AFitaEOIndice` |"),
 ("cadeias binárias na ordem prometida, cláusulas binárias que começam por um de dois pivôs), e para a fórmula plana arbitrária",
  "cadeias binárias na ordem prometida, cláusulas binárias que começam por um de dois pivôs e terminam num nome fora dos dois), e para a fórmula plana arbitrária"),
 ("que a verdade seja o contorno e que a fita seja o índice e a torre são definições da teoria, que entram como entrada.",
  "que a verdade seja o contorno, que a fita seja o índice e que a torre seja a forma do índice são definições da teoria, que entram como entrada."),
 ("`inspect_some`: a recusa devolve uma ocorrência de cláusula violada do bloco que responde.",
  "`inspect_some`: a recusa devolve uma ocorrência de cláusula violada do bloco que responde; a definição `Codex.ClauseReply.run` usa essa ocorrência para formar a chamada seguinte."),
 ("bastam mais de n·ln 2/β passos, um número linear na carga (`bastam_passos_lineares`); com o passo de cem por cento,",
  "bastam mais de n·ln 2/β passos, um número linear na carga (`bastam_passos_lineares`): é o polinômio fixo dos passos, p(n) = (ln 2/β)·n, dado por β antes de qualquer fórmula e o mesmo teto para toda fórmula de n variáveis (`o_polinomio_fixo_e_beta`, `o_mesmo_teto_para_duas_formulas`); com o passo de cem por cento,"),
]
for velho, novo in TROCAS:
    assert t.count(velho) == 1, "%d ocorrencias: %s" % (t.count(velho), velho[:70])
    t = t.replace(velho, novo)
TERMO = re.compile(r"`([a-z][A-Za-z0-9_']*)`")
# 1) a tabela do bloco do leitor da formula, linha a linha
ini = t.index("**O leitor da fórmula.** Definição da teoria"); fim = t.index("**Tetelestai: a consumação do ciclo.**")
bloco = t[ini:fim]; linhas = [l for l in bloco.split("\n") if l.startswith("| ") and not l.startswith("| o que se afirma")]
n_termos = 0
for l in linhas:
    cols = [c.strip() for c in l.strip().strip("|").split("|")]
    assert len(cols) == 3, l[:80]
    termos = TERMO.findall(cols[1]); mods = re.findall(r"`([A-Za-z][A-Za-z0-9_]+)`", cols[2])
    if cols[2] == "—":
        assert not termos; continue
    assert termos and mods, l[:80]
    for x in termos:
        assert [m for m in mods if re.search(r"^(?:theorem|lemma)\s+%s(?![A-Za-z0-9_'])" % re.escape(x), (N / (m + ".lean")).read_text(encoding="utf-8"), flags=re.M)], "termo %s nao e' theorem/lemma em %s" % (x, mods)
        n_termos += 1
# 2) a definicao citada na linha da recusa
cr = (N / "ClausulaComoResposta.lean").read_text(encoding="utf-8")
assert re.search(r"^namespace Codex\.ClauseReply\s*$", cr, flags=re.M) and re.search(r"^def run\b", cr, flags=re.M)
# 3) o paragrafo do Tetelestai
par = [b for b in t.split("\n\n") if b.startswith("**Tetelestai: a consumação do ciclo.**")]; assert len(par) == 1
ONDE = {"ha_o_mecanismo": V / "insumos" / "pedras_r10" / "AMaquina.lean", "o_passo_um_menos_beta_fecha_o_ciclo": V / "insumos" / "pedras_r10" / "OPassoEOFim.lean",
        "bastam_passos_lineares": V / "insumos" / "pedras_r10" / "OPassoEOFim.lean", "com_o_passo_de_cem_por_cento_o_ciclo_nao_fecha": V / "insumos" / "pedras_r10" / "OPassoEOFim.lean",
        "o_nome_fica_inteiro": V / "insumos" / "pedras_r10" / "OPassoEOFim.lean", "a_trava_no_nome": Path(r"C:\t\k411c\final\TGLExt\TraducaoTuring.lean"),
        "o_polinomio_fixo_e_beta": N / "OPolinomioFixoEBeta.lean", "o_mesmo_teto_para_duas_formulas": N / "OPolinomioFixoEBeta.lean"}
assert set(TERMO.findall(par[0])) == set(ONDE), set(TERMO.findall(par[0])) ^ set(ONDE)
for termo, arq in ONDE.items():
    assert re.search(r"^(?:theorem|lemma)\s+%s(?![A-Za-z0-9_'])" % re.escape(termo), arq.read_text(encoding="utf-8"), flags=re.M), termo
for proibido in ("«", "ráculo", "toda posição tem de ser lida", "ler a entrada inteira"):
    assert proibido not in t, proibido
assert "P = nP" not in bloco and "Turing" not in bloco and "P = nP" not in par[0]
b = t.encode("utf-8")
print("trocas:", len(TROCAS), "| linhas da tabela:", len(linhas), "| termos da tabela conferidos:", n_termos, "| termos do Tetelestai:", len(ONDE), "| R20", len(b), "B | sha16", hashlib.sha256(b).hexdigest()[:16])
if "--executar" in sys.argv:
    d = V / "o_que_fica_claro_REV20"; d.mkdir(exist_ok=True); p = d / "O_QUE_FICA_CLARO_v412_R20.md"
    assert not p.exists(), "ja' existe: nao sobrescrevo"
    p.write_bytes(b); print("gravado:", p)
