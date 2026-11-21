# -*- coding: utf-8 -*-
# [DERIVADO v413, claude-construtor-v413 (Etapa 1, 20/11/2026)] copia de C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\preparar_bundle_v412.py; trocas de texto exato com contagem registrada em DERIVACAO_ETAPA1_v413.json (derivador: derivar_scripts_etapa1_v413.py) e subida dos rotulos de versao (v412->v413, v411->v412); o molde fica intacto.
"""preparar_bundle_v413.py -- v413, Etapa 1, item 2 (claude-construtor-v413, 20/11/2026, a servico da gerencia c1; derivado de v412\\preparar_bundle_v412.py): instala no sandbox
C:\\t\\k413c\\final, em TGLExt\\, os modulos novos da v413 a partir das pedras limpas (insumos\\pedras_limpas\\TGLExt\\, ja na forma do kernel: imports TGLExt.<Nome>, fim de linha LF) e do
manifesto insumos\\MANIFESTO_PEDRAS_v413.json (gerados pela gerencia; nunca editados aqui), e troca o modulo que a v413 corrige so' no texto (campo kernel_corrigido do manifesto; recibo
insumos\\kernel_edits\\ERRATA_<Nome>.json), com o arquivo antigo do sandbox guardado na quarentena antes da troca.

O que faz, para cada modulo novo (tudo conferido, nada digitado):
  1. CONFERE o sha256 e os bytes da pedra limpa contra o manifesto (fail-closed: um so' diferente aborta tudo, nada e' gravado);
  2. a UNICA mudanca permitida no texto (ordem da Etapa 1 da v413, item 2): as linhas `#print axioms` SAEM do corpo instalado (a linha inteira; as ancoras sao LIDAS delas antes, com a pilha
     de namespace da linha, para o pos_build conferir no Audit) e o fim do arquivo fica com UMA quebra de linha (rstrip + "\\n", como na v412). Os imports ja vem como TGLExt.<Nome>: nenhuma linha
     de import se troca (import SOLTO de modulo irmao PARA o preparo). Nenhuma prova e' tocada. As fontes ja sao LF (se houvesse CR, o script PARA);
  3. confere por RECONSTRUCAO independente que o instalado == insumo menos as linhas `#print axioms`; grava o diff unificado e os dois sha256 em kernel\\bundle\\;
  4. confere que todo import TGLExt.*/TGL.* existe no kernel do Nos v412 ou no proprio bundle, e todo import Mathlib.* existe na mathlib do sandbox; que os imports de modulo irmao sao os do
     manifesto (imports_tglext); que nenhuma linha `#print axioms` estava dentro de comentario; que nao ha `sorry`, `#eval`, `#print` nem `axiom` no CODIGO (comentarios e cadeias mascarados);
e, para o modulo corrigido: confere a fonte (sha256_saida do manifesto == o do recibo da correcao), que a fonte de origem (sha256_origem) e' a do Nos e a do sandbox (ou que o sandbox ja tem a
corrigida, se o preparo rodou antes), que o CODIGO e' identico ao da origem (comentarios fora, cadeias dentro) e que nao ha linha `#print axioms` (o instalado == o insumo); grava o diff contra a
origem e lista quem depende dele no kernel (pelo grafo de imports do sandbox: os modulos novos e os antigos que o lake vai recompilar).
Grava, na ordem TOPOLOGICA das dependencias (desempate: a ordem_topologica_sugerida do manifesto): pedra\\origem\\<Nome>.lean (os bytes do insumo), pedra\\<Nome>.lean (o instalado), o sandbox
TGLExt\\<Nome>.lean; a raiz TGLExt.lean do sandbox = a do Nos v412 + um import por modulo novo (na ordem topologica); kernel_modulos_novos_v413.json, BUNDLE_v413.json,
kernel\\bundle\\SHA256_POR_MODULO_v413.json, kernel\\ULTIMA_INSTALACAO_v413.json e o construir_kernel_v413.sh (build POR MODULO: o corrigido primeiro, depois os novos na ordem topologica,
parando no primeiro que nao compilar; depois o build inteiro e o Audit).

TROCAR UMA FONTE (a leitura de terceiro pode mudar docstrings; a gerencia regera o manifesto): rodar `reconstruir_kernel_v413.py --manifesto <json> --pedras <pasta>` (este preparo + o build +
o pos_build). O preparo e' idempotente: so' o que mudou e' regravado (o arquivo antigo do sandbox vai para C:\\t\\k413c\\quarentena_<data>, conferido), e o lake recompila so' o modulo trocado e
os que dependem dele (mais a raiz e o Audit). O que mudou e quem depende dele fica em kernel\\ULTIMA_INSTALACAO_v413.json.
Nada toca o Nos (so' leitura). Uso: C:\\Python314\\python.exe -B -X utf8 preparar_bundle_v413.py [--seco] [--manifesto <json>] [--pedras <pasta>] [--kernel-edits <pasta>]"""
import datetime
import difflib
import hashlib
import json
import os
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.dont_write_bytecode = True
PK = Path(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, str(PK))
import lean_texto_v413 as LT  # noqa: E402

SECO = "--seco" in sys.argv
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
arg = lambda k, d: Path(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
MAN_P = arg("--manifesto", PK / "insumos" / "MANIFESTO_PEDRAS_v413.json")
PED = arg("--pedras", PK / "insumos" / "pedras_limpas" / "TGLExt")
KED = arg("--kernel-edits", None)   # (padrao: a pasta do campo saida de cada modulo corrigido no manifesto)
K13 = Path("C:/t/k413c/final")
QUAR = Path("C:/t/k413c") / ("quarentena_" + TS)
NOS = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel")
MATHLIB = K13 / ".lake" / "packages" / "mathlib"
KD = PK / "kernel"; BD = KD / "bundle"
sha = lambda b: hashlib.sha256(b).hexdigest()
RX_PRINT = re.compile(r"^#print axioms (\S+)[ \t]*\n?", re.M)
RX_IMPORT = re.compile(r"^import (\S+)[ \t]*$", re.M)

MAN = json.loads(MAN_P.read_text(encoding="utf-8"))
assert all(k_.startswith("TGLExt.") and k_.count(".") == 1 for k_ in MAN["modulos_novos"]), "modulo novo fora da forma TGLExt.<Nome>"
MODS = [dict(v_, modulo=k_.split(".", 1)[1], modulo_completo=k_) for k_, v_ in MAN["modulos_novos"].items()]
NOMES = [m["modulo"] for m in MODS]
assert len(NOMES) == len(set(NOMES)) == int(MAN["n_modulos_novos"]), ("o manifesto nao tem n_modulos_novos nomes distintos", len(NOMES), MAN["n_modulos_novos"])
assert sum(int(m["teoremas_publicos"]) for m in MODS) == int(MAN["teoremas_publicos_novos"]), "a soma de teoremas_publicos nao e' a teoremas_publicos_novos do manifesto"
assert all(set(m["imports_tglext"]) <= set(NOMES) for m in MODS), "imports_tglext do manifesto que nao e' modulo novo"
SUG_NOMES = [x.split(".", 1)[1] for x in MAN["ordem_topologica_sugerida"]]
assert sorted(SUG_NOMES) == sorted(NOMES), "a ordem_topologica_sugerida do manifesto nao tem exatamente os modulos novos"
KC = MAN.get("kernel_corrigido") or {}
assert all(k_.startswith("TGLExt.") and k_.count(".") == 1 and k_.split(".", 1)[1] not in NOMES for k_ in KC), "modulo corrigido fora da forma TGLExt.<Nome> ou repetido entre os novos"
selo = json.loads((NOS.parent / "um_absoluto_selo.json").read_text(encoding="utf-8"))
assert selo.get("um_version") == "v412", ("o Nos nao e' a v412 selada", selo.get("um_version"))

# ---------------------------------------------------------------- 1. o sha256 de TODAS as copias congeladas (fail-closed antes de gravar qualquer coisa)
bytes_de = {}
ruins = []
for m in MODS:
    p = PED / (m["modulo"] + ".lean")
    b = p.read_bytes()
    if sha(b) != m["sha256_pedra_limpa"] or len(b) != int(m["bytes"]):
        ruins.append([m["modulo"], sha(b)[:16], m["sha256_pedra_limpa"][:16]])
    bytes_de[m["modulo"]] = b
# o modulo corrigido so' no texto: a fonte corrigida (sha256_saida), o recibo da correcao (os mesmos sha256 de origem e de saida; codigo identico) e a fonte de origem no Nos
kc_bytes = {}; kc_rec = {}
for k_, v_ in KC.items():
    nome_ = k_.split(".", 1)[1]
    ked_ = KED if KED else Path(v_["saida"]).parent
    p_ = ked_ / (nome_ + ".lean"); rp_ = ked_.parent / ("ERRATA_%s.json" % nome_)
    b_ = p_.read_bytes(); rec_ = json.loads(rp_.read_text(encoding="utf-8"))
    nos_ = (NOS / "TGLExt" / (nome_ + ".lean")).read_bytes()
    if not (sha(b_) == v_["sha256_saida"] == rec_["sha256_saida"] and v_["sha256_origem"] == rec_["sha256_origem"] == sha(nos_)
            and v_.get("codigo_identico") is True and rec_.get("codigo_identico") is True):
        ruins.append([k_, sha(b_)[:16], v_["sha256_saida"][:16], str(rec_.get("sha256_saida"))[:16], v_["sha256_origem"][:16], sha(nos_)[:16]])
    kc_bytes[nome_] = b_
    kc_rec[nome_] = {"fonte": str(p_), "recibo": str(rp_), "recibo_sha256": sha(rp_.read_bytes()), "nos_bytes": nos_, "manifesto": v_}
assert not ruins, ("pedra limpa (ou fonte corrigida) com sha256/bytes diferente do manifesto ou do recibo da correcao: NADA foi gravado", ruins)

# ---------------------------------------------------------------- 2-4. a transformacao, conferida
deps = {}
saida = {}
entradas = {}
for m in MODS:
    n = m["modulo"]; b = bytes_de[n]; t = b.decode("utf-8")
    assert "\r" not in t, ("CR na fonte: a normalizacao de fim de linha nao esta entre as mudancas permitidas; PARE e pergunte a gerencia", n)
    msk = LT.mascara_comentarios(t)
    assert len(msk) == len(t)
    linhas, mlinhas = t.split("\n"), msk.split("\n")
    pilhas = LT.pilha_de_namespace_por_linha(t)
    # as linhas #print axioms: todas fora de comentario (o texto mascarado mantem a linha)
    i_print = [i for i, l in enumerate(linhas) if re.match(r"^#print axioms \S+[ \t]*$", l)]
    i_print_cod = [i for i, l in enumerate(mlinhas) if re.match(r"^#print axioms \S+[ \t]*$", l)]
    assert i_print == i_print_cod, ("linha `#print axioms` dentro de comentario ou cadeia (nao sai do texto do comentario)", n, sorted(set(i_print) ^ set(i_print_cod))[:5])
    # (v413: o manifesto nao traz a contagem das linhas #print axioms; ela e' MEDIDA aqui e registrada no BUNDLE)
    ancoras = []
    for i in i_print:
        nome = re.match(r"^#print axioms (\S+)", linhas[i]).group(1)
        ancoras.append({"texto": nome, "namespace": ".".join(pilhas[i]), "linha": i + 1})
    # os imports (so' em codigo)
    imp_cod = [(i, re.match(r"^import (\S+)[ \t]*$", l).group(1)) for i, l in enumerate(mlinhas) if re.match(r"^import (\S+)[ \t]*$", l)]
    imp_txt = [(i, re.match(r"^import (\S+)[ \t]*$", l).group(1)) for i, l in enumerate(linhas) if re.match(r"^import (\S+)[ \t]*$", l)]
    assert imp_cod == imp_txt, ("linha import dentro de comentario", n)
    soltos = [x for _, x in imp_txt if x in NOMES]
    assert not soltos, ("import SOLTO de modulo irmao: a fonte nao esta na forma do kernel (import TGLExt.<Nome>); PARE e pergunte a gerencia", n, soltos)
    trocar = {}   # (v413: as pedras limpas ja vem com import TGLExt.<Nome>; nenhuma linha de import se troca)
    irmaos = sorted({x[len("TGLExt."):] for _, x in imp_txt if x.startswith("TGLExt.") and x[len("TGLExt."):] in NOMES})
    assert irmaos == sorted(m["imports_tglext"]), ("os imports de modulo irmao da fonte nao sao os do manifesto (imports_tglext)", n, irmaos, m["imports_tglext"])
    deps[n] = irmaos
    # a transformacao (as duas unicas mudancas)
    novas = []
    for i, l in enumerate(linhas):
        if i in set(i_print):
            continue
        novas.append(("import TGLExt.%s" % trocar[i]) if i in trocar else l)
    out_t = "\n".join(novas).rstrip("\n") + "\n"
    # RECONSTRUCAO independente: o RX das linhas #print axioms (o do molde da IALD2, v410, e o da v412) sobre o texto inteiro; a troca de import por expressao regular fica (na v413 nao troca nada)
    rec = RX_PRINT.sub("", t)
    rec = RX_IMPORT.sub(lambda mm: ("import TGLExt." + mm.group(1)) if mm.group(1) in NOMES else mm.group(0), rec).rstrip("\n") + "\n"
    assert rec == out_t, ("a reconstrucao independente difere da transformacao", n)
    # o diff: so' linhas `#print axioms` removidas, imports trocados e o fim de arquivo
    dif = list(difflib.unified_diff(t.splitlines(True), out_t.splitlines(True), fromfile="insumos/pedras_limpas/TGLExt/%s.lean" % n, tofile="C:/t/k413c/final/TGLExt/%s.lean" % n, n=0))
    menos = [l[1:].rstrip("\n") for l in dif if l.startswith("-") and not l.startswith("---")]
    mais = [l[1:].rstrip("\n") for l in dif if l.startswith("+") and not l.startswith("+++")]
    assert all(re.match(r"^#print axioms \S+[ \t]*$", l) or re.match(r"^import \S+$", l) or l.strip() == "" for l in menos), ("linha removida que nao e' #print axioms/import/branco", n, [l for l in menos if not (l.startswith("#print axioms") or l.startswith("import "))][:3])
    # (o difflib pode alinhar um bloco de linhas em branco entre grupos de #print axioms como "-branco ... +branco": artefato de alinhamento; a prova de que nada mais mudou
    #  e' a reconstrucao independente acima; aqui so' se aceita, alem dos imports trocados, linha em branco)
    assert all(re.match(r"^import TGLExt\.\S+$", l) or l.strip() == "" for l in mais), ("linha acrescentada que nao e' import TGLExt.* nem branco", n, mais[:3])
    assert sum(1 for l in out_t.split("\n") if not l.strip()) <= sum(1 for l in t.split("\n") if not l.strip()), ("mais linhas em branco no instalado que no insumo", n)
    assert sum(1 for l in mais if l.startswith("import TGLExt.")) == len(trocar)
    # o codigo instalado: sem sorry/#eval/#print/axiom; imports existentes
    cod = LT.mascara_comentarios(out_t)
    assert not re.search(r"\bsorry\b", cod), ("sorry no codigo", n)
    assert "#print" not in cod and "#eval" not in cod, ("#print/#eval no codigo instalado", n)
    assert not re.search(r"^\s*axiom\s", cod, re.M), ("declaracao axiom no codigo", n)
    for imp in RX_IMPORT.findall(out_t):
        if imp.startswith("TGLExt.") and imp[len("TGLExt."):] in NOMES:
            continue
        if imp.startswith(("TGLExt.", "TGL.")) or imp in ("TGLExt", "TGL"):
            assert (NOS / (imp.replace(".", "/") + ".lean")).exists(), ("import ausente do kernel do Nos v412", n, imp)
        elif imp.startswith("Mathlib"):
            assert (MATHLIB / (imp.replace(".", "/") + ".lean")).exists(), ("import Mathlib ausente da mathlib do sandbox", n, imp)
        else:
            raise AssertionError(("import de origem desconhecida", n, imp))
    assert not (NOS / "TGLExt" / (n + ".lean")).exists(), ("o modulo ja existe no Nos", n)
    saida[n] = out_t.encode("utf-8")
    nss = sorted({re.match(r"^namespace\s+(\S+)", l.strip()).group(1) for l in mlinhas if re.match(r"^namespace\s+(\S+)", l.strip())})
    entradas[n] = {"modulo": n, "modulo_completo": m["modulo_completo"], "rel": "TGLExt/%s.lean" % n, "autor_da_construcao": m.get("autor_da_construcao"),
                   "fonte_revisada": m.get("fonte_revisada"), "sha256_fonte_revisada": m.get("sha256_fonte_revisada"), "sha256_origem": m.get("sha256_origem"),
                   "codigo_identico_a_origem_no_manifesto": m.get("codigo_identico_a_origem"), "pedra_limpa_no_manifesto": m.get("pedra_limpa"),
                   "insumo": str(PED / (n + ".lean")), "sha256_insumo": sha(b), "sha16_insumo": sha(b)[:16], "bytes_insumo": len(b),
                   "sha256": sha(saida[n]), "sha16": sha(saida[n])[:16], "bytes": len(saida[n]),
                   "imports": RX_IMPORT.findall(out_t), "imports_trocados": [],
                   "dependencias_no_bundle": deps[n], "n_print_axioms_removidos": len(i_print), "ancoras": ancoras, "namespaces": nss,
                   "teoremas_publicos_do_manifesto": m.get("teoremas_publicos"), "relatorios_no_trio_do_manifesto": m.get("relatorios_no_trio"),
                   "diff": "kernel/bundle/%s.diff" % n, "diff_texto": "".join(dif)}

# ---------------------------------------------------------------- a ordem topologica (Kahn; desempate pela ordem do manifesto)
ordem = []; feitos = set(); resto = list(SUG_NOMES)   # (v413: o desempate e' a ordem_topologica_sugerida do manifesto)
while resto:
    prontos = [x for x in resto if set(deps[x]) <= feitos]
    assert prontos, ("ciclo de imports entre as candidatas", resto)
    x = prontos[0]; ordem.append(x); feitos.add(x); resto.remove(x)
dependentes = {x: sorted({y for y in NOMES if x in deps[y]}) for x in NOMES}
ORDEM_IGUAL_A_SUGERIDA = (ordem == SUG_NOMES)


# ---------------------------------------------------------------- o modulo corrigido so' no texto (kernel_corrigido): conferido; quem depende dele no kernel (grafo de imports do sandbox)
def _sem_comentarios(t_):
    """tira os comentarios (-- ate' o fim da linha; /- ... -/ aninhados, inclusive /-- e /-!) e MANTEM as cadeias; normaliza os espacos: o que sobra e' o codigo"""
    out_ = []; i_ = 0; n_ = len(t_); prof = 0; instr = False
    while i_ < n_:
        c_ = t_[i_]
        if prof == 0 and instr:
            out_.append(c_)
            if c_ == "\\" and i_ + 1 < n_:
                out_.append(t_[i_ + 1]); i_ += 2; continue
            if c_ == '"':
                instr = False
            i_ += 1; continue
        if t_.startswith("/-", i_):
            prof += 1; i_ += 2; continue
        if prof > 0:
            if t_.startswith("-/", i_):
                prof -= 1; i_ += 2; continue
            i_ += 1; continue
        if t_.startswith("--", i_):
            j_ = t_.find("\n", i_)
            i_ = n_ if j_ < 0 else j_; continue
        if c_ == '"':
            instr = True
        out_.append(c_); i_ += 1
    return " ".join("".join(out_).split())


grafo = {}
for raiz_ in ("TGL", "TGLExt"):
    for dp_, dn_, fn_ in os.walk(K13 / raiz_):
        for f_ in fn_:
            if f_.endswith(".lean") and ".bak" not in f_:
                pp_ = Path(dp_) / f_
                mod_ = str(pp_.relative_to(K13))[:-len(".lean")].replace(os.sep, ".")
                grafo[mod_] = re.findall(r"(?m)^import\s+(\S+)", LT.mascara_comentarios(pp_.read_bytes().decode("utf-8")))
for f_ in ("TGLExt.lean", "TGL.lean"):
    grafo[f_[:-len(".lean")]] = re.findall(r"(?m)^import\s+(\S+)", (K13 / f_).read_bytes().decode("utf-8"))
for x in NOMES:
    grafo["TGLExt." + x] = RX_IMPORT.findall(saida[x].decode("utf-8"))
grafo["TGLExt"] = sorted(set(grafo.get("TGLExt", [])) | {"TGLExt." + x for x in NOMES})   # (a raiz nova importa os modulos novos)
reverso = {}
for a_, L_ in grafo.items():
    for b_ in L_:
        reverso.setdefault(b_, set()).add(a_)


def dependentes_no_kernel(mod_):
    vis_ = set(); fila_ = [mod_]
    while fila_:
        a_ = fila_.pop()
        for y_ in reverso.get(a_, ()):
            if y_ not in vis_:
                vis_.add(y_); fila_.append(y_)
    return vis_


kc = {}
for nome_, b_ in kc_bytes.items():
    t_ = b_.decode("utf-8"); v_ = kc_rec[nome_]["manifesto"]; nos_t = kc_rec[nome_]["nos_bytes"].decode("utf-8")
    assert "\r" not in t_, ("CR na fonte corrigida: PARE", nome_)
    assert not re.search(r"(?m)^#print axioms", t_), ("linha #print axioms na fonte corrigida (o instalado tem de ser o insumo): PARE", nome_)
    assert _sem_comentarios(t_) == _sem_comentarios(nos_t), ("o CODIGO da fonte corrigida (sem comentarios, com cadeias) difere do da origem no Nos: so' o texto pode mudar; PARE", nome_)
    assert " ".join(LT.mascara_comentarios(t_).split()) == " ".join(LT.mascara_comentarios(nos_t).split()), ("o codigo mascarado da fonte corrigida difere do da origem: PARE", nome_)
    cod_ = LT.mascara_comentarios(t_)
    assert not re.search(r"\bsorry\b", cod_) and "#eval" not in cod_ and "#print" not in cod_ and not re.search(r"^\s*axiom\s", cod_, re.M), ("sorry/#eval/#print/axiom no codigo corrigido", nome_)
    atual_ = (K13 / "TGLExt" / (nome_ + ".lean")).read_bytes()
    assert sha(atual_) in (v_["sha256_origem"], v_["sha256_saida"]), ("o sandbox nao tem nem a fonte de origem nem a corrigida do modulo corrigido: PARE", nome_, sha(atual_)[:16])
    dep_ = dependentes_no_kernel("TGLExt." + nome_)
    dif_ = "".join(difflib.unified_diff(nos_t.splitlines(True), t_.splitlines(True), fromfile="Nos(v412)/tgl_kernel/TGLExt/%s.lean (sha256_origem)" % nome_,
                                        tofile="C:/t/k413c/final/TGLExt/%s.lean (sha256_saida)" % nome_, n=1))
    kc[nome_] = {"modulo": nome_, "modulo_completo": "TGLExt." + nome_, "rel": "TGLExt/%s.lean" % nome_, "insumo": kc_rec[nome_]["fonte"], "recibo_da_correcao": kc_rec[nome_]["recibo"],
                 "recibo_da_correcao_sha256": kc_rec[nome_]["recibo_sha256"], "sha256_origem": v_["sha256_origem"], "sha256_insumo": sha(b_), "sha256": sha(b_), "sha16": sha(b_)[:16], "bytes": len(b_),
                 "sha256_no_sandbox_antes_deste_preparo": sha(atual_), "codigo_identico_a_origem": True, "fundamento": v_.get("fundamento"), "sha256_fundamento": v_.get("sha256_fundamento"),
                 "teoremas_publicos_do_manifesto": v_.get("teoremas_publicos"), "n_print_axioms_removidos": 0,
                 "novos_que_dependem_dele": sorted(x for x in NOMES if ("TGLExt." + x) in dep_),
                 "dependentes_antigos_no_kernel": sorted(y for y in dep_ if not (y.startswith("TGLExt.") and y[len("TGLExt."):] in NOMES)),
                 "diff": "kernel/bundle/%s.diff" % nome_, "diff_texto": dif_}


def fecho_dependentes(xs):
    out = set(xs); fila = list(xs)
    while fila:
        a = fila.pop()
        for y in dependentes[a]:
            if y not in out:
                out.add(y); fila.append(y)
    return [y for y in ordem if y in out]


# ---------------------------------------------------------------- a raiz: a do Nos v412 + um import por modulo, na ordem topologica
raiz_nos = (NOS / "TGLExt.lean").read_bytes().decode("utf-8")
nl = "\r\n" if "\r\n" in raiz_nos else "\n"
assert raiz_nos.endswith(nl), "a raiz do Nos nao termina em quebra de linha"
ROOT_SUFFIX = "".join("import TGLExt.%s%s" % (x, nl) for x in ordem)
for x in ordem:
    assert ("import TGLExt.%s%s" % (x, nl)) not in raiz_nos and not raiz_nos.rstrip().endswith("import TGLExt." + x), ("o import ja esta na raiz do Nos", x)
raiz_nova = (raiz_nos + ROOT_SUFFIX).encode("utf-8")
raiz_k12 = (K13 / "TGLExt.lean").read_bytes()
prefixos_ok = [raiz_nos.encode("utf-8")]
assert raiz_k12 == raiz_nova or raiz_k12.startswith(raiz_nos.encode("utf-8")), "a raiz do k413c nao comeca pela raiz do Nos v412"

if SECO:
    mud = [x for x in ordem if not (K13 / "TGLExt" / (x + ".lean")).exists() or (K13 / "TGLExt" / (x + ".lean")).read_bytes() != saida[x]]
    kc_mud = [x for x in kc if (K13 / "TGLExt" / (x + ".lean")).read_bytes() != kc_bytes[x]]
    print("SECO: nada gravado | modulos novos:", len(ordem), "| a gravar/trocar no sandbox:", len(mud), "| corrigidos a trocar:", kc_mud, "| ordem:", " ".join(ordem),
          "| igual a sugerida do manifesto:", ORDEM_IGUAL_A_SUGERIDA)
    print("     | #print axioms removidos:", sum(e["n_print_axioms_removidos"] for e in entradas.values()), "| imports trocados:", sum(len(e["imports_trocados"]) for e in entradas.values()))
    for x, e in kc.items():
        print("     | corrigido %s: novos que dependem dele %d; dependentes antigos no kernel %d" % (x, len(e["novos_que_dependem_dele"]), len(e["dependentes_antigos_no_kernel"])))
    sys.exit(0)

retirados = []


def troca_com_backup(path, novo, no_lugar=True):
    """grava `novo` em `path`; se `path` existe e difere: backup de BYTES antes (no lugar: .bak_<ts>; no sandbox: na quarentena, fora da arvore do lake), conferido."""
    path = Path(path)
    if path.exists():
        velho = path.read_bytes()
        if velho == novo:
            return False
        bk = (path.parent / (path.name + ".bak_" + TS)) if no_lugar else (QUAR / path.relative_to(K13))
        bk.parent.mkdir(parents=True, exist_ok=True)
        bk.write_bytes(velho); assert bk.read_bytes() == velho
        retirados.append({"arquivo": str(path), "backup": str(bk), "sha256_antigo": sha(velho), "sha256_novo": sha(novo)})
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.parent / (path.name + ".tmp_" + TS)
    tmp.write_bytes(novo); assert tmp.stat().st_size == len(novo)
    os.replace(tmp, path)
    assert path.read_bytes() == novo
    return True


def grava_txt(path, txt):
    path = Path(path); b_ = txt.encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() == b_:
            return
        bk = path.parent / (path.name + ".bak_" + TS); bk.write_bytes(path.read_bytes()); assert bk.read_bytes() == path.read_bytes()
    tmp = path.parent / (path.name + ".tmp"); tmp.write_bytes(b_); assert tmp.stat().st_size == len(b_); os.replace(tmp, path)


mudados = []
for x in ordem:
    troca_com_backup(PK / "pedra" / "origem" / (x + ".lean"), bytes_de[x])
    troca_com_backup(PK / "pedra" / (x + ".lean"), saida[x])
    if troca_com_backup(K13 / "TGLExt" / (x + ".lean"), saida[x], no_lugar=False):
        mudados.append(x)
    assert (K13 / "TGLExt" / (x + ".lean")).read_bytes() == (PK / "pedra" / (x + ".lean")).read_bytes() == saida[x]
    grava_txt(BD / (x + ".diff"), entradas[x]["diff_texto"])
kc_mudados = []
for x, e in kc.items():
    troca_com_backup(PK / "pedra" / "origem" / (x + ".lean"), kc_bytes[x])
    troca_com_backup(PK / "pedra" / (x + ".lean"), kc_bytes[x])
    if troca_com_backup(K13 / "TGLExt" / (x + ".lean"), kc_bytes[x], no_lugar=False):   # (o antigo do sandbox vai para a quarentena, fora da arvore do lake, conferido)
        kc_mudados.append(x)
    assert (K13 / "TGLExt" / (x + ".lean")).read_bytes() == (PK / "pedra" / (x + ".lean")).read_bytes() == kc_bytes[x]
    grava_txt(BD / (x + ".diff"), e["diff_texto"])
raiz_mudou = troca_com_backup(K13 / "TGLExt.lean", raiz_nova, no_lugar=False)
assert (K13 / "TGLExt.lean").read_bytes() == raiz_nova
# (correcao de 17/11, 06:10, depois do teste de fumaca: sem mudanca no sandbox, NADA dos registros da instalacao e' regravado -- o BUNDLE, a lista, a ULTIMA_INSTALACAO e o script do build
#  guardam a instalacao que o build usou; com mudanca, o historico do que saiu para a quarentena ACUMULA, nunca e' apagado)
_bd_p = PK / "BUNDLE_v413.json"
bd_prev = json.loads(_bd_p.read_text(encoding="utf-8")) if _bd_p.exists() else None
if not mudados and not raiz_mudou and not kc_mudados and bd_prev and bd_prev.get("manifesto_sha256") == sha(MAN_P.read_bytes()) \
        and [m_["sha256"] for m_ in bd_prev.get("modulos", [])] == [entradas[x]["sha256"] for x in ordem] \
        and [m_["sha256"] for m_ in bd_prev.get("kernel_corrigido", [])] == [kc[x]["sha256"] for x in kc]:
    print("NADA MUDOU no sandbox (os %d modulos novos, o corrigido e a raiz ja sao os do manifesto): BUNDLE_v413.json, kernel_modulos_novos_v413.json, kernel\\ULTIMA_INSTALACAO_v413.json e construir_kernel_v413.sh ficam como estao" % len(ordem))
    sys.exit(0)
retirados_hist = list((bd_prev or {}).get("retirados_do_sandbox_e_da_pedra") or [])
quarentenas = list((bd_prev or {}).get("quarentenas") or ([bd_prev["quarentena"]] if bd_prev and bd_prev.get("quarentena") else []))
if QUAR.exists():
    quarentenas.append(str(QUAR))
rels = ["TGLExt/%s.lean" % x for x in ordem]
modulos = []
for x in ordem:
    e = dict(entradas[x]); e.pop("diff_texto"); modulos.append(e)
kcl = []
for x in kc:
    e = dict(kc[x]); e.pop("diff_texto"); kcl.append(e)
grava_txt(PK / "kernel_modulos_novos_v413.json", json.dumps({"novos": rels, "n": len(rels), "root_suffix": ROOT_SUFFIX, "ordem_topologica": ordem, "gerado": TS,
                                                             "kernel_corrigido": ["TGLExt/%s.lean" % x for x in kc]}, ensure_ascii=False, indent=1))
grava_txt(PK / "BUNDLE_v413.json", json.dumps({
    "contrato": "BUNDLE_v413", "gerado": TS, "n": len(modulos), "manifesto": str(MAN_P), "manifesto_sha256": sha(MAN_P.read_bytes()), "manifesto_gerado_em": MAN.get("gerado_em"),
    "pedras": str(PED), "normalizacao": "so' a mudanca permitida (ordem da Etapa 1 da v413, item 2): as linhas #print axioms saem do corpo instalado (como na v412) e o fim do arquivo fica com uma quebra "
                                         "de linha; os imports ja vinham como TGLExt.<Nome> (nenhum trocado); as fontes ja eram LF; nenhuma prova tocada; o modulo corrigido entra com os bytes do insumo "
                                         "(sem #print axioms; codigo identico ao da origem)",
    "root_suffix": ROOT_SUFFIX, "ordem_topologica": ordem, "ordem_topologica_sugerida": SUG_NOMES, "ordem_topologica_igual_a_sugerida": ORDEM_IGUAL_A_SUGERIDA, "dependentes": dependentes,
    "retirados_do_sandbox_e_da_pedra": retirados_hist + retirados, "quarentena": str(QUAR) if QUAR.exists() else (bd_prev or {}).get("quarentena"), "quarentenas": quarentenas,
    "modulos": modulos, "kernel_corrigido": kcl}, ensure_ascii=False, indent=1))
sha_mod = {x: {"sha256_insumo": entradas[x]["sha256_insumo"], "sha256_instalado_no_sandbox": entradas[x]["sha256"], "diff": entradas[x]["diff"],
               "n_print_axioms_removidos": entradas[x]["n_print_axioms_removidos"], "imports_trocados": entradas[x]["imports_trocados"]} for x in ordem}
for x in kc:
    sha_mod[x] = {"kernel_corrigido": True, "sha256_insumo": kc[x]["sha256_insumo"], "sha256_instalado_no_sandbox": kc[x]["sha256"], "sha256_origem_no_nos": kc[x]["sha256_origem"],
                  "diff": kc[x]["diff"], "n_print_axioms_removidos": 0, "imports_trocados": []}
grava_txt(BD / "SHA256_POR_MODULO_v413.json", json.dumps(sha_mod, ensure_ascii=False, indent=1))
novos_do_kc = sorted({y for x in kc_mudados for y in kc[x]["novos_que_dependem_dele"]})
reconstruir = fecho_dependentes(sorted(set(mudados) | set(novos_do_kc)))
grava_txt(KD / "ULTIMA_INSTALACAO_v413.json", json.dumps({"quando": TS, "manifesto_sha256": sha(MAN_P.read_bytes()), "mudados_no_sandbox": mudados, "kernel_corrigido_mudado": kc_mudados,
                                                          "raiz_mudou": raiz_mudou,
                                                          "o_lake_recompila": reconstruir + (["TGLExt (raiz)", "TGL.Audit"] if (mudados or raiz_mudou or kc_mudados) else []),
                                                          "kernel_corrigido_recompila": ["TGLExt." + x for x in kc_mudados],
                                                          "dependentes_antigos_do_corrigido_que_o_lake_recompila": sorted({y for x in kc_mudados for y in kc[x]["dependentes_antigos_no_kernel"]}),
                                                          "retirados": retirados}, ensure_ascii=False, indent=1))
# ---------------------------------------------------------------- o script do build (por modulo, na ordem topologica; para no primeiro que nao compilar)
lista = " ".join(["TGLExt.%s" % x for x in kc] + ["TGLExt.%s" % x for x in ordem])
sh = """#!/bin/sh
# Constroi o kernel do SANDBOX da v413 (C:\\t\\k413c\\final; NUNCA o do Nos). Gerado por preparar_bundle_v413.py (claude-construtor-v413) em %(ts)s; nao editar a mao (regerar pelo preparo).
# Molde: v412\\construir_kernel_v412.sh. Diferenca: primeiro o modulo que a v413 corrige so' no texto (%(kc)s), depois os %(n)d modulos novos, UM A UM, na ordem topologica das dependencias
# (`lake build +<modulo>`); o script PARA no primeiro que nao compilar (marca `parou_em=` e nao roda o resto nem o Audit); so' depois vem o `lake build` inteiro (os modulos antigos que dependem
# do corrigido, a raiz e o TGL.Audit) e o Audit (`lake env lean TGL/Audit.lean`).
# O build e' INCREMENTAL no que e' antigo e nao depende do corrigido (o kernel da v412 ja compilado em .lake/build, copiado do k412c) e A FRIO nos modulos novos. Marcas em kernel/construir_marcas.txt.
K="/c/t/k413c/final"
D="/c/IALD/Central de Patentes/work/cadeia_de_selo/v413/kernel"
LAKE=/c/Users/rotol/.elan/bin/lake
mkdir -p "$D"
for f in lake_build.log audit.log build_full.log construir_marcas.txt; do [ -f "$D/$f" ] && cp -p "$D/$f" "$D/$f.bak_$(date +%%Y%%m%%d_%%H%%M%%S)"; done
cd "$K" || exit 9
echo "inicio $(date '+%%Y-%%m-%%d %%H:%%M:%%S')" > "$D/construir_marcas.txt"
echo "epoch_inicio=$(date +%%s)" >> "$D/construir_marcas.txt"
: > "$D/lake_build.log"
rb=0
for m in %(lista)s; do
  t0=$(date +%%s)
  echo "=== MODULO $m (inicio $(date '+%%H:%%M:%%S'))" >> "$D/lake_build.log"
  $LAKE build "+$m" >> "$D/lake_build.log" 2>&1; r=$?
  echo "modulo=$m rc=$r s=$(( $(date +%%s) - t0 ))" >> "$D/construir_marcas.txt"
  if [ "$r" != "0" ]; then rb=$r; echo "parou_em=$m" >> "$D/construir_marcas.txt"; break; fi
done
if [ "$rb" = "0" ]; then
  echo "=== BUILD INTEIRO (inicio $(date '+%%H:%%M:%%S'))" >> "$D/lake_build.log"
  $LAKE build >> "$D/lake_build.log" 2>&1; rb=$?
fi
echo "rc_build=$rb $(date '+%%H:%%M:%%S')" >> "$D/construir_marcas.txt"
echo "epoch_build_fim=$(date +%%s)" >> "$D/construir_marcas.txt"
if [ "$rb" = "0" ]; then
  $LAKE env lean TGL/Audit.lean > "$D/audit.log" 2>&1; ra=$?
else
  ra=99; echo "o Audit NAO rodou: o build parou (rc_build=$rb)" > "$D/audit.log"
fi
echo "rc_audit=$ra $(date '+%%H:%%M:%%S')" >> "$D/construir_marcas.txt"
echo "epoch_audit_fim=$(date +%%s)" >> "$D/construir_marcas.txt"
if [ "$rb" = "0" ] && [ "$ra" = "0" ]; then echo "rc=0" >> "$D/construir_marcas.txt"; else echo "rc=1" >> "$D/construir_marcas.txt"; fi
echo "fim $(date '+%%Y-%%m-%%d %%H:%%M:%%S')" >> "$D/construir_marcas.txt"
cat "$D/construir_marcas.txt"
""" % {"ts": TS, "n": len(ordem), "lista": lista, "kc": ", ".join("TGLExt." + x for x in kc) or "nenhum"}
grava_txt(PK / "construir_kernel_v413.sh", sh)
print("bundle:", len(ordem), "modulos novos | mudados no sandbox nesta rodada:", len(mudados), "| corrigidos trocados:", kc_mudados, "| raiz mudou:", raiz_mudou, "| o lake recompila:", len(reconstruir),
      "modulos novos + raiz + Audit" if (mudados or raiz_mudou or kc_mudados) else "(nada)")
print("ordem:", " ".join(ordem), "| igual a sugerida do manifesto:", ORDEM_IGUAL_A_SUGERIDA)
for x in ordem:
    e = entradas[x]
    print("  %-28s insumo %s -> instalado %s | #print axioms removidos %3d | irmaos %d" % (x, e["sha16_insumo"], e["sha16"], e["n_print_axioms_removidos"], len(e["dependencias_no_bundle"])))
for x, e in kc.items():
    print("  corrigido %-18s origem %s -> instalado %s | novos que dependem dele %d | dependentes antigos no kernel %d" % (x, e["sha256_origem"][:16], e["sha16"], len(e["novos_que_dependem_dele"]),
                                                                                                                       len(e["dependentes_antigos_no_kernel"])))
for r_ in retirados:
    print("  retirado (com backup):", r_["arquivo"], "->", r_["backup"])
