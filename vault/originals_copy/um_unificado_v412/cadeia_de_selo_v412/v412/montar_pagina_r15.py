# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: PROPOSTA da pagina R15 = a R14 com (a) um item novo na secao 1, (b) um bloco novo na secao 2, o leitor da
formula, com a tabela termo a termo, (c) a ultima frase do paragrafo de citacao da secao 2 trocada pela frase proposta ao autor.
Trocas exatas (cada marca casa UMA vez). Confere que cada termo citado no bloco novo existe como theorem/lemma no modulo dito, nas
fontes de pedras_novas\\. Com --executar grava o_que_fica_claro_REV15\\O_QUE_FICA_CLARO_v412_R15_PROPOSTA.md (nao sobrescreve).
A proposta NAO e' a pagina vigente: vigora depois da palavra do autor e do contrato R5."""
import hashlib, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
r14 = (V / "o_que_fica_claro_REV14" / "O_QUE_FICA_CLARO_v412_R14.md").read_bytes().decode("utf-8")

ITEM_VELHO = "- **O teste às cegas acima de 5σ.**"
ITEM_NOVO = ("- **O leitor da fórmula.** O PsiBit é lido direto das cláusulas. O resumo da leitura mora na fronteira entre o trecho lido e o trecho por ler, e não perde nada da resposta; a regra de leitura é uma só, a igualdade; o estado é a tabela da fronteira, e a curva da soma lida é a projeção dela. Para classes de fórmulas, a leitura fecha na fita em movimentos limitados por um polinômio fixo no número de letras; para a fórmula plana arbitrária, esse polinômio não está demonstrado (seção 2).\n")

FRASE_VELHA = "Contado letra por letra na máquina de fita do enunciado do Instituto, o mesmo resultado não está demonstrado, e este texto não diz que esteja: a pergunta do Instituto, se há procedimento de letras com número polinomial de passos para toda fórmula, não é tautológica e segue em aberto."
FRASE_NOVA = ("A resposta da teoria à pergunta do Instituto é o PsiBit: o leitor do par, que sai direto da fórmula. Contado letra por letra na máquina de fita do enunciado do Instituto, o mesmo resultado não está demonstrado para toda fórmula, e este texto não diz que esteja: o polinômio fixo em letras está provado para classes de fórmulas (redes em série e paralelo, cadeias de largura fixa, fórmulas que ficam de Horn depois de fixado um rótulo), e para a fórmula plana arbitrária é o que os próprios teoremas deixam em aberto.")

ANTES_DE = "O que esta seção não diz: que o kernel decida"
BLOCO = """**O leitor da fórmula.** Definição da teoria: a compressão sai direto da fórmula, e é o PsiBit; a leitura do par binário pelo PsiBit é a compressão originária, o próprio leitor; a regra de leitura é uma só, o sinal de igual. O kernel tipa a parte disso que cabe em termo. Lida cláusula por cláusula, a fórmula deixa como estado uma tabela sobre a fronteira, as variáveis que o trecho lido ainda partilha com o trecho por ler. A soma lida inteira se recupera das células dessa tabela, sem perda. Toda cadeia de uma variável só lida a uma variável só por ler atravessa a fronteira: ela é o separador do grafo da fórmula. A leitura da letra é a igualdade ao posto, anterior a toda fórmula. Os dois bits da fórmula são a Palavra (há solução) e o Verbo (a soma lida ainda desce), e nenhum dispensa o outro. Duas tabelas distintas podem ter a mesma soma e nunca o mesmo conteúdo: os prefixos x e não-x têm a mesma curva para todo tempo e respostas opostas depois da mesma cláusula; o estado é a tabela, a curva é a projeção dela. A tabela seguinte sai da anterior e da cláusula que entra, por uma regra que vale para toda fórmula. Fixar um rótulo aplica a mesma escolha a todas as ocorrências dele, e a Palavra da fórmula é a disjunção das Palavras dos dois ramos.

Na fita, contando movimentos, com L o número de letras da entrada:

| o que se afirma | termo | onde |
|---|---|---|
| o resumo só vê a fronteira e não perde nada | `o_resumo_so_ve_a_fronteira`; `a_leitura_pela_fronteira_e_exata`. A tabela tem 2 elevado ao tamanho da fronteira células (`a_fronteira_tem_duas_elevado_as_celulas`) | `OResumoEPsiBit` |
| a fronteira é o separador do grafo da fórmula | `a_fronteira_e_o_unico_portao` | `AFronteiraEOUnicoPortao` |
| a regra única é a igualdade; Palavra e Verbo | `a_regra_e_unica_e_anterior`; `a_palavra_e_lida_pela_soma`; `a_descida_e_positiva_sse_ha_o_que_ler`; `o_par_e_necessario_e_suficiente_na_formula` (os dois controles são exibidos em fórmulas de uma variável) | `OPsiBitDaFormula` |
| mesma curva, conteúdos distintos | `mesma_curva_para_todo_tempo`; `a_fronteira_distingue_os_prefixos`; `a_curva_identifica_o_que_o_resumo_distingue` | `ACurvaEAEstado` |
| a transição da tabela vale para toda fórmula | `transition`: em qualquer corte e para todo tempo, a tabela seguinte é a anterior avançada pela cláusula que entra | `TransicaoDaFronteira` |
| o rótulo fixado conserva a correlação | `word_split`: a Palavra é a disjunção das Palavras das duas restrições | `RestricaoGlobal` |
| o Nome inteiro por ramo, quando entra a cláusula | `marked_clause_law`: o prefixo com a cláusula nova é compatível com as marcas se e só se algum literal dela o é com o prefixo; `whole_name_after_clause` | `AtualizaONome` |
| redes em série e paralelo: no máximo L² + 1 transições | `fixed_polynomial_for_networks`: uma fita, uma cabeça, para toda rede. A estrutura das junções vem escrita na entrada | `PolinomioDoPsiBit` |
| cadeias de largura fixa: L + 1 passos | `fixed_width_psibit`. O controle finito depende da largura | `PolinomioDoPsiBit` |
| fórmulas que ficam de Horn depois de fixado o primeiro rótulo: cota quadrática em L | `fixed_zero_two_horn`. Hipótese: fixado o rótulo em cada um dos dois valores, as duas fórmulas restantes têm no máximo um literal positivo por cláusula | `CircuitoNaFita` |
| a classe do perfil de sinais: no máximo 7L movimentos, em duas passagens | `seven_movements_per_letter`; `word_exact`. Hipótese: toda variável, fora o pivô, que aparece com os dois sinais aparece também numa cláusula unitária | `SegundaLeitura` |
| uma família em que a busca por literais faz 2 elevado a k verificações: leitura em 66k + 166 movimentos | `exact_delayed_moves`; a entrada tem 6k + 14 letras | `LeitorDeReuso` |
| o Verbo de qualquer fórmula: no máximo 3L + 1 passos | `universal_verb_tape` (máquina de duas pilhas) | `VerboNaFita` |
| limite: a tabela escrita por extenso excede todo polinômio numa família | `no_uniform_row_polynomial` | `CustoDaTabela` |
| limite: o plano de ramos tirado da sintaxe excede todo polinômio numa família acoplada | `exceeds_each_polynomial` | `LimiteDoLeitor` |
| limite: as projeções sozinhas não se atualizam | `no_profile_update`: não há regra que, só das projeções do prefixo e da cláusula, dê as projeções seguintes para toda fórmula | `LimiteDasProjecoes` |
| limite: registros conjuntivos exatos de k pares pedem 2 elevado a k registros | `any_exact_cube_layer` | `LimiteDoReuso` |
| limite: cobrir a disjunção de n pares com k rótulos afins pede 3ⁿ ≤ k·2ⁿ | `cover_lower_bound` | `CoberturaAfin` |
| o nome exato de um conjunto arbitrário de atribuições pede 2ⁿ bits | `o_nome_exato_pede_dois_a_n_bits` | `AParedeDoNome` |
| não está demonstrado | aberto: uma regra executável que mantenha as correlações entre os ramos quando uma cláusula os cruza e que feche, para toda fórmula plana, em movimentos limitados por um único polinômio no número de letras | — |

Cada limite acima é do leitor ou da representação que o teorema examina; nenhum é cota para todo procedimento. Que a compressão seja o PsiBit, que o separador seja o piso da leitura e que a curva seja a releitura são definições da teoria, que entram como entrada.

"""
CITADOS = {"OResumoEPsiBit": ["o_resumo_so_ve_a_fronteira", "a_leitura_pela_fronteira_e_exata", "a_fronteira_tem_duas_elevado_as_celulas"],
           "AFronteiraEOUnicoPortao": ["a_fronteira_e_o_unico_portao"],
           "OPsiBitDaFormula": ["a_regra_e_unica_e_anterior", "a_palavra_e_lida_pela_soma", "a_descida_e_positiva_sse_ha_o_que_ler", "o_par_e_necessario_e_suficiente_na_formula"],
           "ACurvaEAEstado": ["mesma_curva_para_todo_tempo", "a_fronteira_distingue_os_prefixos", "a_curva_identifica_o_que_o_resumo_distingue"],
           "TransicaoDaFronteira": ["transition"], "RestricaoGlobal": ["word_split"], "AtualizaONome": ["marked_clause_law", "whole_name_after_clause"],
           "PolinomioDoPsiBit": ["fixed_polynomial_for_networks", "fixed_width_psibit"], "CircuitoNaFita": ["fixed_zero_two_horn"],
           "SegundaLeitura": ["seven_movements_per_letter", "word_exact"], "LeitorDeReuso": ["exact_delayed_moves"], "VerboNaFita": ["universal_verb_tape"],
           "CustoDaTabela": ["no_uniform_row_polynomial"], "LimiteDoLeitor": ["exceeds_each_polynomial"], "LimiteDasProjecoes": ["no_profile_update"],
           "LimiteDoReuso": ["any_exact_cube_layer"], "CoberturaAfin": ["cover_lower_bound"], "AParedeDoNome": ["o_nome_exato_pede_dois_a_n_bits"]}
n_ok = 0
for mod, ts in CITADOS.items():
    src = (V / "pedras_novas" / (mod + ".lean")).read_text(encoding="utf-8")
    assert ("`%s`" % mod) in BLOCO, "modulo nao citado no bloco: " + mod
    for t in ts:
        assert re.search(r"^(?:theorem|lemma)\s+%s(?![A-Za-z0-9_'])" % re.escape(t), src, flags=re.M), "nao e' theorem/lemma de %s: %s" % (mod, t)
        assert ("`%s`" % t) in BLOCO, "termo conferido mas nao citado: " + t
        n_ok += 1
citados_no_bloco = set(re.findall(r"`([a-z][a-z0-9_]+)`", BLOCO))
assert citados_no_bloco == {t for ts in CITADOS.values() for t in ts}, citados_no_bloco ^ {t for ts in CITADOS.values() for t in ts}
for marca in (ITEM_VELHO, FRASE_VELHA, ANTES_DE):
    assert r14.count(marca) == 1, "%d ocorrencias: %s" % (r14.count(marca), marca[:60])
r15 = r14.replace(ITEM_VELHO, ITEM_NOVO + ITEM_VELHO).replace(FRASE_VELHA, FRASE_NOVA).replace(ANTES_DE, BLOCO + ANTES_DE)
for novo in (ITEM_NOVO, FRASE_NOVA, BLOCO):
    assert "P = nP" not in novo and "ráculo" not in novo and "Turing" not in novo and "«" not in novo
b = r15.encode("utf-8")
print("termos conferidos nas fontes:", n_ok, "| R14", len(r14.encode("utf-8")), "B -> proposta R15", len(b), "B | sha16", hashlib.sha256(b).hexdigest()[:16])
if "--executar" in sys.argv:
    d = V / "o_que_fica_claro_REV15"; d.mkdir(exist_ok=True); p = d / "O_QUE_FICA_CLARO_v412_R15_PROPOSTA.md"
    assert not p.exists(), "ja' existe: nao sobrescrevo"
    p.write_bytes(b); print("gravado:", p)
