# -*- coding: utf-8 -*-
"""LIVRO DE PAGAMENTOS DO PCT — cada guia, a ordem de pagar e o vinculo de cada comprovante.

Fonte de verdade, sempre LIDA do artefato (nada digitado):
  * EPCT/<ID>/RECIBOS/DOCUMENTOS_OFICIAIS_WIPO_*/*-rowsp-*.zip  — o pacote RO WASP assinado pela WIPO:
    numero PCT, data/hora de recebimento e as prioridades com documento pedido ao RO (receipt.xml, requ.xml);
  * EPCT/<ID>/RECIBOS/GRU_<cod>_<numero>_EMISSAO.json            — cada GRU emitida no PAG (registro do Codex);
  * EPCT/_BR_NOVO_CRYPTO_20260930/REGISTRO_COMPROVANTE_GRU200_*.json — a GRU 200 do BR novo do Crypto, ja paga.

O que este script escreve (e so isto):
  * EPCT/_GUIAS_PCT_A_PAGAR_20260930/LIVRO_DE_PAGAMENTOS.json + PAGAMENTOS_EM_ORDEM.md (gerados; nunca editar a mao);
  * EPCT/<ID>/RECIBOS/COMPROVANTES_GRU/COMPROVANTE_<cod>_<gru>_<AAAAMMDD>.pdf — COPIA DE BYTES do comprovante achado;
  * EPCT/epct_status.json — os tiques transmitido / recibo_arquivado / taxas_pagas e pct_number / protocol_date,
    com backup de bytes antes; a "nota" so e tocada se estiver vazia ou tiver sido escrita por este script.

O vinculo do comprovante e pelo NUMERO DA GRU lido dentro do PDF: o Pix do Itau traz
"Identificador: BOLETO<nosso-numero>DATA..."; o boleto pago por codigo de barras/DDA traz a linha digitavel,
de onde o nosso-numero sai tirando os digitos verificadores (convenio de 7 posicoes do Banco do Brasil).
Fail-closed: comprovante sem texto, sem GRU conhecida, com valor diferente ou repetido para a mesma GRU
vira ALERTA no livro — nunca vinculo silencioso. Os originais nunca sao movidos nem apagados.

Uso:
  python tools/livro_pagamentos_pct.py              # sincroniza: pacotes oficiais + GRUs + comprovantes -> livro + painel
  python tools/livro_pagamentos_pct.py --sem-painel # nao toca no epct_status.json
"""
import hashlib
import html
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import fitz

CEN = Path(__file__).resolve().parent.parent
EPCT = CEN / "EPCT"
PASTA = EPCT / "_GUIAS_PCT_A_PAGAR_20260930"
LIVRO = PASTA / "LIVRO_DE_PAGAMENTOS.json"
MD = PASTA / "PAGAMENTOS_EM_ORDEM.md"
HTML = PASTA / "PAGAR_AGORA.html"
PAG = "https://meu.inpi.gov.br/pag/"
ENTRADA = PASTA / "COMPROVANTES_ENTRADA"
STATUS = EPCT / "epct_status.json"
BR_NOVO = EPCT / "_BR_NOVO_CRYPTO_20260930"
CAIXAS = [ENTRADA, Path.home() / "Downloads" / "Mobile Devices", Path.home() / "Downloads"]
DESDE = datetime(2026, 9, 29)  # comprovantes da Downloads anteriores a isto nao sao do PCT
OPENSSL = Path(r"C:\Program Files\Git\mingw64\bin\openssl.exe")
D9_DIAS = 7  # decisao D9 do operador: pagar em ate 7 dias da transmissao
PREFIXO_NOTA = "[Central/livro]"

SERVICO = {"200": "pedido nacional (BR)", "201": "transmissao (RO/BR)", "266": "busca internacional (ISA/BR)",
           "253": "copia oficial da prioridade", "293": "taxa internacional (CHF, cambio do dia util anterior)"}
VALOR_FIXO = {"201": 130.0, "266": 1255.0, "253": 90.0}
NOME = {"ACOM_MIRROR": "ACOM Mirror", "ACOM_CRYPTO": "ACOM Crypto", "TGL_TENSOR": "TGL Tensor", "IALD": "IALD",
        "SUPERCONDUTOR": "Supercondutor", "MOTOR_DOBRA": "Motor de Dobra", "PSI_NET": "Psi-NET", "FUSAO_FRIO": "Fusao a Frio",
        "MQC": "MQC", "DIPOLO_TRANSISTOR": "Dipolo Transistor", "CELULA_REVERSAO": "Celula de Reversao", "SKYGRID": "SkyGrid",
        "APRENDIZADO_CONTINUO": "Aprendizado Continuo", "ONCOLOGIA": "Oncologia", "KERNEL_ONTOLOGICO": "Kernel Ontologico"}
# Pedidos ainda NAO transmitidos: as prioridades planejadas (decisoes D6 e da ORDEM 004). Quando o pacote oficial
# aparecer em RECIBOS, ele substitui este plano.
PLANO_SEM_PACOTE = {
    "BR102026003431-2_ACOM_CRYPTO": {"prioridades": ["PCT/BR2025/050558", "1020260034282", "1020260034312", "1020260034533",
                                                      "BR NOVO DO CRYPTO (numero a ler no recibo do MSP)"],
                                     "folhas_estimadas": 22,
                                     "situacao": "PCT do Crypto NAO transmitido: pacote liberado (ADENDO 003); falta o numero do BR novo "
                                                 "(recibo no Modulo de Servicos de Patentes); 5 prioridades (decisao D6)"},
    "BR102026005707-0_ONCOLOGIA": {"prioridades": ["1020260057070"], "folhas_estimadas": 24,
                                   "situacao": "PCT da Oncologia NAO transmitido: rascunho df90000065449257 com os 4 anexos liberados; "
                                               "falta a autorizacao de assinatura e a transmissao"},
}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def agora() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def nome_curto(dev: str) -> str:
    suf = dev.split("_", 1)[1] if "_" in dev else dev
    return NOME.get(suf, suf.replace("_", " "))


def chf_293(folhas: int) -> float:
    return round((1330 + 15 * max(0, folhas - 30) - 200) * 0.10, 2)


def mais_um_mes(d: date) -> date:
    y, m = (d.year + (d.month // 12), d.month % 12 + 1)
    for dia in (d.day, 30, 29, 28):
        try:
            return date(y, m, dia)
        except ValueError:
            continue
    raise ValueError(d)


# ------------------------------------------------------------ pacotes oficiais (RO WASP)
def _unwrap(b: bytes) -> bytes:
    if not OPENSSL.is_file():
        raise SystemExit(f"FALHA VISIVEL: openssl nao encontrado em {OPENSSL}")
    with tempfile.TemporaryDirectory() as t:
        i, o = Path(t) / "i.p7", Path(t) / "o.bin"
        i.write_bytes(b)
        r = subprocess.run([str(OPENSSL), "cms", "-verify", "-noverify", "-binary", "-inform", "DER", "-in", str(i), "-out", str(o)],
                           capture_output=True, text=True)
        if r.returncode != 0 or "Verification successful" not in (r.stderr + r.stdout):
            raise SystemExit("FALHA VISIVEL: envelope CMS nao confere: " + (r.stderr or r.stdout)[:300])
        return o.read_bytes()


def _tx(el, path):
    x = el.find(path)
    return (x.text or "").strip() if x is not None and x.text else ""


def ler_pacote_oficial(dev_dir: Path):
    zips = sorted(dev_dir.glob("RECIBOS/DOCUMENTOS_OFICIAIS_WIPO_*/*-rowsp-*.zip"))
    if not zips:
        return None
    zz = zipfile.ZipFile(zips[-1])
    z1 = zipfile.ZipFile(io.BytesIO(_unwrap(zz.read(zz.namelist()[0]))))
    rz = zipfile.ZipFile(io.BytesIO(_unwrap(z1.read("RECEIPT.dat"))))
    bz = zipfile.ZipFile(io.BytesIO(_unwrap(z1.read("BLOB.dat"))))
    rec = ET.fromstring(rz.read("receipt.xml"))
    raw = bz.read([n for n in bz.namelist() if n.endswith("-requ.xml")][0]).decode("utf-8")
    rq = ET.fromstring(raw[raw.index("<request"):])
    prios = [_tx(c, "doc-number") for c in rq.findall("priority-claims/priority-claim") if c.find("priority-doc-requested") is not None]
    folhas = sum(int(e.get("page-count")) for e in rq.find("check-list") if e.get("page-count"))
    d = _tx(rec, "received-on/date")
    return {"pct": _tx(rec, "document-id/doc-number"), "data": f"{d[:4]}-{d[4:6]}-{d[6:]}", "hora_BRT": _tx(rec, "received-on/time"),
            "codigo_resposta": _tx(rec, "response/code"), "prioridades_com_documento": prios, "folhas_total": folhas,
            "pacote": str(zips[-1].relative_to(CEN)), "pacote_sha256": sha(zips[-1].read_bytes())}


# ------------------------------------------------------------ GRUs emitidas
def ler_grus():
    grus = {}
    for f in sorted(EPCT.glob("BR*/RECIBOS/GRU_*_EMISSAO.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        n = str(d["numero_gru"])
        if n in grus:
            raise SystemExit(f"FALHA VISIVEL: GRU {n} registrada duas vezes ({grus[n]['registro']} e {f})")
        grus[n] = {"gru": n, "codigo": str(d["codigo_servico"]), "valor_brl": float(d["valor_brl"]) if d.get("valor_brl") is not None else None,
                   "pedido": f.parent.parent.name, "pct_destino": d.get("destinacao_operacional"),
                   "processo_253": d.get("processo_administrativo_informado_pag"), "emitida_em": d.get("data") or (d.get("observado_em") or "")[:10],
                   "segunda_via": d.get("download"), "registro": str(f.relative_to(CEN)), "registro_sha256": sha(f.read_bytes()),
                   "situacao_no_registro": d.get("status")}
    for f in sorted(BR_NOVO.glob("REGISTRO_COMPROVANTE_GRU200_*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        n = str(d["gru_number"])
        grus[n] = {"gru": n, "codigo": "200", "valor_brl": float(d["amount_brl"]), "pedido": "_BR_NOVO_CRYPTO_20260930",
                   "pct_destino": None, "processo_253": None, "emitida_em": "2026-09-30",
                   "segunda_via": None, "registro": str(f.relative_to(CEN)), "registro_sha256": sha(f.read_bytes()),
                   "situacao_no_registro": d.get("status"),
                   "comprovante_registrado": d.get("copy", {}).get("path"), "comprovante_registrado_sha256": d.get("copy", {}).get("sha256")}
    return grus


# ------------------------------------------------------------ comprovantes
LD = re.compile(r"(\d{5})\.?(\d{5})\s+(\d{5})\.?(\d{6})\s+(\d{5})\.?(\d{6})\s+(\d)\s+(\d{14})")


def numeros_no_texto(t: str) -> set:
    achados = set(re.findall(r"BOLETO(\d{17})", t))
    achados |= set(re.findall(r"(?<!\d)(29409\d{12})(?!\d)", t))  # 2940916... (201/266/253/200) e 2940915... (293)
    for m in LD.finditer(t):
        f1, f2, f3 = m.group(1) + m.group(2), m.group(3) + m.group(4), m.group(5) + m.group(6)
        livre = f1[4:9] + f2[:10] + f3[:10]
        achados.add(livre[6:23])
    for m in re.finditer(r"(?<!\d)(\d{44})(?!\d)", re.sub(r"[ .\-]", "", t)):
        achados.add(m.group(1)[19:44][6:23])
    return achados


def valores_no_texto(t: str) -> list:
    vs = re.findall(r"R\$\s*([\d\.]+,\d{2})", t)
    vs += re.findall(r"(?i)valor (?:da transação|final|do documento|pago|original):\s*(?:R\$\s*)?([\d\.]+,\d{2})", t)
    return [float(v.replace(".", "").replace(",", ".")) for v in vs]


def data_do_pagamento(t: str):
    """A data/hora do PAGAMENTO, lida da frase do comprovante (nunca a 1a data da pagina, que pode ser o vencimento)."""
    for rx in (r"Pagamento efetuado em (\d{2}/\d{2}/\d{4}) às (\d{2}:\d{2}(?::\d{2})?)",
               r"Realizad[oa] em (\d{2}/\d{2}/\d{4}) às (\d{2}:\d{2}(?::\d{2})?)",
               r"Pago em (\d{2}/\d{2}/\d{4})(?:\s*(?:às|-)\s*(\d{2}:\d{2}(?::\d{2})?))?"):
        m = re.search(rx, t)
        if m:
            return m.group(1) + (" " + m.group(2) if m.lastindex and m.lastindex >= 2 and m.group(2) else "")
    return None


def id_da_transacao(t: str):
    m = re.search(r"ID da transa[cç][aã]o:\s*(E[0-9A-Za-z]{20,})", t)
    return m.group(1) if m else None


def varrer_comprovantes(grus: dict):
    """Devolve (achados, guias, alertas, originais). Le PDFs das caixas, pagina a pagina; nao move nada.
    achados: um por pagina de comprovante com GRU conhecida; guias: PDFs de boleto (1 pagina) de GRU conhecida."""
    achados, guias, alertas, originais, vistos = [], [], [], [], set()
    for cx in CAIXAS:
        if not cx.is_dir():
            continue
        for f in sorted(cx.glob("*.pdf")):
            if cx == CAIXAS[-1] and datetime.fromtimestamp(f.stat().st_mtime) < DESDE:
                continue
            b = f.read_bytes()
            h = sha(b)
            if h in vistos:
                continue
            vistos.add(h)
            try:
                doc = fitz.open(stream=b, filetype="pdf")
                t0 = doc[0].get_text() if doc.page_count else ""
            except Exception as e:  # PDF ilegivel: alerta, nunca vinculo
                alertas.append({"tipo": "PDF_ILEGIVEL", "arquivo": str(f), "erro": str(e)[:200]})
                continue
            T0 = t0.upper()
            if "INPI" not in T0 and "29409" not in t0 and "PROPRIEDADE INDUST" not in T0:
                continue  # a 1a pagina nao e do INPI: nao se le o resto (relatorios longos de outras casas)
            if "FICHA DE COMPENSA" in T0 or "LOCAL DE PAGAMENTO" in T0:
                if doc.page_count == 1:  # e a propria guia (boleto)
                    nn = re.search(r"Nosso-N[uú]mero\s*\n\s*(\d{17})", t0)
                    if nn and nn.group(1) in grus:
                        val = re.search(r"\(=\) Valor documento\s*\n\s*R\$\s*([\d\.,]+)", t0)
                        serv = re.search(r"Serviço:\s*(\d{3})", t0)
                        guias.append({"gru": nn.group(1), "arquivo": str(f), "sha256": h, "bytes": len(b),
                                      "servico": serv.group(1) if serv else None,
                                      "valor": float(val.group(1).replace(".", "").replace(",", ".")) if val else None})
                continue
            if doc.page_count > 300:
                alertas.append({"tipo": "PDF_GRANDE_DEMAIS", "arquivo": str(f), "paginas": doc.page_count})
                continue
            achou = False
            for i in range(doc.page_count):
                t = t0 if i == 0 else doc[i].get_text()
                if "COMPROVANTE" not in t.upper():
                    continue
                nums = {n for n in numeros_no_texto(t) if n in grus}
                if not nums:
                    alertas.append({"tipo": "COMPROVANTE_SEM_GRU_CONHECIDA", "arquivo": str(f), "pagina": i + 1, "sha256": h,
                                    "numeros_lidos": sorted(numeros_no_texto(t))})
                    continue
                if len(nums) > 1:
                    alertas.append({"tipo": "COMPROVANTE_COM_VARIAS_GRUS", "arquivo": str(f), "pagina": i + 1, "sha256": h, "grus": sorted(nums)})
                    continue
                achou = True
                achados.append({"gru": nums.pop(), "arquivo": str(f), "sha256": h, "bytes": len(b), "pagina": i + 1,
                                "paginas_total": doc.page_count, "valores_lidos": valores_no_texto(t), "data_lida": data_do_pagamento(t),
                                "id_transacao": id_da_transacao(t), "texto_sha256": sha(t.encode("utf-8"))})
            if achou and doc.page_count > 1:
                originais.append({"arquivo": str(f), "sha256": h, "bytes": len(b), "paginas": doc.page_count})
    for f in sorted(ENTRADA.glob("*")) if ENTRADA.is_dir() else []:
        if f.is_file() and f.suffix.lower() not in (".pdf", ".txt", ".md"):
            alertas.append({"tipo": "COMPROVANTE_EM_IMAGEM", "arquivo": str(f),
                            "o_que_fazer": "salvar o comprovante em PDF pelo app do banco (o livro le o texto do PDF)"})
    return achados, guias, alertas, originais


# ------------------------------------------------------------ o livro
def montar(sem_painel=False):
    antigo = json.loads(LIVRO.read_text(encoding="utf-8")) if LIVRO.is_file() else {}
    pagos_antes = {g["gru"]: g["comprovante"] for g in antigo.get("guias", []) if g.get("gru") and g.get("comprovante")}
    guias_pdf = {g["gru"]: g["guia_pdf"] for g in antigo.get("guias", []) if g.get("gru") and g.get("guia_pdf")}
    originais_antes = {o["sha256"]: o for o in antigo.get("comprovantes_originais", [])}
    grus = ler_grus()
    pedidos = {}
    for d in sorted(EPCT.glob("BR*")):
        if d.is_dir():
            pedidos[d.name] = {"pedido": d.name, "nome": nome_curto(d.name), "oficial": ler_pacote_oficial(d)}

    # comprovantes: os ja vinculados + os novos achados
    achados, guias_achadas, alertas, originais = varrer_comprovantes(grus)
    # os PDFs originais de varios comprovantes: copia BYTE A BYTE, intocada, na pasta de pagamento
    ORIG = PASTA / "COMPROVANTES_ORIGINAIS"
    for o in originais:
        if o["sha256"] in originais_antes and (CEN / originais_antes[o["sha256"]]["copia"]).is_file():
            continue
        ORIG.mkdir(parents=True, exist_ok=True)
        dst = ORIG / Path(o["arquivo"]).name
        if dst.exists() and sha(dst.read_bytes()) != o["sha256"]:
            dst = ORIG / (Path(o["arquivo"]).stem + "_" + o["sha256"][:8] + ".pdf")
        if not dst.exists():
            tmp = dst.with_name(dst.name + ".tmp")
            shutil.copyfile(o["arquivo"], tmp)
            if sha(tmp.read_bytes()) != o["sha256"]:
                tmp.unlink()
                raise SystemExit(f"FALHA VISIVEL: copia do original nao confere: {o['arquivo']}")
            tmp.replace(dst)
        originais_antes[o["sha256"]] = dict(o, copia=str(dst.relative_to(CEN)), copiado_em=agora())
    vinc = dict(pagos_antes)
    for a in achados:
        g = grus[a["gru"]]
        ja = vinc.get(a["gru"])
        if ja:
            mesmo = ((a.get("id_transacao") and ja.get("id_transacao") == a["id_transacao"])
                     or (ja.get("texto_sha256") and ja.get("texto_sha256") == a["texto_sha256"])
                     or (a["paginas_total"] == 1 and ja.get("sha256") == a["sha256"])
                     or (ja.get("origem_sha256") == a["sha256"] and ja.get("pagina", 1) == a["pagina"]))
            if not mesmo and not any(x.get("tipo") == "POSSIVEL_PAGAMENTO_EM_DUPLICIDADE" and x.get("gru") == a["gru"]
                                     and x.get("id_transacao") == a.get("id_transacao") for x in alertas):
                alertas.append({"tipo": "POSSIVEL_PAGAMENTO_EM_DUPLICIDADE", "gru": a["gru"], "comprovante_ja_vinculado": ja["arquivo"],
                                "outro_comprovante": a["arquivo"], "pagina": a["pagina"], "id_transacao": a.get("id_transacao"),
                                "o_que_fazer": "conferir no extrato se a GRU foi paga duas vezes; se foi, pedir restituicao ao INPI"})
            continue
        if g["valor_brl"] is not None and a["valores_lidos"] and not any(abs(v - g["valor_brl"]) < 0.005 for v in a["valores_lidos"]):
            alertas.append({"tipo": "VALOR_DIFERENTE", "gru": a["gru"], "valor_da_guia": g["valor_brl"], "valores_lidos": a["valores_lidos"],
                            "arquivo": a["arquivo"], "pagina": a["pagina"], "o_que_fazer": "nao vinculado; conferir a guia e o comprovante"})
            continue
        derivado = False
        if g["pedido"] == "_BR_NOVO_CRYPTO_20260930" and g.get("comprovante_registrado_sha256") == a["sha256"]:
            destino = CEN / g["comprovante_registrado"].split("Central de Patentes\\", 1)[-1].replace("\\", "/")
        else:
            dd = EPCT / g["pedido"] / "RECIBOS" / "COMPROVANTES_GRU"
            dd.mkdir(parents=True, exist_ok=True)
            dia = "".join(reversed((a["data_lida"] or "").split(" ")[0].split("/"))) or date.today().strftime("%Y%m%d")
            destino = dd / f"COMPROVANTE_{g['codigo']}_{a['gru']}_{dia}.pdf"
            tmp = destino.with_name(destino.name + ".tmp")
            if a["paginas_total"] == 1:
                shutil.copyfile(a["arquivo"], tmp)
                if sha(tmp.read_bytes()) != a["sha256"]:
                    tmp.unlink()
                    raise SystemExit(f"FALHA VISIVEL: copia do comprovante nao confere: {a['arquivo']}")
            else:
                derivado = True
                src = fitz.open(a["arquivo"])
                nd = fitz.open()
                nd.insert_pdf(src, from_page=a["pagina"] - 1, to_page=a["pagina"] - 1)
                nd.save(str(tmp), garbage=3, deflate=True)
                nd.close()
                src.close()
                tx = fitz.open(str(tmp))
                ok = tx.page_count == 1 and sha(tx[0].get_text().encode("utf-8")) == a["texto_sha256"]
                tx.close()
                if not ok:
                    tmp.unlink()
                    raise SystemExit(f"FALHA VISIVEL: a pagina extraida nao tem o texto da original: {a['arquivo']} p.{a['pagina']}")
            if destino.exists():
                velho = fitz.open(str(destino))
                igual = velho.page_count == 1 and sha(velho[0].get_text().encode("utf-8")) == a["texto_sha256"]
                velho.close()
                if igual:
                    tmp.unlink()
                else:
                    destino = dd / f"COMPROVANTE_{g['codigo']}_{a['gru']}_{dia}_{a['sha256'][:8]}_p{a['pagina']}.pdf"
                    tmp.replace(destino)
            else:
                tmp.replace(destino)
        vinc[a["gru"]] = {"arquivo": str(destino.relative_to(CEN)), "sha256": sha(destino.read_bytes()), "origem": a["arquivo"],
                          "origem_sha256": a["sha256"], "pagina": a["pagina"], "paginas_total": a["paginas_total"],
                          "derivado_de_pdf_com_varios": derivado, "texto_sha256": a["texto_sha256"], "id_transacao": a.get("id_transacao"),
                          "valores_lidos": a["valores_lidos"], "data_lida": a["data_lida"], "vinculado_em": agora()}
    # os PDFs das guias (boletos): copia BYTE A BYTE para RECIBOS/GUIAS_PDF do pedido, conferidos contra o registro
    for gp in guias_achadas:
        g = grus[gp["gru"]]
        if gp["gru"] in guias_pdf and (CEN / guias_pdf[gp["gru"]]["arquivo"]).is_file():
            continue
        if gp["servico"] != g["codigo"] or gp["valor"] is None or g["valor_brl"] is None or abs(gp["valor"] - g["valor_brl"]) > 0.004:
            alertas.append({"tipo": "GUIA_PDF_DIVERGE_DO_REGISTRO", "gru": gp["gru"], "arquivo": gp["arquivo"], "servico_pdf": gp["servico"],
                            "codigo_registro": g["codigo"], "valor_pdf": gp["valor"], "valor_registro": g["valor_brl"]})
            continue
        dd = (EPCT / g["pedido"] / "RECIBOS" / "GUIAS_PDF") if g["pedido"].startswith("BR") else (EPCT / g["pedido"])
        dd.mkdir(parents=True, exist_ok=True)
        dst = dd / f"GRU_{g['codigo']}_{gp['gru']}.pdf"
        if dst.exists() and sha(dst.read_bytes()) == gp["sha256"]:
            pass
        elif dst.exists():
            continue  # ja ha uma copia desta guia (outro download do mesmo boleto)
        else:
            tmp = dst.with_name(dst.name + ".tmp")
            shutil.copyfile(gp["arquivo"], tmp)
            if sha(tmp.read_bytes()) != gp["sha256"]:
                tmp.unlink()
                raise SystemExit(f"FALHA VISIVEL: copia da guia nao confere: {gp['arquivo']}")
            tmp.replace(dst)
        guias_pdf[gp["gru"]] = {"arquivo": str(dst.relative_to(CEN)), "sha256": gp["sha256"], "origem": gp["arquivo"], "copiado_em": agora()}
    # comprovante vinculado que sumiu do disco: alerta
    for n, c in vinc.items():
        if not (CEN / c["arquivo"]).is_file():
            alertas.append({"tipo": "COMPROVANTE_VINCULADO_SUMIU", "gru": n, "arquivo": c["arquivo"]})

    # guias por pedido: as emitidas + as que ainda faltam emitir
    guias, ordem = [], 0
    hoje = date.today()

    def chave(p):
        of = pedidos[p]["oficial"]
        return (0, of["pct"]) if of else (1, {"BR102026003431-2_ACOM_CRYPTO": "1", "BR102026005707-0_ONCOLOGIA": "2"}.get(p, "9"))

    for p in sorted(pedidos, key=chave):
        of = pedidos[p]["oficial"]
        plano = PLANO_SEM_PACOTE.get(p)
        if not of and not plano:
            continue
        prios = of["prioridades_com_documento"] if of else plano["prioridades"]
        folhas = of["folhas_total"] if of else plano["folhas_estimadas"]
        transm = date.fromisoformat(of["data"]) if of else None
        emit = [g for g in grus.values() if g["pedido"] == p]
        esperado = [("201", None), ("266", None)] + [("253", pr) for pr in prios] + [("293", None)]
        usados = set()
        for cod, pr in esperado:
            cand = [g for g in emit if g["codigo"] == cod and g["gru"] not in usados]
            if cod == "253" and pr:
                alvo = re.sub(r"\D", "", pr)
                exato = [g for g in cand if re.sub(r"\D", "", str(g.get("processo_253") or "")) == alvo]
                cand = exato or cand
            g = cand[0] if cand else None
            if g:
                usados.add(g["gru"])
            ordem += 1
            item = {"ordem": ordem, "pedido": p, "nome": pedidos[p]["nome"], "pct": of["pct"] if of else None,
                    "transmitido_em": of["data"] if of else None, "codigo": cod, "servico": SERVICO[cod], "prioridade": pr,
                    "gru": g["gru"] if g else None, "valor_brl": (g["valor_brl"] if g else VALOR_FIXO.get(cod)),
                    "valor_chf_referencia": chf_293(folhas) if cod == "293" else None,
                    "segunda_via": g["segunda_via"] if g else None, "registro_emissao": g["registro"] if g else None,
                    "registro_sha256": g["registro_sha256"] if g else None,
                    "guia_pdf": guias_pdf.get(g["gru"]) if g else None}
            if transm:
                item["pagar_ate_D9"] = (transm + timedelta(days=D9_DIAS)).isoformat()
                item["prazo_legal_1_mes"] = mais_um_mes(transm).isoformat()
            if g and g["gru"] in vinc:
                item["situacao"] = "PAGA_COM_COMPROVANTE"
                item["comprovante"] = vinc[g["gru"]]
            elif g:
                item["situacao"] = "EMITIDA_AGUARDANDO_PAGAMENTO"
                if cod == "293":
                    item["pagar_no_dia"] = g["emitida_em"]
                    if g["emitida_em"] and g["emitida_em"] < hoje.isoformat():
                        alertas.append({"tipo": "GRU_293_DE_OUTRO_DIA_NAO_PAGA", "gru": g["gru"], "pedido": p, "emitida_em": g["emitida_em"],
                                        "o_que_fazer": "NAO pagar esta 293 (o cambio era o do dia da emissao); pedir ao Codex uma 293 nova no dia do pagamento"})
            elif cod == "293":
                item["situacao"] = "A_EMITIR_NO_DIA_DO_PAGAMENTO" if of else "A_EMITIR_APOS_A_TRANSMISSAO"
            else:
                item["situacao"] = "A_EMITIR" if of else "A_EMITIR_APOS_A_TRANSMISSAO"
            guias.append(item)
        sobra = [g for g in emit if g["gru"] not in usados]
        for g in sobra:
            alertas.append({"tipo": "GRU_EMITIDA_FORA_DO_PLANO", "gru": g["gru"], "codigo": g["codigo"], "pedido": p,
                            "o_que_fazer": "conferir se e duplicata antes de pagar"})
        if of and of["codigo_resposta"] != "0":
            alertas.append({"tipo": "RECIBO_COM_CODIGO_DIFERENTE_DE_ZERO", "pedido": p, "pct": of["pct"]})
    # a GRU 200 do BR novo do Crypto
    for g in grus.values():
        if g["codigo"] == "200":
            ordem += 1
            item = {"ordem": ordem, "pedido": g["pedido"], "nome": "BR novo do Crypto", "pct": None, "codigo": "200", "servico": SERVICO["200"],
                    "gru": g["gru"], "valor_brl": g["valor_brl"], "registro_emissao": g["registro"], "registro_sha256": g["registro_sha256"]}
            if g["gru"] in vinc:
                item["situacao"], item["comprovante"] = "PAGA_COM_COMPROVANTE", vinc[g["gru"]]
            elif g.get("comprovante_registrado") and Path(g["comprovante_registrado"]).is_file() \
                    and sha(Path(g["comprovante_registrado"]).read_bytes()) == g.get("comprovante_registrado_sha256"):
                item["situacao"] = "PAGA_COM_COMPROVANTE"
                item["comprovante"] = {"arquivo": str(Path(g["comprovante_registrado"]).relative_to(CEN)), "sha256": g["comprovante_registrado_sha256"],
                                       "origem": "registro de 30/09/2026", "vinculado_em": agora()}
            else:
                item["situacao"] = "PAGA_SEM_COMPROVANTE_NO_DISCO"
            guias.append(item)

    def soma(f):
        return round(sum(g["valor_brl"] or 0 for g in guias if f(g)), 2)

    resumo = {
        "emitidas_aguardando": sum(g["situacao"] == "EMITIDA_AGUARDANDO_PAGAMENTO" for g in guias),
        "emitidas_aguardando_brl": soma(lambda g: g["situacao"] == "EMITIDA_AGUARDANDO_PAGAMENTO"),
        "a_emitir": sum(g["situacao"].startswith("A_EMITIR") for g in guias),
        "a_emitir_brl_sem_293": soma(lambda g: g["situacao"].startswith("A_EMITIR") and g["codigo"] != "293"),
        "a_emitir_293_chf_referencia": round(sum(g["valor_chf_referencia"] or 0 for g in guias if g["codigo"] == "293" and g["situacao"].startswith("A_EMITIR")), 2),
        "pagas_com_comprovante": sum(g["situacao"] == "PAGA_COM_COMPROVANTE" for g in guias),
        "pagas_brl": soma(lambda g: g["situacao"] == "PAGA_COM_COMPROVANTE"),
        "alertas": len(alertas),
    }
    livro = {"_doc": "Gerado por tools/livro_pagamentos_pct.py (Central de Patentes). NAO editar a mao; o Codex nao escreve aqui.",
             "gerado_em": agora(), "regras": {
                 "D9": f"pagar em ate {D9_DIAS} dias da transmissao (decisao do operador)",
                 "prazo_legal": "1 mes do recebimento pelo RO (Regras 14.1(c), 15.3 e 16.1(f) do PCT) [LEGAL]",
                 "293": "emitir e pagar NO MESMO DIA; cambio do dia util anterior ao pagamento; nunca antes do deposito; "
                        "CHF = (1330 + 15 x folhas acima de 30 - 200) x 0,10",
                 "nao_reemitir": "guia emitida nao se reemite; a segunda via e pelo link (login no PAG)"},
             "resumo": resumo, "pedidos": {p: v["oficial"] for p, v in pedidos.items() if v["oficial"]},
             "guias": guias, "alertas": alertas,
             "comprovantes_originais": sorted(originais_antes.values(), key=lambda o: o["arquivo"])}
    escrever_json(LIVRO, livro)
    escrever_texto(MD, gerar_md(livro))
    escrever_texto(HTML, gerar_html(livro))
    if not sem_painel:
        atualizar_painel(livro)
    return livro


def escrever_json(p: Path, obj):
    escrever_texto(p, json.dumps(obj, ensure_ascii=False, indent=1))


def escrever_texto(p: Path, s: str):
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(s, encoding="utf-8")
    if tmp.stat().st_size < 50:
        raise SystemExit(f"FALHA VISIVEL: escrita curta demais em {p}")
    tmp.replace(p)


def brl(v):
    return "—" if v is None else ("R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))


def chf(v):
    return "CHF " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def gerar_md(L):
    R = L["resumo"]
    o = ["# PAGAMENTOS EM ORDEM — as guias do PCT, uma a uma, e o comprovante de cada uma", "",
         f"> Gerado por `tools/livro_pagamentos_pct.py` em {L['gerado_em']}. **Não editar à mão**: rodar o script de novo.",
         "> Os números de GRU vêm dos registros de emissão; o número PCT e a data vêm do pacote oficial assinado pela WIPO.", "",
         "## Resumo", "",
         f"- **Emitidas, aguardando pagamento:** {R['emitidas_aguardando']} guias, {brl(R['emitidas_aguardando_brl'])}",
         f"- **Ainda a emitir:** {R['a_emitir']} guias: {brl(R['a_emitir_brl_sem_293'])} nas 201/266/253 + as 293 "
         f"(referência {chf(R['a_emitir_293_chf_referencia'])}, em reais só no dia)",
         f"- **Pagas, com comprovante vinculado:** {R['pagas_com_comprovante']} guias, {brl(R['pagas_brl'])}",
         f"- **Alertas:** {R['alertas']}", "",
         "## Como pagar sem se perder", "",
         "1. Pague **pedido por pedido**, na ordem da tabela. Um pedido está quitado quando todas as linhas dele ficam ✅.",
         "2. **A 293 só existe no dia**: é emitida e paga **no mesmo dia**, com o câmbio do dia útil anterior. Nunca pagar 293 de outro dia.",
         "3. A segunda via de cada guia já emitida é o link da coluna GRU (pede login no PAG). **Nunca emitir outra guia para o mesmo serviço.**",
         "4. **Comprovante:** salve o comprovante em PDF (Pix ou boleto) e mande para o PC (como o de 30/09, em `Downloads\\Mobile Devices`) "
         "ou coloque em `EPCT\\_GUIAS_PCT_A_PAGAR_20260930\\COMPROVANTES_ENTRADA\\`. O nome do arquivo não importa: "
         "o script lê o número da GRU dentro do PDF, copia para `EPCT\\<pedido>\\RECIBOS\\COMPROVANTES_GRU\\` e marca a linha.",
         "5. O livro avisa se uma GRU aparecer paga duas vezes, se o valor não bater ou se um comprovante não tiver GRU conhecida.", ""]
    if L["alertas"]:
        o += ["## ⚠ Alertas", ""]
        for a in L["alertas"]:
            o.append("- **" + a["tipo"] + "** — " + "; ".join(f"{k}: {v}" for k, v in a.items() if k != "tipo"))
        o.append("")
    o += ["## As guias, na ordem de pagar", ""]
    atual = None
    marca = {"PAGA_COM_COMPROVANTE": "✅ paga", "EMITIDA_AGUARDANDO_PAGAMENTO": "⬜ a pagar", "A_EMITIR": "⏳ a emitir",
             "A_EMITIR_NO_DIA_DO_PAGAMENTO": "⏳ emitir no dia", "A_EMITIR_APOS_A_TRANSMISSAO": "⏳ depois da transmissão",
             "PAGA_SEM_COMPROVANTE_NO_DISCO": "⚠ paga, sem comprovante no disco"}
    for g in L["guias"]:
        cab = (g["pedido"], g.get("pct"))
        if cab != atual:
            atual = cab
            prazo = f" — transmitido em {g['transmitido_em']}; **pagar até {g['pagar_ate_D9']}** (D9); prazo legal {g['prazo_legal_1_mes']} [LEGAL]" \
                if g.get("transmitido_em") else ""
            tit = g.get("pct") or ("pedido nacional; número a ler no recibo do MSP" if g["codigo"] == "200" else "PCT ainda não transmitido")
            o += ["", f"### {g['nome']} — {tit}{prazo}", "",
                  "| # | Cód. | Serviço | GRU | Valor | Situação | Comprovante |", "|---:|---|---|---|---:|---|---|"]
        gru = f"[{g['gru']}]({g['segunda_via']})" if g.get("gru") and g.get("segunda_via") else (g.get("gru") or "—")
        serv = g["servico"] + (f" — prioridade {g['prioridade']}" if g.get("prioridade") else "")
        if g["codigo"] != "293":
            val = brl(g["valor_brl"])
        elif g.get("gru") and g.get("valor_brl") is not None:
            val = f"{brl(g['valor_brl'])} ({chf(g['valor_chf_referencia'])})"
        else:
            val = f"{chf(g['valor_chf_referencia'])} (R$ no dia)"
        comp = ("`" + g["comprovante"]["arquivo"] + "`") if g.get("comprovante") else ""
        if g.get("pagar_no_dia") and g["situacao"] != "PAGA_COM_COMPROVANTE":
            val += f" — **pagar em {g['pagar_no_dia']}, o dia da emissão**"
        o.append(f"| {g['ordem']} | {g['codigo']} | {serv} | {gru} | {val} | {marca.get(g['situacao'], g['situacao'])} | {comp} |")
    o += ["", "## O que este livro não faz", "",
          "Não paga, não emite guia, não acessa o PAG nem o banco. Só lê os registros e os comprovantes que estão no disco e copia "
          "cada comprovante, byte a byte, para a pasta do pedido. Prazo é [LEGAL]: conferir com o agente da PI.", ""]
    return "\n".join(o)


def gerar_html(L):
    """A pagina de pagar: todas as guias na ordem, um botao por guia (abre a guia ja emitida no PAG). Gerada; nunca editar."""
    e = html.escape
    R = L["resumo"]
    n293 = sum(1 for g in L["guias"] if g["codigo"] == "293" and g["situacao"].startswith("A_EMITIR"))
    blocos = []
    grupos = []
    for g in L["guias"]:
        cab = (g["pedido"], g.get("pct"))
        if not grupos or grupos[-1][0] != cab:
            grupos.append((cab, []))
        grupos[-1][1].append(g)
    for cab, gs in grupos:
        g0 = gs[0]
        prazo = (f"pagar até <b>{e(g0['pagar_ate_D9'])}</b> · prazo legal {e(g0['prazo_legal_1_mes'])} [LEGAL]"
                 if g0.get("pagar_ate_D9") else "")
        tit = g0.get("pct") or ("BR 102026024913-0 (pedido nacional)" if g0["codigo"] == "200" else "")
        linhas = []
        for g in gs:
            serv = g["servico"] + (f" — prioridade {g['prioridade']}" if g.get("prioridade") else "")
            if g["codigo"] == "293" and g.get("valor_brl") is None:
                val = chf(g["valor_chf_referencia"])
            else:
                val = brl(g["valor_brl"]) + (f" <small>({chf(g['valor_chf_referencia'])})</small>" if g["codigo"] == "293" else "")
            st = g["situacao"]
            if st == "PAGA_COM_COMPROVANTE":
                acao, cls = "<span class=ok>✓ paga</span>", "paga"
            elif st == "EMITIDA_AGUARDANDO_PAGAMENTO" and g.get("segunda_via"):
                acao, cls = f"<a class=btn href=\"{e(g['segunda_via'])}\" target=_blank rel=noopener>Abrir guia</a>", "apagar"
            elif st.startswith("A_EMITIR"):
                acao, cls = "<span class=esp>o Codex ainda emite</span>", "aemitir"
            else:
                acao, cls = f"<span class=esp>{e(st)}</span>", "aemitir"
            dia = (f"<div class=hoje>pagar em {e(g['pagar_no_dia'])}, o dia da emissão</div>"
                   if g.get("pagar_no_dia") and st != "PAGA_COM_COMPROVANTE" else "")
            chk = (f"<input type=checkbox data-g=\"{e(g['gru'])}\" aria-label=\"marcar como pago\">"
                   if g.get("gru") and st != "PAGA_COM_COMPROVANTE" else "")
            linhas.append(f"<tr class={cls}><td class=c>{chk}</td><td><b>{e(g['codigo'])}</b> {e(serv)}"
                          f"<div class=gru>GRU {e(g.get('gru') or '—')}</div>{dia}</td><td class=v>{val}</td><td class=a>{acao}</td></tr>")
        blocos.append(f"<section><h2>{e(g0['nome'])} <span class=pct>{e(tit)}</span></h2><p class=prazo>{prazo}</p>"
                      f"<table>{''.join(linhas)}</table></section>")
    alertas = "".join("<li><b>" + e(a["tipo"]) + "</b> — " + e("; ".join(f"{k}: {v}" for k, v in a.items() if k != "tipo")) + "</li>"
                      for a in L["alertas"])
    css = """
:root{--bg:#fbfaf7;--fg:#1d1d1b;--mut:#6b6b66;--line:#e4e1d8;--card:#fff;--acc:#1f5d8c;--onacc:#fff;--ok:#2e7d32;--warn:#b25b00}
@media (prefers-color-scheme:dark){:root{--bg:#151514;--fg:#eceae3;--mut:#a3a19a;--line:#33322e;--card:#1e1d1b;--acc:#7db4e0;--onacc:#111;--ok:#81c784;--warn:#ffb74d}}
body{background:var(--bg);color:var(--fg);font:16px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif;margin:0;padding:16px}
main{max-width:880px;margin:auto}h1{font-size:1.5rem;margin:.2em 0}h2{font-size:1.1rem;margin:0}
.pct{color:var(--mut);font-weight:400;font-size:.9rem;margin-left:.4em}.prazo{color:var(--mut);margin:.2em 0 .6em;font-size:.9rem}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;margin:12px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px}.card b{display:block;font-size:1.2rem}
section{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px;margin:12px 0}
table{width:100%;border-collapse:collapse}td{border-top:1px solid var(--line);padding:8px 6px;vertical-align:top}
td.v{white-space:nowrap;text-align:right}td.a{text-align:right;white-space:nowrap}td.c{width:24px}
.gru{color:var(--mut);font-size:.85rem;font-family:ui-monospace,Consolas,monospace}.hoje{color:var(--warn);font-size:.85rem;font-weight:600}
.btn{display:inline-block;background:var(--acc);color:var(--onacc);text-decoration:none;padding:6px 12px;border-radius:7px;font-weight:600}
.ok{color:var(--ok);font-weight:600}.esp{color:var(--mut);font-size:.9rem}tr.marcada td{opacity:.45}ol li{margin:.25em 0}
.al{border-color:var(--warn)}small{color:var(--mut)}
@media (max-width:560px){td.v,td.a{display:block;text-align:left;border-top:0;padding-top:0}}
"""
    js = """
document.querySelectorAll('input[data-g]').forEach(function(c){var k='pct-pago-'+c.dataset.g;
try{if(localStorage.getItem(k)==='1'){c.checked=true;c.closest('tr').classList.add('marcada')}}catch(err){}
c.addEventListener('change',function(){c.closest('tr').classList.toggle('marcada',c.checked);
try{localStorage.setItem(k,c.checked?'1':'0')}catch(err){}})});
"""
    secao_al = ("<section class=al><h2>Alertas</h2><ul>" + alertas + "</ul></section>") if alertas else ""
    return ("<!doctype html><html lang=pt-BR><head><meta charset=utf-8>"
            "<meta name=viewport content=\"width=device-width,initial-scale=1\"><title>Pagar guias PCT</title>"
            "<style>" + css + "</style></head><body><main>"
            "<h1>Pagar as guias do PCT</h1>"
            f"<p class=prazo>Gerada por <code>tools/livro_pagamentos_pct.py</code> em {e(L['gerado_em'])}. Não editar: rodar o script de novo.</p>"
            "<div class=cards>"
            f"<div class=card>Emitidas, a pagar<b>{R['emitidas_aguardando']} guias · {brl(R['emitidas_aguardando_brl'])}</b></div>"
            f"<div class=card>293 ainda a emitir<b>{n293} · {chf(R['a_emitir_293_chf_referencia'])}</b><small>em reais só no dia da emissão</small></div>"
            f"<div class=card>Pagas, com comprovante<b>{R['pagas_com_comprovante']} · {brl(R['pagas_brl'])}</b></div></div>"
            + secao_al +
            "<section><h2>Como pagar</h2><ol>"
            f"<li>Entre no <a href=\"{PAG}\" target=_blank rel=noopener>PAG do INPI</a> <b>neste mesmo navegador</b>. "
            "Os botões abrem a guia já emitida; nunca emita outra.</li>"
            "<li>Em cada linha: <b>Abrir guia</b> → pague pelo Pix da guia (ou pelo código de barras).</li>"
            "<li>Mande cada comprovante em PDF do celular para o PC, como o de 30/09. A Central liga cada comprovante à sua guia pelo número.</li>"
            "<li>A <b>293</b> só se paga <b>no mesmo dia em que foi emitida</b>.</li></ol>"
            "<p class=prazo>A caixinha de cada linha é só para você se guiar (fica neste navegador). O registro oficial é o comprovante.</p></section>"
            + "".join(blocos) +
            "</main><script>" + js + "</script></body></html>")


def atualizar_painel(L):
    st = json.loads(STATUS.read_text(encoding="utf-8")) if STATUS.is_file() else {}
    if STATUS.is_file():
        bak = STATUS.with_name(STATUS.name + ".bak_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
        bak.write_bytes(STATUS.read_bytes())
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    por_pedido = {}
    for g in L["guias"]:
        por_pedido.setdefault(g["pedido"], []).append(g)
    for p, of in L["pedidos"].items():
        dev = st.setdefault(p, {})
        for k in ("transmitido", "recibo_arquivado"):
            if not dev.get(k):
                dev[k], dev[k + "_em"] = True, ts
        dev["pct_number"] = of["pct"]
        dev["protocol_date"] = of["data"]
    for p, gs in por_pedido.items():
        if not (EPCT / p).is_dir() or not p.startswith("BR"):
            continue
        dev = st.setdefault(p, {})
        pagas = all(g["situacao"] == "PAGA_COM_COMPROVANTE" for g in gs)
        if pagas and not dev.get("taxas_pagas"):
            dev["taxas_pagas"], dev["taxas_pagas_em"] = True, ts
        elif not pagas and dev.get("taxas_pagas") and str(dev.get("taxas_pagas_origem", "")) == "livro":
            dev["taxas_pagas"], dev["taxas_pagas_em"] = False, None
        if pagas:
            dev["taxas_pagas_origem"] = "livro"
        n_pg = sum(g["situacao"] == "PAGA_COM_COMPROVANTE" for g in gs)
        of = L["pedidos"].get(p)
        if of:
            cab = (f"{of['pct']} transmitido em {of['data']} {of['hora_BRT'][:2]}:{of['hora_BRT'][2:]} BRT (recibo oficial WIPO conferido "
                   f"no pacote assinado); prioridades com documento pelo RO: {', '.join(of['prioridades_com_documento'])}")
        else:
            cab = PLANO_SEM_PACOTE.get(p, {}).get("situacao", "nao transmitido")
        nota = (f"{PREFIXO_NOTA} {cab}. Guias: {n_pg}/{len(gs)} pagas com comprovante"
                + ("; quitação no PAG e correspondência sobre taxas no ePCT: a conferir pelo Codex" if pagas else "")
                + (f"; pagar até {gs[0]['pagar_ate_D9']} (D9)" if gs[0].get("pagar_ate_D9") and not pagas else "")
                + ". Ver EPCT/_GUIAS_PCT_A_PAGAR_20260930/PAGAMENTOS_EM_ORDEM.md")
        if not dev.get("nota") or str(dev.get("nota")).startswith(PREFIXO_NOTA):
            dev["nota"] = nota
    escrever_texto(STATUS, json.dumps(st, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    L = montar(sem_painel="--sem-painel" in sys.argv)
    R = L["resumo"]
    print(f"livro: {LIVRO}")
    print(f"emitidas aguardando {R['emitidas_aguardando']} ({brl(R['emitidas_aguardando_brl'])}) | a emitir {R['a_emitir']} "
          f"({brl(R['a_emitir_brl_sem_293'])} + 293 {chf(R['a_emitir_293_chf_referencia'])}) | pagas {R['pagas_com_comprovante']} "
          f"({brl(R['pagas_brl'])}) | alertas {R['alertas']}")
    for a in L["alertas"]:
        print("  ALERTA", a["tipo"], {k: v for k, v in a.items() if k != "tipo"})
    sys.exit(1 if any(a["tipo"] in ("POSSIVEL_PAGAMENTO_EM_DUPLICIDADE", "VALOR_DIFERENTE", "COMPROVANTE_VINCULADO_SUMIU",
                                    "RECIBO_COM_CODIGO_DIFERENTE_DE_ZERO") for a in L["alertas"]) else 0)
