# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: compila o CONJUNTO das pedras novas da v413 na forma do kernel, sobre a caixa da v412
(C:\\t\\k412c; so' o binario do Lean, nunca lake). Uso: compilar_conjunto_v413.py <raiz>, onde <raiz> contem TGLExt\\X.lean
(origem ou pedras_limpas). Cada modulo compila como TGLExt.X (cwd = raiz), na ordem dos imports, em ate' 4 processos;
os .olean vao a <raiz>\\..\\build_<nome da raiz>\\TGLExt. Depois de cada modulo, uma AUDITORIA gerada por script imprime
os axiomas de TODO teorema publico do modulo (nomes lidos da fonte, com o namespace), e nao so' os #print que a fonte
traz. Fail-closed: RC, erro, aviso, sorryAx, teorema sem relatorio ou axioma fora do trio reprovam. Recibo:
<raiz>\\..\\CONJUNTO_<nome da raiz>.json."""
import hashlib, json, os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = Path(sys.argv[1]).resolve()
FONTE = RAIZ / "TGLExt"
B = Path(__file__).resolve().parent / "caixa_v413"  # a arvore unica: links da v412 + os novos (montar_caixa_v413.py)
AUD = RAIZ.parent / ("auditoria_" + RAIZ.name)
AUD.mkdir(exist_ok=True)
LEAN = r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe"
SB = Path(r"C:\t\k412c\final\.lake")
assert Path(LEAN).exists() and SB.exists() and FONTE.is_dir() and (B / "CAIXA.json").exists()
caminhos = [str(B), str(SB / "build" / "lib" / "lean")]  # a caixa primeiro: o Lean acha o pacote TGLExt nela
caminhos += [str(p / ".lake" / "build" / "lib" / "lean") for p in sorted((SB / "packages").iterdir())
             if (p / ".lake" / "build" / "lib" / "lean").exists()]
CAIXA_V412 = (SB / "build" / "lib" / "lean").resolve()
env = dict(os.environ)
env["LEAN_PATH"] = ";".join(caminhos)
TRIO = {"propext", "Classical.choice", "Quot.sound"}
REL = re.compile(r"'([^']+)' depends on axioms: \[(.*?)\]", re.S)
SEM = re.compile(r"'([^']+)' does not depend on any axioms")
IMP = re.compile(r"^import (\S+)\s*$", re.M)
DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:(private|protected)\s+)?(?:noncomputable\s+)?(theorem|lemma)\s+([^\s(:{\[]+)")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def sem_comentarios(t):
    out, i, n, prof = [], 0, len(t), 0
    while i < n:
        if t.startswith("/-", i):
            prof += 1; i += 2; continue
        if prof and t.startswith("-/", i):
            prof -= 1; i += 2; continue
        if prof:
            if t[i] == "\n":
                out.append("\n")
            i += 1; continue
        if t.startswith("--", i):
            while i < n and t[i] != "\n":
                i += 1
            continue
        out.append(t[i]); i += 1
    return "".join(out)


def teoremas(texto):
    pilha, nomes = [], []
    for linha in sem_comentarios(texto).split("\n"):
        l = linha.strip()
        m = re.match(r"namespace\s+(\S+)\s*$", l)
        if m:
            pilha.append(("ns", m.group(1))); continue
        m = re.match(r"section(?:\s+(\S+))?\s*$", l)
        if m:
            pilha.append(("sec", m.group(1) or "")); continue
        m = re.match(r"end(?:\s+(\S+))?\s*$", l)
        if m:
            assert pilha, "end sem abertura"
            pilha.pop(); continue
        m = DECL.match(l)
        if m and m.group(1) != "private":
            nm = m.group(3)
            pref = ".".join(x for k, x in pilha if k == "ns")
            nomes.append(nm[7:] if nm.startswith("_root_.") else (pref + "." + nm if pref else nm))
    return nomes


mods = sorted(p.stem for p in FONTE.glob("*.lean"))
deps = {m: [i[7:] for i in IMP.findall((FONTE / (m + ".lean")).read_text(encoding="utf-8"))
            if i.startswith("TGLExt.") and i[7:] in mods] for m in mods}


def roda(cmd, cwd):
    r = subprocess.run(cmd, env=env, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def compila(m):
    t0 = time.time()
    f = FONTE / (m + ".lean")
    alvo = B / "TGLExt" / (m + ".olean")
    assert CAIXA_V412 not in alvo.resolve().parents
    if alvo.exists():
        os.unlink(alvo)  # desfaz o link (ou apaga a compilacao anterior desta caixa); o arquivo da v412 nao muda
    rc, saida = roda([LEAN, "-o", str(alvo), "TGLExt\\" + m + ".lean"], RAIZ)
    (AUD / (m + ".compile.log")).write_text("FONTE: %s\nSHA256: %s\nRC: %d\nSAIDA:\n%s" % (f, sha(f), rc, saida),
                                            encoding="utf-8")
    item = {"modulo": "TGLExt." + m, "fonte": str(f), "sha256": sha(f), "rc": rc, "avisos": saida.count("warning:"),
            "erros": saida.count("error:"), "sorryAx": "sorryAx" in saida}
    nomes = teoremas(f.read_text(encoding="utf-8"))
    item["teoremas"] = len(nomes)
    rel = {}
    if rc == 0:
        a = AUD / ("Audit_" + m + ".lean")
        a.write_text("import TGLExt.%s\n\n%s\n" % (m, "\n".join("#print axioms " + n for n in nomes)), encoding="utf-8")
        rc2, s2 = roda([LEAN, a.name], AUD)
        (AUD / ("Audit_" + m + ".log")).write_text("RC: %d\n%s" % (rc2, s2), encoding="utf-8")
        item.update({"rc_auditoria": rc2, "avisos_auditoria": s2.count("warning:"), "erros_auditoria": s2.count("error:")})
        rel = {n: sorted({x.strip() for x in l.replace("\n", " ").split(",") if x.strip()}) for n, l in REL.findall(s2)}
        rel.update({n: [] for n in SEM.findall(s2)})
    item["relatorios"] = len(rel)
    item["faltando"] = [n for n in nomes if n not in rel]
    item["fora_do_trio"] = {n: sorted(set(x) - TRIO) for n, x in rel.items() if set(x) - TRIO}
    item["axiomas"] = rel
    item["s"] = round(time.time() - t0, 1)
    item["bom"] = not (rc or item["erros"] or item["avisos"] or item["sorryAx"] or item.get("rc_auditoria", 1)
                       or item.get("erros_auditoria", 1) or item.get("avisos_auditoria", 1) or item["faltando"]
                       or item["fora_do_trio"] or not nomes)
    print("%-27s RC %d | %5.1f s | teoremas %3d | relatorios %3d | faltando %d | fora do trio %d | bom %s" % (
        m, rc, item["s"], len(nomes), len(rel), len(item["faltando"]), len(item["fora_do_trio"]), item["bom"]),
        flush=True)
    if not item["bom"]:
        print(saida[-3000:], flush=True)
    return item


feitos, res = set(), {}
t0 = time.time()
with ThreadPoolExecutor(max_workers=4) as ex:
    pend = {}
    while len(res) < len(mods):
        prontos = [m for m in mods if m not in res and m not in pend and all(d in feitos for d in deps[m])]
        for m in prontos:
            pend[m] = ex.submit(compila, m)
        assert pend, "ciclo nos imports: " + ", ".join(m for m in mods if m not in res)
        while not any(f.done() for f in pend.values()):
            time.sleep(0.5)
        for m in [k for k, f in pend.items() if f.done()]:
            res[m] = pend.pop(m).result()
            if res[m]["bom"]:
                feitos.add(m)
        mudou = True
        while mudou:
            mudou = False
            for k in mods:
                ruins = [d for d in deps[k] if d in res and not res[d]["bom"]]
                if k not in res and k not in pend and ruins:
                    res[k] = {"modulo": "TGLExt." + k, "bom": False, "nao_compilado": "depende de " + ", ".join(ruins)}
                    mudou = True

tot_t = sum(r.get("teoremas", 0) for r in res.values())
tot_r = sum(r.get("relatorios", 0) for r in res.values())
rec = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "raiz": str(RAIZ), "lean_path": caminhos, "dependencias": deps,
       "modulos": res, "teoremas": tot_t, "relatorios": tot_r, "todos_bons": all(r["bom"] for r in res.values()),
       "s": round(time.time() - t0, 1)}
dados = json.dumps(rec, ensure_ascii=False, indent=1).encode("utf-8")
dest = RAIZ.parent / ("CONJUNTO_" + RAIZ.name + ".json")
tmp = dest.with_name(dest.name + ".tmp")
tmp.write_bytes(dados)
assert tmp.read_bytes() == dados
tmp.replace(dest)
print("CONJUNTO %s: %d modulos | teoremas %d | relatorios %d | todos bons %s | %.0f s | recibo %s sha16 %s" % (
    RAIZ.name, len(res), tot_t, tot_r, rec["todos_bons"], rec["s"], dest.name, sha(dest)[:16]))
