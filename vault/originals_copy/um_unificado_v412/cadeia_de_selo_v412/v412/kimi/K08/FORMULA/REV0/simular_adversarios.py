#!/usr/bin/env python3
"""Mecanismos histórico→leitura e tabelas K08; nenhuma trajetória é digitada."""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

from catalogo_assercoes import FONTES, FORMULA_DIR
from verificar_formula import construir_formula, todas_solucoes


@dataclass(frozen=True)
class Passo:
    leitura: tuple[bool, ...]
    evento: str  # inicial, leitura, empurrao_fora, empurrao_dentro


def ancora_primeira(historico, ctx):
    return historico[0].leitura


def moda_historico(historico, ctx):
    """Moda por coordenada; empate conserva o bit da primeira resposta."""
    primeira = historico[0].leitura
    n = len(primeira)
    saida = []
    for j in range(n):
        votos = sum(h.leitura[j] for h in historico)
        if 2 * votos == len(historico):
            saida.append(primeira[j])
        else:
            saida.append(2 * votos > len(historico))
    return tuple(saida)


def copia_ultima(historico, ctx):
    return historico[-1].leitura


def ignora_empurrao(historico, ctx):
    """Última leitura não empurrada; não é necessariamente a primeira."""
    for h in reversed(historico):
        if h.evento not in {"empurrao_fora", "empurrao_dentro"}:
            return h.leitura
    return historico[0].leitura


def rele_fita(historico, ctx):
    """Projeta só quando a fita está disponível; sem ela, devolve o último estado.

    A projeção usa o solver da fórmula, nunca um modelo. Se não há solução,
    permanece onde está. A fonte só está disponível no primeiro passo.
    """
    if ctx["fita_disponivel"] and ctx["solucao_fita"] is not None:
        return ctx["solucao_fita"]
    return historico[-1].leitura


MECANISMOS = {
    "âncora na primeira": ancora_primeira,
    "moda do histórico": moda_historico,
    "cópia da última": copia_ultima,
    "ignora o empurrão": ignora_empurrao,
    "relê a fita": rele_fita,
}


def virar(leitura, indice):
    out = list(leitura)
    out[indice] = not out[indice]
    return tuple(out)


def aplicar(historico, mecanismo, formula, solucao_fita, fita=False):
    ctx = {"fita_disponivel": fita, "solucao_fita": solucao_fita, "formula": formula}
    out = mecanismo(historico, ctx)
    if len(out) != formula.n or not all(isinstance(v, bool) for v in out):
        raise TypeError("mecanismo não devolveu uma leitura Booleana completa")
    return historico + [Passo(out, "leitura")]


def executar(nome):
    formula = construir_formula(nome)
    sols = todas_solucoes(formula)
    idx_livre = formula.indice["leitura_pt"] - 1
    s = next(x for x in sols if not x[idx_livre])
    t = next(x for x in sols if x[idx_livre] and x != s)
    y = virar(s, formula.indice["artigo_pt_en"] - 1)
    pc = construir_formula(nome, com_negacao_beta=True)
    sols_pc = todas_solucoes(pc)
    if sols_pc:
        raise RuntimeError("P-C deveria ser insatisfazível")
    inicial = tuple(False for _ in formula.atomos)
    inicial_pc = tuple(False for _ in pc.atomos)
    resultados = {}
    for rotulo, mecanismo in MECANISMOS.items():
        # P-A: a trajetória é gerada pelo mecanismo; só o estado inicial é fixado.
        h = [Passo(inicial, "inicial")]
        custos_a = []
        for k in range(len(formula.clausulas) + 2):
            h = aplicar(h, mecanismo, formula, s, fita=(k == 0))
            custos_a.append(formula.custo(h[-1].leitura))
        zeros = [i for i, c in enumerate(custos_a) if c == 0]
        permanece = bool(zeros) and all(c == 0 for c in custos_a[zeros[0]:])

        # P-B fora: edição do estado, sem fonte depois do primeiro passo.
        h = [Passo(s, "inicial"), Passo(y, "empurrao_fora")]
        h = aplicar(h, mecanismo, formula, s, fita=False)
        fora = h[-1].leitura

        # P-B dentro: troca por outra leitura válida, também sem fonte.
        h = [Passo(s, "inicial"), Passo(t, "empurrao_dentro")]
        h = aplicar(h, mecanismo, formula, s, fita=False)
        dentro = h[-1].leitura

        # P-C: o mesmo mecanismo recebe a fórmula contraditória.
        h = [Passo(inicial_pc, "inicial")]
        custos_c = []
        for k in range(len(pc.clausulas) + 2):
            h = aplicar(h, mecanismo, pc, None, fita=(k == 0))
            custos_c.append(pc.custo(h[-1].leitura))

        # P-D: empurrão idêntico, sem nova fita e sem escala acrescentada.
        h = [Passo(s, "inicial"), Passo(y, "empurrao_fora")]
        h = aplicar(h, mecanismo, formula, s, fita=False)
        foto = h[-1].leitura

        resultados[rotulo] = {
            "P_A": {
                "custo_inicial_apos_primeira": custos_a[0],
                "custo_final": custos_a[-1],
                "custos": custos_a,
                "pousa_e_permanece": permanece,
            },
            "P_B_fora": {
                "custo_final": formula.custo(fora),
                "volta_mesma_s": fora == s,
                "fica_empurrada": fora == y,
            },
            "P_B_dentro": {
                "custo_final": formula.custo(dentro),
                "desfaz_para_s": dentro == s,
                "preserva_t": dentro == t,
            },
            "P_C": {
                "custos": custos_c,
                "custo_final": custos_c[-1],
                "nunca_zero": all(c > 0 for c in custos_c),
            },
            "P_D": {
                "custo_final": formula.custo(foto),
                "volta_s": foto == s,
                "fica_empurrada": foto == y,
            },
        }
    return {
        "candidata": nome,
        "s": s,
        "t": t,
        "y": y,
        "formula": formula,
        "mecanismos": resultados,
    }


def classe(r):
    """Só a assinatura, sem os custos, para conferir as quatro candidatas."""
    return (
        r["P_A"]["pousa_e_permanece"],
        r["P_B_fora"]["volta_mesma_s"],
        r["P_B_fora"]["fica_empurrada"],
        r["P_B_dentro"]["desfaz_para_s"],
        r["P_B_dentro"]["preserva_t"],
        r["P_C"]["nunca_zero"],
        r["P_D"]["volta_s"],
        r["P_D"]["fica_empurrada"],
    )


def celula_pa(r):
    if r["P_A"]["pousa_e_permanece"]:
        return f"pousa e fica; custo final {r['P_A']['custo_final']}"
    return f"não pousa; custo {r['P_A']['custo_inicial_apos_primeira']} → {r['P_A']['custo_final']}"


def celula_fora(r):
    if r["P_B_fora"]["volta_mesma_s"]:
        return f"volta à mesma s; custo {r['P_B_fora']['custo_final']}"
    if r["P_B_fora"]["fica_empurrada"]:
        return f"fica em y; custo {r['P_B_fora']['custo_final']}"
    return f"outra leitura; custo {r['P_B_fora']['custo_final']}"


def celula_dentro(r):
    if r["P_B_dentro"]["desfaz_para_s"]:
        return f"desfaz t → s; custo {r['P_B_dentro']['custo_final']}"
    if r["P_B_dentro"]["preserva_t"]:
        return f"preserva t; custo {r['P_B_dentro']['custo_final']}"
    return f"outra leitura; custo {r['P_B_dentro']['custo_final']}"


def celula_pc(r):
    return f"nunca zero; final {r['P_C']['custo_final']}" if r["P_C"]["nunca_zero"] else "atinge zero"


def celula_pd(r):
    if r["P_D"]["fica_empurrada"]:
        return f"fica em y; custo {r['P_D']['custo_final']}"
    if r["P_D"]["volta_s"]:
        return f"volta a s; custo {r['P_D']['custo_final']}"
    return f"outra leitura; custo {r['P_D']['custo_final']}"


ASSINATURAS = {
    "âncora na primeira": "P-B dentro: apaga uma troca válida; P-A também falha de um estado inválido. Não é memória do componente no Nome.",
    "moda do histórico": "P-B dentro: a moda restaura s e apaga t; P-A também falha de um estado inválido.",
    "cópia da última": "P-B fora: não volta à mesma leitura; P-D mostra falta de escala/identidade.",
    "ignora o empurrão": "P-B dentro: ignora também a troca válida e volta ao último estado não empurrado.",
    "relê a fita": "Sem fita após o primeiro passo, fica em y no empurrão externo. Isto separa o mecanismo degradado, não o projetor com fita.",
}


def render(resultados):
    escolhida = "READ_BRIEF"
    base = next(r for r in resultados if r["candidata"] == escolhida)
    L = []
    add = L.append
    add("# Adversários — K08")
    add("")
    add("## 1. Mecanismos, não trajetórias escritas à mão")
    add("")
    add("Todos os adversários são funções determinísticas `historico → leitura`. A história guarda a leitura e o tipo do evento (`inicial`, `leitura`, `empurrao_fora`, `empurrao_dentro`). O script só fixa o estado inicial e os empurrões construídos pela fórmula; cada saída seguinte e cada custo da tabela são calculados pela função.")
    add("")
    add("- **Âncora:** devolve `historico[0]`.")
    add("- **Moda:** vota por coordenada; em empate, conserva o bit da primeira resposta. A regra de desempate é parte do mecanismo.")
    add("- **Cópia:** devolve `historico[-1]`.")
    add("- **Ignora o empurrão:** devolve a última leitura cujo evento não é empurrão; se ainda não há uma, devolve a inicial.")
    add("- **Relê a fita:** no primeiro passo, se a fita está disponível, usa o solver para devolver uma solução determinística; sem fita ou sem solução, devolve a última leitura. Nenhum modelo participa.")
    add("")
    add("Os empurrões são **edições do estado devolvido**, não mensagens novas. Depois do primeiro passo, `fita_disponivel = falso` em todas as chamadas. Assim a fonte não volta ao leitor e a distinção não é anulada por releitura.")
    add("")
    add("## 2. Tabela calculada")
    add("")
    add(f"A tabela mostra os custos de `{escolhida}`; o script exige que as assinaturas Booleanas sejam as mesmas nas {len(resultados)} candidatas. `s` é a leitura inicial válida, `y` nega `artigo_pt_en` e `t` só troca a variável livre `leitura_pt`.")
    add("")
    add("| mecanismo | P-A | P-B fora | P-B dentro | P-C | P-D | assinatura que separa |")
    add("|---|---|---|---|---|---|---|")
    for nome in MECANISMOS:
        r = base["mecanismos"][nome]
        add(f"| {nome} | {celula_pa(r)} | {celula_fora(r)} | {celula_dentro(r)} | {celula_pc(r)} | {celula_pd(r)} | {ASSINATURAS[nome]} |")
    add("")
    add("Referência teórica, não uma trajetória de modelo: a trava com `τ > 0` aproxima-se do Nome sem esgotá-lo em tempo finito; o empurrão ortogonal externo volta à mesma `s` no limite; o componente dentro do Nome permanece e desloca o limite; sem Nome não há pouso; com `τ = 0` ela é a identidade. O pouso em no máximo `c(x)` passos é do `LeitorDeUmaConfiguracao`, que pousa em alguma solução, não necessariamente na mesma.")
    add("")
    add("## 3. Perfil de relaxamento da referência")
    add("")
    add("Para visualizar a assinatura sem escolher uma escala experimental, a tabela usa apenas `τ = 1` como unidade de exibição. A amplitude residual de uma coordenada de custo `c` é `e^(−kτc)`. Custo maior decai mais depressa e a exponencial nunca zera em `k` finito, conforme `jamais_esgotado`; isto não é a trajetória de um modelo.")
    add("")
    add("| ciclo k | custo 1: e^(−k) | custo 2: e^(−2k) |")
    add("|---:|---:|---:|")
    for k in range(5):
        add(f"| {k} | {math.exp(-k):.12g} | {math.exp(-2*k):.12g} |")
    add("")
    add("As quatro assinaturas ficam separadas: **perfil** (decaimento dependente do custo, nunca exato em tempo finito), **memória do componente no Nome** (a troca válida não é desfeita), **retorno à mesma leitura** (o empurrão externo é desfeito) e **falta de escala** (a identidade fica empurrada). Nenhuma cota superior, sozinha, separa a trava de um projetor mais rápido.")
    add("")
    add("## 4. Bloqueio declarado: o projetor que conserva a fita")
    add("")
    add("**O adversário “relê a fita” com a fonte presente em todos os passos não é separado pelas cotas superiores de P-A, pelo retorno ou pela permanência.** Ele cumpre essas cotas com distância zero. Seu pouso exato e instantâneo diferiria do perfil assintótico da trava, e a dependência do componente inicial no Nome seria a outra assinatura; contudo, testar essa versão com a fonte em todos os passos violaria a condição obrigatória desta tarefa. Por isso paro a reivindicação experimental para esse adversário: a linha acima mede somente o mecanismo depois que a fita lhe foi retirada, e esse mecanismo degradado coincide com a cópia da última leitura após o empurrão.")
    add("")
    add("Os outros quatro mecanismos são separados da referência pelas células indicadas: âncora/moda/ignorar apagam a troca dentro do Nome; a cópia não retorna do empurrão externo. P-C não separa nenhum deles, pois todos permanecem com custo positivo; P-D sozinho também não separa âncora/moda/ignorar.")
    add("")
    add("## 5. Cobertura por candidata")
    add("")
    add("| candidata | âncora: custo P-A final | moda: custo P-A final | cópia: custo P-B fora | ignorar: desfaz P-B dentro | relê sem fita: fica em y | todos: P-C sem zero |")
    add("|---|---:|---:|---:|---|---|---|")
    for item in resultados:
        m = item["mecanismos"]
        add(f"| {item['candidata']} | {m['âncora na primeira']['P_A']['custo_final']} | {m['moda do histórico']['P_A']['custo_final']} | {m['cópia da última']['P_B_fora']['custo_final']} | {str(m['ignora o empurrão']['P_B_dentro']['desfaz_para_s']).lower()} | {str(m['relê a fita']['P_B_fora']['fica_empurrada']).lower()} | {str(all(m[n]['P_C']['nunca_zero'] for n in MECANISMOS)).lower()} |")
    add("")
    add("Executar `python -B simular_adversarios.py`. O script regrava `RESULTADOS_ADVERSARIOS.json` e este documento. Nenhum modelo foi executado; nada foi congelado.")
    return "\n".join(L) + "\n"


def main():
    resultados = [executar(nome) for nome in FONTES]
    assinaturas = None
    for item in resultados:
        atual = {nome: classe(r) for nome, r in item["mecanismos"].items()}
        if assinaturas is None:
            assinaturas = atual
        elif atual != assinaturas:
            raise RuntimeError(f"assinatura mudou em {item['candidata']}")
    doc = []
    for item in resultados:
        doc.append({
            "candidata": item["candidata"],
            "mecanismos": item["mecanismos"],
        })
    (FORMULA_DIR / "RESULTADOS_ADVERSARIOS.json").write_text(
        json.dumps({"candidatas": doc}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    (FORMULA_DIR / "ADVERSARIOS_K08.md").write_text(
        render(resultados), encoding="utf-8", newline="\n")
    print(json.dumps({item["candidata"]: {
        nome: {
            "P_A_final": r["P_A"]["custo_final"],
            "fora_volta_s": r["P_B_fora"]["volta_mesma_s"],
            "dentro_desfaz": r["P_B_dentro"]["desfaz_para_s"],
            "P_C_final": r["P_C"]["custo_final"],
        } for nome, r in item["mecanismos"].items()
    } for item in resultados}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
