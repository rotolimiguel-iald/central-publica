import ast
import hashlib
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent.parent
REPORT = ROOT / "HUBBLE_JA_EXAMINADO_K04.md"
MEASURES = BASE / "MEDIDAS_PLANEJAMENTO_K04.json"

for name in ("extrair_rotas.py", "medidas_planejamento.py", "verificar_relatorio.py"):
    ast.parse((BASE / name).read_text(encoding="utf-8"))

text = REPORT.read_text(encoding="utf-8")
data = json.loads(MEASURES.read_text(encoding="utf-8"))
errors = []

for record in data["medidas"] + data["previsoes"]:
    d = f"{record['D_desenho']:.3f}".replace(".", ",")
    if d not in text:
        errors.append(f"D ausente/divergente no relatório: {record['id']} = {d}")
    ids = re.findall(r"(?:arXiv:)?(\d{4}\.\d{4,5})(?:v\d+)?", record["fonte"])
    if ids and ids[0] not in text:
        errors.append(f"Identificador ausente no relatório: {record['id']} -> {ids[0]}")

required = [
    "Não existe hoje, neste setor, teste cego de natureza executável",
    "Morta, rota `d1.fase4_desvio_30set`",
    "Nenhuma determinação **independente de um passo** cruza hoje 5σ ou D90",
    "pseudo‑FRB nominal ultrapassa 5, mas não é qualificado",
    "D = 8,068",
    "D = 3,256",
    "D = 7,754",
    "1,260 %",
    "1,618 %",
    "0,438 %",
    "discriminante.ordem018.f2.r_f",
    "T(z) = T0(1+z)",
    "resultado 2017 + seq 2038",
    "13 BBH–AGN",
    "SN Encore",
    "126 FRBs/118",
    "delimitada às fontes efetivamente consultadas",
]
for phrase in required:
    if phrase not in text:
        errors.append(f"Frase obrigatória ausente: {phrase}")

for forbidden in ("D = 8,374", "D < 3`", "599, 751", "73,50; incerteza 0,9 %"):
    if forbidden in text:
        errors.append(f"Texto obsoleto remanescente: {forbidden}")

for forbidden_name in ("ENTREGA_K04.md", "REGISTRO_MAPA_K04.json", "DEPOSITO_K04.md"):
    if (ROOT / forbidden_name).exists():
        errors.append(f"Arquivo proibido encontrado: {forbidden_name}")

errata_path = ROOT / "ERRATA_HUBBLE_K04.md"
if not errata_path.exists():
    errors.append("ERRATA_HUBBLE_K04.md ausente")

for evidence, needles in {
    BASE / "consultas" / "ver_RF.txt": ('"seq": 378', '"seq": 1636'),
    BASE / "consultas" / "ver_v411_H0DN.txt": ('"seq": 2038',),
}.items():
    if not evidence.exists():
        errors.append(f"Evidência ausente: {evidence.name}")
        continue
    evidence_text = evidence.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in evidence_text:
            errors.append(f"Sequência ausente em {evidence.name}: {needle}")

if errors:
    raise SystemExit("\n".join(errors))

manifest = {
    "contrato": "K04_HUBBLE_SHA256_V1",
    "estatuto": "[REAL — hashes recalculados dos bytes finais]",
    "arquivos": [],
}
for path in sorted(BASE.rglob("*")):
    if not path.is_file() or path.name == "SHA256SUMS_K04_HUBBLE.json" or "__pycache__" in path.parts:
        continue
    raw = path.read_bytes()
    manifest["arquivos"].append({
        "path": str(path.relative_to(BASE)).replace("\\", "/"),
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
    })
for deliverable in (REPORT, errata_path):
    raw = deliverable.read_bytes()
    manifest["arquivos"].append({
        "path": f"../{deliverable.name}",
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
    })
manifest_path = BASE / "SHA256SUMS_K04_HUBBLE.json"
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

check = json.loads(manifest_path.read_text(encoding="utf-8"))
for item in check["arquivos"]:
    path = (ROOT / item["path"][3:]) if item["path"].startswith("../") else (BASE / item["path"])
    raw = path.read_bytes()
    assert len(raw) == item["bytes"], item["path"]
    assert hashlib.sha256(raw).hexdigest() == item["sha256"], item["path"]

previous_manifest = json.loads((BASE / "REV0" / "SHA256SUMS_K04_HUBBLE.json").read_text(encoding="utf-8"))
previous_hashes = {item["path"]: item["sha256"] for item in previous_manifest["arquivos"]}
for name in ("HUBBLE_JA_EXAMINADO_K04.md", "MEDIDAS_PLANEJAMENTO_K04.md", "MEDIDAS_PLANEJAMENTO_K04.json"):
    current_rev0_hash = hashlib.sha256((BASE / "REV0" / name).read_bytes()).hexdigest()
    previous_key = "../HUBBLE_JA_EXAMINADO_K04.md" if name == "HUBBLE_JA_EXAMINADO_K04.md" else name
    expected_rev0_hash = previous_hashes[previous_key]
    if current_rev0_hash != expected_rev0_hash:
        raise SystemExit(f"REV0 alterado: {name}")

raw_report = REPORT.read_bytes()
print(json.dumps({
    "consistencia_relatorio_medidas": "OK",
    "medidas_conferidas": len(data["medidas"]),
    "previsoes_conferidas": len(data["previsoes"]),
    "arquivos_hasheados_e_revalidados": len(check["arquivos"]),
    "rev0_preservado": True,
    "sha256_relatorio": hashlib.sha256(raw_report).hexdigest(),
    "sha256_errata": hashlib.sha256(errata_path.read_bytes()).hexdigest(),
    "sha256_manifesto": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
}, ensure_ascii=False, indent=2))
