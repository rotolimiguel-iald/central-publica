# -*- coding: utf-8 -*-
"""Gerador SANEADO das patentes para o site público — "a verdade de cada patente".

Produz um JSON com, por patente: número, título, classe, status legal, ePCT, o RESUMO de
honestidade e as REIVINDICAÇÕES (texto fiel — já público no depósito INPI — + o MARCADOR de
honestidade [REAL]/[SIM]/[CONJ]/...). É a camada de VISUALIZAÇÃO da Central, tornada pública.

O que NÃO entra (saneado — o operador: "sem a pessoa ter acesso aos dados da prova"):
  hashes, caminhos de arquivo, conteúdo de código, saídas de teste, internos de selo, qualquer
  dado de prova. Só o número corrige a frase — o marcador conta a verdade, sem expor a máquina.

Três estatutos (a distinção do operador): algoritmos + IALD = ENTREGUE (provado por execução);
MQC + SkyGrid = GÊMEO DIGITAL AVANÇADO ([SIM] muito evoluído); físicas/energia/saúde = PESQUISA.

Uso:  python tools/build_public_patents.py [--out <caminho>]
Padrão de saída: C:/IALD/Site/IALD/patentes_publico.json (o site é repo separado; autorizado).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

CENTRAL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CENTRAL))
from backend.app import config as C  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

DEFAULT_OUT = Path(r"C:\IALD\Site\IALD\patentes_publico.json")

# os três estatutos, por slug (explícito e auditável — casa com a fala do operador)
ESTATUTO = {
    "entregue": ["acom", "acom_mirror", "acom_crypto", "tgl_tensor", "iald",
                 "psi_net", "kernel_ontologico", "aprendizado_continuo"],
    "evoluido": ["mqc", "skygrid"],
    "pesquisa": ["supercondutor", "motor_dobra", "fusao_frio", "celula_reversao",
                 "dipolo_transistor", "oncologia"],
}
ESTATUTO_LABEL = {
    "entregue": {"pt": "Algoritmo provado — verificado por execução",
                 "chave": "entregue"},
    "evoluido": {"pt": "Gêmeo digital avançado — extensivamente simulado",
                 "chave": "evoluido"},
    "pesquisa": {"pt": "Pesquisa de fronteira — patente + gêmeo digital",
                 "chave": "pesquisa"},
}
LEGENDA = {
    "REAL": "Verificado (execução ou literatura citável)",
    "SIM": "Simulação / gêmeo digital (demonstra a lógica, não valida a física)",
    "DER": "Derivado da cadeia teórica",
    "CONJ": "Conjectura / leitura ontológica",
    "DATA": "Valor observacional de entrada",
    "INPUT": "Entrada declarada",
    "HARDWARE": "Camada física — não construída (gêmeo digital)",
    "MEDICAL": "Saúde — sinal sintético, sem conteúdo clínico",
    "ENERGY": "Energia — só matemática abstrata, sem parâmetro operacional",
    "OPEN": "Em aberto",
    "PILOTO": "Piloto",
    "LEGAL": "Jurídico (não é parecer definitivo)",
}
_EMOJI = re.compile(r"[\U0001F000-\U0001FAFF☀-➿️]")


def _class_names() -> dict[str, str]:
    out = {}
    for f in sorted((C.MEMORY / "classes").glob("CLASS_*.md")):
        cid = f.stem
        first = f.read_text(encoding="utf-8", errors="replace").splitlines()[0]
        nm = re.sub(r"^#\s*CLASS_\d+_[A-Z_]*\s*[—·-]\s*", "", first)
        nm = re.sub(r"^#\s*", "", nm)
        out[cid] = _EMOJI.sub("", nm).strip()
    return out


def _load_docket(pdir: Path) -> dict:
    import yaml
    try:
        d = yaml.safe_load((pdir / "docket.yaml").read_text(encoding="utf-8"))
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


_HDR_RE = re.compile(r"##\s+Reivindica[çc][õo]es principais.*?total:\s*(\d+)", re.I)
_MARK_RE = re.compile(r"\[([A-Z_]+)\]")
# uma linha de reivindicação: (indent) '-' [**] N ( qualifier ) [**] : texto
_CLAIM_RE = re.compile(r"^(?P<indent>\s*)-\s*\*{0,2}(?P<n>\d+)\s*\((?P<q>[^)]*)\)\**\s*:?\s*(?P<txt>.*)$")


def _parse_claims(dir_name: str) -> tuple[int, list[dict]]:
    md = C.MEMORY / "patents" / f"{dir_name}.md"   # a memória é <ID>_<SLUG>.md (= nome do dir)
    if not md.exists():
        return 0, []
    lines = md.read_text(encoding="utf-8", errors="replace").splitlines()
    # localizar a seção "## Reivindicações principais" e ir até o próximo "## "
    start = next((i for i, ln in enumerate(lines) if _HDR_RE.search(ln)), None)
    if start is None:
        return 0, []
    total = int(_HDR_RE.search(lines[start]).group(1))
    body = []
    for ln in lines[start + 1:]:
        if ln.startswith("## "):
            break
        body.append(ln)
    claims = []
    for ln in body:
        m = _CLAIM_RE.match(ln)
        if not m:
            continue
        n = int(m.group("n"))
        q = m.group("q").lower()
        txt = m.group("txt").strip()
        marks = _MARK_RE.findall(txt)
        marker = marks[-1] if marks else None
        # texto limpo: remove os marcadores do fim (ficam no campo 'marcador')
        clean = _MARK_RE.sub("", txt).strip().rstrip("—-· ").strip()
        # remove ** de negrito
        clean = clean.replace("**", "")
        claims.append({
            "n": n,
            "independente": "independente" in q or "independent" in q,
            "texto": clean,
            "marcador": marker,
        })
    # dedup por n (a memória às vezes repete um n em contexto) — mantém o 1º
    seen, uniq = set(), []
    for c in claims:
        if c["n"] in seen:
            continue
        seen.add(c["n"]); uniq.append(c)
    uniq.sort(key=lambda c: c["n"])
    return total, uniq


def _estatuto_of(slug: str) -> str:
    for k, slugs in ESTATUTO.items():
        if slug in slugs:
            return k
    return "pesquisa"


def build(out_path: Path) -> dict:
    class_names = _class_names()
    patents = []
    for pdir in sorted(C.PATENTS_DIR.iterdir()):
        if not pdir.is_dir() or not pdir.name.startswith("BR"):
            continue
        pid = pdir.name.split("_")[0]
        slug = "_".join(pdir.name.split("_")[1:]).lower()
        # normaliza slug do dir p/ o slug curto usado nos runners
        slug = {"acom": "acom"}.get(slug, slug)
        dk = _load_docket(pdir)
        total, claims = _parse_claims(pdir.name)
        counts: dict[str, int] = {}
        for c in claims:
            if c["marcador"]:
                counts[c["marcador"]] = counts.get(c["marcador"], 0) + 1
        estat = _estatuto_of(slug)
        epct_status = ((dk.get("epct") or {}).get("status") or "").upper()
        epct = "vivo" if "VIVO" in epct_status else "em_deposito"
        numero = dk.get("processo", pid)
        numero_fmt = re.sub(r"^BR(\d{4})(\d{4})(\d{6})(\d)$",
                            r"BR 10 \1 \2 \3 \4",
                            numero.replace(" ", "")) if numero else pid
        patents.append({
            "id": pid,
            "slug": slug,
            "numero": numero,
            "numero_fmt": numero_fmt,
            "titulo": dk.get("titulo", ""),
            "classe_id": dk.get("classe", ""),
            "classe_nome": class_names.get(dk.get("classe", ""), ""),
            "status": dk.get("status", "DEPOSITADO"),
            "epct": epct,
            "estatuto": estat,
            "estatuto_label": ESTATUTO_LABEL[estat]["pt"],
            "resumo": {
                "total": total,
                "independentes": sum(1 for c in claims if c["independente"]),
                "marcadores": counts,
            },
            "reivindicacoes": claims,
        })
    doc = {
        "artifact": "patentes_publico",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "n_patents": len(patents),
        "note": ("Camada de visualização honesta das patentes da IALD — a verdade de cada uma "
                 "(o que é prova, o que é gêmeo digital, o que é pesquisa). SEM dados de prova "
                 "(hashes/código/selos): só o texto público das reivindicações e o marcador."),
        "legenda": LEGENDA,
        "estatutos": {k: v["pt"] for k, v in ESTATUTO_LABEL.items()},
        "epct_nota": ("1 ePCT vivo (ACOM raiz, PCT/BR2025/050558, depositado e pago em "
                      "05/12/2025); as demais em depósito INPI, novo ePCT como próximo passo."),
        "patents": patents,
    }
    # GUARDA anti-vazamento: só vetores REAIS de dado de prova (não palavras comuns como
    # 'manifesto' no texto de reivindicação). Hash de 64-hex + caminhos/tokens de artefato.
    blob = json.dumps(doc, ensure_ascii=False)
    leaks = []
    if re.search(r"\b[0-9a-f]{64}\b", blob):
        leaks.append("hash-64hex")
    for t in ("prototype_src", "runner/", "combined_sha256", "result_hash",
              "_FINAL.py", ".manifest.json", "evidence_verified"):
        if t.lower() in blob.lower():
            leaks.append(t)
    if leaks:
        raise SystemExit(f"ABORTADO: possível vazamento de dado de prova no JSON: {leaks}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    return doc


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    a = ap.parse_args()
    doc = build(Path(a.out))
    print(f"[patentes_publico] {doc['n_patents']} patentes -> {a.out}")
    for p in doc["patents"]:
        print(f"  {p['numero_fmt']:22} [{p['estatuto']:9}] {p['resumo']['total']:>2} reiv "
              f"({','.join(f'{k}:{v}' for k, v in p['resumo']['marcadores'].items()) or '—'}) "
              f"{p['titulo'][:42]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
