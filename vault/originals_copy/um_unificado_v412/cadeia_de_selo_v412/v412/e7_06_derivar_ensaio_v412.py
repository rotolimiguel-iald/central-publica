"""R7: deriva as copias `_r7` do ENSAIO A SECO e dos seus auxiliares a partir das `_r5` (pagina R18, 153 modulos) para a pagina R21 e a DECIMA SEGUNDA lista (156 modulos). O ensaio le as contagens do contrato, do manifesto e do kernel
(nada e' digitado); as trocas sao so' de nome de arquivo e de texto de rotulo. O que sobra dos padroes de risco e' listado no log e conferido por grep depois."""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_deriv_v412 as DV

ESTE = "e7_06_derivar_ensaio_v412.py"
COM = [("contrato R5", "contrato R11", 0), ("pagina R18", "pagina R25", 0), ("DECIMA lista", "DECIMA SEGUNDA lista", 0), ("decima lista", "decima segunda lista", 0), ("DECIMA_LISTA_CONFERIDA_v412", "DUODECIMA_LISTA_CONFERIDA_v412", 0),
       ("manifesto R10", "manifesto R12", 0), ("ancoras R10", "ancoras R12", 0), ("pedras_r10", "pedras_r12", 0)]
LISTA = ["guarda_ordem_de_chamada_v412_r5.py", "exame_pontos_v412_r5.py", "simular_arvore_do_nos_v412_r5.py", "guardas_estaticas_bancada_v412_r5.py", "conferir_citacoes_v412_r5.py", "topo_com_resultado_v412_r5.py",
         "guarda_conversa_v412_r5.py", "quadro_v397_r5.py", "e3_topo_derivado_v412_r5.py", "ensaio_a_seco_v412_r5.py"]
for orig in LISTA:
    DV.derivar(orig, orig.replace("_r5", "_r7"), COM, ESTE)
DV.derivar("e5_71_resultado_ensaio_v412.py", "e7_71_resultado_ensaio_v412.py", COM, ESTE)
