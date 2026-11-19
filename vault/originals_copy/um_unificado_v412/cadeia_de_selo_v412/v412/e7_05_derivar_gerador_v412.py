"""R7: deriva as copias `_r7` do DELTA, do GERADOR do candidato, dos RECIBOS, da guarda de material privado e do fecho do kernel a partir das `_r5` (153 modulos, pagina R18) para a DECIMA SEGUNDA lista (156 modulos) e a pagina R21."""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_deriv_v412 as DV

ESTE = "e7_05_derivar_gerador_v412.py"
COM = [("contrato R5", "contrato R11", 0), ("pagina R18", "pagina R25", 0), ("DECIMA lista", "DECIMA SEGUNDA lista", 0), ("decima lista", "decima segunda lista", 0), ("DECIMA_LISTA_CONFERIDA_v412", "DUODECIMA_LISTA_CONFERIDA_v412", 0),
       ("texto_publico_r18", "texto_publico_r25", 0), ("manifesto R10", "manifesto R12", 0), ("ancoras R10", "ancoras R12", 0), ("pedras_r10", "pedras_r12", 0), ("a pagina R9", "a pagina R24", 0)]
DERIVACOES = [
    ("delta_v412_r5.py", "delta_v412_r7.py", COM + [
        ("== N_MODULOS_DO_MANIFESTO == 153 and", "== N_MODULOS_DO_MANIFESTO == 156 and", 1), ("manifesto vigente (153)", "manifesto vigente (156)", 1), ("os 153 modulos novos de TGLExt/", "os 156 modulos novos de TGLExt/", 1),
        ("o bundle dos 40 modulos", "o bundle dos 156 modulos", 0), ("(40 modulos)", "(156 modulos)", 0)]),
    ("gerar_candidato_v412_r5.py", "gerar_candidato_v412_r7.py", COM + [
        ("len(nov) == DL.N_MODULOS_DO_MANIFESTO == 153", "len(nov) == DL.N_MODULOS_DO_MANIFESTO == 156", 1), (" (A) kernel: 153 modulos novos", " (A) kernel: 156 modulos novos", 1), ("regenerada com os 40 imports", "regenerada com os 156 imports", 1),
        ("os 40 modulos do bundle", "os 156 modulos do bundle", 0),
        # (R10) o nome do modulo no livro de pedras e' composto em LaTeX (coluna de texto): dois modulos tem nome de arquivo em minusculas com sublinhado (sonda_cadeia_caminho, sonda_n0_contraexemplo), e o sublinhado cru faz o pdflatex parar (Missing $ inserted). Mostra-se o nome com o sublinhado escapado; o `rel` (que acha o arquivo e o hash) nao muda.
        ("'    (\"v412\", \"%s\", \"%s\", None, None),%s' % (_nome_mod(rel), rel, CRLF)", "'    (\"v412\", \"%s\", \"%s\", None, None),%s' % (_nome_mod(rel).replace(\"_\", chr(92) * 2 + \"_\"), rel, CRLF)", 1)]),
    ("e5_40_recibos_v412.py", "e7_40_recibos_v412.py", COM + []),
    ("guarda_material_privado_v412_r5.py", "guarda_material_privado_v412_r7.py", COM + []),
    ("gerar_pronto_kernel_r5_v412.py", "gerar_pronto_kernel_r7_v412.py", COM + [
        ("n_marcas == N == 153 and", "n_marcas == N == 156 and", 1), ("o esperado e' 153 de 153", "o esperado e' 156 de 156", 1), ("as bandeiras novas so' dos 111 modulos novos", "as bandeiras novas so' dos 114 modulos novos", 1),
        ("KERNEL DA DECIMA SEGUNDA lista FECHADO NO SANDBOX k412c: 153 de 153 compilaram a frio", "KERNEL DA DECIMA SEGUNDA LISTA FECHADO NO SANDBOX k412c: 156 de 156 compilaram a frio", 0), ("KERNEL DA DECIMA lista FECHADO NO SANDBOX k412c: 153 de 153 compilaram a frio", "KERNEL DA DECIMA SEGUNDA LISTA FECHADO NO SANDBOX k412c: 156 de 156 compilaram a frio", 0),
        ("compilaram com os 153 imports", "compilaram com os 156 imports", 1), ('"contrato_r5"', '"contrato_r7"', 1), ("a decima segunda lista foi conferida (12/12)", "a decima segunda lista foi conferida (todas as checagens)", 0), ("a decima lista foi conferida (12/12)", "a decima segunda lista foi conferida (todas as checagens)", 0),
        ("os 153 modulos novos, a raiz e o Audit foram compilados neste build; para isso os artefatos de build dos 42 modulos da setima lista foram MOVIDOS", "os 156 modulos, a raiz e o Audit foram compilados neste build; para isso os artefatos de build dos 156 modulos da decima primeira lista foram MOVIDOS (FRIO_DAS_156_R11_v412.json; o kernel da decima primeira lista ficou guardado em kernel\\\\GUARDA_R7_KERNEL_v412.json)", 1),
        # (R11, gerencia c1, 18/11) o build a frio da decima segunda lista moveu os artefatos dos 156 (e7_03b_frio_das_156_v412.py): o fecho le o recibo novo
        ('frio = ler_json(K / "FRIO_DOS_42_R5_v412.json")', 'frio = ler_json(K / "FRIO_DAS_156_R11_v412.json")', 1),
        ('"artefatos_dos_42_movidos_para_a_compilacao_a_frio"', '"artefatos_dos_156_movidos_para_a_compilacao_a_frio"', 1),
        ('"PRE_COLISAO_v412_R5.json", "FRIO_DOS_42_R5_v412.json",', '"PRE_COLISAO_v412_R5.json", "FRIO_DAS_156_R11_v412.json",', 1),
        ("scripts _r5 derivados dos _c4 por troca exata com contagem registrada (DERIVACAO_R5_v412.json); os anteriores ficam intactos; o estado do fecho R4 de kernel/ tem copia .bak_c4 (kernel/GUARDA_C4_v412.json)",
         "scripts _r7 derivados dos _r5 por troca exata com contagem registrada (DERIVACAO_R7_PIPELINE_v412.json); os anteriores ficam intactos; o estado do kernel da decima lista foi copiado para fora de work\\\\ (kernel/GUARDA_R5_KERNEL_v412.json)", 1),
        ("KERNEL DA DECIMA LISTA FECHADO NO SANDBOX k412c: 153 de 153", "KERNEL DA DECIMA SEGUNDA LISTA FECHADO NO SANDBOX k412c: 156 de 156", 1),
        ("a frio os 153 modulos novos","a frio os 156 modulos", 0), ("a decima lista", "a decima segunda lista", 0),
        ("dos 153 modulos da decima segunda lista foram MOVIDOS", "dos 153 modulos da decima lista foram MOVIDOS", 0),
        ("N = int(man[\"n_modulos\"])\n", "N = int(man[\"n_modulos\"])\n_gd = Path(ler_json(K / \"GUARDA_R5_KERNEL_v412.json\")[\"destino\"])\npos10, fl10 = ler_json(_gd / \"kernel\" / \"POS_BUILD_v412.json\"), ler_json(_gd / \"kernel\" / \"FLAGS_v412.json\")\n", 1),
        ('         "estatuto": "[REAL] medido no sandbox', '         "decima_lista_build_anterior": {"nota": "o build da decima lista (153 modulos, a frio, saida zero) fica so\' como informacao: nao e\' o kernel do candidato", "linha_TOTAL": pos10["linha_TOTAL"], "escada": fl10["escada"], "n_bandeiras": fl10["n_flags"], "copia": str(_gd)},\n         "estatuto": "[REAL] medido no sandbox', 1)]),
]
for orig, dest, trocas in DERIVACOES:
    DV.derivar(orig, dest, trocas, ESTE)
