"""R7: deriva as copias `_r7` dos scripts de TEXTO e de REGISTROS a partir das `_r5` (pagina R18, 153 modulos) para a pagina R21 e a DECIMA SEGUNDA lista (156 modulos). Cada troca especifica tem contagem minima; o que sobra dos padroes de risco
fica no log (DERIVACAO_R7_PIPELINE_v412.json, campo risco_restante) e e' conferido por grep depois."""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_deriv_v412 as DV

ESTE = "e7_04_derivar_texto_v412.py"
COM = [("contrato R5", "contrato R11", 0), ("pagina R18", "pagina R25", 0), ("DECIMA lista", "DECIMA SEGUNDA lista", 0), ("decima lista", "decima segunda lista", 0), ("DECIMA_LISTA_CONFERIDA_v412", "DUODECIMA_LISTA_CONFERIDA_v412", 0),
       ("texto_publico_r18", "texto_publico_r25", 0), ("manifesto R10", "manifesto R12", 0), ("ancoras R10", "ancoras R12", 0), ("pedras_r10", "pedras_r12", 0)]

DIZ_A_NOVO = ("    \"[REAL] na máquina da teoria, o mecanismo de processamento por circuito fecha o circuito em tantos atos quantas as cláusulas e, fechado, responde se a fórmula tem solução (ha_o_mecanismo, em AMaquina); "
              "ao longo do ciclo do passo 1 − β, a atribuição que resolve guarda o peso 1 e o Nome fica inteiro (o_nome_fica_inteiro, em OPassoEOFim)\",\n")
LEIS_A_NOVAS = ("    \"[INPUT] definição da teoria: Tetelestai é a consumação cíclica do processamento mecânico que permite resposta coerente, a conferência que devolve consumado ou não consumado\",\n"
                "    \"[ONTO] que o sim da resposta seja o Tetelestai do processamento é leitura da teoria, não termo\",\n")
DIZ_L_MAQUINA = ('DIZ_L_MAQUINA = ("[REAL] na máquina da teoria, com passos que são atos sobre o todo e não movimentos de cabeça na fita: o polinômio fixo dos passos, p(n) = (ln 2/β)·n, é dado por β antes de qualquer fórmula e é o mesmo teto para toda fórmula de n variáveis "\n'
                 '                "(o_polinomio_fixo_e_beta, o_mesmo_teto_para_duas_formulas, em OPolinomioFixoEBeta); sem o pagamento o ciclo não fecha, e com o passo 1 − β ele fecha linearmente na carga (a_razao_do_colapso, em ORazaoDoColapsoEBeta); "\n'
                 '                "decidir custa a carga, nem mais nem menos (o_custo_de_decidir_e_a_carga, em OCustoEAIsometria); β é parâmetro real entre 0 e 1 e a identificação com o β da teoria é entrada; 1 − β é o fator de cada passo, não um polinômio no número de letras")\n')
LEIS_L_NOVA = ("    \"[INPUT] definições da teoria: o polinômio fixo dos passos é dado por β, anterior a toda fórmula; o colapso é a razão do polinômio (sem o pagamento o ciclo não fecha; com o passo 1 − β ele fecha linearmente na carga); o custo é a carga, a isometria\",\n")

DERIVACOES = [
    ("textos_registros_v412_r5.py", "textos_registros_v412_r7.py", COM + [
        ('    "[REAL] o par binário é a Palavra (há solução)', DIZ_A_NOVO + '    "[REAL] o par binário é a Palavra (há solução)', 1),
        ('    "[ONTO] ler o problema como pergunta de existência de mecanismo', LEIS_A_NOVAS + '    "[ONTO] ler o problema como pergunta de existência de mecanismo', 1),
        ('    "AFitaEOIndice": ("a fita é o índice e a torre", "[INPUT]"),\n', '    "AFitaEOIndice": ("a fita é o índice; a torre é a forma do índice", "[INPUT]"),\n'
         '    "OPolinomioFixoEBeta": ("o polinômio fixo dos passos é dado por β", "[INPUT]"),\n    "ORazaoDoColapsoEBeta": ("o colapso é a razão do polinômio", "[INPUT]"),\n    "OCustoEAIsometria": ("o custo é a carga, a isometria", "[INPUT]"),\n', 1),
        ("a verdade é o contorno; a fita é o índice e a torre\"", "a verdade é o contorno; a fita é o índice; a torre é a forma do índice\"", 1),
        ("DIZ_L_UNIDADES = ", DIZ_L_MAQUINA + "DIZ_L_UNIDADES = ", 1),
        ("]\nESTATUTO_L = (", LEIS_L_NOVA.rstrip("\n") + "\n]\nESTATUTO_L = (", 1)]),
    ("registros_v412_r5.py", "registros_v412_r7.py", COM + [
        ("[TX.DIZ_L_UNIDADES] + diz_tab + [TX.DIZ_L_FECHO]", "[TX.DIZ_L_UNIDADES] + diz_tab + [TX.DIZ_L_MAQUINA, TX.DIZ_L_FECHO]", 1)]),
    ("e5_12_titulos_dos_cabecalhos_v412.py", "e7_12_titulos_dos_cabecalhos_v412.py", COM + [('"lista": "decima (insumos/pedras_r12)"', '"lista": "duodecima (insumos/pedras_r12)"', 1)]),
    ("e5_13_secoes_tipa_v412.py", "e7_13_secoes_tipa_v412.py", COM + []),
    ("e5_60_registros_v412.py", "e7_60_registros_v412.py", COM + []),
    ("texto_publico_v412_r5.py", "texto_publico_v412_r7.py", COM + [
        # (R11, gerencia c1, 18/11) a pagina R25 traz theta (o estado de angulo), pi (pi/4) e o piso (floor(p(n)) + 1), que o inputenc utf8
        # do artigo nao cobre: o pdflatex parava em "Unicode character". So' acrescimo na tabela; nada do que ja' convertia muda.
        ('GREGAS = {"τ": r"\\tau", "α": r"\\alpha", "β": r"\\beta", "ρ": r"\\rho", "σ": r"\\sigma", "Δ": r"\\Delta", "Λ": r"\\Lambda"}',
         'GREGAS = {"τ": r"\\tau", "α": r"\\alpha", "β": r"\\beta", "ρ": r"\\rho", "σ": r"\\sigma", "Δ": r"\\Delta", "Λ": r"\\Lambda", "θ": r"\\theta", "π": r"\\pi", "⌊": r"\\lfloor", "⌋": r"\\rfloor"}', 1)]),
    ("blocos_texto_publico_v412_r5.py", "blocos_texto_publico_v412_r7.py", COM + []),
    ("e5_23_texto_publico_gerar_v412.py", "e7_23_texto_publico_gerar_v412.py", COM + [('"4a_texto_publico_r18"', '"4a_texto_publico_r21"', 0)]),
    ("guarda_frases_v412_r5.py", "guarda_frases_v412_r7.py", COM + []),
    ("e5_30_verbatim_congelado_v412.py", "e7_30_verbatim_congelado_v412.py", COM + []),
    ("verificar_historia_texto_v412_r5.py", "verificar_historia_texto_v412_r7.py", COM + []),
    ("runtime_v412_codigo_r5.py", "runtime_v412_codigo_r7.py", COM + []),
]
for orig, dest, trocas in DERIVACOES:
    DV.derivar(orig, dest, trocas, ESTE)
