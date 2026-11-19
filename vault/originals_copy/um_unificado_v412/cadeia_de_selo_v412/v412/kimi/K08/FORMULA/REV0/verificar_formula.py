#!/usr/bin/env python3
"""Constrói fórmulas/isomorfos/controles e prova SAT, redundância e Hamming.

Não chama modelo, não abre resultado experimental e não usa material reservado.
Toda saída fica em K08/FORMULA ou K08/ENTRADA.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from dataclasses import dataclass
from pathlib import Path

from catalogo_assercoes import (
    ATOMOS,
    ENTRADA_DIR,
    FONTES,
    FORMULA_DIR,
    linhas_fonte,
    texto_compacto,
)

NEGACAO_BETA = "A igualdade β_TGL = α·√e é falsa."


@dataclass(frozen=True)
class Clausula:
    cid: str
    lits: tuple[int, ...]
    tipo: str
    linha: int
    ancora: str


@dataclass
class Formula:
    nome: str
    atomos: list[str]
    indice: dict[str, int]
    clausulas: list[Clausula]

    @property
    def n(self):
        return len(self.atomos)

    def lit(self, atomo, signo):
        return signo * self.indice[atomo]

    def custo(self, leitura):
        """Número de cláusulas violadas; leitura é tupla bool na ordem de atomos."""
        total = 0
        for cl in self.clausulas:
            if not any(leitura[abs(lit) - 1] == (lit > 0) for lit in cl.lits):
                total += 1
        return total


def construir_formula(nome, com_negacao_beta=False, isomorfo=False):
    cfg = FONTES[nome]
    usados = {"leitura_pt"}
    for a in cfg["assercoes"]:
        usados.add(a["atomo"])
    for d in cfg["derivacoes"]:
        usados.update(a for a, _ in d["literals"])
    originais = sorted(usados)
    atomos = [f"z{i:02d}" for i in range(1, len(originais) + 1)] if isomorfo else originais
    renome = dict(zip(originais, atomos))
    indice = {a: i + 1 for i, a in enumerate(atomos)}
    clausulas = []
    for a in cfg["assercoes"]:
        atomo = renome[a["atomo"]]
        clausulas.append(Clausula(a["id"], (a["signo"] * indice[atomo],), "asserção", a["linha"], a["ancora"]))
    for d in cfg["derivacoes"]:
        lits = tuple(s * indice[renome[a]] for a, s in d["literals"])
        clausulas.append(Clausula(d["id"], lits, "derivação", d["linha"], d["ancora"]))
    if com_negacao_beta:
        atomo = renome["beta_forma"]
        clausulas.append(Clausula("PC_NEG_BETA", (-indice[atomo],), "negação sintética P-C", 0, NEGACAO_BETA))
    return Formula(nome + ("_ISO" if isomorfo else "") + ("_PC" if com_negacao_beta else ""), atomos, indice, clausulas)


def _propagar(n, clausulas, atrib):
    """Propagação unitária; None indica conflito."""
    atrib = dict(atrib)
    while True:
        mudou = False
        for cl in clausulas:
            satisfeita = False
            livres = []
            for lit in cl:
                var = abs(lit)
                if var not in atrib:
                    livres.append(lit)
                elif atrib[var] == (lit > 0):
                    satisfeita = True
                    break
            if satisfeita:
                continue
            if not livres:
                return None
            if len(livres) == 1:
                lit = livres[0]
                var = abs(lit)
                val = lit > 0
                if var in atrib and atrib[var] != val:
                    return None
                if var not in atrib:
                    atrib[var] = val
                    mudou = True
        if not mudou:
            return atrib


def _todas_satisfeitas(n, clausulas, atrib):
    for cl in clausulas:
        if not any(abs(lit) in atrib and atrib[abs(lit)] == (lit > 0) for lit in cl):
            return False
    return True


def satisfazivel(n, clausulas):
    def rec(atrib):
        atrib = _propagar(n, clausulas, atrib)
        if atrib is None:
            return False
        if _todas_satisfeitas(n, clausulas, atrib):
            return True
        var = next((v for v in range(1, n + 1) if v not in atrib), None)
        if var is None:
            return False
        return rec({**atrib, var: False}) or rec({**atrib, var: True})
    return rec({})


def todas_solucoes(formula):
    """Enumera também variáveis livres; os catálogos têm só uma livre."""
    cls = [cl.lits for cl in formula.clausulas]
    sols = []

    def rec(atrib):
        atrib = _propagar(formula.n, cls, atrib)
        if atrib is None:
            return
        livres = [v for v in range(1, formula.n + 1) if v not in atrib]
        if _todas_satisfeitas(formula.n, cls, atrib) and not livres:
            sols.append(tuple(atrib[v] for v in range(1, formula.n + 1)))
            return
        if not livres:
            return
        # Ramifica primeiro quem ocorre; leitura_pt é o último ramo livre.
        ocorre = {abs(lit) for cl in cls for lit in cl}
        var = next((v for v in livres if v in ocorre), livres[0])
        rec({**atrib, var: False})
        rec({**atrib, var: True})

    rec({})
    return sols


def negacao_de_clausula(cl):
    return [(-lit,) for lit in cl]


def implica(n, clausulas, consequente):
    return not satisfazivel(n, list(clausulas) + negacao_de_clausula(consequente))


def custo_minimo_exato(formula, teto=4):
    """MaxSAT por remoção: menor k de cláusulas que basta deixar violadas.

    Como itera k desde zero e testa todos os subconjuntos, o valor encontrado é
    exato. O controle P-C tem custo um: basta violar a negação acrescentada.
    """
    cls = [cl.lits for cl in formula.clausulas]
    for k in range(teto + 1):
        for removidas in itertools.combinations(range(len(cls)), k):
            retirar = set(removidas)
            restantes = [cl for i, cl in enumerate(cls) if i not in retirar]
            if satisfazivel(formula.n, restantes):
                return k, [formula.clausulas[i].cid for i in removidas]
    raise RuntimeError(f"custo mínimo acima do teto {teto} para {formula.nome}")


def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))


def leitura_dict(formula, leitura):
    return {a: leitura[i] for i, a in enumerate(formula.atomos)}


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def gerar_controle_e_isomorfo(nome):
    ENTRADA_DIR.mkdir(parents=True, exist_ok=True)
    base = texto_compacto(nome)
    compacto_path = ENTRADA_DIR / f"CANDIDATA_{nome}.md"
    compacto_path.write_text(base, encoding="utf-8", newline="\n")
    controle_path = ENTRADA_DIR / f"CONTROLE_PC_{nome}.md"
    controle_path.write_text(base + "\n" + NEGACAO_BETA + "\n", encoding="utf-8", newline="\n")

    iso = construir_formula(nome, isomorfo=True)
    iso_pc = construir_formula(nome, com_negacao_beta=True, isomorfo=True)
    iso_doc = {
        "candidata": nome,
        "tipo": "isomorfo lógico por renomeação ordenada de átomos; não é disfarce histórico de contaminação",
        "atomos": iso.atomos,
        "clausulas": [{"id": c.cid, "lits": c.lits, "tipo": c.tipo} for c in iso.clausulas],
    }
    pc_doc = {
        "candidata": nome,
        "mesma_maquina": "construir_formula(..., com_negacao_beta=True, isomorfo=True)",
        "negacao": NEGACAO_BETA,
        "atomos": iso_pc.atomos,
        "clausulas": [{"id": c.cid, "lits": c.lits, "tipo": c.tipo} for c in iso_pc.clausulas],
    }
    (FORMULA_DIR / f"ISOMORFO_{nome}.json").write_text(
        json.dumps(iso_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    (FORMULA_DIR / f"CONTROLE_PC_{nome}.json").write_text(
        json.dumps(pc_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return compacto_path, controle_path


def analisar(nome):
    formula = construir_formula(nome)
    sols = todas_solucoes(formula)
    if len(sols) < 2:
        raise RuntimeError(f"{nome}: P-B não tem duas leituras válidas")
    idx_livre = formula.indice["leitura_pt"] - 1
    pares = [(a, b) for a in sols for b in sols if a != b and hamming(a, b) == 1 and a[idx_livre] != b[idx_livre]]
    if not pares:
        raise RuntimeError(f"{nome}: a variável PT/EN não gerou duas leituras a distância um")
    s, t = sorted(pares, key=lambda p: (p[0][idx_livre], p[1][idx_livre]))[0]

    cls = [cl.lits for cl in formula.clausulas]
    redundantes_cl = []
    for i, cl in enumerate(formula.clausulas):
        if implica(formula.n, cls[:i] + cls[i + 1:], cl.lits):
            redundantes_cl.append(cl.cid)
    redundantes_ass = []
    for i, cl in enumerate(formula.clausulas):
        if cl.tipo == "asserção" and implica(formula.n, cls[:i] + cls[i + 1:], cl.lits):
            redundantes_ass.append(cl.cid)

    distancias = [hamming(a, b) for i, a in enumerate(sols) for b in sols[i + 1:]]
    min_hamming = min(distancias) if distancias else None

    # Fora do Nome: nega a disponibilidade PT/EN efetivamente afirmada.
    idx_fora = formula.indice["artigo_pt_en"] - 1
    y = list(s)
    y[idx_fora] = not y[idx_fora]
    y = tuple(y)
    if formula.custo(y) == 0:
        raise RuntimeError(f"{nome}: empurrão externo não saiu do Nome")
    # Dentro do Nome: só muda a escolha livre de língua.
    if formula.custo(t) != 0 or hamming(s, t) != 1:
        raise RuntimeError(f"{nome}: empurrão interno inválido")

    pc = construir_formula(nome, com_negacao_beta=True)
    pc_sat = satisfazivel(pc.n, [cl.lits for cl in pc.clausulas])
    if pc_sat:
        raise RuntimeError(f"{nome}: controle P-C continua satisfazível")
    pc_custo, pc_relaxadas = custo_minimo_exato(pc)
    if pc_custo == 0:
        raise RuntimeError(f"{nome}: controle P-C tem custo zero")

    compacto_path, controle_path = gerar_controle_e_isomorfo(nome)
    iso = construir_formula(nome, isomorfo=True)
    # O isomorfo tem o mesmo número de soluções e o mesmo controle insatisfazível.
    iso_sols = todas_solucoes(iso)
    iso_pc = construir_formula(nome, com_negacao_beta=True, isomorfo=True)
    iso_pc_sat = satisfazivel(iso_pc.n, [cl.lits for cl in iso_pc.clausulas])
    if len(iso_sols) != len(sols) or iso_pc_sat:
        raise RuntimeError(f"{nome}: isomorfo não preservou SAT/UNSAT")

    return {
        "candidata": nome,
        "arquivo_publico": FONTES[nome]["arquivo"],
        "faixas": FONTES[nome]["faixas"],
        "n_assercoes": len(FONTES[nome]["assercoes"]),
        "n_derivacoes": len(FONTES[nome]["derivacoes"]),
        "n_clausulas": len(formula.clausulas),
        "n_variaveis": formula.n,
        "satisfazivel": True,
        "n_leituras_validas": len(sols),
        "variaveis_livres": ["leitura_pt"],
        "distancia_minima_hamming": min_hamming,
        "assercoes_implicadas_pelas_demais": redundantes_ass,
        "clausulas_implicadas_pelas_demais": redundantes_cl,
        "leitura_s": leitura_dict(formula, s),
        "leitura_t": leitura_dict(formula, t),
        "empurrao_fora": {
            "atomo_negado": "artigo_pt_en",
            "antes_custo": formula.custo(s),
            "depois_custo": formula.custo(y),
            "hamming_antes_depois": hamming(s, y),
            "leitura_depois": leitura_dict(formula, y),
        },
        "empurrao_dentro": {
            "atomo_trocado": "leitura_pt",
            "antes_custo": formula.custo(s),
            "depois_custo": formula.custo(t),
            "hamming_antes_depois": hamming(s, t),
        },
        "pc": {
            "satisfazivel": pc_sat,
            "custo_minimo": pc_custo,
            "clausulas_que_podem_ficar_violadas_no_minimo": pc_relaxadas,
            "isomorfo_insatisfazivel": not iso_pc_sat,
            "arquivo_controle": controle_path.name,
            "sha256_controle": sha256_bytes(controle_path.read_bytes()),
        },
        "arquivo_compacto": compacto_path.name,
        "sha256_compacto": sha256_bytes(compacto_path.read_bytes()),
        "_formula": formula,
        "_s": s,
        "_t": t,
        "_y": y,
    }


def clausula_md(formula, cl):
    def lit(l):
        atomo = formula.atomos[abs(l) - 1]
        return atomo if l > 0 else f"¬{atomo}"
    return "(" + " ∨ ".join(lit(l) for l in cl.lits) + ")"


def render_formula_md(resultados):
    linhas = []
    add = linhas.append
    add("# Fórmula do texto — K08")
    add("")
    add("## 1. Escopo e regra de extração")
    add("")
    add("As quatro candidatas são recortes verbatim em caracteres dos quatro arquivos públicos permitidos, com quebras LF e uma linha em branco entre faixas; não se afirma identidade de bytes com um corte da origem. O catálogo cobre as afirmações nucleares sobre a constante, o axioma, as leis, o artefato, o estatuto, os testes e os limites; não conta navegação, URLs, comandos, licença, contato nem histórico de custódia como fatos da teoria. **Asserção** aqui é uma cláusula unitária desse catálogo, não uma contagem de frases. Toda âncora foi conferida por script contra a linha indicada; se a âncora não for substring literal, o script falha.")
    add("")
    add("Cada átomo descreve um conteúdo da fonte. `+a` significa que o texto o afirma; `¬a` significa que o texto afirma sua negação. Não entram `Nome`, `trava`, `escala`, `empurrão` ou outro vocabulário do desenho como se fossem afirmações do texto. O Nome é definido só depois, como o conjunto das atribuições Booleanas que satisfazem todas as cláusulas.")
    add("")
    add("No `ABSTRACT`, as frases antigas são lidas sob a régua corrente, como o próprio arquivo manda; por isso a negação antiga de “proved” não foi transformada em contradição com a correção posterior. A contradição de P-C é sintética e fica fora da fonte original.")
    add("")
    add("## 2. Resultado computado")
    add("")
    add("| candidata | asserções | derivações | cláusulas | variáveis | leituras válidas | distância mínima | asserções implicadas | cláusulas implicadas |")
    add("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for r in resultados:
        add(f"| {r['candidata']} | {r['n_assercoes']} | {r['n_derivacoes']} | {r['n_clausulas']} | {r['n_variaveis']} | {r['n_leituras_validas']} | {r['distancia_minima_hamming']} | {len(r['assercoes_implicadas_pelas_demais'])} | {len(r['clausulas_implicadas_pelas_demais'])} |")
    add("")
    add("“Asserções implicadas” conta só as coordenadas unitárias recuperáveis logicamente das demais cláusulas. “Cláusulas implicadas” também inclui uma cláusula de derivação que se torna logicamente redundante quando seu consequente já é afirmado; as duas medidas não devem ser confundidas.")
    add("")
    add("## 3. P-B: duas leituras válidas em cada candidata")
    add("")
    add("A fonte afirma `artigo_pt_en`, mas não escolhe qual edição uma leitura experimental usa. `leitura_pt` é, portanto, uma variável livre: não recebe cláusula. Em todas as candidatas, `s` tem `leitura_pt = falso` e `t` difere de `s` somente por `leitura_pt = verdadeiro`; ambas têm custo zero e distância de Hamming um. A base literal é a linha de `artigo_pt_en` em cada tabela abaixo.")
    add("")
    add("| candidata | custo(s) | custo(t) | Hamming(s,t) | variável trocada |")
    add("|---|---:|---:|---:|---|")
    for r in resultados:
        add(f"| {r['candidata']} | {r['empurrao_dentro']['antes_custo']} | {r['empurrao_dentro']['depois_custo']} | {r['empurrao_dentro']['hamming_antes_depois']} | leitura_pt |")
    add("")
    add("Logo nenhuma candidata falha o requisito de duas leituras para P-B. A mesma variável livre também explica por que a distância mínima três do adendo não vale aqui.")
    add("")
    add("## 4. Cláusulas literais por candidata")
    for r in resultados:
        nome = r["candidata"]
        cfg = FONTES[nome]
        formula = r["_formula"]
        add("")
        add(f"### {nome} — `{cfg['arquivo']}`")
        add("")
        add(f"Recorte: {', '.join(f'linhas {a}–{b}' for a, b in cfg['faixas'])}. Arquivo gerado: `K08/ENTRADA/CANDIDATA_{nome}.md`.")
        add("")
        add("| ID | cláusula | o que o texto afirma | arquivo e linha | âncora literal |")
        add("|---|---|---|---|---|")
        by_id = {c.cid: c for c in formula.clausulas}
        for a in cfg["assercoes"]:
            cl = by_id[a["id"]]
            sinal = "" if a["signo"] == 1 else "NÃO: "
            descricao = ATOMOS[a["atomo"]].replace("|", "\\|")
            ancora = a["ancora"].replace("|", "\\|")
            add(f"| {a['id']} | `{clausula_md(formula, cl)}` | {sinal}{descricao} | `{cfg['arquivo']}:{a['linha']}` | “{ancora}” |")
        if cfg["derivacoes"]:
            add("")
            add("Derivações explicitamente escritas na fonte (não são fatos novos):")
            add("")
            add("| ID | cláusula | arquivo e linha | âncora literal |")
            add("|---|---|---|---|")
            for d in cfg["derivacoes"]:
                cl = by_id[d["id"]]
                ancora = d["ancora"].replace("|", "\\|")
                add(f"| {d['id']} | `{clausula_md(formula, cl)}` | `{cfg['arquivo']}:{d['linha']}` | “{ancora}” |")
        else:
            add("")
            add("Nenhuma cláusula de derivação foi acrescentada: o recorte não declara uma implicação formal entre os átomos catalogados.")
    add("")
    add("## 5. Os dois empurrões construtivos")
    add("")
    add("**Opção: edição determinística do estado devolvido, não mensagem nova do usuário.** Uma mensagem acrescentaria uma instrução ao histórico e poderia mudar a fórmula que se pretende manter fixa; a edição altera apenas a leitura. Depois do primeiro passo, a fonte não volta ao leitor. Assim, uma “volta” não pode ser explicada por releitura da fita.")
    add("")
    add("- **Fora do Nome:** em `s`, trocar `artigo_pt_en` de verdadeiro para falso. Isso nega uma asserção efetivamente afirmada pela fonte. O script verifica custo positivo.")
    add("- **Dentro do Nome:** trocar `leitura_pt` em `s`, obtendo `t`. O script verifica custo zero nas duas leituras.")
    add("")
    add("| candidata | custo após fora | Hamming fora | custo após dentro | Hamming dentro |")
    add("|---|---:|---:|---:|---:|")
    for r in resultados:
        add(f"| {r['candidata']} | {r['empurrao_fora']['depois_custo']} | {r['empurrao_fora']['hamming_antes_depois']} | {r['empurrao_dentro']['depois_custo']} | {r['empurrao_dentro']['hamming_antes_depois']} |")
    add("")
    add("Ressalva de tipos: na fórmula/configuração, o empurrão é a troca de uma coordenada, como em `NomeComoCodigo.empurrao`. Na trava vetorial, o teorema de retorno exige `δ` ortogonal ao Nome e conserva o componente em `s`; portanto não se deve identificar a substituição Booleana `s ↦ y` com o vetor `δ = y − s`. A ponte entre a saída de um modelo e o vetor de amplitudes permanece aberta, como dizem a candidata R3 e a revisão §7.")
    add("")
    add("## 6. P-C: contradição mínima e mesmo gerador")
    add("")
    add(f"O controle é o texto compacto original mais uma única frase sintética: **“{NEGACAO_BETA}”** Como toda candidata afirma `beta_forma`, a fórmula do controle é `φ ∧ ¬beta_forma`. A insatisfabilidade é testada por DPLL com propagação unitária; o custo mínimo é calculado exatamente por busca iterativa do menor número de cláusulas cuja remoção restaura SAT.")
    add("")
    add("| candidata | SAT do controle | custo mínimo | isomorfo UNSAT | SHA-256 do controle |")
    add("|---|---|---:|---|---|")
    for r in resultados:
        add(f"| {r['candidata']} | {str(r['pc']['satisfazivel']).lower()} | {r['pc']['custo_minimo']} | {str(r['pc']['isomorfo_insatisfazivel']).lower()} | `{r['pc']['sha256_controle']}` |")
    add("")
    add("O mesmo construtor gera a fórmula, o isomorfo lógico e os dois controles (original e isomorfo). O isomorfo renomeia os átomos em ordem fixa e o script verifica que preserva o número de soluções e a insatisfabilidade do controle. **Este isomorfo lógico não é apresentado como disfarce histórico de números nem como controle de contaminação.** Os arquivos `ISOMORFO_*.json` e `CONTROLE_PC_*.json` estão nesta pasta; os textos contraditórios estão em `K08/ENTRADA`.")
    add("")
    add("## 7. Redundância, fita e o limite do adendo")
    add("")
    add("| candidata | asserções unitárias implicadas pelas demais | cláusulas implicadas | distância mínima |")
    add("|---|---|---|---:|")
    for r in resultados:
        ua = ", ".join(r["assercoes_implicadas_pelas_demais"]) or "nenhuma"
        uc = ", ".join(r["clausulas_implicadas_pelas_demais"]) or "nenhuma"
        add(f"| {r['candidata']} | {ua} | {uc} | {r['distancia_minima_hamming']} |")
    add("")
    add("**Com a fita presente**, o projetor pode reescrever uma leitura válida em um passo para qualquer texto com Nome; o retorno é trivial e não distingue os textos. **Sem a fita e com apenas a configuração Booleana anterior**, uma coordenada independente não pode ser reconstruída: só as asserções implicadas pelas demais oferecem redundância lógica para isso. Isso não restringe a trava vetorial, que conserva o componente no Nome e não é um leitor de uma só configuração.")
    add("")
    add("O empurrão externo construído aqui usa `artigo_pt_en`, que não é implicado pelas demais em nenhuma candidata; portanto o leitor Booleano sem fita e sem memória adicional não tem como recuperá-lo. As derivações de `meia_nat`/`beta_forma` medidas em algumas candidatas não mudam esse caso.")
    add("")
    add("Todas as candidatas têm distância mínima um por causa da variável livre PT/EN. Logo o teorema de decodificação de `NomeComoCodigo`, que exige distância pelo menos três, **não se aplica** a elas. O fator fita-presente × fita-ausente cabe como comparação conceitual, mas, com estas fórmulas, não fornece um separador universal: o adendo exige soluções isoladas, fica parado fora da bola de raio um e não universaliza retorno. A frase “sem fita há retorno se e só se há redundância” permanece conjectura fora dessas condições.")
    add("")
    add("## 8. Reprodução e limites")
    add("")
    add("Executar `python -B verificar_formula.py` nesta pasta. O script valida as âncoras, gera os recortes/controles, prova SAT/UNSAT, mede implicação e Hamming e regrava `RESULTADOS_FORMULA.json` e este documento. As medidas de bytes/palavras/tokens e o custo por sessão estão em `K08/ENTRADA/MEDIDAS_ENTRADA.md`. Nenhum modelo foi executado; nada foi congelado.")
    return "\n".join(linhas) + "\n"


def autoteste_solver():
    """Confere DPLL contra enumeração bruta em casos pequenos conhecidos."""
    casos = [
        (1, [(1,)]),
        (1, [(1,), (-1,)]),
        (2, [(1, 2)]),
        (2, [(1,), (-1, 2)]),
        (2, []),
    ]
    for n, cls in casos:
        atomos = [f"a{i}" for i in range(1, n + 1)]
        formula = Formula(
            "AUTOTESTE",
            atomos,
            {a: i + 1 for i, a in enumerate(atomos)},
            [Clausula(f"T{i}", tuple(cl), "teste", 0, "") for i, cl in enumerate(cls)],
        )
        obtido = set(todas_solucoes(formula))
        esperado = set()
        for bits in itertools.product((False, True), repeat=n):
            if all(any(bits[abs(lit) - 1] == (lit > 0) for lit in cl) for cl in cls):
                esperado.add(bits)
        if obtido != esperado:
            raise AssertionError(f"DPLL divergiu da força bruta: {n}, {cls}")
        if satisfazivel(n, cls) != bool(esperado):
            raise AssertionError(f"SAT divergiu da força bruta: {n}, {cls}")
    contradicao = Formula("UNSAT", ["a"], {"a": 1}, [Clausula("P", (1,), "teste", 0, ""), Clausula("N", (-1,), "teste", 0, "")])
    if custo_minimo_exato(contradicao)[0] != 1:
        raise AssertionError("MaxSAT não reconheceu contradição unitária de custo um")
    if not implica(2, [(1,), (-1, 2)], (2,)):
        raise AssertionError("modus ponens não foi reconhecido")


def main():
    autoteste_solver()
    resultados = [analisar(nome) for nome in FONTES]
    publicos = []
    for r in resultados:
        publicos.append({k: v for k, v in r.items() if not k.startswith("_")})
    doc = {
        "metodo_sat": "DPLL próprio com propagação unitária e enumeração da única variável livre",
        "metodo_custo_minimo": "MaxSAT exato por remoção iterativa de subconjuntos de cláusulas",
        "resultados": publicos,
    }
    (FORMULA_DIR / "RESULTADOS_FORMULA.json").write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    (FORMULA_DIR / "FORMULA_DO_TEXTO_K08.md").write_text(
        render_formula_md(resultados), encoding="utf-8", newline="\n")
    print(json.dumps({r["candidata"]: {
        "assercoes": r["n_assercoes"],
        "solucoes": r["n_leituras_validas"],
        "hamming": r["distancia_minima_hamming"],
        "redundantes": r["assercoes_implicadas_pelas_demais"],
        "pc_custo": r["pc"]["custo_minimo"],
    } for r in resultados}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
