# -*- coding: utf-8 -*-
"""conferir_setima_lista_v412.py -- (contrato R4) confere a SETIMA lista de pedras: (1) o sha256 e os bytes de cada um dos 42 arquivos de insumos\\pedras_r7 contra insumos\\MANIFESTO_PEDRAS_v412_R7.json;
(2) que os 40 modulos da quinta lista sao identicos BYTE A BYTE aos de insumos\\pedras_r5 (e contra o sha256 do manifesto R5); (3) que so' Token2 e AMaquina sao novos em relacao a quinta; (4) que Token2 difere da sexta
(insumos\\pedras_r6) so' em comentarios e docstrings (dois metodos independentes: remocao aninhada de comentarios; mascara de comentarios com espaco normalizado; os dois concordam); (5) que nenhum nome novo colide com um modulo existente
no kernel do Nos (Token2 x TGLExt.Token) e que os imports de irmaos resolvem dentro da lista. So' leitura; grava kernel\\SETIMA_LISTA_CONFERIDA_v412.json. Cada checagem diz quantos itens examinou; zero e' falha."""
import hashlib, json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from e2_lib_v412 import Exame, salvar_json, sha16_arq
NOS_K = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt")
R5, R6, R7 = HERE / "insumos" / "pedras_r5", HERE / "insumos" / "pedras_r6", HERE / "insumos" / "pedras_r7"
M5 = json.loads((HERE / "insumos" / "MANIFESTO_PEDRAS_v412_R5.json").read_bytes().decode("utf-8"))
M7 = json.loads((HERE / "insumos" / "MANIFESTO_PEDRAS_v412_R7.json").read_bytes().decode("utf-8"))
sh = lambda b: hashlib.sha256(b).hexdigest()
e = Exame("setima_lista")


def nest_strip(t):
    out, i, n, prof = [], 0, len(t), 0
    while i < n:
        if t.startswith("/-", i):
            prof += 1; i += 2; continue
        if prof and t.startswith("-/", i):
            prof -= 1; i += 2; continue
        if prof:
            i += 1; continue
        if t.startswith("--", i):
            while i < n and t[i] != "\n":
                i += 1
            continue
        out.append(t[i]); i += 1
    return re.sub(r"\s+", " ", "".join(out)).strip()


def mask(t):
    out, i, n, prof = [], 0, len(t), 0
    while i < n:
        if t.startswith("/-", i):
            prof += 1; out.append("  "); i += 2; continue
        if prof and t.startswith("-/", i):
            prof -= 1; out.append("  "); i += 2; continue
        if prof:
            out.append(" "); i += 1; continue
        if t.startswith("--", i):
            while i < n and t[i] != "\n":
                out.append(" "); i += 1
            continue
        out.append(t[i]); i += 1
    return " ".join("".join(out).split())


ent7 = {x["modulo"]: x for x in M7["modulos"]}
ent5 = {x["modulo"]: x for x in M5["modulos"]}
falhas = []
bad = [m for m, x in ent7.items() if not (R7 / (m + ".lean")).exists() or sh((R7 / (m + ".lean")).read_bytes()) != x["sha256"] or (R7 / (m + ".lean")).stat().st_size != int(x["bytes"])]
e.chk("os %d arquivos de pedras_r7 tem o sha256 e os bytes do manifesto R7" % len(ent7), not bad and len(ent7) == int(M7["n_modulos"]) == 42, len(ent7), bad[:5])
sobra = sorted(p.stem for p in R7.glob("*.lean") if p.stem not in ent7)
e.chk("nenhum arquivo em pedras_r7 fora do manifesto", not sobra, len(list(R7.glob("*.lean"))), sobra)
ig = [m for m in ent5 if m in ent7 and (R5 / (m + ".lean")).read_bytes() == (R7 / (m + ".lean")).read_bytes() and ent5[m]["sha256"] == ent7[m]["sha256"] == sh((R7 / (m + ".lean")).read_bytes())]
e.chk("os 40 da quinta lista sao identicos byte a byte (pedras_r5 x pedras_r7) e no manifesto", len(ig) == 40 == len(ent5), len(ent5), sorted(set(ent5) - set(ig))[:5])
novos = sorted(set(ent7) - set(ent5))
e.chk("so' Token2 e AMaquina sao novos em relacao a quinta, e o manifesto diz o mesmo", novos == ["AMaquina", "Token2"] == sorted(M7["novas_em_relacao_a_quinta_lista"]), len(novos), novos)
t6, t7 = (R6 / "Token2.lean").read_text(encoding="utf-8"), (R7 / "Token2.lean").read_text(encoding="utf-8")
e.chk("Token2: so' comentarios e docstrings mudaram da sexta para a setima, pelos DOIS metodos, e o texto mudou", nest_strip(t6) == nest_strip(t7) and mask(t6) == mask(t7) and t6 != t7 and M7["mudaram_da_sexta_lista"] == ["Token2"], 2, [len(t6), len(t7)])
a6 = (R6 / "AMaquina.lean").read_bytes() == (R7 / "AMaquina.lean").read_bytes()
e.chk("AMaquina e' igual byte a byte na sexta e na setima", a6, 1)
colide = [m for m in ent7 if (NOS_K / (m + ".lean")).exists()]
e.chk("nenhum modulo da lista colide com um arquivo de TGLExt/ do Nos (Token2 x Token)", not colide and (NOS_K / "Token.lean").exists(), len(ent7), colide)
imps = {}
nao_res = []
for m in ent7:
    for imp in re.findall(r"(?m)^import\s+(\S+)", (R7 / (m + ".lean")).read_text(encoding="utf-8")):
        imps.setdefault(m, []).append(imp)
        base = imp.split(".")[-1] if imp.startswith("TGLExt.") else imp
        if imp.startswith("Mathlib") or imp.startswith("Init") or imp.startswith("Lean"):
            continue
        nome = imp.replace("TGLExt.", "").split(".")[-1] if imp.startswith("TGLExt.") else imp
        if nome in ent7 or (NOS_K / (imp.replace("TGLExt.", "").replace(".", "/") + ".lean")).exists() or (NOS_K.parent / (imp.replace(".", "/") + ".lean")).exists():
            continue
        nao_res.append((m, imp))
e.chk("todo import de irmao ou de TGLExt/TGL resolve na lista ou no kernel do Nos (Token2 importa TGLExt.Token, AMaquina importa Token2)", not nao_res, sum(len(v) for v in imps.values()), nao_res[:5])
tok = [i for i in imps.get("Token2", [])]; am = [i for i in imps.get("AMaquina", [])]
e.chk("Token2 importa AMedidaEOIf, OTempoEACauda e TGLExt.Token; AMaquina importa Token2 e OHabitanteDoNome", {"AMedidaEOIf", "OTempoEACauda", "TGLExt.Token"} <= set(tok) and {"Token2", "OHabitanteDoNome"} <= set(am), len(tok) + len(am), [tok, am])
out = {"ok": e.ok, "resumo": e.resumo(), "checagens": e.linhas, "manifesto_R7_sha16": sha16_arq(HERE / "insumos" / "MANIFESTO_PEDRAS_v412_R7.json"), "manifesto_R5_sha16": sha16_arq(HERE / "insumos" / "MANIFESTO_PEDRAS_v412_R5.json")}
salvar_json(HERE / "kernel" / "SETIMA_LISTA_CONFERIDA_v412.json", out)
print(e.resumo())
for l in e.linhas:
    if not l["ok"]:
        print("FALHOU:", l["checagem"], l["n_itens_examinados"], str(l["detalhe"])[:300])
sys.exit(0 if e.ok else 1)
