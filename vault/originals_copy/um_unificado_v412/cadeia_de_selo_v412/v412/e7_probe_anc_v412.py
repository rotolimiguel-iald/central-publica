"""R7 (so' leitura): mostra campos de ANCORAS_ESCOLHIDAS_v412.json: os nomes da pagina fora da tabela que nao sao declaracao de modulo da lista; os problemas; a tabela do leitor."""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
D = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
a = json.loads((D / "ANCORAS_ESCOLHIDAS_v412.json").read_bytes().decode("utf-8"))
print("fora da lista:", a["nomes_da_pagina_fora_da_tabela_do_leitor_que_nao_sao_declaracao_de_modulo_da_lista"])
print("problemas:", json.dumps(a["problemas"], ensure_ascii=False)[:800])
print("tabela:", {k: v for k, v in a["tabela_do_leitor"].items() if k != "termos_sem_ancora_em_modulo_da_linha"}, a["tabela_do_leitor"]["termos_sem_ancora_em_modulo_da_linha"])
for r, v in a["registros"].items():
    for m, d in v["modulos"].items():
        if d["citados_pela_pagina"] and "pagina" in str([x["regras"] for x in d["ancoras"]]):
            pass
print("n termos citados pela pagina em modulos:", sum(len(d["citados_pela_pagina"]) for v in a["registros"].values() for d in v["modulos"].values()))
