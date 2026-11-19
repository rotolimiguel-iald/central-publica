"""Independent finite checks of sparse tape moves and shared literal labels."""
from itertools import combinations, product
from pathlib import Path
import json


def positive_heads(clause):
    return [i for i, positive in clause if positive]


def horn_inputs(cnf):
    alternatives = [positive_heads(c) or [None] for c in cnf]
    bodies = [[i for i, positive in c if not positive] for c in cnf]
    for selected in product(*alternatives):
        yield list(zip(bodies, selected))


def encode(rules):
    result = []
    for body, head in rules:
        for i in body:
            result.extend("+" * i + "?")
        result.extend("!" if head is None else "+" * head + "=")
    return "".join(result)


def machine(text):
    # A finite controller. Input head p, work head j. Blank work cells mean false.
    p = j = ticks = travel = returns = 0
    work = set()
    mode, active, changed, bad = "scan", True, False, False
    limit = (len(text) + 1) * (3 * len(text) + 2)
    while mode != "halt":
        old_p, old_j = p, j
        if mode == "home":
            if j:
                j -= 1
            else:
                mode = "scan"
        elif mode == "back":
            if p:
                p -= 1
            else:
                returns += 1
                mode, active, changed, bad = "scan", True, False, False
        elif p == len(text):
            mode = "back" if changed else "halt"
        else:
            symbol = text[p]
            p += 1
            if symbol == "+":
                j += 1
            elif symbol == "?":
                mode, active = "home", active and j in work
            elif symbol == "=":
                if active and j not in work:
                    changed = True
                    work.add(j)
                mode, active = "home", True
            elif symbol == "!":
                active, bad = True, bad or active
            else:
                raise ValueError(symbol)
        assert abs(old_p - p) <= 1 and abs(old_j - j) <= 1
        ticks += 1
        travel += abs(old_p - p) + abs(old_j - j)
        assert ticks <= limit and travel <= 2 * ticks
    return (not bad), ticks, travel, returns


def reference(cnf, n):
    return any(all(any(x[i] == sign for i, sign in c) for c in cnf)
               for x in product((False, True), repeat=n))


def controls():
    n = 3
    literals = list(product(range(n), (False, True)))
    clauses = [()] + [(l,) for l in literals] + list(combinations(literals, 2))
    clauses.extend(tuple(enumerate(signs)) for signs in product((False, True), repeat=n))
    # Additional case makes the same variable occur twice with the same sign.
    clauses.append(((1, True), (1, True)))
    inputs = [p for m in range(3) for p in product(clauses, repeat=m)]
    # Reverse-ordered implications demand more than one layer of propagation.
    inputs.append((((2, False), (0, True)), ((1, False), (2, True)), ((1, True),), ((0, False),)))
    inputs.append((((0, True), (1, True)), ((0, False),)))
    counts = {"cnfs": 0, "horn_selections_checked": 0, "sat": 0, "unsat": 0,
              "max_rewinds": 0, "max_observed_input_plus_work_moves": 0}
    for p in inputs:
        answers = []
        for rules in horn_inputs(p):
            ans, ticks, moves, rewinds = machine(encode(rules))
            horn_cnf = [[(i, False) for i in body] + ([(head, True)] if head is not None else [])
                        for body, head in rules]
            assert ans == reference(horn_cnf, n), (p, rules)
            answers.append(ans)
            counts["horn_selections_checked"] += 1
            counts["max_rewinds"] = max(counts["max_rewinds"], rewinds)
            counts["max_observed_input_plus_work_moves"] = max(
                counts["max_observed_input_plus_work_moves"], moves)
        expected = reference(p, n)
        assert any(answers) == expected
        counts["cnfs"] += 1
        counts["sat" if expected else "unsat"] += 1
    return counts


if __name__ == "__main__":
    report = controls()
    payload = (json.dumps(report, indent=2) + "\n").encode()
    target = Path(__file__).with_name("CONTROLE_FITA.json")
    if target.exists():
        assert target.read_bytes() == payload
    else:
        with target.open("xb") as f:
            f.write(payload)
    print(report)
