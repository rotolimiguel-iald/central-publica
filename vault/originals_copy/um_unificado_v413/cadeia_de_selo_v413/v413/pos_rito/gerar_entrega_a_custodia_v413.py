# -*- coding: utf-8 -*-
"""gerar_entrega_a_custodia_v413.py -- (Etapa 3 da v413, 20/11/2026) grava, POR ULTIMO, o ENTREGA_A_CUSTODIA_v413.json pelo modelo da custodia
(work\\custodia_v413_preparo_20nov\\ENTREGA_A_CUSTODIA_v413.MODELO.json, esquema entrega_a_custodia/1), com tudo LIDO na hora: os tres sha256 do Nos
(o um.py, o selo, o handoff), os recibos do B(n) pela funcao da G1 (fatos.recibos_bn_resolvidos) e o pino conjunto deles, o recibo da guarda privada (as
fases pre e pos desta pasta) com o numero de termos novos, o canal do app (o padrao do modelo: o quadro) e as decisoes do operador passadas por
--decisao <ID> <fala por bytes> "<o que decide>" (uma ou mais; cada uma com o sha256 lido da fala). ATO DA GERENCIA: so' depois das tres marcas, do
B(n) e das superficies; o vigia da custodia so' dispara com custodia_pode_comecar=true e os tres sha256 iguais aos do disco.
Recusa: sem o handoff, o selo v413 ou o um.py pinado; com o conferidor que nao bateu; com a guarda do titulo reprovando; com termo privado novo sem a
decisao TERMO_PRIVADO_ISENTO_v413 na lista; com o B(n) sem os tres recibos e sem a decisao BN_DISPENSADO_v413 na lista. Escrita por temporario e troca
atomica. --ensaio: grava em etapa3\\ensaio_entrega\\ (nunca no lugar que o vigia le) e nao exige o Nos na v413 (le o que houver; so' o esquema conta)."""
import hashlib, json, os, re, subprocess, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
CEN = Path(r"C:\IALD\Central de Patentes"); sys.path.insert(0, str(CEN / "tools"))
from custodia_g1 import fatos as FG  # noqa: E402
from custodia_g1.caminhos import Caminhos  # noqa: E402
P = Path(__file__).resolve().parent; V = P.parent; NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"); ENSAIO = "--ensaio" in sys.argv
MOD = CEN / "work" / "custodia_v413_preparo_20nov" / "ENTREGA_A_CUSTODIA_v413.MODELO.json"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
lj = lambda p: json.loads(Path(p).read_text(encoding="utf-8"))
modelo = lj(MOD); assert modelo["esquema"] == "entrega_a_custodia/1" and modelo["versao"] == "v413"
dec = []; a = sys.argv
for i, x in enumerate(a):
    if x == "--decisao":
        idd, fala, oq = a[i + 1], a[i + 2], a[i + 3]
        assert Path(fala).is_file() and len(oq) >= 10, ("decisao sem a fala por bytes ou sem o que decide", idd)
        dec.append({"id": idd, "fala": str(Path(fala)), "fala_sha256": sha(fala), "o_que_decide": oq, "conteudo": {}})
ids = {d["id"] for d in dec}
# AO LADO (21/11/2026, gerencia c1): na isencao de termo privado, o conteudo leva a PROPOSTA conferida dos nomes exatos (isencao_trinity_v413.py:
# >= 12 caracteres, a regra da G1; verificada com a contagem da G1 sobre os pares da fase pos). So' entra se a proposta for limpa e citar a MESMA fala.
_PROP = V / "ISENCAO_TRINITY_PROPOSTA_v413.json"
for d_ in dec:
    if d_["id"] == "TERMO_PRIVADO_ISENTO_v413" and _PROP.is_file():
        _p = lj(_PROP)
        assert _p["verificacao"]["limpa"] is True and not _p["verificacao"]["barrados_com_isencao"], "a proposta de isencao nao e' limpa"
        assert _p["fala_do_operador"]["sha256"] == d_["fala_sha256"], "a proposta de isencao cita outra fala"
        assert _p["nomes_exatos"] and all(isinstance(s, str) and len(s) >= 12 for s in _p["nomes_exatos"]), "nome curto na proposta"
        d_["conteudo"] = {"nomes_exatos": _p["nomes_exatos"], "proposta": {"arquivo": str(_PROP), "sha256": sha(_PROP)},
                          "verificacao": {"pares": _p["verificacao"]["pares"], "barrados_com_isencao": [], "limpa": True},
                          "pergunta_da_gerencia": _p["pergunta_da_gerencia"], "regra_da_g1": _p["regra_da_g1"],
                          "alcance": "so' a v413 e so' estes textos literais; qualquer outro casamento do marcador 28 ou de outro marcador segue parando a custodia"}
# AO LADO (21/11/2026, gerencia c1): --pendente <ID> "<pergunta ao autor>" declara uma decisao do autor que NAO vem nesta entrega. Pelo handoff da
# custodia (secao 2.5) a decisao que nao vem para no passo dela; a guarda da custodia NAO afrouxa. So' a isencao de termo privado pode ser pendente; a
# pendencia vai ao campo nota (nunca a decisoes_do_operador, de onde a custodia grava arquivos de decisao). Sem --pendente, a recusa e' a de antes.
pend = []
for i, x in enumerate(a):
    if x == "--pendente":
        idd, perg = a[i + 1], a[i + 2]
        assert idd == "TERMO_PRIVADO_ISENTO_v413" and len(perg) >= 20 and idd not in ids, ("pendencia invalida", idd)
        pend.append({"id": idd, "pergunta": perg})
pids = {p_["id"] for p_ in pend}
um, selo_p, ho = NOS / "um.py", NOS / "um_absoluto_selo.json", NOS / "HANDOFF_v413_CUSTODIA.md"
falhas = []
selo = lj(selo_p)
if not ENSAIO:
    ESP = lj(V / "ESPERADOS_v413.json"); CF = lj(V / "CONFERENCIA_POS_RITO_v413_FOCO.json")
    if not ho.is_file():
        falhas.append("sem o HANDOFF_v413_CUSTODIA.md (o compositor grava por ultimo)")
    if selo.get("um_version") != "v413" or selo["sha256"]["um.py"] != sha(um) or sha(um)[:16] != ESP["candidato_sha16"]:
        falhas.append("o selo nao e' v413 ou o um.py nao e' o pinado")
    if CF.get("ok") is not True:
        falhas.append("o conferidor da v413 nao bateu")
    r = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", str(P / "guarda_titulo_versao_v413.py"), "v413"], capture_output=True, text=True, encoding="utf-8", errors="replace", stdin=subprocess.DEVNULL)
    if r.returncode != 0:
        falhas.append("a guarda do titulo reprovou")
gp = {f: lj(V / ("GUARDA_PRIVADA_v413_%s.json" % f)) for f in ("pre", "pos") if (V / ("GUARDA_PRIVADA_v413_%s.json" % f)).is_file()}
termos = int(gp["pos" if "pos" in gp else "pre"].get("termos_novos", 0)) if gp else 0   # AO LADO 21/11: a fase mais nova, sem somar pre e pos
if not gp and not ENSAIO:
    falhas.append("sem o recibo da guarda privada (GUARDA_PRIVADA_v413_pre.json / _pos.json)")
if termos and "TERMO_PRIVADO_ISENTO_v413" not in ids and "TERMO_PRIVADO_ISENTO_v413" not in pids:
    falhas.append("termo privado novo (%d) sem a decisao TERMO_PRIVADO_ISENTO_v413 do autor na lista (nem declarada pendente)" % termos)
c = Caminhos({}); res, prob = FG.recibos_bn_resolvidos(c, "v413")
rec = {p_: res[p_]["caminho"] if p_ in res else None for p_ in ("aplicacao", "parada", "religamento")}
estado = "APLICADA_E_RELIGADA" if all(rec.values()) else ("APLICADA_RELIGAMENTO_PENDENTE" if rec["aplicacao"] and rec["parada"] else "NAO_FEITA")
if estado != "APLICADA_E_RELIGADA" and "BN_DISPENSADO_v413" not in ids and not ENSAIO:
    falhas.append("o B(n) da v413 esta' %s e nao ha a decisao BN_DISPENSADO_v413 do autor na lista" % estado)
pinos = sorted(p_ for p_ in V.rglob("PINO_RECIBOS_*_v413.json") if ".bak_" not in p_.name)
ent = {"esquema": modelo["esquema"], "versao": "v413", "custodia_pode_comecar": not falhas and not ENSAIO, "quem": "claude-c1", "quando": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
       "nos": {"um_py_sha256": sha(um), "selo_sha256": sha(selo_p), "handoff_sha256": sha(ho) if ho.is_file() else None},
       "bancada": {"estado": estado, "recibos": rec, "pino_recibos": str(pinos[0]) if len(pinos) == 1 else None,
                   "nota": "" if estado == "APLICADA_E_RELIGADA" else ("recibos ausentes: %s" % "; ".join(prob))},
       "guarda_privada": {"recibo": str(V / "GUARDA_PRIVADA_v413_pos.json") if "pos" in gp else (str(V / "GUARDA_PRIVADA_v413_pre.json") if "pre" in gp else None),
                          "recibos": {f: str(V / ("GUARDA_PRIVADA_v413_%s.json" % f)) for f in gp}, "termos_novos": termos},
       "app": {"canal": {"tipo": "quadro", "thread": None, "unidade": None}},
       "decisoes_do_operador": dec,
       "nota": "gerado por pos_rito\\gerar_entrega_a_custodia_v413.py; tudo lido na hora" + (" | ENSAIO: nao e' a entrega" if ENSAIO else "")
               + "".join(" | PENDENTE DO AUTOR (nao vem nesta entrega; pelo handoff da custodia, secao 2.5, para no passo dela): %s: %s" % (p_["id"], p_["pergunta"]) for p_ in pend)}
if falhas and not ENSAIO:
    print("RECUSO a entrega (nada gravado):"); [print("  -", f) for f in falhas]; sys.exit(1)
dest = (V / "etapa3" / "ensaio_entrega") if ENSAIO else V
dest.mkdir(parents=True, exist_ok=True); out = dest / ("ENTREGA_A_CUSTODIA_v413%s.json" % ("_ENSAIO" if ENSAIO else ""))
if out.exists():
    out.with_name(out.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(out.read_bytes())
b = json.dumps(ent, ensure_ascii=False, indent=1).encode("utf-8"); tmp = out.with_name(out.name + ".tmp"); tmp.write_bytes(b); assert tmp.stat().st_size == len(b); os.replace(tmp, out)
assert set(ent) == set(modelo) and set(ent["nos"]) == set(modelo["nos"]) and set(ent["bancada"]) <= set(modelo["bancada"]) | {"nota"}, "a entrega saiu fora do esquema do modelo"
print("%s gravado | custodia_pode_comecar=%s | B(n) %s | termos privados novos %d | decisoes %d | pendentes do autor %d | falhas no ensaio: %s" % (out, ent["custodia_pode_comecar"], estado, termos, len(dec), len(pend), falhas if ENSAIO else "-"))
