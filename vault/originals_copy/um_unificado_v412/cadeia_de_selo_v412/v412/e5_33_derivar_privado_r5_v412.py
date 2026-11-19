"""R5: deriva guarda_material_privado_v412_r5.py (os insumos pinados passam a ser os do contrato R5: a pagina R18 e a traducao, os textos novos, o contrato R5 e tudo de insumos\\; VERBATIM_CONGELADO_v412.json segue FORA da varredura, resposta 7 da D224)."""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
from e5_deriv_v412 import derivar
derivar("guarda_material_privado_v412.py", "guarda_material_privado_v412_r5.py", [
    ('os.path.join(HERE, "o_que_fica_claro_REV13", "O_QUE_FICA_CLARO_v412_R13.md")', 'os.path.join(HERE, "o_que_fica_claro_REV18", "O_QUE_FICA_CLARO_v412_R18.md")', 1),
    ('os.path.join(HERE, "O_QUE_FICA_CLARO_v412_R13_EN.md")', 'os.path.join(HERE, "O_QUE_FICA_CLARO_v412_R18_EN.md")', 1),
    ('os.path.join(HERE, "CONTRATO_v412_R4.md")]', 'os.path.join(HERE, "CONTRATO_v412_R5.md")]', 1),
], "e5_33_derivar_privado_r5_v412.py")
