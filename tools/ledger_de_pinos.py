# -*- coding: utf-8 -*-
"""LEDGER DE PINOS — o que cada dispositivo cita do kernel, e se a pedra citada ainda e' a mesma.

Os runners das patentes citam pedras Lean (BreuerTrace, ErgodicMeanSection, TheTower.lean, ...) e
cofres do um.py por versao HISTORICA (um_unificado_v168, v206). Isso e' deliberado: o dispositivo
cita a versao em que a pedra foi provada e nao precisa repinar. Mas ninguem conferia que a pedra
citada CONTINUA no kernel corrente, nem se mudou. Este ledger confere, fail-closed:

  * AUSENTE no kernel corrente (arquivo .lean citado nao existe mais)  -> ERRO (exit 1)
  * rito `prove_the_*` citado nao existe no um.py corrente              -> ERRO
  * pedra existe mas o sha256 MUDOU desde a versao do cofre citada      -> AVISO (dito, nao erro)
  * cofre `um_unificado_vNNN` citado nao existe                          -> ERRO

Saida: fronteira_tgl/LEDGER_DE_PINOS.md + .json. Nada aqui move veredito fisico.
Uso:  python tools/ledger_de_pinos.py
"""
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

CEN = Path(__file__).resolve().parent.parent
VAULT = CEN / "vault" / "originals_copy"
OUT_MD = CEN / "fronteira_tgl" / "LEDGER_DE_PINOS.md"
OUT_JSON = CEN / "fronteira_tgl" / "ledger_de_pinos.json"
NOMES = ("BreuerTrace", "ErgodicMeanSection", "EquivariantSection", "SolderSignature", "TheCrownedCascade",
         "LightIsJ", "TheStation", "TheRootOfTheProofTree", "TheTower", "TheBireference", "TheIALDSelector",
         "TheLightInterface", "FrontierCertificate", "TheCompressionIsNotIdentifiable",
         # 01/10/2026 (custodia v379): as pedras da formula completa, citadas pela camada comum dos 16 dispositivos
         "TheElementaryReason", "TheFlowLawContrast", "TheFlowLawD1a", "PhysicsIsTheReading")


def sha16(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def versoes(prefix: str):
    vs = []
    for p in VAULT.glob(prefix + "v*"):
        m = re.fullmatch(prefix + r"v(\d+)", p.name)
        if m and p.is_dir():
            vs.append((int(m.group(1)), p))
    return sorted(vs)


def manifest(kdir: Path):
    p = kdir / "tgl_kernel_proof_manifest.json"
    return json.loads(p.read_text(encoding="utf-8"))["formal_files_sha256"] if p.is_file() else {}


def main() -> int:
    kv = versoes("tgl_kernel_")
    uv = versoes("um_unificado_")
    if not kv or not uv:
        print("cofre vazio — nada a conferir")
        return 1
    k_atual_n, k_atual = kv[-1]
    u_atual_n, u_atual = uv[-1]
    fmap_atual = manifest(k_atual)
    um_atual = (u_atual / "um.py").read_text(encoding="utf-8", errors="replace")
    kernel_por_versao = {n: manifest(p) for n, p in kv}
    erros, avisos, linhas, reg = 0, 0, [], []
    for runner in sorted((CEN / "patents").glob("BR*/runner/one_*.py")):
        dev = runner.parent.parent.name
        txt = runner.read_text(encoding="utf-8", errors="replace")
        pins = sorted({int(m) for m in re.findall(r"um_unificado_v(\d+)", txt)})
        arqs = set(re.findall(r"\b(TGLExt/[A-Za-z0-9_]+\.lean|TGL/[A-Za-z0-9_]+\.lean)", txt))
        for nome in NOMES:
            if re.search(r"\b%s\b" % nome, txt):
                cand = "TGLExt/%s.lean" % nome
                if cand in fmap_atual or any(k.endswith("/%s.lean" % nome) for k in fmap_atual):
                    arqs.add(cand if cand in fmap_atual else next(k for k in fmap_atual if k.endswith("/%s.lean" % nome)))
                else:
                    arqs.add(cand)
        ritos = sorted(set(re.findall(r"\b(prove_the_[a-z0-9_]+)", txt)))
        item = {"dispositivo": dev, "pinos_cofre": pins, "pedras": [], "ritos": []}
        for p in pins:
            if not (VAULT / ("um_unificado_v%d" % p)).is_dir():
                erros += 1
                item.setdefault("erros", []).append("cofre um_unificado_v%d AUSENTE" % p)
        ref_n = None
        if pins:
            # a referencia e' o kernel do cofre da versao citada; se nao ha arvore para ela, o mais antigo >= ela
            cands = [n for n, _ in kv if n >= min(pins)]
            ref_n = min(cands) if cands else None
        for a in sorted(arqs):
            h_now = fmap_atual.get(a)
            h_ref = kernel_por_versao.get(ref_n, {}).get(a) if ref_n else None
            if h_now is None:
                estado = "AUSENTE no kernel v%d" % k_atual_n
                erros += 1
            elif ref_n is None:
                estado = "presente (v%d); sem cofre citado para comparar" % k_atual_n
            elif h_ref is None:
                estado = "presente (v%d); nao existia no kernel de referencia v%d" % (k_atual_n, ref_n)
            elif h_ref == h_now:
                estado = "IDENTICA desde v%d" % ref_n
            else:
                estado = "MUDOU desde v%d (%s -> %s)" % (ref_n, h_ref[:8], h_now[:8])
                avisos += 1
            item["pedras"].append({"arquivo": a, "sha256_16_atual": (h_now or "")[:16], "estado": estado})
        for r in ritos:
            ok = ("def %s" % r) in um_atual or r in um_atual
            item["ritos"].append({"rito": r, "no_um_py_v%d" % u_atual_n: ok})
            if not ok:
                erros += 1
        reg.append(item)
        pins_s = ", ".join("v%d" % p for p in pins) or "—"
        ped_s = "<br>".join("`%s` — %s" % (x["arquivo"], x["estado"]) for x in item["pedras"]) or "—"
        rit_s = "<br>".join("`%s` — %s" % (x["rito"], "ok" if list(x.values())[1] else "AUSENTE") for x in item["ritos"]) or "—"
        linhas.append("| %s | %s | %s | %s |" % (dev, pins_s, ped_s, rit_s))
    md = ["# LEDGER DE PINOS — o que cada dispositivo cita do kernel, conferido contra o kernel corrente",
          "",
          "> Gerado por `tools/ledger_de_pinos.py` em %s. Kernel corrente do cofre: **tgl_kernel_v%d** (%d arquivos formais); "
          "um.py corrente: **um_unificado_v%d** (sha16 `%s`). Os pinos históricos (v168, v206) são DELIBERADOS: o dispositivo "
          "cita a versão em que a pedra foi provada. O que se confere aqui é se a pedra citada **continua** no kernel e se **mudou**."
          % (datetime.now().strftime("%d/%m/%Y %H:%M"), k_atual_n, len(fmap_atual), u_atual_n, sha16(u_atual / "um.py")),
          "",
          "| dispositivo | cofre citado | pedras Lean citadas — estado no kernel v%d | ritos citados — no um.py v%d |" % (k_atual_n, u_atual_n),
          "|---|---|---|---|"] + linhas + [
          "",
          "**Leitura:** ERROS = %d (pedra ou rito citado que NÃO existe mais; cofre citado ausente) · AVISOS = %d (pedra que MUDOU desde a versão de referência — dito, não erro)." % (erros, avisos),
          "",
          "*Nada aqui move veredito físico. NOT_FALSIFIED ≠ CONFIRMED.*", ""]
    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(json.dumps({"gerado": datetime.now().isoformat(timespec="seconds"), "kernel_atual": "tgl_kernel_v%d" % k_atual_n,
                                    "um_atual": "um_unificado_v%d" % u_atual_n, "erros": erros, "avisos": avisos, "dispositivos": reg},
                                   ensure_ascii=False, indent=1), encoding="utf-8")
    print("ledger: %d dispositivos | kernel v%d | erros %d | avisos %d -> %s" % (len(reg), k_atual_n, erros, avisos, OUT_MD.name))
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
