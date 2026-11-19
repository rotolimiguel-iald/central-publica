# -*- coding: utf-8 -*-
"""conferir_quinta_lista_v412.py -- (claude-construtor-v412, continuacao 2, 17/11/2026) so' LEITURA das fontes. Confere a QUINTA lista de pedras antes de levar o sandbox k412c da quarta para a quinta:
  (1) o sha256 e os bytes de cada um dos 40 arquivos de insumos\\pedras_r5 contra insumos\\MANIFESTO_PEDRAS_v412_R5.json (e que a pasta nao tem arquivo a mais nem a menos);
  (2) quais dos 40 sao identicos byte a byte aos de insumos\\pedras_r4 (e contra o sha256 do manifesto R4) e quais mudaram; que os que mudaram sao exatamente os do campo `mudaram_da_quarta_lista` do manifesto R5;
  (3) para os que mudaram, que o CODIGO fora de comentarios e docstrings e' o mesmo, por DOIS metodos independentes: (a) o do conferir_so_comentarios_r1_r4_v412.py (texto sem comentarios, cadeias mantidas, espaco
      normalizado) e (b) o de lean_texto_v412.mascara_comentarios (comentarios e cadeias trocados por espaco, espaco normalizado). Se algum diferir em codigo, sai 1 (e quem roda PARA e relata);
  (4) que os campos do manifesto que o preparo usa (modulos, ordem, imports, imports_de_candidatas, namespaces, linhas_print_axioms, declaracoes_theorem_lemma, sorry, n_modulos, ficam_fora) sao os mesmos da quarta lista;
  (5) que ANCORAS_PROPOSTAS_v412_R5.json aponta para o sha256 do manifesto R5.
Grava kernel\\CODIGO_R4_R5_v412.json (arquivo novo). Nao toca em insumos\\.
uso: C:\\Python314\\python.exe -B -X utf8 conferir_quinta_lista_v412.py"""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
INS = os.path.join(HERE, "insumos")
sys.path.insert(0, HERE)
import lean_texto_v412 as LT  # noqa: E402
sha = lambda b: hashlib.sha256(b).hexdigest()


def metodo_a(t):
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


def metodo_b(t):
    return re.sub(r"\s+", " ", LT.mascara_comentarios(t)).strip()


M4 = json.load(open(os.path.join(INS, "MANIFESTO_PEDRAS_v412_R4.json"), encoding="utf-8"))
M5p = os.path.join(INS, "MANIFESTO_PEDRAS_v412_R5.json")
M5 = json.load(open(M5p, encoding="utf-8"))
m4 = {m["modulo"]: m for m in M4["modulos"]}; m5 = {m["modulo"]: m for m in M5["modulos"]}
falhas = []
# (1)
ped5 = os.path.join(INS, "pedras_r5"); ped4 = os.path.join(INS, "pedras_r4")
arqs5 = sorted(f for f in os.listdir(ped5)); esperados = sorted(n + ".lean" for n in m5)
if arqs5 != esperados:
    falhas.append(["pedras_r5 tem arquivo a mais ou a menos", sorted(set(arqs5) ^ set(esperados))])
if len(m5) != int(M5["n_modulos"]) or len(M5["modulos"]) != len(m5):
    falhas.append(["n_modulos != modulos distintos do manifesto R5", len(m5), M5["n_modulos"]])
res = {}; sha_ruim = []
for n, m in m5.items():
    b5 = open(os.path.join(ped5, n + ".lean"), "rb").read()
    ok_sha = (sha(b5) == m["sha256"] and len(b5) == int(m["bytes"]))
    if not ok_sha:
        sha_ruim.append([n, sha(b5)[:16], m["sha256"][:16]])
    e = {"sha16": sha(b5)[:16], "bytes": len(b5), "sha256_confere_com_o_manifesto_r5": ok_sha, "tem_CR": b"\r" in b5}
    # (2)
    if n not in m4:
        e["estado"] = "NOVO_NA_QUINTA"; falhas.append(["modulo novo na quinta lista (nao previsto)", n])
        res[n] = e; continue
    b4 = open(os.path.join(ped4, n + ".lean"), "rb").read()
    e["sha256_r4_confere_com_o_manifesto_r4"] = (sha(b4) == m4[n]["sha256"])
    if b4 == b5:
        e["estado"] = "identico_byte_a_byte"
        e["manifesto_r4_sha256_igual"] = (m4[n]["sha256"] == m["sha256"])
    else:
        # (3)
        ca, cb = metodo_a(b4.decode("utf-8")), metodo_a(b5.decode("utf-8"))
        da, db = metodo_b(b4.decode("utf-8")), metodo_b(b5.decode("utf-8"))
        if ca == cb and da == db:
            e["estado"] = "so_comentarios_e_docstrings"
            e["codigo_sha16_metodo_a"] = sha(ca.encode("utf-8"))[:16]; e["codigo_sha16_metodo_b"] = sha(da.encode("utf-8"))[:16]
            e["bytes_r4"] = len(b4); e["bytes_r5"] = len(b5)
        else:
            e["estado"] = "CODIGO_DIFERE"
            for rot, x, y in (("a", ca, cb), ("b", da, db)):
                if x != y:
                    k = next((i for i, (p, q) in enumerate(zip(x, y)) if p != q), min(len(x), len(y)))
                    e["primeira_diferenca_metodo_" + rot] = {"posicao": k, "antes": x[max(0, k - 80):k + 100], "depois": y[max(0, k - 80):k + 100]}
            falhas.append(["CODIGO DIFERE (PARE e relate)", n])
    # (4) campos que o preparo usa
    campos = ("imports", "imports_de_candidatas", "namespaces", "linhas_print_axioms", "declaracoes_theorem_lemma", "sorry", "frente", "de_quem")
    dif = [c for c in campos if m4[n].get(c) != m.get(c)]
    e["campos_do_manifesto_diferentes_da_quarta"] = dif
    if dif:
        falhas.append(["campo do manifesto difere da quarta lista", n, dif])
    res[n] = e
if sha_ruim:
    falhas.append(["sha256/bytes diferente do manifesto R5", sha_ruim])
ordem4 = [m["modulo"] for m in M4["modulos"]]; ordem5 = [m["modulo"] for m in M5["modulos"]]
if ordem4 != ordem5:
    falhas.append(["a ordem dos modulos no manifesto difere da quarta lista"])
for c in ("n_modulos", "ficam_fora", "imports_soltos_de_candidatas", "imports_soltos_sem_modulo_no_conjunto"):
    if M4.get(c) != M5.get(c):
        falhas.append(["campo de topo do manifesto difere da quarta lista", c])
mudaram_achados = sorted(n for n, e in res.items() if e["estado"] == "so_comentarios_e_docstrings")
mudaram_dito = sorted(M5.get("mudaram_da_quarta_lista") or [])
if mudaram_achados != mudaram_dito:
    falhas.append(["os que mudaram (achados por mim) != mudaram_da_quarta_lista do manifesto R5", mudaram_achados, mudaram_dito])
# (5)
ap = json.load(open(os.path.join(INS, "ANCORAS_PROPOSTAS_v412_R5.json"), encoding="utf-8"))
ap_ok = ap.get("manifesto_sha256") == sha(open(M5p, "rb").read())
if not ap_ok:
    falhas.append(["ANCORAS_PROPOSTAS_v412_R5.json nao aponta para o sha256 do manifesto R5"])
cont = {}
for e in res.values():
    cont[e["estado"]] = cont.get(e["estado"], 0) + 1
rep = {"contagem": cont, "mudaram_da_quarta_lista_achados": mudaram_achados, "mudaram_da_quarta_lista_do_manifesto": mudaram_dito, "pedras_r5_arquivos": len(arqs5),
       "manifesto_r5_sha16": sha(open(M5p, "rb").read())[:16], "ancoras_r5_aponta_para_o_manifesto_r5": ap_ok, "falhas": falhas, "por_modulo": res,
       "metodo": "(a) texto sem comentarios (`--`, `/- -/` aninhado, docstrings), cadeias mantidas, espaco normalizado; (b) lean_texto_v412.mascara_comentarios (comentarios e cadeias em branco), espaco normalizado; os dois tem de concordar; so' leitura"}
out = os.path.join(HERE, "kernel", "CODIGO_R4_R5_v412.json")
with open(out + ".tmp", "w", encoding="utf-8") as fh:
    fh.write(json.dumps(rep, ensure_ascii=False, indent=1))
os.replace(out + ".tmp", out)
print(cont, "| mudaram:", mudaram_achados, "| falhas:", falhas, "| gravado:", out, "sha16", sha(open(out, "rb").read())[:16])
sys.exit(1 if falhas else 0)
