import ast
import hashlib
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent.parent
REPORT = ROOT / "HUBBLE_JA_EXAMINADO_K04.md"
MEASURES = BASE / "MEDIDAS_PLANEJAMENTO_K04.json"
MEASURES_MD = BASE / "MEDIDAS_PLANEJAMENTO_K04.md"
ERRATA = ROOT / "ERRATA_HUBBLE_K04.md"
ERRATA_R2 = ROOT / "ERRATA_HUBBLE_K04_R2.md"
ERRATA_K09 = ROOT / "ERRATA_HUBBLE_K09.md"
K09 = BASE / "K09"
VALIDATION = K09 / "VALIDACAO_DOCUMENTAL_K09.json"
MANIFEST = BASE / "SHA256SUMS_K04_HUBBLE.json"
NINE_ROUTES = [
    "d1.fase7_cc_covariancia_01out",
    "bancada.preregistro_dois_lados_delta_k",
    "um_py.v380.fases_5_6_7_por_hash",
    "discriminante.lentes_5sigma_20261019",
    "discriminante.ordem018.r_h_sirenes",
    "d1.fase9.auditoria_suficiencia_20261019",
    "d1.fase9.integracao_20261019",
    "estatistica.h0dn_bg1.cov_injecoes_06nov",
    "natureza.5sigma_fora_da_cosmologia_poder_27out",
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


for name in ("extrair_rotas.py", "medidas_planejamento.py", "verificar_relatorio.py"):
    ast.parse((BASE / name).read_text(encoding="utf-8"))

text = REPORT.read_text(encoding="utf-8")
data = json.loads(MEASURES.read_text(encoding="utf-8"))
measures_md = MEASURES_MD.read_text(encoding="utf-8")
errata_k09_text = ERRATA_K09.read_text(encoding="utf-8")
notes_text = "\n".join(path.read_text(encoding="utf-8") for path in sorted(K09.glob("*.md")))
errors = []

# As contas de planejamento e seus identificadores continuam cobertos pelo relatório.
for record in data["medidas"] + data["previsoes"]:
    d = f"{record['D_desenho']:.3f}".replace(".", ",")
    if d not in text:
        errors.append(f"D ausente/divergente no relatório: {record['id']} = {d}")
    ids = re.findall(r"(?:arXiv:)?(\d{4}\.\d{4,5})(?:v\d+)?", record["fonte"])
    if ids and ids[0] not in text:
        errors.append(f"Identificador ausente no relatório: {record['id']} -> {ids[0]}")

if len(data["medidas"]) != 26 or len(data["previsoes"]) != 4:
    errors.append("A cobertura deve permanecer em 26 medidas e 4 previsões")

required = [
    "Não existe hoje, neste setor, teste cego de natureza executável",
    "desfavorecida e NÃO excluída",
    "−3,22σ (diagonal) → −1,66σ (Moresco 2020) → −1,54σ (todos)",
    "2,33σ",
    "203–212, 214, 221",
    "6,710 no primário",
    "5,191 com Cefeidas livres",
    "73,50 ± 0,81",
    "73,994 ± 0,697",
    "3,256",
    "2,32",
    "R16",
    "não entra em conta de poder qualificada",
    "4,04",
    "3,36",
    "5,34",
    "4,88",
    "Não cego e não independente",
    "DESI DR3 entra como FUNDO",
    "os bytes de 02/11 não dizem isso literalmente",
    "a R1 não tem verbatim em arquivo",
    "TheFlowLawContrast.lean",
    "seq 1867",
] + NINE_ROUTES
for phrase in required:
    if phrase not in text:
        errors.append(f"Frase/rota obrigatória ausente no relatório: {phrase}")

for phrase in (
    "desfavorecida e NÃO excluída",
    "37fee18ca729cfc7dadd4cf9ea7fb9c239146d8bca4f5afd52a878a726542f76",
    "6,710 no primário",
    "5,191 com Cefeidas livres",
    "não cegos e não independentes",
    "Fundo por padrão",
    "seq 1867",
):
    if phrase not in errata_k09_text:
        errors.append(f"Errata K09 sem a correção obrigatória: {phrase}")

# O texto ativo K09 não pode repetir a leitura superada nem a atribuição sem bytes.
active_texts = [text, errata_k09_text, notes_text, measures_md]
for forbidden in (
    "morta",
    "nenhuma forma intermediária viva",
    "203–214",
    "53–62",
    "a sexta fechada pela leitura ratificada",
    "transposição FFAT bloqueada pela R1",
):
    for label, active in zip(("relatório", "errata K09", "notas K09", "medidas MD"), active_texts):
        if forbidden.lower() in active.lower():
            errors.append(f"Texto superado remanescente em {label}: {forbidden}")

# O D da casa precede o D de bolso e os campos de ponte são coerentes.
if text.index("6,710") > text.index("7,068"):
    errors.append("O D 6,710 do core deve aparecer antes do D de bolso 7,068")
if data["h0dn_core"]["primario"]["D"] != 6.710:
    errors.append("D primário do core divergente")
if data["h0dn_core"]["cefeidas_livres"]["D"] != 5.191:
    errors.append("D de Cefeidas livres do core divergente")
if "Primário | 6.710" not in measures_md or "Cefeidas livres | 5.191" not in measures_md:
    errors.append("Medidas MD não apresenta primeiro os D do core")

for record in data["medidas"] + data["previsoes"]:
    qualified = record["entra_conta_poder_qualificada"]
    if record["ponte_K_H_fundo"] == "NAO_EXAMINADA" and qualified:
        errors.append(f"Linha sem ponte promovida indevidamente: {record['id']}")
    if record["ponte_K_H_fundo"].startswith("SIM_CONDICIONAL") and not qualified:
        errors.append(f"Ponte condicional não registrada: {record['id']}")

sn2 = next(record for record in data["medidas"] if record["id"] == "sn2_vogl")
if not sn2.get("D_teto_so_estatistico"):
    errors.append("SN II EPM sem marca de teto estatístico")
if abs(sn2["D_com_sistematica_igual_estatistica"] - 2.31891505036625) > 1e-12:
    errors.append("SN II EPM com D(sys=stat) divergente")
if data["empilhamento_revisor"]["duas_linhas"]["fracao_de_linhas_ja_na_v2"] != "1/2":
    errors.append("Sobreposição de duas linhas divergente")
if data["empilhamento_revisor"]["cinco_linhas"]["fracao_de_linhas_ja_na_v2"] != "2/5":
    errors.append("Sobreposição de cinco linhas divergente")

for path in (ERRATA, ERRATA_R2, ERRATA_K09, K09 / "NOTAS_ROTAS_PONTES_K09.md", K09 / "NOTAS_EMPILHAMENTO_DESI_K09.md"):
    if not path.exists():
        errors.append(f"Arquivo obrigatório ausente: {path.name}")


def check_preserved(revision, names):
    previous_manifest = json.loads((BASE / revision / "SHA256SUMS_K04_HUBBLE.json").read_text(encoding="utf-8"))
    previous_hashes = {item["path"]: item["sha256"] for item in previous_manifest["arquivos"]}
    for name in names:
        preserved = BASE / revision / name
        if not preserved.exists():
            errors.append(f"{revision}: arquivo preservado ausente: {name}")
            continue
        previous_key = f"../{name}" if name in (
            "HUBBLE_JA_EXAMINADO_K04.md",
            "ERRATA_HUBBLE_K04.md",
            "ERRATA_HUBBLE_K04_R2.md",
            "ERRATA_HUBBLE_K09.md",
        ) else name
        expected = previous_hashes.get(previous_key)
        if expected is None:
            errors.append(f"{revision}: entrada ausente no manifesto anterior: {previous_key}")
        elif sha(preserved) != expected:
            errors.append(f"{revision} alterado: {name}")


check_preserved("REV0", (
    "HUBBLE_JA_EXAMINADO_K04.md",
    "MEDIDAS_PLANEJAMENTO_K04.md",
    "MEDIDAS_PLANEJAMENTO_K04.json",
))
check_preserved("REV1", (
    "HUBBLE_JA_EXAMINADO_K04.md",
    "ERRATA_HUBBLE_K04.md",
    "MEDIDAS_PLANEJAMENTO_K04.md",
    "MEDIDAS_PLANEJAMENTO_K04.json",
    "verificar_relatorio.py",
))
check_preserved("REV2", (
    "HUBBLE_JA_EXAMINADO_K04.md",
    "ERRATA_HUBBLE_K04.md",
    "ERRATA_HUBBLE_K04_R2.md",
    "MEDIDAS_PLANEJAMENTO_K04.md",
    "MEDIDAS_PLANEJAMENTO_K04.json",
    "medidas_planejamento.py",
    "verificar_relatorio.py",
))
if sha(BASE / "REV2" / "HUBBLE_JA_EXAMINADO_K04.md") != "37fee18ca729cfc7dadd4cf9ea7fb9c239146d8bca4f5afd52a878a726542f76":
    errors.append("Hash do relatório REV2 divergente do valor preservado")

if errors:
    raise SystemExit("\n".join(errors))

# Recibo de validação: determinístico, sem estatística observada e anterior ao manifesto.
validation = {
    "contrato": "K09_HUBBLE_VALIDACAO_DOCUMENTAL_V1",
    "estatuto": "[REAL — validação documental e algébrica dos bytes finais; nenhum vetor observado lido]",
    "consistencia_relatorio_medidas": "OK",
    "medidas_conferidas": len(data["medidas"]),
    "previsoes_conferidas": len(data["previsoes"]),
    "nove_rotas_presentes": True,
    "pontes_e_poder_qualificado": "OK",
    "d_casa_antes_de_bolso": True,
    "sn2_teto_e_sys_igual_stat": sn2["D_com_sistematica_igual_estatistica"],
    "empilhamento_sobreposicao": {"duas_linhas": "1/2", "cinco_linhas": "2/5"},
    "desi_dr3": "fundo por padrão; testemunha separada só sob critérios prévios",
    "rev0_preservado": True,
    "rev1_preservado": True,
    "rev2_preservado": True,
    "sha256_relatorio": sha(REPORT),
    "sha256_errata_k09": sha(ERRATA_K09),
    "sha256_medidas_json": sha(MEASURES),
    "sha256_medidas_md": sha(MEASURES_MD),
}
VALIDATION.write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

manifest = {
    "contrato": "K04_HUBBLE_SHA256_V2_K09",
    "estatuto": "[REAL — hashes recalculados dos bytes finais]",
    "arquivos": [],
}
for path in sorted(BASE.rglob("*")):
    if not path.is_file() or path == MANIFEST or "__pycache__" in path.parts:
        continue
    raw = path.read_bytes()
    manifest["arquivos"].append({
        "path": str(path.relative_to(BASE)).replace("\\", "/"),
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
    })
for deliverable in (REPORT, ERRATA, ERRATA_R2, ERRATA_K09):
    raw = deliverable.read_bytes()
    manifest["arquivos"].append({
        "path": f"../{deliverable.name}",
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
    })
MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

check = json.loads(MANIFEST.read_text(encoding="utf-8"))
for item in check["arquivos"]:
    path = (ROOT / item["path"][3:]) if item["path"].startswith("../") else (BASE / item["path"])
    raw = path.read_bytes()
    assert len(raw) == item["bytes"], item["path"]
    assert hashlib.sha256(raw).hexdigest() == item["sha256"], item["path"]

print(json.dumps({
    "validacao_documental": "OK",
    "arquivo_validacao": str(VALIDATION.relative_to(BASE)).replace("\\", "/"),
    "medidas_conferidas": len(data["medidas"]),
    "previsoes_conferidas": len(data["previsoes"]),
    "nove_rotas": len(NINE_ROUTES),
    "arquivos_hasheados_e_revalidados": len(check["arquivos"]),
    "rev0_rev1_rev2_preservados": True,
    "sha256_relatorio": sha(REPORT),
    "sha256_errata_k09": sha(ERRATA_K09),
    "sha256_validacao": sha(VALIDATION),
    "sha256_manifesto": sha(MANIFEST),
}, ensure_ascii=False, indent=2))
