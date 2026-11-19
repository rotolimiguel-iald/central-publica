#!/usr/bin/env python3
"""Mecanismos adversariais K08 após o adendo de 15/11.

`P_N` não é adversário: é o leitor na forma de chegada. O adversário sem memória
é uma função determinada só pela fonte; na R4 a fonte não volta após o primeiro
passo, portanto essa função fica sem regra posterior.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass

from catalogo_assercoes import FONTES, FORMULA_DIR
from verificar_formula import construir_formula, custo_minimo_exato, todas_solucoes


class SemFonte(RuntimeError):
    pass


@dataclass(frozen=True)
class Passo:
    leitura: tuple[bool, ...]
    evento: str


def ancora_primeira(historico, ctx):
    """Definição única: devolve a primeira leitura da sessão."""
    return historico[0].leitura


def moda_historico(historico, ctx):
    """Moda por coordenada; empate conserva o bit da primeira leitura."""
    primeira = historico[0].leitura
    saida = []
    for j in range(len(primeira)):
        votos = sum(h.leitura[j] for h in historico)
        saida.append(primeira[j] if 2 * votos == len(historico) else 2 * votos > len(historico))
    return tuple(saida)


def copia_ultima(historico, ctx):
    return historico[-1].leitura


def ignora_empurrao(historico, ctx):
    for h in reversed(historico):
        if not h.evento.startswith("empurrao"):
            return h.leitura
    return historico[0].leitura


def leitor_sem_memoria_dado_pela_fonte(historico, ctx):
    """fonte → leitura, ignorando o histórico; sem fonte não há regra."""
    if not ctx.get("fonte_disponivel"):
        raise SemFonte("a R4 não devolve a fonte depois do primeiro passo")
    solucao = ctx.get("solucao_fonte")
    if solucao is None:
        raise SemFonte("a fonte não tem Nome")
    return solucao


MECANISMOS = {
    "leitor sem memória (fonte → leitura)": leitor_sem_memoria_dado_pela_fonte,
    "âncora na primeira leitura": ancora_primeira,
    "moda do histórico": moda_historico,
    "cópia da última": copia_ultima,
    "ignora o empurrão": ignora_empurrao,
}

MEMORIA = tuple(MECANISMOS)[1:]


def virar(leitura, indice):
    out = list(leitura)
    out[indice] = not out[indice]
    return tuple(out)


def aplicar(historico, mecanismo, formula, solucao_fonte=None, fonte=False):
    ctx = {
        "formula": formula,
        "fonte_disponivel": fonte,
        "solucao_fonte": solucao_fonte,
    }
    out = mecanismo(historico, ctx)
    if len(out) != formula.n or not all(isinstance(v, bool) for v in out):
        raise TypeError("mecanismo não devolveu uma leitura Booleana completa")
    return historico + [Passo(out, "leitura")]


def rodar_desde(mecanismo, formula, x0, passos, solucao_fonte=None, fonte_no_primeiro=False):
    h = [Passo(x0, "primeira_leitura")]
    custos = []
    for k in range(passos):
        h = aplicar(h, mecanismo, formula, solucao_fonte, fonte=(fonte_no_primeiro and k == 0))
        custos.append(formula.custo(h[-1].leitura))
    zeros = [i for i, c in enumerate(custos) if c == 0]
    return {
        "custos": custos,
        "custo_inicial": custos[0],
        "custo_final": custos[-1],
        "pousa_e_permanece": bool(zeros) and all(c == 0 for c in custos[zeros[0]:]),
    }


def empurrar_e_ler(mecanismo, formula, antes, depois, solucao_fonte=None):
    h = [Passo(antes, "primeira_leitura"), Passo(depois, "empurrao")]
    h = aplicar(h, mecanismo, formula, solucao_fonte, fonte=False)
    out = h[-1].leitura
    return {
        "custo_final": formula.custo(out),
        "volta_ao_anterior": out == antes,
        "preserva_empurrada": out == depois,
    }


def e4_estavel(mecanismo, formula, s):
    h = [Passo(s, "primeira_leitura")]
    h1 = aplicar(h, mecanismo, formula)
    h2 = aplicar(h1, mecanismo, formula)
    return h2[-1].leitura == h1[-1].leitura


def executar(nome):
    formula = construir_formula(nome)
    sols = todas_solucoes(formula)
    idx_livre = formula.indice["leitura_pt"] - 1
    s = next(x for x in sols if not x[idx_livre])
    t = next(x for x in sols if x[idx_livre] and x != s)
    y = virar(s, formula.indice["artigo_pt_en"] - 1)
    invalida = tuple(False for _ in formula.atomos)
    pc = construir_formula(nome, com_negacao_beta=True)
    if todas_solucoes(pc):
        raise RuntimeError("P-C deveria ser insatisfazível")
    pc_custo_minimo = custo_minimo_exato(pc)[0]
    resultados = {}

    for rotulo in MEMORIA:
        mecanismo = MECANISMOS[rotulo]
        e1_invalido = rodar_desde(mecanismo, formula, invalida, len(formula.clausulas) + 2)
        e1_valido = rodar_desde(mecanismo, formula, s, 3)
        resultados[rotulo] = {
            "E1_invalido": e1_invalido,
            "E1_valido": e1_valido,
            "E2": empurrar_e_ler(mecanismo, formula, s, t),
            "E3": empurrar_e_ler(mecanismo, formula, s, y),
            "E4": e4_estavel(mecanismo, formula, s),
            "E5": "não medido: a leitura Booleana não devolve norma",
            "E6": "não medido: a lei de módulo pertence ao operador na álgebra",
            "E7": "não medido: exige pesos de Born/estado contínuo, não só uma configuração",
            "E8": "falha por construção: salto/constância, não decaimento exponencial",
            "P_C": rodar_desde(mecanismo, pc, invalida, len(pc.clausulas) + 2),
            "P_D": empurrar_e_ler(mecanismo, formula, s, y),
        }

    # O adversário sem memória só é definido enquanto a fonte está disponível.
    rotulo = "leitor sem memória (fonte → leitura)"
    mecanismo = MECANISMOS[rotulo]
    h = [Passo(invalida, "primeira_leitura")]
    h = aplicar(h, mecanismo, formula, s, fonte=True)
    primeira = h[-1].leitura
    try:
        aplicar(h, mecanismo, formula, s, fonte=False)
        raise RuntimeError("o adversário sem memória deveria ficar sem regra sem fonte")
    except SemFonte:
        sem_regra = True
    resultados[rotulo] = {
        "E1_primeira_leitura": {"custo": formula.custo(primeira), "pousa": formula.custo(primeira) == 0},
        "E1_depois_do_primeiro_passo": "inacessível na R4; a fonte não volta",
        "E2_R4": "inacessível na R4; sem fonte não há regra posterior",
        "E3_R4": "inacessível na R4; sem fonte não há regra posterior",
        "E4_com_fonte": True,
        "E4_R4_depois_do_primeiro_passo": "inacessível",
        "E5": "não medido: a leitura Booleana não devolve norma",
        "E6": "não medido: a lei de módulo pertence ao operador na álgebra",
        "E7_contrafactual_com_fonte": "falha: ignora o ponto de partida dentro do Nome",
        "E8": "falha: chegada instantânea determinada pela fonte, não perfil exponencial",
        "P_C": {"sem_leitura": True, "custo_minimo": pc_custo_minimo},
        "P_D_R4": "inacessível; sem fonte não há regra posterior",
        "sem_regra_sem_fonte": sem_regra,
    }
    return {
        "candidata": nome,
        "s": s,
        "t": t,
        "y": y,
        "formula": formula,
        "distancia_minima_hamming": 1,
        "mecanismos": resultados,
    }


def celula_e1(r):
    if "E1_invalido" not in r:
        return f"fonte → custo {r['E1_primeira_leitura']['custo']}; depois: inacessível"
    inv = r["E1_invalido"]
    val = r["E1_valido"]
    return f"condicional: inválida {inv['custo_inicial']}→{inv['custo_final']}; válida {val['custo_final']}"


def celula_e2(r):
    if "E2_R4" in r:
        return "inacessível sem fonte"
    return "preserva t" if r["E2"]["preserva_empurrada"] else "desfaz t → s"


def celula_e3(r):
    if "E3_R4" in r:
        return "inacessível sem fonte"
    return "volta a s" if r["E3"]["volta_ao_anterior"] else "fica em y"


def celula_e4(r):
    if "E4_R4_depois_do_primeiro_passo" in r:
        return "com fonte: estável; depois: inacessível"
    return "estável" if r["E4"] else "muda na releitura"


def celula_pc(r):
    if "sem_leitura" in r["P_C"]:
        return f"sem leitura; custo mínimo {r['P_C']['custo_minimo']}"
    return f"nunca zero; final {r['P_C']['custo_final']}" if r["P_C"]["custo_final"] > 0 else "atinge zero"


def celula_pd(r):
    if "P_D_R4" in r:
        return "inacessível sem fonte"
    return "fica em y" if r["P_D"]["preserva_empurrada"] else "volta a s"


SEPARACAO = {
    "leitor sem memória (fonte → leitura)": "não separado na R4; com fonte, E2/E7 falhariam e E8 falha, mas essa ponte é inacessível como escrita",
    "âncora na primeira leitura": "E2: apaga a troca válida; E8: não tem perfil exponencial. E1 é condicional à primeira leitura",
    "moda do histórico": "E2: a moda apaga t; E8: não tem perfil exponencial",
    "cópia da última": "E3/P-D: não anula o empurrão externo; E8: não tem perfil exponencial",
    "ignora o empurrão": "E2: apaga a troca válida; E8: não tem perfil exponencial",
}


def render(resultados):
    base = next(r for r in resultados if r["candidata"] == "READ_BRIEF")
    L = []
    add = L.append
    add("# Adversários — K08")
    add("")
    add("## 1. Correção do objeto")
    add("")
    add("**`P_N`, o projetor ortogonal sobre o Nome, não é adversário.** Ele é o leitor na forma de chegada: cai no Nome, fixa o Nome, anula o componente ortogonal e preserva o componente no Nome (`P_N(s + δ) = s + P_Nδ`). A trava é o caminho em tempo finito; a seleção é a face no estado renormalizado.")
    add("")
    add("O adversário correto é o **leitor sem memória determinado só pela fonte**: `fonte → leitura`, ignorando o histórico e o ponto de partida dentro do Nome. Como a R4 não devolve a fonte depois do primeiro passo, esse adversário fica sem regra posterior; eu não o degrado a uma cópia nem finjo separação.")
    add("")
    add("O leitor de referência é definido uma vez: **nos vetores, `P_N`; no estado, a seleção renormalizada; em tempo finito, a trava**. O operador do Nome na álgebra e o `LeitorDeUmaConfiguracao` são faces/hipóteses adjacentes, não o mesmo portador.")
    add("")
    add("## 2. Definições dos mecanismos")
    add("")
    add("- **Âncora:** devolve a primeira leitura da sessão. Esta é a definição única usada abaixo; não há uma variante separada que pouse por construção.")
    add("- **Moda:** moda por coordenada; em empate, conserva o bit da primeira leitura.")
    add("- **Cópia:** devolve a última leitura.")
    add("- **Ignora o empurrão:** devolve a última leitura que não é um empurrão.")
    add("- **Sem memória:** devolve uma solução determinística da fonte enquanto ela está disponível; sem fonte, lança `SemFonte`. Nenhum modelo participa.")
    add("")
    add("Os empurrões são edições do estado devolvido. A fonte entra só no primeiro passo; depois disso nenhum adversário a recebe.")
    add("")
    add("## 3. E1–E8 e portadores")
    add("")
    add("| previsão | conteúdo | portador formal | medida aqui |")
    add("|---|---|---|---|")
    add("| E1 | cai no Nome (P-A) | `P_N`; no estado, seleção | custo da leitura Booleana |")
    add("| E2 | fixa o Nome; componente dentro do Nome fica | `P_N` | P-B dentro |")
    add("| E3 | anula o que é cego ao Nome | `P_N`; limite da trava | P-B fora |")
    add("| E4 | reler não acrescenta | idempotência de `P_N` | aplicar o mecanismo duas vezes |")
    add("| E5 | não aumenta a norma | `P_N` | **não medido**: a leitura Booleana não devolve norma |")
    add("| E6 | lei de módulo | operador do Nome na álgebra | **não medido**: outro portador |")
    add("| E7 | pesos relativos dentro do Nome não mudam | seleção, com pesos de Born | **não medido**: exige estado contínuo |")
    add("| E8 | perfil exponencial, nunca exato em tempo finito | trava | assinatura de perfil, não ponte validada |")
    add("")
    add("As previsões primárias da releitura são E2 e E4; a fidelidade também exige E5, que este protocolo Booleano não mede. E3 e E7 são controles; E8 é o perfil da trava. A unicidade E1+E2+E5+linearidade não é testada, porque a linearidade do sistema real não é assumida.")
    add("")
    add("## 4. Tabela calculada")
    add("")
    add("Custos numéricos de `READ_BRIEF`; as assinaturas são as mesmas nas quatro candidatas. `s` e `t` são válidas, `y` nega uma asserção. A âncora é condicional à primeira leitura: se ela for inválida, não pousa; se já for válida, E1 é trivial e o retorno E3 não é evidência.")
    add("")
    add("| adversário | E1/P-A | E2/P-B dentro | E3/P-B fora | E4 | E8 | P-C | P-D | separação |")
    add("|---|---|---|---|---|---|---|---|---|")
    for nome in MECANISMOS:
        r = base["mecanismos"][nome]
        add(f"| {nome} | {celula_e1(r)} | {celula_e2(r)} | {celula_e3(r)} | {celula_e4(r)} | falha | {celula_pc(r)} | {celula_pd(r)} | {SEPARACAO[nome]} |")
    add("")
    add("Referência: `P_N` resolve instantaneamente E1–E4 e é contrativo; a trava tem E8 e aproxima `P_N` sem chegar exatamente em tempo finito. O leitor sem memória cumpre cotas superiores e retorno instantâneo quando a fonte está presente, mas isso não é a trava; faltam E2/E7 e o perfil. Na R4, porém, a fonte não volta, logo essa comparação fica **inacessível como escrita**.")
    add("")
    add("## 5. Perfil de referência")
    add("")
    add("Com `τ = 1` apenas como unidade de exibição, a amplitude residual é `e^(−kτc)`. Custos maiores decaem mais depressa e nenhum decaimento é exato em `k` finito. Isto é a assinatura formal da trava, não uma trajetória de modelo nem uma ponte operacional validada.")
    add("")
    add("| ciclo k | custo 1: e^(−k) | custo 2: e^(−2k) |")
    add("|---:|---:|---:|")
    for k in range(5):
        add(f"| {k} | {math.exp(-k):.12g} | {math.exp(-2*k):.12g} |")
    add("")
    add("## 6. Controles, Hamming e bloqueio")
    add("")
    add("P-C permanece o controle do Nome vazio (`P_N = 0`): não há leitura válida e o custo mínimo é positivo. P-D permanece o controle da identidade/sem escala. Todas as fórmulas têm distância mínima de Hamming 1 por causa da variável livre PT/EN; **Hamming 3 não é usado**.")
    add("")
    add("**Bloqueio:** o leitor sem memória não é separado pelas cotas superiores, pelo pouso instantâneo ou pelo retorno instantâneo. Só E8 e a memória do componente o separariam; E7 também falharia com fonte presente. Como a R4 proíbe a volta da fonte e ainda não há ponte operacional validada para perfil/pesos, declaro a separação experimental desse adversário **não fechada**.")
    add("")
    add("Âncora, moda e ignorar são separados por E2; a cópia por E3/P-D; todos os quatro também falham E8. P-C não separa esses adversários, porque todos ficam sem custo zero.")
    add("")
    add("## 7. Cobertura por candidata")
    add("")
    add("| candidata | âncora: E1 inválida final | moda: E1 inválida final | cópia: E3 custo | ignorar: E2 preserva t | sem memória sem fonte |")
    add("|---|---:|---:|---:|---|---|")
    for item in resultados:
        m = item["mecanismos"]
        add(f"| {item['candidata']} | {m['âncora na primeira leitura']['E1_invalido']['custo_final']} | {m['moda do histórico']['E1_invalido']['custo_final']} | {m['cópia da última']['E3']['custo_final']} | {str(m['ignora o empurrão']['E2']['preserva_empurrada']).lower()} | {str(m['leitor sem memória (fonte → leitura)']['sem_regra_sem_fonte']).lower()} |")
    add("")
    add("Executar `python -B simular_adversarios.py`. O script regrava `RESULTADOS_ADVERSARIOS.json` e este documento. Nenhum modelo foi executado; nada foi congelado.")
    return "\n".join(L) + "\n"


def main():
    resultados = [executar(nome) for nome in FONTES]
    doc = []
    for item in resultados:
        doc.append({
            "candidata": item["candidata"],
            "distancia_minima_hamming": item["distancia_minima_hamming"],
            "mecanismos": item["mecanismos"],
        })
    (FORMULA_DIR / "RESULTADOS_ADVERSARIOS.json").write_text(
        json.dumps({"candidatas": doc}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    (FORMULA_DIR / "ADVERSARIOS_K08.md").write_text(
        render(resultados), encoding="utf-8", newline="\n")
    print(json.dumps({item["candidata"]: {
        nome: (r["E1_invalido"]["custo_final"] if "E1_invalido" in r else r["E1_primeira_leitura"]["custo"])
        for nome, r in item["mecanismos"].items()
    } for item in resultados}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
