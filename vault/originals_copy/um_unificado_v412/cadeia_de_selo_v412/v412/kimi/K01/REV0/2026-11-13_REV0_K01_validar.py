#!/usr/bin/env python3
"""K01: contas de DESENHO e validação documental; nunca abre dados observados."""
from __future__ import annotations

import hashlib
import json
import math
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ALPHA_FINE_CODATA_2018 = 0.0072973525693
Z_90_ONE_SIDED = 1.2815515655446004
D_90 = 5.0 + Z_90_ONE_SIDED
ORDER = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_13nov_vamos_comecar_a_construir_a_v412_camada_iald_cientifica_t1_3mais1_gh_tau_teste_cego_5_sigma_kimi_verbatim.txt")
ORDER_SHA256 = "4698446c391f9abae54575b678ab6794aec54492918df988b767292e4cbe47a0"
REQUIRED_CHANNEL_FIELDS = {
    "previsao", "dado", "cegueira", "poder_desenho",
    "independencia", "sete_ressalvas", "consequencia_negativo",
}
REQUIRED_ROUTE_FIELDS = {
    "tipo", "rota_id", "dominio", "titulo", "pergunta", "dados",
    "metodo", "resultado", "veredito", "estatuto", "status",
    "olhou_dados", "defeito", "nao_refazer", "proximo_passo",
    "onde", "artefatos", "refs", "corrige", "nota",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def design() -> dict:
    """Somente álgebra fiducial de desenho; nenhum centro novo é lido."""
    beta = ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)
    m2_pred = beta * math.sin(math.pi / 4.0) * 1000.0  # meV; E0 = 1 eV DECLARADO
    m2_planejamento = 8.677557259966656  # meV; centro público já conhecido, só planning
    gap_relativo_dm2 = 2.0 * (1.0 - m2_pred / m2_planejamento)
    precisao_5 = gap_relativo_dm2 / 5.0
    precisao_90 = gap_relativo_dm2 / D_90
    d_juno_conservador = gap_relativo_dm2 / 0.005
    d_juno_publicado = gap_relativo_dm2 / 0.003
    m2_juno_only_planning = 8.660254037844387  # meV; entrada direta JUNO já conhecida, só planning
    gap_relativo_juno_only = 2.0 * (1.0 - m2_pred / m2_juno_only_planning)
    k_menos_1 = 0.0838071748529643  # lido do core; não é H0 nem razão observada
    delta_neff = 0.11946607525373273
    delta_sum_ev = 0.000199  # 0,199 meV, separação NH mínima registrada no core
    coma_delta_mpc = abs(110.8497713445941 - 101.90278629474811)
    gamma_th = 5.22636371728147e-14
    inicio_juno = date(2025, 8, 26)
    seis_anos = date(inicio_juno.year + 6, inicio_juno.month, inicio_juno.day)
    return {
        "estatuto": "[DERIVED] apenas desenho; não é Z, H0, veredito nem resultado observado",
        "beta_runtime": beta,
        "D90": D_90,
        "m2": {
            "pred_meV": m2_pred,
            "precisao_dm2_para_5sigma": precisao_5,
            "precisao_dm2_para_D90": precisao_90,
            "D_se_precisao_dm2_0p5pct": d_juno_conservador,
            "D_se_precisao_dm2_0p3pct": d_juno_publicado,
            "juno_only_planning": {
                "precisao_dm2_para_5sigma": gap_relativo_juno_only / 5.0,
                "precisao_dm2_para_D90": gap_relativo_juno_only / D_90,
                "D_se_precisao_dm2_0p5pct": gap_relativo_juno_only / 0.005,
                "D_se_precisao_dm2_0p3pct": gap_relativo_juno_only / 0.003,
            },
            "exposicao_nominal_seis_anos_desde_2025_08_26": seis_anos.isoformat(),
            "data_de_publicacao": "OPEN: exposição não é promessa de liberação",
        },
        "hubble": {
            "K_menos_1_desenho": k_menos_1,
            "sigma_relativa_total_para_D90": k_menos_1 / D_90,
        },
        "neff": {
            "D_SO_0p045": delta_neff / 0.045,
            "D_S4_historico_0p03": delta_neff / 0.03,
            "sigma_para_5sigma": delta_neff / 5.0,
            "sigma_para_D90": delta_neff / D_90,
        },
        "sum_mnu": {
            "D_SO_DESI_0p03eV": delta_sum_ev / 0.03,
            "D_SO_DESI_LiteBIRD_0p015eV": delta_sum_ev / 0.015,
            "sigma_para_D90_eV": delta_sum_ev / D_90,
        },
        "ringdown": {
            "D10_melhor_planejamento": 3.9346337577944936,
            "D14_teto_sem_sistematica": 4.63741267778178,
            "fator_informacao_D10_para_D90": (D_90 / 3.9346337577944936) ** 2,
            "fator_informacao_D14_para_D90": (D_90 / 4.63741267778178) ** 2,
        },
        "coma": {
            "delta_pred_controle_mpc": coma_delta_mpc,
            "sigma_total_para_D90_mpc": coma_delta_mpc / D_90,
        },
        "th229": {
            "sigma_excess_para_D90_por_s": gamma_th / D_90,
            "observacao": "não se transforma FWHM/cota 90% em σ; poder estatístico segue OPEN",
        },
        "sr87": {
            "sigma_excess_para_D90_por_s": 2.3588364708421127e-15 / D_90,
        },
        "decoerencia_juno_n_menos2": {
            "sigma_excess_para_D90_por_s": 1.17e-37 / D_90,
            "observacao": "cota 90% não é σ; apenas requisito fiducial",
        },
        "nmc_shapiro_modelo_simples": {
            "D_N25_sigma_10ms": 0.05 * math.sqrt(25) / 0.01,
            "observacao": "ilustração; o core registra cerca de 21 sem expor todos os fatores",
        },
    }


def _summary_line_count(text: str) -> int:
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines) if line.strip() == "## RESUMO"), None)
    if start is None:
        raise AssertionError("ENTREGA_K01.md sem seção ## RESUMO")
    count = 0
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        if line.strip():
            count += 1
    return count


def validate() -> dict:
    canais_path = ROOT / "CANAIS_K01.json"
    registro_path = ROOT / "REGISTRO_MAPA_K01.json"
    canais_doc = json.loads(canais_path.read_text(encoding="utf-8"))
    registro = json.loads(registro_path.read_text(encoding="utf-8"))
    assert isinstance(canais_doc, dict)
    assert set(canais_doc["ressalvas_glossario"]) == {f"R{i}" for i in range(1, 8)}
    canais = canais_doc["canais"]
    assert isinstance(canais, list) and canais
    ids = [c["id"] for c in canais]
    assert len(ids) == len(set(ids)), "id de canal duplicado"
    for canal in canais:
        assert REQUIRED_CHANNEL_FIELDS <= set(canal), f"campos ausentes em {canal.get('id')}"
        assert set(canal["sete_ressalvas"]) == {f"R{i}" for i in range(1, 8)}, canal["id"]
        assert canal["classificacao"] in {
            "EXISTE E ESTÁ LIGADO", "EXISTE NA BANCADA MAS NÃO ESTÁ LIGADO",
            "SABIDO POR REFERÊNCIA", "AUSENTE",
        }, canal["id"]
    assert REQUIRED_ROUTE_FIELDS <= set(registro)
    assert registro["tipo"] == "ROTA"
    assert registro["olhou_dados"] is False
    assert registro["status"] == "PROPOSTA"
    assert registro["estatuto"] == "DECLARADO"
    assert registro["corrige"] in (None, "")
    entrega = (ROOT / "ENTREGA_K01.md").read_text(encoding="utf-8")
    summary_lines = _summary_line_count(entrega)
    assert summary_lines <= 15, f"resumo tem {summary_lines} linhas"
    termo = "descoberta autoevidente em dados públicos, carente de creditação acadêmica"
    assert termo in entrega
    assert "NOT_FALSIFIED" in entrega and "CONFIRMED" in entrega
    order_bytes = ORDER.read_bytes()
    assert len(order_bytes) == 886
    assert hashlib.sha256(order_bytes).hexdigest() == ORDER_SHA256
    names = [
        "ENTREGA_K01.md", "CANAIS_K01.json", "PRE_REGISTRO_CEGO_RASCUNHO_K01.md",
        "REGISTRO_MAPA_K01.json", "PERGUNTA_K01.md", "K01_validar.py",
    ]
    files = []
    for name in names:
        path = ROOT / name
        assert path.is_file(), f"arquivo ausente: {name}"
        files.append({"arquivo": name, "bytes": path.stat().st_size, "sha256": sha256(path)})
    return {
        "contrato": "VALIDACAO_DOCUMENTAL_K01_V1",
        "json_validos": ["CANAIS_K01.json", "REGISTRO_MAPA_K01.json"],
        "n_canais": len(canais),
        "sete_campos_por_canal": True,
        "sete_ressalvas_por_canal": True,
        "registro_no_formato_modelo": True,
        "registro_foi_registrado": False,
        "resumo_linhas_nao_vazias": summary_lines,
        "resumo_limite": 15,
        "ordem_original": {"bytes": len(order_bytes), "sha256": ORDER_SHA256},
        "arquivos": files,
        "escopo": "somente documental; nenhum teste empírico executado; nenhum vetor observado lido",
    }


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "desenho"
    if mode == "desenho":
        print(json.dumps(design(), ensure_ascii=False, indent=2))
        return
    if mode == "validar":
        result = validate()
        out = ROOT / "VALIDACAO_K01.json"
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    raise SystemExit("uso: python K01_validar.py [desenho|validar]")


if __name__ == "__main__":
    main()
