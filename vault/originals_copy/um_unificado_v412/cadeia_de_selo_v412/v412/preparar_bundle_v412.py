# -*- coding: utf-8 -*-
"""preparar_bundle_v412.py -- v412, Etapa 1, item 2 (claude-construtor-v412, 17/11/2026, a servico da gerencia c1): instala no sandbox C:\\t\\k412c\\final, em TGLExt\\, os modulos novos
da v412 a partir das copias CONGELADAS em insumos\\pedras\\ e do manifesto insumos\\MANIFESTO_PEDRAS_v412.json (gerados pela gerencia; nunca editados aqui).
Molde: v410\\preparar_bundle_v410_06nov.py (IALD2) e preparar_bundle_v410_aescala_09nov.py (AEscala); v409\\preparar_bundle_v409_05nov.py (dois modulos).

O que faz, para cada modulo (tudo conferido, nada digitado):
  1. CONFERE o sha256 da copia congelada contra o manifesto (fail-closed: um so' diferente aborta tudo, nada e' gravado);
  2. as DUAS unicas mudancas permitidas no texto (ordem da Etapa 1, item 2): (a) a linha `import <Nome>` de uma candidata irma (lista `imports_de_candidatas` do manifesto) passa a
     `import TGLExt.<Nome>`; (b) o que o molde da v410 fez com as linhas `#print axioms`: SAEM do corpo instalado (a linha inteira; as ancoras sao LIDAS delas antes, com a pilha de
     namespace da linha, para o pos_build conferir no Audit) e o fim do arquivo fica com UMA quebra de linha (rstrip + "\\n", como o molde). Nenhuma prova e' tocada. As fontes ja sao LF
     (conferido: nenhum CR; se houvesse, o script PARA: a normalizacao de fim de linha nao esta entre as mudancas permitidas);
  3. confere por RECONSTRUCAO independente que o instalado == insumo menos as linhas `#print axioms` com as linhas de import trocadas; grava o diff unificado e os dois sha256 em kernel\\bundle\\;
  4. confere que todo import TGLExt.*/TGL.* existe no kernel do Nos v411 ou no proprio bundle, e todo import Mathlib.* existe na mathlib do sandbox; que nenhuma linha `#print axioms`
     estava dentro de comentario; que nao ha `sorry`, `#eval`, `#print` nem `axiom` no CODIGO (comentarios e cadeias mascarados);
e grava, na ordem TOPOLOGICA das dependencias (desempate: a ordem do manifesto): pedra\\origem\\<Nome>.lean (os bytes do insumo), pedra\\<Nome>.lean (o instalado), o sandbox
TGLExt\\<Nome>.lean; a raiz TGLExt.lean do sandbox = a do Nos v411 + um import por modulo (na ordem topologica); kernel_modulos_novos_v412.json, BUNDLE_v412.json,
kernel\\bundle\\SHA256_POR_MODULO_v412.json e o construir_kernel_v412.sh (build POR MODULO na ordem topologica, parando no primeiro que nao compilar; depois o build inteiro e o Audit).

TROCAR UMA FONTE (a ordem 023 pode mudar texto de sete fontes; a gerencia regera o manifesto): rodar `reconstruir_kernel_v412.py` (este preparo + o build + o pos_build). O preparo e'
idempotente: so' o que mudou e' regravado (o arquivo antigo do sandbox vai para C:\\t\\k412c\\quarentena_<data>, conferido), e o lake recompila so' o modulo trocado e os que dependem
dele (mais a raiz e o Audit). O que mudou e quem depende dele fica em kernel\\ULTIMA_INSTALACAO_v412.json.
Nada toca o Nos (so' leitura). Uso: C:\\Python314\\python.exe -B -X utf8 preparar_bundle_v412.py [--seco] [--manifesto <json>] [--pedras <pasta>]"""
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
import lean_texto_v412 as LT  # noqa: E402

SECO = "--seco" in sys.argv
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
arg = lambda k, d: Path(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
MAN_P = arg("--manifesto", PK / "insumos" / "MANIFESTO_PEDRAS_v412.json")
PED = arg("--pedras", PK / "insumos" / "pedras")
K12 = Path("C:/t/k412c/final")
QUAR = Path("C:/t/k412c") / ("quarentena_" + TS)
NOS = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel")
MATHLIB = K12 / ".lake" / "packages" / "mathlib"
KD = PK / "kernel"; BD = KD / "bundle"
sha = lambda b: hashlib.sha256(b).hexdigest()
RX_PRINT = re.compile(r"^#print axioms (\S+)[ \t]*\n?", re.M)
RX_IMPORT = re.compile(r"^import (\S+)[ \t]*$", re.M)

MAN = json.loads(MAN_P.read_text(encoding="utf-8"))
MODS = MAN["modulos"]
NOMES = [m["modulo"] for m in MODS]
assert len(NOMES) == len(set(NOMES)) == int(MAN["n_modulos"]), ("o manifesto nao tem n_modulos nomes distintos", len(NOMES), MAN["n_modulos"])
assert not MAN.get("imports_soltos_sem_modulo_no_conjunto"), ("o manifesto diz import solto sem modulo no conjunto", MAN.get("imports_soltos_sem_modulo_no_conjunto"))
assert set(MAN["imports_soltos_de_candidatas"]) <= set(NOMES), "import solto do manifesto que nao e' modulo do conjunto"
selo = json.loads((NOS.parent / "um_absoluto_selo.json").read_text(encoding="utf-8"))
assert selo.get("um_version") == "v411", ("o Nos nao e' a v411 selada", selo.get("um_version"))

# ---------------------------------------------------------------- 1. o sha256 de TODAS as copias congeladas (fail-closed antes de gravar qualquer coisa)
bytes_de = {}
ruins = []
for m in MODS:
    p = PED / (m["modulo"] + ".lean")
    b = p.read_bytes()
    if sha(b) != m["sha256"] or len(b) != int(m["bytes"]):
        ruins.append([m["modulo"], sha(b)[:16], m["sha256"][:16]])
    bytes_de[m["modulo"]] = b
assert not ruins, ("copia congelada com sha256/bytes diferente do manifesto: NADA foi gravado", ruins)

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
    assert len(i_print) == int(m["linhas_print_axioms"]), ("numero de #print axioms != manifesto", n, len(i_print), m["linhas_print_axioms"])
    ancoras = []
    for i in i_print:
        nome = re.match(r"^#print axioms (\S+)", linhas[i]).group(1)
        ancoras.append({"texto": nome, "namespace": ".".join(pilhas[i]), "linha": i + 1})
    # os imports (so' em codigo)
    imp_cod = [(i, re.match(r"^import (\S+)[ \t]*$", l).group(1)) for i, l in enumerate(mlinhas) if re.match(r"^import (\S+)[ \t]*$", l)]
    imp_txt = [(i, re.match(r"^import (\S+)[ \t]*$", l).group(1)) for i, l in enumerate(linhas) if re.match(r"^import (\S+)[ \t]*$", l)]
    assert imp_cod == imp_txt, ("linha import dentro de comentario", n)
    assert [x for _, x in imp_txt] == list(m["imports"]), ("os imports da fonte nao sao os do manifesto", n, [x for _, x in imp_txt], m["imports"])
    trocar = {i: x for i, x in imp_txt if x in NOMES}
    assert sorted(trocar.values()) == sorted(m["imports_de_candidatas"]), ("os imports de candidatas irmas nao sao os do manifesto", n, sorted(trocar.values()), m["imports_de_candidatas"])
    deps[n] = sorted(set(trocar.values()))
    # a transformacao (as duas unicas mudancas)
    novas = []
    for i, l in enumerate(linhas):
        if i in set(i_print):
            continue
        novas.append(("import TGLExt.%s" % trocar[i]) if i in trocar else l)
    out_t = "\n".join(novas).rstrip("\n") + "\n"
    # RECONSTRUCAO independente: o RX do molde da v410 sobre o texto inteiro + a troca por expressao regular so' das linhas de import de candidata
    rec = RX_PRINT.sub("", t)
    rec = RX_IMPORT.sub(lambda mm: ("import TGLExt." + mm.group(1)) if mm.group(1) in NOMES else mm.group(0), rec).rstrip("\n") + "\n"
    assert rec == out_t, ("a reconstrucao independente difere da transformacao", n)
    # o diff: so' linhas `#print axioms` removidas, imports trocados e o fim de arquivo
    dif = list(difflib.unified_diff(t.splitlines(True), out_t.splitlines(True), fromfile="insumos/pedras/%s.lean" % n, tofile="C:/t/k412c/final/TGLExt/%s.lean" % n, n=0))
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
            assert (NOS / (imp.replace(".", "/") + ".lean")).exists(), ("import ausente do kernel do Nos v411", n, imp)
        elif imp.startswith("Mathlib"):
            assert (MATHLIB / (imp.replace(".", "/") + ".lean")).exists(), ("import Mathlib ausente da mathlib do sandbox", n, imp)
        else:
            raise AssertionError(("import de origem desconhecida", n, imp))
    assert not (NOS / "TGLExt" / (n + ".lean")).exists(), ("o modulo ja existe no Nos", n)
    saida[n] = out_t.encode("utf-8")
    entradas[n] = {"modulo": n, "rel": "TGLExt/%s.lean" % n, "frente": m["frente"], "de_quem": m["de_quem"], "estado_da_revisao": m["estado_da_revisao"],
                   "origem_da_gerencia": m["origem"], "insumo": str(PED / (n + ".lean")), "sha256_insumo": sha(b), "sha16_insumo": sha(b)[:16], "bytes_insumo": len(b),
                   "sha256": sha(saida[n]), "sha16": sha(saida[n])[:16], "bytes": len(saida[n]),
                   "imports": RX_IMPORT.findall(out_t), "imports_trocados": [{"antes": "import " + x, "depois": "import TGLExt." + x} for x in [trocar[i] for i in sorted(trocar)]],
                   "dependencias_no_bundle": deps[n], "n_print_axioms_removidos": len(i_print), "ancoras": ancoras, "namespaces": m["namespaces"],
                   "declaracoes_theorem_lemma_do_manifesto": m["declaracoes_theorem_lemma"], "diff": "kernel/bundle/%s.diff" % n, "diff_texto": "".join(dif)}

# ---------------------------------------------------------------- a ordem topologica (Kahn; desempate pela ordem do manifesto)
ordem = []; feitos = set(); resto = list(NOMES)
while resto:
    prontos = [x for x in resto if set(deps[x]) <= feitos]
    assert prontos, ("ciclo de imports entre as candidatas", resto)
    x = prontos[0]; ordem.append(x); feitos.add(x); resto.remove(x)
dependentes = {x: sorted({y for y in NOMES if x in deps[y]}) for x in NOMES}


def fecho_dependentes(xs):
    out = set(xs); fila = list(xs)
    while fila:
        a = fila.pop()
        for y in dependentes[a]:
            if y not in out:
                out.add(y); fila.append(y)
    return [y for y in ordem if y in out]


# ---------------------------------------------------------------- a raiz: a do Nos v411 + um import por modulo, na ordem topologica
raiz_nos = (NOS / "TGLExt.lean").read_bytes().decode("utf-8")
nl = "\r\n" if "\r\n" in raiz_nos else "\n"
assert raiz_nos.endswith(nl), "a raiz do Nos nao termina em quebra de linha"
ROOT_SUFFIX = "".join("import TGLExt.%s%s" % (x, nl) for x in ordem)
for x in ordem:
    assert ("import TGLExt.%s%s" % (x, nl)) not in raiz_nos and not raiz_nos.rstrip().endswith("import TGLExt." + x), ("o import ja esta na raiz do Nos", x)
raiz_nova = (raiz_nos + ROOT_SUFFIX).encode("utf-8")
raiz_k12 = (K12 / "TGLExt.lean").read_bytes()
prefixos_ok = [raiz_nos.encode("utf-8")]
assert raiz_k12 == raiz_nova or raiz_k12.startswith(raiz_nos.encode("utf-8")), "a raiz do k412c nao comeca pela raiz do Nos v411"

if SECO:
    mud = [x for x in ordem if not (K12 / "TGLExt" / (x + ".lean")).exists() or (K12 / "TGLExt" / (x + ".lean")).read_bytes() != saida[x]]
    print("SECO: nada gravado | modulos:", len(ordem), "| a gravar/trocar no sandbox:", len(mud), "| ordem:", " ".join(ordem))
    print("     | #print axioms removidos:", sum(e["n_print_axioms_removidos"] for e in entradas.values()), "| imports trocados:", sum(len(e["imports_trocados"]) for e in entradas.values()))
    sys.exit(0)

retirados = []


def troca_com_backup(path, novo, no_lugar=True):
    """grava `novo` em `path`; se `path` existe e difere: backup de BYTES antes (no lugar: .bak_<ts>; no sandbox: na quarentena, fora da arvore do lake), conferido."""
    path = Path(path)
    if path.exists():
        velho = path.read_bytes()
        if velho == novo:
            return False
        bk = (path.parent / (path.name + ".bak_" + TS)) if no_lugar else (QUAR / path.relative_to(K12))
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
    if troca_com_backup(K12 / "TGLExt" / (x + ".lean"), saida[x], no_lugar=False):
        mudados.append(x)
    assert (K12 / "TGLExt" / (x + ".lean")).read_bytes() == (PK / "pedra" / (x + ".lean")).read_bytes() == saida[x]
    grava_txt(BD / (x + ".diff"), entradas[x]["diff_texto"])
raiz_mudou = troca_com_backup(K12 / "TGLExt.lean", raiz_nova, no_lugar=False)
assert (K12 / "TGLExt.lean").read_bytes() == raiz_nova
# (correcao de 17/11, 06:10, depois do teste de fumaca: sem mudanca no sandbox, NADA dos registros da instalacao e' regravado -- o BUNDLE, a lista, a ULTIMA_INSTALACAO e o script do build
#  guardam a instalacao que o build usou; com mudanca, o historico do que saiu para a quarentena ACUMULA, nunca e' apagado)
_bd_p = PK / "BUNDLE_v412.json"
bd_prev = json.loads(_bd_p.read_text(encoding="utf-8")) if _bd_p.exists() else None
if not mudados and not raiz_mudou and bd_prev and bd_prev.get("manifesto_sha256") == sha(MAN_P.read_bytes()) \
        and [m_["sha256"] for m_ in bd_prev.get("modulos", [])] == [entradas[x]["sha256"] for x in ordem]:
    print("NADA MUDOU no sandbox (os %d modulos e a raiz ja sao os do manifesto): BUNDLE_v412.json, kernel_modulos_novos_v412.json, kernel\\ULTIMA_INSTALACAO_v412.json e construir_kernel_v412.sh ficam como estao" % len(ordem))
    sys.exit(0)
retirados_hist = list((bd_prev or {}).get("retirados_do_sandbox_e_da_pedra") or [])
quarentenas = list((bd_prev or {}).get("quarentenas") or ([bd_prev["quarentena"]] if bd_prev and bd_prev.get("quarentena") else []))
if QUAR.exists():
    quarentenas.append(str(QUAR))
rels = ["TGLExt/%s.lean" % x for x in ordem]
modulos = []
for x in ordem:
    e = dict(entradas[x]); e.pop("diff_texto"); modulos.append(e)
grava_txt(PK / "kernel_modulos_novos_v412.json", json.dumps({"novos": rels, "n": len(rels), "root_suffix": ROOT_SUFFIX, "ordem_topologica": ordem, "gerado": TS}, ensure_ascii=False, indent=1))
grava_txt(PK / "BUNDLE_v412.json", json.dumps({
    "contrato": "BUNDLE_v412", "gerado": TS, "n": len(modulos), "manifesto": str(MAN_P), "manifesto_sha256": sha(MAN_P.read_bytes()), "manifesto_gerado_em": MAN.get("gerado_em"),
    "pedras": str(PED), "normalizacao": "so' as duas mudancas permitidas (ordem da Etapa 1, item 2): import de candidata irma -> import TGLExt.<Nome>; as linhas #print axioms saem do corpo instalado "
                                         "(como o molde da v410) e o fim do arquivo fica com uma quebra de linha; as fontes ja eram LF; nenhuma prova tocada",
    "ficam_fora": MAN.get("ficam_fora"), "root_suffix": ROOT_SUFFIX, "ordem_topologica": ordem, "dependentes": dependentes,
    "retirados_do_sandbox_e_da_pedra": retirados_hist + retirados, "quarentena": str(QUAR) if QUAR.exists() else (bd_prev or {}).get("quarentena"), "quarentenas": quarentenas,
    "modulos": modulos}, ensure_ascii=False, indent=1))
grava_txt(BD / "SHA256_POR_MODULO_v412.json", json.dumps({x: {"sha256_insumo": entradas[x]["sha256_insumo"], "sha256_instalado_no_sandbox": entradas[x]["sha256"],
                                                              "diff": entradas[x]["diff"], "n_print_axioms_removidos": entradas[x]["n_print_axioms_removidos"],
                                                              "imports_trocados": entradas[x]["imports_trocados"]} for x in ordem}, ensure_ascii=False, indent=1))
reconstruir = fecho_dependentes(mudados)
grava_txt(KD / "ULTIMA_INSTALACAO_v412.json", json.dumps({"quando": TS, "manifesto_sha256": sha(MAN_P.read_bytes()), "mudados_no_sandbox": mudados, "raiz_mudou": raiz_mudou,
                                                          "o_lake_recompila": reconstruir + (["TGLExt (raiz)", "TGL.Audit"] if (mudados or raiz_mudou) else []),
                                                          "retirados": retirados}, ensure_ascii=False, indent=1))
# ---------------------------------------------------------------- o script do build (por modulo, na ordem topologica; para no primeiro que nao compilar)
lista = " ".join("TGLExt.%s" % x for x in ordem)
sh = """#!/bin/sh
# Constroi o kernel do SANDBOX da v412 (C:\\t\\k412c\\final; NUNCA o do Nos). Gerado por preparar_bundle_v412.py (claude-construtor-v412) em %(ts)s; nao editar a mao (regerar pelo preparo).
# Molde: v410\\construir_kernel_v410.sh. Diferenca: os %(n)d modulos novos sao construidos UM A UM, na ordem topologica das dependencias (`lake build +<modulo>`), e o script PARA no
# primeiro que nao compilar (marca `parou_em=` e nao roda o resto nem o Audit); so' depois vem o `lake build` inteiro (a raiz e o TGL.Audit) e o Audit (`lake env lean TGL/Audit.lean`).
# O build e' INCREMENTAL no que e' antigo (o kernel da v411 ja compilado em .lake/build, copiado do k411c) e A FRIO nos modulos novos. Marcas em kernel/construir_marcas.txt.
K="/c/t/k412c/final"
D="/c/IALD/Central de Patentes/work/cadeia_de_selo/v412/kernel"
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
""" % {"ts": TS, "n": len(ordem), "lista": lista}
grava_txt(PK / "construir_kernel_v412.sh", sh)
print("bundle:", len(ordem), "modulos | mudados no sandbox nesta rodada:", len(mudados), "| raiz mudou:", raiz_mudou, "| o lake recompila:", len(reconstruir), "modulos novos + raiz + Audit" if (mudados or raiz_mudou) else "(nada)")
print("ordem:", " ".join(ordem))
for x in ordem:
    e = entradas[x]
    print("  %-26s insumo %s -> instalado %s | #print axioms removidos %3d | imports trocados %d" % (x, e["sha16_insumo"], e["sha16"], e["n_print_axioms_removidos"], len(e["imports_trocados"])))
for r_ in retirados:
    print("  retirado (com backup):", r_["arquivo"], "->", r_["backup"])
