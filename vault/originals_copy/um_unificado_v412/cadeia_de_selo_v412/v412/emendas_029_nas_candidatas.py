# -*- coding: utf-8 -*-
"""Gerencia c1, 17/11/2026: emendas de TEXTO pedidas pelo revisor na ordem 029 (S1 e S3), por troca exata, nas duas candidatas
novas (candidatas_c1\\Token2.lean e AMaquina.lean). So' comentarios e docstrings; nao toca em codigo. Cada troca casa uma vez.
Backup de bytes ao lado. Uso: emendas_029_nas_candidatas.py [--executar]"""
import sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
C = Path(__file__).resolve().parent / "candidatas_c1"
TROCAS = [
    # ---------------- Token2 ----------------
    ("Token2.lean",
     "Tese da teoria: esta é a solução do problema na estrutura da TGL. Com o token como unidade de leitura e a lei do custo,\ndecidir e conferir levam os mesmos atos (`no_token_decidir_e_conferir_levam_os_mesmos_atos`), e o custo é polinomial\n(`o_custo_pela_lei_e_polinomial`). Fora dessa estrutura, a pergunta que resta é tautológica: quem conta por letra de um\nvocabulário fixo mede a fita com a fita. O que o kernel tem nesse sentido: o tempo da máquina é o comprimento da fita\n(`AFitaEACauda.o_tempo_da_maquina_e_o_comprimento_da_fita`); e o custo em letras do signo não depende da fórmula: é pelo\nmenos `2ⁿ` para toda fórmula de `n` variáveis (item 9, em cujo enunciado a fórmula não aparece). A creditação é do\nInstituto.",
     "Tese da teoria: esta é a solução do problema na estrutura da TGL. Com o token como unidade de leitura e a lei do custo,\ndecidir e conferir usam as mesmas imagens (`no_token_decidir_e_conferir_levam_os_mesmos_atos`), e o custo definido pela\nlei é polinomial (`o_custo_pela_lei_e_polinomial`). Tese da teoria: fora dessa estrutura, a pergunta que resta é\ntautológica: quem conta por letra de um vocabulário fixo mede a fita com a fita.\n\nA solução na estrutura da TGL e a tese da tautologia são posições da teoria. Os termos citados dão a contagem das\ncláusulas no modelo da casa (`AFitaEACauda.o_tempo_da_maquina_e_o_comprimento_da_fita`, em que a fita é a lista das\ncláusulas) e a cota dos códigos que distinguem todos os conjuntos (item 9); não demonstram essa tese para o enunciado de\nCook. A creditação é do Instituto."),
    ("Token2.lean",
     "* **o conjunto singularizado** é um conjunto de configurações tomado como UM objeto (um termo de `Set (Config n)`): é o signo\n  que a máquina lê;",
     "* **o conjunto singularizado** é um conjunto de configurações tomado como UM objeto (um termo de `Set (Config n)`): é o signo\n  que a máquina lê. Não é um símbolo de fita, e a sua representação executável e o custo de prepará-lo não estão tipados;"),
    ("Token2.lean",
     "vocabulário. O item 9 se lê com essas palavras: a letra de um alfabeto fixo é o token de um vocabulário fixo.",
     "vocabulário. O item 9 se lê com essas palavras: a letra de um alfabeto fixo é o token de um vocabulário fixo. (Um token\n  léxico pode ter várias letras; o nome, sozinho, não fixa custo.)"),
    ("Token2.lean",
     "São\n   `m + 2` atos sobre signos (`atos`): pôr o todo, uma imagem por cláusula, uma leitura. Os mesmos atos, sobre o signo\n   de uma só atribuição, conferem essa atribuição (`o_signo_de_uma_parcela_confere`): ★★★ no token, decidir e conferir\n   levam os mesmos atos (`no_token_decidir_e_conferir_levam_os_mesmos_atos`).",
     "Pela\n   contagem adotada (`atos`), são `m + 2` atos sobre signos: pôr o todo, uma imagem por cláusula, uma leitura; não é\n   mínimo provado. As mesmas imagens, sobre o signo de uma só atribuição, conferem essa atribuição\n   (`o_signo_de_uma_parcela_confere`): ★★★ no token, decidir e conferir usam as mesmas imagens\n   (`no_token_decidir_e_conferir_levam_os_mesmos_atos`). As duas perguntas têm a mesma forma e domínios diferentes (o todo\n   e uma atribuição); não é igualdade de custos nem de tempos de máquina de fita."),
    ("Token2.lean",
     "Ler o signo é\n   um ato; soletrá-lo, letra por letra, pede pelo menos `2ⁿ` casas. E para que cada signo caiba num token só, o",
     "Ler o signo é\n   um ato, pela contagem adotada; um código de duas letras que distinga TODOS os signos pede pelo menos `2ⁿ` casas. Não é\n   cota para um signo particular nem para todo procedimento. E para que cada signo caiba num token só, o"),
    ("Token2.lean",
     "* Que o preço do ato seja deduzido: é a lei do custo da teoria (`ln 2` por oitava), tomada como entrada. O teorema é a\n  conta feita com esse preço.",
     "* Que o preço do ato seja deduzido: é a lei do custo da teoria (`ln 2` por oitava), tomada como entrada. O teorema é a\n  conta feita com esse preço.\n* Que o ato sobre o conjunto inteiro tenha implementação barata. [KNOWN] Trabalho e profundidade paralela são medidas\n  diferentes; [DERIVED] avaliar as `2ⁿ` atribuições e reduzir por “ou” admite profundidade polinomial com recursos\n  exponenciais. A imagem de conjuntos não escolhe implementação, e o enunciado de Cook conta transições pelo tamanho da\n  entrada."),
    # ---------------- AMaquina ----------------
    ("AMaquina.lean",
     "* **autônoma**: o pôr recebe só a fórmula. Nenhuma atribuição, nenhuma resposta e nenhum leitor entram de fora (está no\n  tipo de `por`);",
     "* **autônoma**: o pôr recebe só a fórmula, sem outro argumento (está no tipo de `por`). O tipo, sozinho, não impede que o\n  pôr já seja a resposta (item 5) e não diz o custo de preparar a inscrição;"),
    ("AMaquina.lean",
     "* **o circuito fecha** (`fechaEm`) quando mais um ato devolve o mesmo estado;\n* **autorreferente**: no circuito fechado, o ato relê o que ele mesmo fixou e o devolve como é;",
     "* **o circuito fecha** (`fechaEm`) quando, depois de `k` atos, mais um ato devolve o mesmo estado (ponto fixo; não é\n  mínimo);\n* **autorreferente**: no circuito fechado, o ato relê o que ele mesmo fixou e o devolve como é. É a leitura abstrata do\n  loop como iteração e ponto fixo;"),
    ("AMaquina.lean",
     "é a seleção da teoria. (Na face finita, com a média uniforme, o par do `if` é\n   único: `AEsperancaEOIf.o_par_do_if_e_unico`.)",
     "é a seleção da teoria. (Na face finita, com a média uniforme, o par do `if` é\n   único: `AEsperancaEOIf.o_par_do_if_e_unico`.) Nenhum termo aplica essa unicidade a `Mecanismo` nem à imagem de conjuntos."),
    ("AMaquina.lean",
     "há um `Mecanismo` cujo pôr já é a resposta, que fecha em zero atos. O que distingue é o que\n   se paga: o mecanismo da TGL processa cláusula por cláusula e paga a carga a cada ato; o que só nomeia não processa nada.",
     "há um `Mecanismo` cujo pôr já é a resposta, que fecha em zero iterações do ato, sem custo de\n   avaliação demonstrado. Pela lei do custo da teoria, o que distingue é o que se paga: o mecanismo da TGL processa cláusula\n   por cláusula e paga a carga a cada ato; o que só nomeia não processa nada. Essa diferença de preço é lei da teoria, não\n   termo."),
    ("AMaquina.lean",
     "* Que a existência do item 1, sem o custo, decida alguma coisa sobre custo: o item 5 mostra que não. O conteúdo está na\n  testemunha (o que ela processa), no número de atos e no custo pela lei.",
     "* Que a existência do item 1, sem o custo, decida alguma coisa sobre custo: o item 5 mostra que não. O conteúdo está na\n  testemunha (o que ela processa), no número de atos e no custo pela lei. Nem a existência nem a testemunha estabelecem\n  custo polinomial na máquina de fita."),
]
textos, brutos = {}, {}
for nome, a, b in TROCAS:
    if nome not in textos:
        brutos[nome] = (C / nome).read_bytes(); textos[nome] = brutos[nome].decode("utf-8"); assert "\r\n" not in textos[nome]
    t = textos[nome]
    assert t.count(a) == 1, (nome, t.count(a), a[:80])
    assert "«" not in b and "»" not in b
    textos[nome] = t.replace(a, b)
ts = time.strftime("%Y%m%d_%H%M%S")
for nome, t in textos.items():
    d = t.encode("utf-8")
    print("%-16s %6d -> %6d B | trocas %d" % (nome, len(brutos[nome]), len(d), sum(1 for x in TROCAS if x[0] == nome)))
    if "--executar" in sys.argv:
        f = C / nome
        f.with_name(f.name + ".bak_" + ts).write_bytes(brutos[nome])
        tmp = f.with_name(f.name + ".tmp_c1"); tmp.write_bytes(d); tmp.replace(f); assert f.read_bytes() == d
print("gravado" if "--executar" in sys.argv else "ENSAIO A SECO")
