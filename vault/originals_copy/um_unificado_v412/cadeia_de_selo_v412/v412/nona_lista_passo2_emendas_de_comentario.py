# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: passo 2 da nona lista. Trocas EXATAS, so' em comentario e docstring, nas copias de trabalho de
pedras_novas\\ (o metodo de 17/11: sai quem disse, quando e em que revisao; fica o enunciado, a fonte por nome de modulo e o limite).
Cada troca tem de casar UMA vez. Depois confere, modulo a modulo, que o CODIGO (tudo fora de comentario e docstring) e' identico ao de
pedras_novas\\origem\\. Os cabecalhos das quatro pedras maiores foram refeitos antes, a mao, e passam pela mesma conferencia.
Uso: nona_lista_passo2_emendas_de_comentario.py [--executar]"""
import hashlib, json, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; D = V / "pedras_novas"; O = D / "origem"; EXEC = "--executar" in sys.argv
TROCAS = [
 ("ACurvaEAEstado", "## 2. Auxiliares do laço: a leitura", "## 2. Auxiliares: a leitura"),
 ("ACurvaEAEstado", "(auxiliar do laço)", "(auxiliar)"),
 ("CadeiasDeBolsas", "A hipótese em t é da REV65. -/", "A hipótese em t é a de `OPsibitEACompressao`. -/"),
 ("ConsultaPonderada", "uma célula do resumo de Kimi, em qualquer corte.", "uma célula do resumo de `OResumoEPsiBit`, em qualquer corte."),
 ("FitaComCusto", "sob o limiar pago da Palavra da REV65. -/", "sob o limiar pago da Palavra de `OPsibitEACompressao`. -/"),
 ("LeitorDaFormula", "/- Candidata isolada. Um ramo dispensado", "/- Um ramo dispensado"),
 ("LeiturasComFolga", "sobre a soma da candidata do passo 1 − β.", "sobre a soma de `OPassoEOFim` (o passo 1 − β)."),
 ("OResumoEPsiBit", "a soma lida da casa sobre o custo da fórmula", "a soma lida sobre o custo da fórmula"),
 ("PolinomioDoPsiBit", "Direct correspondence to Kimi's two channels at every real t.", "Direct correspondence to the two channels of `OPsiBitDaFormula` at every real t."),
 ("PontePalavraVerbo", "/-- Os dois bits da candidata calculados da sintaxe. -/", "/-- Os dois bits de `OPsibitEACompressao` calculados da sintaxe. -/"),
 ("ProjecaoDaFronteira", "A cell in the existing Kimi summary is exactly a fiber sum.", "A cell in the summary of `OResumoEPsiBit` is exactly a fiber sum."),
 ("sonda_cadeia_caminho", "# Sonda (não é candidata): a `Cadeia`", "# Sonda: a `Cadeia`"),
 ("sonda_cadeia_caminho", "Verifica, sobre a pedra já compilada:", "Verifica:"),
 ("sonda_n0_contraexemplo", "# Sonda (não é candidata): por que", "# Sonda: por que"),
 ("sonda_n0_contraexemplo", "Verificação formal do contraexemplo que fixou o enunciado de", "Verificação formal do contraexemplo que fixa em `CNF 1` o enunciado de"),
 ("sonda_n0_contraexemplo", "`TGLExt.OPsiBitDaFormula.o_par_e_necessario_e_suficiente_na_formula` em `CNF 1`.", "`TGLExt.OPsiBitDaFormula.o_par_e_necessario_e_suficiente_na_formula`."),
 ("sonda_n0_contraexemplo", "os dois controles existem — é o teorema da candidata.", "os dois controles existem — é o teorema de `OPsiBitDaFormula`."),
]


def sem_comentarios(t):
    out, i, n, prof = [], 0, len(t), 0
    while i < n:
        if t.startswith("/-", i):
            prof += 1; i += 2; continue
        if prof and t.startswith("-/", i):
            prof -= 1; i += 2; continue
        if prof:
            i += 1; continue
        if t.startswith("--", i):
            while i < n and t[i] != "\n":
                i += 1
            continue
        out.append(t[i]); i += 1
    return "\n".join(l.rstrip() for l in "".join(out).split("\n") if l.strip())


feitas = 0
for nome, velho, novo in TROCAS:
    f = D / (nome + ".lean"); t = f.read_bytes().decode("utf-8")
    if velho not in t:
        # ja' aplicada (as 17 casaram uma vez na primeira rodada, de 18/11) e, em FitaComCusto, emendada de novo pelo passo 2b
        continue
    assert t.count(velho) == 1, "%s: %d ocorrencias de %r" % (nome, t.count(velho), velho)
    feitas += 1
    if EXEC:
        b = t.replace(velho, novo).encode("utf-8"); tmp = f.with_name(f.name + ".tmp_c1"); tmp.write_bytes(b); tmp.replace(f)
print("trocas a fazer/feitas agora:", feitas, "de", len(TROCAS), "| executar:", EXEC)
rel, difere = [], []
for f in sorted(D.glob("*.lean")):
    o = O / f.name; assert o.exists(), "sem origem: " + f.name
    a, b = o.read_bytes(), f.read_bytes()
    igual_cod = sem_comentarios(a.decode("utf-8")) == sem_comentarios(b.decode("utf-8"))
    if not igual_cod:
        difere.append(f.name)
    rel.append({"modulo": f.stem, "sha256_origem": hashlib.sha256(a).hexdigest(), "sha256_trabalho": hashlib.sha256(b).hexdigest(),
                "bytes_iguais": a == b, "codigo_identico": igual_cod})
print("modulos:", len(rel), "| bytes iguais a' origem:", sum(r["bytes_iguais"] for r in rel), "| mudados so' em comentario:", sum((not r["bytes_iguais"]) and r["codigo_identico"] for r in rel), "| CODIGO DIFERE:", difere)
assert not difere
if EXEC:
    p = D / "EMENDAS_DE_COMENTARIO.json"; tmp = p.with_name(p.name + ".tmp_c1")
    tmp.write_bytes(json.dumps({"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "trocas_exatas": [list(x) for x in TROCAS],
                                "cabecalhos_refeitos_a_mao": ["OResumoEPsiBit", "OPsiBitDaFormula", "AFronteiraEOUnicoPortao", "ACurvaEAEstado"], "modulos": rel}, ensure_ascii=False, indent=1).encode("utf-8")); tmp.replace(p)
    print("gravado:", p.name)
