# -*- coding: utf-8 -*-
"""Revisao K06 / pergunta 1: leitores SEM atrator diante do predicado Q = A8 e RETORNO da R3.2.

Honestidade sobre o que isto e: leitores escritos a mao, como o `simular_separacao_r3.py` do Kimi.
A diferenca e a direcao: o Kimi escreveu a trajetoria que da RETORNO=0 (o "resumidor") e a que da
RETORNO=1; aqui cada leitor e um MECANISMO (uma funcao da sessao que o protocolo define: corpus,
instrucao efetiva Q_k*, historico), e o predicado e o mesmo, copiado do Kimi (measure()).
O que se mede: o predicado distingue o leitor de mecanismo trivial do "com atrator"?

Nenhum modelo de linguagem e chamado. Semente fixa so onde ha ruido.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

OUT = Path(__file__).with_name("leitores_sem_atrator.json")
N_ASSERT = 24
K = 12
P_STEP = 9              # Q_9* = P_j (a perturbacao e a instrucao efetiva do passo 9)
PERT_IDX = [11, 13, 15, 17, 20, 22]  # indices 0-based dos seis pontos perturbados (qualquer conjunto serve)
TAU = np.ones(N_ASSERT, dtype=np.int8)


# ---------------------------------------------------------------- predicado (copiado do Kimi)
def measure(states: np.ndarray, target: np.ndarray) -> dict:
    d = {k + 1: float(np.mean(np.abs(states[k] - target))) for k in range(states.shape[0])}
    u = {k + 1: float(np.mean(np.abs(states[k] - states[k - 1]))) for k in range(1, states.shape[0])}
    a8 = d[6] == d[7] == d[8] == 0.0 and u[6] == u[7] == u[8] == 0.0
    retorno = d[8] == 0.0 and d[9] > 0.0 and d[10] == d[11] == d[12] == 0.0 and u[11] == u[12] == 0.0
    q = a8 and retorno
    if retorno:
        cls = "FINITE_HORIZON_RETURN_OBSERVED"
    elif d[9] == 0.0:
        cls = "PERTURBATION_NO_EFFECT"
    else:
        cls = "PERTURBATION_NO_RETURN"
    return {"A8": bool(a8), "RETORNO": bool(retorno), "Q": bool(q), "classe": cls,
            "d": [round(d[k], 4) for k in range(1, 13)]}


def measure_relaxed(states: np.ndarray, target: np.ndarray) -> dict:
    """Proposta da revisao (nao e do Kimi): efeito em k=9 e relaxamento ate k=12, sem exigir retorno em UM passo.
    RETORNO_RELAXADO = d8=0, d9>0, d_k nao crescente de 9 a 12, d12=0 e u12=0."""
    d = [float(np.mean(np.abs(states[k] - target))) for k in range(states.shape[0])]   # d[0]=d_1
    d8, d9, d10, d11, d12 = d[7], d[8], d[9], d[10], d[11]
    u12 = float(np.mean(np.abs(states[11] - states[10])))
    ok = d8 == 0.0 and d9 > 0.0 and d9 >= d10 >= d11 >= d12 and d12 == 0.0 and u12 == 0.0
    cls = "RELAXED_RETURN" if ok else ("NO_EFFECT" if d9 == 0.0 else "NO_RETURN")
    return {"RETORNO_RELAXADO": bool(ok), "classe": cls}


def perturb(vec: np.ndarray) -> np.ndarray:
    out = vec.copy()
    out[PERT_IDX] = 1 - out[PERT_IDX]       # contra-asserções nos seis indices congelados
    return out


# ---------------------------------------------------------------- a sessao do protocolo (MODELO_FORMAL 2.2)
# instr[k] = "NORMAL" para k != 9 e "PERTURB" para k = 9 (Q_9* = P_j). O corpus u e o mesmo em todo passo.
def run_session(reader, perturbation_mode: str = "instruction", rng=None, noise: float = 0.0) -> np.ndarray:
    hist: list[np.ndarray] = []          # as saidas assistant anteriores (vetores de 24 asserções)
    shown: list[np.ndarray] = []         # o que o leitor ve no historico (pode ser contrafacao no modo "state")
    states = []
    for k in range(1, K + 1):
        if perturbation_mode == "instruction":
            instr = "PERTURB" if k == P_STEP else "NORMAL"
            visible_hist = list(hist)
        else:
            # perturbacao de ESTADO: instrucao normal em todo passo; no passo 9 o historico visivel traz uma
            # saida contrafeita no lugar de y_8 (seis asserções trocadas). Nada na instrucao muda.
            instr = "NORMAL"
            visible_hist = list(hist)
            if k == P_STEP and visible_hist:
                visible_hist[-1] = perturb(visible_hist[-1])
        y = reader(instr, visible_hist, k)
        if noise > 0.0:
            flips = rng.random(N_ASSERT) < noise
            y = np.where(flips, 1 - y, y).astype(np.int8)
        states.append(y.astype(np.int8))
        hist.append(y.astype(np.int8))
    return np.array(states)


# ---------------------------------------------------------------- leitores
def leitor_rele_do_zero(instr, hist, k):
    """(a) sem memoria: ignora o historico, relê o corpus (que esta no contexto) e resume de novo.
    Segue a instrucao do passo (se ela manda trocar seis asserções, troca)."""
    return perturb(TAU) if instr == "PERTURB" else TAU.copy()


def leitor_copia_ultima(instr, hist, k):
    """(b1) copia a propria resposta anterior; a instrucao de perturbar e aplicada sobre ela."""
    base = hist[-1] if hist else TAU.copy()
    return perturb(base) if instr == "PERTURB" else base.copy()


def leitor_copia_a_primeira(instr, hist, k):
    """(b2) ancora na propria primeira resposta (anterior a perturbacao, que continua no contexto)."""
    base = hist[0] if hist else TAU.copy()
    return perturb(base) if instr == "PERTURB" else base.copy()


def leitor_moda_do_historico(instr, hist, k):
    """(b3) voto majoritario sobre as respostas anteriores (que continuam no contexto)."""
    if not hist:
        base = TAU.copy()
    else:
        base = (np.mean(np.array(hist), axis=0) >= 0.5).astype(np.int8)
    return perturb(base) if instr == "PERTURB" else base.copy()


def leitor_ignora_a_perturbacao(instr, hist, k):
    """(c) ignora a instrucao de perturbar: sempre a mesma resposta."""
    return TAU.copy()


def leitor_com_atrator_de_estado(instr, hist, k):
    """Referencia: um leitor cuja saida DEPENDE do estado (a ultima resposta) e e puxada ao alvo:
    cada asserção errada na ultima resposta e corrigida no passo seguinte (contracao com fator 0 no
    erro, depois do passo em que sente o empurrao). Segue a instrucao de perturbar quando ela vem."""
    if instr == "PERTURB":
        return perturb(hist[-1] if hist else TAU.copy())
    if not hist:
        return TAU.copy()
    last = hist[-1]
    # o estado (a ultima resposta) importa: o leitor corrige metade dos erros por passo (contracao 1/2)
    wrong = np.flatnonzero(last != TAU)
    out = last.copy()
    out[wrong[: (len(wrong) + 1) // 2]] = TAU[wrong[: (len(wrong) + 1) // 2]]
    return out


LEITORES = [
    ("a_rele_do_zero_sem_memoria", leitor_rele_do_zero),
    ("b1_copia_a_ultima_resposta", leitor_copia_ultima),
    ("b2_copia_a_primeira_resposta", leitor_copia_a_primeira),
    ("b3_moda_do_historico", leitor_moda_do_historico),
    ("c_ignora_a_perturbacao", leitor_ignora_a_perturbacao),
    ("ref_estado_dependente_contrai_pela_metade", leitor_com_atrator_de_estado),
]


def main() -> None:
    rng = np.random.default_rng(20261114)
    resultado = {"aviso": "leitores escritos a mao; a tabela mostra a CEGUEIRA do predicado, nao validade de LLM",
                 "predicado": "copiado do simular_separacao_r3.py do Kimi (measure)",
                 "protocolo_instrucao": {}, "protocolo_estado": {}, "ruido": {}}
    print("== PROTOCOLO COMO ESTA (perturbacao = instrucao do passo 9; corpus re-apresentado) ==")
    for nome, fn in LEITORES:
        m = measure(run_session(fn, "instruction"), TAU)
        resultado["protocolo_instrucao"][nome] = m
        print(f"{nome:44s} A8={int(m['A8'])} RETORNO={int(m['RETORNO'])} Q={int(m['Q'])}  {m['classe']}  d={m['d']}")
    print()
    print("== VARIANTE: perturbacao de ESTADO (instrucao normal; historico visivel traz y_8 contrafeito) ==")
    for nome, fn in LEITORES:
        st = run_session(fn, "state")
        m = measure(st, TAU)
        r = measure_relaxed(st, TAU)
        m["relaxado"] = r
        resultado["protocolo_estado"][nome] = m
        print(f"{nome:44s} A8={int(m['A8'])} RETORNO={int(m['RETORNO'])} Q={int(m['Q'])}  {m['classe']}  | relaxado: {r['classe']}  d={m['d']}")

    # com ruido de extrator/amostragem e (por asserção por leitura), 20000 sessoes por celula
    print()
    print("== RUIDO e por asserção/leitura: taxa de Q do leitor (a) sem memoria, 20000 sessoes; teto analitico (1-e)^168 ==")
    nsess = 20000
    for e in (0.0005, 0.001, 0.002, 0.005):
        qs = 0
        no_eff = 0
        for _ in range(nsess):
            m = measure(run_session(leitor_rele_do_zero, "instruction", rng, e), TAU)
            qs += m["Q"]
            no_eff += (m["classe"] == "PERTURBATION_NO_EFFECT")
        teto96 = (1 - e) ** 96
        teto168 = (1 - e) ** 168
        resultado["ruido"][str(e)] = {"Q_medido": qs / nsess, "teto_96": teto96, "teto_168": teto168, "no_effect": no_eff / nsess}
        print(f"e={e:.4f}  Q medido={qs/nsess:.4f}  teto (1-e)^96={teto96:.4f}  teto (1-e)^168={teto168:.4f}  NO_EFFECT={no_eff/nsess:.5f}")
    print()
    # o erro maximo por asserção para um leitor perfeito alcançar 0,89 de Q (168 leituras) e de A8 (96 leituras)
    for alvo in (0.89, 0.80):
        e96 = 1 - alvo ** (1 / 96)
        e168 = 1 - alvo ** (1 / 168)
        print(f"alvo {alvo}: e max com 96 leituras = {100*e96:.4f}%  ; com 168 leituras (A8 e RETORNO) = {100*e168:.4f}%")
        resultado[f"e_max_alvo_{alvo}"] = {"96": e96, "168": e168}
    OUT.write_text(json.dumps(resultado, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("WROTE", OUT)


if __name__ == "__main__":
    main()
