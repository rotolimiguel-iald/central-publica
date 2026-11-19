# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: as emendas de COMENTARIO pedidas pelo parecer da ordem 031 (REVISAO_031_U1/U2/U3_Codex.md e o recibo
031_RESULTADO.json), nas copias de trabalho de pedras_novas\\. Trocas exatas (cada marca casa UMA vez); depois confere que o codigo
de cada modulo e' identico ao da fonte do autor (pedras_novas\\origem). As copias congeladas em REV_031 e em insumos\\pedras_r9 nao
sao tocadas: o resultado vai numa lista nova. Uso: nona_lista_passo2b_emendas_do_parecer_031.py [--executar]"""
import hashlib, json, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; D = V / "pedras_novas"; O = D / "origem"; EXEC = "--executar" in sys.argv
GATE = ("* Nada sobre a natureza. Validade no kernel não é creditação; o gate não se move.", "* Nada sobre a natureza. Validade no kernel não é creditação.")
BAL = ("\n\nSem sorry, sem axioma novo.\n-/", "\n-/")
TROCAS = [
 # --- OResumoEPsiBit (U2: resumo por soma sobre atribuicoes completas; citar a transicao; fronteira plena; residuos)
 ("OResumoEPsiBit", "O que já estava tipado: o fator da cláusula", "Termos em que este arquivo se apoia: o fator da cláusula"),
 ("OResumoEPsiBit", "(`AContagemEACarga`). O que não tinha: a forma do resumo que a leitura carrega entre uma cláusula e a seguinte.",
  "(`AContagemEACarga`). O termo deste arquivo: a forma do resumo que a leitura carrega entre uma cláusula e a seguinte."),
 ("OResumoEPsiBit", "4. `a_fronteira_tem_duas_elevado_as_celulas`: a tabela do resumo tem `2^{|fronteira|}` células, não `2ⁿ`.",
  "4. `a_fronteira_tem_duas_elevado_as_celulas`: a tabela do resumo tem `2^{|fronteira|}` células; com a fronteira plena\n   são `2ⁿ` (item 7)."),
 ("OResumoEPsiBit", "5. ★★ `a_leitura_pela_fronteira_e_exata`: a soma lida inteira se obtém das células da fronteira — o resumo não perde\n   nada da resposta final (perda zero).",
  "5. ★★ `a_leitura_pela_fronteira_e_exata`: a soma lida inteira é a soma, célula a célula da fronteira, dos produtos do\n   peso lido pelo peso por ler das atribuições que caem na célula — agrupar pela fronteira não perde nada da soma. (A\n   soma simples das células do resumo dá a partição do prefixo: `ProjecaoDaFronteira.total_projection`.)"),
 ("OResumoEPsiBit", "6. ★ `a_atualizacao_pela_clausula_seguinte`: a cláusula seguinte atualiza o resumo em dois movimentos — estender às\n   variáveis novas pagando ou não pagando (o par da cláusula: 1 ou `e^{−t}`) e contrair as variáveis que saíram da\n   fronteira — e a forma registrada é que o resumo novo se escreve do velho mais o fator da cláusula lida.",
  "6. ★ `a_atualizacao_pela_clausula_seguinte`: o resumo depois da cláusula seguinte é a soma, sobre as atribuições que\n   caem na célula nova, do peso lido antes multiplicado pelo fator da cláusula (1 ou `e^{−t}`). A identidade é escrita\n   sobre atribuições completas: expande o peso pelo fator novo. A recorrência de tabela a tabela (estender às variáveis\n   novas e contrair as que saíram da fronteira) é `TransicaoDaFronteira.transition`."),
 ("OResumoEPsiBit", "lidas ainda partilham com as por ler. Em cada célula, a soma dos pesos lidos de todas as atribuições parciais que nela\ncaem.",
  "lidas ainda partilham com as por ler. Em cada célula, a soma dos pesos lidos de todas as atribuições que nela\ncaem."),
 ("OResumoEPsiBit", "**Como a cláusula seguinte o atualiza?** Em dois movimentos, os dois lados do par: estende a tabela às variáveis\nnovas, célula a célula pagando ou não pagando (o fator da cláusula, a lei dos dois valores), e contrai as variáveis\nque nenhuma cláusula futura toca mais (soma-se sobre elas: foram lidas até o fim). O resumo nunca toca as `2ⁿ`\natribuições: toca a fronteira.",
  "**Como a cláusula seguinte o atualiza?** Pelo fator dela: 1 se a cláusula é satisfeita, `e^{−t}` se não (a lei dos\ndois valores). Neste arquivo a identidade é escrita sobre atribuições completas. A regra que leva a tabela de uma\nfronteira à tabela da seguinte, estendendo às variáveis novas e contraindo as que nenhuma cláusula futura toca, é\n`TransicaoDaFronteira.transition`."),
 ("OResumoEPsiBit",) + GATE, ("OResumoEPsiBit",) + BAL,
 # --- OPsiBitDaFormula (U2/U3: regra fixa, nao unicidade entre regras; s > n ln 2; identidade escalar; residuos)
 ("OPsiBitDaFormula", "   (`x l.var == l.pos`); a regra é uma só e não tem a fórmula como entrada.",
  "   (`x l.var == l.pos`); a regra é fixa e não tem a fórmula como entrada (o termo não compara regras concorrentes)."),
 ("OPsiBitDaFormula", "3. ★ `a_palavra_e_lida_pela_soma`: a Palavra da fórmula (o Nome está habitado?) é lida pela soma, paga a carga",
  "3. ★ `a_palavra_e_lida_pela_soma`: a Palavra da fórmula (o Nome está habitado?) é lida pela soma, com o tempo pago\n   acima da carga, `s > n·ln 2`"),
 ("OPsiBitDaFormula", "6. ★ `o_par_da_formula_se_le_do_produto_dos_pares`: o par da fórmula lê-se do produto dos pares das cláusulas (a\n   função do gráviton, no sentido lido no cabeçalho: o par do par).",
  "6. ★ `o_par_da_formula_se_le_do_produto_dos_pares`: identidade escalar da soma lida: ela é a soma, sobre as\n   atribuições, do produto dos fatores das cláusulas. Os dois canais leem-se dela em separado, pelos termos da Palavra\n   (item 3) e da descida (item 4). Chamar a isso a função do gráviton, o par do par, é interpretação da teoria."),
 ("OPsiBitDaFormula",) + GATE, ("OPsiBitDaFormula",) + BAL,
 # --- AFronteiraEOUnicoPortao (U2/U3: o tipo conclui que a fronteira nao e' vazia; a pertinencia ao percurso e' de OSeparadorNoPercurso)
 ("AFronteiraEOUnicoPortao", "2. ★★ `a_fronteira_e_o_unico_portao`: toda cadeia de uma variável só-lida (está nas cláusulas lidas e em nenhuma por\n   ler) a uma só-por-ler passa pela fronteira. Não há atalho: quem sai do lido entra no por-ler atravessando a\n   fronteira.",
  "2. ★★ `a_fronteira_e_o_unico_portao`: havendo cadeia de uma variável só-lida (está nas cláusulas lidas e em nenhuma\n   por ler) a uma só-por-ler, a fronteira não é vazia: o termo exibe um vértice dela. O enunciado não registra que\n   esse vértice pertence à cadeia; a pertinência ao percurso é `OSeparadorNoPercurso.o_percurso_atravessa_a_fronteira`."),
 ("AFronteiraEOUnicoPortao", "   (`a_fronteira_basta_ao_resumo`) e a fronteira é o único portão do grafo — os dois juntos: a leitura da resposta\n   passa pela fronteira e por nada mais.",
  "   (`a_fronteira_basta_ao_resumo`) e, havendo a cadeia, a fronteira não é vazia — os dois juntos, num termo só."),
 ("AFronteiraEOUnicoPortao", "leitura repousa (o\nresumo é função das células dela). A porta é única porque o separador não se contorna: toda via de\ninformação do lido ao por-ler o atravessa.",
  "leitura repousa (o\nresumo é função das células dela). Que todo percurso do lido ao por-ler tenha um vértice na fronteira é o termo de\n`OSeparadorNoPercurso`; que ela seja o menor separador, ou o único, não está provado."),
 ("AFronteiraEOUnicoPortao",) + GATE, ("AFronteiraEOUnicoPortao",) + BAL,
 ("AFronteiraEOUnicoPortao", "/-- ★★ **A FRONTEIRA É O ÚNICO PORTÃO**: toda cadeia de uma variável só-lida a uma só-por-ler passa pela fronteira:\nhá um vértice da cadeia na fronteira. Prova por indução estrutural:",
  "/-- ★★ **A FRONTEIRA É O ÚNICO PORTÃO**: havendo cadeia de uma variável só-lida a uma só-por-ler, a fronteira tem um\nvértice (o enunciado não diz que ele está na cadeia; ver `OSeparadorNoPercurso`). Prova por indução estrutural:"),
 ("AFronteiraEOUnicoPortao", "/-- ★ **A LEITURA TEM UM SÓ PORTÃO**: o resumo da leitura mora na fronteira (pedra `OResumoEPsiBit`), e a fronteira é\no único portão do grafo da fórmula — a leitura da resposta passa por ela e por nada mais. -/",
  "/-- ★ **A LEITURA TEM UM SÓ PORTÃO**: o resumo da leitura é função das células da fronteira (`OResumoEPsiBit`), e,\nhavendo cadeia do só-lido ao só-por-ler, a fronteira não é vazia. -/"),
 # --- ACurvaEAEstado (U2/U3: exemplo em uma variavel; celulas distintas para t diferente de zero; projecao geral; residuos)
 ("ACurvaEAEstado", "2. ★ `mesma_curva_para_todo_tempo`: os dois prefixos têm a mesma curva inteira, para todo tempo (a obstrução de\n   `PalavrasResiduais`, provada de novo aqui nos termos de `OResumoEPsiBit`).",
  "2. ★ `mesma_curva_para_todo_tempo`: os dois prefixos têm a mesma curva inteira, para todo tempo (a obstrução de\n   `PalavrasResiduais`, nos termos de `OResumoEPsiBit`)."),
 ("ACurvaEAEstado", "para todo tempo. (A\nobstrução de `PalavrasResiduais`, provada de novo nos termos de `OResumoEPsiBit`.) -/", "para todo tempo. (A\nobstrução de `PalavrasResiduais`, nos termos de `OResumoEPsiBit`.) -/"),
 ("ACurvaEAEstado", "(Auxiliares, marcados como tais:", "Os itens 1 a 5 são provados no exemplo de uma variável (`CNF 1`); as células dos dois resumos diferem para `t ≠ 0`\n(em `t = 0` todos os fatores valem 1). A projeção do prefixo em qualquer número de variáveis é\n`ProjecaoDaFronteira.total_projection`.\n\n(Auxiliares, marcados como tais:"),
 ("ACurvaEAEstado",) + GATE, ("ACurvaEAEstado",) + BAL,
 # --- as duas sondas (residuo: balanco)
 ("sonda_cadeia_caminho", "\n\nSem sorry, sem axioma novo.", ""), ("sonda_n0_contraexemplo", "\n\nSem sorry, sem axioma novo.", ""),
 ("OPsiBitDaFormula", "decidível por `Fintype.decidableExistsFintype` nesta versão; a equivalência", "decidível por `Fintype.decidableExistsFintype`; a equivalência"),
 # --- AParedeDoNome (U1: a frase do alcance; processo e balanco vao ao recibo)
 ("AParedeDoNome", "4. ★★ `o_nome_exato_pede_dois_a_n_bits`: se o estado cabe em `p` bits, então `p ≥ 2ⁿ`. Nenhum resumo exato por cláusula\n   cabe em número de bits polinomial em `n`, para toda fórmula.",
  "4. ★★ `o_nome_exato_pede_dois_a_n_bits`: se o estado cabe em `p` bits, então `p ≥ 2ⁿ`. É a cota para um estado que\n   represente qualquer conjunto de atribuições e responda a toda continuação; há conjuntos particulares com descrição\n   curta."),
 ("AParedeDoNome", "* Nada sobre a natureza. O gate não se move.\n\nEstatutos: `[REAL no sandbox]` os termos · `[INPUT]` a lei · `[ONTO, leitura deste arquivo]` “nome” como o estado do\natualizador. Sem sorry, sem axiom.\n-/",
  "* Nada sobre a natureza.\n\nEstatutos: `[INPUT]` a lei · `[ONTO, leitura deste arquivo]` “nome” como o estado do atualizador.\n-/"),
 # --- dois comentarios do Codex com palavra de sucessao (U2: nomear a grafia e a familia)
 ("FitaPlanaAnterior", "/-- The same length L that charged the earlier flat tape for the Verb also charges", "/-- The same length L that charges the flat tape of `VerboNaFita` for the Verb also charges"),
 ("LeitorDaFamilia", "/-- A single pass on the previous exponential family. For a lone pair only the", "/-- A single pass on the `coupled` family of `LeituraIntegrada`. For a lone pair only the"),
 # --- FitaComCusto (U2: desigualdade estrita)
 ("FitaComCusto", "Leitura final sob o limiar pago da Palavra de `OPsibitEACompressao`. -/", "Leitura final com t acima do limiar pago da Palavra de `OPsibitEACompressao`. -/"),
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


textos, falhas, feitas = {}, [], 0
for nome, velho, novo in TROCAS:
    t = textos.get(nome) or (D / (nome + ".lean")).read_bytes().decode("utf-8")
    if velho not in t and novo and novo in t:
        textos[nome] = t; continue
    if t.count(velho) != 1:
        falhas.append((nome, t.count(velho), velho[:70])); textos[nome] = t; continue
    textos[nome] = t.replace(velho, novo); feitas += 1
print("trocas:", len(TROCAS), "| a fazer agora:", feitas, "| FALHAS:", len(falhas))
for f in falhas:
    print("   FALHA:", f)
assert not falhas
for nome, t in textos.items():
    assert sem_comentarios((O / (nome + ".lean")).read_bytes().decode("utf-8")) == sem_comentarios(t), "codigo difere: " + nome
print("codigo identico ao da fonte do autor nos", len(textos), "modulos tocados:", sorted(textos))
if EXEC:
    for nome, t in textos.items():
        f = D / (nome + ".lean"); b = t.encode("utf-8")
        if f.read_bytes() != b:
            tmp = f.with_name(f.name + ".tmp_c1"); tmp.write_bytes(b); tmp.replace(f)
    p = D / "EMENDAS_DO_PARECER_031.json"; tmp = p.with_name(p.name + ".tmp_c1")
    tmp.write_bytes(json.dumps({"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "trocas_exatas": [list(x) for x in TROCAS],
                                "sha256_depois": {n: hashlib.sha256((D / (n + ".lean")).read_bytes()).hexdigest() for n in sorted(textos)}}, ensure_ascii=False, indent=1).encode("utf-8")); tmp.replace(p)
    print("gravado:", p.name)
