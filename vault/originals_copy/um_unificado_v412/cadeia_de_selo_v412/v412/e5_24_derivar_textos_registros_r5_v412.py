"""R5: deriva textos_registros_v412_r5.py de textos_registros_v412.py (que fica intacto): a camada cientifica ganha os dois trechos das pedras da oitava lista e troca o limite da pergunta por letra (o veredito do R5 trocou um trecho por tres);
os numeros de modulos saem do texto fixo (entram por formatacao, lidos do manifesto); entram os textos do registro novo leitor_da_formula_v412 (o que nao sai da tabela da pagina por script) e as oito entradas novas da lista de definicoes."""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
from e5_deriv_v412 import derivar
EU = "e5_24_derivar_textos_registros_r5_v412.py"
NOVO_FIM = '''
# ------------------------------------------------------------------------------------------------- leitor_da_formula_v412 (as linhas do que o artefato mostra saem da tabela da pagina publica, por script, em registros_v412_r5.py)
DIZ_L_FORMA = "[REAL] %s: %s (%s)"
DIZ_L_FECHO = "[REAL] cada limite acima é do leitor ou da representação que o teorema examina; nenhum é cota para todo procedimento"
DIZ_L_UNIDADES = "[REAL] cada classe nomeada tem a sua máquina, a sua grafia e a sua unidade (transições, passos, deslocamentos ou movimentos), ditas na linha dela; L é o comprimento da entrada na grafia da linha"
LIM_L_FORMA = "[OPEN] não está demonstrado: %s"
LIM_L = [
    "[OPEN] o polinômio fixo para a Palavra de toda fórmula plana não está demonstrado: para classes de fórmulas, cada uma com a sua máquina e a sua grafia, a leitura fecha na fita dentro de um polinômio fixo no número de letras; para a fórmula plana arbitrária, não",
    "[OPEN] quem gerasse uniformemente, a partir da entrada, os indicadores dos blocos decidiria se a fórmula tem solução; o custo dessa geração não está cotado",
]
ND_L = ["que haja um polinômio fixo em letras para a Palavra de toda fórmula plana", "que algum dos limites seja cota para todo procedimento", "que a fronteira seja o menor separador, ou o único", "que a creditação esteja feita: a creditação é do Instituto e de quem observa de fora",
        "que o gate tenha se movido", "número novo da natureza"]
LEIS_L = [
    "[INPUT] definição da teoria: a compressão sai direto da fórmula, e é o PsiBit; a leitura do par binário pelo PsiBit é a compressão originária, o próprio leitor; a regra de leitura é uma só, o sinal de igual",
    "[INPUT] definições da teoria: o separador é o piso da leitura; a curva é a releitura; a recusa é um nome com conteúdo; a verdade é o contorno; a fita é o índice e a torre",
]
ESTATUTO_L = ("[REAL — o kernel (%d módulos novos de TGLExt, dos quais %d deste registro; as âncoras deste registro: %d) e os registros anteriores, lidos a cada rito; INPUT as definições da teoria listadas em extras e em cunhagens_v412; "
              "OPEN o polinômio fixo para a Palavra de toda fórmula plana]")
'''
derivar("textos_registros_v412.py", "textos_registros_v412_r5.py", [
    ('"""textos_registros_v412.py -- o texto dos quatro registros da v412 (dados). Sai da pagina publica (O_QUE_FICA_CLARO_v412_R9.md) e dos cabecalhos das pedras congeladas, sem acrescentar afirmacao.',
     '"""textos_registros_v412_r5.py -- o texto dos cinco registros da v412 (dados). Sai da pagina publica (O_QUE_FICA_CLARO_v412_R18.md) e dos cabecalhos das pedras congeladas, sem acrescentar afirmacao.', 1),
    # a camada cientifica: os dois trechos das pedras da oitava lista, antes do item de P = nP
    ('    "[REAL] P = nP é teorema da TGL nas classes do seu dicionário:',
     '    "[REAL] o passo é o fator 1 − β, com β parâmetro real entre 0 e 1 (a identificação com o β da teoria é entrada): o ciclo fecha num número de passos linear no número de variáveis, cada passo age sobre o todo, e o Nome fica inteiro; com o fator 1 o ciclo não fecha; não é contagem de letras (OPassoEOFim)",\n'
     '    "[REAL] o par binário é a Palavra (há solução) e o Verbo (a soma lida ainda desce), lidos com o tempo pago acima da carga: o par responde por toda fórmula; é a compressão da leitura, o todo em dois bits, não a compressão a partir das letras da fórmula (OPsibitEACompressao)",\n'
     '    "[REAL] P = nP é teorema da TGL nas classes do seu dicionário:', 1),
    ('    "[OPEN] a pergunta do Instituto, se há procedimento de letras com número polinomial de passos para toda fórmula, segue em aberto e não é tautológica",',
     '    "[OPEN] um procedimento de letras com um polinômio fixo para toda fórmula não está demonstrado, e a pergunta não é tautológica; o que se sabe da contagem por letra está no registro leitor_da_formula_v412",', 1),
    ('    "[INPUT] definições da teoria de Luz e de máquina (mecanismo de processamento por circuito), enunciadas no cabeçalho de AMaquina, na seção que o arquivo tipa",',
     '    "[INPUT] definições da teoria de Luz e de máquina (mecanismo de processamento por circuito), enunciadas no cabeçalho de AMaquina, na seção que o arquivo tipa",\n'
     '    "[INPUT] lei da teoria: o passo é 1 − β; o ciclo encerra e guarda a informação preservada (OPassoEOFim)",\n'
     '    "[INPUT] lei da teoria: a compressão sai direto da fórmula, e é o PsiBit; a leitura do par binário pelo PsiBit é a compressão originária (OPsibitEACompressao)",', 1),
    ('ESTATUTO_A = ("[REAL — o kernel (42 módulos novos de TGLExt; as âncoras desta camada: %d)', 'ESTATUTO_A = ("[REAL — o kernel (%d módulos novos de TGLExt, dos quais %d desta camada; as âncoras desta camada: %d)', 1),
    ('ESTATUTO_B = ("[REAL — o kernel (42 módulos novos de TGLExt; as âncoras desta frente: %d)', 'ESTATUTO_B = ("[REAL — o kernel (%d módulos novos de TGLExt, dos quais %d desta frente; as âncoras desta frente: %d)', 1),
    ('    "TipoIIIControles": ("a luz testemunhada na cunha, a torre, a fronteira e o vínculo", "[INPUT]"),\n}',
     '    "TipoIIIControles": ("a luz testemunhada na cunha, a torre, a fronteira e o vínculo", "[INPUT]"),\n'
     '    "OPassoEOFim": ("o passo é 1 − β", "[INPUT]"),\n'
     '    "OPsibitEACompressao": ("a compressão é o PsiBit: o par binário da leitura", "[INPUT]"),\n'
     '    "OResumoEPsiBit": ("a compressão sai direto da fórmula", "[INPUT]"),\n'
     '    "OPsiBitDaFormula": ("a regra de leitura é uma só, o sinal de igual", "[INPUT]"),\n'
     '    "AFronteiraEOUnicoPortao": ("o separador é o piso da leitura", "[INPUT]"),\n'
     '    "ACurvaEAEstado": ("a curva é a releitura", "[INPUT]"),\n'
     '    "AClausulaExemplificativa": ("a verdade é o contorno; a cláusula é exemplificativa", "[INPUT]"),\n'
     '    "AFitaEOIndice": ("a fita é o índice e a torre", "[INPUT]"),\n}' + NOVO_FIM, 1),
], EU, imports=False)
