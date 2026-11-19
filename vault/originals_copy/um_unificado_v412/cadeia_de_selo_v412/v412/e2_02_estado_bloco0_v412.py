import sys
sys.path.insert(0, r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
from e2_lib_v412 import *

K = D / "kernel"
estado_bloco(
    "0_checagem_vazia_do_pos_build",
    True,
    {"derivador": D / "e2_01_derivar_pos_build_r4_v412.py", "pos_build_r4": D / "pos_build_kernel_v412_r4.py", "recibo": K / "BUILT_CHECAGEM_CORRIGIDA_R4_v412.json", "lib": D / "e2_lib_v412.py"},
    nota="a checagem Built passou vazia por filtro de prefixo; corrigida na copia _r4 (r2 e r3 intactos); examina 8 modulos; 4 controles negativos + 1 positivo",
    proximo="bloco 3 (VERBATIM_CONGELADO), depois bloco 4 (guarda de frases), bloco 2 (registros), bloco 1 (delta/gerador), 5, 6, 7, 8",
)
print("estado gravado", ESTADO)
