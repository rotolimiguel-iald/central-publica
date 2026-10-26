# -*- coding: utf-8 -*-
"""CONFERÊNCIA FINAL INDEPENDENTE da custódia de uma versão (C15; molde: conferencia_final_v397.py). O cético mecânico: refaz do zero,
SEM importar nada do pacote G1 nem da esteira (só a biblioteca padrão), as afirmações que a custódia faz. Só leitura (rede: GET no raw
do GitHub e no site). Fail-closed: cada item ok/FALHA. Os dois literais de hoje (1426 formais, 29229 declarações) viram contagens
DERIVADAS do manifesto de prova que o próprio selo pina (o item 2 já o confere por hash).

 1. o selo do Nós: um.py vNNN = o pino; o um.py do Nós, do espelho e do cofre têm os mesmos bytes;
 2. o cofre um_unificado_vNNN: cada artefato que o selo lista e que está no cofre bate com o sha256 do selo;
 3. o cofre tgl_kernel_vNNN: cada arquivo formal do manifesto de prova bate; nenhuma declaração fora do trio;
 4. o GitHub (raw) serve o um.py e o selo com os bytes do pino; o README raw traz o pino;
 5. o site no ar: o index traz «vNNN · <pin16>» e o read-brief/llms citam o pino;
 6. os dois repositórios: HEAD = origin/main, árvore sem mudança rastreada pendente nos caminhos da custódia.
Uso: python conferencia.py vNNN --saida ARQUIVO.json [--sem-rede]   (exit 0 só se tudo ok)"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path
from urllib.parse import quote

NOS = Path(os.environ.get("G1_RAIZ_NOS") or r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
TB = Path(os.environ.get("G1_RAIZ_TB") or r"C:\IALD\Artigo\the_boundary")
ESP = TB / "Um (absoluto) \u2014 Grande Atrator"
CEN = Path(os.environ.get("G1_RAIZ_CEN") or r"C:\IALD\Central de Patentes")
RAW = "https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/"
SITE = "https://teoriadagravitacaoluminodinamica.com/"
TRIO = ("propext", "Classical.choice", "Quot.sound")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def get(url):
    rq = urllib.request.Request(url, headers={"Cache-Control": "no-cache", "User-Agent": "conferencia-final-g1"})
    with urllib.request.urlopen(rq, timeout=180) as r:
        return r.read()


def _git_exe():
    """O git do PATH, ou os lugares usuais do Windows (tarefa agendada roda com PATH mínimo); G1_GIT_EXE força (ensaios). Ausente: «git» e a falha aparece."""
    f = os.environ.get("G1_GIT_EXE")
    if f:
        return f
    w = shutil.which("git")
    if w:
        return w
    for cand in (r"C:\Program Files\Git\cmd\git.exe", r"C:\Program Files\Git\bin\git.exe", r"C:\Program Files (x86)\Git\cmd\git.exe"):
        if os.path.isfile(cand):
            return cand
    return "git"


def git(repo, *a):
    """stdout do git. Falha (git ausente, rc != 0) LEVANTA: antes devolvia «» e dois «» eram «HEAD = origin/main» — falha de leitura virava «ok»."""
    try:
        r = subprocess.run([_git_exe(), "-C", str(repo)] + list(a), capture_output=True, text=True, encoding="utf-8", errors="replace")
    except OSError as e:
        raise RuntimeError("git não executou: %r" % (e,))
    if r.returncode != 0:
        raise RuntimeError("git %s falhou (rc %s): %s" % (" ".join(a)[:70], r.returncode, (r.stderr or r.stdout).strip()[-160:]))
    return r.stdout.strip()


def conferir(v, rede=True):
    V, KV = CEN / "vault" / "originals_copy" / ("um_unificado_" + v), CEN / "vault" / "originals_copy" / ("tgl_kernel_" + v)
    R = []

    def item(nome, ok, det=""):
        R.append((nome, bool(ok), det))
        print("%-6s %s %s" % ("ok" if ok else "FALHA", nome, det))

    selo = json.loads((NOS / "um_absoluto_selo.json").read_text(encoding="utf-8"))
    pin = selo["sha256"]["um.py"]
    p16 = pin[:16]
    b_nos, b_esp, b_cof = (NOS / "um.py").read_bytes(), (ESP / "um.py").read_bytes(), (V / "um.py").read_bytes()
    item("1 selo do Nós = %s e o pino" % v, selo.get("um_version") == v and sha(b_nos) == pin, p16)
    item("1 um.py igual no Nós, no espelho e no cofre", sha(b_esp) == pin and sha(b_cof) == pin, "%d bytes" % len(b_nos))
    lis = selo["sha256"]
    no_cofre = [n for n in lis if (V / n).is_file()]
    div = [n for n in no_cofre if sha((V / n).read_bytes()) != lis[n]]
    item("2 cofre %s: artefatos do selo presentes conferem" % v, no_cofre and not div,
         "%d conferidos, %d divergentes, %d do selo fora do cofre" % (len(no_cofre), len(div), len(lis) - len(no_cofre)))
    pm_raw = (KV / "tgl_kernel_proof_manifest.json").read_bytes()
    item("3 o manifesto de prova do cofre do kernel é o que o selo pina", sha(pm_raw) == selo["sha256"].get("tgl_kernel_proof_manifest.json"))
    pm = json.loads(pm_raw.decode("utf-8"))
    ff = pm["formal_files_sha256"]
    kdiv = [r for r, h in ff.items() if not (KV / r).is_file() or sha((KV / r).read_bytes()) != h]
    fora = [k for k, x in pm["axiom_report"].items() if any(a not in TRIO for a in (x or []))]
    item("3 cofre do kernel: arquivos formais conferem", len(ff) > 0 and not kdiv, "%d formais, %d divergentes/ausentes" % (len(ff), len(kdiv)))
    item("3 axiom_report no trio", len(pm["axiom_report"]) > 0 and not fora, "%d declarações, %d fora" % (len(pm["axiom_report"]), len(fora)))
    A3 = "Um (absoluto) \u2014 Grande Atrator/"
    if rede:
        try:
            gu = get(RAW + quote(A3 + "um.py"))
            gs = get(RAW + quote(A3 + "um_absoluto_selo.json"))
            gr = get(RAW + "README.md").decode("utf-8", "replace")
            item("4 GitHub raw: um.py = pino", sha(gu) == pin, "%d bytes" % len(gu))
            item("4 GitHub raw: selo = o selo do Nós", sha(gs) == sha((NOS / "um_absoluto_selo.json").read_bytes()))
            item("4 GitHub raw: README traz o pino", p16 in gr)
        except Exception as e:  # noqa: BLE001
            item("4 GitHub raw", False, repr(e)[:160])
        try:
            si = get(SITE).decode("utf-8", "replace")
            sb = get(SITE + "read-brief.md").decode("utf-8", "replace")
            sl = get(SITE + "llms.txt").decode("utf-8", "replace")
            item("5 site no ar: index com «%s · pin16»" % v, ("%s \u00b7 %s" % (v, p16)) in si)
            item("5 site no ar: read-brief e llms citam o pino", p16 in sb and p16 in sl)
        except Exception as e:  # noqa: BLE001
            item("5 site no ar", False, repr(e)[:160])
    for nome, repo, caminhos in (("espelho", TB, ["."]),
                                 ("Central", CEN, ["vault/originals_copy/um_unificado_" + v, "vault/originals_copy/tgl_kernel_" + v, "fronteira_tgl",
                                                   "patents/_formula_completa", "memory/TGL_ATLAS.md"])):
        try:
            h, o = git(repo, "rev-parse", "HEAD"), git(repo, "rev-parse", "origin/main")
            pend = git(repo, "status", "--porcelain", "--untracked-files=no", "--", *caminhos)
        except RuntimeError as e:
            item("6 %s: HEAD = origin/main e nada pendente na custódia" % nome, False, "git falhou: %s" % str(e)[:200])
            continue
        item("6 %s: HEAD = origin/main e nada pendente na custódia" % nome, bool(h) and h == o and not pend, "%s %s" % (h[:8], ("| pendente: " + pend[:120]) if pend else ""))
    return R, pin


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("versao")
    ap.add_argument("--saida", required=True)
    ap.add_argument("--sem-rede", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    R, pin = conferir(a.versao, rede=not a.sem_rede)
    n_ok = sum(1 for _, ok, _ in R if ok)
    print("\nCONFERÊNCIA FINAL: %d/%d ok" % (n_ok, len(R)))
    Path(a.saida).write_text(json.dumps({"itens": [{"item": n, "ok": ok, "detalhe": d} for n, ok, d in R], "ok": n_ok, "total": len(R), "pin": pin, "versao": a.versao},
                                        ensure_ascii=False, indent=1), encoding="utf-8")
    return 0 if n_ok == len(R) else 1


if __name__ == "__main__":
    sys.exit(main())
