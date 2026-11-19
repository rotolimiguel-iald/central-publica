# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: a pagina R18 = a R17 mais duas linhas na tabela do leitor da formula (as duas pedras que entraram por
ordem do autor depois do corte: a clausula exemplificativa; a fita e o indice) e duas definicoes da teoria na frase de fecho do
bloco. Trocas exatas (cada marca casa UMA vez). Confere, linha a linha da tabela, que cada termo citado e' theorem/lemma em algum dos
modulos da propria linha (fontes de pedras_novas\\). Com --executar grava o_que_fica_claro_REV18\\O_QUE_FICA_CLARO_v412_R18.md."""
import hashlib, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
t = (V / "o_que_fica_claro_REV17" / "O_QUE_FICA_CLARO_v412_R17.md").read_bytes().decode("utf-8")
ANTES = "| mesma curva, conteúdos distintos |"
NOVAS = ("| a cláusula é exemplificativa: basta um literal que se encaixe | `a_clausula_e_exemplificativa`: a cláusula vale se e só se algum literal vale. `o_caput_nao_esgota_a_variavel`: o literal só lê a sua variável. `a_verdade_e_lida_no_contorno` e `a_leitura_nao_e_cem_por_cento_em_tempo_finito`: a trava do custo tende à projeção sobre as soluções e, havendo amplitude fora delas, não a atinge em tempo finito | `AClausulaExemplificativa` |\n"
         "| a fita é o índice: toda posição tem de ser lida, e o mesmo nome leva o mesmo valor | `quem_nao_visita_nao_le`: um leitor cego a uma posição dá a mesma resposta a duas fitas de respostas opostas; é a cota de ler a entrada inteira. `sat_formulaDa` e `a_coreferencia_obriga_o_transporte`: numa família de duas cláusulas unitárias sobre a mesma variável, há solução se e só se as duas posições lidas concordam | `AFitaEOIndice` |\n")
FECHO_VELHO = "que a curva seja a releitura e que a recusa seja um nome com conteúdo são definições da teoria, que entram como entrada."
FECHO_NOVO = "que a curva seja a releitura, que a recusa seja um nome com conteúdo, que a verdade seja o contorno e que a fita seja o índice e a torre são definições da teoria, que entram como entrada."
for marca in (ANTES, FECHO_VELHO):
    assert t.count(marca) == 1, "%d ocorrencias: %s" % (t.count(marca), marca[:60])
t = t.replace(ANTES, NOVAS + ANTES).replace(FECHO_VELHO, FECHO_NOVO)
ini = t.index("**O leitor da fórmula.** Definição da teoria"); fim = t.index("O que esta seção não diz: que o kernel decida")
bloco = t[ini:fim]; linhas = [l for l in bloco.split("\n") if l.startswith("| ") and not l.startswith("| o que se afirma")]
n_termos = 0
for l in linhas:
    cols = [c.strip() for c in l.strip().strip("|").split("|")]
    assert len(cols) == 3, l[:80]
    termos = re.findall(r"`([a-z][a-z0-9_]+)`", cols[1]); mods = re.findall(r"`([A-Za-z][A-Za-z0-9_]+)`", cols[2])
    if cols[2] == "—":
        assert not termos; continue
    assert termos and mods, l[:80]
    for x in termos:
        assert [m for m in mods if re.search(r"^(?:theorem|lemma)\s+%s(?![A-Za-z0-9_'])" % re.escape(x), (V / "pedras_novas" / (m + ".lean")).read_text(encoding="utf-8"), flags=re.M)], "termo %s nao e' theorem/lemma em %s" % (x, mods)
        n_termos += 1
assert "«" not in bloco and "ráculo" not in bloco and "P = nP" not in bloco and "Turing" not in bloco
b = t.encode("utf-8")
print("linhas de conteudo da tabela:", len(linhas), "| termos conferidos:", n_termos, "| R18", len(b), "B | sha16", hashlib.sha256(b).hexdigest()[:16])
if "--executar" in sys.argv:
    d = V / "o_que_fica_claro_REV18"; d.mkdir(exist_ok=True); p = d / "O_QUE_FICA_CLARO_v412_R18.md"
    assert not p.exists(), "ja' existe: nao sobrescrevo"
    p.write_bytes(b); print("gravado:", p)
