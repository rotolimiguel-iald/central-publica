# -*- coding: utf-8 -*-
"""conferir_so_comentarios_r1_r4_v412.py -- (claude-construtor-v412, complemento da Etapa 1, 17/11/2026) so' LEITURA. Para cada modulo que existe nas duas listas (insumos\\pedras da primeira,
insumos\\pedras_r4 da quarta), confere se o CODIGO e' o mesmo: o texto sem comentarios (`--` e `/- ... -/` com aninhamento, inclusive docstrings), com as cadeias "..." MANTIDAS, e com o espaco em
branco normalizado (sequencias de espaco/quebra viram um espaco). Diz, por modulo, igual ou diferente (e a primeira diferenca). Grava kernel\\CODIGO_R1_R4_v412.json.
uso: C:\\Python314\\python.exe -B -X utf8 conferir_so_comentarios_r1_r4_v412.py"""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
INS = os.path.join(HERE, "insumos")
sha = lambda b: hashlib.sha256(b).hexdigest()


def sem_comentarios(t):
    out = []; i = 0; n = len(t); prof = 0; cad = False
    while i < n:
        c = t[i]; d = t[i + 1] if i + 1 < n else ""
        if prof > 0:
            if c == "/" and d == "-":
                prof += 1; i += 2; continue
            if c == "-" and d == "/":
                prof -= 1; i += 2
                if prof == 0:
                    out.append(" ")
                continue
            i += 1; continue
        if cad:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(t[i + 1]); i += 2; continue
            if c == '"':
                cad = False
            i += 1; continue
        if c == "/" and d == "-":
            prof = 1; i += 2; continue
        if c == "-" and d == "-":
            j = t.find("\n", i); j = n if j < 0 else j
            i = j; continue
        if c == '"':
            cad = True
        out.append(c); i += 1
    return re.sub(r"\s+", " ", "".join(out)).strip()


m1 = {m["modulo"]: m for m in json.load(open(os.path.join(INS, "MANIFESTO_PEDRAS_v412.json"), encoding="utf-8"))["modulos"]}
m4 = {m["modulo"]: m for m in json.load(open(os.path.join(INS, "MANIFESTO_PEDRAS_v412_R4.json"), encoding="utf-8"))["modulos"]}
res = {}
for n, m in m4.items():
    if n not in m1:
        res[n] = {"estado": "novo"}; continue
    b1 = open(os.path.join(INS, "pedras", n + ".lean"), "rb").read(); b4 = open(os.path.join(INS, "pedras_r4", n + ".lean"), "rb").read()
    if b1 == b4:
        res[n] = {"estado": "identico_byte_a_byte"}; continue
    c1 = sem_comentarios(b1.decode("utf-8")); c4 = sem_comentarios(b4.decode("utf-8"))
    if c1 == c4:
        res[n] = {"estado": "so_comentarios_e_docstrings", "codigo_sha16": sha(c4.encode("utf-8"))[:16], "bytes_antes": len(b1), "bytes_depois": len(b4)}
    else:
        k = next((i for i, (x, y) in enumerate(zip(c1, c4)) if x != y), min(len(c1), len(c4)))
        res[n] = {"estado": "CODIGO_DIFERE", "primeira_diferenca": {"posicao": k, "antes": c1[max(0, k - 60):k + 80], "depois": c4[max(0, k - 60):k + 80]}}
cont = {}
for v in res.values():
    cont[v["estado"]] = cont.get(v["estado"], 0) + 1
rep = {"contagem": cont, "por_modulo": res, "metodo": "codigo = texto sem comentarios (`--`, `/- -/` aninhado, docstrings), cadeias mantidas, espaco em branco normalizado; so' leitura"}
out = os.path.join(HERE, "kernel", "CODIGO_R1_R4_v412.json")
with open(out + ".tmp", "w", encoding="utf-8") as fh:
    fh.write(json.dumps(rep, ensure_ascii=False, indent=1))
os.replace(out + ".tmp", out)
print(cont, [k for k, v in res.items() if v["estado"] == "CODIGO_DIFERE"])
