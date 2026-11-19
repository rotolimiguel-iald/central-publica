"""Finite independent checks. Masks denote subsets of variable indices, not model states."""
import itertools
import json
from collections import Counter
from pathlib import Path


def run():
    n = 3
    worlds = range(1 << n)
    clauses = [tuple((i, value) for i, value in enumerate(pattern) if value != -1)
               for pattern in itertools.product((-1, 0, 1), repeat=n)]
    clauses.extend([((0, 0), (0, 1)), ((0, 1), (0, 1)), ((1, 0), (2, 0), (2, 1))])
    support = {c: sum(1 << i for i in {k for k, _ in c}) for c in clauses}
    passes = {c: [any((x >> i & 1) == value for i, value in c) for x in worlds] for c in clauses}
    cases = 0
    features = Counter()
    for p, c, tail in itertools.product(clauses, repeat=3):
        f = support[p] & (support[c] | support[tail])
        g = (support[p] | support[c]) & support[tail]
        bag = f | support[c]
        factor = 1 << (bag & ~f).bit_count()
        features["introducao"] += bool(bag & ~f)
        features["esquecimento"] += bool(f & ~g)
        features["introducao_e_esquecimento"] += bool(bag & ~f) and bool(f & ~g)
        features["variavel_nova_que_sai_imediatamente"] += bool(support[c] & ~support[p] & ~g)
        for q in (0, 1, 3):
            before, after, prediction = Counter(), Counter(), Counter()
            for x in worlds:
                prefix_weight = 1 if passes[p][x] else q
                before[x & f] += prefix_weight
                after[x & g] += prefix_weight * (1 if passes[c][x] else q)
            for z in worlds:
                if z & ~bag == 0:
                    prediction[z & g] += before[z & f] * (1 if passes[c][z] else q)
            assert all(factor * v == prediction[u] for u, v in after.items()), (p,c,tail,q)
            assert set(after) == set(prediction)
            cases += 1
    return {"n":n,"clausulas":len(clauses),"triplas_de_clausulas":len(clauses)**3,
            "valores_do_peso_de_violacao":[0,1,3],"transicoes_conferidas":cases,
            "caracteristicas_das_triplas":dict(features)}


if __name__ == "__main__":
    result = run()
    target = Path(__file__).with_name("CONTROLE_EXATO.json")
    payload = (json.dumps(result, ensure_ascii=False, indent=2)+"\n").encode()
    if target.exists():
        assert target.read_bytes() == payload
    else:
        with target.open("xb") as out:
            out.write(payload)
    print(json.dumps(result, ensure_ascii=False))
