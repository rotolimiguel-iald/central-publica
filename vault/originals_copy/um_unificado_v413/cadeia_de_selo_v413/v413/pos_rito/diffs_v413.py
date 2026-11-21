# -*- coding: utf-8 -*-
"""diffs_v413.py -- (Etapa 3 da v413, 20/11/2026; molde: v412\\diffs_v412.py) DEPOIS do rito e do conferidor que BATEU: os dois diffs que a custodia
publica em diferencas_v413\\ (a G1 os exige: espelho_pares.montar_pares, item 7), gravados em ...\\cadeia_de_selo\\v413\\:
  (1) DIFF_KERNEL_v413.txt: arquivos novos, removidos e mudados do kernel EMBUTIDO do um.py v413 do Nos contra o do um.py v412 selado (o backup de
      bytes da instalacao, lido do APLICADO_AO_CANONICO mais novo e conferido pelo sha16 da origem do ESPERADOS);
  (2) DIFF_v412_v413.diff: `diff -u` do um.py v412 contra o v413 (o registro da subida; texto, nao e' prova de nada).
Recusa se o um.py do Nos nao for o candidato pinado, se o backup nao for a v412, se houver modulo removido, se os novos nao forem EXATAMENTE os de
kernel_modulos_novos_v413.json, ou se os mudados nao forem EXATAMENTE a raiz TGLExt.lean e o modulo corrigido (o CASO NOVO da v413). Tudo LIDO
(sha256 calculado aqui; nada digitado). Escrita por temporario; backup de bytes do que ja' existir. Recibo DIFFS_v413_RECIBO.json.
ENSAIO: --reproduzir-v412 <pasta> refaz, com o MESMO codigo, o DIFF_KERNEL_v412.txt e o DIFF_v411_v412.diff da v412 a partir dos dois um.py que o
recibo da v412 pina (o backup da v411 no Nos e o um.py v412 do Nos, conferidos pelo sha256 do recibo), grava na <pasta> e confere que os bytes sao
os publicados (o controle positivo da maquina). uso: python -I -B -X utf8 diffs_v413.py [--reproduzir-v412 <pasta>]"""
import ast, glob, hashlib, json, os, shutil, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
P = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(P); V412 = os.path.join(os.path.dirname(V), "v412")
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
sha = lambda b: hashlib.sha256(b).hexdigest()


def embutido(raw):
    lines = raw.decode("utf-8").splitlines(keepends=True)
    i0 = [i for i, l in enumerate(lines) if l.startswith("_EMBEDDED_KERNEL_FILES = {")]
    assert len(i0) == 1, i0
    j = i0[0] + 1
    while lines[j].rstrip("\r\n") != "}":
        j += 1
    return ast.literal_eval("".join(lines[i0[0]:j + 1]).split("=", 1)[1].strip())


def diff_kernel(rb, rc, va, vb, nomes_lista, mudados_esperados, frase_final):
    E0, E1 = embutido(rb), embutido(rc)
    h0, h1 = sha(rb)[:16], sha(rc)[:16]
    novos = sorted(set(E1) - set(E0)); removidos = sorted(set(E0) - set(E1)); mudados = sorted(k for k in set(E0) & set(E1) if E0[k] != E1[k])
    nomes_novos = sorted({os.path.splitext(os.path.basename(k))[0] for k in novos})
    print("embutidos: %s %d | %s %d | novos %d | removidos %d | mudados %d | lista dos novos %d" % (va, len(E0), vb, len(E1), len(novos), len(removidos), len(mudados), len(nomes_lista)))
    assert not removidos, ("modulo removido do kernel", removidos[:10])
    assert nomes_novos == sorted(nomes_lista), ("os novos nao sao os da lista", sorted(set(nomes_novos) ^ set(nomes_lista))[:10])
    assert mudados == sorted(mudados_esperados), ("os mudados nao sao os esperados", mudados, sorted(mudados_esperados))
    out = ["DIFF DO KERNEL EMBUTIDO %s (%s) -> %s (%s)" % (va, h0, vb, h1), "", "novos (%d):" % len(novos)]
    out += ["  + %s  %s  %d B" % (k, sha(E1[k].encode("utf-8"))[:16], len(E1[k].encode("utf-8"))) for k in novos]
    out += ["", "removidos (%d):" % len(removidos)] + ["  - " + k for k in removidos]
    out += ["", "mudados (%d):" % len(mudados)] + ["  ~ %s  %s -> %s" % (k, sha(E0[k].encode("utf-8"))[:16], sha(E1[k].encode("utf-8"))[:16]) for k in mudados]
    out += ["", frase_final % {"vb": vb, "n": len(novos), "a": len(E0), "b": len(E1)}]
    return "\n".join(out) + "\n", {"novos": len(novos), "removidos": 0, "mudados": mudados, "h0": h0, "h1": h1}


def diff_u(base, cand, va, vb, h0, h1):
    dif = shutil.which("diff"); assert dif, "diff -u nao esta no PATH"
    r = subprocess.run([dif, "-u", "--label", "um.py %s %s" % (va, h0), "--label", "um.py %s %s" % (vb, h1), base, cand], capture_output=True)
    assert r.returncode in (0, 1), ("diff -u falhou", r.returncode, r.stderr[:300])
    return r.stdout, dif, r.returncode


def grava(p, b):
    if os.path.exists(p):
        bk = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bk, "wb").write(open(p, "rb").read())
    open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)


FRASE_V412 = "a %(vb)s acrescenta %(n)d modulos novos ao kernel embutido (%(a)d -> %(b)d arquivos); nenhum removido; os mudados acima sao os que importam os novos ou os contam"
FRASE_V413 = ("a %(vb)s acrescenta %(n)d modulos novos ao kernel embutido (%(a)d -> %(b)d arquivos); nenhum removido; os mudados acima sao a raiz, que importa os novos, "
              "e o modulo corrigido, que troca so' a docstring (o codigo e' identico)")
if "--reproduzir-v412" in sys.argv:
    dest = sys.argv[sys.argv.index("--reproduzir-v412") + 1]; os.makedirs(dest, exist_ok=True)
    REC = json.load(open(os.path.join(V412, "DIFFS_v412_RECIBO.json"), encoding="utf-8"))
    rb, rc = open(REC["base"]["path"], "rb").read(), open(REC["candidato"]["path"], "rb").read()
    assert sha(rb) == REC["base"]["sha256"] and sha(rc) == REC["candidato"]["sha256"], "os dois um.py pinados pelo recibo da v412 nao estao no disco com o sha256 do recibo"
    KN = json.load(open(os.path.join(V412, "kernel_modulos_novos_v412.json"), encoding="utf-8"))
    nomes = [os.path.splitext(os.path.basename(x))[0] for x in KN["novos"]]
    txt, d = diff_kernel(rb, rc, "v411", "v412", nomes, REC["DIFF_KERNEL_v412.txt"]["mudados"], FRASE_V412)
    pk = os.path.join(dest, "DIFF_KERNEL_v412.txt"); grava(pk, txt.encode("utf-8"))
    out_u, dif, rcd = diff_u(REC["base"]["path"], REC["candidato"]["path"], "v411", "v412", d["h0"], d["h1"])
    pd = os.path.join(dest, "DIFF_v411_v412.diff"); grava(pd, out_u)
    ok_k = sha(txt.encode("utf-8")) == REC["DIFF_KERNEL_v412.txt"]["sha256"] == sha(open(os.path.join(V412, "DIFF_KERNEL_v412.txt"), "rb").read())
    ok_u = sha(out_u) == REC["DIFF_v411_v412.diff"]["sha256"]
    print("REPRODUCAO DA v412:", "OS DOIS DIFFS SAO OS PUBLICADOS, BYTE A BYTE" if (ok_k and ok_u) else "DIFERENTE", "| kernel", ok_k, "| diff -u", ok_u)
    sys.exit(0 if (ok_k and ok_u) else 1)
ESP = json.load(open(os.path.join(V, "ESPERADOS_v413.json"), encoding="utf-8")); assert ESP.get("gerador") == "esperados_v413_foco.py" and not ESP.get("ensaio")
AP = sorted(glob.glob(os.path.join(V, "APLICADO_AO_CANONICO_*.json"))); assert AP, "nenhum APLICADO_AO_CANONICO_*.json: a v413 nao foi instalada por instalar_v413.py"
BASE = json.load(open(AP[-1], encoding="utf-8"))["backups"]["um.py"]["backup"]; CAND = os.path.join(NOS, "um.py")
rb, rc = open(BASE, "rb").read(), open(CAND, "rb").read()
assert sha(rb)[:16] == ESP["origem_sha16"], ("o backup nao e' a v412 selada", sha(rb)[:16])
assert sha(rc)[:16] == ESP["candidato_sha16"] and len(rc) == ESP["candidato_bytes"], ("o um.py do Nos nao e' o candidato pinado", sha(rc)[:16])
CF = json.load(open(os.path.join(V, "CONFERENCIA_POS_RITO_v413_FOCO.json"), encoding="utf-8")); assert CF["ok"] is True and CF["um_py_sha16"] == sha(rc)[:16], "o conferidor nao bateu: nao faco os diffs"
KN = json.load(open(os.path.join(V, "kernel_modulos_novos_v413.json"), encoding="utf-8"))
nomes = [os.path.splitext(os.path.basename(x))[0] for x in KN["novos"]]
assert sorted("TGLExt/" + n + ".lean" for n in nomes) == sorted(ESP["bundle_sha256"])
txt, d = diff_kernel(rb, rc, "v412", "v413", nomes, ["TGLExt.lean"] + list(ESP["kernel_corrigido"]), FRASE_V413)
pk = os.path.join(V, "DIFF_KERNEL_v413.txt"); grava(pk, txt.encode("utf-8"))
out_u, dif, rcd = diff_u(BASE, CAND, "v412", "v413", d["h0"], d["h1"])
pd = os.path.join(V, "DIFF_v412_v413.diff"); grava(pd, out_u)
rec = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "por": "pos_rito\\diffs_v413.py", "base": {"path": BASE, "sha256": sha(rb), "bytes": len(rb)},
       "candidato": {"path": CAND, "sha256": sha(rc), "bytes": len(rc)},
       "DIFF_KERNEL_v413.txt": {"sha256": sha(open(pk, "rb").read()), "bytes": os.path.getsize(pk), "novos": d["novos"], "removidos": 0, "mudados": d["mudados"]},
       "DIFF_v412_v413.diff": {"sha256": sha(out_u), "bytes": len(out_u), "ferramenta": dif, "rc": rcd}}
pr = os.path.join(V, "DIFFS_v413_RECIBO.json"); grava(pr, json.dumps(rec, ensure_ascii=False, indent=1).encode("utf-8"))
print("DIFF_KERNEL_v413.txt %s | DIFF_v412_v413.diff: %d B sha16 %s | recibo %s" % (rec["DIFF_KERNEL_v413.txt"]["sha256"][:16], len(out_u), sha(out_u)[:16], pr))
