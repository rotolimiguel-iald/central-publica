# -*- coding: utf-8 -*-
"""portao_do_pilar_candidato_v412.py -- (contrato R4, secao 7b) o PORTAO DO PILAR NO CANDIDATO, por LEITURA DE CODIGO (nada roda; nada importa torch; nada toca a placa): confere, por sha256 do texto de cada nome de topo, que o gerador NAO
tocou nenhuma das tres entradas da chave do cache do pilar (o trabalhador embutido _QP_WORKER_SRC, a especificacao canonica _QP_SPEC_JSON e beta pelo motor _qp_beta) nem nada do fecho de dependencias da funcao da chave (_qp_key e o que ela e as tres
entradas leem), e que _EMBEDDED_KERNEL_FILES, _LEAN_THEOREM_FLAGS, os registros e o texto da v412 continuam FORA desse fecho. As entradas e o fecho sao os de PORTAO_DO_PILAR_v412.json (lidos por script). So' leitura.
Grava PORTAO_DO_PILAR_CANDIDATO_v412.json. O passo seguinte ao rito (conferir, antes dele, que o ambiente da placa e' o do cache; se nao for, PARAR) NAO e' deste script: ele nao toca a placa.
uso: C:\\Python314\\python.exe -B -X utf8 portao_do_pilar_candidato_v412.py [<candidato.py>]"""
import ast, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from e2_lib_v412 import Exame, salvar_json, sha16_arq
sha = lambda b: hashlib.sha256(b).hexdigest()
CAND = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "um_v412_candidato.py")
BASE = os.path.join(HERE, "base_v411", "um.py")
PJ = json.load(open(os.path.join(HERE, "PORTAO_DO_PILAR_v412.json"), encoding="utf-8"))


def carregar(p):
    src = open(p, "rb").read().decode("utf-8")
    tree = ast.parse(src)
    top = {}
    for n in tree.body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            top[n.name] = n
        elif isinstance(n, ast.Assign):
            for tg in n.targets:
                if isinstance(tg, ast.Name):
                    top[tg.id] = n
        elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name):
            top[n.target.id] = n
    return src, top


def fecho(top, raizes):
    vis, fila = set(), list(raizes)
    while fila:
        a = fila.pop()
        if a in vis or a not in top:
            continue
        vis.add(a)
        fila.extend(sorted({x.id for x in ast.walk(top[a]) if isinstance(x, ast.Name) and x.id in top and x.id != getattr(top[a], "name", None)}))
    return vis


bsrc, btop = carregar(BASE)
csrc, ctop = carregar(CAND)
ENTRADAS = {"worker_sha256": ["_qp_materialize", "_QP_WORKER_SRC", "_qp_dir"], "spec_canonica": ["_QP_SPEC_JSON", "_qp_canon", "_QP_SPEC_SHA256"], "beta_hex": ["_qp_beta"]}
raizes = ["_qp_key"] + sum(ENTRADAS.values(), [])
fb, fc = fecho(btop, raizes), fecho(ctop, raizes)
seg = lambda src, top, n: ast.get_source_segment(src, top[n])
e = Exame("portao_do_pilar_no_candidato")
e.chk("o fecho de dependencias da chave e' o mesmo na base e no candidato (%d nomes)" % len(fb), fb == fc and len(fb) > 0, len(fb), sorted(fb ^ fc)[:6])
dif = [n for n in sorted(fb) if n in ctop and sha(seg(bsrc, btop, n).encode()) != sha(seg(csrc, ctop, n).encode())]
e.chk("o texto de CADA nome do fecho tem o mesmo sha256 na base e no candidato", not dif and len(fb) > 0, len(fb), dif[:6])
por_entrada = {}
for k, nomes in ENTRADAS.items():
    hs = {n: (sha(seg(bsrc, btop, n).encode())[:16], sha(seg(csrc, ctop, n).encode())[:16]) for n in nomes if n in btop and n in ctop}
    por_entrada[k] = {n: {"base": a, "candidato": b, "igual": a == b} for n, (a, b) in hs.items()}
    e.chk("a entrada %s (%s): cada nome tem o mesmo sha256 na base e no candidato" % (k, ", ".join(nomes)), set(hs) == set(nomes) and all(a == b for a, b in hs.values()), len(nomes), por_entrada[k])
PROIBIDOS = ["_EMBEDDED_KERNEL_FILES", "_LEAN_THEOREM_FLAGS", "_V412_SPECS", "_V412_SECAO", "_V412_NOMES_REGISTROS", "_V412_TOPO", "_v412_guarda_frases", "_v412_travessia", "_v412_secao_tex", "_v412_rodar_specs", "_v412_topo_texto", "_V411_SPECS", "_V411_TOPO"]
dentro = [n for n in PROIBIDOS if n in fc]
e.chk("nenhum nome do que a v412 muda (kernel embutido, bandeiras, registros, texto do artigo e do resumo) esta' no fecho da chave do candidato", not dentro, len(PROIBIDOS), dentro)
e.chk("as tres entradas da chave sao as de PORTAO_DO_PILAR_v412.json", set(PJ["entradas_da_chave"]) == set(ENTRADAS), len(ENTRADAS), sorted(PJ["entradas_da_chave"]))
e.chk("o candidato difere da base (nao e' copia: o gerador rodou)", sha(csrc.encode()) != sha(bsrc.encode()), 2)
out = {"ok": e.ok, "resumo": e.resumo(), "checagens": e.linhas, "candidato": {"arquivo": CAND, "sha16": sha(csrc.encode())[:16], "bytes": len(csrc.encode())}, "base_v411_sha16": sha(bsrc.encode())[:16],
       "entradas": por_entrada, "n_nomes_do_fecho": len(fb), "portao_json_sha16": sha16_arq(os.path.join(HERE, "PORTAO_DO_PILAR_v412.json")),
       "falta_antes_do_rito": "conferir que o ambiente da placa (torch, cuda, numpy, scipy, python, gpu) e' o do cache; se nao for, PARAR e avisar (ha' treino em curso na placa): ato da gerencia, nao deste script"}
salvar_json(os.path.join(HERE, "PORTAO_DO_PILAR_CANDIDATO_v412.json"), out)
print(e.resumo())
for l in e.linhas:
    if not l["ok"]:
        print("FALHOU:", l["checagem"], l["n_itens_examinados"], str(l["detalhe"])[:300])
sys.exit(0 if e.ok else 1)
