# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: PROPOSTA da pagina R16 = a R14 com (a) um item novo na secao 1, (b) o bloco do leitor da formula na
secao 2, com a tabela termo a termo, (c) a ultima frase do paragrafo de citacao da secao 2. E' a proposta R15 emendada linha a linha
pelo parecer da ordem 031 (REVISAO_031_U3_Codex.md e a matriz do recibo) e acrescida das linhas das duas pastas fechadas depois
(a chave da cadeia binaria e o handshake do Nome) e do termo do separador no percurso. Trocas exatas sobre a R14. Confere que cada
termo citado existe como theorem/lemma no modulo dito (fontes de pedras_novas\\). Com --executar grava
o_que_fica_claro_REV16\\O_QUE_FICA_CLARO_v412_R16_PROPOSTA.md, ou, com --vigente, O_QUE_FICA_CLARO_v412_R16.md (nao sobrescreve).
--frase A|B escolhe a abertura da frase sobre a pergunta do Instituto: A = "A resposta da teoria ... e' o PsiBit"; B = a redacao
sugerida pelo revisor, "A teoria propoe o PsiBit como leitor". A escolha e' do autor."""
import hashlib, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
r14 = (V / "o_que_fica_claro_REV14" / "O_QUE_FICA_CLARO_v412_R14.md").read_bytes().decode("utf-8")
qual = sys.argv[sys.argv.index("--frase") + 1] if "--frase" in sys.argv else "A"

ITEM_VELHO = "- **O teste às cegas acima de 5σ.**"
ITEM_NOVO = ("- **O leitor da fórmula.** O PsiBit é lido direto das cláusulas. O resumo da leitura é uma tabela sobre a fronteira entre o trecho lido e o trecho por ler, e agrupar a soma lida pela fronteira não perde nada; a regra de leitura da letra é fixa, a igualdade; o estado é a tabela, e a curva da soma lida é a projeção dela. Para classes de fórmulas, cada uma com a sua máquina e a sua grafia, a leitura fecha na fita dentro de um polinômio fixo no número de letras; para a fórmula plana arbitrária, esse polinômio não está demonstrado (seção 2).\n")

FRASE_VELHA = "Contado letra por letra na máquina de fita do enunciado do Instituto, o mesmo resultado não está demonstrado, e este texto não diz que esteja: a pergunta do Instituto, se há procedimento de letras com número polinomial de passos para toda fórmula, não é tautológica e segue em aberto."
ABERTURA = {"A": "A resposta da teoria à pergunta do Instituto é o PsiBit: o leitor do par, que sai direto da fórmula.",
            "B": "A teoria propõe o PsiBit como leitor: o leitor do par, que sai direto da fórmula."}[qual]
FRASE_NOVA = (ABERTURA + " Contado letra por letra na máquina de fita do enunciado do Instituto, o mesmo resultado não está demonstrado para toda fórmula, e este texto não diz que esteja: o polinômio fixo em letras está provado para classes de fórmulas, cada uma com a sua máquina e a sua grafia (redes em série e paralelo com as junções escritas na entrada, cadeias de largura fixada, fórmulas em que as duas restrições da primeira variável são de Horn, cadeias binárias ordenadas, cláusulas binárias com dois pivôs), e para a fórmula plana arbitrária é o que os próprios teoremas deixam em aberto.")

ANTES_DE = "O que esta seção não diz: que o kernel decida"
BLOCO = """**O leitor da fórmula.** Definição da teoria: a compressão sai direto da fórmula, e é o PsiBit; a leitura do par binário pelo PsiBit é a compressão originária, o próprio leitor; a regra de leitura é uma só, o sinal de igual. O kernel tipa a parte disso que cabe em termo. Lida cláusula por cláusula, a fórmula deixa como estado uma tabela sobre a fronteira, as variáveis que o trecho lido ainda partilha com o trecho por ler. Agrupar a soma lida pela fronteira não perde nada: a soma inteira é, célula a célula, o peso lido vezes o peso por ler. Todo percurso de uma variável só lida a uma variável só por ler tem um vértice na fronteira: ela separa o grafo da fórmula. A regra de leitura da letra é a igualdade ao posto, e não depende da fórmula. Os dois bits da fórmula são a Palavra (há solução) e o Verbo (a soma lida ainda desce); em fórmulas de uma variável, cada um sozinho confunde fórmulas que o outro distingue. Duas tabelas distintas podem ter a mesma soma e nunca o mesmo conteúdo: os prefixos x e não-x têm a mesma curva para todo tempo e respostas opostas depois da mesma cláusula; o estado é a tabela, a curva é a projeção dela. Dadas as duas fronteiras, a tabela seguinte sai da anterior e da cláusula que entra, por uma regra que vale para toda fórmula. Fixar um rótulo aplica a mesma escolha a todas as ocorrências dele, e a Palavra da fórmula é a disjunção das Palavras dos dois ramos. Dois blocos só se juntam pelo mesmo conteúdo nos nomes que partilham, e a recusa de uma proposta devolve a própria cláusula violada.

Na tabela, cada linha tem a sua máquina, a sua grafia e a sua unidade (transições, passos ou deslocamentos); L é o comprimento da entrada na grafia da linha.

| o que se afirma | termo | onde |
|---|---|---|
| o resumo só vê a fronteira, e agrupar por ela não perde nada | `o_resumo_so_ve_a_fronteira`: o resumo é constante em cada célula da fronteira. `a_leitura_pela_fronteira_e_exata`: a soma lida inteira agrupa, célula a célula, o peso lido pelo peso por ler. `total_projection`: a soma das células dá a soma lida do prefixo, em qualquer número de variáveis. A tabela tem 2 elevado ao tamanho da fronteira células (`a_fronteira_tem_duas_elevado_as_celulas`), inclusive quando a fronteira é o conjunto de todas as variáveis | `OResumoEPsiBit`, `ProjecaoDaFronteira` |
| todo percurso do só lido ao só por ler tem um vértice na fronteira | `o_percurso_atravessa_a_fronteira`, com o percurso dado como lista explícita. Não se prova que a fronteira seja o menor separador, nem o único. `a_fronteira_e_o_unico_portao` conclui só que, havendo a cadeia, a fronteira não é vazia | `OSeparadorNoPercurso`, `AFronteiraEOUnicoPortao` |
| a regra de leitura é fixa e é a igualdade; Palavra e Verbo | `a_regra_e_unica_e_anterior`: a regra não tem a fórmula como entrada (o termo não compara regras concorrentes). `a_palavra_e_lida_pela_soma`: com o tempo pago acima de n·ln 2. `a_descida_e_positiva_sse_ha_o_que_ler`: para todo tempo, a descida é positiva se e só se há atribuição de custo não nulo. `o_par_e_necessario_e_suficiente_na_formula`: os dois controles, em fórmulas de uma variável | `OPsiBitDaFormula` |
| mesma curva, conteúdos distintos | `mesma_curva_para_todo_tempo`; `palavras_opostas_depois_da_mesma_clausula`; `a_fronteira_distingue_os_prefixos` (as células diferem para tempo não nulo); `a_curva_identifica_o_que_o_resumo_distingue`. É o exemplo de uma variável | `ACurvaEAEstado` |
| a transição da tabela vale para toda fórmula | `transition`: em todo corte anterior ao fim e para todo tempo, a tabela seguinte é a anterior avançada pela cláusula que entra, dadas a fronteira antiga e a nova. A identidade não dá cota de construção nem de tempo | `TransicaoDaFronteira` |
| o rótulo fixado conserva a correlação | `word_split`: a Palavra é a disjunção das Palavras das duas restrições. Não dá, por si, o custo de avaliar os ramos | `RestricaoGlobal` |
| o Nome inteiro por ramo, quando entra a cláusula | `marked_clause_law`: o prefixo com a cláusula nova é compatível com as marcas se e só se algum literal dela o é com o prefixo (vale para a cláusula vazia e para qualquer lista de marcas). `whole_name_after_clause`: com número positivo de passos e β entre 0 e 1 | `AtualizaONome` |
| dois blocos juntam-se pelo conteúdo dos nomes partilhados | `semantic_handshake` | `HandshakeDoNome` |
| a recusa devolve a cláusula violada | `reuses_clause`: a recusa vale para toda atribuição que coincida nas variáveis da cláusula. `reply_bounds` e `call_bound`: para um bloco de m cláusulas, no máximo m recusas e m + 1 chamadas a um proponente exato. O custo de produzir a proposta seguinte não está cotado | `ARecusaTemConteudo`, `ClausulaComoResposta` |
| redes em série e paralelo, com as junções escritas na entrada: no máximo L² + 1 transições | `fixed_polynomial_for_networks`: uma máquina de uma fita e uma cabeça, a mesma para toda rede | `PolinomioDoPsiBit` |
| cadeias de bolsas de largura fixada: L + 1 passos | `fixed_width_psibit`. O controle depende da largura; não é máquina uniforme quando a largura faz parte da entrada | `PolinomioDoPsiBit` |
| fórmulas em que as duas restrições da primeira variável são de Horn: cota quadrática em L | `fixed_zero_two_horn`: os deslocamentos somam no máximo 27L + 16 + 4(L + 1)(3L + 2). Não inclui achar um pivô que sirva | `CircuitoNaFita` |
| a classe do perfil de sinais: no máximo 7L movimentos, em duas passagens | `seven_movements_per_letter`: a cota vale para toda fita. `word_exact`: a saída é a Palavra quando toda variável, fora o pivô, que aparece com os dois sinais aparece também numa cláusula unitária | `SegundaLeitura` |
| cadeia binária ordenada: a correlação entre as pontas cabe em quatro bits e sai das letras em exatamente L deslocamentos | `one_head`; `closed_path`, com a cláusula que liga as duas pontas. A classe é prometida: a ordenação e o reconhecimento dela em entradas arbitrárias não estão contados | `CadeiaNaFita`, `DuasPontasLivres` |
| cláusulas binárias com dois pivôs: os quatro ramos em exatamente 7L + 8T movimentos, T o número de marcas de endereço | `exact_movements`; `branch_exact` | `ReguaNaFita` |
| uma família de 6k + 14 letras: a busca por literais faz pelo menos 2 elevado a k verificações; outro leitor lê a mesma família em exatamente 66k + 166 movimentos | `delayed_letters`; `delayed_checks`; `exact_delayed_moves`. São contagens de leitores e de operações diferentes | `CustoDaBuscaLiteral`, `LeitorDeReuso` |
| o Verbo de qualquer fórmula: no máximo 3L + 1 passos | `universal_verb_tape`: máquina de duas pilhas, com endereços unários. É o Verbo, não a Palavra | `VerboNaFita` |
| o transporte da inscrição em dois bits por letra, com a reconstrução: 6L deslocamentos | `any_cnf_transport` (8L com a rebobinagem do canal). A Palavra pede leitura adicional | `TransporteDaInscricao` |
| limite: a lista explícita de linhas da tabela excede todo polinômio numa família | `no_uniform_row_polynomial` | `CustoDaTabela` |
| limite: toda execução completa do plano de ramos tirado da sintaxe excede todo polinômio numa família acoplada | `exceeds_each_polynomial` | `LimiteDoLeitor` |
| limite: as projeções sozinhas não se atualizam | `no_profile_update`: não há função que, do perfil de projeções do prefixo e da cláusula inteira, dê o perfil seguinte para todo prefixo e toda cláusula | `LimiteDasProjecoes` |
| limite: registros conjuntivos exatos de k pares pedem pelo menos 2 elevado a k registros | `any_exact_cube_layer` | `LimiteDoReuso` |
| limite: cobrir exatamente a conjunção de n cláusulas de dois literais sobre pares disjuntos com k rótulos afins pede 3ⁿ ≤ k·2ⁿ | `cover_lower_bound` | `CoberturaAfin` |
| limite: uma chave de b bits que responda sozinha a toda continuação que fixa w rótulos livres tem b ≥ 2 elevado a w | `binary_key_bound`. As fórmulas que realizam relações arbitrárias podem ser longas: não é cota no comprimento L | `CapacidadeDosRotulos` |
| limite: a chave em fase densa excede todo polinômio numa família | `no_fixed_dense_budget` | `CustoDaFaseDensa` |
| limite: um registrador de p bits, exato para toda continuação de toda fórmula em n variáveis, tem p ≥ 2ⁿ | `o_nome_exato_pede_dois_a_n_bits`. É piso de espaço no pior caso, em n; não estima tempo nem o comprimento L | `AParedeDoNome` |
| a redução: toda fórmula se embute, em no máximo 5L + 15 passos, numa instância de dois blocos com uma ponte, compatível se e só se a original é | `linear_embedding`. Logo uma regra uniforme para os indicadores dos blocos decidiria se a fórmula tem solução | `ClausulaNoSeparador` |
| não está demonstrado | aberto: uma única máquina executável que decida a Palavra de toda fórmula plana em movimentos limitados por um polinômio fixo no número de letras. Identidades entre tabelas, limites de um leitor e controles finitos não dão esse resultado | — |

Cada limite acima é do leitor ou da representação que o teorema examina; nenhum é cota para todo procedimento. Que a compressão seja o PsiBit, que o separador seja o piso da leitura, que a curva seja a releitura e que a recusa seja um nome com conteúdo são definições da teoria, que entram como entrada.

"""
CITADOS = {"OResumoEPsiBit": ["o_resumo_so_ve_a_fronteira", "a_leitura_pela_fronteira_e_exata", "a_fronteira_tem_duas_elevado_as_celulas"],
           "ProjecaoDaFronteira": ["total_projection"], "OSeparadorNoPercurso": ["o_percurso_atravessa_a_fronteira"],
           "AFronteiraEOUnicoPortao": ["a_fronteira_e_o_unico_portao"],
           "OPsiBitDaFormula": ["a_regra_e_unica_e_anterior", "a_palavra_e_lida_pela_soma", "a_descida_e_positiva_sse_ha_o_que_ler", "o_par_e_necessario_e_suficiente_na_formula"],
           "ACurvaEAEstado": ["mesma_curva_para_todo_tempo", "palavras_opostas_depois_da_mesma_clausula", "a_fronteira_distingue_os_prefixos", "a_curva_identifica_o_que_o_resumo_distingue"],
           "TransicaoDaFronteira": ["transition"], "RestricaoGlobal": ["word_split"], "AtualizaONome": ["marked_clause_law", "whole_name_after_clause"],
           "HandshakeDoNome": ["semantic_handshake"], "ARecusaTemConteudo": ["reuses_clause"], "ClausulaComoResposta": ["reply_bounds", "call_bound"],
           "PolinomioDoPsiBit": ["fixed_polynomial_for_networks", "fixed_width_psibit"], "CircuitoNaFita": ["fixed_zero_two_horn"],
           "SegundaLeitura": ["seven_movements_per_letter", "word_exact"], "CadeiaNaFita": ["one_head"], "DuasPontasLivres": ["closed_path"],
           "ReguaNaFita": ["exact_movements", "branch_exact"], "CustoDaBuscaLiteral": ["delayed_letters", "delayed_checks"],
           "LeitorDeReuso": ["exact_delayed_moves"], "VerboNaFita": ["universal_verb_tape"], "TransporteDaInscricao": ["any_cnf_transport"],
           "CustoDaTabela": ["no_uniform_row_polynomial"], "LimiteDoLeitor": ["exceeds_each_polynomial"], "LimiteDasProjecoes": ["no_profile_update"],
           "LimiteDoReuso": ["any_exact_cube_layer"], "CoberturaAfin": ["cover_lower_bound"], "CapacidadeDosRotulos": ["binary_key_bound"],
           "CustoDaFaseDensa": ["no_fixed_dense_budget"], "AParedeDoNome": ["o_nome_exato_pede_dois_a_n_bits"], "ClausulaNoSeparador": ["linear_embedding"]}
n_ok = 0
for mod, ts in CITADOS.items():
    src = (V / "pedras_novas" / (mod + ".lean")).read_text(encoding="utf-8")
    assert ("`%s`" % mod) in BLOCO, "modulo nao citado no bloco: " + mod
    for t in ts:
        assert re.search(r"^(?:theorem|lemma)\s+%s(?![A-Za-z0-9_'])" % re.escape(t), src, flags=re.M), "nao e' theorem/lemma de %s: %s" % (mod, t)
        assert ("`%s`" % t) in BLOCO, "termo conferido mas nao citado: " + t
        n_ok += 1
citados_no_bloco = set(re.findall(r"`([a-z][a-z0-9_]+)`", BLOCO)); esperados = {t for ts in CITADOS.values() for t in ts}
assert citados_no_bloco == esperados, citados_no_bloco ^ esperados
for marca in (ITEM_VELHO, FRASE_VELHA, ANTES_DE):
    assert r14.count(marca) == 1, "%d ocorrencias: %s" % (r14.count(marca), marca[:60])
r16 = r14.replace(ITEM_VELHO, ITEM_NOVO + ITEM_VELHO).replace(FRASE_VELHA, FRASE_NOVA).replace(ANTES_DE, BLOCO + ANTES_DE)
for novo in (ITEM_NOVO, FRASE_NOVA, BLOCO):
    assert "P = nP" not in novo and "ráculo" not in novo and "Turing" not in novo and "«" not in novo
linhas_tab = [l for l in BLOCO.split("\n") if l.startswith("| ") and not l.startswith("| o que se afirma")]
b = r16.encode("utf-8")
print("frase:", qual, "| termos conferidos nas fontes:", n_ok, "| linhas de conteudo da tabela:", len(linhas_tab), "| R14", len(r14.encode("utf-8")), "B -> R16", len(b), "B | sha16", hashlib.sha256(b).hexdigest()[:16])
if "--executar" in sys.argv:
    d = V / "o_que_fica_claro_REV16"; d.mkdir(exist_ok=True)
    p = d / ("O_QUE_FICA_CLARO_v412_R16.md" if "--vigente" in sys.argv else "O_QUE_FICA_CLARO_v412_R16_PROPOSTA_frase_%s.md" % qual)
    assert not p.exists(), "ja' existe: nao sobrescrevo"
    p.write_bytes(b); print("gravado:", p)
