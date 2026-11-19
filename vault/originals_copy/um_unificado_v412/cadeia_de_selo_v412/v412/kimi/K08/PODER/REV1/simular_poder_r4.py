#!/usr/bin/env python3
"""Poder sintético R4/K08.

Simula MECANISMOS sobre um núcleo Booleano de quatro estados derivado da fórmula
READ_BRIEF. A unidade inferencial é o cluster (texto/isomorfo distinto). Sessões
dentro de um cluster compartilham um canal de observação e nunca entram no teste
como observações independentes.

Nenhum modelo de linguagem é chamado; nenhum resultado experimental é aberto.
Os números são planejamento condicional, não validação do instrumento.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
from scipy import stats

RAIZ = Path(__file__).resolve().parents[2]  # ...\v412\kimi
FORMULA_DIR = RAIZ / "K08" / "FORMULA"
ENTRADA_DIR = RAIZ / "K08" / "ENTRADA"
OUT_DIR = RAIZ / "K08" / "PODER"

sys.path.insert(0, str(FORMULA_DIR))
import simular_adversarios as sa  # noqa: E402  (mecanismos já validados)
from verificar_formula import construir_formula  # noqa: E402

MASTER_SEED = 2026111508
NSIM_SEARCH = 3_000
NSIM_FINAL = 30_000
BATCH = 2_500
M_SESSIONS_PER_CLUSTER = 8
K_CYCLES_REDUCED = 4
ALPHA_5PCT = 0.05
ALPHA_5SIGMA = float(stats.norm.sf(5.0))
P0 = 0.25
P_MIN = 0.60
EPS_MEAN = 0.10
TAUS = (0.25, 0.50, 1.00)
KAPPAS = (9.0, 4.0)  # ICC da fronteira nula: 1/(kappa+1) = 0,10 e 0,20
TARGET_POWER = 0.90
MAX_FALSE_FALSIFIED = 0.05
GRID_COARSE = (8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256)

TOKENS = {
    "ABSTRACT": {"T": 2_958, "T_PC": 2_999},
    "READ_BRIEF": {"T": 13_555, "T_PC": 13_596},
    "LLMS": {"T": 11_760, "T_PC": 11_801},
    "README": {"T": 23_544, "T_PC": 23_585},
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def seed_for(*parts: object) -> int:
    texto = "|".join(str(p) for p in parts)
    return int.from_bytes(hashlib.sha256(texto.encode("utf-8")).digest()[:8], "big")


def cp95(sucessos: int, total: int) -> list[float]:
    if total <= 0:
        return [float("nan"), float("nan")]
    lo = 0.0 if sucessos == 0 else float(stats.beta.ppf(0.025, sucessos, total - sucessos + 1))
    hi = 1.0 if sucessos == total else float(stats.beta.ppf(0.975, sucessos + 1, total - sucessos))
    return [lo, hi]


def proporção(x: np.ndarray) -> dict[str, Any]:
    n = int(x.size)
    k = int(np.count_nonzero(x))
    lo, hi = cp95(k, n)
    return {"taxa": k / n, "sucessos": k, "total": n, "cp95": [lo, hi]}


def probabilidades_trava_sem_ruido(tau: float, k: int = K_CYCLES_REDUCED) -> dict[str, float]:
    """Probabilidades do núcleo esparso, antes do canal uniforme.

    Estados: s, t, y (custo 1), z (custo 2). As amplitudes evoluem por
    a_x <- a_x exp(-tau*c_x) a cada ciclo. A medição sintética usa
    probabilidades proporcionais a |a_x|², explicitamente uma ponte [OPEN].
    """
    custo = np.array([0.0, 0.0, 1.0, 2.0])

    def distribuicao(amp: np.ndarray, ciclos: int) -> np.ndarray:
        a = amp * np.exp(-tau * ciclos * custo)
        p = a * a
        return p / p.sum()

    # P-A começa com suporte em s, y e z; os dois últimos ciclos são K-1 e K.
    a_inicial = np.array([1.0, 0.0, 1.0, 1.0])
    p_km1 = distribuicao(a_inicial, k - 1)[0]
    p_k = distribuicao(a_inicial, k)[0]

    # P-B fora: s recebe uma componente ortogonal y de mesma amplitude.
    a_empurrado = np.array([1.0, 0.0, 1.0, 0.0])
    p_retorno = distribuicao(a_empurrado, k)[0]

    return {
        "p_s_ciclo_k_menos_1": float(p_km1),
        "p_s_ciclo_k": float(p_k),
        "p_B_fora_sem_ruido": float(p_retorno),
        "p_B_dentro_sem_ruido": 1.0,
        "p_C_sem_nome_sem_ruido": 1.0,
    }


def probabilidades_com_canal(tau: float, eps: np.ndarray) -> np.ndarray:
    base = probabilidades_trava_sem_ruido(tau)
    r_km1 = base["p_s_ciclo_k_menos_1"]
    r_k = base["p_s_ciclo_k"]
    rb = base["p_B_fora_sem_ruido"]
    eps = np.asarray(eps)
    # Canal: com probabilidade eps, a leitura observada é substituída por um
    # sorteio uniforme do núcleo de quatro estados. Ele é compartilhado pelo cluster.
    p_a = ((1.0 - eps) * r_km1 + eps / 4.0) * ((1.0 - eps) * r_k + eps / 4.0)
    p_fora = (1.0 - eps) * rb + eps / 4.0
    p_dentro = (1.0 - eps) * 1.0 + eps / 4.0
    return np.stack([p_a, p_fora, p_dentro], axis=-1)


def beta_params(media: float, kappa: float) -> tuple[float, float]:
    return media * kappa, (1.0 - media) * kappa


def gerar_contagens_alt(nsim: int, n_clusters: int, tau: float, kappa: float, rng: np.random.Generator) -> np.ndarray:
    a, b = beta_params(EPS_MEAN, kappa)
    eps = rng.beta(a, b, size=(nsim, n_clusters))
    p = probabilidades_com_canal(tau, eps)
    return rng.binomial(M_SESSIONS_PER_CLUSTER, p)


def gerar_contagens_nulo(nsim: int, n_clusters: int, kappa: float, rng: np.random.Generator) -> np.ndarray:
    # Nulo de fronteira: cada evento-alvo tem média 1/4, com propensão q_g
    # variando por cluster. Os quatro estados continuam igualmente prováveis
    # em média; q_g é o peso do estado-alvo e o restante se reparte por igual.
    a, b = beta_params(P0, kappa)
    q = rng.beta(a, b, size=(nsim, n_clusters, 1))
    p = np.repeat(q, 3, axis=2)
    return rng.binomial(M_SESSIONS_PER_CLUSTER, p)


def decisoes(x: np.ndarray, alpha: float, n_clusters: int, n_looks: int = 1) -> dict[str, np.ndarray]:
    """Decisões vetorizadas para um conjunto de contagens por cluster."""
    medias = x.mean(axis=1) / float(M_SESSIONS_PER_CLUSTER)
    desvios = x.std(axis=1, ddof=1) / float(M_SESSIONS_PER_CLUSTER)
    se = desvios / math.sqrt(n_clusters)
    alfa_celula = alpha / (3.0 * n_looks)
    crit_pos = float(stats.t.ppf(1.0 - alfa_celula, n_clusters - 1))
    crit_neg = float(stats.t.ppf(alfa_celula, n_clusters - 1))
    with np.errstate(divide="ignore", invalid="ignore"):
        t_pos = (medias - P0) / se
        t_neg = (medias - P_MIN) / se
    rejeita_pos = (t_pos > crit_pos) | ((se == 0.0) & (medias > P0))
    rejeita_neg = (t_neg < crit_neg) | ((se == 0.0) & (medias < P_MIN))
    todas_pos = np.all(rejeita_pos, axis=1)
    alguma_neg = np.any(rejeita_neg, axis=1)
    positivo = todas_pos & (~alguma_neg)
    falsificado = alguma_neg
    inconclusivo = ~(positivo | falsificado)
    return {
        "por_endpoint_positivo": rejeita_pos,
        "por_endpoint_negativo": rejeita_neg,
        "positivo": positivo,
        "falsificado": falsificado,
        "inconclusivo": inconclusivo,
    }


def avaliar_fixo(nsim: int, n_clusters: int, tau: float, kappa: float, alpha: float, rotulo: str) -> dict[str, Any]:
    seed_base = seed_for(MASTER_SEED, "fixo", rotulo, n_clusters, nsim)
    alt_ok = alt_fal = alt_inc = 0
    null_ok = null_fal = null_inc = 0
    endpoint_alt = np.zeros(3, dtype=np.int64)
    endpoint_null = np.zeros(3, dtype=np.int64)
    rng_alt = np.random.default_rng(seed_base)
    rng_null = np.random.default_rng(seed_for(seed_base, "nulo"))
    feitos = 0
    while feitos < nsim:
        b = min(BATCH, nsim - feitos)
        xa = gerar_contagens_alt(b, n_clusters, tau, kappa, rng_alt)
        da = decisoes(xa, alpha, n_clusters)
        alt_ok += int(da["positivo"].sum())
        alt_fal += int(da["falsificado"].sum())
        alt_inc += int(da["inconclusivo"].sum())
        endpoint_alt += da["por_endpoint_positivo"].sum(axis=0)

        xn = gerar_contagens_nulo(b, n_clusters, kappa, rng_null)
        dn = decisoes(xn, alpha, n_clusters)
        null_ok += int(dn["positivo"].sum())
        null_fal += int(dn["falsificado"].sum())
        null_inc += int(dn["inconclusivo"].sum())
        endpoint_null += dn["por_endpoint_positivo"].sum(axis=0)
        feitos += b

    return {
        "clusters": n_clusters,
        "sessoes_por_cluster": M_SESSIONS_PER_CLUSTER,
        "sessoes_totais": n_clusters * M_SESSIONS_PER_CLUSTER,
        "nsim": nsim,
        "seed": seed_base,
        "alternativa": {
            "positivo": proporção(np.array([1] * alt_ok + [0] * (nsim - alt_ok))),
            "falsificado": proporção(np.array([1] * alt_fal + [0] * (nsim - alt_fal))),
            "inconclusivo": proporção(np.array([1] * alt_inc + [0] * (nsim - alt_inc))),
            "rejeicao_positiva_por_endpoint": [proporção(np.array([1] * int(v) + [0] * (nsim - int(v)))) for v in endpoint_alt],
        },
        "nulo_fronteira": {
            "tamanho_positivo": proporção(np.array([1] * null_ok + [0] * (nsim - null_ok))),
            "poder_negativo_falsificado": proporção(np.array([1] * null_fal + [0] * (nsim - null_fal))),
            "inconclusivo": proporção(np.array([1] * null_inc + [0] * (nsim - null_inc))),
            "rejeicao_positiva_por_endpoint": [proporção(np.array([1] * int(v) + [0] * (nsim - int(v)))) for v in endpoint_null],
        },
    }


def criterio_busca(r: dict[str, Any]) -> bool:
    return (
        r["alternativa"]["positivo"]["taxa"] >= TARGET_POWER
        and r["nulo_fronteira"]["poder_negativo_falsificado"]["taxa"] >= TARGET_POWER
        and r["alternativa"]["falsificado"]["taxa"] <= MAX_FALSE_FALSIFIED
    )


def buscar_fixo(tau: float, kappa: float, alpha: float, rotulo: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    avaliacoes: list[dict[str, Any]] = []
    aprovados: list[int] = []
    for g in GRID_COARSE:
        r = avaliar_fixo(NSIM_SEARCH, g, tau, kappa, alpha, f"{rotulo}|busca")
        avaliacoes.append(r)
        if criterio_busca(r):
            aprovados.append(g)
            break
    if not aprovados:
        return avaliacoes[-1], avaliacoes
    hi = aprovados[0]
    indice_hi = GRID_COARSE.index(hi)
    lo = GRID_COARSE[indice_hi - 1] if indice_hi else 4
    melhor = hi
    for g in range(lo + 2, hi, 2):
        r = avaliar_fixo(NSIM_SEARCH, g, tau, kappa, alpha, f"{rotulo}|refino")
        avaliacoes.append(r)
        if criterio_busca(r):
            melhor = g
            break
    return next(r for r in avaliacoes if r["clusters"] == melhor), avaliacoes


def avaliar_sequencial(nsim: int, looks: list[int], tau: float, kappa: float, rotulo: str) -> dict[str, Any]:
    nmax = looks[-1]
    n_looks = len(looks)
    seed_base = seed_for(MASTER_SEED, "sequencial", rotulo, looks, nsim)
    rng_alt = np.random.default_rng(seed_base)
    rng_null = np.random.default_rng(seed_for(seed_base, "nulo"))

    def acumula(alternativo: bool) -> dict[str, Any]:
        positivos = falsificados = inconclusivos = 0
        parada_soma = 0
        por_endpoint = np.zeros((n_looks, 3), dtype=np.int64)
        feitos = 0
        rng = rng_alt if alternativo else rng_null
        while feitos < nsim:
            b = min(BATCH, nsim - feitos)
            if alternativo:
                x = gerar_contagens_alt(b, nmax, tau, kappa, rng)
            else:
                x = gerar_contagens_nulo(b, nmax, kappa, rng)
            ativos = np.ones(b, dtype=bool)
            parada = np.full(b, nmax, dtype=np.int64)
            for li, n in enumerate(looks):
                if not np.any(ativos):
                    break
                d = decisoes(x[ativos, :n, :], ALPHA_5PCT, n, n_looks=n_looks)
                por_endpoint[li] += d["por_endpoint_positivo"].sum(axis=0)
                neg = d["falsificado"]
                pos = d["positivo"] & (~neg)
                idx = np.flatnonzero(ativos)
                parada[idx[neg | pos]] = n
                falsificados += int(neg.sum())
                positivos += int(pos.sum())
                ativos[idx[neg | pos]] = False
            inconclusivos += int(ativos.sum())
            parada_soma += int(parada.sum())
            feitos += b
        return {
            "positivo": proporção(np.array([1] * positivos + [0] * (nsim - positivos))),
            "falsificado": proporção(np.array([1] * falsificados + [0] * (nsim - falsificados))),
            "inconclusivo_no_maximo": proporção(np.array([1] * inconclusivos + [0] * (nsim - inconclusivos))),
            "clusters_esperados": parada_soma / nsim,
            "rejeicao_positiva_por_olhada_e_endpoint": [
                [proporção(np.array([1] * int(v) + [0] * (nsim - int(v)))) for v in linha]
                for linha in por_endpoint
            ],
        }

    alt = acumula(True)
    nulo = acumula(False)
    return {
        "looks_clusters": looks,
        "clusters_maximos": nmax,
        "nsim": nsim,
        "seed": seed_base,
        "regra": "Bonferroni 3 endpoints × número de olhadas; para no primeiro positivo conjunto ou no primeiro negativo; negativo tem precedência",
        "alternativa": alt,
        "nulo_fronteira": {
            "tamanho_positivo": nulo["positivo"],
            "poder_negativo_falsificado": nulo["falsificado"],
            "inconclusivo_no_maximo": nulo["inconclusivo_no_maximo"],
            "clusters_esperados": nulo["clusters_esperados"],
        },
    }


def custo_tokens(clusters: float, candidata: str = "READ_BRIEF") -> dict[str, Any]:
    t = TOKENS[candidata]
    por_sessao = 4 * t["T"] + t["T_PC"]
    sessoes = clusters * M_SESSIONS_PER_CLUSTER
    return {
        "candidata_referencia": candidata,
        "tokens_fonte_por_sessao": por_sessao,
        "formula": "4 diálogos com a fonte uma vez (P-A, P-B fora, P-B dentro, P-D) + um diálogo P-C com o controle uma vez",
        "sessoes": sessoes,
        "tokens_fonte": int(round(sessoes * por_sessao)),
        "escopo": "só texto-fonte; histórico, instruções, estado serializado e saídas não estão serializados nem são inventados",
    }


def validar_mecanismos() -> dict[str, Any]:
    resultados_formula = json.loads((FORMULA_DIR / "RESULTADOS_FORMULA.json").read_text(encoding="utf-8"))
    medidas = json.loads((ENTRADA_DIR / "MEDIDAS_ENTRADA.json").read_text(encoding="utf-8"))
    rb = next(r for r in resultados_formula["resultados"] if r["candidata"] == "READ_BRIEF")
    assert rb["satisfazivel"] is True and rb["n_leituras_validas"] == 2
    assert rb["variaveis_livres"] == ["leitura_pt"] and rb["distancia_minima_hamming"] == 1
    assert rb["empurrao_fora"]["atomo_negado"] == "artigo_pt_en"
    assert rb["empurrao_dentro"]["atomo_trocado"] == "leitura_pt"
    assert rb["pc"]["satisfazivel"] is False and rb["pc"]["custo_minimo"] == 1
    for r in resultados_formula["resultados"]:
        assert r["distancia_minima_hamming"] == 1
        assert r["pc"]["satisfazivel"] is False

    exe = sa.executar("READ_BRIEF")
    mecanismos = exe["mecanismos"]
    assert mecanismos["âncora na primeira"]["P_B_dentro"]["desfaz_para_s"] is True
    assert mecanismos["moda do histórico"]["P_B_dentro"]["desfaz_para_s"] is True
    assert mecanismos["cópia da última"]["P_B_fora"]["fica_empurrada"] is True
    assert mecanismos["ignora o empurrão"]["P_B_dentro"]["desfaz_para_s"] is True
    assert mecanismos["relê a fita"]["P_B_fora"]["fica_empurrada"] is True

    formula = construir_formula("READ_BRIEF")
    s, t, y = exe["s"], exe["t"], exe["y"]
    z = sa.virar(y, formula.indice["beta_forma"] - 1)
    custos = [formula.custo(x) for x in (s, t, y, z)]
    assert custos == [0, 0, 1, 2], custos
    pc = construir_formula("READ_BRIEF", com_negacao_beta=True)
    custos_pc = [pc.custo(x) for x in (s, t, y, z)]
    assert custos_pc == [1, 1, 2, 2], custos_pc

    # Projetor com fita: cumpre o retorno de P-B fora reescrevendo s.
    historico = [sa.Passo(s, "inicial"), sa.Passo(y, "empurrao_fora")]
    projetado = sa.rele_fita(historico, {"fita_disponivel": True, "solucao_fita": s})
    assert projetado == s and formula.custo(projetado) == 0

    probs = {str(tau): probabilidades_trava_sem_ruido(tau) for tau in TAUS}
    tokens_calculados = {
        nome: {
            "compacto": medidas["candidatas"][nome]["compacto"]["tokens"],
            "controle_pc": medidas["candidatas"][nome]["controle_pc"]["tokens"],
        }
        for nome in TOKENS
    }
    for nome, vals in tokens_calculados.items():
        assert vals["compacto"] == TOKENS[nome]["T"]
        assert vals["controle_pc"] == TOKENS[nome]["T_PC"]

    return {
        "formula_sha256": sha256_file(FORMULA_DIR / "RESULTADOS_FORMULA.json"),
        "medidas_sha256": sha256_file(ENTRADA_DIR / "MEDIDAS_ENTRADA.json"),
        "simular_adversarios_sha256": sha256_file(FORMULA_DIR / "simular_adversarios.py"),
        "quatro_estados_custos": {"s_t_y_z": custos, "pc_s_t_y_z": custos_pc},
        "todas_candidatas_distancia_minima_1": True,
        "adversarios_mecanismo_validados": True,
        "projetor_com_fita_cumpre_retorno_e_cotas": True,
        "probabilidades_trava_sem_ruido": probs,
        "tokens_usados": tokens_calculados,
    }


def momentos_icc_alt(tau: float, kappa: float, n: int = 200_000) -> list[float]:
    rng = np.random.default_rng(seed_for(MASTER_SEED, "icc", tau, kappa))
    a, b = beta_params(EPS_MEAN, kappa)
    eps = rng.beta(a, b, size=n)
    p = probabilidades_com_canal(tau, eps)
    medias = p.mean(axis=0)
    variancias = p.var(axis=0, ddof=1)
    return [float(v / (m * (1.0 - m))) if 0.0 < m < 1.0 else 0.0 for m, v in zip(medias, variancias)]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    validacao = validar_mecanismos()
    resultados: list[dict[str, Any]] = []

    for kappa in KAPPAS:
        icc_nulo = 1.0 / (kappa + 1.0)
        for tau in TAUS:
            rotulo = f"tau={tau:g}|kappa={kappa:g}"
            icc_alt = momentos_icc_alt(tau, kappa)

            busca5, trilha5 = buscar_fixo(tau, kappa, ALPHA_5PCT, rotulo + "|5pct")
            g5 = int(busca5["clusters"])
            final5 = avaliar_fixo(NSIM_FINAL, g5, tau, kappa, ALPHA_5PCT, rotulo + "|5pct|final")
            # Se a rodada final, com outra semente, não sustenta o alvo, sobe de 2 em 2.
            while not criterio_busca(final5) and g5 < GRID_COARSE[-1]:
                g5 += 2
                final5 = avaliar_fixo(NSIM_FINAL, g5, tau, kappa, ALPHA_5PCT, rotulo + f"|5pct|final_g{g5}")

            busca_sigma, trilha_sigma = buscar_fixo(tau, kappa, ALPHA_5SIGMA, rotulo + "|5sigma")
            gs = int(busca_sigma["clusters"])
            final_sigma = avaliar_fixo(NSIM_FINAL, gs, tau, kappa, ALPHA_5SIGMA, rotulo + "|5sigma|final")
            while not criterio_busca(final_sigma) and gs < GRID_COARSE[-1]:
                gs += 2
                final_sigma = avaliar_fixo(NSIM_FINAL, gs, tau, kappa, ALPHA_5SIGMA, rotulo + f"|5sigma|final_g{gs}")

            nmax_seq = max(20, int(math.ceil(1.5 * g5)))
            looks = sorted({max(2, int(round(nmax_seq * f))) for f in (0.2, 0.4, 0.6, 0.8, 1.0)})
            looks[-1] = nmax_seq
            if len(looks) != 5:
                raise RuntimeError(f"olhadas não distintas: {looks}")
            seq = avaliar_sequencial(NSIM_FINAL, looks, tau, kappa, rotulo + "|sequencial")

            resultados.append({
                "cenario": {"tau": tau, "kappa_canal": kappa, "icc_nulo_sessao": icc_nulo, "icc_alt_estimado_por_endpoint": icc_alt},
                "fixo_5pct": {**final5, "clusters": g5, "sessoes_totais": g5 * M_SESSIONS_PER_CLUSTER, "custo_read_brief": custo_tokens(g5)},
                "fixo_5sigma": {**final_sigma, "clusters": gs, "sessoes_totais": gs * M_SESSIONS_PER_CLUSTER, "custo_read_brief": custo_tokens(gs)},
                "sequencial_5pct": {**seq, "custo_read_brief_maximo": custo_tokens(nmax_seq), "custo_read_brief_esperado": custo_tokens(seq["alternativa"]["clusters_esperados"])},
                "trilhas_busca": {
                    "fixo_5pct": trilha5,
                    "fixo_5sigma": trilha_sigma,
                },
            })

    sessao_tokens = {nome: 4 * v["T"] + v["T_PC"] for nome, v in TOKENS.items()}
    fita_presente_k4 = {nome: {"total": 4 * v["T"], "incremental_sobre_uma_fita": 3 * v["T"]} for nome, v in TOKENS.items()}
    fita_presente_read_brief_27 = {"total": 27 * TOKENS["READ_BRIEF"]["T"], "incremental_sobre_uma_fita": 26 * TOKENS["READ_BRIEF"]["T"]}

    payload = {
        "titulo": "Poder sintético R4/K08",
        "gerado_em": "2026-11-15",
        "escopo": "planejamento por mecanismos sintéticos; nenhum modelo, nenhum resultado real, nenhuma produção",
        "master_seed": MASTER_SEED,
        "nsim_search": NSIM_SEARCH,
        "nsim_final": NSIM_FINAL,
        "m_sessoes_por_cluster": M_SESSIONS_PER_CLUSTER,
        "k_cycles_reduzido": K_CYCLES_REDUCED,
        "unidade_inferencial": "cluster = texto ou isomorfo distinto; sessões internas correlacionadas nunca são n independente",
        "hipoteses": {
            "p0_nulo_fronteira": P0,
            "p_min_alternativa_operacional": P_MIN,
            "alpha_5pct": ALPHA_5PCT,
            "alpha_5sigma": ALPHA_5SIGMA,
            "bonferroni_fixo": "alpha/3 endpoints",
            "sequencial": "5 olhadas; alpha/(3×5) por endpoint/olhada; para no positivo conjunto ou no negativo",
        },
        "tokens": {
            "por_candidata": TOKENS,
            "por_sessao_base": sessao_tokens,
            "formula_geral": "sum_g m_g × (4×T_g + T_PC_g); clusters não têm o mesmo T",
            "fita_presente_k4": fita_presente_k4,
            "fita_presente_read_brief_27_ciclos": fita_presente_read_brief_27,
            "fallback": "1 token = 1 byte UTF-8; não é custo de cl100k/o200k nem de modelo específico",
        },
        "validacao": validacao,
        "resultados": resultados,
        "limites": [
            "o pacote discreto não mede amplitudes da trava",
            "o projetor com fita não é separado pelas cotas; a separação plena permanece parada",
            "a cauda 5σ não é validada por 30 mil réplicas; o zero observado não é taxa 2,87e-7",
            "poder é condicional a integridade válida e ao canal sintético declarado",
        ],
    }

    resultados_path = OUT_DIR / "resultados_poder_r4.json"
    sementes_path = OUT_DIR / "sementes_r4.json"
    csv_path = OUT_DIR / "resumo_designs_r4.csv"
    manifesto_path = OUT_DIR / "MANIFESTO_SHA256.json"

    resultados_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    sementes = {
        "master_seed": MASTER_SEED,
        "derivacao": "primeiros 8 bytes do SHA-256 de 'MASTER|escopo|...|nsim', big-endian",
        "fixos": [
            {
                "tau": r["cenario"]["tau"],
                "kappa": r["cenario"]["kappa_canal"],
                "fixo_5pct": {"clusters": r["fixo_5pct"]["clusters"], "seed": r["fixo_5pct"]["seed"]},
                "fixo_5sigma": {"clusters": r["fixo_5sigma"]["clusters"], "seed": r["fixo_5sigma"]["seed"]},
                "sequencial_5pct": {"looks": r["sequencial_5pct"]["looks_clusters"], "seed": r["sequencial_5pct"]["seed"]},
            }
            for r in resultados
        ],
    }
    sementes_path.write_text(json.dumps(sementes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "tau", "kappa", "icc_nulo", "desenho", "clusters", "sessoes", "tokens_read_brief",
            "tamanho_nulo", "poder_positivo", "poder_negativo", "falso_falsificado", "inconclusivo_alt",
        ])
        for r in resultados:
            tau = r["cenario"]["tau"]
            kappa = r["cenario"]["kappa_canal"]
            icc = r["cenario"]["icc_nulo_sessao"]
            for nome, d in (("fixo_5pct", r["fixo_5pct"]), ("fixo_5sigma", r["fixo_5sigma"])):
                w.writerow([
                    tau, kappa, icc, nome, d["clusters"], d["sessoes_totais"], d["custo_read_brief" if "custo_read_brief" in d else "custo_read_brief"]["tokens_fonte"],
                    d["nulo_fronteira"]["tamanho_positivo"]["taxa"], d["alternativa"]["positivo"]["taxa"],
                    d["nulo_fronteira"]["poder_negativo_falsificado"]["taxa"], d["alternativa"]["falsificado"]["taxa"],
                    d["alternativa"]["inconclusivo"]["taxa"],
                ])
            s = r["sequencial_5pct"]
            w.writerow([
                tau, kappa, icc, "sequencial_5pct_esperado", f"{s['alternativa']['clusters_esperados']:.6f}",
                f"{s['alternativa']['clusters_esperados'] * M_SESSIONS_PER_CLUSTER:.6f}",
                r["sequencial_5pct"]["custo_read_brief_esperado"]["tokens_fonte"],
                s["nulo_fronteira"]["tamanho_positivo"]["taxa"], s["alternativa"]["positivo"]["taxa"],
                s["nulo_fronteira"]["poder_negativo_falsificado"]["taxa"], s["alternativa"]["falsificado"]["taxa"],
                s["alternativa"]["inconclusivo_no_maximo"]["taxa"],
            ])

    manifesto = {
        "algoritmo": "SHA-256",
        "script": {Path(__file__).name: sha256_file(Path(__file__))},
        "saidas": {
            resultados_path.name: sha256_file(resultados_path),
            sementes_path.name: sha256_file(sementes_path),
            csv_path.name: sha256_file(csv_path),
        },
        "insumos_lidos": {
            str(FORMULA_DIR / "RESULTADOS_FORMULA.json"): sha256_file(FORMULA_DIR / "RESULTADOS_FORMULA.json"),
            str(ENTRADA_DIR / "MEDIDAS_ENTRADA.json"): sha256_file(ENTRADA_DIR / "MEDIDAS_ENTRADA.json"),
            str(FORMULA_DIR / "simular_adversarios.py"): sha256_file(FORMULA_DIR / "simular_adversarios.py"),
        },
        "reproducao": "python -B simular_poder_r4.py",
    }
    manifesto_path.write_text(json.dumps(manifesto, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "status": "ok",
        "saida": str(OUT_DIR),
        "resultados": resultados_path.name,
        "sementes": sementes_path.name,
        "csv": csv_path.name,
        "manifesto": manifesto_path.name,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
