# [DERIVADO v412 r7, claude-construtor-v412 (contrato R11)] copia de e5_13_secoes_tipa_v412.py; trocas de texto exato com contagem registrada em DERIVACAO_R7_PIPELINE_v412.json (derivador: e7_04_derivar_texto_v412.py). O original fica intacto.
"""R5 (so' leitura): mostra, dos cabecalhos das pedras congeladas da decima segunda lista, a secao cujo titulo diz o que o arquivo TIPA, para os modulos dados na linha de comando (ou os oito que a decima segunda lista acrescenta)."""
import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
from e7_lib_v412 import PEDRAS
mods = sys.argv[1:] or ["AClausulaExemplificativa", "ACurvaEAEstado", "AFitaEOIndice", "AFronteiraEOUnicoPortao", "OPsiBitDaFormula", "OResumoEPsiBit"]
for k in mods:
    t = (PEDRAS / (k + ".lean")).read_bytes().decode("utf-8")
    h = re.search(r"/-!(.*?)-/", t, re.S).group(1)
    secs = re.split(r"(?m)^(?=#{1,3} )", h)
    print("=====", k)
    for s in secs:
        tit = s.split("\n", 1)[0].strip()
        if tit.startswith("# ") or re.search(r"\btipa\b", tit):
            print(s.strip()[:1100]); print("   ..")
        elif tit.startswith("#"):
            print("   [secao]", tit)
