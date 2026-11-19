#!/usr/bin/env python3
"""K01: contas de DESENHO e validação documental; nunca abre dados observados."""
from __future__ import annotations

import hashlib
import json
import math
import subprocess
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
    """Somente álgebra fiducial de desenho em Δm²₂₁; nenhuma estatística observada."""
    beta = ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)
    m2_pred = beta * math.sin(math.pi / 4.0) * 1000.0  # meV; E0 = 1 eV DECLARADO
    dm2_pred = (m2_pred * 1.0e-3) ** 2  # eV²; conversão exata com m1≈0

    # Determinação pública elegível mais recente: arXiv:2609.37895v1, 207,2 dias.
    dm2_latest = 7.388e-5
    sigma_latest = 0.078e-5
    gap_latest = 1.0 - dm2_pred / dm2_latest

    # Históricos, mantidos somente para auditoria da correção e nunca como planning atual.
    dm2_59d = 7.50e-5
    sigma_59d = 0.12e-5
    gap_59d = 1.0 - dm2_pred / dm2_59d
    dm2_global_hist = (8.677557259966656 * 1.0e-3) ** 2
    gap_global_hist = 1.0 - dm2_pred / dm2_global_hist

    k_menos_1 = 0.0838071748529643  # lido do core; não é H0 nem razão observada
    delta_neff = 0.11946607525373273
    delta_sum_ev = 0.000199  # 0,199 meV, separação NH mínima registrada no core
    coma_delta_mpc = abs(110.8497713445941 - 101.90278629474811)
    gamma_th = 5.22636371728147e-14
    inicio_juno = date(2025, 8, 26)
    seis_anos = date(inicio_juno.year + 6, inicio_juno.month, inicio_juno.day)
    return {
        "estatuto": "[DERIVED] apenas desenho em Δm²₂₁; não é Z, H0, veredito nem resultado observado",
        "beta_runtime": beta,
        "D90": D_90,
        "m2": {
            "pred_meV": m2_pred,
            "dm2_pred_eV2": dm2_pred,
            "planning_atual": {
                "fonte": "JUNO Collaboration, arXiv:2609.37895v1, 2026-09-29, 207,2 dias",
                "dm2_planning_eV2": dm2_latest,
                "sigma_total_eV2": sigma_latest,
                "m2_planning_meV_conversao_exata": math.sqrt(dm2_latest) * 1000.0,
                "r_sigma_sobre_planning": sigma_latest / dm2_latest,
                "D_com_sigma_publicado": abs(dm2_latest - dm2_pred) / sigma_latest,
                "precisao_relativa_para_5sigma": gap_latest / 5.0,
                "precisao_relativa_para_D90": gap_latest / D_90,
                "D_se_precisao_relativa_0p5pct": gap_latest / 0.005,
                "D_se_precisao_relativa_0p3pct": gap_latest / 0.003,
                "poder_conjoint_duas_testemunhas": "OPEN: não calculado; D_P e D_S ficam separados",
                "nota": "D usa Δm² integralmente; qualquer σ_m₂ por propagação é apenas aproximação de primeiro order",
            },
            "historico_59d_nao_planning_atual": {
                "fonte": "JUNO Collaboration, arXiv:2511.14593v1, 2025-11-18, 59,1 dias",
                "dm2_eV2": dm2_59d,
                "sigma_eV2": sigma_59d,
                "D_se_precisao_relativa_0p5pct": gap_59d / 0.005,
                "precisao_relativa_para_D90": gap_59d / D_90,
            },
            "historico_global_nao_planning_atual": {
                "dm2_eV2": dm2_global_hist,
                "D_se_precisao_relativa_0p5pct": gap_global_hist / 0.005,
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


def _under_armed(d_p: float | None, d_s: float | None = None) -> str:
    valores = [d for d in (d_p, d_s) if d is not None]
    if not valores:
        return "AWAITING_SOURCE"
    return "UNDER" if max(valores) < 5.0 else "ARMED"


def veredito_sintetico(r_p: float | None, s_state: str, r_s: float | None = None,
                       d_p: float | None = 6.0, d_s: float | None = 6.0) -> str:
    """Implementa somente a tabela-verdade R2, com valores sintéticos."""
    if r_p is None:
        return "AWAITING_SOURCE_P"
    if not math.isfinite(r_p) or r_p < 0:
        return "INCONCLUSIVE_P"
    if s_state == "INVALID":
        return "INCONCLUSIVE_S"
    if s_state != "ABSENT" and (r_s is None or not math.isfinite(r_s) or r_s < 0):
        return "INCONCLUSIVE_S"

    if r_p >= 5:
        if s_state == "ABSENT":
            return "SINGLE_P"
        if s_state == "NONINDEPENDENT":
            return "BOTH_NONINDEPENDENT" if r_s >= 5 else "SINGLE_P"
        if s_state == "INDEPENDENT":
            return "FALSIFIED" if r_s >= 5 else "SINGLE_P"
        raise ValueError(s_state)

    if s_state == "ABSENT":
        return "TENSION_P" if r_p >= 3 else _under_armed(d_p)
    if s_state == "NONINDEPENDENT":
        if r_s >= 5:
            return "SINGLE_S"
        return "TENSION_P" if r_p >= 3 else _under_armed(d_p)
    if s_state == "INDEPENDENT":
        if r_s >= 5:
            return "SINGLE_S"
        if r_p >= 3 and r_s >= 3:
            return "BOTH"
        if r_p >= 3:
            return "TENSION_P"
        if r_s >= 3:
            return "TENSION_S"
        if r_p <= 1 and r_s <= 1:
            return "MATCHED"
        return _under_armed(d_p, d_s)
    raise ValueError(s_state)


def synthetic_cases() -> list[dict]:
    """Casos R2 executáveis; nenhum valor vem de dados observados."""
    definicoes = [
        ("P≥5, S ausente", 5.0, "ABSENT", None, "SINGLE_P"),
        ("P≥5, S não independente <5", 5.0, "NONINDEPENDENT", 4.0, "SINGLE_P"),
        ("P≥5, S independente <5", 5.0, "INDEPENDENT", 4.9, "SINGLE_P"),
        ("P e S independentes ≥5", 5.0, "INDEPENDENT", 5.0, "FALSIFIED"),
        ("P≥5 e S≥5 não independente", 5.0, "NONINDEPENDENT", 5.0, "BOTH_NONINDEPENDENT"),
        ("3≤P<5 e S independente ≥5", 3.5, "INDEPENDENT", 5.0, "SINGLE_S"),
        ("3≤P<5 e S não independente ≥5", 3.5, "NONINDEPENDENT", 5.0, "SINGLE_S"),
        ("ambos independentes em [3,5)", 3.5, "INDEPENDENT", 4.5, "BOTH"),
        ("1<P<3 e S independente ≥5", 2.0, "INDEPENDENT", 5.0, "SINGLE_S"),
        ("1<P<3 e S não independente ≥5", 2.0, "NONINDEPENDENT", 5.0, "SINGLE_S"),
        ("P≤1 e S independente ≥5", 0.5, "INDEPENDENT", 5.0, "SINGLE_S"),
        ("P≤1 e S não independente ≥5", 0.5, "NONINDEPENDENT", 5.0, "SINGLE_S"),
        ("1<P<3 e 3≤S<5: só S em tensão", 2.0, "INDEPENDENT", 4.5, "TENSION_S"),
        ("P≤1 e 3≤S<5: só S em tensão", 0.5, "INDEPENDENT", 4.5, "TENSION_S"),
        ("P≤1 e S≤1: matched", 0.5, "INDEPENDENT", 0.8, "MATCHED"),
        ("P≥3 e S ausente", 3.0, "ABSENT", None, "TENSION_P"),
        ("P<3 e S ausente: armed", 2.0, "ABSENT", None, "ARMED"),
        ("P<3 e S não independente <5: armed", 2.0, "NONINDEPENDENT", 4.0, "ARMED"),
        ("P com r não finito: integridade P", float("nan"), "INDEPENDENT", 5.0, "INCONCLUSIVE_P"),
        ("S INVALID domina mesmo com r_S≥5", 2.0, "INVALID", 5.0, "INCONCLUSIVE_S"),
        ("covariância cruzada ausente não é INVALID", 2.0, "NONINDEPENDENT", 5.0, "SINGLE_S"),
        ("r_S não finito é INVALID intrínseco", 2.0, "INDEPENDENT", float("nan"), "INCONCLUSIVE_S"),
        ("P ausente", None, "ABSENT", None, "AWAITING_SOURCE_P"),
        ("P≥5 e S independente <5: nunca BOTH", 5.0, "INDEPENDENT", 4.9, "SINGLE_P"),
    ]
    casos = []
    for nome, r_p, estado, r_s, esperado in definicoes:
        obtido = veredito_sintetico(r_p, estado, r_s)
        r_p_json = r_p if r_p is None or math.isfinite(r_p) else str(r_p)
        r_s_json = r_s if r_s is None or math.isfinite(r_s) else str(r_s)
        casos.append({"caso": nome, "r_P": r_p_json, "estado_S": estado,
                      "r_S": r_s_json, "esperado": esperado, "obtido": obtido,
                      "passa": obtido == esperado})
    return casos


def validate() -> dict:
    canais_path = ROOT / "CANAIS_K01.json"
    registro_path = ROOT / "REGISTRO_MAPA_K01.json"
    canais_doc = json.loads(canais_path.read_text(encoding="utf-8"))
    registro = json.loads(registro_path.read_text(encoding="utf-8"))
    assert isinstance(canais_doc, dict)
    assert set(canais_doc["ressalvas_glossario"]) == {f"R{i}" for i in range(1, 8)}
    canais = canais_doc["canais"]
    assert isinstance(canais, list) and len(canais) == 20, "a entrega deve conter exatamente 20 canais"
    ids = [c["id"] for c in canais]
    assert len(ids) == len(set(ids)), "id de canal duplicado"
    fontes = set(canais_doc["fontes_publicas"])
    for canal in canais:
        assert REQUIRED_CHANNEL_FIELDS <= set(canal), f"campos ausentes em {canal.get('id')}"
        assert all(canal[field] is not None for field in REQUIRED_CHANNEL_FIELDS)
        assert set(canal["sete_ressalvas"]) == {f"R{i}" for i in range(1, 8)}, canal["id"]
        assert canal["classificacao"] in {
            "EXISTE E ESTÁ LIGADO", "EXISTE NA BANCADA MAS NÃO ESTÁ LIGADO",
            "SABIDO POR REFERÊNCIA", "AUSENTE",
        }, canal["id"]
        for chave in ("formula", "valor", "local_core"):
            assert chave in canal["previsao"], f"previsao.{chave} ausente em {canal['id']}"
        for chave in ("existe_hoje", "publico", "conhecimento", "calendario", "fontes"):
            assert chave in canal["dado"], f"dado.{chave} ausente em {canal['id']}"
        for chave in ("possivel", "como", "impedimento"):
            assert chave in canal["cegueira"], f"cegueira.{chave} ausente em {canal['id']}"
        for chave in ("conta", "sigma_fonte", "avaliacao"):
            assert chave in canal["poder_desenho"], f"poder_desenho.{chave} ausente em {canal['id']}"
        for chave in ("sobreposicao", "nota"):
            assert chave in canal["independencia"], f"independencia.{chave} ausente em {canal['id']}"
        for chave in ("tipo", "se_falsifica", "se_sem_poder"):
            assert chave in canal["consequencia_negativo"], f"negativo.{chave} ausente em {canal['id']}"
        for fonte in canal["dado"].get("fontes", []) + canal["dado"].get("liberacoes", []):
            assert fonte in fontes, f"fonte não resolvida {fonte} em {canal['id']}"

    m2 = next(c for c in canais if c["id"] == "neutrino_m2_juno")
    atual = design()["m2"]["planning_atual"]
    for campo_json, campo_design in (
        ("D", "D_com_sigma_publicado"),
        ("D_0p5pct", "D_se_precisao_relativa_0p5pct"),
        ("D_0p3pct", "D_se_precisao_relativa_0p3pct"),
        ("precisao_relativa_para_5sigma", "precisao_relativa_para_5sigma"),
        ("precisao_relativa_para_D90", "precisao_relativa_para_D90"),
    ):
        assert math.isclose(m2["poder_desenho"][campo_json], atual[campo_design], rel_tol=0.0, abs_tol=1.0e-12), campo_json
    assert m2["poder_desenho"]["poder_conjoint"].startswith("[OPEN]")

    pre = (ROOT / "PRE_REGISTRO_CEGO_RASCUNHO_K01.md").read_text(encoding="utf-8")
    for token in (
        "Tabela-verdade", "ABSENT", "NONINDEPENDENT", "INDEPENDENT", "INVALID",
        "TGL_NU_M2_FALSIFIED", "T_SINGLE(P)_AWAITING_S", "T_SINGLE(S)_NONINDEPENDENT",
        "TENSION_BOTH_NONINDEPENDENT", "OPEN_RULE_GAP", "integridade intrínseca",
        "covariância condicional **cruzada", "INCONCLUSIVE_SYSTEMATICS__INTEGRITY_S",
        "liberação/abertura/comunicação", "poder conjunto", "D_{\\rm exato}",
    ):
        assert token in pre, f"tabela/guarda sem o token necessário: {token}"
    assert "7,0594" not in pre, "planning linear antigo reapareceu no pré-registro"
    entrega = (ROOT / "ENTREGA_K01.md").read_text(encoding="utf-8")
    assert "7,0594" not in entrega, "planning linear antigo reapareceu na entrega"
    assert "não como rol atualizado de 2026" in entrega
    casos_sinteticos = synthetic_cases()
    falhas_sinteticas = [c for c in casos_sinteticos if not c["passa"]]
    assert not falhas_sinteticas, f"casos sintéticos R2 falharam: {falhas_sinteticas}"

    assert REQUIRED_ROUTE_FIELDS <= set(registro)
    assert registro["tipo"] == "ROTA"
    assert registro["olhou_dados"] is False
    assert registro["status"] == "PROPOSTA"
    assert registro["estatuto"] == "DECLARADO"
    assert registro["corrige"] in (None, "")
    for artefato in registro["artefatos"]:
        assert Path(artefato).is_file(), f"artefato do registro ausente: {artefato}"

    summary_lines = _summary_line_count(entrega)
    assert summary_lines <= 15, f"resumo tem {summary_lines} linhas"
    termo = "descoberta autoevidente em dados públicos, carente de creditação acadêmica"
    assert termo in entrega
    assert "NOT_FALSIFIED" in entrega and "CONFIRMED" in entrega
    order_bytes = ORDER.read_bytes()
    assert len(order_bytes) == 886
    assert hashlib.sha256(order_bytes).hexdigest() == ORDER_SHA256

    rota_id = registro["rota_id"]
    comando = [sys.executable, r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "consultar", rota_id]
    proc = subprocess.run(comando, check=True, capture_output=True, text=True)
    consulta = json.loads(proc.stdout)
    ja_existe = any(r.get("rota_id") == rota_id for r in consulta.get("rotas", []))
    assert not ja_existe, f"a rota já foi registrada e não deve ser duplicada: {rota_id}"

    names = [
        "ENTREGA_K01.md", "CANAIS_K01.json", "PRE_REGISTRO_CEGO_RASCUNHO_K01.md",
        "REGISTRO_MAPA_K01.json", "PERGUNTA_K01.md", "ERRATA_K01.md", "ERRATA_K01_R2.md", "K01_validar.py",
    ]
    files = []
    for name in names:
        path = ROOT / name
        assert path.is_file(), f"arquivo ausente: {name}"
        files.append({"arquivo": name, "bytes": path.stat().st_size, "sha256": sha256(path)})

    rev0_esperado = {
        "ENTREGA_K01.md": (24391, "c21cf76acc3cf16d95ae6f3cd050578de3f618aa30ad60ead883bee063ee66cf"),
        "CANAIS_K01.json": (83527, "4caf58e61e30d03dd9d7f4c624d06d33a3846d12dcff183e4c9d5396bb7535d1"),
        "PRE_REGISTRO_CEGO_RASCUNHO_K01.md": (16431, "667f321f0a91a90a00282d3706d34f91fc6dfc1e3e3656868003e2d892846735"),
        "REGISTRO_MAPA_K01.json": (5444, "332d80cb6eecb2847f9adda428ee66c6d6e821d789f50ae127580919f9386c61"),
        "PERGUNTA_K01.md": (4466, "a7a61ef03b55a12666d56ac987859cf0b705e67781b04e7b4158d7acea55fe76"),
        "K01_validar.py": (8773, "f5a527706e6f9bebf713006d75b98bac4947b6d0df139771ff34a0e5d1e248f9"),
        "VALIDACAO_K01.json": (1581, "ea695619e241f595b08df68705eb4e59cc2b460d0e10963c60e296c9e91acea0"),
    }
    rev0 = []
    for nome, (n_bytes, hash_esperado) in rev0_esperado.items():
        path = ROOT / "K01" / "REV0" / f"2026-11-13_REV0_{nome}"
        assert path.is_file(), f"backup REV0 ausente: {path}"
        assert path.stat().st_size == n_bytes, f"backup REV0 mudou de tamanho: {nome}"
        assert sha256(path) == hash_esperado, f"backup REV0 mudou de conteúdo: {nome}"
        rev0.append({"arquivo": str(path.relative_to(ROOT)), "bytes": n_bytes, "sha256": hash_esperado})

    rev1_esperado = {
        "ENTREGA_K01.md": (28836, "482223368239a565c3953bac3ec8e84aaecd36f33008193c714be957b4f41fcc"),
        "CANAIS_K01.json": (87641, "8943d3fc3074c7c5f8676c2588ed6ad67aaaac9daefaac4b7daaf146b6479bab"),
        "PRE_REGISTRO_CEGO_RASCUNHO_K01.md": (24344, "95127964bc9414ffed724ca71aae21ece40a779b95353346df740ec681006f0a"),
        "REGISTRO_MAPA_K01.json": (7653, "7bb2dbc66636cb7a8bede51d85170cb18e0c7dc632d86ab24543cce70e64c745"),
        "PERGUNTA_K01.md": (5538, "ebb60057ddd928e8b207d4e9d6977f453cff4ab5a214690deb2052cdddf9c9de"),
        "K01_validar.py": (14816, "4d8f15a7526874032baedf4b61d495fb12057950f4efc2653985d6e31b7a2dcf"),
        "VALIDACAO_K01.json": (4328, "7d82d17894696c606352aa13b89922f99bca4a3e844c759e299ded636d8f8f93"),
    }
    rev1 = []
    for nome, (n_bytes, hash_esperado) in rev1_esperado.items():
        path = ROOT / "K01" / "REV1" / f"2026-11-13_REV1_{nome}"
        assert path.is_file(), f"backup REV1 ausente: {path}"
        assert path.stat().st_size == n_bytes, f"backup REV1 mudou de tamanho: {nome}"
        assert sha256(path) == hash_esperado, f"backup REV1 mudou de conteúdo: {nome}"
        rev1.append({"arquivo": str(path.relative_to(ROOT)), "bytes": n_bytes, "sha256": hash_esperado})

    return {
        "contrato": "VALIDACAO_DOCUMENTAL_K01_V3_R2",
        "json_validos": ["CANAIS_K01.json", "REGISTRO_MAPA_K01.json"],
        "n_canais": len(canais),
        "exatamente_20_canais": True,
        "sete_campos_por_canal": True,
        "campos_aninhados_completos": True,
        "fontes_resolvidas": True,
        "sete_ressalvas_por_canal": True,
        "planning_exato_em_delta_m2": atual,
        "tabela_verdade_presente": True,
        "guarda_alinhada": True,
        "registro_no_formato_modelo": True,
        "registro_real_consultado": {
            "comando": "python C:\\IALD\\MAPA_DE_ROTAS\\rotas.py consultar \"" + rota_id + "\"",
            "rota_id": rota_id,
            "rota_ja_registrada": False,
            "registro_foi_registrado": False,
        },
        "resumo_linhas_nao_vazias": summary_lines,
        "resumo_limite": 15,
        "ordem_original": {"bytes": len(order_bytes), "sha256": ORDER_SHA256},
        "arquivos": files,
        "rev0": rev0,
        "rev1": rev1,
        "testes_sinteticos": {
            "n": len(casos_sinteticos),
            "todos_passam": True,
            "casos": casos_sinteticos,
            "fronteira_invalid_nonindependent_confirmada": True,
            "cobertura_x_ge_5_com_outra_menor_ou_ausente": True,
            "tension_both_somente_ambos_em_3_a_5": True,
        },
        "escopo": "somente documental e casos sintéticos; nenhum teste empírico executado; nenhum vetor observado lido; nenhum registro no Mapa ou depósito na fila",
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
