# -*- coding: utf-8 -*-
"""esperados_v413_foco.py -- (Etapa 3 da v413, construtor da Etapa 3 a servico da gerencia c1, 20/11/2026; molde: v412\\esperados_v412_foco.py)
os ESPERADOS da v413 LIDOS dos artefatos, para o rito (rito_v413.sh le candidato_sha16), o instalador, a reversao, o conferidor
pos-rito (conferir_pos_rito_v413_foco.py), os diffs e o compositor do handoff. Nada e' digitado: todo hash e todo numero vem de arquivo.

PARAMETRIZADO PELO CAMINHO DO CANDIDATO (a Etapa 2 gera o candidato): --candidato <caminho> (ou a variavel V413_CANDIDATO); sem isso, o caminho
e' lido do fecho da Etapa 2 (PREPARACAO_v413_PRONTA.json: candidato.caminho) ou do manifesto do candidato (CANDIDATO_v413.json: candidato).
Enquanto a Etapa 2 nao fechar, RECUSA com mensagem clara (saida 2) e nao grava nada.

Le (so' leitura): o candidato e o seu manifesto (CANDIDATO_v413.json), o fecho da Etapa 2 (PREPARACAO_v413_PRONTA.json), o portao do pilar NO
CANDIDATO (PORTAO_DO_PILAR_CANDIDATO_v413.json), o fecho da Etapa 1 (PRONTO_PARA_CANDIDATO_v413.json), a lista dos modulos novos e do corrigido
(kernel_modulos_novos_v413.json), o manifesto (insumos\\MANIFESTO_PEDRAS_v413.json), o bundle (BUNDLE_v413.json), as bandeiras (kernel\\FLAGS_v413.json),
o recibo do kernel (kernel\\KERNEL_RECIBO_v413.json), a cobertura (kernel\\KH_N1_v413.json), o sandbox C:\\t\\k413c\\final (as 22 fontes, a raiz e o
Audit), o Nos (a v412 selada: um.py, selo, core, a raiz, o Audit e o OResumoEPsiBit antigo), o contrato R2 (as cinco palavras de veredito), o
portao do pilar da Etapa 1 e os esperados da v412 (o pilar e os 156 modulos da v412). Confere tambem, no candidato: o kernel EMBUTIDO (as 21 fontes
novas e o OResumoEPsiBit corrigido com os bytes do bundle; a raiz igual a do sandbox), a linha unica UM_VERSION = "v413", as tres linhas da guarda
de palavra proibida do rito (uma vez cada) e as exigencias da custodia (o par _V413_FONTES/_V413_VERBATINS2 e o nome kh_n1_cobertura_v413).
Grava ESPERADOS_v413.json (backup de bytes do anterior; escrita por temporario).

ENSAIO (so' para os testes desta etapa): com V413_ENSAIO_DIR=<pasta>, o Nos e' <pasta>\\Nos, os insumos da Etapa 2 (CANDIDATO_v413.json,
PREPARACAO_v413_PRONTA.json, PORTAO_DO_PILAR_CANDIDATO_v413.json) sao lidos de <pasta> e a saida vai para <pasta>\\ESPERADOS_v413.json; o resto
(Etapa 1, sandbox, contrato, v412) e' o real, so' lido. Uso: esperados_v413_foco.py [--candidato <caminho>]"""
import ast, hashlib, json, os, re, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; V412 = V.parent / "v412"
NOS_REAL = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
ENSAIO = os.environ.get("V413_ENSAIO_DIR")
if ENSAIO:
    W = Path(ENSAIO).resolve(); assert W.is_dir() and W != V and os.path.normcase(str(W)).find(os.path.normcase(str(NOS_REAL))) < 0, "pasta de ensaio invalida"
    NOS = W / "Nós"; E2 = W
else:
    W = None; NOS = NOS_REAL; E2 = V
SB = Path(os.environ.get("V413_SANDBOX") or r"C:\t\k413c\final")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
shb = lambda b: hashlib.sha256(b).hexdigest()
lj = lambda p: json.loads(Path(p).read_text(encoding="utf-8"))


def recusa(msg, rc=2):
    print("RECUSO (esperados_v413_foco.py): " + msg)
    sys.exit(rc)


# ---------------------------------------------------------------- o candidato (parametrizado) e os insumos da Etapa 2
arg_c = None
if "--candidato" in sys.argv:
    i = sys.argv.index("--candidato"); arg_c = sys.argv[i + 1] if i + 1 < len(sys.argv) else None
arg_c = arg_c or os.environ.get("V413_CANDIDATO")
PREPP, CMP, PORP = E2 / "PREPARACAO_v413_PRONTA.json", E2 / "CANDIDATO_v413.json", E2 / "PORTAO_DO_PILAR_CANDIDATO_v413.json"
if not PREPP.is_file():
    recusa("a Etapa 2 ainda nao fechou: falta %s (o fecho da Etapa 2 traz o candidato; sem ele nao ha esperados)" % PREPP)
if not CMP.is_file():
    recusa("falta o manifesto do candidato %s (a Etapa 2 o grava junto do candidato)" % CMP)
PREP, CM = lj(PREPP), lj(CMP)
if PREP.get("fechou") is not True:
    recusa("o fecho da Etapa 2 (%s) nao diz fechou=true" % PREPP.name)
pc = PREP.get("candidato") if isinstance(PREP.get("candidato"), dict) else {}
cand_path = arg_c or pc.get("caminho") or CM.get("candidato")
if not cand_path:
    recusa("nenhum caminho do candidato: passe --candidato <caminho> (ou V413_CANDIDATO), ou o fecho da Etapa 2 tem de trazer candidato.caminho")
CAND = Path(cand_path)
if not CAND.is_file():
    recusa("o candidato nao existe no caminho dado: %s" % CAND)
craw = CAND.read_bytes(); c256 = shb(craw); c16 = c256[:16]
for nome, d in (("o manifesto do candidato (CANDIDATO_v413.json)", CM), ("o fecho da Etapa 2 (PREPARACAO_v413_PRONTA.json)", pc)):
    if d.get("sha16") is None or d.get("bytes") is None:
        recusa("%s nao traz sha16 e bytes do candidato" % nome)
    if d["sha16"] != c16 or int(d["bytes"]) != len(craw):
        recusa("%s nao e' deste candidato: diz %s/%s B, o disco tem %s/%d B" % (nome, d["sha16"], d["bytes"], c16, len(craw)))
if not PORP.is_file():
    recusa("falta o portao do pilar NO CANDIDATO (%s): a Etapa 2 o roda sobre o candidato" % PORP.name)
POR = lj(PORP)
if POR.get("ok") is not True or (POR.get("candidato") or {}).get("sha16") != c16:
    recusa("o portao do pilar no candidato nao passou ou nao e' deste candidato (%s)" % PORP.name)

# ---------------------------------------------------------------- a Etapa 1 (o kernel), lida
PK = lj(V / "PRONTO_PARA_CANDIDATO_v413.json"); assert PK.get("etapa_1_fechou") is True, "o fecho da Etapa 1 nao fechou"
KN = lj(V / "kernel_modulos_novos_v413.json"); MAN = lj(V / "insumos" / "MANIFESTO_PEDRAS_v413.json"); BU = lj(V / "BUNDLE_v413.json")
FJ = lj(V / "kernel" / "FLAGS_v413.json"); KR = lj(V / "kernel" / "KERNEL_RECIBO_v413.json"); KH = lj(V / "kernel" / "KH_N1_v413.json")
novos = list(KN["novos"]); NN = len(novos)
assert NN == len(set(novos)) == KN["n"] == MAN["n_modulos_novos"] == BU["n"] == len(BU["modulos"]) == KH["n_modulos_novos"] > 0, ("as listas dos modulos novos nao concordam", NN, KN["n"], MAN["n_modulos_novos"], BU["n"])
assert BU["manifesto_sha256"] == sha(V / "insumos" / "MANIFESTO_PEDRAS_v413.json"), "o bundle nao e' do manifesto do disco"
corr = list(KN.get("kernel_corrigido") or []); bkc = {x["rel"]: x for x in BU["kernel_corrigido"]}; krc = {x["path"]: x for x in KR["kernel_corrigido"]}
assert corr and set(corr) == set(bkc) == set(krc) == {"TGLExt/" + m.split(".", 1)[1] + ".lean" for m in MAN["kernel_corrigido"]}, ("o modulo corrigido nao concorda entre as listas", corr, sorted(bkc), sorted(krc))
bm = {x["rel"]: x for x in BU["modulos"]}; assert set(bm) == set(novos)
manmods = {"TGLExt/" + k.split(".", 1)[1] + ".lean": v for k, v in MAN["modulos_novos"].items()}; assert set(manmods) == set(novos), "o manifesto e a lista dos novos diferem"
bundle = {}
for rel in sorted(novos):
    x = bm[rel]; p = SB / Path(*rel.split("/"))
    assert x["sha256_insumo"] == manmods[rel]["sha256_pedra_limpa"], ("o insumo do bundle nao e' a pedra limpa do manifesto", rel)
    pl = Path(manmods[rel]["pedra_limpa"]); assert pl.is_file() and sha(pl) == manmods[rel]["sha256_pedra_limpa"], ("a pedra limpa do manifesto nao esta' no disco com o sha256 do manifesto", rel)
    assert p.is_file() and sha(p) == x["sha256"], ("o sandbox nao tem a fonte normalizada do bundle", rel)
    assert not (NOS / "tgl_kernel" / Path(*rel.split("/"))).exists(), ("um modulo novo ja' esta' no kernel do Nos", rel)
    bundle[rel] = x["sha256"]
kcorr = {}
for rel in sorted(corr):
    b_, k_ = bkc[rel], krc[rel]; mk = MAN["kernel_corrigido"]["TGLExt." + rel[len("TGLExt/"):-len(".lean")]]
    assert b_["sha256_origem"] == k_["sha256_antes"] == mk["sha256_origem"] and b_["sha256"] == k_["sha256_depois"] == mk["sha256_saida"], ("o antes/depois do corrigido nao concorda", rel)
    assert b_["sha256"] != b_["sha256_origem"] and b_.get("codigo_identico_a_origem") is True and mk.get("codigo_identico") is True, ("o corrigido nao muda so' o texto", rel)
    p = SB / Path(*rel.split("/")); assert p.is_file() and sha(p) == b_["sha256"], ("o sandbox nao tem o corrigido", rel)
    pn = NOS / "tgl_kernel" / Path(*rel.split("/")); assert pn.is_file() and sha(pn) == b_["sha256_origem"], ("o Nos nao tem o modulo antigo (v412) do corrigido", rel)
    kcorr[rel] = {"sha256_antes": b_["sha256_origem"], "sha256_depois": b_["sha256"], "bytes_depois": b_["bytes"], "declaracoes": list(k_["declaracoes"]),
                  "recibo_da_correcao": b_.get("recibo_da_correcao"), "recibo_da_correcao_sha256": b_.get("recibo_da_correcao_sha256")}
# a raiz e o Audit: antes (o Nos v412) e depois (o sandbox)
raiz_a, raiz_d = KR["raiz"]["sha256_antes"], KR["raiz"]["sha256_depois"]; aud_a, aud_d = KR["audit"]["sha256_antes"], KR["audit"]["sha256_depois"]
assert sha(NOS / "tgl_kernel" / "TGLExt.lean") == raiz_a and sha(NOS / "tgl_kernel" / "TGL" / "Audit.lean") == aud_a, "a raiz ou o Audit do Nos nao sao os da v412 selada (KERNEL_RECIBO_v413 antes)"
assert sha(SB / "TGLExt.lean") == raiz_d and sha(SB / "TGL" / "Audit.lean") == aud_d, "a raiz ou o Audit do sandbox nao sao os do recibo (depois)"
raiz_txt = (SB / "TGLExt.lean").read_text(encoding="utf-8")
assert all(("import TGLExt." + r[len("TGLExt/"):-len(".lean")]) in raiz_txt for r in novos), "a raiz do sandbox nao importa todos os novos"

# ---------------------------------------------------------------- a origem: a v412 selada no Nos
E412 = lj(V412 / "ESPERADOS_v412.json")
um0 = NOS / "um.py"; selo0 = lj(NOS / "um_absoluto_selo.json"); core0 = lj(NOS / "um_absoluto.json")["core"]
assert selo0["um_version"] == "v412" and selo0["sha256"]["um.py"] == sha(um0), "o selo do Nos nao e' o da v412 ou nao pina o um.py do disco"
assert sha(um0)[:16] == E412["candidato_sha16"], "o um.py do Nos nao e' o candidato selado da v412 (ESPERADOS_v412)"
o16 = sha(um0)[:16]
for k_ in ("base_v412_sha16", "base_sha16"):
    if CM.get(k_) is not None and CM[k_] != o16:
        recusa("o manifesto do candidato diz %s=%s, mas o Nos tem %s" % (k_, CM[k_], o16))
# os 156 modulos da v412 no Nos (o corrigido com o sha antigo) e as duas pedras anteriores a ela
b412 = dict(E412["bundle_sha256"]); mal412 = [r for r, s in b412.items() if not (NOS / "tgl_kernel" / Path(*r.split("/"))).is_file() or sha(NOS / "tgl_kernel" / Path(*r.split("/"))) != s]
assert not mal412, ("modulos da v412 ausentes ou diferentes no kernel do Nos", mal412[:5])
assert all(b412.get(r) == kcorr[r]["sha256_antes"] for r in kcorr), "o sha antigo do corrigido nao e' o da v412 selada"

# ---------------------------------------------------------------- a escada e as bandeiras
kf0 = core0["kernel_formalization"]; tr0 = sorted(k for k, v in kf0.items() if v is True)
lad0 = (core0.get("external_ladder") or {}).get("n_theorems_expected")
assert isinstance(lad0, int) and lad0 > 0, "a escada da v412 nao se leu do core (external_ladder)"
assert isinstance(FJ["flags"], list) and all(isinstance(f, list) and str(f[0]).startswith("ext_") for f in FJ["flags"])
chaves_novas = sorted(f[0] for f in FJ["flags"]); nb = len(chaves_novas)
assert nb == len(set(chaves_novas)) == FJ["n_flags"] == KH["n_bandeiras"] > 0, (nb, FJ["n_flags"], KH["n_bandeiras"])
assert not set(chaves_novas) & set(kf0), "uma chave de bandeira nova ja' existe no kernel_formalization da v412"
assert all(("_413_" in k) for k in chaves_novas), "bandeira nova fora do prefixo _413_ do contrato"
esc = [lad0, lad0 + nb]
for k_, alvo in (("escada", esc), ("n_bandeiras", nb)):
    if CM.get(k_) is not None and CM[k_] != alvo:
        recusa("o manifesto do candidato diz %s=%r; o lido (core da v412 + FLAGS_v413) e' %r" % (k_, CM[k_], alvo))
if (CM.get("kernel") or {}).get("modulos_novos") not in (None, NN):
    recusa("o manifesto do candidato diz kernel.modulos_novos=%r; a lista tem %d" % (CM["kernel"]["modulos_novos"], NN))
decl_novas = sorted({d for x in KR["pedras"] for d in x.get("declaracoes", [])} - {d for r in kcorr for d in kcorr[r]["declaracoes"]})

# ---------------------------------------------------------------- o contrato R2: as palavras de veredito dos registros (por script)
CT = V / "CONTRATO_v413_R2.md"; ctt = CT.read_text(encoding="utf-8"); assert (V / "contrato_REV2" / "CONTRATO_v413_R2.md").read_bytes() == CT.read_bytes(), "o contrato R2 difere da copia congelada"
s2 = re.search(r"^## 2\. .*?(?=^## 3\. )", ctt, re.M | re.S); assert s2, "secao 2 do contrato nao achada"
pal = dict(re.findall(r"^- `([a-z0-9_]+_v413)`[^\n]*\n  `([A-Z0-9_]+)`", s2.group(0), re.M))
assert pal and all(k.endswith("_v413") for k in pal), "nenhum registro da v413 lido do contrato"
for k_, w_ in pal.items():
    for proib in ("CONFIRMED", "PROVED_BY", "P_EQUALS_NP", "TURING_SOLVED", "CLAY_SOLVED", "MILLENNIUM"):
        assert not re.search(r"(?<!NOT_)(?<!UN)" + proib if proib == "CONFIRMED" else proib, w_), ("palavra proibida no veredito do contrato", k_, proib)

# ---------------------------------------------------------------- o candidato por dentro
ctxt = craw.decode("utf-8")
L = ctxt.splitlines(keepends=True)
i0 = [i for i, l in enumerate(L) if l.startswith("_EMBEDDED_KERNEL_FILES = {")]
assert len(i0) == 1, ("o candidato nao tem UMA linha _EMBEDDED_KERNEL_FILES", len(i0))
j = i0[0] + 1
while L[j].rstrip("\r\n") != "}":
    j += 1
EMB = ast.literal_eval("".join(L[i0[0]:j + 1]).split("=", 1)[1].strip())
mal_emb = [r for r in list(bundle) if r not in EMB or shb(EMB[r].encode("utf-8")) != bundle[r]] + [r for r in kcorr if r not in EMB or shb(EMB[r].encode("utf-8")) != kcorr[r]["sha256_depois"]]
assert not mal_emb, ("o kernel embutido no candidato nao tem os bytes do bundle", mal_emb[:5])
assert shb(EMB["TGLExt.lean"].encode("utf-8")) == raiz_d and shb(EMB["TGL/Audit.lean"].encode("utf-8")) == aud_d, "a raiz ou o Audit embutidos nao sao os do sandbox"
mal412e = [r for r, s in b412.items() if r not in kcorr and (r not in EMB or shb(EMB[r].encode("utf-8")) != s)]
assert not mal412e, ("um modulo da v412 mudou no kernel embutido (so' o corrigido pode mudar)", mal412e[:5])
uv = [l.strip() for l in L if l.startswith("UM_VERSION")]
assert len(uv) == 1 and re.match(r'^UM_VERSION = "v413"(\s|#|$)', uv[0]), ("a linha UM_VERSION do candidato nao e' a unica e com v413", uv)
GUARDA = ['if (re.search(r"(?<!NOT_)(?<!UN)CONFIRMED", _v)', 'or re.search(r"(?<!AP)PROVED_BY", _v)', 'or "TGL_PROVED" in _v or "CONSCIOUSNESS_PROVED" in _v):']
gcont = [ctxt.count(g) for g in GUARDA]; assert gcont == [1, 1, 1], ("a guarda de palavra proibida do rito nao esta' uma vez no candidato", gcont)
exig = {"par_V413_FONTES": bool(re.search(r"^_V413_FONTES\s*=", ctxt, re.M)), "par_V413_VERBATINS2": bool(re.search(r"^_V413_VERBATINS2\s*=", ctxt, re.M)),
        "kh_n1_cobertura_v413": "kh_n1_cobertura_v413" in ctxt}
exig["todas"] = all(exig.values())

# ---------------------------------------------------------------- o pilar: o mesmo resultado da v412, pelo cache; o ambiente do cache (para o portao do rito)
POR1 = lj(V / "PORTAO_DO_PILAR_v413.json")
pil = dict(E412["pilar"]); cdir = NOS_REAL.parent / "cache" / "checkpoints" / "quantum_pillar" / pil["key"]
rj = cdir / "result.json"; assert sha(rj) == pil["result_sha256"] == (cdir / "result.json.sha256").read_text(encoding="ascii").strip(), "o cache do pilar nao guarda o resultado da v412"
assert pil["key"] in (POR1.get("estado_lido") or {}).get("chaves_no_stdout_v412", []), "a chave do pilar nao e' a que o rito da v412 leu"
cenv = lj(rj).get("env") or {}; env_cache = {k: cenv.get(k) for k in ("torch", "cuda", "numpy", "scipy", "python", "gpu")}
assert all(env_cache.values()), ("o ambiente do cache esta' incompleto", env_cache)

# ---------------------------------------------------------------- pre-condicoes de processo que o instalador confere (so' registradas aqui)
topo = E2 / "TOPO_RATIFICADO_v413_DERIVADO.json"; pino_pre = E2 / "PINO_RECIBO_PRE_SELO_v413.json"
pre = None
if pino_pre.is_file():
    pp = lj(pino_pre)
    pre = {"path": str(pino_pre), "sha16": sha(pino_pre)[:16], "contrato": pp.get("contrato"), "utilizavel": pp.get("utilizavel_como_recibo_pre_selo_do_B_n"),
           "versao_nos": pp.get("versao_nos"), "um_py_sha16_do_nos": pp.get("um_py_sha16_do_nos"), "veredito": pp.get("veredito")}
esp = {
    "gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "gerador": "esperados_v413_foco.py", "ensaio": bool(ENSAIO), "ensaio_dir": str(W) if W else None,
    "nota": "esperados da v413 (Etapa 3; molde v412\\esperados_v412_foco.py): o rito le candidato_sha16; o instalador, a reversao, o conferidor, os diffs e o compositor leem o resto; tudo lido",
    "versao": "v413", "versao_anterior": "v412", "um_version_esperada": "v413",
    "candidato": {"caminho": str(CAND), "sha16": c16, "sha256": c256, "bytes": len(craw), "manifesto": str(CMP), "manifesto_sha16": sha(CMP)[:16], "fecho_etapa2": str(PREPP), "fecho_etapa2_sha16": sha(PREPP)[:16]},
    "candidato_sha16": c16, "candidato_sha256": c256, "candidato_bytes": len(craw),
    "origem_sha16": o16,
    "base_v412": {"um_py_sha256": sha(um0), "selo_sha256": sha(NOS / "um_absoluto_selo.json"), "core_sha256": sha(NOS / "um_absoluto.json"), "selo_timestamp": selo0.get("timestamp")},
    "gate_verdict_v412": selo0["qg_closure_verdict"],
    "escada": esc, "n_bandeiras_novas": nb, "n_bandeiras_true_v412": len(tr0), "bandeiras_novas_chaves": chaves_novas, "flags_sha16": sha(V / "kernel" / "FLAGS_v413.json")[:16],
    "kernel": {"modulos_novos": NN, "raiz_antes_sha256": raiz_a, "raiz_antes_sha16": raiz_a[:16], "audit_antes_sha256": aud_a, "audit_antes_sha16": aud_a[:16],
               "raiz_depois_sha256": raiz_d, "raiz_depois_sha16": raiz_d[:16], "audit_depois_sha256": aud_d, "audit_depois_sha16": aud_d[:16],
               "pronto_kernel_sha16": sha(V / "PRONTO_PARA_CANDIDATO_v413.json")[:16], "kernel_recibo_sha16": sha(V / "kernel" / "KERNEL_RECIBO_v413.json")[:16],
               "kh_decl": KH["linha_TOTAL"]["decl"], "kh_thm": KH["linha_TOTAL"]["thm"], "kh_decl_v412": KH["linha_TOTAL_v412"]["decl"], "kh_thm_v412": KH["linha_TOTAL_v412"]["thm"],
               "declaracoes_novas": decl_novas, "n_declaracoes_novas": len(decl_novas), "embutido_confere": True, "n_embutidos": len(EMB)},
    "bundle_sha256": bundle, "bundle_nota": "sha256 da fonte NORMALIZADA dos novos (a que o candidato embute e o rito materializa no Nos); cada uma ligada a' pedra limpa do manifesto (sha256_insumo == sha256_pedra_limpa, conferido aqui) por BUNDLE_v413.json",
    "manifesto_pedra_limpa_sha256": {rel: manmods[rel]["sha256_pedra_limpa"] for rel in sorted(novos)},
    "kernel_corrigido": kcorr, "kernel_corrigido_nota": "o modulo que EXISTE no Nos e e' SUBSTITUIDO (so' a docstring; codigo identico): o instalador confere o sha antigo e guarda os bytes; a reversao o devolve; o conferidor exige o sha novo",
    "bundle_recibo_sha16": sha(V / "BUNDLE_v413.json")[:16], "manifesto_sha16": sha(V / "insumos" / "MANIFESTO_PEDRAS_v413.json")[:16],
    "modulos_v412_sha256": b412, "pedras_v411_e_antes_sha256": E412["bundle_pedras_anteriores_sha256"],
    "registros_v413": pal, "registros_do_candidato": CM.get("registros"),
    "contrato": {"arquivo": CT.name, "sha16": sha(CT)[:16]},
    "pilar": dict(pil, env_do_cache=env_cache, cache_dir=str(cdir), portao_v413_sha16=sha(V / "PORTAO_DO_PILAR_v413.json")[:16], portao_candidato_sha16=sha(PORP)[:16]),
    "exigencias_da_custodia": exig,
    "guarda_do_rito": {"linhas": GUARDA, "contagem_no_candidato": gcont},
    "topo_derivado": {"path": str(topo), "existe": topo.is_file(), "sha16": sha(topo)[:16] if topo.is_file() else None},
    "pre_selo_bn": pre,
    "troca_dita": {"regra": "um veredito herdado da v412 so' pode mudar nos numeros: trocando os hashes hexadecimais e os numeros por marcadores neutros, fica identico ao da v412",
                   "escada": esc, "hashes": [o16, c16]},
}
out = (W or V) / "ESPERADOS_v413.json"
if out.exists():
    bak = out.with_name(out.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")); bak.write_bytes(out.read_bytes()); assert bak.read_bytes() == out.read_bytes()
b = json.dumps(esp, ensure_ascii=False, indent=1).encode("utf-8"); tmp = out.with_name(out.name + ".tmp_e3"); tmp.write_bytes(b); assert tmp.stat().st_size == len(b); tmp.replace(out)
print("ESPERADOS_v413.json%s | candidato %s (%d B) | origem %s | escada %s | novos %d + corrigido %d | raiz %s -> %s | audit %s -> %s | exigencias da custodia %s | sha16 %s" % (
    " [ENSAIO]" if ENSAIO else "", c16, len(craw), o16, esc, NN, len(kcorr), raiz_a[:16], raiz_d[:16], aud_a[:16], aud_d[:16], "OK" if exig["todas"] else "FALTAM %s" % [k for k, v in exig.items() if not v], shb(b)[:16]))
