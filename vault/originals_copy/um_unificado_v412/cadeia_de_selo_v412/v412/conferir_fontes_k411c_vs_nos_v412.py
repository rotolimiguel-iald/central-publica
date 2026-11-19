# -*- coding: utf-8 -*-
"""conferir_fontes_k411c_vs_nos_v412.py -- (claude-construtor-v412, 17/11/2026) ANTES de copiar o sandbox: (1) MEDE o tamanho da origem C:\\t\\k411c\\final (sem seguir juncoes:
a juncao .lake\\packages aponta para a mathlib compilada do k404c e NAO e' copiada) e o espaco livre do disco C:; (2) confere por sha256 que as FONTES do sandbox de origem
(todo .lean fora de .lake, a raiz TGLExt.lean, TGL.lean, lakefile.toml, lean-toolchain, lake-manifest.json) sao as do kernel do Nos v411 SELADO (so' leitura nos dois);
(3) confere que NENHUM dos 34 modulos do manifesto da v412 existe no Nos nem na origem (fonte ou objeto compilado em .lake\\build), comparando sem caixa (o disco do Windows nao
distingue caixa). Arquivo que so' existe num dos lados e' listado (nao e' erro por si). Grava CONFERENCIA_FONTES_K411C_v412.json. Molde: v411\\conferir_fontes_k410c_vs_nos_v411.py
(so' os rotulos sobem; a medicao do tamanho e a conferencia dos 34 nomes sao novas). Nada e' escrito fora desta pasta.
uso: C:\\Python314\\python.exe -B -X utf8 conferir_fontes_k411c_vs_nos_v412.py"""
import hashlib, json, os, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS_K = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós", "tgl_kernel")
SB = os.path.join("C:" + os.sep, "t", "k411c", "final")
MAN = os.path.join(HERE, "insumos", "MANIFESTO_PEDRAS_v412.json")
SAIDA = os.path.join(HERE, "CONFERENCIA_FONTES_K411C_v412.json")
EXTRA = ["TGLExt.lean", "TGL.lean", "lakefile.toml", "lean-toolchain", "lake-manifest.json"]


def fontes(raiz):
    out = {}
    for dp, dn, fn in os.walk(raiz):
        dn[:] = [d for d in dn if d not in (".lake", ".git", "probe")]
        for f in fn:
            if f.endswith(".lean") and ".bak_" not in f:
                p = os.path.join(dp, f)
                out[os.path.relpath(p, raiz).replace(os.sep, "/")] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    for f in EXTRA:
        p = os.path.join(raiz, f)
        if os.path.exists(p):
            out[f] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return out


def tamanho_sem_juncoes(raiz):
    tot = n = 0; juncoes = []
    pilha = [raiz]
    while pilha:
        d = pilha.pop()
        with os.scandir(d) as it:
            for e in it:
                if e.is_junction() or e.is_symlink():
                    juncoes.append(e.path); continue
                if e.is_dir(follow_symlinks=False):
                    pilha.append(e.path)
                elif e.is_file(follow_symlinks=False):
                    tot += e.stat(follow_symlinks=False).st_size; n += 1
    return tot, n, juncoes


tam, narq, junc = tamanho_sem_juncoes(SB)
du = shutil.disk_usage("C:" + os.sep)
a, b = fontes(NOS_K), fontes(SB)
comuns = sorted(set(a) & set(b))
dif = [r for r in comuns if a[r] != b[r]]
so_nos = sorted(set(a) - set(b))
so_sb = sorted(set(b) - set(a))
selo = json.load(open(os.path.join(os.path.dirname(NOS_K), "um_absoluto_selo.json"), encoding="utf-8"))
man = json.load(open(MAN, encoding="utf-8"))
nomes = [m["modulo"] for m in man["modulos"]]
colide = {}
for raiz, rot in ((NOS_K, "nos"), (SB, "k411c")):
    d_ = os.path.join(raiz, "TGLExt")
    existentes = {f.lower() for f in os.listdir(d_)}
    lib = os.path.join(raiz, ".lake", "build", "lib", "lean", "TGLExt")
    objs = {f.lower() for f in os.listdir(lib)} if os.path.isdir(lib) else set()
    for n_ in nomes:
        hit = [x for x in (n_.lower() + ".lean", n_.lower()) if x in existentes] + [x for x in (n_.lower() + ".olean", n_.lower() + ".ilean", n_.lower() + ".trace") if x in objs]
        if hit:
            colide.setdefault(n_, {})[rot] = hit
rep = {"nos_kernel": NOS_K, "sandbox_origem": SB, "selo_um_version": selo.get("um_version"),
       "origem_bytes_sem_juncoes": tam, "origem_gb_sem_juncoes": round(tam / 1e9, 3), "origem_arquivos": narq, "origem_juncoes_nao_seguidas": junc,
       "disco_C_livre_bytes": du.free, "disco_C_livre_gb": round(du.free / 1e9, 3), "disco_C_total_gb": round(du.total / 1e9, 3),
       "folga_depois_da_copia_gb": round((du.free - tam) / 1e9, 3),
       "n_nos": len(a), "n_sandbox": len(b), "n_comuns": len(comuns), "n_diferentes": len(dif),
       "diferentes": dif[:50], "so_no_nos": so_nos[:50], "so_no_sandbox": so_sb[:50], "todas_as_comuns_iguais": not dif, "todas_as_do_nos_no_sandbox": not so_nos,
       "identico": (not dif and not so_nos and not so_sb),
       "modulos_v412": len(nomes), "colisoes_de_nome_de_modulo_sem_caixa": colide, "sem_colisao_de_nome_de_modulo": not colide}
open(SAIDA + ".tmp", "w", encoding="utf-8").write(json.dumps(rep, ensure_ascii=False, indent=1)); os.replace(SAIDA + ".tmp", SAIDA)
print(json.dumps({k: v for k, v in rep.items() if k not in ("diferentes",)}, ensure_ascii=False, indent=1)[:3000])
ok = rep["selo_um_version"] == "v411" and rep["todas_as_comuns_iguais"] and rep["todas_as_do_nos_no_sandbox"] and not colide and rep["folga_depois_da_copia_gb"] > 20
print("CONFERENCIA:", "OK" if ok else "FALHA")
sys.exit(0 if ok else 1)
