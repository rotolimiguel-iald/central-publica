from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pin(path: Path) -> dict:
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha(path)}


def summary_count(path: Path) -> int:
    count = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            break
        if line.strip():
            count += 1
    return count


# 1. Arquivos exigidos
required = [
    "ENTREGA_K10.md", "REGISTRO_MAPA_K10.json",
    "REGISTRO_MAPA_K08.json", "REGISTRO_MAPA_K09.json",
    "PRE_REGISTRO_INCREMENTO_JUNO_RASCUNHO_K10.md",
    "PRE_REGISTRO_INCREMENTO_JUNO_RASCUNHO_K09.md",
    "INSUMOS_PARA_A_PERGUNTA_K09.md", "INSUMOS_PARA_A_PERGUNTA_K08.md",
    "ERRATA_K10_PRE_REGISTRO.md", "ERRATA_K10_M2.md",
    "ERRATA_K10_HUBBLE_COMBINACAO.md", "ERRATA_K10_K08.md",
    "ERRATA_RESIDUOS_EIXOS_K01_K04.md",
    "ENTREGA_K09.md", "ENTREGA_K08.md",
    "M2_DESFECHOS_E_SEGUNDA_TESTEMUNHA_K04.md",
    "ERRATA_NEUTRINO_V412_DADOS_K09.json",
    "ERRATA_M2_K09.md", "ERRATA_M2_K09_15nov.md",
    "HUBBLE_JA_EXAMINADO_K04.md", "ERRATA_HUBBLE_K09.md",
    "COMBINACAO_K04.md", "ERRATA_COMBINACAO_K09.md",
    "RESSALVAS_UMA_A_UMA_K04.md",
    "MODELO_FORMAL_R4_K08.md", "REGISTRO_UMPY_RASCUNHO_R2_K08.md",
    "PROTOCOLO_EXPERIMENTAL_R4_K08.md", "PODER_R4_K08.md",
    "CONTAMINACAO_R4_K08.md", "ERRATA_PODER_K08_15nov.md",
    "ERRATA_PODER_TOKENS_K08.md", "ERRATA_FORMAL_K08_15nov.md",
    "ERRATA_CONTAMINACAO_K08_15nov.md",
    "FORMULA_DO_TEXTO_K08.md", "ADVERSARIOS_K08.md",
    "K08/FORMULA/FORMULA_DO_TEXTO_K08.md", "K08/FORMULA/ADVERSARIOS_K08.md",
    "K08/FORMULA/simular_adversarios.py", "K08/FORMULA/MANIFESTO_FORMULA_K08.json",
    "K08/FORMULA/RESULTADOS_FORMULA.json", "K08/FORMULA/RESULTADOS_ADVERSARIOS.json",
    "K08/PODER/simular_poder_r4.py", "K08/PODER/resultados_poder_r4.json",
    "K08/PODER/MANIFESTO_SHA256.json",
]
for name in required:
    assert (ROOT / name).is_file(), name

# 2. Topo da ENTREGA_K10
n_top = summary_count(ROOT / "ENTREGA_K10.md")
assert n_top <= 15, n_top
text = (ROOT / "ENTREGA_K10.md").read_text(encoding="utf-8")
assert "Revisão interna" in text
assert "aprovada em revisão independente" not in text
assert "conferências distintas e independentes" not in text

# 3. Hashes declarados na tabela da ENTREGA_K10 batem com o disco
import re
declared = dict(re.findall(r"\| `([^`]+)` \| `([0-9a-f]{64})` \|", text))
for name, h in declared.items():
    name = name.replace("\\", "/").split(" (")[0]
    p = ROOT / name
    assert p.is_file(), name
    assert sha(p) == h, f"hash divergente: {name}"

# 4. Registros propostos
reg10 = json.loads((ROOT / "REGISTRO_MAPA_K10.json").read_text(encoding="utf-8"))
assert isinstance(reg10, list) and len(reg10) == 2
expected_routes = {
    "outro.k08_teste_cego_da_camada_iald_r4_v412",
    "estatistica.v412.k04_hubble_m2_combinacao",
}
map_results = {}
for reg in reg10 + [
    json.loads((ROOT / "REGISTRO_MAPA_K08.json").read_text(encoding="utf-8")),
    json.loads((ROOT / "REGISTRO_MAPA_K09.json").read_text(encoding="utf-8")),
]:
    assert reg["tipo"] == "ANOTACAO"
    assert reg["olhou_dados"] is False
    assert reg["estatuto"].startswith("DECLARADO"), reg["rota_id"]
    for item in reg["artefatos"]:
        if item.endswith("VALIDACAO_K10_15nov.json"):
            continue  # escrito abaixo
        assert Path(item).is_file(), item
for route in expected_routes | {"outro.k06_camada_cientifica_iald_r32_v412"}:
    query = subprocess.run(
        [sys.executable, r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "consultar", route],
        cwd=r"C:\IALD", capture_output=True, text=True, check=True,
    )
    data = json.loads(query.stdout)
    hits = [item for item in data["rotas"] if item["rota_id"] == route]
    assert len(hits) >= 1, f"rota alvo ausente no Mapa: {route}"
    map_results[route] = {"encontrada": True, "n": data["n"]}

# 5. Reprodução na árvore corrente (scripts K08 determinísticos)
before = {
    "K08/FORMULA/ADVERSARIOS_K08.md": sha(ROOT / "K08/FORMULA/ADVERSARIOS_K08.md"),
    "K08/FORMULA/RESULTADOS_ADVERSARIOS.json": sha(ROOT / "K08/FORMULA/RESULTADOS_ADVERSARIOS.json"),
    "K08/FORMULA/RESULTADOS_FORMULA.json": sha(ROOT / "K08/FORMULA/RESULTADOS_FORMULA.json"),
    "K08/FORMULA/FORMULA_DO_TEXTO_K08.md": sha(ROOT / "K08/FORMULA/FORMULA_DO_TEXTO_K08.md"),
    "K08/PODER/resultados_poder_r4.json": sha(ROOT / "K08/PODER/resultados_poder_r4.json"),
    "K08/PODER/sementes_r4.json": sha(ROOT / "K08/PODER/sementes_r4.json"),
    "K08/PODER/resumo_designs_r4.csv": sha(ROOT / "K08/PODER/resumo_designs_r4.csv"),
}
runs = [
    ("K08/FORMULA", "verificar_formula.py"),
    ("K08/FORMULA", "simular_adversarios.py"),
    ("K08/PODER", "simular_poder_r4.py"),
]
for sub, script in runs:
    proc = subprocess.run(
        [sys.executable, "-B", script], cwd=ROOT / sub,
        capture_output=True, text=True, timeout=600,
    )
    assert proc.returncode == 0, f"{script}: {proc.stderr[-2000:]}"
for name, h in before.items():
    assert sha(ROOT / name) == h, f"regeneração não idempotente: {name}"

# 6. Manifesto final
pins = {name: pin(ROOT / name) for name in required}
pins["VALIDACAO_K10_15nov.json"] = "SELF"
validation = {
    "contract": "K10_RODADA4_FINAL_DELIVERY_VALIDATION_V1",
    "created_at": datetime.now().astimezone().isoformat(),
    "review": "revisão interna (quatro frentes executadas e conferidas por esta casa); a revisão distinta cabe à gerência",
    "summary_nonempty_lines_ENTREGA_K10": n_top,
    "declared_hashes_match_disk": sorted(declared),
    "registration_written_to_map": False,
    "map_target_routes": map_results,
    "observed_data_opened": False,
    "models_executed": False,
    "canonical_kernel_or_um_py_changed": False,
    "secao_2_k10_suspensa_pelo_adendo_C": True,
    "reproduction_on_current_tree": {
        "scripts": [f"{sub}/{script}" for sub, script in runs],
        "outputs_byte_identical": sorted(before),
        "k09_validators": "validar_k09.py e verificar_relatorio.py rodados verdes pelas frentes m2 e Hubble nesta rodada",
    },
    "custody_notes": [
        "ENTREGA_K08.md congelada pelo depósito seq 685; supersessões listadas em ERRATA_K10_K08.md",
        "ENTREGA_K09.md corrigida ao lado; K04/M2/REV4/ENTREGA_K09.md preserva os bytes do depósito seq 686",
        "REGISTRO_MAPA_K08.json e REGISTRO_MAPA_K09.json marcados SUPERADA pela proposta da rodada 4",
    ],
    "pins": pins,
}
vpath = ROOT / "VALIDACAO_K10_15nov.json"
vpath.write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
pins["VALIDACAO_K10_15nov.json"] = pin(vpath)

# 7. Depósito (texto mínimo: o que foi entregue, onde, e que aguarda a conferência)
main = pin(ROOT / "ENTREGA_K10.md")
registration = pin(ROOT / "REGISTRO_MAPA_K10.json")
text_dep = (
    "[DECLARADO] K10 (rodada 4: os consertos da conferência de 15/11) entregue na pasta da rodada: "
    "as quatro erratas por frente (K08; pré-registro; m2; Hubble e combinação), o pré-registro do incremento "
    "reescrito ao lado, os insumos reescritos, os resíduos de um eixo marcados SUPERADA, os registros propostos "
    "(K08 e K09 atualizados ao lado; K10 como par de ANOTACAOs nas rotas vivas) e a validação. "
    "A seção 2 da K10 está suspensa pelo ADENDO C. Aguarda a conferência da gerência."
    + f"\n\nEntrega: {main['path']}\nSHA-256: {main['sha256']}\n"
    + f"Registro proposto: {registration['path']}\nSHA-256: {registration['sha256']}\n"
    + f"Validação: {vpath}\nSHA-256: {sha(vpath)}\n"
)
dpath = ROOT / "DEPOSITO_K10.md"
dpath.write_text(text_dep, encoding="utf-8")

print(json.dumps({
    "status": "PASS",
    "summary_nonempty_lines_ENTREGA_K10": n_top,
    "map_target_routes": map_results,
    "validation": pin(vpath),
    "deposit_payload": pin(dpath),
}, ensure_ascii=False, indent=2))
