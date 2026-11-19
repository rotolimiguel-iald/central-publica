# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: as emendas de COMENTARIO pedidas pelo parecer da ordem 034 (REVISAO_034_Y2_Codex.md e _Y3_) em tres fontes
da lista final, nas copias de trabalho de pedras_novas\\ (as copias congeladas em insumos\\pedras_r11 ficam como registro):
- OPolinomioFixoEBeta: a docstring de polinomioFixo passa a dizer limiar real suficiente (Y2, necessario), com o orcamento inteiro
  uniforme floor(p(n)) + 1 e sem minimalidade;
- OCustoEAIsometria: o titulo e o item 1 trocam "nem mais, nem menos" pela exatidao do limiar (Y2, necessario); o item 4 ganha o custo
  pagando um por ato (Y2, opcional);
- AClausulaExemplificativa: a docstring isolada de o_fecho_exemplificativo repete a condicao que o tipo ja' traz (Y3).
Trocas exatas; confere que o codigo e' identico ao da fonte do autor (pedras_novas\\origem). Grava pedras_novas\\EMENDAS_DO_PARECER_034.json.
Uso: nona_lista_passo2h_emendas_do_parecer_034.py [--executar]"""
import hashlib, json, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; D = V / "pedras_novas"; O = D / "origem"; R11 = V / "insumos" / "pedras_r11"; EXEC = "--executar" in sys.argv
h = lambda b: hashlib.sha256(b).hexdigest()
TROCAS = {
 "OPolinomioFixoEBeta": [
  ("/-- [DEF] O POLINÔMIO FIXO DA LEITURA: o número de passos que fecha o ciclo, em função da carga, com o β fixado\nantes de toda fórmula. -/",
   "/-- [DEF] O POLINÔMIO FIXO DA LEITURA: o limiar real suficiente acima do qual qualquer número inteiro de passos fecha\no ciclo, em função da carga, com o β fixado antes de toda fórmula. Um orçamento inteiro uniforme é `⌊p(n)⌋ + 1`; o\ntipo não afirma que esse orçamento seja o mínimo. -/"),
 ],
 "OCustoEAIsometria": [
  ("# O custo é a carga, a isometria: decidir custa a carga, nem mais, nem menos",
   "# O custo é a carga, a isometria: a carga é o limiar exato do tempo da leitura que decide toda fórmula"),
  ("1. ★ `o_custo_de_decidir_e_a_carga`: decidir custa a carga — a leitura decide para toda fórmula se e somente se o\n   tempo pago passa da carga, nem mais, nem menos (é `AContagemEACarga.a_contagem_e_a_carga_para_formulas`).",
   "1. ★ `o_custo_de_decidir_e_a_carga`: a carga é o limiar exato — a leitura decide para toda fórmula se e somente se o\n   tempo pago passa da carga; com o tempo igual à carga, já há fórmula que ela não decide (é\n   `AContagemEACarga.a_contagem_e_a_carga_para_formulas`)."),
  ("   `(|φ| + 2)·n·ln 2`. Que cada ato sobre o todo pague a carga é a lei do custo, tomada como entrada; a conta é a de\n   `Token2.o_custo_pela_lei_e_polinomial`.",
   "   `(|φ| + 2)·n·ln 2`; pagando um por ato, o custo total é o próprio número de atos, `|φ| + 2`. Que cada ato sobre o\n   todo pague a carga é a lei do custo, tomada como entrada; a conta é a de `Token2.o_custo_pela_lei_e_polinomial`."),
 ],
 "AClausulaExemplificativa": [
  ("/-- ★★ **O FECHO EXEMPLIFICATIVO**: a cláusula é exemplificativa (um literal que se encaixa basta); o caput não\nesgota a variável; a verdade se lê no contorno; e a leitura não é cem por cento em tempo finito. -/",
   "/-- ★★ **O FECHO EXEMPLIFICATIVO**: a cláusula é exemplificativa (um literal que se encaixa basta); o caput não\nesgota a variável; a verdade se lê no contorno; e, havendo uma atribuição de custo não nulo em que o vetor tem\namplitude não nula, a trava não chega à projeção em tempo finito (com `v = 0`, a trava e a projeção coincidem). -/"),
 ],
}
RESTOS = {"OPolinomioFixoEBeta": ["o número de passos que fecha o ciclo, em função"], "OCustoEAIsometria": ["nem mais, nem menos"], "AClausulaExemplificativa": ["e a leitura não é cem por cento em tempo finito. -/"]}  # o item 5 do cabecalho segue com a frase, com a hipotese do item 4


def sem_comentarios(t):  # a mesma funcao dos passos 2f e 2g
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


rec = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "parecer": ["revisao_orquestrador\\REVISAO_034_Y2_Codex.md", "revisao_orquestrador\\REVISAO_034_Y3_Codex.md"],
       "trocas_exatas": {}, "sha256_antes_r11": {}, "sha256_depois": {}}
novos = {}
for nome, trocas in TROCAS.items():
    f = D / (nome + ".lean"); t = f.read_bytes().decode("utf-8"); orig = (O / (nome + ".lean")).read_bytes().decode("utf-8")
    r11 = (R11 / (nome + ".lean")).read_bytes()
    if all(t.count(nv) == 1 and t.count(vl) == 0 for vl, nv in trocas):
        print(nome, "| ja' aplicado")
    else:
        assert f.read_bytes() == r11, nome + ": a copia de trabalho nao e' a R11"
        for vl, nv in trocas:
            assert t.count(vl) == 1, (nome, t.count(vl), vl[:60]); t = t.replace(vl, nv)
    assert sem_comentarios(orig) == sem_comentarios(t), nome + ": codigo difere da fonte do autor"
    for r in RESTOS[nome]:
        assert r not in t, nome + ": sobrou " + r
    novos[nome] = t.encode("utf-8")
    rec["trocas_exatas"][nome] = [list(x) for x in trocas]; rec["sha256_antes_r11"][nome] = h(r11); rec["sha256_depois"][nome] = h(novos[nome])
    print(nome, "| codigo identico ao do autor | bytes", len(r11), "->", len(novos[nome]), "| sha16", h(novos[nome])[:16], "| trocas", len(trocas))
if EXEC:
    for nome, b in novos.items():
        f = D / (nome + ".lean")
        if f.read_bytes() != b:
            tmp = f.with_name(f.name + ".tmp_c1"); tmp.write_bytes(b); assert tmp.stat().st_size == len(b); tmp.replace(f)
    p = D / "EMENDAS_DO_PARECER_034.json"; assert not p.exists(), "recibo ja' existe"
    p.write_bytes(json.dumps(rec, ensure_ascii=False, indent=1).encode("utf-8")); print("gravado:", p.name)
