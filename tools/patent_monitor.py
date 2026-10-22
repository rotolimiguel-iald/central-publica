# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║  MONITOR DE PATENTES — o vigia dos andamentos (INPI + ePCT)       ║
║  Central de Patentes IALD/TGL. Roda na máquina do operador.       ║
╚══════════════════════════════════════════════════════════════════╝

O QUE FAZ
─────────
Acompanha o andamento administrativo dos 16 processos da Central:
  * AUDITORIA DE PRAZOS (retroativa, roda AGORA, sem rede): computa os prazos legais
    da LPI 9.279/96 a partir das datas de depósito/prioridade de cada docket e verifica,
    processo a processo, se algum prazo passou, está próximo, ou ainda não venceu.
  * RPI (a fonte LEGAL): baixa a Revista da Propriedade Industrial (o "diário oficial"
    das patentes, publicada toda terça) e extrai os despachos dos 16 processos.
  * BUSCA INPI (sinal antecipado, NÃO-OFICIAL): consulta best-effort por processo.
  * ePCT: MANUAL ASSISTIDO — a Central não automatiza o portal WIPO (login+2FA); rastreia
    o status que o operador registra e conta os prazos internacionais, alertando.
Movimentos novos são gravados num store próprio (andamentos/) e viram notas que fluem
para o Prompt Compiler.

A RÉGUA (aqui é sagrada — são PRAZOS LEGAIS)
───────────────────────────────────────────
1. NUNCA dizer "sem movimentação, você está seguro". O monitor sinaliza o que DETECTA
   (sinais positivos) e defere a vigilância autoritativa dos prazos fatais ao operador +
   agente de PI. Todo movimento é marcado para CONFIRMAÇÃO do operador.
2. Uma FALHA de busca é ALTA e visível: "não consegui checar" ≠ "nada mudou". O monitor
   registra a falha ruidosamente e jamais a converte em silêncio tranquilizador.
3. Não sou advogado. Todo prazo é [LEGAL] "conferir com agente" — a auditoria FLAGA
   possíveis problemas; não afirma conformidade legal.
4. NÃO muta os docket.yaml manuais (têm comentários [LEGAL] do operador). Os movimentos
   vão para um store separado (andamentos/), referenciado pelo docket.
5. Zero física aqui: é um monitor jurídico-administrativo. Sem β, sem veredito físico.

USO
───
  python tools/patent_monitor.py --audit                 # auditoria de prazos (offline)
  python tools/patent_monitor.py --backfill                # RPI retroativa pelo XML oficial, desde a RPI 2864 (rede)
  python tools/patent_monitor.py --check-now             # RPI da semana + Busca (rede)
  python tools/patent_monitor.py --status                # o que está no store
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field, asdict
from datetime import date, datetime, timezone
from pathlib import Path

try:
    import yaml  # já usado pelo reindex do backend
except Exception:                                          # pragma: no cover
    print("ERRO: PyYAML ausente (pip install pyyaml). O monitor lê os dockets em YAML.", file=sys.stderr)
    raise

CENTRAL = Path(__file__).resolve().parent.parent
PATENTS_DIR = CENTRAL / "patents"
STORE = CENTRAL / "andamentos"                             # store PRÓPRIO (não muta os dockets)
LEDGER = STORE / "movements.jsonl"                         # append-only, auditável
AUDIT_OUT = STORE / "deadline_audit.json"

# ── Prazos da LPI 9.279/96 (Patente de Invenção — PI). Todos [LEGAL], conferir com agente. ──
# Fontes: LPI Art. 30 (publicação 18m), Art. 33 (exame 36m), Art. 84 (anuidades a partir do
# 3º ano). PCT: fase nacional no BR a 30 meses da prioridade. As janelas são o entendimento
# corrente — casos de contagem, feriados e prorrogações exigem o agente de PI.
DEADLINE_RULES = [
    {"key": "publicacao_18m", "months": 18, "from": "priority",
     "titulo": "Publicação do pedido (LPI Art. 30)",
     "nota": "Publicação automática aos 18 meses da prioridade; pode ser antecipada a pedido. "
             "Antes disso o pedido corre em sigilo — poucos/nenhum despacho público na RPI."},
    {"key": "exame_36m", "months": 36, "from": "filing", "fatal": True,
     "titulo": "Pedido de exame (LPI Art. 33)",
     "nota": "PRAZO FATAL: requerer o exame em até 36 meses do DEPÓSITO. Não requerer => "
             "ARQUIVAMENTO definitivo do pedido. Este é o prazo duro dos pedidos novos."},
    {"key": "anuidade_3a_24m", "months": 24, "from": "filing",
     "titulo": "3ª anuidade — abertura da janela (LPI Art. 84)",
     "nota": "Anuidades a partir do início do 3º ano (24 meses do depósito). Pagamento "
             "ordinário nos 3 meses seguintes; com retribuição adicional, independente de notificação, nos 6 meses "
             "subsequentes (LPI art. 84 §2º). [errata 19/10/2026: o texto anterior dizia «por mais 3 meses»]"},
    {"key": "fase_nacional_pct_30m", "months": 30, "from": "priority", "only_if_pct": True, "fatal": True,
     "titulo": "Fase nacional PCT no BR (30 meses da prioridade)",
     "nota": "PRAZO FATAL para a fase nacional brasileira do PCT (30 meses). A entrada em "
             "OUTROS países varia (30/31m) — conferir país a país com o agente."},
]

DUE_SOON_DAYS = 180        # janela de "vence em breve" (T-180): tempo de agir com o agente


def _months_after(d: date, months: int) -> date:
    """Data + N meses, com clamp do dia (para fins de contagem administrativa aproximada)."""
    m = d.month - 1 + months
    y = d.year + m // 12
    mo = m % 12 + 1
    # clamp do dia ao último dia do mês alvo
    import calendar
    day = min(d.day, calendar.monthrange(y, mo)[1])
    return date(y, mo, day)


def _parse_date(v) -> date | None:
    if isinstance(v, date):
        return v
    if isinstance(v, str):
        for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
            try:
                return datetime.strptime(v.strip(), fmt).date()
            except ValueError:
                pass
    return None


@dataclass
class Docket:
    dir: str
    processo: str | None
    titulo: str | None
    filing_date: date | None
    priority_date: date | None
    has_pct: bool
    pct_numero: str | None
    status: str | None
    alert_level: str | None
    raw: dict = field(default_factory=dict)


def load_dockets() -> list[Docket]:
    out = []
    for dk in sorted(PATENTS_DIR.glob("*/docket.yaml")):
        try:
            y = yaml.safe_load(dk.read_text(encoding="utf-8")) or {}
        except Exception as e:
            print(f"[monitor] AVISO: docket ilegível {dk.parent.name}: {e}", file=sys.stderr)
            continue
        ep = y.get("epct")
        pct_num = (ep.get("numero") if isinstance(ep, dict) else ep) or None
        has_pct = bool(pct_num) and "PCT" in str(pct_num).upper()
        out.append(Docket(
            dir=dk.parent.name, processo=y.get("processo"), titulo=y.get("titulo"),
            filing_date=_parse_date(y.get("filing_date")),
            priority_date=_parse_date(y.get("priority_date")) or _parse_date(y.get("filing_date")),
            has_pct=has_pct, pct_numero=pct_num if has_pct else None,
            status=y.get("status"), alert_level=y.get("alert_level"), raw=y))
    return out


def processos_vigiados() -> set[str]:
    """Os números que a RPI vigia: o `processo` de cada docket e os `processos_adicionais` dele. (05/10/2026: o BR novo do
    Crypto, BR102026024913-0, é a mesma invenção do docket do Crypto e não ganha pasta própria em patents/ — uma pasta nova
    viraria um 17º dispositivo para o FINAL, o índice público e o painel.)"""
    procs = set()
    for d in load_dockets():
        if d.processo:
            procs.add(d.processo)
        for x in (d.raw.get("processos_adicionais") or []):
            n = x.get("processo") if isinstance(x, dict) else x
            if n:
                procs.add(str(n))
    return procs


# ═══════════════════════════════════════════════════════════════════════════════
#  AUDITORIA DE PRAZOS — retroativa, offline, roda AGORA
# ═══════════════════════════════════════════════════════════════════════════════

def audit_deadlines(today: date) -> dict:
    """Computa, processo a processo, os prazos da LPI a partir das datas do docket e
    classifica cada um: nao_vencido | vence_em_breve | VENCIDO_CONFERIR. Nada é afirmado
    como conformidade legal — tudo é [LEGAL] para conferência com o agente."""
    dockets = load_dockets()
    resultados = []
    resumo = {"processos": len(dockets), "processos_adicionais": 0, "prazos_vencidos_a_conferir": 0,
              "prazos_proximos": 0, "prazos_futuros": 0, "sem_data_de_deposito": 0}
    # 19/10/2026: além dos dockets, os processos adicionais com data de depósito própria (fase nacional BR 11 do ACOM; BR novo do Crypto)
    alvos = []
    for d in dockets:
        alvos.append((d.processo, d.dir, d.titulo, d.filing_date, d.priority_date, d.has_pct, None))
        for x in (d.raw.get("processos_adicionais") or []):
            fd = _parse_date(x.get("filing_date")) if isinstance(x, dict) else None
            if isinstance(x, dict) and x.get("processo") and fd:
                alvos.append((str(x["processo"]), d.dir, x.get("papel") or d.titulo, fd, _parse_date(x.get("priority_date")) or fd, False, d.dir))
    for (processo_, dir_, titulo_, base_filing, base_prio, has_pct_, adicional_de) in alvos:
        item = {"processo": processo_, "dir": dir_, "titulo": (titulo_ or "")[:70],
                "filing_date": base_filing.isoformat() if base_filing else None,
                "priority_date": base_prio.isoformat() if base_prio else None,
                "has_pct": has_pct_, "prazos": []}
        if adicional_de:
            item["adicional_de"] = adicional_de
            resumo["processos_adicionais"] += 1
        if not base_filing:
            resumo["sem_data_de_deposito"] += 1
            item["ALERTA"] = "SEM data de depósito no docket — impossível computar prazos [LEGAL]"
            resultados.append(item)
            continue
        for rule in DEADLINE_RULES:
            if rule.get("only_if_pct") and not has_pct_:
                continue
            base = base_prio if rule["from"] == "priority" else base_filing
            if not base:
                continue
            due = _months_after(base, rule["months"])
            dias = (due - today).days
            if dias < 0:
                estado = "VENCIDO_CONFERIR"
                resumo["prazos_vencidos_a_conferir"] += 1
            elif dias <= DUE_SOON_DAYS:
                estado = "vence_em_breve"
                resumo["prazos_proximos"] += 1
            else:
                estado = "nao_vencido"
                resumo["prazos_futuros"] += 1
            item["prazos"].append({
                "prazo": rule["titulo"], "key": rule["key"],
                "vencimento": due.isoformat(), "dias_restantes": dias,
                "estado": estado, "fatal": bool(rule.get("fatal")),
                "base": f"{rule['months']}m de {'prioridade' if rule['from']=='priority' else 'depósito'}",
                "nota_legal": rule["nota"], "marcador": "[LEGAL] conferir com agente de PI",
            })
        resultados.append(item)
    return {
        "gerado_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "referencia_hoje": today.isoformat(),
        "disclaimer": ("AUDITORIA INTERNA — NÃO é parecer jurídico. Computa os prazos da LPI "
                       "9.279/96 a partir das datas dos dockets. VENCIDO_CONFERIR significa 'a data "
                       "computada já passou — CONFIRA com o agente se foi cumprido', jamais 'você "
                       "perdeu o prazo'. Feriados, prorrogações e contagens especiais exigem o agente."),
        "resumo": resumo, "processos": resultados,
    }


def print_audit(rep: dict) -> None:
    r = rep["resumo"]
    print(f"\n{'='*78}\nAUDITORIA DE PRAZOS — {rep['referencia_hoje']} (LPI 9.279/96) [LEGAL, não é parecer]\n{'='*78}")
    print(f"  {r['processos']} processos (+{r.get('processos_adicionais', 0)} adicionais) · vencidos-a-conferir: {r['prazos_vencidos_a_conferir']} · "
          f"próximos (T-{DUE_SOON_DAYS}d): {r['prazos_proximos']} · futuros: {r['prazos_futuros']}"
          + (f" · SEM data: {r['sem_data_de_deposito']}" if r['sem_data_de_deposito'] else ""))
    # o que EXIGE atenção primeiro: vencidos e próximos, fatais no topo
    urgentes = []
    for p in rep["processos"]:
        for z in p.get("prazos", []):
            if z["estado"] in ("VENCIDO_CONFERIR", "vence_em_breve"):
                urgentes.append((p["processo"], z))
    urgentes.sort(key=lambda t: (t[1]["estado"] != "VENCIDO_CONFERIR", not t[1]["fatal"], t[1]["dias_restantes"]))
    if urgentes:
        print(f"\n  ⚠ EXIGEM ATENÇÃO ({len(urgentes)}):")
        for proc, z in urgentes:
            tag = "‼ FATAL" if z["fatal"] else "•"
            print(f"    {tag} {proc}: {z['prazo']} — {z['vencimento']} "
                  f"({z['dias_restantes']}d) [{z['estado']}]")
    else:
        print("\n  ✓ Nenhum prazo vencido nem próximo (T-180d) pela contagem dos dockets.")
        print("    (os processos são jovens; os prazos duros — exame 36m, fase nacional 30m — ainda não chegaram)")
    print("\n  próximos vencimentos por processo:")
    for p in rep["processos"]:
        if not p.get("prazos"):
            print(f"    {p['processo']}: {p.get('ALERTA','—')}"); continue
        prox = min(p["prazos"], key=lambda z: z["dias_restantes"])
        print(f"    {p['processo']} ({p['dir'][:22]}): próximo = {prox['prazo'].split('(')[0].strip()} "
              f"em {prox['vencimento']} ({prox['dias_restantes']}d)")
    print(f"\n  {rep['disclaimer']}\n")


# ═══════════════════════════════════════════════════════════════════════════════
#  ADAPTADORES DE BUSCA — RPI (legal) e Busca INPI (sinal). Falha BARULHENTA.
# ═══════════════════════════════════════════════════════════════════════════════
# NOTA HONESTA: estes adaptadores fazem rede REAL. Não foram validados ao vivo neste
# ambiente — precisam rodar na máquina do operador (com internet). Uma FALHA aqui é ALTA e
# NUNCA é convertida em "sem movimentação". O parse é testável offline em amostra.

RPI_BASE = "https://revistas.inpi.gov.br/rpi/"   # portal da RPI (a URL exata do PDF varia por edição)


def _fetch(url: str, timeout: int = 60) -> bytes:
    """GET simples via stdlib (sem dependências novas). Levanta em qualquer falha — de
    propósito: o chamador PRECISA saber que não conseguiu checar."""
    import urllib.request
    req = urllib.request.Request(url, headers={"User-Agent": "IALD-Central-Monitor/1.0 (patent docket)"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def parse_rpi_text(text: str, process_numbers: set[str]) -> list[dict]:
    """Extrai despachos da RPI (representação em TEXTO) para os processos dados.
    Testável offline: alimente o texto de uma RPI (ou uma amostra) e os números.
    Retorna [{processo, codigo_despacho, trecho}]. O formato da RPI lista, por despacho,
    o número do processo e um código; casamos por número."""
    import re
    found = []
    # normaliza os números (com e sem pontuação) para casar as duas grafias da RPI
    norm = {}
    for pn in process_numbers:
        digits = re.sub(r"\D", "", pn)
        norm[digits] = pn
    CODE = r"\((\d{1,3}\.\d{1,3}(?:\.\d{1,3})?)\)"          # código de despacho (n.n[.n])
    for m in re.finditer(r"(BR\s*\d{2}\s*\d{4}\s*\d{6}[\s\-]*\d)", text):
        digits = re.sub(r"\D", "", m.group(1))
        if digits not in norm:
            continue
        # Na RPI o código do despacho costuma vir LOGO APÓS o número do processo (mesmo bloco).
        # Preferimos o código à FRENTE, numa janela curta; só então caímos para trás. O código
        # é best-effort e deve ser conferido contra a RPI real — a atribuição pode errar em
        # layouts atípicos, por isso vai marcado 'codigo_incerto' quando veio de trás.
        fwd = re.search(CODE, text[m.end(): m.end() + 90])
        incerto = False
        cod = None
        if fwd:
            cod = fwd.group(1)
        else:
            bwd = re.search(CODE, text[max(0, m.start() - 90): m.start()])
            if bwd:
                cod = bwd.group(1); incerto = True
        ctx = text[max(0, m.start() - 40): m.end() + 200]
        found.append({"processo": norm[digits], "codigo_despacho": cod,
                      "codigo_incerto": incerto, "trecho": " ".join(ctx.split())[:300]})
    return found


def fetch_and_parse_rpi(rpi_pdf_url: str, process_numbers: set[str]) -> list[dict]:
    """Baixa um PDF da RPI e extrai os despachos. Requer um extrator de texto de PDF
    (pdfplumber ou PyPDF2). Falha BARULHENTA se ausente ou se a rede cair."""
    data = _fetch(rpi_pdf_url)          # levanta se a rede falhar (de propósito)
    text = None
    try:
        import pdfplumber, io  # type: ignore
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            text = "\n".join((pg.extract_text() or "") for pg in pdf.pages)
    except ImportError:
        try:
            import io
            try:
                from pypdf import PdfReader  # type: ignore  (sucessor do PyPDF2)
            except ImportError:
                from PyPDF2 import PdfReader  # type: ignore
            rd = PdfReader(io.BytesIO(data))
            text = "\n".join((pg.extract_text() or "") for pg in rd.pages)
        except ImportError:
            raise RuntimeError("FALHA: nenhum extrator de PDF instalado (pip install pypdf). "
                               "NÃO consegui LER a RPI — isto NÃO significa 'sem movimentação'.")
    return parse_rpi_text(text or "", process_numbers)


# ── RPI pelo XML OFICIAL (validado ao vivo em 22/09/2026, RPI 2864 a 2907) ─────────────────
# O INPI publica, por edição, `txt/P<n>.zip` contendo `Patente_<n>_<ddmmaaaa>.xml`: um <despacho> por ato, com
# <codigo>, <titulo>, <processo-patente>/<numero> e <comentario>. Casar por número é exato (sem heurística de PDF).
# O servidor só responde a User-Agent de navegador (sem ele, a conexão pendura). Edição ainda não publicada devolve
# uma página HTML em vez do zip: isso é «ainda não saiu», não falha.
RPI_XML_URL = "https://revistas.inpi.gov.br/txt/P{n}.zip"
RPI_STATE = STORE / "rpi_state.json"
RPI_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) IALD-Central-Monitor/1.1"
RPI_PRIMEIRA = 2864          # RPI de 25/11/2025, antes do 1º depósito da família (05/12/2025)


def fetch_rpi_xml(n: int, process_numbers: set[str], timeout: int = 120) -> dict | None:
    """Baixa a edição n da RPI (XML oficial) e devolve {numero, data, despachos:[...]} só dos processos dados.
    None = a edição ainda não existe. Qualquer outra falha LEVANTA (o chamador registra como FALHA)."""
    import io, re, urllib.request, zipfile
    import xml.etree.ElementTree as ET
    req = urllib.request.Request(RPI_XML_URL.format(n=n), headers={"User-Agent": RPI_UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
    if data[:2] != b"PK":
        return None
    zf = zipfile.ZipFile(io.BytesIO(data))
    xn = [x for x in zf.namelist() if x.lower().endswith(".xml")]
    if not xn:
        raise RuntimeError(f"RPI {n}: zip sem XML ({zf.namelist()}) — formato mudou; NÃO é 'sem movimentação'")
    root = ET.fromstring(zf.read(xn[0]))
    alvo = {re.sub(r"\D", "", p): p for p in process_numbers}
    out = []
    for d in root.iter("despacho"):
        pp = d.find("processo-patente")
        numero = pp.findtext("numero") if pp is not None else None
        dig = re.sub(r"\D", "", numero or "")
        if dig in alvo:
            out.append({"processo": alvo[dig], "codigo": d.findtext("codigo"), "titulo": d.findtext("titulo"),
                        "comentario": (d.findtext("comentario") or "").strip()})
    return {"numero": root.get("numero"), "data": root.get("dataPublicacao"), "despachos": out}


def scan_rpi(process_numbers: set[str], desde: int | None = None, max_edicoes: int = 60) -> dict:
    """Lê as edições da RPI ainda não lidas (a partir de rpi_state.json, ou de `desde`), grava os despachos dos
    processos no ledger (fonte RPI, a confirmar pelo operador) e avança o estado. Para na 1ª edição inexistente."""
    from datetime import datetime as _dt
    estado = json.loads(RPI_STATE.read_text(encoding="utf-8")) if RPI_STATE.exists() else {}
    n = desde if desde is not None else int(estado.get("ultima_rpi_lida", RPI_PRIMEIRA - 1)) + 1
    lidas, novos_total, ultima = [], [], estado.get("ultima_rpi_lida")
    for _ in range(max_edicoes):
        ed = fetch_rpi_xml(n, process_numbers)
        if ed is None:
            break
        movs = []
        for a in ed["despachos"]:
            trecho = ("RPI %s — %s — %s" % (ed["numero"], a["titulo"], a["comentario"])).strip(" —")
            movs.append({"processo": a["processo"], "data": _dt.strptime(ed["data"], "%d/%m/%Y").date().isoformat(),
                         "codigo_despacho": a["codigo"], "trecho": trecho[:600], "fonte": "RPI", "rpi": ed["numero"],
                         "lido_por": "monitor — XML oficial " + RPI_XML_URL.format(n=n)})
        rec = record_movements(movs)
        novos_total.extend(rec["novos"])
        lidas.append({"rpi": ed["numero"], "data": ed["data"], "despachos": len(ed["despachos"]), "novos": len(rec["novos"])})
        ultima = int(ed["numero"])
        n += 1
    if ultima is not None:
        estado.update(ultima_rpi_lida=ultima, atualizado_utc=datetime.now(timezone.utc).isoformat(timespec="seconds"),
                      data_da_ultima=(lidas[-1]["data"] if lidas else estado.get("data_da_ultima")))
        STORE.mkdir(parents=True, exist_ok=True)
        tmp = RPI_STATE.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(estado, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(RPI_STATE)
    return {"edicoes_lidas": lidas, "novos": novos_total, "ultima_rpi_lida": ultima,
            "data_da_ultima": estado.get("data_da_ultima")}


def probe_inpi() -> dict:
    """Confirma que o cano até o INPI está aberto (reachability real). NÃO é 'sem movimentação'
    — é só 'o INPI respondeu'. Uma falha aqui é FALHA de rede, reportada como tal."""
    alvos = {"rpi": "https://revistas.inpi.gov.br/rpi/", "busca": "https://busca.inpi.gov.br/pePI/"}
    out = {}
    import urllib.request, urllib.error
    for nome, url in alvos.items():
        try:
            req = urllib.request.Request(url, method="HEAD",
                                         headers={"User-Agent": "IALD-Central-Monitor/1.0"})
            with urllib.request.urlopen(req, timeout=25) as r:
                out[nome] = {"ok": True, "http": r.status}
        except Exception as e:                                  # noqa: BLE001 — reportar qualquer falha
            out[nome] = {"ok": False, "erro": str(e)[:120]}
    return out


def run_now(today: date | None = None) -> dict:
    """O QUE O BOTÃO DA CENTRAL DISPARA. Roda tudo o que dá para rodar HONESTAMENTE agora:
      1. AUDITORIA DE PRAZOS (offline, sempre funciona) — atualiza deadline_audit.json;
      2. REACHABILITY do INPI (real) — o cano está aberto?
      3. tenta extrair despachos ao vivo; captura o resultado OU a falha, sem nunca convertê-la
         em 'sem movimentação'.
    Escreve andamentos/last_run.json com o desfecho honesto. Retorna esse desfecho."""
    today = today or date.today()
    STORE.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")

    # 1. auditoria (sempre)
    rep = audit_deadlines(today)
    AUDIT_OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")

    # 2. reachability
    reach = probe_inpi()
    inpi_up = any(v.get("ok") for v in reach.values())

    # 3. tentativa de despachos ao vivo — honesta
    fetch = {"tentado": True, "novos": 0, "fonte": None, "estado": None, "erro": None}
    procs = processos_vigiados()
    # 3a. RPI pelo XML oficial (a fonte LEGAL). Falha é FALHA, registrada à parte.
    rpi = {"estado": None, "erro": None}
    try:
        sr = scan_rpi(procs)
        feed_compiler_notes(sr["novos"])
        rpi.update(estado="ok", novos=len(sr["novos"]), edicoes_lidas=len(sr["edicoes_lidas"]),
                   ultima_rpi_lida=sr["ultima_rpi_lida"], data_da_ultima=sr["data_da_ultima"],
                   despachos_novos=[{k: m.get(k) for k in ("processo", "data", "codigo_despacho", "rpi")} for m in sr["novos"]])
    except Exception as e:                                      # noqa: BLE001
        rpi.update(estado="FALHA_DE_BUSCA_RPI", erro=str(e)[:200])
    fetch["rpi"] = rpi
    try:
        # a Busca por processo é o caminho alvo (targeted), porém depende de sessão/captcha do
        # portal — deixado explícito; levanta NotImplementedError enquanto não validado ao vivo.
        movimentos = []
        for p in sorted(procs):
            movimentos.extend([{**m, "fonte": "BUSCA", "data": today.isoformat()}
                               for m in [fetch_busca_inpi(p)]])
        rec = record_movements(movimentos)
        feed_compiler_notes(rec["novos"])
        fetch.update(novos=len(rec["novos"]), fonte="BUSCA", estado="ok")
    except NotImplementedError as e:
        fetch.update(estado="adaptador_em_validacao", erro=str(e)[:200])
    except Exception as e:                                      # noqa: BLE001
        fetch.update(estado="FALHA_DE_BUSCA", erro=str(e)[:200])

    r = rep["resumo"]
    result = {
        "iniciado_utc": started, "concluido_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "referencia_hoje": today.isoformat(),
        "auditoria": {"processos": r["processos"],
                      "vencidos_a_conferir": r["prazos_vencidos_a_conferir"],
                      "proximos": r["prazos_proximos"]},
        "inpi_reachability": reach, "inpi_up": inpi_up,
        "despachos": fetch,
        # A LEITURA HONESTA que a UI mostra — nunca 'tudo certo, nada mudou' sem qualificar.
        "leitura": (
            ("INPI respondeu; " if inpi_up else "⚠ INPI NÃO respondeu (falha de rede) — ") +
            (f"RPI (XML oficial) lida até a edição {rpi.get('ultima_rpi_lida')} de {rpi.get('data_da_ultima')}: "
             f"{rpi.get('novos', 0)} despacho(s) novo(s) dos nossos processos; " if rpi["estado"] == "ok"
             else f"⚠ FALHA ao ler a RPI ({rpi.get('erro')}) — isto NÃO significa 'sem movimentação'; ") +
            ("Busca por processo (pePI, sinal não-oficial): adaptador em validação (sessão/captcha do "
             "portal); a AUDITORIA DE PRAZOS rodou e está atualizada." if fetch["estado"] == "adaptador_em_validacao"
             else f"despachos: {fetch['estado']} ({fetch['novos']} novos).")),
        "regua": ("Uma falha de busca é FALHA, jamais 'sem movimentação'. Prazos são [LEGAL] — "
                  "conferir com o agente de PI."),
    }
    (STORE / "last_run.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def fetch_busca_inpi(processo: str) -> dict:
    """SINAL ANTECIPADO (NÃO-OFICIAL): consulta best-effort a Busca do INPI por processo.
    Frágil por natureza (anti-bot/captcha). Falha BARULHENTA. O que vier daqui é sempre
    marcado [NAO-OFICIAL] até confirmar na RPI."""
    # A Busca do INPI usa sessão/captcha; a implementação viável depende do estado do portal
    # no momento da execução na máquina do operador. Deixado como ponto de extensão explícito
    # para NÃO fingir que funciona: levanta, e o chamador registra a falha como falha.
    raise NotImplementedError("Busca INPI: adaptador a validar na máquina do operador "
                              "(sessão/captcha do portal). Sinal [NAO-OFICIAL]; a fonte legal é a RPI.")


# ═══════════════════════════════════════════════════════════════════════════════
#  STORE DE MOVIMENTOS + FEED DO PROMPT COMPILER
# ═══════════════════════════════════════════════════════════════════════════════

def _load_ledger() -> list[dict]:
    if not LEDGER.exists():
        return []
    out = []
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def _movement_id(m: dict) -> str:
    import hashlib
    key = f"{m.get('processo')}|{m.get('fonte')}|{m.get('data')}|{m.get('codigo_despacho')}|{m.get('trecho','')[:80]}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]


def record_movements(new: list[dict]) -> dict:
    """Grava movimentos NOVOS (dedup por id) no ledger append-only. Retorna os que entraram."""
    STORE.mkdir(parents=True, exist_ok=True)
    seen = {m.get("id") for m in _load_ledger()}
    entered = []
    with LEDGER.open("a", encoding="utf-8") as f:
        for m in new:
            m = dict(m)
            m.setdefault("detectado_utc", datetime.now(timezone.utc).isoformat(timespec="seconds"))
            m.setdefault("confirmado_pelo_operador", False)
            m["id"] = _movement_id(m)
            if m["id"] in seen:
                continue
            seen.add(m["id"])
            f.write(json.dumps(m, ensure_ascii=False) + "\n")
            entered.append(m)
    return {"novos": entered, "total_no_ledger": len(seen)}


def feed_compiler_notes(movements: list[dict]) -> Path:
    """Transforma movimentos novos em um bloco Markdown que o Prompt Compiler pode incluir
    no CLAUDE_CODE_TASK.md. Os movimentos entram no MESMO fluxo das notas dos dispositivos."""
    STORE.mkdir(parents=True, exist_ok=True)
    out = STORE / "andamentos_para_o_compiler.md"
    lines = ["## ANDAMENTOS DE PROCESSO — movimentos novos (para confirmação do operador)\n",
             "> Detectados pelo monitor. Fonte legal = RPI. Sinais [NAO-OFICIAL] pedem confirmação na RPI.\n"]
    if not movements:
        lines.append("\n_(nenhum movimento novo desde a última compilação)_\n")
    for m in movements:
        oficial = "RPI (oficial)" if m.get("fonte") == "RPI" else f"{m.get('fonte')} [NAO-OFICIAL]"
        lines.append(f"- **{m.get('processo')}** · {m.get('data','?')} · {oficial} · "
                     f"despacho `{m.get('codigo_despacho') or '—'}` — {m.get('trecho','')[:200]} "
                     f"`[a confirmar]`")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


# ═══════════════════════════════════════════════════════════════════════════════
#  CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Monitor de andamentos de patente (INPI + ePCT) — Central IALD/TGL")
    ap.add_argument("--run", action="store_true", help="O QUE O BOTÃO DISPARA: auditoria + reachability INPI + tenta despachos (honesto)")
    ap.add_argument("--audit", action="store_true", help="auditoria de prazos (offline, roda agora)")
    ap.add_argument("--backfill", action="store_true", help="RPI retroativa (XML oficial) desde a RPI 2864 de 25/11/2025 (rede)")
    ap.add_argument("--check-now", action="store_true", help="RPI da semana + Busca (rede)")
    ap.add_argument("--status", action="store_true", help="mostra o que está no store de movimentos")
    ap.add_argument("--since", default="2025-12-05", help="data inicial do backfill (1º depósito)")
    ap.add_argument("--today", default=None, help="referência de 'hoje' (YYYY-MM-DD) para a auditoria")
    args = ap.parse_args(argv)

    if not any([args.run, args.audit, args.backfill, args.check_now, args.status]):
        ap.print_help()
        return 0

    if args.run:
        res = run_now(_parse_date(args.today) or date.today())
        print(f"[monitor] RUN concluído · INPI up: {res['inpi_up']} · "
              f"despachos: {res['despachos']['estado']} ({res['despachos']['novos']} novos) · "
              f"prazos a conferir: {res['auditoria']['vencidos_a_conferir'] + res['auditoria']['proximos']}")
        print(f"[monitor] {res['leitura']}")
        print(f"[monitor] desfecho salvo em {(STORE / 'last_run.json').relative_to(CENTRAL)}")

    if args.audit:
        today = _parse_date(args.today) or date.today()
        rep = audit_deadlines(today)
        STORE.mkdir(parents=True, exist_ok=True)
        AUDIT_OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
        print_audit(rep)
        print(f"[monitor] auditoria salva em {AUDIT_OUT.relative_to(CENTRAL)}")

    if args.status:
        led = _load_ledger()
        naoconf = [m for m in led if not m.get("confirmado_pelo_operador")]
        print(f"[monitor] store: {len(led)} movimentos no ledger · {len(naoconf)} não confirmados pelo operador")
        for m in led[-12:]:
            print(f"    {m.get('data','?')} {m.get('processo')} [{m.get('fonte')}] "
                  f"{m.get('codigo_despacho') or ''} {'✓' if m.get('confirmado_pelo_operador') else '•novo'}")

    if args.backfill or args.check_now:
        procs = processos_vigiados()
        print(f"[monitor] {'BACKFILL desde a RPI ' + str(RPI_PRIMEIRA) if args.backfill else 'CHECK-NOW'} · {len(procs)} processos")
        # RPI pelo XML oficial (validado ao vivo em 22/09/2026). Backfill relê desde a 1ª edição da família;
        # check-now lê só as edições ainda não lidas (rpi_state.json). O ledger deduplica por id.
        try:
            sr = scan_rpi(procs, desde=RPI_PRIMEIRA if args.backfill else None)
        except Exception as e:                                  # noqa: BLE001
            print(f"[monitor] ⚠ FALHA ao ler a RPI: {e} — isto NÃO significa 'sem movimentação'.")
            return 2
        feed_compiler_notes(sr["novos"])
        print(f"[monitor] RPI lida até a edição {sr['ultima_rpi_lida']} ({sr['data_da_ultima']}); "
              f"{len(sr['edicoes_lidas'])} edição(ões) nesta rodada; {len(sr['novos'])} despacho(s) novo(s).")
        for m in sr["novos"]:
            print(f"    {m['data']} {m['processo']} [RPI {m.get('rpi')}] {m['codigo_despacho']} — {m['trecho'][:120]}")
        print("[monitor] A Busca por processo (pePI) segue sem adaptador; a RPI é a fonte legal. Prazos são [LEGAL].")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
