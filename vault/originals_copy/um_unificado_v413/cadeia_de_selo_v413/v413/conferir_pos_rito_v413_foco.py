# -*- coding: utf-8 -*-
"""conferir_pos_rito_v413_foco.py -- (Etapa 3 da v413, 20/11/2026; molde: v412\\conferir_pos_rito_v412_foco.py) confere, DEPOIS do rito v413,
SO' LENDO o Nos, o que tinha de mudar e o que nao podia, contra o estado SELADO da v412 (os backups que o instalador gravou, lidos pelo
APLICADO_AO_CANONICO_<ts>.json mais novo) e o ESPERADOS_v413.json (esperados_v413_foco.py). Autocontido (licao v411: nenhuma dependencia de arquivo
alem dos que le). Grava CONFERENCIA_POS_RITO_v413_FOCO.json. Saida 0 so' se TUDO bater. Checagens:
 1. o stdout: termina com RITO_RC=0; a linha do kernel (lake build: True) e a escada de depois («teoremas limpos: B/B»); o autoteste do fail-closed
    PASSOU; nenhum SEAL_WITHHELD; o pilar REAPROVEITADO com a chave do cache e nenhuma linha de calculo do pilar; o um.py do Nos e' o candidato;
 2. o selo: existe; um_version v413; sha256/um.py == o do arquivo; todo arquivo que o selo pina bate; o veredito do gate == o da v412; nada formal
    sem selar e as recusas de dado iguais as da v412;
 3. NADA DA v412 PERDIDO: todo registro com veredito do core da v412 existe no core novo com o MESMO veredito, salvo a troca dita (hashes e numeros
    por marcadores neutros); toda chave do selo da v412 existe no selo novo;
 4. os registros novos do contrato R2 existem com a palavra de veredito do contrato, all_verified; os registros novos do core sao exatamente os do
    contrato (mais o kh_n1_cobertura_v413 da custodia; blocos sem veredito ficam ditos a parte), como o C1 da G1 os compara;
 5. a GUARDA DE PALAVRA PROIBIDA DO RITO, lida do candidato (as tres linhas, uma vez cada), aplicada a TODO veredito do core; e, nos vereditos novos,
    as palavras que a ordem da Etapa 3 proibe;
 6. as bandeiras: todas as True da v412 seguem True; as novas == as chaves do FLAGS_v413.json; o estatuto da prova traz a escada de depois;
 7. o relatorio de axiomas: nenhum sorryAx e nada fora do trio; as declaracoes novas e as do corrigido estao nele; a cobertura KH (o registro kh mais
    novo) == as declaracoes auditadas == as do KH_N1 medido no sandbox (a regua do C1 da G1);
 8. o kernel do Nos: os modulos novos com o sha256 do bundle; o CORRIGIDO com o sha256 novo; os outros modulos da v412 com o sha256 de antes; a raiz e
    o Audit com o sha256 do sandbox; a raiz importa os novos.
ENSAIO: V413_ENSAIO_DIR=<pasta> (o Nos e' <pasta>\\Nos; ESPERADOS, CANDIDATO e registro de <pasta>); o recibo vai a <pasta>."""
import glob, hashlib, json, os, re, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
NOS_REAL = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
ENSAIO = os.environ.get("V413_ENSAIO_DIR")
if ENSAIO:
    W = Path(ENSAIO).resolve(); NOS, REG, E2 = W / "Nós", W / "registro", W
else:
    W = None; NOS, REG, E2 = NOS_REAL, V, V
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
lj = lambda p: json.loads(Path(p).read_text(encoding="utf-8"))
ESP = lj(E2 / "ESPERADOS_v413.json"); assert ESP.get("gerador") == "esperados_v413_foco.py" and bool(ESP.get("ensaio")) == bool(ENSAIO)
ap = [os.environ["V413_APLICADO"]] if os.environ.get("V413_APLICADO") else sorted(glob.glob(str(REG / "APLICADO_AO_CANONICO_*.json"))); assert ap, "nenhum APLICADO_AO_CANONICO_*.json"
AP = lj(ap[-1]); B = AP["backups"]
linhas = []; ok_total = True


def chk(nome, cond, detalhe=None):
    global ok_total
    ok_total = ok_total and bool(cond); linhas.append({"checagem": nome, "ok": bool(cond), "detalhe": detalhe})
    print(("ok    " if cond else "FALHOU"), nome, "" if cond else str(detalhe)[:600])


# a v412 selada: dos backups do instalador (o estado que estava no Nos antes do rito)
selo0 = lj(B["um_absoluto_selo.json"]["backup"]); core0 = lj(B["um_absoluto.json"]["backup"])["core"]
assert sha(B["um.py"]["backup"])[:16] == ESP["origem_sha16"] and B["um_absoluto_selo.json"]["sha256"] == ESP["base_v412"]["selo_sha256"], "os backups nao sao a v412 selada"
um1 = NOS / "um.py"; selo_p = NOS / "um_absoluto_selo.json"
# 1. o stdout e o um.py
so_b = (NOS / "rodada_v413_stdout.txt").read_bytes(); so = so_b.decode("utf-8", "replace"); sol = so.rstrip().split("\n")
chk("o stdout do rito termina com RITO_RC=0", sol and sol[-1].strip() == "RITO_RC=0", sol[-3:] if sol else None)
A_, B_ = ESP["escada"]
esc_so = re.findall(r"teoremas limpos: (\d+)/(\d+)", so)
chk("a escada de depois no stdout (teoremas limpos: %d/%d)" % (B_, B_), bool(esc_so) and esc_so[0] == (str(B_), str(B_)), esc_so[:3])
chk("o lake build do rito passou (lake build: True) e a verificacao do kernel nao saiu FAILED na rodada principal", "lake build: True" in so and ">>> TGL_KERNEL_STAGE1_VERIFIED" in so, [l for l in sol if "lake build:" in l][:2])
chk("o autoteste do fail-closed PASSOU e nenhum selo foi retido (SEAL_WITHHELD)", ">>> FAIL_CLOSED_SELFTEST_PASSED <<<" in so and "SEAL_WITHHELD" not in so, [l for l in sol if "SEAL_WITHHELD" in l or "SELFTEST" in l][:3])
m_reuso = re.findall(r"pilar quantico: REAPROVEITADO da rodada[^\n]*\(chave ([0-9a-f]{24})\)", so)
chk("o pilar foi REAPROVEITADO pela chave do cache (%s) e nao houve linha de calculo" % ESP["pilar"]["key"], m_reuso == [ESP["pilar"]["key"]] and "pilar quantico: o trabalhador da GPU foi lancado" not in so, m_reuso)
chk("o um.py do Nos e' o candidato (sha16 e bytes)", sha(um1)[:16] == ESP["candidato_sha16"] and um1.stat().st_size == ESP["candidato_bytes"], (sha(um1)[:16], um1.stat().st_size))
# 2. o selo
chk("o selo existe (nao foi retido)", selo_p.is_file(), str(selo_p))
selo1 = lj(selo_p) if selo_p.is_file() else {}
R1 = lj(NOS / "um_absoluto.json"); core1 = R1["core"]
chk("o selo novo diz um_version v413", selo1.get("um_version") == "v413", selo1.get("um_version"))
chk("o selo novo pina o um.py do disco (sha256/um.py)", (selo1.get("sha256") or {}).get("um.py") == sha(um1), (selo1.get("sha256") or {}).get("um.py"))
mal_sel = [k for k, h in (selo1.get("sha256") or {}).items() if not (NOS / k).is_file() or sha(NOS / k) != h]
chk("todo arquivo que o selo novo pina bate com o disco (%d)" % len(selo1.get("sha256") or {}), not mal_sel and set(selo1.get("sha256") or {}) == set(selo0["sha256"]), {"divergem": mal_sel, "conjunto_igual_ao_da_v412": set(selo1.get("sha256") or {}) == set(selo0["sha256"])})
chk("o veredito do gate e' o da v412 (o gate nao se move)", selo1.get("qg_closure_verdict") == selo0.get("qg_closure_verdict") == ESP["gate_verdict_v412"], selo1.get("qg_closure_verdict"))
ns0, ns1 = selo0.get("not_sealed_this_run") or {}, selo1.get("not_sealed_this_run") or {}
chk("nada formal sem selar; as recusas de dado iguais as da v412", (ns1.get("formais") or []) == [] and sorted(ns1.get("recusas_de_dado") or []) == sorted(ns0.get("recusas_de_dado") or []),
    {"formais": ns1.get("formais"), "recusas": ns1.get("recusas_de_dado")})
chk("o selo registra o autoteste PASSED", selo1.get("fail_closed_selftest") == "FAIL_CLOSED_SELFTEST_PASSED", selo1.get("fail_closed_selftest"))
# 3. nada da v412 perdido


def neutro(v):   # (a regra do ensaio a seco: os vizinhos so' mudam numeros) hashes hexadecimais e numeros viram marcadores neutros
    return re.sub(r"\d+", "<N>", re.sub(r"[0-9a-f]{16,64}", "<H>", str(v)))


reg0 = {k: m["verdict"] for k, m in core0.items() if isinstance(m, dict) and m.get("verdict")}
faltam = [k for k in reg0 if not (isinstance(core1.get(k), dict) and core1[k].get("verdict"))]
mudaram = {k: (reg0[k][:120], str(core1[k]["verdict"])[:120]) for k in reg0 if k not in faltam and core1[k]["verdict"] != reg0[k]}
fora_da_troca = {k: v for k, v in mudaram.items() if neutro(core1[k]["verdict"]) != neutro(reg0[k])}
chk("nenhum registro com veredito da v412 sumiu do core (%d herdados)" % len(reg0), not faltam, faltam[:10])
chk("nenhum veredito herdado mudou fora da troca dita (escada e hash do um.py); mudaram pela troca dita: %d" % (len(mudaram) - len(fora_da_troca)), not fora_da_troca, fora_da_troca)
sk_falta = [k for k in selo0 if k not in selo1]
chk("toda chave do selo da v412 existe no selo novo (%d)" % len(selo0), not sk_falta, sk_falta[:10])
# 4. os registros novos
pal = ESP["registros_v413"]
reg_ruins = {n: (core1.get(n) or {}).get("verdict") for n, w in pal.items() if (core1.get(n) or {}).get("verdict") != w}
chk("os %d registros do contrato R2 existem com a palavra de veredito do contrato" % len(pal), not reg_ruins, reg_ruins)
nao_ver = [n for n in pal if (core1.get(n) or {}).get("all_verified") is not True]
chk("os registros do contrato estao all_verified", not nao_ver, nao_ver)
novos_core = sorted(k for k in core1 if k not in core0 and isinstance(core1[k], dict) and core1[k].get("verdict"))
aux_core = sorted(k for k in core1 if k not in core0 and isinstance(core1[k], dict) and "verdict" not in core1[k])
esperados_reg = set(pal) | ({"kh_n1_cobertura_v413"} if (ESP.get("exigencias_da_custodia") or {}).get("kh_n1_cobertura_v413") else set())
chk("os registros novos do core sao exatamente os do contrato (mais o kh_n1_cobertura_v413 da custodia): a regua do C1 da G1", set(novos_core) == esperados_reg,
    {"a_mais": sorted(set(novos_core) - esperados_reg), "faltam": sorted(esperados_reg - set(novos_core)), "blocos_sem_veredito": aux_core})
# 5. a guarda de palavra proibida do rito (lida do candidato) e as palavras da ordem
utxt = um1.read_bytes().decode("utf-8", "replace")
G = ESP["guarda_do_rito"]["linhas"]
chk("as tres linhas da guarda do rito estao no um.py do Nos, uma vez cada", [utxt.count(g) for g in G] == [1, 1, 1], [utxt.count(g) for g in G])
proib_rito = [k for k, m in core1.items() if isinstance(m, dict) and (re.search(r"(?<!NOT_)(?<!UN)CONFIRMED", str(m.get("verdict") or "")) or re.search(r"(?<!AP)PROVED_BY", str(m.get("verdict") or ""))
                                                                       or "TGL_PROVED" in str(m.get("verdict") or "") or "CONSCIOUSNESS_PROVED" in str(m.get("verdict") or ""))]
chk("nenhum veredito do core cai na guarda de palavra proibida do rito (a mesma regex, sem excecao)", not proib_rito, proib_rito[:10])
PROIB = ("P_EQUALS_NP", "TURING_SOLVED", "CLAY_SOLVED", "MILLENNIUM")
proib_novos = [k for k in novos_core if any(w in str(core1[k]["verdict"]) for w in PROIB)]
chk("nenhum veredito novo traz as palavras que a ordem proibe (%s)" % ", ".join(PROIB), not proib_novos, proib_novos)
# 6. as bandeiras
kf0, kf1 = core0["kernel_formalization"], core1["kernel_formalization"]
t0 = {k for k, v in kf0.items() if v is True}; t1 = {k for k, v in kf1.items() if v is True}
caiu = sorted(t0 - t1)
chk("todas as bandeiras True da v412 seguem True (%d)" % len(t0), not caiu and len(t0) == ESP["n_bandeiras_true_v412"], {"caiu": caiu[:10], "true_v412": len(t0)})
novas = t1 - t0; esperadas = set(ESP["bandeiras_novas_chaves"])
chk("as bandeiras True novas sao exatamente as %d chaves do FLAGS_v413.json (nem mais, nem menos)" % len(esperadas), novas == esperadas and len(esperadas) == ESP["n_bandeiras_novas"],
    {"novas": len(novas), "esperadas": len(esperadas), "a_mais": sorted(novas - esperadas)[:5], "faltam": sorted(esperadas - novas)[:5]})
_est = str((core1.get("estatuto_da_prova_v391") or {}).get("verdict"))
chk("o veredito do estatuto da prova traz a escada de depois (%d) e nao a de antes (%d)" % (B_, A_), str(B_) in _est and str(A_) not in _est, _est[:200])
# 7. os axiomas e a cobertura
TRIO = {"propext", "Classical.choice", "Quot.sound"}
ax1 = kf1.get("axiom_report") or {}
fora = [(k, sorted(set(v) - TRIO)[:3]) for k, v in ax1.items() if isinstance(v, list) and set(x for x in v if isinstance(x, str)) - TRIO]
com_sorry = [k for k, v in ax1.items() if "sorryAx" in json.dumps(v)]
chk("o relatorio de axiomas nao tem sorryAx (%d entradas)" % len(ax1), not com_sorry, com_sorry[:10])
chk("nenhuma entrada do relatorio de axiomas fora do trio", not fora, fora[:10])
dn = ESP["kernel"]["declaracoes_novas"]; dc = [d for r in ESP["kernel_corrigido"].values() for d in r["declaracoes"]]
falta_ax = [d for d in dn + dc if d not in ax1]
chk("as %d declaracoes novas e as %d do corrigido estao no relatorio de axiomas" % (len(dn), len(dc)), not falta_ax, falta_ax[:10])
kh = sorted((k for k in core1 if re.fullmatch(r"kh_n1_cobertura_v\d+", k)), key=lambda k: int(k.rsplit("v", 1)[1]))
khl = ((core1.get(kh[-1]) or {}).get("lido") or {}) if kh else {}
chk("a cobertura KH (o registro kh mais novo, %s) == as declaracoes auditadas == o medido no sandbox (%d/%d)" % (kh[-1] if kh else None, ESP["kernel"]["kh_decl"], ESP["kernel"]["kh_thm"]),
    bool(kh) and int(khl.get("constantes_cobertas", -1)) == len(ax1) == ESP["kernel"]["kh_decl"] and int(khl.get("teoremas_cobertos", -1)) == ESP["kernel"]["kh_thm"],
    {"registro": kh[-1] if kh else None, "lido": khl, "axiom_report": len(ax1)})
# 8. o kernel do Nos
K = NOS / "tgl_kernel"
mal = [rel for rel, s in ESP["bundle_sha256"].items() if not (K / Path(*rel.split("/"))).is_file() or sha(K / Path(*rel.split("/"))) != s]
chk("os %d modulos novos estao no kernel do Nos com o sha256 do bundle" % len(ESP["bundle_sha256"]), not mal, mal[:10])
malc = [rel for rel, x in ESP["kernel_corrigido"].items() if not (K / Path(*rel.split("/"))).is_file() or sha(K / Path(*rel.split("/"))) != x["sha256_depois"]]
chk("o modulo CORRIGIDO esta' no Nos com o sha256 novo (%s)" % ", ".join(sorted(ESP["kernel_corrigido"])), not malc, malc)
mal412 = [rel for rel, s in ESP["modulos_v412_sha256"].items() if rel not in ESP["kernel_corrigido"] and (not (K / Path(*rel.split("/"))).is_file() or sha(K / Path(*rel.split("/"))) != s)]
chk("os outros modulos da v412 seguem com o sha256 de antes (%d)" % (len(ESP["modulos_v412_sha256"]) - len(ESP["kernel_corrigido"])), not mal412, mal412[:10])
chk("a raiz TGLExt.lean e o TGL/Audit.lean do Nos sao os do sandbox (depois)", sha(K / "TGLExt.lean") == ESP["kernel"]["raiz_depois_sha256"] and sha(K / "TGL" / "Audit.lean") == ESP["kernel"]["audit_depois_sha256"],
    (sha(K / "TGLExt.lean")[:16], sha(K / "TGL" / "Audit.lean")[:16]))
raiz = (K / "TGLExt.lean").read_text(encoding="utf-8")
sem_import = [rel for rel in ESP["bundle_sha256"] if ("import TGLExt." + rel[len("TGLExt/"):-len(".lean")]) not in raiz]
chk("a raiz TGLExt.lean do Nos importa os %d novos" % len(ESP["bundle_sha256"]), not sem_import, sem_import[:10])
man1 = NOS / "tgl_kernel_proof_manifest.json"; fm1 = lj(man1).get("formal_files_sha256") or {}
malm = [r for r in list(ESP["bundle_sha256"]) + list(ESP["kernel_corrigido"]) if fm1.get(r) != (ESP["bundle_sha256"].get(r) or ESP["kernel_corrigido"].get(r, {}).get("sha256_depois"))]
chk("o manifesto do kernel novo pina os novos e o corrigido com os sha256 esperados", not malm, malm[:10])
rec = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "ok": ok_total, "ensaio": bool(ENSAIO), "aplicado": os.path.basename(ap[-1]), "esperados_sha16": sha(E2 / "ESPERADOS_v413.json")[:16],
       "selo_sha16": sha(selo_p)[:16] if selo_p.is_file() else None, "um_py_sha16": sha(um1)[:16], "stdout_sha16": hashlib.sha256(so_b).hexdigest()[:16], "checagens": linhas,
       "registros_novos_do_core": novos_core, "blocos_sem_veredito_novos": aux_core,
       "nota": "conferidor da v413 (Etapa 3; molde: o conferidor enxuto da v412), so' leitura do Nos; validade no kernel nao e' creditacao; o gate nao se move"}
out = (W or V) / ("CONFERENCIA_POS_RITO_v413_FOCO.json" if not ENSAIO else "CONFERENCIA_POS_RITO_v413_FOCO_ENSAIO.json")
if out.exists():
    out.with_name(out.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(out.read_bytes())
tmp = out.with_name(out.name + ".tmp_e3"); tmp.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8"); tmp.replace(out)
print("CONFERENCIA POS-RITO v413%s:" % (" [ENSAIO]" if ENSAIO else ""), "TUDO BATE" if ok_total else "ALGO NAO BATE", "| checagens", len(linhas), "| ok", sum(1 for l in linhas if l["ok"]))
sys.exit(0 if ok_total else 1)
