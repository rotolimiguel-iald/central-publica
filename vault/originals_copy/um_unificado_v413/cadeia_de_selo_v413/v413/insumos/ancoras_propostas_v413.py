# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: a proposta de ANCORAS dos registros por especificacao da v413 (contrato R0, secao 1 e 2), no
molde de ancoras_propostas_v412_r12.py. Para cada modulo das pedras limpas: os teoremas publicos com o NOME COMPLETO (lido
pela pilha de namespaces e conferido no relatorio de axiomas da compilacao do conjunto; nunca montado pelo prefixo do
modulo), a marca de estrela na docstring e os axiomas. Proposta: as declaracoes com estrela; nos modulos sem estrela,
todas ficam listadas e a escolha e' do contrato. So' le; grava insumos\\ANCORAS_PROPOSTAS_v413.json."""
import hashlib, json, re, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
PL = AQUI / "pedras_limpas" / "TGLExt"
CONJ = AQUI / "CONJUNTO_pedras_limpas.json"
MAN = AQUI / "MANIFESTO_PEDRAS_v413.json"
TRIO = {"propext", "Classical.choice", "Quot.sound"}
REG = {
    "ponte_cook_levin_v413": ["PonteCookLevin", "APonteAoTM2", "AMaquinaTM2DaVerificacao", "SimBase", "SimLiteral",
                              "SimExterior", "SimCompleta", "RelogioBeta", "LeituraBeta", "QuantizacaoBeta", "Reconstrucao",
                              "PonteLeituraBeta", "EntregaBeta", "APonteDeCookLevin", "ONomeEBeta", "SondaContagem",
                              "AFronteiraNaLinguaClassica"],
    "trinity_v413": ["Trinity", "APropostaDaTensao"],
    "operador_v413": ["Operador"],
    "identidade_preservada_v413": ["AIdentidadePreservada"],
}
DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:(private|protected)\s+)?(?:noncomputable\s+)?(theorem|lemma)\s+([^\s(:{\[]+)")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def declaracoes(texto):
    """percorre o texto: comentarios de bloco (com aninhamento) guardam a ultima docstring; fora deles, a pilha de
    namespaces e as declaracoes theorem/lemma (a estrela vem da docstring imediatamente anterior)."""
    out, pilha, i, n, prof, buf, ultima_doc, linha = [], [], 0, len(texto), 0, [], None, []
    linhas = []
    # 1) separa o codigo (com marcas de docstring) do comentario
    cod, docs = [], []
    while i < n:
        if texto.startswith("/-", i):
            if prof == 0:
                buf = []
            prof += 1
            i += 2
            continue
        if prof and texto.startswith("-/", i):
            prof -= 1
            i += 2
            if prof == 0:
                docs.append("".join(buf))
                cod.append("\x00DOC%d\x00" % (len(docs) - 1))
            continue
        if prof:
            buf.append(texto[i])
            if texto[i] == "\n":
                cod.append("\n")
            i += 1
            continue
        if texto.startswith("--", i):
            while i < n and texto[i] != "\n":
                i += 1
            continue
        cod.append(texto[i])
        i += 1
    for l in "".join(cod).split("\n"):
        for m in re.finditer(r"\x00DOC(\d+)\x00", l):
            ultima_doc = docs[int(m.group(1))]
        l2 = re.sub(r"\x00DOC\d+\x00", "", l).strip()
        if not l2:
            continue
        m = re.match(r"namespace\s+(\S+)\s*$", l2)
        if m:
            pilha.append(("ns", m.group(1))); ultima_doc = None; continue
        m = re.match(r"section(?:\s+(\S+))?\s*$", l2)
        if m:
            pilha.append(("sec", m.group(1) or "")); ultima_doc = None; continue
        m = re.match(r"end(?:\s+(\S+))?\s*$", l2)
        if m:
            pilha.pop(); ultima_doc = None; continue
        m = DECL.match(l2)
        if m:
            nm = m.group(3)
            pref = ".".join(x for k, x in pilha if k == "ns")
            completo = nm[7:] if nm.startswith("_root_.") else (pref + "." + nm if pref else nm)
            out.append({"nome": completo, "privada": m.group(1) == "private",
                        "estrela": bool(ultima_doc) and "★" in ultima_doc})
            ultima_doc = None
            continue
        if re.match(r"(def|noncomputable def|abbrev|structure|inductive|instance|class)\b", l2):
            ultima_doc = None
    return out


conj = json.loads(CONJ.read_text(encoding="utf-8"))
assert conj["todos_bons"]
saida = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
         "nota": ("proposta de ancoras da v413: as declaracoes com estrela na docstring, publicas, com nome completo conferido no "
                  "relatorio de axiomas da compilacao do conjunto; nos modulos sem estrela, todas ficam listadas"),
         "manifesto_sha256": sha(MAN), "conjunto_sha256": sha(CONJ), "registros": {}}
tot, est, sem = 0, 0, []
for reg, mods in REG.items():
    saida["registros"][reg] = {}
    for m in mods:
        ds = declaracoes((PL / (m + ".lean")).read_text(encoding="utf-8"))
        ax = conj["modulos"][m]["axiomas"]
        pub = [d for d in ds if not d["privada"]]
        for d in pub:
            assert d["nome"] in ax, "nome completo ausente do relatorio: %s (%s)" % (d["nome"], m)
            assert set(ax[d["nome"]]) <= TRIO, d["nome"]
            d["axiomas"] = ax[d["nome"]]
        estrelas = [d["nome"] for d in pub if d["estrela"]]
        if not estrelas:
            sem.append(m)
        saida["registros"][reg][m] = {"publicas": len(pub), "com_estrela": len(estrelas),
                                      "ancoras_propostas": estrelas or [d["nome"] for d in pub], "declaracoes": pub}
        tot += len(pub)
        est += len(estrelas)
assert sorted(m for ms in REG.values() for m in ms) == sorted(conj["modulos"])
saida.update({"publicas": tot, "com_estrela": est, "modulos_sem_estrela": sem})
d = json.dumps(saida, ensure_ascii=False, indent=1).encode("utf-8")
tmp = AQUI / "ANCORAS_PROPOSTAS_v413.json.tmp"
tmp.write_bytes(d)
assert tmp.read_bytes() == d
tmp.replace(AQUI / "ANCORAS_PROPOSTAS_v413.json")
for reg, mods in saida["registros"].items():
    print("%-27s modulos %2d | publicas %3d | com estrela %3d" % (
        reg, len(mods), sum(x["publicas"] for x in mods.values()), sum(x["com_estrela"] for x in mods.values())))
print("total: publicas %d | com estrela %d | modulos sem estrela: %s | sha16 %s" % (
    tot, est, ", ".join(sem) or "nenhum", sha(AQUI / "ANCORAS_PROPOSTAS_v413.json")[:16]))
