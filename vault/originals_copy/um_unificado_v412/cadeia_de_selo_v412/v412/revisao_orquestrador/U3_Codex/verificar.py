"""Conferência local da ORDEM 018. Grava somente no retorno próprio."""
import hashlib
import json
import re
from pathlib import Path

here = Path(__file__).resolve().parent
v412 = here.parents[1]
work = v412.parent.parent
source = v412 / "candidatas_c1/REV16/CopiadorEImpostor.lean"
order = Path("C:/IALD/TUNEL_CLAUDE_APP/ORDEM_018_revisao_do_que_a_gerencia_produziu_em_16nov.md")
corpus = work / "cunhagens_13out"
old = v412 / "candidatas_c1/REV15" / source.name

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def write_new(p, value):
    data = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()
    if p.exists():
        if p.read_bytes() != data:
            raise ValueError(f"Preservar evidência anterior: {p.name}")
        return
    with p.open("xb") as f:
        f.write(data)

pins = []
for name, pin in re.findall(r"\x60([^\x60\r\n]+)\x60 \((?:sha16|sha256) \x60([0-9a-f]+)\x60\)", order.read_text(encoding="utf-8-sig")):
    p = Path(name) if Path(name).is_absolute() else corpus / name
    actual = digest(p)
    pins.append(dict(arquivo=str(p), sha256=actual, pino_ordem=pin, coincide=actual.startswith(pin)))
assert len(pins) == 20 and all(x["coincide"] for x in pins), pins
write_new(here.parent / "FONTES_018.json", dict(ordem=str(order), sha256=digest(order), fontes=pins))
local = here / source.name
src = source.read_text(encoding="utf-8-sig")
decl = re.compile(r"^theorem ([\w.]+)", re.M)
lst = decl.findall(src)
previous = set(decl.findall(old.read_text(encoding="utf-8-sig")))
printed = re.findall(r"^#print axioms ([\w.]+)", src, re.M)
logfile = here / "build/CopiadorEImpostor.log"
log = logfile.read_text(encoding="utf-8-sig")
cert = re.findall(r"'TGLExt\.CopiadorEImpostor\.([\w.]+)' (?:does not depend on any axioms|depends on axioms:\s*\[([^\]]*)\])", log)
ax = sorted({a.strip() for _, items in cert for a in items.split(",") if a.strip()})
assert digest(source) == digest(local) and "RC: 0" in log
assert sorted(lst) == sorted(printed) == sorted(n for n,_ in cert) and len(set(lst)) == 118
assert ax == ["Classical.choice", "Quot.sound", "propext"] and not re.search(r"(?:warning:|error:|sorryAx)", log, re.I)
corpus_files = sorted(corpus.glob("OPERADOR_*.txt"))
quotes = []
for i, line in enumerate(src.splitlines(), 1):
    for m in re.finditer(r"«([^»]+)»", line):
        quotes.append(dict(linha=i, literal=m[1].encode(), fontes=[]))
for p in corpus_files:
    raw = p.read_bytes()
    for q in quotes:
        if q["literal"] in raw:
            for row, line in enumerate(raw.splitlines(), 1):
                if q["literal"] in line:
                    q["fontes"].append(dict(arquivo=p.name, linha=row, sha256=hashlib.sha256(raw).hexdigest()))
for q in quotes:
    q["literal_sha256"] = hashlib.sha256(q.pop("literal")).hexdigest()
assert len(quotes) == src.count("«") == src.count("»")
result = dict(fonte=str(source),sha256=digest(source),anterior_sha256=digest(old),log_sha256=digest(logfile),script_compilacao_sha256=digest(here / "compilar_candidata.ps1"),objeto_sha256=digest(here / "build/CopiadorEImpostor.olean"),lean=log.splitlines()[2],rc=0,teoremas=len(lst),teoremas_na_anterior=len(previous),novos=[n for n in lst if n not in previous],retirados=sorted(previous-set(lst)),sem_axiomas=sum(not x for _,x in cert),axiomas_encontrados=ax,avisos=0,arquivos_de_fala_consultados=len(corpus_files),citacoes_em_uma_linha=quotes,sem_correspondencia=[q["linha"] for q in quotes if not q["fontes"]])
write_new(here / "CONFERENCIA.json",result)
print(len(pins),len(lst),len(printed),len(cert),len(result["novos"]),result["retirados"],result["sem_axiomas"],len(quotes),result["sem_correspondencia"])

