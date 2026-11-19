# -*- coding: utf-8 -*-
"""diffs_v412.py -- (gerencia c1, 19/11/2026, depois do rito e do conferidor enxuto que BATEU) os dois diffs que a custodia publica em
`diferencas_v412/` (a G1 os exige de N: espelho_pares.montar_pares, item 7):
  (1) DIFF_KERNEL_v412.txt: arquivos novos, removidos e mudados do kernel EMBUTIDO do um.py v412 do Nos contra o do um.py v411 selado
      (o backup de bytes da instalacao, um.py.bak_20261118_235146, conferido pelo sha16 da origem dos ESPERADOS);
  (1b) DIFF_v411_v412.diff: `diff -u` do um.py v411 contra o v412 (o registro da subida; texto, nao e' prova de nada).
Tudo LIDO (sha256 calculado aqui; nada digitado). Recusa se o um.py do Nos nao for o candidato pinado, se o backup nao for a v411, se houver
modulo removido, ou se os novos nao forem exatamente os 156 de kernel_modulos_novos_v412.json. Escrita por temporario. Recibo DIFFS_v412_RECIBO.json.
uso: python -I -B -X utf8 diffs_v412.py"""
import ast, hashlib, json, os, shutil, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
V = os.path.dirname(os.path.abspath(__file__))
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
sha = lambda b: hashlib.sha256(b).hexdigest()
ESP = json.load(open(os.path.join(V, "ESPERADOS_v412.json"), encoding="utf-8"))
BASE = os.path.join(NOS, "um.py.bak_20261118_235146"); CAND = os.path.join(NOS, "um.py")
rb, rc = open(BASE, "rb").read(), open(CAND, "rb").read()
assert sha(rb)[:16] == ESP["origem_sha16"], ("o backup nao e' a v411 selada", sha(rb)[:16])
assert sha(rc)[:16] == ESP["candidato_sha16"] and len(rc) == ESP["candidato_bytes"], ("o um.py do Nos nao e' o candidato pinado", sha(rc)[:16])


def embutido(raw):
    lines = raw.decode("utf-8").splitlines(keepends=True)
    i0 = [i for i, l in enumerate(lines) if l.startswith("_EMBEDDED_KERNEL_FILES = {")]
    assert len(i0) == 1, i0
    j = i0[0] + 1
    while lines[j].rstrip("\r\n") != "}":
        j += 1
    return ast.literal_eval("".join(lines[i0[0]:j + 1]).split("=", 1)[1].strip())


E0, E1 = embutido(rb), embutido(rc)
h0, h1 = sha(rb)[:16], sha(rc)[:16]
novos = sorted(set(E1) - set(E0)); removidos = sorted(set(E0) - set(E1)); mudados = sorted(k for k in set(E0) & set(E1) if E0[k] != E1[k])
KN = json.load(open(os.path.join(V, "kernel_modulos_novos_v412.json"), encoding="utf-8"))
lista = (KN.get("novos") or KN.get("modulos")) if isinstance(KN, dict) else KN
assert lista, "kernel_modulos_novos_v412.json sem a lista dos novos"
nomes_lista = sorted({os.path.splitext(os.path.basename(str(x if isinstance(x, str) else (x.get("arquivo") or x.get("nome") or x.get("modulo")))))[0] for x in lista})
nomes_novos = sorted({os.path.splitext(os.path.basename(k))[0] for k in novos})
print("embutidos: v411 %d | v412 %d | novos %d | removidos %d | mudados %d | lista dos novos %d" % (len(E0), len(E1), len(novos), len(removidos), len(mudados), len(nomes_lista)))
assert not removidos, ("modulo removido do kernel", removidos[:10])
assert len(novos) == ESP["kernel"]["modulos_novos"] == 156, ("os novos nao sao 156", len(novos))
assert nomes_novos == nomes_lista, ("os novos nao sao os da lista", sorted(set(nomes_novos) ^ set(nomes_lista))[:10])
out = ["DIFF DO KERNEL EMBUTIDO v411 (%s) -> v412 (%s)" % (h0, h1), "", "novos (%d):" % len(novos)]
out += ["  + %s  %s  %d B" % (k, sha(E1[k].encode("utf-8"))[:16], len(E1[k].encode("utf-8"))) for k in novos]
out += ["", "removidos (%d):" % len(removidos)] + ["  - " + k for k in removidos]
out += ["", "mudados (%d):" % len(mudados)] + ["  ~ %s  %s -> %s" % (k, sha(E0[k].encode("utf-8"))[:16], sha(E1[k].encode("utf-8"))[:16]) for k in mudados]
out += ["", "a v412 acrescenta %d modulos novos ao kernel embutido (%d -> %d arquivos); nenhum removido; os mudados acima sao os que importam os novos ou os contam" % (len(novos), len(E0), len(E1))]
pk = os.path.join(V, "DIFF_KERNEL_v412.txt")
open(pk + ".tmp", "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n"); os.replace(pk + ".tmp", pk)
print("\n".join(out[:1]), "| mudados:", mudados[:10])
dif = shutil.which("diff"); pd = os.path.join(V, "DIFF_v411_v412.diff")
assert dif, "diff -u nao esta no PATH"
r = subprocess.run([dif, "-u", "--label", "um.py v411 %s" % h0, "--label", "um.py v412 %s" % h1, BASE, CAND], capture_output=True)
assert r.returncode in (0, 1), ("diff -u falhou", r.returncode, r.stderr[:300])
open(pd + ".tmp", "wb").write(r.stdout); os.replace(pd + ".tmp", pd)
rec = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "por": "gerencia c1 (diffs_v412.py)", "base": {"path": BASE, "sha256": sha(rb), "bytes": len(rb)},
       "candidato": {"path": CAND, "sha256": sha(rc), "bytes": len(rc)},
       "DIFF_KERNEL_v412.txt": {"sha256": sha(open(pk, "rb").read()), "bytes": os.path.getsize(pk), "novos": len(novos), "removidos": 0, "mudados": mudados},
       "DIFF_v411_v412.diff": {"sha256": sha(r.stdout), "bytes": len(r.stdout), "ferramenta": dif, "rc": r.returncode}}
pr = os.path.join(V, "DIFFS_v412_RECIBO.json")
open(pr + ".tmp", "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1)); os.replace(pr + ".tmp", pr)
print("DIFF_v411_v412.diff: %d B sha16 %s | recibo %s" % (len(r.stdout), sha(r.stdout)[:16], pr))
