# -*- coding: utf-8 -*-
"""esperados_v412_foco.py -- (gerencia c1, 18/11/2026, Etapa 3 ENXUTA: PLANO_ETAPA3_ENXUTA_v412.md) os ESPERADOS da v412 LIDOS dos
artefatos, para o rito (rito_v412.sh le candidato_sha16), o instalador, a reversao e o conferidor enxuto (conferir_pos_rito_v412_foco.py).
Substitui, nesta versao, o gerar_esperados_v412.py herdado da v411 (versao sem modulo novo), que segue marcado [A ADAPTAR v412] e nao roda.
A v412 TEM modulo novo: 156 fontes da lista R12 (insumos\\MANIFESTO_PEDRAS_v412_R12.json), 5478 bandeiras novas, cinco registros novos.
So' le: o candidato e o seu manifesto (CANDIDATO_v412.json), o fecho do kernel (PRONTO_PARA_CANDIDATO_v412_R7.json), a lista dos
modulos novos (kernel_modulos_novos_v412.json), o manifesto R12, o sandbox C:\\t\\k412c\\final (a raiz, o Audit e os 156), o Nos (o um.py,
o selo e o core da v411 selada, a raiz e o Audit do kernel), o contrato R11 (as palavras de veredito), o portao do pilar e os esperados da
v411 (o pilar). Grava ESPERADOS_v412.json (backup de bytes do anterior, se houver)."""
import hashlib, json, os, re, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"); SB = Path(r"C:\t\k412c\final")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
lj = lambda p: json.loads(Path(p).read_text(encoding="utf-8"))
CM = lj(V / "CANDIDATO_v412.json"); PK = lj(V / "PRONTO_PARA_CANDIDATO_v412_R7.json"); KN = lj(V / "kernel_modulos_novos_v412.json")
M12 = lj(V / "insumos" / "MANIFESTO_PEDRAS_v412_R12.json"); E411 = lj(V.parent / "v411" / "ESPERADOS_v411.json"); POR = lj(V / "PORTAO_DO_PILAR_CANDIDATO_v412.json")
cand = V / "um_v412_candidato.py"
assert sha(cand)[:16] == CM["sha16"] and cand.stat().st_size == CM["bytes"], "o candidato do disco nao e' o do CANDIDATO_v412.json"
assert PK.get("kernel_fechou") is True, "o fecho do kernel nao fechou"
# a origem: a v411 selada no Nos
um0 = NOS / "um.py"; selo0 = lj(NOS / "um_absoluto_selo.json"); core0 = lj(NOS / "um_absoluto.json")["core"]
assert sha(um0)[:16] == CM["base_v411_sha16"] == E411["candidato_sha16"], "o Nos nao tem a v411 selada"
assert selo0["um_version"] == "v411" and selo0["sha256"]["um.py"] == sha(um0), "o selo do Nos nao e' o da v411 ou nao pina o um.py do disco"
# os modulos novos: a lista do construtor == o manifesto R12 == o sandbox
novos = list(KN["novos"]); assert len(novos) == len(set(novos)) == KN["n"] == 156 == M12["n_modulos"], (len(novos), KN["n"], M12["n_modulos"])
man = {"TGLExt/" + x["modulo"] + ".lean": x["sha256"] for x in M12["modulos"]}
assert set(man) == set(novos), ("a lista dos modulos novos difere do manifesto R12", sorted(set(man) ^ set(novos))[:5])
# a fonte que o sandbox e o candidato embutem e' a NORMALIZADA (BUNDLE_v412.json: import de candidata irma -> import TGLExt.<Nome>; as linhas
# #print axioms saem); o recibo do bundle liga cada uma a' fonte crua da lista (sha256_insumo == o do manifesto R12)
BU = lj(V / "BUNDLE_v412.json"); assert BU["manifesto_sha256"] == sha(V / "insumos" / "MANIFESTO_PEDRAS_v412_R12.json") and BU["n"] == 156
bm = {x["rel"]: x for x in BU["modulos"]}; assert set(bm) == set(novos)
bundle = {}
for rel in sorted(novos):
    x = bm[rel]; p = SB / Path(*rel.split("/"))
    assert x["sha256_insumo"] == man[rel], ("o insumo do bundle nao e' a fonte do manifesto R12", rel)
    assert p.is_file() and sha(p) == x["sha256"], ("o sandbox nao tem a fonte normalizada do bundle", rel)
    assert not (NOS / "tgl_kernel" / Path(*rel.split("/"))).exists(), ("um modulo novo ja' esta' no kernel do Nos", rel)
    bundle[rel] = x["sha256"]
# a escada e as bandeiras
esc = list(CM["escada"]); assert len(esc) == 2 and esc[1] - esc[0] == CM["n_bandeiras"] > 0, (esc, CM["n_bandeiras"])
kf0 = core0["kernel_formalization"]; tr0 = sorted(k for k, v in kf0.items() if v is True)   # (as True do kernel_formalization nao sao so' a escada: ha' chaves de estado tambem)
FJ = lj(V / "kernel" / "FLAGS_v412.json")
assert isinstance(FJ["flags"], list) and all(isinstance(f, list) and str(f[0]).startswith("ext_") for f in FJ["flags"]), "FLAGS_v412.json[flags] nao e' a lista [chave, declaracao, modulo, origem]"
chaves_novas = sorted(f[0] for f in FJ["flags"]); assert len(chaves_novas) == len(set(chaves_novas)) == FJ["n_flags"] == CM["n_bandeiras"], (len(chaves_novas), FJ["n_flags"], CM["n_bandeiras"])
assert not set(chaves_novas) & set(kf0), "uma chave de bandeira nova ja' existe no kernel_formalization da v411"
# as cinco palavras de veredito do contrato R11
c11 = (V / "CONTRATO_v412_R11.md").read_text(encoding="utf-8")
NOMES = ["iald_camada_cientifica_v412", "leitor_da_formula_v412", "matematica_que_restava_v412", "parede_do_teste_cego_v412", "cunhagens_v412"]
pal = {}
for n in NOMES:
    a = re.findall(r"^- `%s`\n  `([A-Z0-9_]+)`" % n, c11, re.M); assert len(a) == 1, (n, len(a)); pal[n] = a[0]
# o pilar: o mesmo resultado da v411, conferido pelo portao do pilar sobre ESTE candidato
assert POR.get("ok") is True and POR["candidato"]["sha16"] == CM["sha16"], "o portao do pilar nao e' deste candidato ou nao passou"
cdir = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\checkpoints\quantum_pillar") / E411["pilar"]["key"]
assert sha(cdir / "result.json") == E411["pilar"]["result_sha256"], "o cache do pilar nao guarda o resultado da v411"
esp = {
    "gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "gerador": "esperados_v412_foco.py",
    "nota": "esperados ENXUTOS da v412 (Etapa 3 enxuta; PLANO_ETAPA3_ENXUTA_v412.md): o rito le candidato_sha16; o instalador, a reversao e o conferidor enxuto leem o resto; o gerar_esperados_v412.py herdado (v411, sem modulo novo) nao roda",
    "versao": "v412", "um_version_esperada": "v412",
    "candidato_sha16": CM["sha16"], "candidato_sha256": CM["sha256"], "candidato_bytes": CM["bytes"],
    "origem_sha16": CM["base_v411_sha16"],
    "base_v411": {"um_py_sha256": sha(um0), "selo_sha256": sha(NOS / "um_absoluto_selo.json"), "core_sha256": sha(NOS / "um_absoluto.json"), "selo_timestamp": selo0.get("timestamp")},
    "gate_verdict_v411": selo0["qg_closure_verdict"],
    "escada": esc, "n_bandeiras_novas": CM["n_bandeiras"], "n_bandeiras_true_v411": len(tr0), "bandeiras_novas_chaves": chaves_novas, "flags_sha16": sha(V / "kernel" / "FLAGS_v412.json")[:16],
    "kernel": {"modulos_novos": len(bundle), "raiz_antes_sha16": sha(NOS / "tgl_kernel" / "TGLExt.lean")[:16], "audit_antes_sha16": sha(NOS / "tgl_kernel" / "TGL" / "Audit.lean")[:16],
               "raiz_depois_sha16": sha(SB / "TGLExt.lean")[:16], "audit_depois_sha16": sha(SB / "TGL" / "Audit.lean")[:16], "pronto_kernel_sha16": sha(V / "PRONTO_PARA_CANDIDATO_v412_R7.json")[:16]},
    "bundle_sha256": bundle, "bundle_nota": "sha256 da fonte NORMALIZADA (a que o candidato embute e o rito materializa no Nos); cada uma ligada a' fonte crua da lista R12 por BUNDLE_v412.json (sha256_insumo)",
    "bundle_recibo_sha16": sha(V / "BUNDLE_v412.json")[:16], "manifesto_r12_sha16": sha(V / "insumos" / "MANIFESTO_PEDRAS_v412_R12.json")[:16],
    "bundle_pedras_anteriores_sha256": E411["bundle_v410_sha256"],   # as duas ultimas pedras ja' seladas (v410: IALD2 e AEscala; a v411 nao teve modulo novo), que o instalador confere no Nos
    "registros_v412": pal, "registros_do_candidato": CM.get("registros"),
    "pilar": dict(E411["pilar"], portao_sha16=sha(V / "PORTAO_DO_PILAR_CANDIDATO_v412.json")[:16]),
    "troca_dita": {"regra": "um veredito herdado da v411 so' pode mudar nos numeros (a regra do ensaio a seco: os vizinhos so' mudam numeros): trocando os hashes hexadecimais e os numeros por marcadores neutros, fica identico ao da v411",
                   "escada": esc, "hashes": [CM["base_v411_sha16"], CM["sha16"]]},
}
out = V / "ESPERADOS_v412.json"
if out.exists():
    bak = out.with_name(out.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")); bak.write_bytes(out.read_bytes()); assert bak.read_bytes() == out.read_bytes()
b = json.dumps(esp, ensure_ascii=False, indent=1).encode("utf-8"); tmp = out.with_name(out.name + ".tmp_c1"); tmp.write_bytes(b); assert tmp.stat().st_size == len(b); tmp.replace(out)
print("ESPERADOS_v412.json | candidato", esp["candidato_sha16"], "| origem", esp["origem_sha16"], "| escada", esc, "| modulos novos", len(bundle), "| raiz", esp["kernel"]["raiz_antes_sha16"], "->", esp["kernel"]["raiz_depois_sha16"],
      "| audit", esp["kernel"]["audit_antes_sha16"], "->", esp["kernel"]["audit_depois_sha16"], "| sha16", hashlib.sha256(b).hexdigest()[:16])
