# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: conferencia das pedras do Kimi (v412/candidatas_kimi) e da entrega do Codex
(v413/ponte_tm2_codex) sobre a caixa do kernel da v412 (C:\\t\\k412c\\final), mais a sonda da contagem da gerencia.

Regras: so' o binario do Lean (nunca lake); nada se escreve nas oficinas do Kimi ou do Codex (os .olean, logs e o
recibo ficam em k412c\\ desta pasta). As pedras do Kimi importam quatro modulos da gerencia pelo nome de candidata
(AContagemEACarga, AMaquinaEALeitura, OPassoEOFim, CamadaCientifica); na v412 eles estao instalados como TGLExt.<nome>.
Por isso as pedras do Kimi sao COPIADAS byte a byte para k412c\\src e so' essas linhas de import sao reescritas; o
recibo guarda o sha256 do original, o da copia e cada linha trocada. As fontes do Codex compilam no lugar, sem copia.
As duas pedras do Kimi que o Codex substituiu (APonteAoTM2 e AMaquinaTM2DaVerificacao, mesmos nomes de modulo) nao
entram: entram as versoes do Codex. Recibo: k412c\\CONFERENCIA_K412C.json."""
import hashlib, json, os, re, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
OUT = AQUI / "k412c"
SRC = OUT / "src"
BUILD = OUT / "build"
LOGS = OUT / "logs"
for d in (SRC, BUILD, LOGS):
    d.mkdir(parents=True, exist_ok=True)

LEAN = r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe"
CAIXA = Path(r"C:\t\k412c\final")
SELADO = Path(r"C:\t\k412c\imp_3e741dcaa58ef2b8\tgl_kernel")
V412 = AQUI.parents[1] / "v412"
KIMI = V412 / "candidatas_kimi"
CODEX = AQUI.parent / "ponte_tm2_codex"
TRIO = {"propext", "Classical.choice", "Quot.sound"}
REESCRITA = {"AContagemEACarga", "AMaquinaEALeitura", "OPassoEOFim", "CamadaCientifica"}

assert Path(LEAN).exists(), "lean.exe ausente"
assert (CAIXA / ".lake" / "build" / "lib" / "lean" / "TGLExt.olean").exists(), "caixa k412c sem build"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# (modulo, pasta da fonte, se e' copia reescrita do Kimi, papel)
KIMI_ORDEM = ["OResumoEPsiBit", "AFronteiraEOUnicoPortao", "OPsiBitDaFormula", "ACurvaEAEstado", "AFitaEOIndice",
              "AIdentidadePreservada", "AClausulaExemplificativa", "APropostaDaTensao", "OCustoEAIsometria",
              "APonteDeCookLevin", "ONomeEBeta", "OPolinomioFixoEBeta", "ORazaoDoColapsoEBeta"]
KIMI_SONDAS = ["sonda_cadeia_caminho", "sonda_n0_contraexemplo"]
CODEX_ORDEM = [("APonteAoTM2", CODEX), ("AMaquinaTM2DaVerificacao", CODEX),
               ("SimBase", CODEX / "simulacao"), ("SimExterior", CODEX / "simulacao"),
               ("SimLiteral", CODEX / "simulacao"), ("SimCompleta", CODEX / "simulacao"),
               ("RelogioBeta", CODEX / "leitura_beta"), ("LeituraBeta", CODEX / "leitura_beta"),
               ("QuantizacaoBeta", CODEX / "leitura_beta"), ("Reconstrucao", CODEX / "leitura_beta"),
               ("PonteLeituraBeta", CODEX / "leitura_beta"), ("EntregaBeta", CODEX / "leitura_beta")]
GERENCIA = [("SondaContagem", AQUI / "sonda_contagem")]

# 1. a caixa e' a do selo?
fontes_caixa = sorted(p.name for p in (CAIXA / "TGLExt").glob("*.lean"))
fontes_selado = sorted(p.name for p in (SELADO / "TGLExt").glob("*.lean"))
difere = [n for n in fontes_caixa if n in fontes_selado and sha(CAIXA / "TGLExt" / n) != sha(SELADO / "TGLExt" / n)]
caixa = {
    "caixa": str(CAIXA), "selado_materializado": str(SELADO),
    "um_py_selado_sha256": sha(SELADO.parent / "um.py"),
    "n_fontes_TGLExt_caixa": len(fontes_caixa), "n_fontes_TGLExt_selado": len(fontes_selado),
    "so_na_caixa": sorted(set(fontes_caixa) - set(fontes_selado)),
    "so_no_selado": sorted(set(fontes_selado) - set(fontes_caixa)),
    "fontes_com_bytes_diferentes": difere,
    "TGLExt_lean_igual": sha(CAIXA / "TGLExt.lean") == sha(SELADO / "TGLExt.lean"),
    "TGLExt_olean_sha256": sha(CAIXA / ".lake" / "build" / "lib" / "lean" / "TGLExt.olean"),
    "TGLExt_olean_mtime": time.strftime("%Y-%m-%d %H:%M:%S",
                                        time.localtime((CAIXA / ".lake/build/lib/lean/TGLExt.olean").stat().st_mtime)),
}
print("caixa: fontes %d/%d, diferentes %d, so_na_caixa %d, so_no_selado %d, TGLExt.lean igual %s" % (
    len(fontes_caixa), len(fontes_selado), len(difere), len(caixa["so_na_caixa"]), len(caixa["so_no_selado"]),
    caixa["TGLExt_lean_igual"]), flush=True)

# 2. LEAN_PATH: a caixa da v412 e o build desta conferencia; nada das oficinas
lib = CAIXA / ".lake"
caminhos = [str(lib / "build" / "lib" / "lean")]
caminhos += [str(p / ".lake" / "build" / "lib" / "lean") for p in sorted((lib / "packages").iterdir())
             if (p / ".lake" / "build" / "lib" / "lean").exists()]
caminhos.append(str(BUILD))
env = dict(os.environ)
env["LEAN_PATH"] = ";".join(caminhos)
versao = subprocess.run([LEAN, "--version"], capture_output=True, text=True).stdout.strip()


def copia_reescrita(mod):
    orig = KIMI / (mod + ".lean")
    raw = orig.read_bytes()
    txt = raw.decode("utf-8")
    trocas = []
    linhas = txt.split("\n")
    for i, l in enumerate(linhas):
        m = re.match(r"^import\s+(\S+)\s*\r?$", l)
        if m and m.group(1) in REESCRITA:
            nova = l.replace("import " + m.group(1), "import TGLExt." + m.group(1), 1)
            trocas.append({"linha": i + 1, "antes": l.rstrip("\r"), "depois": nova.rstrip("\r")})
            linhas[i] = nova
    novo = "\n".join(linhas).encode("utf-8")
    dest = SRC / (mod + ".lean")
    tmp = SRC / (mod + ".lean.tmp")
    tmp.write_bytes(novo)
    assert tmp.read_bytes() == novo
    tmp.replace(dest)
    return {"original": str(orig), "sha256_original": sha(orig), "copia": str(dest), "sha256_copia": sha(dest),
            "trocas_de_import": trocas}, dest


def compila(mod, pasta, arquivo):
    t0 = time.time()
    r = subprocess.run([LEAN, "-o", str(BUILD / (mod + ".olean")), arquivo.name], env=env, cwd=str(pasta),
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    saida = (r.stdout or "") + (r.stderr or "")
    (LOGS / (mod + ".log")).write_text("FONTE: %s\nSHA256: %s\nRC: %d\nSAIDA:\n%s" % (arquivo, sha(arquivo),
                                                                                   r.returncode, saida),
                                      encoding="utf-8")
    ax = [l.strip() for l in saida.split("\n") if "depends on axioms" in l or "does not depend" in l]
    fora = []
    for l in ax:
        m = re.search(r"depends on axioms: \[(.*)\]", l)
        if m:
            usados = {a.strip() for a in m.group(1).split(",") if a.strip()}
            if usados - TRIO:
                fora.append(l)
    return {"modulo": mod, "fonte": str(arquivo), "sha256_fonte": sha(arquivo), "rc": r.returncode,
            "segundos": round(time.time() - t0, 1), "avisos": saida.count("warning:"), "erros": saida.count("error:"),
            "sorryAx": "sorryAx" in saida, "n_axiomas_impressos": len(ax), "axiomas": ax,
            "fora_do_trio": fora, "cauda_da_saida_se_falhou": saida[-3000:] if r.returncode else ""}


resultado = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "lean": versao, "caixa": caixa,
             "lean_path": caminhos, "copias_do_kimi": {}, "modulos": [],
             "nao_conferidas_substituidas_pelo_codex": {
                 m: sha(KIMI / (m + ".lean")) for m in ("APonteAoTM2", "AMaquinaTM2DaVerificacao")}}
parou = None
falhou = set()
etapas = [(m, None, "kimi") for m in KIMI_ORDEM] + [(m, p, "codex") for m, p in CODEX_ORDEM] + \
         [(m, p, "gerencia") for m, p in GERENCIA] + [(m, None, "kimi_sonda") for m in KIMI_SONDAS]


def importa(arq):
    return [m.group(1) for m in re.finditer(r"^import\s+(\S+)", Path(arq).read_text(encoding="utf-8"), re.M)]


for mod, pasta, quem in etapas:
    if quem.startswith("kimi"):
        info, arq = copia_reescrita(mod)
        resultado["copias_do_kimi"][mod] = info
        pasta_c = SRC
    else:
        arq = pasta / (mod + ".lean")
        pasta_c = pasta
    dep_falha = [i for i in importa(arq) if i in falhou]
    if dep_falha:
        falhou.add(mod)
        resultado["modulos"].append({"modulo": mod, "quem": quem, "rc": None,
                                     "pulado": "importa modulo que falhou: " + ", ".join(dep_falha)})
        print("%-28s %-10s PULADO (importa %s)" % (mod, quem, ", ".join(dep_falha)), flush=True)
        continue
    r = compila(mod, pasta_c, arq)
    r["quem"] = quem
    resultado["modulos"].append(r)
    print("%-28s %-10s RC %s | %6.1f s | avisos %d | erros %d | sorryAx %s | fora do trio %d" % (
        mod, quem, r["rc"], r["segundos"], r["avisos"], r["erros"], r["sorryAx"], len(r["fora_do_trio"])), flush=True)
    if r["rc"] != 0 or r["erros"] or r["sorryAx"]:
        falhou.add(mod)
        if not parou:
            parou = mod

ok = [m for m in resultado["modulos"] if m.get("rc") == 0 and not m.get("erros") and not m.get("sorryAx")]
resultado["resumo"] = {
    "compilaram": len(ok), "total": len(resultado["modulos"]),
    "com_aviso": [m["modulo"] for m in ok if m.get("avisos")],
    "fora_do_trio": {m["modulo"]: m["fora_do_trio"] for m in resultado["modulos"] if m.get("fora_do_trio")},
    "primeira_falha": parou,
}
rec = OUT / "CONFERENCIA_K412C.json"
tmp = OUT / "CONFERENCIA_K412C.json.tmp"
dados = json.dumps(resultado, ensure_ascii=False, indent=1).encode("utf-8")
tmp.write_bytes(dados)
assert tmp.read_bytes() == dados
tmp.replace(rec)
print("RESUMO:", json.dumps(resultado["resumo"], ensure_ascii=False), flush=True)
print("recibo:", rec, "sha16", sha(rec)[:16], flush=True)
