#!/usr/bin/env python3
"""Auditoria final independente e fecho de hashes K09/REV2.

Lê somente os artefatos de planejamento e os textos produzidos. Não consulta
fontes novas, não abre vetores de dados e não executa teste observado.
"""
from __future__ import annotations

import hashlib
import json
import math
from datetime import date, timedelta
from pathlib import Path

K09 = Path(__file__).resolve().parents[1]
M2 = Path(__file__).resolve().parents[2]
KIMI = Path(__file__).resolve().parents[4]
MEDIDAS = K09 / "medidas"
REV2 = M2 / "REV2"
REV3 = M2 / "REV3"
DATA = KIMI / "ERRATA_NEUTRINO_V412_DADOS_K09.json"
RESULTS = MEDIDAS / "resultados_planejamento_k09.json"
OUT_AUDIT = MEDIDAS / "auditoria_final_independente_k09.json"
MANIFEST_K09 = MEDIDAS / "MANIFESTO_K09.json"
HASHES_K09 = MEDIDAS / "hashes_K09.txt"
MANIFEST_REV2 = REV2 / "medidas" / "MANIFESTO_REV2.json"
HASHES_REV2 = REV2 / "medidas" / "hashes_REV2.txt"
MANIFEST_REV3 = REV3 / "K09" / "medidas" / "MANIFESTO_REV3.json"
HASHES_REV3 = REV3 / "K09" / "medidas" / "hashes_REV3.txt"
FECHO = MEDIDAS / "FECHO_HASHES_K09.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def close(actual: float, expected: float, tol: float = 1e-10) -> None:
    assert math.isclose(actual, expected, rel_tol=0.0, abs_tol=tol), (actual, expected)


def cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def main() -> None:
    # Recálculo independente, sem importar o script de planejamento.
    alpha = 0.0072973525693
    beta = alpha * math.sqrt(math.e)
    m2 = beta * math.sin(math.pi / 4.0) * 1000.0
    pred = (m2 / 1000.0) ** 2 / 1e-5
    close(m2, 8.507414099900329, 1e-12)
    close(pred, 7.2376094667182915, 1e-12)

    def r_m2(mu: float, sigma: float) -> float:
        mass = math.sqrt(10.0 * mu)
        return abs(mass - m2) / (0.5 * (sigma / mu) * mass)

    def r_delta(mu: float, sigma: float) -> float:
        return abs(mu - pred) / sigma

    expected = {
        "JUNO_59_1": (r_m2(7.50, 0.12), 2.206054482873198),
        "JUNO_207_2": (r_m2(7.388, 0.078), 1.9379969609289271),
        "NuFIT_tabela_m2": (r_m2(7.537, 0.10), 3.024242478121835),
        "NuFIT_tabela_delta": (r_delta(7.537, 0.10), 2.993905332817084),
        "NuFIT_artigo_m2": (r_m2(7.530, 0.097), 3.044179410035495),
        "NuFIT_artigo_delta": (r_delta(7.530, 0.097), 3.014335394656791),
        "NuFIT_core_simetrico_m2": (r_m2(7.530, 0.10), 2.9528540277344297),
        "SK_Gd_m2": (r_m2(9.08, 0.54), 3.605064022654631),
        "SK_Gd_delta": (r_delta(9.08, 0.54), 3.4118343208920527),
        "SK_Gd_vs_JUNO": ((9.08 - 7.388) / math.sqrt(0.54**2 + 0.078**2), 3.101148851444389),
    }
    for name, (actual, target) in expected.items():
        close(actual, target, 2e-12), name

    w1, w2 = 1.0 / 0.12**2, 1.0 / 0.078**2
    mu_inc = (w2 * 7.388 - w1 * 7.50) / (w2 - w1)
    sd_inc = 1.0 / math.sqrt(w2 - w1)
    close(mu_inc, 7.306060606060605, 1e-12)
    close(sd_inc, 0.10264046441372396, 1e-12)
    z_inc = abs(mu_inc - 7.50) / math.hypot(sd_inc, 0.12)
    close(z_inc, 1.2281764972582434, 1e-12)
    close(abs(7.50 - 7.388) / math.sqrt(0.12**2 - 0.078**2), z_inc, 1e-12)

    p_le1 = 2.0 * cdf(1.0) - 1.0
    p_1_3 = 2.0 * (cdf(3.0) - cdf(1.0))
    p_lt3 = 2.0 * cdf(3.0) - 1.0
    close(p_le1, 0.6826894921370856, 1e-15)
    close(p_1_3, 0.31461071179965416, 1e-15)
    close(p_lt3, 0.9973002039367398, 1e-15)

    # MATCHED Solares: intervalo inferior L..U e cauda superior H, via independente.
    def band_m2_local(mean: float, sd: float, sigma_future: float, t: float) -> float:
        disc = m2 * m2 - 20.0 * t * sigma_future
        lower = 0.0
        if disc >= 0.0:
            root = math.sqrt(disc)
            low = (m2 - root) / 2.0
            high_lower = (m2 + root) / 2.0
            lower = cdf((high_lower**2 / 10.0 - mean) / sd) - cdf((low**2 / 10.0 - mean) / sd)
        high = (m2 + math.sqrt(m2 * m2 + 20.0 * t * sigma_future)) / 2.0
        return lower + 1.0 - cdf((high**2 / 10.0 - mean) / sd)

    payload = json.loads(RESULTS.read_text(encoding="utf-8"))
    solar_payload = next(row for row in payload["matched_conjunta"] if row["id"] == "Solares_sem_KamLAND")
    p_primary = 1.0 - band_m2_local(7.388, 0.078, 0.078, 1.0)
    p_solar = 1.0 - band_m2_local(6.10, 0.95, 0.95, 1.0)
    close(p_primary, solar_payload["P_rP_le_1"], 2e-12)
    close(p_solar, solar_payload["P_rS_le_1"], 2e-12)
    close(p_primary * p_solar, solar_payload["P_matched_conjunta_C0_brinquedo"], 2e-12)

    # Datas recalculadas dos agregados, sem reutilizar strings do documento.
    cutoff = date(2026, 5, 18)
    delta = 7.388 - pred
    d90 = 5.0 + 1.2815515655446004
    info = 207.2 * 0.078**2
    t5 = info / (delta / 5.0) ** 2
    td90 = info / (delta / d90) ** 2
    t3 = info / (delta / 3.0) ** 2
    mass_now = math.sqrt(10.0 * 7.388)
    mass_gap = abs(mass_now - m2)
    t5_m2 = info / (mass_now * mass_gap / (5.0 * 5.0)) ** 2
    td90_m2 = info / (mass_now * mass_gap / (5.0 * d90)) ** 2
    t3_m2 = info / (mass_now * mass_gap / (5.0 * 3.0)) ** 2
    assert (cutoff + timedelta(days=t5 - 207.2)).isoformat() == "2029-08-16"
    assert (cutoff + timedelta(days=td90 - 207.2)).isoformat() == "2031-10-31"
    assert (cutoff + timedelta(days=t5)).isoformat() == "2030-03-11"
    assert (cutoff + timedelta(days=td90)).isoformat() == "2032-05-25"
    assert (cutoff + timedelta(days=t3)).isoformat() == "2027-10-01"
    assert (cutoff + timedelta(days=t5_m2 - 207.2)).isoformat() == "2029-08-01"
    assert (cutoff + timedelta(days=td90_m2 - 207.2)).isoformat() == "2031-10-08"
    assert (cutoff + timedelta(days=t5_m2)).isoformat() == "2030-02-25"
    assert (cutoff + timedelta(days=td90_m2)).isoformat() == "2032-05-02"
    assert (cutoff + timedelta(days=t3_m2)).isoformat() == "2027-09-26"
    s0 = math.sqrt(0.078**2 - ((0.078**2 - 0.12**2) / (1.0 / 207.2 - 1.0 / 59.1)) / 207.2)
    close(s0, 0.05258765230433696, 1e-12)
    sk_extra = 411.52 * (0.54 / (2.0 * 9.08 * abs(math.sqrt(90.8) - m2) / (5.0 * math.sqrt(90.8)))) ** 2 - 411.52
    close(sk_extra, 380.07855357458413, 1e-9)

    # JSON, cronologia, identificadores e ausência de instalação/marcadores.
    text = DATA.read_text(encoding="utf-8")
    data = json.loads(text)
    lowered = text.lower()
    for forbidden in ("kimi-cite://", "prosa de instalação", "instruções de instalação", "installation instructions", "install now", "instalar agora"):
        assert forbidden not in lowered, forbidden
    assert len(data["degraus_juno"]) == 2
    assert len(data["ajustes_globais"]) == 2
    juno = data["degraus_juno"][1]
    first = date.fromisoformat(juno["primeira_apresentacao_publica"]["data"])
    explicit = date.fromisoformat(juno["primeira_confirmacao_explicita_do_valor"]["data"])
    pin = date.fromisoformat(data["pinos"]["data_do_congelamento"])
    article = date.fromisoformat(juno["artigo"]["data"])
    assert first < pin and explicit < pin and article > pin
    assert juno["janela_dados_fim"] == "2026-05-18"
    assert juno["primeira_apresentacao_publica"]["identificador"] == "indico.global/event/15740/contributions/155563"
    assert juno["primeira_apresentacao_publica"]["estatuto"] == "DECLARADO_sem_resposta_crua_guardada"
    assert juno["primeira_confirmacao_explicita_do_valor"]["identificador"] == "indico.ihep.ac.cn/event/28557/contributions/223278"
    assert juno["noticia_secundaria"]["data"] == "2026-07-22"
    assert "sha256_regra_original" not in data["pinos"]
    assert data["pinos"]["frozen_hash_objeto_congelado"].startswith("4bdae22a")
    assert data["pinos"]["sha256_arquivo_regra_py"].startswith("2564d7c9")
    assert data["pinos"]["sha256_arquivo_resultado_json"].startswith("6f0963a5")
    assert data["pinos"]["sha256_dicionario_portado"].startswith("e248777")
    assert data["pinos"]["frozen_hash_objeto_congelado"] != data["pinos"]["sha256_dicionario_portado"]
    prev = data["previsao_publicada"]
    assert prev["valor_8_51_no_acervo"]["data"] == "2026-01-22"
    assert prev["publicacao_zenodo"]["publication_date"] == "2026-02-17"
    assert prev["publicacao_zenodo"]["created"].startswith("2026-02-20")
    assert data["degraus_juno"][0]["posicao_relativa_a_previsao_publicada"] == "anterior_ao_valor_publicado"
    assert data["degraus_juno"][1]["posicao_relativa_a_previsao_publicada"] == "posterior_ao_valor_publicado"
    nufit = data["ajustes_globais"][0]
    assert nufit["erro_mais_1e-5_eV2"] == 0.094 and nufit["erro_menos_1e-5_eV2"] == 0.10
    close(nufit["r_m2"], expected["NuFIT_tabela_m2"][1], 1e-12)
    close(nufit["r_delta_m2_21"], expected["NuFIT_tabela_delta"][1], 1e-12)
    assert data["ajustes_globais"][0]["primeira_apresentacao_publica"]["data"] is None
    close(data["incremento_59_207_ilustrativo"]["distancia_ao_centro_59_sigma_correta_aninhamento"], z_inc, 1e-12)
    close(data["segunda_testemunha"]["distancia_ao_JUNO_207_sigma"], expected["SK_Gd_vs_JUNO"][1], 1e-12)

    # Preservação real de REV2 e da errata R3.
    r3_root = KIMI / "ERRATA_M2_K04_R3.md"
    r3_rev2 = REV2 / "ERRATA_M2_K04_R3.md"
    assert r3_root.exists() and r3_rev2.exists()
    assert sha(r3_root) == sha(r3_rev2)
    assert sha(M2 / "scripts" / "medidas_planejamento.py") == sha(REV2 / "scripts" / "medidas_planejamento.py")
    assert sha(M2 / "medidas" / "resultados_planejamento.json") == sha(REV2 / "medidas" / "resultados_planejamento.json")
    rev2_main = (REV2 / "M2_DESFECHOS_E_SEGUNDA_TESTEMUNHA_K04.md").read_text(encoding="utf-8")
    assert "— R3" in rev2_main.splitlines()[0]
    rev3_main = (REV3 / "M2_DESFECHOS_E_SEGUNDA_TESTEMUNHA_K04.md").read_text(encoding="utf-8")
    assert "— K09" in rev3_main.splitlines()[0]
    assert (REV3 / "K09" / "scripts" / "medidas_planejamento_k09.py").exists()
    assert (REV3 / "K09" / "medidas" / "resultados_planejamento_k09.json").exists()
    current_main = (KIMI / "M2_DESFECHOS_E_SEGUNDA_TESTEMUNHA_K04.md").read_text(encoding="utf-8")
    assert "— K09" in current_main.splitlines()[0]
    assert sha(REV2 / "M2_DESFECHOS_E_SEGUNDA_TESTEMUNHA_K04.md") != sha(KIMI / "M2_DESFECHOS_E_SEGUNDA_TESTEMUNHA_K04.md")
    assert sha(REV3 / "M2_DESFECHOS_E_SEGUNDA_TESTEMUNHA_K04.md") != sha(KIMI / "M2_DESFECHOS_E_SEGUNDA_TESTEMUNHA_K04.md")

    # Resultados publicados nos arquivos de planejamento.
    payload = json.loads(RESULTS.read_text(encoding="utf-8"))
    for row in payload["desfechos"]:
        p = row["independente"]["verdade_previsao"]["m2"]
        assert round(100 * p["P_r_le_1"], 2) == 68.27
        assert round(100 * p["P_1_lt_r_lt_3"], 2) == 31.46
        assert round(100 * p["P_r_lt_3"], 2) == 99.73
        for model in ("independente", "cumulativo_C_igual_s2_brinquedo"):
            for truth in row[model]:
                if truth == "covariancia_real":
                    continue
                for metric in ("delta", "m2"):
                    q = row[model][truth][metric]
                    close(q["P_r_le_1"] + q["P_1_lt_r_lt_3"] + q["P_3_le_r_lt_5"] + q["P_r_ge_5"], 1.0, 4e-12)
                    close(q["P_r_lt_3"], q["P_r_le_1"] + q["P_1_lt_r_lt_3"], 4e-12)
    solar = next(row for row in payload["matched_conjunta"] if row["id"] == "Solares_sem_KamLAND")
    close(solar["P_matched_conjunta_C0_brinquedo"], p_primary * p_solar, 2e-12)
    assert len(payload["incremento_1_2_3_anos"]) == 3
    calendar_rows = {(row["alvo"], row["metrica"]): row for row in payload["desempenho"]["sem_piso_por_metrica"]}
    assert calendar_rows[("5sigma", "m2")]["data_ideal_cumulativa_apos_corte"] == "2029-08-01"
    assert calendar_rows[("5sigma", "m2")]["data_ideal_incremento_apos_corte"] == "2030-02-25"
    assert calendar_rows[("D90", "m2")]["data_ideal_cumulativa_apos_corte"] == "2031-10-08"
    assert calendar_rows[("D90", "m2")]["data_ideal_incremento_apos_corte"] == "2032-05-02"
    assert calendar_rows[("r_3", "m2")]["data_ideal_incremento_apos_corte"] == "2027-09-26"
    assert (MEDIDAS / "calendario_metricas_duplas_k09.md").exists()

    audit = {
        "veredito": "APROVADO_NA_CONFERENCIA_FINAL",
        "teste_observado_executado": False,
        "novas_buscas": False,
        "json_valido_e_datas_coerentes": True,
        "json_sem_marcadores_e_sem_prosa_de_instalacao": True,
        "recalculo_independente": {
            "m2_pred_meV": m2,
            "delta_pred": pred,
            "NuFIT_tabela_r_m2": expected["NuFIT_tabela_m2"][0],
            "NuFIT_tabela_r_delta": expected["NuFIT_tabela_delta"][0],
            "NuFIT_artigo_r_m2": expected["NuFIT_artigo_m2"][0],
            "NuFIT_artigo_r_delta": expected["NuFIT_artigo_delta"][0],
            "NuFIT_core_simetrico_r_m2": expected["NuFIT_core_simetrico_m2"][0],
            "SK_Gd_r_m2": expected["SK_Gd_m2"][0],
            "SK_Gd_distancia_JUNO_sigma": expected["SK_Gd_vs_JUNO"][0],
            "incremento_centro": mu_inc,
            "incremento_sigma": sd_inc,
            "incremento_distancia_59_sigma": z_inc,
            "benchmark_P_r_le_1_pct": 100 * p_le1,
            "benchmark_P_1_lt_r_lt_3_pct": 100 * p_1_3,
            "benchmark_P_r_lt_3_pct": 100 * p_lt3,
            "MATCHED_solares_pct": 100 * p_primary * p_solar,
            "piso_dois_pontos_s0": s0,
            "SK_Gd_dias_adicionais_cenario": sk_extra,
        },
        "calendario_metricas_duplas": {
            "m2_5sigma_cumulativo": "2029-08-01",
            "m2_5sigma_incremento": "2030-02-25",
            "m2_D90_cumulativo": "2031-10-08",
            "m2_D90_incremento": "2032-05-02",
            "m2_r3_incremento": "2027-09-26",
        },
        "REV2_e_ERRATA_R3_preservados": True,
        "REV3_K09_anterior_ao_adendo_preservado": True,
        "bloqueios": [
            "resposta crua de 22/06/2026 não guardada",
            "data exata da primeira disponibilização pública da tabela NuFIT",
            "covariância inter-liberações e P–S",
            "independência física e persistência da anomalia SK-Gd",
            "decomposição estatística/sistemática do erro futuro e piso real",
            "escolha de regra, fonte, escada e custódia antes do selo",
        ],
    }
    OUT_AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Manifesto dos entregáveis K09; caches e arquivos de fecho ficam fora do payload.
    root_files = [
        KIMI / "M2_DESFECHOS_E_SEGUNDA_TESTEMUNHA_K04.md",
        KIMI / "ERRATA_M2_K09.md",
        KIMI / "ERRATA_M2_K09_15nov.md",
        KIMI / "PRE_REGISTRO_INCREMENTO_JUNO_RASCUNHO_K09.md",
        DATA,
    ]
    k09_files = sorted(
        p for p in K09.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts
        and p.suffix in {".py", ".json", ".md", ".txt"}
        and p not in {MANIFEST_K09, HASHES_K09, FECHO}
    )
    entries = []
    for path in root_files + k09_files:
        entries.append({
            "arquivo": path.relative_to(KIMI).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha(path),
        })
    entries.sort(key=lambda row: row["arquivo"])
    MANIFEST_K09.write_text(json.dumps({
        "schema": "k04.m2.k09.manifesto.v1",
        "teste_observado_executado": False,
        "arquivos": entries,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    hash_entries = entries + [{
        "arquivo": MANIFEST_K09.relative_to(KIMI).as_posix(),
        "bytes": MANIFEST_K09.stat().st_size,
        "sha256": sha(MANIFEST_K09),
    }]
    hash_entries.sort(key=lambda row: row["arquivo"])
    HASHES_K09.write_text("".join(f"{row['sha256']}  {row['arquivo']}\n" for row in hash_entries), encoding="utf-8")

    # Manifesto integral da preservação REV2, sem incluir os próprios arquivos de fecho.
    rev2_files = sorted(
        p for p in REV2.rglob("*")
        if p.is_file() and p not in {MANIFEST_REV2, HASHES_REV2}
    )
    rev2_entries = []
    for path in rev2_files:
        rev2_entries.append({
            "arquivo": path.relative_to(M2).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha(path),
        })
    MANIFEST_REV2.write_text(json.dumps({
        "schema": "k04.m2.rev2.preservacao.manifesto.v1",
        "arquivos": rev2_entries,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rev2_hash_entries = rev2_entries + [{
        "arquivo": MANIFEST_REV2.relative_to(M2).as_posix(),
        "bytes": MANIFEST_REV2.stat().st_size,
        "sha256": sha(MANIFEST_REV2),
    }]
    rev2_hash_entries.sort(key=lambda row: row["arquivo"])
    HASHES_REV2.write_text("".join(f"{row['sha256']}  {row['arquivo']}\n" for row in rev2_hash_entries), encoding="utf-8")

    # Manifesto integral da preservação REV3 (estado K09 anterior ao adendo).
    rev3_files = sorted(
        p for p in REV3.rglob("*")
        if p.is_file() and p not in {MANIFEST_REV3, HASHES_REV3}
    )
    rev3_entries = []
    for path in rev3_files:
        rev3_entries.append({
            "arquivo": path.relative_to(M2).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha(path),
        })
    MANIFEST_REV3.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_REV3.write_text(json.dumps({
        "schema": "k04.m2.rev3.preservacao.manifesto.v1",
        "arquivos": rev3_entries,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rev3_hash_entries = rev3_entries + [{
        "arquivo": MANIFEST_REV3.relative_to(M2).as_posix(),
        "bytes": MANIFEST_REV3.stat().st_size,
        "sha256": sha(MANIFEST_REV3),
    }]
    rev3_hash_entries.sort(key=lambda row: row["arquivo"])
    HASHES_REV3.write_text("".join(f"{row['sha256']}  {row['arquivo']}\n" for row in rev3_hash_entries), encoding="utf-8")

    # Verificação pós-escrita de todos os pinos listados.
    for row in entries:
        path = KIMI / row["arquivo"]
        assert path.stat().st_size == row["bytes"]
        assert sha(path) == row["sha256"]
    for row in rev2_entries:
        path = M2 / row["arquivo"]
        assert path.stat().st_size == row["bytes"]
        assert sha(path) == row["sha256"]
    for row in rev3_entries:
        path = M2 / row["arquivo"]
        assert path.stat().st_size == row["bytes"]
        assert sha(path) == row["sha256"]
    close_report = {
        "veredito": audit["veredito"],
        "auditoria_final": {
            "arquivo": OUT_AUDIT.relative_to(KIMI).as_posix(),
            "sha256": sha(OUT_AUDIT),
        },
        "manifesto_K09": {
            "arquivo": MANIFEST_K09.relative_to(KIMI).as_posix(),
            "sha256": sha(MANIFEST_K09),
            "arquivos_no_payload": len(entries),
        },
        "hashes_K09": {
            "arquivo": HASHES_K09.relative_to(KIMI).as_posix(),
            "sha256": sha(HASHES_K09),
        },
        "manifesto_REV2": {
            "arquivo": MANIFEST_REV2.relative_to(KIMI).as_posix(),
            "sha256": sha(MANIFEST_REV2),
            "arquivos_preservados": len(rev2_entries),
        },
        "hashes_REV2": {
            "arquivo": HASHES_REV2.relative_to(KIMI).as_posix(),
            "sha256": sha(HASHES_REV2),
        },
        "manifesto_REV3": {
            "arquivo": MANIFEST_REV3.relative_to(KIMI).as_posix(),
            "sha256": sha(MANIFEST_REV3),
            "arquivos_preservados": len(rev3_entries),
        },
        "hashes_REV3": {
            "arquivo": HASHES_REV3.relative_to(KIMI).as_posix(),
            "sha256": sha(HASHES_REV3),
        },
        "verificacao_pos_escrita": True,
        "bloqueios": audit["bloqueios"],
    }
    FECHO.write_text(json.dumps(close_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(close_report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
