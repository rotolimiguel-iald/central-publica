import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
CONSULTAS = BASE / "consultas"
resumo = {}
for path in sorted(CONSULTAS.glob("ver_*.txt")):
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    rota = payload.get("rota", {})
    resumo[path.name] = {
        "rota_id": rota.get("rota_id"),
        "status": rota.get("status"),
        "titulo": rota.get("titulo"),
        "pergunta": rota.get("pergunta"),
        "dados": rota.get("dados"),
        "metodo": rota.get("metodo"),
        "resultado": rota.get("resultado"),
        "veredito": rota.get("veredito"),
        "defeito": rota.get("defeito"),
        "nao_refazer": rota.get("nao_refazer"),
        "historico": rota.get("historico"),
        "registros": [
            {
                chave: registro.get(chave)
                for chave in (
                    "seq", "tipo", "titulo", "status", "veredito", "resultado",
                    "dados", "metodo", "pergunta", "nota", "defeito", "nao_refazer",
                )
                if chave in registro
            }
            for registro in payload.get("registros", [])
        ],
    }
with (BASE / "indice_rotas_lido.json").open("w", encoding="utf-8") as handle:
    json.dump(resumo, handle, ensure_ascii=False, indent=2)
    handle.write("\n")

fase9 = resumo["ver_Fase9.txt"]
with (BASE / "fase9_resumo_e_sequencias.txt").open("w", encoding="utf-8") as handle:
    for chave in ("rota_id", "status", "titulo", "pergunta", "dados", "metodo", "resultado", "veredito", "defeito", "nao_refazer"):
        handle.write(f"{chave.upper()}: {fase9.get(chave)}\n\n")
    handle.write("HISTÓRICO (seq; tipo; status; resumo)\n")
    for item in fase9.get("historico") or []:
        handle.write(f"{item.get('seq')}; {item.get('tipo')}; {item.get('status')}; {item.get('resumo')}\n")
