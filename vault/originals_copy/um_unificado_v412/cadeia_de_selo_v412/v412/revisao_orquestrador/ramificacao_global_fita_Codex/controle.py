"""Small independent oracle for the two polarity branches and the explicit formula plan."""
from itertools import product
import json
from random import Random


def passes(formula, assignment):
    return all(any(assignment[i] == sign for i, sign in clause) for clause in formula)


def truth(formula, n):
    return any(passes(formula, x) for x in product((False, True), repeat=n))


def restrict(formula, i, value):
    return [tuple(lit for lit in clause if lit[0] != i) for clause in formula
            if (i, value) not in clause]


def pivots(formula):
    raw = [i for clause in formula for i in [j for j, sign in clause if sign][1:]]
    # Lean List.dedup keeps the last occurrence.
    return tuple(reversed(dict.fromkeys(reversed(raw))))


def horn(formula):
    rules = []
    for clause in formula:
        pos = [j for j, value in clause if value]
        if len(pos) > 1:
            return None
        rules.append(([j for j, value in clause if not value], pos))
    known = set()
    while True:
        previous = len(known)
        for body, head in rules:
            if all(x in known for x in body):
                if not head:
                    return False
                known.update(head)
        if len(known) == previous:
            return True


def run(formula, plan):
    if not plan:
        answer = horn(formula)
        assert answer is not None
        return answer, 1
    j, *tail = plan
    a, left = run(restrict(formula, j, False), tail)
    b, right = run(restrict(formula, j, True), tail)
    return a or b, left + right


def plain_length(formula):
    return sum(1 + sum(i + 1 for i, _ in clause) for clause in formula)


def fast(formula):
    quartet = set()
    all_true = True
    for clause in formula:
        all_true &= any(value for _, value in clause)
        if len(clause) == 2 and {i for i, _ in clause} == {0, 1}:
            quartet.add(tuple(value for _, value in sorted(clause)))
    if len(quartet) == 4:
        return False
    return True if all_true else None


def check(formula, n):
    expected = truth(formula, n)
    ids = pivots(formula)
    assert run(formula, ids) == (expected, 2**len(ids))
    fast_answer = fast(formula)
    assert fast_answer is None or fast_answer == expected
    for j in range(n):
        for value in (False, True):
            residual = restrict(formula, j, value)
            assert plain_length(residual) <= plain_length(formula)
            for a in product((False, True), repeat=n):
                changed = a[:j] + (value,) + a[j+1:]
                assert passes(residual, a) == passes(formula, changed)


def main():
    lit = tuple(product(range(2), (False, True)))
    clauses = ((),) + tuple(product(lit, repeat=1)) + tuple(product(lit, repeat=2))
    total = 0
    for count in range(3):
        for f in product(clauses, repeat=count):
            check(f, 2)
            total += 1
    rng = Random(18)
    for _ in range(600):
        n = rng.randrange(1, 6)
        f = [tuple((rng.randrange(n), bool(rng.getrandbits(1))) for _ in range(rng.randrange(6)))
             for _ in range(rng.randrange(8))]
        check(f, n)
    pairs = []
    coupled_examples = []
    for m in range(11):
        disjoint = [((i, True), (m+i, True)) for i in range(m)]
        answer, visits = run(disjoint, pivots(disjoint))
        assert answer and fast(disjoint) is True and visits == 2**m and plain_length(disjoint) == 2*m*(m+1)
        pairs.append(dict(pairs=m, unary_letters=plain_length(disjoint), leaf_visits=visits))
        if m:
            coupled = [tuple((i, False) for i in range(m)), *disjoint]
            assert fast(coupled) is None and run(coupled, pivots(coupled)) == (True, 2**m)
            assert passes(coupled, [False]*m + [True]*m)
            coupled_examples.append(dict(pairs=m, unary_letters=plain_length(coupled), leaf_visits=2**m))
    print(json.dumps(dict(exhaustive_two_variables=total, seeded_extra=600, seed=18,
                          disjoint_examples=pairs, coupled_examples=coupled_examples), indent=2))


if __name__ == "__main__":
    main()

