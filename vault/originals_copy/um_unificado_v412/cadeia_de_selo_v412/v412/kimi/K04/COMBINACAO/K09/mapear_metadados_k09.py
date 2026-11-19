"""Extrai metadados documentais da K09; nao carrega NPZ nem avalia R3/R4/R5/R7."""
from __future__ import annotations

import collections
import datetime as dt
import hashlib
import json
from pathlib import Path

RAIZ = Path(r"C:\IALD")
AQUI = Path(__file__).resolve().parent
CORE = RAIZ / r"Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
MAPA = RAIZ / r"MAPA_DE_ROTAS\rotas.jsonl"
REDE = RAIZ / r"Central de Patentes\work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov\network"


def sha256(caminho: Path) -> str:
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


def escrever_json(caminho: Path, objeto: object) -> None:
    caminho.write_text(json.dumps(objeto, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    # Leitura estritamente documental: chaves ja seladas, sem calculo novo.
    core = json.loads(CORE.read_text(encoding="utf-8"))["core"]["h0dn_bg1_v411"]
    values = core["values"]
    print("=== values.decomposicao_conferencias: somente somas de pesos")
    decomposicao = values["decomposicao_conferencias"]
    print(json.dumps({k: decomposicao[k] for k in ("soma_w2", "sum_w2_touched", "soma_w2_ok")}, ensure_ascii=False, indent=2))
    print("=== values.estresse.i_tau_por_linha: modelo, tau e D ja selados")
    estresse_tau = values["estresse"]["i_tau_por_linha"]
    print(json.dumps({k: estresse_tau[k] for k in ("modelo", "tau_hat", "D")}, ensure_ascii=False, indent=2))
    print("=== referencias R3/R4/R7 ja seladas")
    esperado = values["esperado_pelos_agregados"][1]
    referencias = {
        "primario": {k: values["primario"].get(k) for k in ("D", "z_null", "p_unilateral")},
        "cefeidas_livres": {"D": values["cefeidas_livres"]["D"]},
        "esperado_cefeidas_livres": {k: esperado[k] for k in ("z_nulo_esperado", "z_K_esperado", "prob_z_nulo_ge_5_dado_o_publicado")},
    }
    print(json.dumps(referencias, ensure_ascii=False, indent=2))

    fatores = json.loads((REDE / "factors.json").read_text(encoding="utf-8"))
    por_familia = collections.defaultdict(list)
    for fator in fatores:
        por_familia[fator["family"]].append({
            "index": fator["index"],
            "name": fator["name"],
            "upstream_semantics": fator["upstream_semantics"],
        })
    print("=== fatores: somente identificadores e semantica documental")
    print(json.dumps({k: v for k, v in por_familia.items() if k != "HMS"}, ensure_ascii=False, indent=2))
    print("=== contagens de fatores")
    print(json.dumps({k: len(v) for k, v in por_familia.items()}, ensure_ascii=False, sort_keys=True))

    # Censo R7: recorta o estado examinado pelo revisor, antes do seq 2063.
    registros = []
    with MAPA.open("rb") as fonte:
        for numero_linha, linha in enumerate(fonte, 1):
            try:
                registro = json.loads(linha.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue
            if isinstance(registro.get("seq"), int) and registro["seq"] <= 2062:
                registros.append((numero_linha, registro))

    olhou = [(n, r) for n, r in registros if r.get("olhou_dados") is True and r.get("rota_id")]
    rotas_todas = {r["rota_id"] for _, r in registros if r.get("rota_id")}
    rotas_olhou = {r["rota_id"] for _, r in olhou}
    rotas_hubble = sorted({
        r["rota_id"] for _, r in olhou
        if r["rota_id"].startswith(("d1.", "hubble.")) or "h0dn" in r["rota_id"]
    })
    agora = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    consulta = {
        "fonte": str(MAPA),
        "recorte": "registros JSONL validos com seq inteiro <= 2062; mesmo universo de 2.062 registros da revisao de 14/11/2026",
        "filtro_olhou_dados": "olhou_dados is true e rota_id presente",
        "filtro_hubble": "rota_id começa com d1. ou hubble., ou contém h0dn",
        "agregacao": "rota_id distinto; registros permanecem apenas como metadados",
        "finalidade": "teto de contagem para R7; nao é N independente nem denominador Sidak",
    }
    linhas_exportadas = [{
        "seq": r["seq"],
        "rota_id": r["rota_id"],
        "quando": r.get("quando"),
        "tipo": r.get("tipo"),
        "dominio": r.get("dominio"),
        "olhou_dados": True,
        "grupo_hubble_pela_consulta": r["rota_id"] in rotas_hubble,
    } for _, r in olhou]
    exportacao = {
        "estatuto": "METADADOS_DE_CENSO__TETO_NAO_N_INDEPENDENTE",
        "data_exportacao": agora,
        "consulta": consulta,
        "totais": {
            "registros_no_recorte": len(registros),
            "rotas_no_recorte": len(rotas_todas),
            "registros_olhou_dados": len(olhou),
            "rotas_olhou_dados": len(rotas_olhou),
            "rotas_hubble_olhou_dados": len(rotas_hubble),
        },
        "rotas_hubble": rotas_hubble,
        "registros_olhou_dados_metadados": linhas_exportadas,
    }
    caminho_exportacao = AQUI / "CENSO_R7_MAPA_K09.json"
    escrever_json(caminho_exportacao, exportacao)
    manifesto = {
        "estatuto": "MANIFESTO_DE_SNAPSHOT__SOMENTE_METADADOS",
        "data_exportacao": agora,
        "consulta": consulta,
        "fonte": {
            "path": str(MAPA),
            "sha256_no_momento_da_leitura": sha256(MAPA),
            "observacao": "o hash cobre o Mapa vivo lido; o recorte seq<=2062 preserva o universo examinado pelo revisor",
        },
        "artefato_exportado": {
            "path": str(caminho_exportacao),
            "bytes": caminho_exportacao.stat().st_size,
            "sha256": sha256(caminho_exportacao),
        },
        "totais": exportacao["totais"],
        "nao_contem": ["resultado cientifico", "vetor", "p global", "Z global", "N estrela", "N independente"],
    }
    escrever_json(AQUI / "MANIFESTO_CENSO_R7_MAPA_K09.json", manifesto)
    print("=== censo R7 exportado; somente metadados")
    print(json.dumps(manifesto, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
