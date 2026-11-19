"""Independent finite checks for the marked update and the two-sweep profile."""
from __future__ import annotations

import hashlib
import itertools
import json
import os
import tempfile
from collections import Counter
from fractions import Fraction
from pathlib import Path

# A signed integer has one-based magnitude internally; address zero is +/-1.
Clause = tuple[int, ...]
Formula = tuple[Clause, ...]
Assignment = tuple[bool, ...]
SOURCES = ("AtualizaONome.lean", "PerfilDeSinais.lean", "DuasPassagens.lean",
           "SegundaLeitura.lean", "GuardaDoPerfil.lean", "LeituraCertificada.lean",
           "CustoDaBuscaLiteral.lean")


def words(alphabet, max_length):
    return [word for k in range(max_length + 1) for word in itertools.product(alphabet, repeat=k)]


def holds(lit: int, assignment: Assignment) -> bool:
    return assignment[abs(lit) - 1] == (lit > 0)


def satisfies(formula: Formula, assignment: Assignment) -> bool:
    return all(any(holds(lit, assignment) for lit in clause) for clause in formula)


def literal_search(formula: Formula, marks: Clause) -> bool:
    if not formula:
        positive = {l for l in marks if l > 0}
        return all(l > 0 or -l not in positive for l in marks)
    return any(literal_search(formula[1:], (l,) + marks) for l in formula[0])


def marked_checks(prefixes, clauses, marks, literals, assignments):
    # A bit position here represents a full assignment of the test oracle only.
    agrees = {m: sum(1 << k for k, x in enumerate(assignments)
                     if all(holds(l, x) for l in m)) for m in marks}
    marked = 0
    search_calls = 0
    tests_by_mark_count = Counter()
    for p in prefixes:
        pair_values = {m: {l: literal_search(p, (l,) + m) for l in literals} for m in marks}
        search_calls += len(marks) * len(literals)
        for c in clauses:
            # Re-evaluate the entire extended formula from scratch, independently of the update.
            models = sum(1 << k for k, x in enumerate(assignments) if satisfies(p + (c,), x))
            for m, row in pair_values.items():
                from_update = any(row[lit] for lit in c)
                from_oracle = bool(models & agrees[m])
                if from_update != from_oracle:
                    raise AssertionError((p, c, m, from_update, from_oracle))
                marked += from_update
                tests_by_mark_count[len(m)] += 1
    return {"comparacoes": sum(tests_by_mark_count.values()), "por_numero_de_marcas": tests_by_mark_count,
            "verdadeiras": marked, "consultas_ao_produtor_por_escolha_literal": search_calls}


def encode(formula: Formula) -> str:
    return "".join("".join("." * (abs(lit) - 1) + ("+" if lit > 0 else "-")
                           for lit in clause) + "|" for clause in formula)


def covers_by_occurrence(formula: Formula) -> bool:
    forced = {abs(c[0]) for c in formula if len(c) == 1}
    lits = {l for c in formula for l in c}
    return all(l == 1 or -l not in lits or l in forced for l in lits if l > 0)


def sweep_reader(formula: Formula):
    tape = encode(formula)
    bank = [[False] * 4]
    input_head = work_head = 0
    moves = [0, 0, 0, 0, 0]  # input1, work1, input rewind, input2, work2
    accepted = True
    completed = [True, True]
    for phase, input_slot, work_slot in [(1, 0, 1), (2, 3, 4)]:
        first = True
        current = [False, False]
        while input_head < len(tape):
            symbol = tape[input_head]
            input_head += 1
            moves[input_slot] += 1
            if symbol == ".":
                work_head += 1
                moves[work_slot] += 1
                if work_head == len(bank):
                    bank.append([False] * 4)
            elif symbol == "|":
                if phase == 2:
                    completed = [a and b for a, b in zip(completed, current)]
                    current = [False, False]
                first = True
            else:
                positive = symbol == "+"
                flags = bank[work_head]
                if phase == 1:
                    flags[0 if positive else 1] = True
                    if first and input_head < len(tape) and tape[input_head] == "|":
                        flags[2 if positive else 3] = True
                else:
                    seen_pos, seen_neg, unit_pos, unit_neg = flags
                    picked = unit_pos or (not unit_neg and seen_pos)
                    if work_head != 0:
                        accepted &= unit_pos or unit_neg or not (seen_pos and seen_neg)
                    for i, b in enumerate((False, True)):
                        current[i] |= (b if work_head == 0 else picked) == positive
                first = False
                while work_head:
                    work_head -= 1
                    moves[work_slot] += 1
        if phase == 1:
            while input_head:
                input_head -= 1
                moves[2] += 1
    return {"classe": accepted, "bits_lidos": completed, "L": len(tape),
            "movimentos": sum(moves), "movimentos_por_fase": moves}


def profile_check(formula, assignments):
    result = sweep_reader(formula)
    models = [x for x in assignments if satisfies(formula, x)]
    exact = [any(x[0] == b for x in models) for b in (False, True)]
    observed = result["bits_lidos"]
    covers = result["classe"]
    L = result["L"]
    ticks = sum(abs(lit) - 1 for c in formula for lit in c)
    expected_counts = [L, 2 * ticks, L, L, 2 * ticks]
    assert result["movimentos_por_fase"] == expected_counts and result["movimentos"] <= 7 * L
    assert covers == covers_by_occurrence(formula)
    assert all(not seen or branch for seen, branch in zip(observed, exact))
    assert not covers or observed == exact
    return result, exact


def delayed_search_check(k):
    """Count the leaves reached by the actual first-success order."""
    formula = ((2, 3),) * k + ((-2, 4), (-2, -4))
    result, exact = profile_check(formula, tuple(itertools.product((False, True), repeat=4)))

    def visit(index, marks):
        if index == len(formula):
            return literal_search((), marks), 1
        leaves = 0
        for literal in formula[index]:
            hit, count = visit(index + 1, marks + (literal,))
            leaves += count
            if hit:
                return True, leaves
        return False, leaves

    runs = [visit(0, (mark,)) for mark in (-1, 1)]
    assert exact == [True, True] and result["bits_lidos"] == [False, False]
    assert not result["classe"] and result["L"] == 6 * k + 14
    assert all(hit and leaves >= 2**k for hit, leaves in runs)
    return {**result, "k": k, "bits_oraculo": exact, "folhas_por_ramo": [r[1] for r in runs]}


def main():
    if not __debug__:
        raise RuntimeError("Assertions must be enabled")
    literals = tuple(i * sign for i in range(1, 4) for sign in (-1, 1))
    assignments = tuple(itertools.product((False, True), repeat=3))
    clauses = words(literals, 2)
    prefixes = words(clauses, 2)
    transitions = marked_checks(prefixes, clauses, words(literals, 2), literals, assignments)
    counts = Counter()
    totals = [0] * 5
    highest = Fraction(0)
    categories = Counter()
    for p in prefixes:
        r, exact = profile_check(p, assignments)
        counts["formulas"] += 1
        counts["dentro_da_classe"] += r["classe"]
        counts["fora_da_classe"] += not r["classe"]
        counts["bits_comparados"] += 2
        counts["bits_verdadeiros_reconhecidos"] += sum(r["bits_lidos"])
        counts["bits_verdadeiros_oraculo"] += sum(exact)
        counts["formulas_com_algum_bit_perdido_fora_da_classe"] += r["bits_lidos"] != exact
        counts["formulas_sat_com_dois_bits_lidos_falsos"] += any(exact) and not any(r["bits_lidos"])
        categories["".join(str(int(b)) for b in r["bits_lidos"])] += 1
        totals = [x + y for x, y in zip(totals, r["movimentos_por_fase"])]
        if r["L"]:
            highest = max(highest, Fraction(r["movimentos"], r["L"]))
    examples = {}
    for label, p in {"formula_vazia": (), "clausula_vazia": ((),),
                     "misto_satisfazivel": ((2, 3), (-2, -3)),
                     "igualdade_com_y": ((-1, 2), (1, -2), (2,)),
                     "desigualdade_com_y": ((1, 2), (-1, -2), (2,)),
                     "duas_unitarias_opostas": ((2,), (-2,))}.items():
        r, exact = profile_check(p, assignments)
        examples[label] = {**r, "bits_oraculo": exact, "fita": encode(p)}
    assert examples["misto_satisfazivel"]["bits_oraculo"] == [True, True]
    assert examples["misto_satisfazivel"]["bits_lidos"] == [False, False]
    for label, pair in (("igualdade_com_y", [False, True]), ("desigualdade_com_y", [True, False])):
        assert examples[label]["bits_lidos"] == pair and examples[label]["classe"]
        assert examples[label]["movimentos"] == 45 and examples[label]["L"] == 11
    # A single positive singleton at unary address 128. The pivot is free.
    # Analytic oracle: extend either pivot value by setting address 128 true.
    long_address = sweep_reader(((129,),))
    assert long_address["classe"] and long_address["bits_lidos"] == [True, True]
    assert long_address["movimentos_por_fase"] == [130, 256, 130, 130, 256]
    root = Path(__file__).resolve().parent
    report = {"status": "PASS", "escopo": "Controles finitos por oráculo. As enumerações de atribuições são exclusivas do teste.",
              "dominio": {"variaveis": 3, "pivo_perfil": 0, "ordem_bits": [False, True],
                          "atribuicoes_por_formula": len(assignments), "literais": len(literals),
                          "clausulas_ordenadas_com_0_a_2_literais": len(clauses),
                          "prefixos_ordenados_com_0_a_2_clausulas": len(prefixes),
                          "pares_prefixo_proxima_clausula": len(prefixes)*len(clauses),
                          "listas_ordenadas_de_0_a_2_marcas": len(words(literals, 2)),
                          "sinais_repeticoes_e_marcas_contraditorias": True},
              "transicoes_marcadas": transitions, "perfil": dict(counts),
              "pares_lidos_00_01_10_11": categories,
              "ordem_movimentos": ["entrada_ida_1", "trabalho_1", "entrada_retorno", "entrada_ida_2", "trabalho_2"],
              "movimentos_acumulados_por_fase": totals, "maior_razao_movimentos_L_no_dominio": str(highest),
              "limite_conferido": "7L movimentos das duas cabeças para todo caso testado, incluindo retorno. Sem custo de preparação do oráculo atribuído ao leitor.",
              "exemplos": examples, "endereco_unario_128_com_oraculo_analitico": long_address,
              "familia_satisfazivel_com_busca": [delayed_search_check(k) for k in (1, 5, 10)],
              "sha256_fonte_do_controle": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "sha256_fontes_lean_na_execucao": {name: hashlib.sha256((root/name).read_bytes()).hexdigest() for name in SOURCES}}
    dest = root / "controle_finito.json"
    data = (json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    if dest.exists() and dest.read_bytes() == data:
        print(dest)
        return
    with tempfile.NamedTemporaryFile("wb", dir=root, delete=False) as handle:
        tmp = Path(handle.name)
        handle.write(data)
    if tmp.read_bytes() != data:
        raise RuntimeError("Temporary receipt differs")
    os.replace(tmp, dest)
    print(dest)


if __name__ == "__main__":
    main()

