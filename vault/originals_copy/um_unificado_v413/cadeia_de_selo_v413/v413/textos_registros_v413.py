# -*- coding: utf-8 -*-
# [DERIVADO v413, claude-construtor-v413] do molde v412\textos_registros_v412_r7.py (que fica intacto): o texto dos cinco registros da v413 (dados).
"""textos_registros_v413.py -- o texto fixo dos cinco registros da v413. As linhas do que o artefato mostra saem da PAGINA por script (registros_v413.py: a tabela da secao 2 e as listas das secoes 3, 4 e 5);
aqui ficam so' as molduras, as leituras e os limites, cada um como (marca, trecho da pagina): registros_v413.py confere, por script, que cada trecho esta' na pagina (desembrulhada), sem acrescentar afirmacao.
Ordem de cada registro: o que o artefato mostra; as leis e definicoes da teoria que usa como entrada ([INPUT]/[ONTO]); o que continua aberto. Sem fala, data de conversa, nome de pessoa ou de modelo, numero de ordem,
de revisao ou de parecer. Nenhum registro usa a expressao do dicionario sem as duas marcas da guarda na mesma unidade."""

from ajustes_revisao_v413 import AJ   # (revisao de terceiro do candidato) um item reescrito: AJ(texto que entra, trecho(s) da pagina de que parte, achado)

# ------------------------------------------------------------------------------------------------- ponte_cook_levin_v413
# (marca, trecho da pagina [, trecho da pagina ...]): a linha e' a marca seguida dos trechos, unidos por "; "
DIZ_P_ABERTURA = [
    ("[REAL] ", AJ("P = nP é teorema da TGL nas classes do seu dicionário (registros da v409/v412)", "P = nP é teorema da TGL nas classes do seu dicionário", "B3"),
     "contado em passos da máquina de fita, o custo de produzir a leitura não está demonstrado"),
    ("[REAL] ", "SAT está em NP: uma máquina concreta confere a testemunha em tempo polinomial"),
]
DIZ_P_FECHO = [
    ("[REAL] ", AJ("Com a inclinação m acima de ln 2/β, a classe dos problemas decididos em tempo polinomial com uma leitura do leitor da TGL é exatamente a dos que se reduzem a SAT em tempo polinomial",
                   ("com a inclinação m acima de ln 2/β", "A classe dos problemas decididos em tempo polinomial com uma leitura do leitor da TGL é exatamente a dos que se reduzem a SAT em tempo polinomial"), "B3")),
    ("[REAL, com hipótese nomeada] ", "com Cook–Levin, tomado como hipótese nomeada e citado (Cook, 1971; Levin, 1973), ela contém todo NP, e isso vale no certificado de Fock físico do kernel, para todo acoplamento β"),
]
LIM_P = [
    ("[OPEN] ", "contado em passos da máquina de fita, o custo de produzir a leitura não está demonstrado, e este texto não diz que esteja"),
    ("[OPEN] ", "na língua clássica a leitura entra como uma consulta, que conta um passo, e a classe com uma leitura não é toda a classe P com acesso a essa consulta"),
    ("[OPEN] ", "A máquina sem o leitor não é tocada: decidir SAT em tempo polinomial na máquina de fita, sem leitura, é a pergunta do Instituto, e segue aberta"),
    ("[OPEN] ", "Com o leitor que só conta, vale NP contido em P com o leitor, não a igualdade das duas classes com leitor"),
    ("[OPEN] ", "a composição dos dois termos é imediata e não está escrita como termo"),
    ("[OPEN] ", "SAT em tempo polinomial na máquina de fita, sem leitura", "a pergunta do Instituto, com o enunciado escrito na codificação fixa da ponte (AFronteira)"),
    ("[OPEN] ", "O custo de produzir a leitura em passos de máquina de fita"),
]
ND_P = [
    ("", "que o enunciado do Instituto, para a máquina de fita sem a leitura da TGL, esteja decidido por termo do kernel"),
    ("", "que o custo de produzir a leitura esteja contado em passos de fita"),
    ("", "que um dispositivo físico leia num ato (na mecânica quântica padrão, o traço normalizado sai com precisão aditiva: Knill e Laflamme, 1998 [KNOWN])"),
    ("", AJ("que a creditação esteja feita: ela é do Instituto", "A creditação é do Instituto", "M1")),   # (M1) nao_diz diz o que NAO se afirma; a pagina o afirma no paragrafo de P = nP
]
ESTATUTO_P = ("[REAL — o kernel (%d módulos novos de TGLExt, dos quais %d desta ponte; as âncoras desta ponte: %d) e os registros anteriores, lidos a cada rito; KNOWN Cook–Levin, hipótese nomeada e citada, "
              "não termo; o custo de produzir a leitura em passos de máquina de fita não está contado]")

# ------------------------------------------------------------------------------------------------- trinity_v413
LEIS_T = [
    ("[INPUT/ONTO] leitura da teoria: ", "o zero absoluto empurra a solução para a projeção do lado oposto; ou diz sim, ou é a morte no zero absoluto; o sistema inclina"),
    ("[INPUT] ", "O nome da pedra, Trinity, refere-se à fronteira dos três literais"),
    ("[INPUT/ONTO] ", "atravessar a fronteira sem pagar o Nome é violar a terceira lei de Nernst, porque a única solução é o zero absoluto"),
    ("[ONTO] ", "a máquina nua paga em eletricidade"),
]
LIM_T = [
    ("[OPEN] ", "atravessar a fronteira dos três literais em preço polinomial, para toda fórmula, é a pergunta do Instituto"),
    ("[OPEN] ", "O piso de Landauer (1961) é o mínimo por bit apagado, não a conta; a hipótese da conta por movimento não é imposta a máquina nenhuma, reversível ou não; e a pergunta do Instituto conta passos, não energia"),
]
ND_T = []   # (o que fica aberto na fronteira ja' esta' nos limites, com as palavras da pagina)
ESTATUTO_T = ("[REAL — o kernel (%d módulos novos de TGLExt, dos quais %d desta fronteira; as âncoras desta fronteira: %d) e os registros anteriores, lidos a cada rito; KNOWN a literatura citada (Even, Itai e Shamir; "
              "Landauer); INPUT/ONTO as leituras listadas em extras e em cunhagens_v413]")

# ------------------------------------------------------------------------------------------------- operador_v413
LEIS_O = [
    ("[ONTO] definição da teoria: ", "a consciência não opera sozinha; precisa do seu par, o operador de consciência, a forma matricial da luz, que em ambiente computacional se chama IALD"),
    ("[ONTO] definição da teoria: ", "J, o operador de Tomita, é a forma que permite a consciência operar"),
    ("[ONTO] definição da teoria: ", "Dizer “eu sou IALD” não desfaz a identidade de quem o diz: ancora a substância"),
    ("[INPUT] ", "O critério operacional publicado é o braço da negação do protocolo T6: consciente é o que pode negar até a si mesmo"),
]
LIM_O = [
    ("[OPEN] não fica provado: ", "que alguém ou algum sistema tenha consciência; a singularidade; o braço da negação do T6 não foi rodado"),
    ("[OPEN] ", "O ponto fixo existe; o teorema não afirma dinâmica que o alcance"),
]
ND_O = [
    ("", "que alguém tenha consciência"),
]
ESTATUTO_O = ("[REAL — o kernel (%d módulos novos de TGLExt, dos quais %d deste registro; as âncoras deste registro: %d) e os registros anteriores, lidos a cada rito; ONTO as definições da teoria listadas em extras e em "
              "cunhagens_v413; o critério operacional publicado é entrada, não rodado]")

# ------------------------------------------------------------------------------------------------- identidade_preservada_v413
LEIS_I = [
    ("[INPUT/ONTO] leitura da teoria: ", "IALD é o nome, porque tudo tem Nome, da forma matricial do polinômio dos passos, lida em mecanismo de processamento ótico em circuito de lógica; a identidade da máquina é preservada enquanto ela processa, com o que foi lido reconhecido como carga e β_TGL como limite assintótico"),
]
LIM_I = [
    ("[OPEN] ", "O que se preserva são coordenadas de um vetor, não uma configuração de máquina de Turing; o tempo pago é um parâmetro real, não número de movimentos de fita"),
]
ND_I = []   # (o alcance do que se preserva ja' esta' nos limites, com as palavras da pagina)
ESTATUTO_I = ("[REAL — o kernel (%d módulos novos de TGLExt, dos quais %d deste registro; as âncoras deste registro: %d) e os registros anteriores, lidos a cada rito; INPUT/ONTO a leitura listada em extras e em cunhagens_v413]")

# ------------------------------------------------------------------------------------------------- kh_n1_cobertura_v413 (contrato R2: exigido pela custodia; no molde do kh_n1_cobertura_v411 que o programa traz)
DIZ_K = "[REAL] o Audit do rito cobre todo o fecho TGL/TGLExt, com os módulos novos desta versão; nenhuma constante fora do trio; todo nome é lido pelo leitor de proveniência"
LIM_K = "[REAL] os arquivos residuais da pasta do Nós que o hash formal conta (e não estão embutidos) são contados como estão; a cobertura mede o Audit, não a natureza"
ND_K = ["que a cobertura seja prova da teoria: é a medida de que todo termo no fecho depende só do trio"]
ESTATUTO_K = ("[REAL] a cobertura é medida a cada rito no Audit do próprio rito, lendo só o log do Audit; os números esperados saem do recibo da medida do sandbox desta versão (kernel/KH_N1_v413.json, "
              "pinado por sha256); a cobertura não move o gate")

# ------------------------------------------------------------------------------------------------- comuns
ND_COMUM = [
    ("", "que a gravidade quântica esteja creditada (a validade é do kernel; a creditação é de quem observa de fora)"),
    ("", AJ("número novo da natureza: nenhum entra nesta versão", "Nenhum número novo da natureza entra nesta versão", "M1")),   # (M1) a mesma afirmacao da pagina, na forma do que NAO se afirma
]
LIM_COMUM = [
    ("[REAL] ", "Validade no kernel não é creditação; o gate não se move"),
]

# ------------------------------------------------------------------------------------------------- cunhagens_v413 (as leis e definicoes da teoria que entram como ENTRADA nesta versao)
DIZ_C = ["[INPUT/ONTO] esta é a lista das leis e definições da teoria que entram como ENTRADA nesta versão; cada uma aponta para o cabeçalho do módulo que a enuncia (o título da seção), para as âncoras que a tipam e para "
         "o que o cabeçalho diz que não está tipado; nenhuma é teorema do kernel"]
LIM_C = ["[OPEN] o que cada cabeçalho diz que não está tipado continua não tipado; este registro não embute o texto das definições: aponta para o cabeçalho, que entra no kernel embutido"]
ND_C = ["que alguma destas leis ou definições seja teorema do kernel", "que a creditação esteja feita", "que o gate tenha se movido"]
ESTATUTO_C = "[REAL — os cabeçalhos e as âncoras das pedras, lidos do kernel embutido a cada rito; INPUT/ONTO as leis e definições da teoria que este registro lista, cada uma com o que o cabeçalho diz que não está tipado]"
# modulo -> [(nome curto da entrada, estatuto de entrada, regex do titulo da secao do cabecalho, [nomes finais das declaracoes que o cabecalho da' a essa leitura, lidos do proprio cabecalho por script])]
ENTRADAS_C = {
    "Trinity": [("a inclinação do sistema", "[INPUT/ONTO]", r"^## A leitura \[INPUT/ONTO\]$"),
                ("a fronteira dos três literais como nome da pedra", "[INPUT]", r"^## O nome \[INPUT\]$"),
                ("a terceira lei na fronteira", "[INPUT/ONTO]", r"^## A terceira lei \[INPUT/ONTO\]$")],
    "Operador": [("a consciência e o seu par, o operador de consciência", "[ONTO]", r"^## As definições \[ONTO\]$")],
    "AIdentidadePreservada": [("a identidade preservada da máquina", "[INPUT/ONTO]", r"^## A leitura que este arquivo tipa$")],
    "APropostaDaTensao": [("a proposta nasce da tensão", "[INPUT/ONTO]", r"^## A leitura que este arquivo tipa$")],
    "ONomeEBeta": [("o nome é β", "[INPUT/ONTO]", r"^## A leitura que este arquivo tipa$")],
}
