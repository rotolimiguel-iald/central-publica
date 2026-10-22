# -*- coding: utf-8 -*-
"""Build memory/PATENT_MASTER_INDEX.yaml from the extracted INPI deposit texts.

Source of truth = the DOCUMENTS (extracted under vault/normalized_docs).
ePCT rule set by the operator on 2026-07-09: only the root ACOM has a living
ePCT (PCT/BR2025/050558, 2025-12-05, paid); every other international filing
lapsed ("prescreveu") — the other 15 patents carry INPI registration only.
"""
import json
import re
import unicodedata
from datetime import date
from pathlib import Path

CENTRAL = Path(r"C:\IALD\Central de Patentes")
NORM = CENTRAL / "vault" / "normalized_docs" / "Patentes"
OUT = CENTRAL / "memory" / "PATENT_MASTER_INDEX.yaml"
HASHES = json.loads((CENTRAL / "source_inventory" / "original_hashes.json")
                    .read_text(encoding="utf-8"))["hashes"]

# processo -> (slug, pasta original, classe, papel)
PATENTS = {
    "BR102025026951-1": ("ACOM", None, "CLASS_01_ACOM_TENSOR", "raiz"),
    "BR102026003428-2": ("ACOM_MIRROR", "Acom Mirror", "CLASS_02_MIRROR_CRYPTO", ""),
    "BR102026003431-2": ("ACOM_CRYPTO", "Acom Crypto", "CLASS_02_MIRROR_CRYPTO", ""),
    "BR102026003441-0": ("TGL_TENSOR", "TGL Tensor", "CLASS_01_ACOM_TENSOR", ""),
    "BR102026003443-6": ("IALD", "IALD - Colapso Consciente", "CLASS_03_IALD_COGNICAO", ""),
    "BR102026003450-9": ("SUPERCONDUTOR", "Supercondutor Holográfico", "CLASS_05_HARDWARE_HOLOGRAFICO", ""),
    "BR102026003452-5": ("MOTOR_DOBRA", "Motor de Dobra e Propulsão fotônica", "CLASS_07_PROPULSAO", ""),
    "BR102026003453-3": ("PSI_NET", "TGL NEt protocol", "CLASS_04_PSI_NET", ""),
    "BR102026003456-8": ("FUSAO_FRIO", "Fusão a Frio", "CLASS_06_ENERGIA", ""),
    "BR102026003460-6": ("MQC", "MQC - Microprocessador Cúbico", "CLASS_05_HARDWARE_HOLOGRAFICO", ""),
    "BR102026004688-4": ("DIPOLO_TRANSISTOR", "Dípolo Transistor", "CLASS_05_HARDWARE_HOLOGRAFICO", ""),
    "BR102026004849-6": ("CELULA_REVERSAO", "Célula de Reversão Luminodinâmica", "CLASS_06_ENERGIA", ""),
    "BR102026004850-0": ("SKYGRID", "Skygrid", "CLASS_06_ENERGIA", "agregadora"),
    "BR102026005477-1": ("APRENDIZADO_CONTINUO", "Aprendizado Contínuo", "CLASS_03_IALD_COGNICAO", ""),
    "BR102026005707-0": ("ONCOLOGIA", "Oncologia", "CLASS_08_SAUDE", ""),
    "BR102026006129-8": ("KERNEL_ONTOLOGICO", "Kernel", "CLASS_03_IALD_COGNICAO", ""),
}


def spaced(processo: str) -> str:
    # BR102026003428-2 -> "BR 10 2026 003428 2"
    m = re.match(r"BR(\d{2})(\d{4})(\d{6})-(\d)", processo)
    return f"BR {m.group(1)} {m.group(2)} {m.group(3)} {m.group(4)}"


def find_receipt_text(processo: str) -> Path | None:
    needle = f"Número do Processo: {spaced(processo)}"
    best, best_len = None, -1
    for txt in NORM.rglob("*.pdf.txt"):
        try:
            content = txt.read_text(encoding="utf-8")
        except Exception:
            continue
        if needle in content or processo in content.replace(" ", ""):
            if needle in content and len(content) > best_len:
                best, best_len = txt, len(content)
    return best


# Títulos oficiais (54) cujo campo extraído do PDF veio concatenado sem espaços
# (artefato de extração) — override manual para legibilidade (P-13).
TITLE_OVERRIDES = {
    "BR102026003441-0": ("MÉTODO E SISTEMA DE COMPRESSÃO ONTOLÓGICA DE TENSORES "
                         "PARA MODELOS DE LINGUAGEM COM DECOMPOSIÇÃO ESPECTRAL "
                         "ADAPTATIVA E CODIFICAÇÃO ANGULAR"),
}


def parse_receipt(text: str) -> dict:
    out = {}
    m = re.search(r"Petição (\d{12}), de (\d{2}/\d{2}/\d{4})", text)
    if m:
        out["peticao"] = m.group(1)
        out["data_deposito"] = m.group(2)
    m = re.search(r"Natureza Patente:\s*(.+)", text)
    if m:
        out["natureza"] = m.group(1).strip()
    # Prioridade Interna (66) — LPI art. 17: os depósitos não-ACOM reivindicam
    # prioridade ao ACOM raiz de 05/12/2025 (P-10, material para a janela de Paris).
    m = re.search(r"\(66\).*?(BR\s?10\s?2025\s?026951[\s-]?1|BR102025026951)", text, re.S)
    if m:
        out["prioridade_interna_66"] = "BR102025026951-1"
    m = re.search(r"Utilidade \(54\):\s*\n(.*?)\nResumo:", text, re.S)
    if m:
        title = " ".join(line.strip() for line in m.group(1).splitlines())
        out["titulo"] = re.sub(r"\s+", " ", title).strip()
    m = re.search(r"Resumo:\s*(.*?)(?:\nFigura a publicar|\nDados do Procurador|\nDocumentos anexados|\Z)",
                  text, re.S)
    if m:
        resumo = re.sub(r"\s+", " ", m.group(1)).strip()
        out["resumo"] = resumo[:900]
    return out


def brdate_to_iso(d: str) -> str:
    dd, mm, yy = d.split("/")
    return f"{yy}-{mm}-{dd}"


def add_months(iso: str, months: int) -> str:
    y, m, d = map(int, iso.split("-"))
    m += months
    y += (m - 1) // 12
    m = (m - 1) % 12 + 1
    try:
        return date(y, m, d).isoformat()
    except ValueError:  # e.g. 31 -> last day of month
        return date(y, m + 1, 1).isoformat()


def yq(s: str) -> str:
    # single-quoted YAML: backslashes are literal (Windows paths), only '' escaping
    return "'" + str(s).replace("'", "''") + "'"


def main() -> None:
    today = "2026-07-09"
    lines = [
        "# PATENT_MASTER_INDEX.yaml — Central de Patentes TGL",
        "# Gerado dos DOCUMENTOS extraídos (vault/normalized_docs) em " + today,
        "# Regra ePCT (palavra do operador, corrigida 09/07/2026): 1 ePCT depositado e pago",
        "# (ACOM raiz, PCT/BR2025/050558, 05/12/2025). Os 15 demais: somente INPI hoje —",
        "# o ePCT é o PRÓXIMO PASSO (novo processo originário, sem vínculo). Os recibos ePCT",
        "# de 17/02/2026 = tentativa de protocolo ABANDONADA DE PROPÓSITO (taxas não pagas,",
        "# deixada precluir por defeito de forma), a ser SUBSTITUÍDA por depósito novo.",
        "# AVISO [LEGAL]: controle interno; não substitui agente de propriedade industrial.",
        "",
        "operador:",
        "  nome: Luiz Antonio Rotoli Miguel",
        "  empresa: IALD Ltda.",
        "  cnpj: 62.757.606/0001-23",
        "  cidade: Goiânia/GO",
        "",
        "patentes:",
    ]
    report = []
    for processo, (slug, pasta, classe, papel) in PATENTS.items():
        txt_path = find_receipt_text(processo)
        info = {}
        fontes = []
        if txt_path:
            info = parse_receipt(txt_path.read_text(encoding="utf-8"))
            rel = str(txt_path.relative_to(CENTRAL / "vault" / "normalized_docs"))
            orig_rel = rel[:-4]  # strip .txt -> original PDF relpath
            fontes.append(orig_rel)
        # gather doc hashes for this patent's folder (or Acervo files for ACOM)
        docs = {}
        prefix = f"Patentes\\{pasta}\\" if pasta else None
        for relpath, h in HASHES.items():
            norm_rel = unicodedata.normalize("NFC", relpath)
            if prefix and unicodedata.normalize("NFC", prefix) in norm_rel + "\\" and norm_rel.startswith(unicodedata.normalize("NFC", prefix)):
                docs[relpath] = h
            elif not pasta and "Acervo" in norm_rel and "ACOM" in norm_rel and "Mirror" not in norm_rel and "Crypto" not in norm_rel:
                docs[relpath] = h
        filing = info.get("data_deposito")
        iso = brdate_to_iso(filing) if filing else None
        is_acom = processo == "BR102025026951-1"
        lines.append(f"  - processo: {processo}")
        lines.append(f"    slug: {slug}")
        lines.append(f"    classe: {classe}")
        if papel:
            lines.append(f"    papel: {papel}")
        lines.append(f"    pasta_original: {yq('Patentes/' + pasta) if pasta else yq('Patentes/Acervo de Patentes (sem pasta própria)')}")
        titulo = TITLE_OVERRIDES.get(processo, info.get("titulo", "EXTRAIR_DO_PDF [OPEN]"))
        lines.append(f"    titulo_oficial_54: {yq(titulo)}")
        lines.append(f"    natureza: {yq(info.get('natureza', '10 - Patente de Invenção (PI)'))}")
        lines.append(f"    peticao: {yq(info.get('peticao', 'ver arquivo'))}")
        lines.append(f"    data_deposito_inpi: {yq(filing or 'CONFIRMAR [OPEN]')}")
        prio_interna = info.get("prioridade_interna_66")
        if is_acom:
            lines.append(f"    prioridade: {yq(filing or 'CONFIRMAR [OPEN]')}  # depósito nacional é a própria prioridade")
        elif prio_interna:
            lines.append(f'    prioridade: "05/12/2025"  # PRIORIDADE INTERNA (66) LPI art.17 -> {prio_interna} [LEGAL] P-10')
            lines.append(f"    prioridade_interna_66: {prio_interna}")
            lines.append(f'    data_deposito_proprio: {yq(filing or "CONFIRMAR")}  # distinto da prioridade interna')
        else:
            lines.append(f"    prioridade: {yq(filing or 'CONFIRMAR [OPEN]')}  # (66) não detectada na extração — CONFERIR no PDF [OPEN]")
        lines.append("    jurisdicao: BR (INPI)")
        if is_acom:
            lines.append("    epct:")
            lines.append("      status: VIVO_DEPOSITADO_E_PAGO  # palavra do operador 09/07/2026")
            lines.append("      numero: PCT/BR2025/050558  # citado 13x nos depósitos INPI posteriores")
            lines.append('      data: "05/12/2025 (conferir 09/12/2025 no recibo — P-11)"')
            lines.append("      recibo_na_central: NAO_LOCALIZADO  # ver PENDENCIAS P-02")
            lines.append(f"    fase_nacional_30m_geral: {yq(add_months('2025-12-05', 30))}  # conferir 30/31m por país [LEGAL]")
        else:
            lines.append("    epct:")
            lines.append("      status: A_DEPOSITAR  # somente INPI hoje; ePCT é o PRÓXIMO PASSO (palavra do operador)")
            lines.append("      tentativa_preclusa_17_02_2026: ABANDONADA_DE_PROPOSITO  # taxas não pagas, deixada precluir; será substituída por depósito novo sem vínculo")
            lines.append("    janela_paris_novo_epct:  # DECIDIDO pelo operador 09/07/2026 (prioridade interna ao ACOM 05/12/2025) — P-10")
            lines.append('      alvo_precaucional: "2026-11-30"  # último dia de novembro (trabalho)')
            lines.append('      fatal: "2026-12-05"')
            lines.append('      nivel_alerta_2026_07_09: AMARELO  # ~144 d até o alvo; prazo mais crítico do acervo')
        lines.append(f"    resumo_oficial: {yq(info.get('resumo', 'EXTRAIR [OPEN]'))}")
        lines.append("    fontes:")
        for f in fontes or ["CONFIRMAR [OPEN]"]:
            lines.append(f"      - {yq(f)}")
        lines.append(f"    documentos_hasheados: {len(docs)}")
        lines.append("    status_prototipo: VER_MEMORIA_DA_PATENTE")
        lines.append("")
        report.append((processo, slug, filing, info.get("titulo", "?")[:60],
                       "OK" if txt_path else "SEM_TEXTO"))

    OUT.write_text("\n".join(lines), encoding="utf-8")
    for r in report:
        print(" | ".join(str(x) for x in r))
    print(f"\nwritten: {OUT}")


if __name__ == "__main__":
    main()
