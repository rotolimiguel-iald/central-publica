#!/usr/bin/env python3
"""Validação estática dos artefatos K09; nenhum dado observado é lido."""
from __future__ import annotations

import hashlib
import json
import math
from datetime import date
from pathlib import Path

K09 = Path(__file__).resolve().parents[1]
M2 = Path(__file__).resolve().parents[2]
KIMI = Path(__file__).resolve().parents[4]
RESULTS = K09 / "medidas" / "resultados_planejamento_k09.json"
DATA = KIMI / "ERRATA_NEUTRINO_V412_DADOS_K09.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def close(a: float, b: float, tol: float = 1e-12) -> None:
    assert math.isclose(a, b, rel_tol=0.0, abs_tol=tol), (a, b)


def main() -> None:
    payload = json.loads(RESULTS.read_text(encoding="utf-8"))
    data_text = DATA.read_text(encoding="utf-8")
    data = json.loads(data_text)
    assert "kimi-cite://" not in data_text
    assert "prosa de instalação" not in data_text.lower()
    assert len(data["degraus_juno"]) == 2
    assert len(data["ajustes_globais"]) == 2
    assert data["segunda_testemunha"]["id"] == "SK_Gd_reator"
    assert data["pinos"]["sha256_regra_original"].startswith("4bdae22a")
    assert data["pinos"]["sha256_dicionario_portado"].startswith("e248777")
    assert data["pinos"]["sha256_regra_original"] != data["pinos"]["sha256_dicionario_portado"]
    juno = data["degraus_juno"][1]
    first = date.fromisoformat(juno["primeira_apresentacao_publica"]["data"])
    explicit = date.fromisoformat(juno["primeira_confirmacao_explicita_do_valor"]["data"])
    pin = date.fromisoformat(data["pinos"]["data_original"])
    article = date.fromisoformat(juno["artigo"]["data"])
    assert first < pin and explicit < pin and article > pin
    assert juno["janela_dados_fim"] == "2026-05-18"
    nufit = data["ajustes_globais"][0]
    assert nufit["erro_mais_1e-5_eV2"] == 0.094
    assert nufit["erro_menos_1e-5_eV2"] == 0.10
    close(nufit["r_m2"], 3.024242478121835)
    close(nufit["r_delta_m2_21"], 2.993905332817084)
    assert data["ajustes_globais"][0]["primeira_apresentacao_publica"]["data"] is None
    close(data["segunda_testemunha"]["distancia_ao_JUNO_207_sigma"], 3.101148851444389)
    close(data["incremento_59_207_ilustrativo"]["distancia_ao_centro_59_sigma_correta_aninhamento"], 1.2281764972582434)
    for row in payload["desfechos"]:
        for model in ("independente", "cumulativo_C_igual_s2_brinquedo"):
            for truth in row[model]:
                if truth == "covariancia_real":
                    continue
                for metric in ("delta", "m2"):
                    p = row[model][truth][metric]
                    close(p["P_r_le_1"] + p["P_1_lt_r_lt_3"] + p["P_3_le_r_lt_5"] + p["P_r_ge_5"], 1.0, 4e-12)
                    close(p["P_r_lt_3"], p["P_r_le_1"] + p["P_1_lt_r_lt_3"], 4e-12)
    for row in payload["desfechos"]:
        p = row["independente"]["verdade_previsao"]["m2"]
        assert round(100 * p["P_r_le_1"], 2) == 68.27
        assert round(100 * p["P_1_lt_r_lt_3"], 2) == 31.46
        assert round(100 * p["P_r_lt_3"], 2) == 99.73
    solar = next(row for row in payload["matched_conjunta"] if row["id"] == "Solares_sem_KamLAND")
    close(solar["P_matched_conjunta_C0_brinquedo"], 0.07348108476748191)
    perf = payload["desempenho"]
    assert perf["sem_piso_desde_207"]["5sigma"]["data_ideal_cumulativa_apos_corte"] == "2029-08-16"
    assert perf["sem_piso_desde_207"]["D90"]["data_ideal_cumulativa_apos_corte"] == "2031-10-31"
    assert perf["sem_piso_desde_207"]["5sigma"]["data_ideal_incremento_apos_corte"] == "2030-03-11"
    assert perf["sem_piso_desde_207"]["D90"]["data_ideal_incremento_apos_corte"] == "2032-05-25"
    assert perf["tensao_3sigma_sem_piso"]["data_ideal_incremento_apos_corte"] == "2027-10-01"
    assert not perf["piso_ilustrativo_dois_pontos_reais"]["5sigma_alcancavel"]
    assert not perf["piso_ilustrativo_dois_pontos_reais"]["D90_alcancavel"]
    assert len(payload["incremento_1_2_3_anos"]) == 3
    # A R3 editorial permanece idêntica ao snapshot REV2.
    assert sha(KIMI / "ERRATA_M2_K04_R3.md") == sha(M2 / "REV2" / "ERRATA_M2_K04_R3.md")
    assert sha(M2 / "scripts" / "medidas_planejamento.py") == sha(M2 / "REV2" / "scripts" / "medidas_planejamento.py")
    main_text = (KIMI / "M2_DESFECHOS_E_SEGUNDA_TESTEMUNHA_K04.md").read_text(encoding="utf-8")
    pre_text = (KIMI / "PRE_REGISTRO_INCREMENTO_JUNO_RASCUNHO_K09.md").read_text(encoding="utf-8")
    errata_text = (KIMI / "ERRATA_M2_K09.md").read_text(encoding="utf-8")
    for text in (main_text, pre_text, errata_text):
        assert "kimi-cite://" not in text
    for required in ("3,024242", "2,993905", "3,101149", "1,228176", "4bdae22a", "e248777", "16/08/2029", "31/10/2031"):
        assert required in main_text, required
    assert "31/03/2028" not in main_text
    assert "19/09/2031" not in main_text
    for required in ("1 ano = 365,25 d", "2 anos = 730,50 d", "3 anos = 1095,75 d", "11/03/2030", "25/05/2032", "uma única vez"):
        assert required in pre_text, required
    assert "Nenhum teste observado foi executado" in main_text
    report = {
        "status": "OK",
        "teste_observado_executado": False,
        "json_valido": True,
        "sem_kimi_cite": True,
        "cronologia_antes_do_pino": True,
        "benchmarks": {"P_r_le_1": 68.27, "P_1_lt_r_lt_3": 31.46, "P_r_lt_3": 99.73, "MATCHED_solares": 7.348108},
        "NuFIT_tabela": {"r_m2": nufit["r_m2"], "r_delta": nufit["r_delta_m2_21"]},
        "incremento_sigma": data["incremento_59_207_ilustrativo"]["distancia_ao_centro_59_sigma_correta_aninhamento"],
        "REV2_R3_preservada": True,
        "bloqueios_abertos": ["data exata da primeira disponibilização da tabela NuFIT", "covariância inter-liberações e P–S", "independência física de S", "regra/fonte/custódia antes do selo"],
    }
    out = K09 / "medidas" / "validacao_estatica_k09.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
