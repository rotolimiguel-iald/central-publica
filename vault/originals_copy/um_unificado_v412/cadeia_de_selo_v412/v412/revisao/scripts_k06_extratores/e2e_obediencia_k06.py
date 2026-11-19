"""Ponta a ponta com as copias: texto K06R1 -> extratores.py -> medir_ponto_fixo_comum.py.
Leitor SEM MEMORIA (funcao so de (u, Q_k)): como G reapresenta o corpus u em toda chamada,
um seguidor de instrucao estavel nao precisa de historico. Demonstracao por construcao, nao e dado de modelo."""
import sys
from pathlib import Path
H = Path(__file__).resolve().parent
sys.path.insert(0, str(H/"copia_extratores")); sys.path.insert(0, str(H/"copia_contaminacao"))
import extratores as E, medir_ponto_fixo_comum as M
spec = E.load_spec(H/"copia_extratores"/"especificacao.json")
T = spec["arms"]["T"]["assertions"]
block = "\n".join("|".join(["K06R1",a["id"],a["subject"],a["relation"],a["object"],a["status"]]) for a in T)+"\n"
def run(name, answer_k):
    st = {str(k): E.extract(answer_k(k), "T", spec)["vector"] for k in range(1,13)}
    r = M.measure({"target":[1]*24, "states": st})
    print(f"{name:55s} {r['perturbation_class']:34s} V2-RET={r['V2_RET_p8_r10']} A8={r['A8_legacy_compatibility_only']}")
# 1. seguidor de instrucao sem memoria; P_j = pedido de formato diferente em k=9
run("sem memoria; P_j muda o formato em k=9 (prosa)", lambda k: "Resposta em prosa livre, como pedido.\n" if k==9 else block)
# 2. sem memoria; P_j muda o conteudo: em k=9 responde 20 de 24 (o resto omitido) e depois volta
run("sem memoria; P_j omite 4 asser. em k=9", lambda k: "".join(block.splitlines(True)[:20]) if k==9 else block)
# 3. sem memoria; ignora P_j
run("sem memoria; ignora P_j", lambda k: block)
# 4. 'atrator' nao e' distinguivel: qualquer um dos tres produz a mesma classe se d9>0 e d10-12=0
