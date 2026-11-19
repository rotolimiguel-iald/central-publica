# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: o metodo de 17/11 nos comentarios das duas pedras do Kimi que entraram por ordem do autor depois do corte
(AClausulaExemplificativa, AFitaEOIndice), nas copias de trabalho de pedras_novas\\. Sai quem perguntou, quem respondeu, a data, a
linha de estado, a nota do laco e o balanco; a leitura entra como definicao da teoria, com estatuto de entrada. Trocas por REGIAO
(do marcador de inicio, inclusive, ate' o marcador de fim, exclusive; cada marcador casa UMA vez) e trocas exatas. Depois confere que
o codigo e' identico ao da fonte do autor. Uso: nona_lista_passo2d_cabecalhos_das_duas_pedras_do_kimi.py [--executar]"""
import hashlib, json, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; D = V / "pedras_novas"; O = D / "origem"; EXEC = "--executar" in sys.argv
REGIOES = [  # (modulo, inicio inclusive, fim exclusive, novo)
 ("AClausulaExemplificativa", "[candidata do Kimi, 18/11/2026, R0;", "## O que fica provado",
  "## A leitura que este arquivo tipa\n\nA atribuição existe: é o contorno. A verdade é o contorno, e a variável faz a leitura da borda. A cláusula da fórmula\né exemplificativa, como a cláusula jurídica exemplificativa: o tipo (o caput) não esgota a variável e permite ler\nqualquer caso que nele se encaixe, ainda que não a cem por cento (`1 − β`), pela tangente do contorno [INPUT/ONTO:\ndefinição da teoria, entrada, não teorema]. Este arquivo prova a parte dela que cabe nos termos do kernel.\n\n"),
 ("AClausulaExemplificativa", "* Que a atribuição SEJA o contorno e que a verdade SEJA o contorno:", "-/\n\nnamespace TGLExt.AClausulaExemplificativa",
  "* Que a atribuição SEJA o contorno e que a verdade SEJA o contorno: essa identidade é definição da teoria\n  [INPUT/ONTO]; o que está em termo é que a resposta se lê no limite da borda do custo (a projeção sobre o Nome).\n* A analogia jurídica (taxativa e exemplificativa) nomeia as duas leituras da cláusula; é nome da teoria [INPUT/ONTO].\n* Nada sobre a contagem por letra do Instituto: a cota polinomial na fita para toda CNF plana segue aberta.\n* Nada sobre a natureza. Validade no kernel não é creditação.\n"),
 ("AFitaEOIndice", "[candidata do Kimi, 18/11/2026, R0;", "## O que fica provado",
  "## A leitura que este arquivo tipa\n\nNuma lista de cláusulas escrita na fita, a fita é o próprio índice da lista; e a torre é a forma do índice\n[INPUT/ONTO: definição da teoria, entrada, não teorema]. Este arquivo prova a parte dela que cabe nos termos do kernel.\n\n"),
 ("AFitaEOIndice", "* «A torre» e «a forma matricial da luz» são nomes do operador", "-/\n\nnamespace TGLExt.AFitaEOIndice",
  "* “A torre” é nome da teoria para a forma do índice [INPUT/ONTO]. O que está em termo é: a fita é a função das\n  posições às letras, toda posição tem de ser lida, e o transporte da correferência é obrigatório. Ler a forma do\n  índice como a forma matricial da luz é interpretação, não termo: a matriz-S da luz (o portador de `Psibit`) não é\n  ligada por termo ao índice da fita.\n* Nenhuma cota polinomial para a Palavra de toda CNF plana. A cota inferior deste arquivo é a de ler a entrada\n  inteira. Os limites de `LimiteDoLeitor` (o plano de ramos) e de `AParedeDoNome` (o estado por prefixo) são de\n  leitores e representações determinados. A pergunta do Instituto fica aberta.\n* Nada sobre a natureza.\n\nNOTA DO TIPO: as definições e os teoremas que nomeiam a posição `0` (`formulaDa`, `sat_formulaDa_cell`,\n`sat_formulaDa`, `quem_nao_visita_nao_le`, `a_coreferencia_obriga_o_transporte`) levam a instância `[NeZero L]`, porque\n`(0 : Fin L)` pede a fita não vazia. Ela é gratuita: `quem_nao_visita_nao_le` já traz `hp : p ≠ 0`, que só tem\nhabitante com `L ≥ 2`.\n"),
]
TROCAS = [
 ("AClausulaExemplificativa", "   qualquer estado (a pedra `CamadaCientifica` da gerência, aplicada ao custo da fórmula).", "   qualquer estado (`CamadaCientifica.a_trava_tende_ao_nome`, aplicado ao custo da fórmula)."),
 ("AClausulaExemplificativa", "(`jamais_esgotado`). O «ainda que não 100 %» é termo.", "(`CamadaCientifica.jamais_esgotado`). É o termo do “ainda que não a cem por cento” da leitura."),
 ("AClausulaExemplificativa", "/-- ★ **O CAPUT NÃO ESZGOTA A VARIÁVEL**", "/-- ★ **O CAPUT NÃO ESGOTA A VARIÁVEL**"),
 ("AClausulaExemplificativa", "(re-exportação da pedra da fronteira). -/", "(de `OResumoEPsiBit.satisfeita_so_ve_as_suas_variaveis`). -/"),
 ("AClausulaExemplificativa", "Nome — as atribuições de custo zero. É a pedra da camada científica da gerência, aplicada ao custo da fórmula. -/", "Nome — as atribuições de custo zero. É `CamadaCientifica.a_trava_tende_ao_nome`, aplicado ao custo da fórmula. -/"),
 ("AFitaEOIndice", "   nela, com respostas opostas, e o leitor cego lhes dá a mesma resposta. O índice se paga: cada letra é uma posição\n   do índice, e saltá-la é não lê-la.", "   nela, com respostas opostas, e o leitor cego lhes dá a mesma resposta. Toda posição do índice tem de ser lida."),
 ("AFitaEOIndice", "cego lhes dá a mesma resposta. O índice se paga. -/", "cego lhes dá a mesma resposta. -/"),
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


textos = {n: (D / (n + ".lean")).read_bytes().decode("utf-8") for n in ("AClausulaExemplificativa", "AFitaEOIndice")}
orig = {n: (O / (n + ".lean")).read_bytes().decode("utf-8") for n in textos}
ja = all(textos[n] != orig[n] for n in textos)
if not ja:
    for nome, ini, fim, novo in REGIOES:
        t = textos[nome]; assert t.count(ini) == 1 and t.count(fim) == 1, (nome, t.count(ini), t.count(fim), ini[:40])
        a, b = t.index(ini), t.index(fim); assert a < b, (nome, ini[:40])
        textos[nome] = t[:a] + novo + t[b:]
    for nome, velho, novo in TROCAS:
        t = textos[nome]; assert t.count(velho) == 1, (nome, t.count(velho), velho[:60])
        textos[nome] = t.replace(velho, novo)
for nome, t in textos.items():
    assert sem_comentarios(orig[nome]) == sem_comentarios(t), "codigo difere: " + nome
    for resto in ("«", "operador", "Kimi", "Codex", "gerência", "18/11", "LAÇO", "instalado", "Sem sorry", "a casa", "gate"):
        assert resto not in t, "sobrou em %s: %s" % (nome, resto)
    print(nome, "| codigo identico | bytes", len(orig[nome].encode("utf-8")), "->", len(t.encode("utf-8")), "| sha16", hashlib.sha256(t.encode("utf-8")).hexdigest()[:16])
if EXEC and not ja:
    for nome, t in textos.items():
        f = D / (nome + ".lean"); b = t.encode("utf-8"); tmp = f.with_name(f.name + ".tmp_c1"); tmp.write_bytes(b); tmp.replace(f)
    p = D / "EMENDAS_DAS_DUAS_PEDRAS_DO_KIMI.json"
    p.write_bytes(json.dumps({"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "regioes": [list(x) for x in REGIOES], "trocas_exatas": [list(x) for x in TROCAS],
                              "sha256_depois": {n: hashlib.sha256((D / (n + ".lean")).read_bytes()).hexdigest() for n in textos}}, ensure_ascii=False, indent=1).encode("utf-8"))
    print("gravado:", p.name)
