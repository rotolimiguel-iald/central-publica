#!/usr/bin/env python3
"""Gera ERRATA_ADVERSARIOS_K08_15nov.md a partir dos resultados correntes."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

FORMULA_DIR = Path(__file__).resolve().parent
SAIDA = FORMULA_DIR / "ERRATA_ADVERSARIOS_K08_15nov.md"
RESULTADOS = json.loads((FORMULA_DIR / "RESULTADOS_ADVERSARIOS.json").read_text(encoding="utf-8"))
FORMULAS = json.loads((FORMULA_DIR / "RESULTADOS_FORMULA.json").read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    base = next(r for r in RESULTADOS["candidatas"] if r["candidata"] == "READ_BRIEF")
    por_formula = {r["candidata"]: r for r in FORMULAS["resultados"]}
    L = []
    add = L.append
    add("# Errata — adversários K08, adendo de 15/11")
    add("")
    add("## Correção principal")
    add("")
    add("A REV0 misturava dois objetos sob “projetor”. `P_N` aplicado ao estado **não é adversário**: é o leitor na forma de chegada, cai no Nome, fixa o Nome e preserva o componente no Nome. O adversário é o **leitor sem memória determinado só pela fonte** (`fonte → leitura`), que ignora o histórico. Essa é a leitura exigida pelo adendo de 15/11.")
    add("")
    add("Na R4, a fonte não volta depois do primeiro passo. Logo o adversário sem memória fica sem regra posterior; a ponte à trava/`P_N` é inacessível como escrita. Não se substitui essa ausência por uma cópia da última leitura nem se apresenta isso como separação.")
    add("")
    add("## Divergência da âncora, resolvida")
    add("")
    add("Definição única: **a âncora devolve a primeira leitura da sessão**. Portanto E1/P-A é condicional: se a primeira leitura for inválida, ela não pousa; se a primeira já for válida, ela pousa trivialmente e retorna após um empurrão externo. A frase do MODELO (“pousa e retorna”) vale só sob a condição de primeira leitura válida; a linha antiga do ADVERSARIOS (“não pousa”) era o caso com primeira leitura inválida. As duas eram casos diferentes da mesma regra.")
    add("")
    rb = base["mecanismos"]
    add(f"Com `READ_BRIEF`: primeira leitura inválida dá custo {rb['âncora na primeira leitura']['E1_invalido']['custo_inicial']} → {rb['âncora na primeira leitura']['E1_invalido']['custo_final']}; primeira leitura válida dá custo {rb['âncora na primeira leitura']['E1_valido']['custo_final']}.")
    add("")
    add("## Tabela corrente E1–E8")
    add("")
    add("| adversário | E1 | E2 | E3 | E4 | E8 | separação |")
    add("|---|---|---|---|---|---|---|")
    add("| leitor sem memória (fonte → leitura) | custo 0 com fonte; depois inacessível | inacessível sem fonte | inacessível sem fonte | estável com fonte; depois inacessível | falha | **não separado na R4**; cotas/retorno instantâneo não bastam |")
    add("| âncora na primeira leitura | condicional | desfaz t → s | volta a s | estável | falha | **E2**, e também E8 |")
    add("| moda do histórico | condicional | desfaz t → s | volta a s | estável | falha | **E2**, e também E8 |")
    add("| cópia da última | condicional | preserva t | fica em y | estável | falha | **E3/P-D**, e também E8 |")
    add("| ignora o empurrão | condicional | desfaz t → s | volta a s | estável | falha | **E2**, e também E8 |")
    add("")
    add("E5 (não aumentar norma), E6 (lei de módulo) e E7 (pesos relativos dentro do Nome) não são medidos pela leitura Booleana atual: E5 exige norma, E6 pertence ao operador na álgebra e E7 exige estado contínuo/pesos de Born. E7 permanece como separador formal de mapas que caem no Nome por outro caminho, mas não é ponte operacional validada aqui.")
    add("")
    add("## Hamming e fórmulas")
    add("")
    add("| candidata | leituras válidas | Hamming mínimo | uso de Hamming 3 |")
    add("|---|---:|---:|---|")
    for nome, f in por_formula.items():
        add(f"| {nome} | {f['n_leituras_validas']} | {f['distancia_minima_hamming']} | não usado |")
    add("")
    add("P-C permanece o controle do Nome vazio (`P_N = 0`), com custo lógico mínimo 1 em todas as candidatas. Nenhum modelo foi executado.")
    add("")
    add("## Arquivos e hashes")
    add("")
    add("| arquivo | SHA-256 |")
    add("|---|---|")
    for rel in (
        "REV0/ADVERSARIOS_K08.md",
        "REV0/FORMULA_DO_TEXTO_K08.md",
        "ADVERSARIOS_K08.md",
        "FORMULA_DO_TEXTO_K08.md",
        "RESULTADOS_ADVERSARIOS.json",
    ):
        path = FORMULA_DIR / rel
        add(f"| `{rel}` | `{sha(path)}` |")
    add("")
    add("A versão anterior da pasta `FORMULA` está preservada em `FORMULA/REV0/`. O hash corrente desta errata consta do manifesto, não dentro do próprio texto.")
    SAIDA.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"errata": str(SAIDA), "sha256": sha(SAIDA)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
