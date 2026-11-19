"""cria o JSON da ROTA cadeia.preparacao_v412.etapa2_candidato (tipo ROTA) a partir do registro de RESULTADO ja' escrito (mesmos campos de identificacao); o rotas.py exige a ROTA antes do RESULTADO."""
import json, sys
from pathlib import Path
D = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
r = json.loads((D / "registro_mapa_construtor_etapa2_v412.json").read_bytes().decode("utf-8"))
rota = {"tipo": "ROTA", "rota_id": r["rota_id"], "dominio": r["dominio"], "titulo": r["titulo"], "pergunta": r["pergunta"], "dados": r["dados"], "metodo": r["metodo"],
        "resultado": "(a rota abre aqui; o resultado vem no registro seguinte)", "estatuto": "REAL", "status": "EM_CURSO", "olhou_dados": False, "refs": r["refs"],
        "nota": "Rota da Etapa 2 da v412 pelo contrato R4: candidato, guarda por travessia, ensaio a seco. Consultou o Mapa antes (rotas da v412)."}
(D / "registro_mapa_construtor_etapa2_rota_v412.json").write_bytes(json.dumps(rota, ensure_ascii=False, indent=1).encode("utf-8"))
print("ok")
