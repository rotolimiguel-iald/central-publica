#!/usr/bin/env python3
"""REVISAO_K05_CAMPO — conferencias mecanicas do revisor distinto (tarefas 5, 7 e 8b/8c).
SOMENTE LEITURA do que e do Kimi. A validacao do REGISTRO usa a propria guarda do rotas.py em DRY-RUN
(importa `_valida`; NAO chama `registrar`; nada e gravado no livro)."""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from hashlib import sha256
from pathlib import Path

sys.dont_write_bytecode = True
KIMI = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi")
CAMPO = KIMI / "K05" / "CAMPO"
FALA = Path(r"C:\IALD\Central de Patentes\work\vitrine_postura_13nov\OPERADOR_13nov_concordo_com_o_meio_o_campo_e_dual_sim_a_nota_a_calculadora_e_o_zenodo_verbatim.txt")
SAIDA = Path(__file__).resolve().parent / "conferir_integracao_saida.json"


def h(p: Path) -> str:
    return sha256(p.read_bytes()).hexdigest()


out: dict = {}

# ---------------------------------------------------------------- 7: hashes
decl_hashes = {}
for linha in (CAMPO / "HASHES_CAMPO_K05.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^([0-9a-f]{64})\s+(\S.*)$", linha)
    if m:
        decl_hashes.setdefault(m.group(2).strip(), []).append(m.group(1))

pares = {
    "ERRATA_CAMPO_K05.md": KIMI / "ERRATA_CAMPO_K05.md",
    "CAMPO_DUAL_LEVANTAMENTO_K05.md": KIMI / "CAMPO_DUAL_LEVANTAMENTO_K05.md",
    "K05/CAMPO/CONSULTAS_CAMPO_K05.md": CAMPO / "CONSULTAS_CAMPO_K05.md",
    "K05/CAMPO/medir_campo.py": CAMPO / "medir_campo.py",
    "K05/CAMPO/medidas_campo.json": CAMPO / "medidas_campo.json",
    "K05/CAMPO/execucao_medidas.log": CAMPO / "execucao_medidas.log",
    "K05/CAMPO/REV0/CAMPO_DUAL_LEVANTAMENTO_K05.md": CAMPO / "REV0" / "CAMPO_DUAL_LEVANTAMENTO_K05.md",
    "K05/CAMPO/REV0/CONSULTAS_CAMPO_K05.md": CAMPO / "REV0" / "CONSULTAS_CAMPO_K05.md",
    "K05/CAMPO/REV0/medir_campo.py": CAMPO / "REV0" / "medir_campo.py",
    "K05/CAMPO/REV0/medidas_campo.json": CAMPO / "REV0" / "medidas_campo.json",
    "K05/CAMPO/REV0/execucao_medidas.log": CAMPO / "REV0" / "execucao_medidas.log",
}
conf = {}
for chave, caminho in pares.items():
    real = h(caminho)
    decl = decl_hashes.get(chave, [])
    conf[chave] = {"real": real, "declarado_em_HASHES": decl, "confere": real in decl}
out["hashes_HASHES_CAMPO_K05"] = conf

# tabela da ERRATA (REV0 antes / vigente depois)
errata = (KIMI / "ERRATA_CAMPO_K05.md").read_text(encoding="utf-8")
tab = {}
for m in re.finditer(r"\|\s*`([^`]+)`\s*\|\s*`([0-9a-f]{64})`[^|]*\|\s*`([0-9a-f]{64})`", errata):
    tab[m.group(1)] = (m.group(2), m.group(3))
conf2 = {}
for nome, (antes, depois) in tab.items():
    rev0 = h(CAMPO / "REV0" / nome)
    vig = h((KIMI / nome) if nome == "CAMPO_DUAL_LEVANTAMENTO_K05.md" else (CAMPO / nome))
    conf2[nome] = {"REV0_real": rev0, "REV0_declarado": antes, "REV0_confere": rev0 == antes,
                   "vigente_real": vig, "vigente_declarado": depois, "vigente_confere": vig == depois}
out["hashes_tabela_ERRATA"] = conf2
out["REV0_tres_arquivos_identicos_aos_vigentes"] = {
    n: h(CAMPO / "REV0" / n) == h(CAMPO / n) for n in ("medir_campo.py", "medidas_campo.json", "execucao_medidas.log")
}
fb = FALA.read_bytes()
out["fala"] = {"bytes": len(fb), "sha256": sha256(fb).hexdigest(),
               "confere_529_e_2772005945b946c1": len(fb) == 529 and sha256(fb).hexdigest().startswith("2772005945b946c1")}

# diff REV0 -> vigente do levantamento (para ver o que a errata mexeu de fato)
import difflib
a = (CAMPO / "REV0" / "CAMPO_DUAL_LEVANTAMENTO_K05.md").read_text(encoding="utf-8").splitlines()
b = (KIMI / "CAMPO_DUAL_LEVANTAMENTO_K05.md").read_text(encoding="utf-8").splitlines()
out["diff_REV0_para_vigente_levantamento"] = [l for l in difflib.unified_diff(a, b, "REV0", "vigente", lineterm="", n=0)]

# ---------------------------------------------------------------- 5: aspas « »
falat = fb.decode("utf-8")
alvos = ["CAMPO_DUAL_LEVANTAMENTO_K05.md", "ERRATA_CAMPO_K05.md", "ENTREGA_K05.md", "PERGUNTA_K05.md", "DEPOSITO_K05.md",
         "K05/CAMPO/CONSULTAS_CAMPO_K05.md"]
aspas = {}
for nome in alvos:
    p = KIMI / nome
    t = p.read_text(encoding="utf-8")
    achados = []
    for m in re.finditer(r"«([^»]*)»", t):
        trecho = m.group(1)
        linha = t.count("\n", 0, m.start()) + 1
        achados.append({"linha": linha, "trecho": trecho[:300], "bytes_na_fala": trecho in falat,
                        "bytes_na_fala_apos_trim": trecho.strip() in falat})
    aspas[nome] = achados
out["aspas_francesas"] = aspas

# ---------------------------------------------------------------- 8b: REGISTRO
reg_path = KIMI / "REGISTRO_MAPA_K05.json"
reg = json.loads(reg_path.read_text(encoding="utf-8"))
spec = importlib.util.spec_from_file_location("rotas_ro", r"C:\IALD\MAPA_DE_ROTAS\rotas.py")
rotas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rotas)
modelo_keys = set(rotas.MODELO.keys())
out["registro_chaves"] = {
    "modelo": sorted(modelo_keys), "registro": sorted(reg.keys()),
    "faltam_do_modelo": sorted(modelo_keys - set(reg.keys())),
    "extras_fora_do_modelo": sorted(set(reg.keys()) - modelo_keys),
}
regs = rotas._le()  # SOMENTE LEITURA do livro (confere a cadeia de hash)
ids = {r["rota_id"] for r in regs if r["tipo"] == "ROTA"}
seqs = {r["seq"] for r in regs}
try:
    r2 = rotas._valida(reg, ids, seqs)  # dry-run: nao grava
    out["registro_guarda_dry_run"] = {"passou": True, "n_registros_no_livro": len(regs), "cabeca": regs[-1]["sha"][:16],
                                       "artefatos_resolvidos": len(r2.get("artefatos", []))}
except Exception as e:  # noqa: BLE001
    out["registro_guarda_dry_run"] = {"passou": False, "erro": str(e)}
out["registro_refs_existem_no_livro"] = {r: (r in ids) for r in reg.get("refs", [])}
out["registro_rota_id_ja_existe"] = reg["rota_id"] in ids
tem_aspas = {k: ("«" in str(v) or "»" in str(v)) for k, v in reg.items()}
out["registro_caracteres_aspas_francesas"] = [k for k, v in tem_aspas.items() if v]
confs = {}
for k, v in reg.items():
    for m in re.finditer(r"\bconfirm\w*", json.dumps(v, ensure_ascii=False), flags=re.I):
        confs.setdefault(k, []).append(json.dumps(v, ensure_ascii=False)[max(0, m.start() - 40):m.end() + 5])
out["registro_palavras_confirm_por_campo"] = confs
out["registro_tamanho_max_texto"] = {k: len(str(reg[k])) for k in rotas.TEXTOS if k in reg}
# artefatos: existem?
out["registro_artefatos_existem"] = {a: Path(a).is_file() for a in reg.get("artefatos", [])}

# ---------------------------------------------------------------- 8c: DEPOSITO
dep = (KIMI / "DEPOSITO_K05.md").read_text(encoding="utf-8")
decl = dict(re.findall(r"(?m)^(Entrega|Registro proposto|Validação): (.+)\n(?:SHA-256: ([0-9a-f]{64}))", dep) and [])
pins = re.findall(r"(?m)^(Entrega|Registro proposto|Validação): (\S.*)\nSHA-256: ([0-9a-f]{64})", dep)
out["deposito_pins"] = [{"rotulo": r, "caminho": c, "declarado": s, "real": h(Path(c)), "confere": h(Path(c)) == s} for r, c, s in pins]
out["deposito_primeiro_token"] = dep.split()[0]
out["deposito_expressoes"] = {
    "revisada internamente": "revisada internamente" in dep.lower(),
    "aprovada em revisao independente": bool(re.search(r"aprovad\w+ em revis\w+ independente", dep, re.I)),
    "palavra_confirm": [m.group(0) for m in re.finditer(r"\bconfirm\w*", dep, re.I)],
}

# VALIDACAO_K05.json: pins
val = json.loads((KIMI / "VALIDACAO_K05.json").read_text(encoding="utf-8"))
vp = {}
for k, v in val.get("pins", {}).items():
    p = Path(v["path"])
    vp[k] = {"confere": p.is_file() and h(p) == v["sha256"] and p.stat().st_size == v["bytes"]}
out["validacao_pins"] = vp
out["validacao_review_campo"] = val.get("review")
out["validacao_summary_nonempty_lines_declarado"] = val.get("summary_nonempty_lines")

# ---------------------------------------------------------------- 8a: ENTREGA topo
ent = (KIMI / "ENTREGA_K05.md").read_text(encoding="utf-8").splitlines()
topo = []
for l in ent:
    if l.startswith("## "):
        break
    if l.strip():
        topo.append(l)
out["entrega_topo_linhas_nao_vazias"] = len(topo)

SAIDA.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2))
