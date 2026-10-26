# -*- coding: utf-8 -*-
"""Perna 2 — a CENTRAL PRIVADA (C1, C3..C12, C14, C15): sondagem, cofre `um_unificado_vNNN` + `tgl_kernel_vNNN`, medição cofre × cofre,
snapshot do `Chatgpt\\`, runner da Fronteira (pedra genérica), módulo comum dos 16 dispositivos (camada genérica), os 16 dispositivos, os 16
FINAL, o ledger de pinos, commit/push com LISTA DE PERMISSÃO (nunca `git add -u` varrendo modificação alheia — L5) e a conferência final.

Generaliza (e substitui, para a v399 em diante) os scripts derivados à mão a cada versão (`sondar_`, `cofre_`, `medir_`, `snapshot_chatgpt_`,
`patch_runner_`, `patch_formula_`, `rodar_16_`, `conferencia_final_`): 63 trocas contadas + 1 regex na v397. O defeito L1 (o manifesto do
cofre lia o objeto-arquivo em vez de `["core"]` e saía com `registros_novos_vNNN = {}` e `pilar_quantico = null`) está CORRIGIDO aqui.

Nada aqui move o gate nem o kernel; recusa é resultado; falha de leitura é falha visível."""
import concurrent.futures as cf
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path

from . import fatos as F
from . import nos, patches, recibos, textos, util
from .generico import custodia_generica as CG
from .motor import Passo, aplicado, bloqueado, falta, superado, superado_rel, indeterminado
from .util import Parar, FalhaLeitura

FORA_RE = re.compile(r"^(dry_|imp_|sim_|base_|superado_|scratch$|kernel$|kb_stub|pilar_anterior|quarentena|tentativa|exame_preflight$|bancada_B3_ensaio_|delta_19out$|imp$|arvore_simulada|falso_nos$)")
EXCL_RAIZ = re.compile(r"^(CUSTODY_MANIFEST\.json|FATOS_CUSTODIA\.json|SEMANTICA_CUSTODIA\.json|NOTA_DE_CUSTODIA\.md|HANDOFF_v\d+_CUSTODIA\.md|HANDOFF_CUSTODIA_CONJUNTA.*|rodada_v\d+_stdout.*\.txt)$")
LIM = 5 * 1024 * 1024
LISTA_NEGRA = re.compile(r"\.bak_|\.tmp|/work/|^work/|EPCT/|\.env$|auth\.json|stack_v7|psion_state|terceiros|iald_privado|andamentos/|frontend/", re.I)
TRIO = set(nos.TRIO)


# =================================================================== utilidades
def _py(ctx):
    return str(ctx.c.PYTHON)


def _commit_central(ctx):
    """O commit `custodia(vN): …` da Central (aceita a custódia conjunta, `custodia(v392+v393+v394)`); erro de git é FalhaLeitura, nunca «sem commit»."""
    return util.commit_da_custodia(ctx.c.CEN, ctx.versao)


def _tracos_historicos(ctx):
    """Versão histórica (o Nós já selou outra): o commit custodia(vN): da Central. Existir não PROVA o que o passo fez: quem usa isto sem ler o artefato
    do commit marca SUPERADO_REL (dito), nunca APLICADO."""
    return None if ctx.corrente else _commit_central(ctx)


def _recibo(ctx, nome, dados):
    """O recibo do passo: no run_dir da execução (como antes) E DURÁVEL na pasta de trabalho da versão (recibos.gravar), de modo que a marca de «já aplicado»
    de um PROCESSO SEGUINTE o leia (achado dos céticos: C11 só enxergava o recibo do run_dir da própria execução). Devolve o recibo gravado."""
    d = ctx.run_dir or (ctx.c.RUNS / ("%s_avulso" % ctx.versao))
    d.mkdir(parents=True, exist_ok=True)
    (d / (nome + ".json")).write_text(json.dumps(dados, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return recibos.gravar(ctx, nome, dados)


def _recibo_lido(ctx, nome):
    return recibos.ler(ctx, nome)


# =================================================================== C1 — sondagem -> fatos_vNNN.json
def _ja_c1(ctx):
    p = ctx.trabalho_da_versao("fatos_%s.json" % ctx.versao)
    cv = ctx.c.cofre(ctx.versao)
    if (cv / "FATOS_CUSTODIA.json").is_file():
        return aplicado("FATOS_CUSTODIA.json já está no cofre")
    return aplicado("%s" % p) if p else falta("sem fatos_%s.json em work\\custodia_%s_*" % (ctx.versao, ctx.versao))


def _pre_c1(ctx):
    f = list(ctx.nos_marcas.faltam)
    return f


def _ap_c1(ctx):
    Fa = ctx.fatos
    bad = []
    if Fa["registros_sumidos"]:
        bad.append("registros sumidos: %s" % Fa["registros_sumidos"])
    if Fa["kernel"]["fora_do_trio"]:
        bad.append("declarações fora do trio: %d" % Fa["kernel"]["fora_do_trio"])
    if Fa["registro"]["pt"] != Fa["registro"]["en"]:
        bad.append("registro PT (%d) != EN (%d)" % (Fa["registro"]["pt"], Fa["registro"]["en"]))
    if Fa["registro"]["novos"] != Fa["registros_novos"]:
        bad.append("registro novos != blocos novos do core")
    esc = Fa["escada"]["esperadas"]
    bad += ["contrato %s com expected_ladder %s != %s" % (k, x, esc) for k, x in Fa["contratos_expected_ladder"].items() if x != esc]
    if Fa["kh"]["constantes"] != Fa["kernel"]["declaracoes"]:
        bad.append("kh_n1 constantes (%s) != declarações auditadas (%s)" % (Fa["kh"]["constantes"], Fa["kernel"]["declaracoes"]))
    if not Fa["handoff"].get("ok"):
        bad += Fa["handoff"].get("divergencias", ["handoff ausente"])
    if bad:
        raise Parar("os fatos medidos reprovam a custódia (gate de C1)", bad)
    ctx.W.mkdir(parents=True, exist_ok=True)
    p = ctx.W / ("fatos_%s.json" % ctx.versao)
    if p.is_file():
        antigo = json.loads(p.read_text(encoding="utf-8"))
        if antigo.get("pin") != Fa["pin"]:
            raise Parar("fatos_%s.json já existe com OUTRO pino: o selo foi refeito (errata ao lado, decisão da gerência)" % ctx.versao)
    else:
        util.escrever_json(p, Fa, backup=False)
    core = F.Artefatos(ctx.c, ctx.versao, "nos" if ctx.corrente else "cofre").core
    util.escrever_json(ctx.W / "textos_blocos_novos.json", F.textos_dos_blocos(core, Fa["registros_novos"]), backup=True)
    return {"fatos": p.name, "blocos": len(Fa["blocos"])}


# =================================================================== a semântica (rascunho mecânico, DECLARADO) — ESPEC_CENTRAL §4.3
def titulo_slug(ctx):
    t = util.ascii_sem_acento(ctx.bloco_diario.titulo_pt).upper() if ctx.bloco_diario else ctx.versao.upper()
    return re.sub(r"[^A-Z0-9]+", "_", t).strip("_")


def semantica_rascunho(ctx, Fa, core):
    blocos = {}
    for k in Fa["registros_novos"]:
        r = core.get(k)
        if not isinstance(r, dict):
            continue
        segs = [s for s in str(r.get("verdict") or "").split("__") if re.search(r"(^|_)(NOT|NO|NEVER)_", s) or s.endswith(("_UNMOVED", "_UNTOUCHED"))]
        regra = {"verdict_deve_conter": segs, "verdict_nao_deve_conter": [], "campos": []}
        if k.startswith("cunhagens_"):
            regra["campos"] = [{"caminho": "kernel.bandeiras", "par_igual": True}, {"caminho": "kernel.declaracoes_no_trio", "par_igual": True}]
        blocos[k] = regra
    return {"schema": "custodia_semantica/1", "versao": ctx.versao, "estatuto": "DECLARADO", "rascunho_por": "script custodia_g1 (sem modelo)", "revisor": None,
            "revisao": 0, "blocos": blocos, "mudados_permitidos": [], "titulo_slug": titulo_slug(ctx), "veredito_camada_sufixo": None,
            "docstring_item": None,
            "nao_se_afirma_extra": ["(%s, %s) %s" % (ctx.versao, k, x) for k in Fa["registros_novos"] for x in (core.get(k) or {}).get("nao_diz", [])],
            "fontes": {"titulo": "diário da linhagem (cabeçalho do bloco vNNN SELADA)", "nao_se_afirma_extra": "core[<bloco>].nao_diz, verbatim"}}


# =================================================================== C3 — o cofre
def _manifest_do_cofre(ctx):
    m = ctx.c.cofre(ctx.versao) / "CUSTODY_MANIFEST.json"
    return util.ler_json(m) if m.is_file() else None


def _ja_c3(ctx):
    c, v = ctx.c, ctx.versao
    m = _manifest_do_cofre(ctx)
    km = c.cofre_kernel(v) / "CUSTODY_MANIFEST.json"
    if not m or not km.is_file():
        return falta("cofre um_unificado_%s e/ou tgl_kernel_%s ausentes" % (v, v))
    pin = ctx.pin_completo
    if pin and m.get("um_py_pin") != pin:
        return indeterminado("o cofre existe com OUTRO pino (selo refeito?): %s" % str(m.get("um_py_pin"))[:16])
    # RE-HASH (achado dos céticos): o manifesto do cofre é AUTODECLARADO («0 divergentes» é o que ele diz de si). A marca confere os BYTES.
    rh = ctx.memo("rehash_cofre", lambda: rehash_cofre(ctx, m))
    if rh["divergentes"]:
        return bloqueado("o cofre %s DIVERGE do próprio manifesto/do manifesto de prova (%d divergência(s)): %s" % (v, len(rh["divergentes"]), "; ".join(rh["divergentes"][:4])))
    legado = "" if m.get("fatos_custodia") else " (cofre legado: sem FATOS_CUSTODIA.json — a pedra genérica não o lê)"
    return aplicado("re-hash: %d/%d artefatos e %d/%d arquivos formais do kernel conferem por sha256 (manifesto declara %s divergentes)%s" % (
        rh["artefatos"], rh["artefatos"], rh["kernel"], rh["kernel"], m.get("mismatches"), legado))


def rehash_cofre(ctx, m):
    """Refaz do zero os hashes que o manifesto do cofre AFIRMA: cada artefato, o um.py contra o pino e cada arquivo formal do kernel contra o manifesto de
    prova do cofre do kernel (e este contra o sha que o manifesto do kernel guarda). Devolve {artefatos, kernel, divergentes[]}."""
    c, v = ctx.c, ctx.versao
    V, KV = c.cofre(v), c.cofre_kernel(v)
    div = []
    n_art = 0
    for a in m.get("artifacts", []):
        n_art += 1
        nome, h = a.get("file"), a.get("sha256")
        if not nome or not h:
            div.append("artefato sem file/sha256 no manifesto: %r" % (a,))
            continue
        p = V / nome
        if not p.is_file() or util.sha256_arquivo(p) != h:
            div.append("artefato %s" % nome)
    if m.get("um_py_pin") and (not (V / "um.py").is_file() or util.sha256_arquivo(V / "um.py") != m["um_py_pin"]):
        div.append("um.py do cofre != um_py_pin")
    pmf = KV / "tgl_kernel_proof_manifest.json"
    pm = util.ler_json(pmf)
    n_k = 0
    for rel, h in pm["formal_files_sha256"].items():
        n_k += 1
        p = KV / rel
        if not p.is_file() or util.sha256_arquivo(p) != h:
            div.append("kernel %s" % rel)
    kmj = util.ler_json(KV / "CUSTODY_MANIFEST.json")
    if kmj.get("tgl_kernel_proof_manifest_sha256") and util.sha256_arquivo(pmf) != kmj["tgl_kernel_proof_manifest_sha256"]:
        div.append("manifesto de prova do cofre do kernel != o sha que o CUSTODY_MANIFEST do kernel guarda")
    return {"artefatos": n_art, "kernel": n_k, "divergentes": div}


def _pre_c3(ctx):
    c, v = ctx.c, ctx.versao
    f = []
    if c.cofre(v).exists() or c.cofre_kernel(v).exists():
        f.append("o cofre %s já existe — nada se sobrescreve (parcial: renomear para .PARCIAL_<ts>, nunca apagar)" % v)
    if not ctx.corrente or not ctx.nos_marcas.um_py_confere:
        f.append("o Nós não está em %s selada com o um.py igual ao pino" % v)
        return f
    ant = ctx.anterior_cofre
    if not c.cofre(ant).is_dir():
        f.append("cofre base %s ausente" % ant)
    if (ctx.ordem or textos.ordem_padrao(c)) is None:
        f.append("a ordem do operador (arquivo verbatim) não foi achada: passe --ordem")
    return f


def _ap_c3(ctx):
    c, v = ctx.c, ctx.versao
    Fa = ctx.fatos
    ant = Fa["anterior"]
    V, KV, VB, KB = c.cofre(v), c.cofre_kernel(v), c.cofre(ant), c.cofre_kernel(ant)
    ordem = ctx.ordem or textos.ordem_padrao(c)
    selo = ctx.selo_nos
    mundo = util.ler_json(c.NOS / "um_absoluto.json")
    core = mundo.get("core") or {}                      # L1: ["core"], não o objeto-arquivo
    pm = util.ler_json(c.NOS / "tgl_kernel_proof_manifest.json")
    mb = util.ler_json(VB / "CUSTODY_MANIFEST.json")
    pin = util.sha256_arquivo(c.NOS / "um.py")
    if pin != selo["sha256"]["um.py"] or selo.get("um_version") != v or pin != Fa["pin"]:
        raise Parar("pino/versão do Nós != fatos — PARAR")
    if selo["qg_closure_verdict"] != mb["gate"]:
        raise Parar("gate != cofre %s — PARAR (o gate não se move por custódia)" % ant)
    if selo.get("fail_closed_selftest") != "FAIL_CLOSED_SELFTEST_PASSED":
        raise Parar("autoteste não passou")
    if (nos.escada_do_stdout(c, v) or "") != Fa["escada"]["texto"]:
        raise Parar("a escada %s não está no stdout da rodada" % Fa["escada"]["texto"])
    if [n for n, ax in pm["axiom_report"].items() if set(ax or []) - TRIO]:
        raise Parar("declarações fora do trio")
    # 1) artefatos: a lista do cofre base (menos o que é por versão), mais o stdout/handoff de cada versão em (ant, v], mais o que o selo lista e o Nós tem
    fixos = sorted(p.name for p in VB.iterdir() if p.is_file() and not EXCL_RAIZ.match(p.name))
    extra = []
    for k in range(util.versao_num(ant) + 1, ctx.n + 1):
        for nome in ("rodada_v%d_stdout.txt" % k, "HANDOFF_v%d_CUSTODIA.md" % k):
            if (c.NOS / nome).is_file():
                extra.append(nome)
            elif k == ctx.n:
                raise Parar("falta no Nós: " + nome)
    do_selo = sorted(n for n in selo["sha256"] if n not in fixos and (c.NOS / n).is_file() and not EXCL_RAIZ.match(n))
    arts, vistos = [], set()
    for nome in fixos + do_selo + extra:
        if nome in vistos:
            continue
        vistos.add(nome)
        src = c.NOS / nome
        if not src.is_file():
            raise Parar("falta no Nós: " + nome)
        dst = V / nome
        util.mkdir(dst.parent)
        shutil.copyfile(src, dst)
        h1, h2 = util.sha256_arquivo(src), util.sha256_arquivo(dst)
        if h1 != h2:
            raise Parar("cópia diverge: " + nome)
        ss = selo["sha256"].get(nome)
        arts.append({"file": nome, "sha256": h1, "matches_seal": (h1 == ss) if ss else None, "estatuto": "SELADO" if ss else "DOCUMENTO (fora do hash do selo)"})
    mism = [a["file"] for a in arts if a["matches_seal"] is False]
    if mism:
        raise Parar("artefato difere do selo", mism)
    shutil.copyfile(VB / "NOTA_DE_CUSTODIA.md", V / "NOTA_DE_CUSTODIA.md")
    arts.append({"file": "NOTA_DE_CUSTODIA.md", "sha256": util.sha256_arquivo(V / "NOTA_DE_CUSTODIA.md"), "matches_seal": None, "estatuto": "DOCUMENTO (do cofre %s)" % ant})
    # 2) pilar quântico: worker e spec do cofre base == Nós
    for n in ("pilar_quantico_spec.json", "pilar_quantico_worker.py"):
        if util.sha256_arquivo(VB / "quantum_pillar" / n) != util.sha256_arquivo(c.NOS / "quantum_pillar" / n):
            raise Parar("pilar: %s difere do Nós" % n)
    n_qp = 0
    for p in (VB / "quantum_pillar").rglob("*"):
        if p.is_file():
            d = V / "quantum_pillar" / p.relative_to(VB / "quantum_pillar")
            util.mkdir(d.parent)
            shutil.copyfile(p, d)
            n_qp += 1
    reuse = (core.get("quantum_pillar_v384") or {}).get("reuse") or {}
    em = []
    n_emenda = "%s_incorporacao_manifesto.json" % v
    if (c.CS / n_emenda).is_file():
        (V / "emendas_e_manifestos").mkdir(parents=True, exist_ok=True)
        shutil.copyfile(c.CS / n_emenda, V / "emendas_e_manifestos" / n_emenda)
        em.append(n_emenda)
    # 3) a cadeia de selo filtrada
    cad = {"regra": "cópia de bytes dos arquivos de primeiro nível e das subpastas de registro; FORA: ensaios a seco, simulações, bases, tentativas, rascunhos, árvores "
                    "simuladas e o falso Nós de teste, cópias do kernel (o kernel vai inteiro em tgl_kernel_%s) e todo arquivo > 5 MB — ficam em work\\cadeia_de_selo, fora do git" % v,
           "pastas": {}}
    for d in (v, v + "_selo"):
        src = c.CS / d
        if not src.is_dir():
            cad["pastas"][d] = "AUSENTE em work\\cadeia_de_selo"
            continue
        ent, fora_sub, grandes = 0, {}, []
        for p in src.rglob("*"):
            if not p.is_file():
                continue
            rel = p.relative_to(src)
            top = rel.parts[0] if len(rel.parts) > 1 else None
            if top and FORA_RE.match(top):
                fs = fora_sub.setdefault(top, [0, 0]); fs[0] += 1; fs[1] += p.stat().st_size
                continue
            if any(x in ("raiz", "temp", "__pycache__", ".lake") for x in rel.parts[:-1]) or len(str(V / ("cadeia_de_selo_" + v) / d / rel)) > 250:
                fs = fora_sub.setdefault("copias_de_teste_e_caminhos_longos", [0, 0]); fs[0] += 1; fs[1] += p.stat().st_size
                continue
            if p.stat().st_size > LIM:
                grandes.append({"arquivo": str(rel), "bytes": p.stat().st_size, "sha256": util.sha256_arquivo(p)})
                continue
            dst = V / ("cadeia_de_selo_" + v) / d / rel
            util.mkdir(dst.parent)
            shutil.copyfile(p, dst)
            ent += 1
        cad["pastas"][d] = {"arquivos_no_cofre": ent, "subpastas_fora": {k: {"arquivos": x[0], "bytes": x[1]} for k, x in sorted(fora_sub.items())}, "arquivos_grandes_fora": grandes}
    # gate novo (ESPEC_CENTRAL C3): a cadeia de selo copiada fica dentro de ±50% da anterior (diretório de ensaio de nome novo não entra calado)
    ant_cad = VB / ("cadeia_de_selo_" + ant) / ("MANIFESTO_CADEIA_DE_SELO_%s.json" % ant)
    if ant_cad.is_file():
        a_ = util.ler_json(ant_cad)["pastas"].get(ant, {})
        if isinstance(a_, dict) and a_.get("arquivos_no_cofre") and isinstance(cad["pastas"].get(v), dict):
            r = cad["pastas"][v]["arquivos_no_cofre"] / a_["arquivos_no_cofre"]
            if not 0.5 <= r <= 1.5:
                raise Parar("a cadeia de selo copiada (%d arquivos) está fora de ±50%% da anterior (%d): diretório de ensaio novo entrando em silêncio?"
                            % (cad["pastas"][v]["arquivos_no_cofre"], a_["arquivos_no_cofre"]))
    (V / ("cadeia_de_selo_" + v)).mkdir(parents=True, exist_ok=True)
    util.escrever_json(V / ("cadeia_de_selo_" + v) / ("MANIFESTO_CADEIA_DE_SELO_%s.json" % v), cad, backup=False)
    # 4) o kernel
    kfiles = pm["formal_files_sha256"]
    for rel, hk in kfiles.items():
        src = c.NOS / "tgl_kernel" / rel
        if not (src.is_file() and util.sha256_arquivo(src) == hk):
            raise Parar("kernel: %s não confere com o manifesto de prova" % rel)
        d = KV / rel
        util.mkdir(d.parent)
        shutil.copyfile(src, d)
    for n in ("lakefile.toml", "lean-toolchain", "lake-manifest.json"):
        if (c.NOS / "tgl_kernel" / n).is_file() and n not in kfiles:
            shutil.copyfile(c.NOS / "tgl_kernel" / n, KV / n)
    shutil.copyfile(c.NOS / "tgl_kernel_proof_manifest.json", KV / "tgl_kernel_proof_manifest.json")
    h_pm = util.sha256_arquivo(KV / "tgl_kernel_proof_manifest.json")
    if h_pm != selo["sha256"]["tgl_kernel_proof_manifest.json"]:
        raise Parar("o manifesto de prova não confere com o selo")
    kb = util.ler_json(KB / "CUSTODY_MANIFEST.json")
    antes = {str(p.relative_to(KB)).replace("\\", "/") for p in KB.rglob("*.lean")}
    agora = {r for r in kfiles if r.endswith(".lean")}
    novos_lean = sorted(agora - antes)
    km = {"version": v, "data_custodia": datetime.now().strftime("%Y-%m-%d"), "formal_files": len(kfiles), "declaracoes_no_axiom_report": len(pm["axiom_report"]), "fora_do_trio": 0,
          "formal_source_hash": pm["formal_source_hash"], "kernel_e_derivado_do_um_py": True,
          "delta_%s_%s" % (ant, v): {"lean_novos": len(novos_lean), "lean_removidos": len(antes - agora), "formal_files_%s" % ant: kb.get("formal_files"), "declaracoes_%s" % ant: kb.get("declaracoes_no_axiom_report")},
          "modulos_novos_%s" % v: novos_lean, "tgl_kernel_proof_manifest_sha256": h_pm}
    util.escrever_json(KV / "CUSTODY_MANIFEST.json", km, backup=False)
    # 5) FATOS_CUSTODIA.json e a SEMANTICA (rascunho) dentro do cofre, com o pino no manifesto (D1)
    util.escrever_json(V / "FATOS_CUSTODIA.json", Fa, backup=False)
    sem = semantica_rascunho(ctx, Fa, core)
    util.escrever_json(V / "SEMANTICA_CUSTODIA.json", sem, backup=False)
    # 6) o manifesto do cofre
    ordem_raw = ordem.read_bytes()
    # 25/10/2026 (custódia conjunta v399+v400): os registros novos são os de toda versão K com anterior < K <= v (a v400 não trouxe registro;
    # os da v399, que a v400 corrige, entram aqui), nunca só o sufixo _vN
    _ka, _kv = int(ctx.anterior_cofre[1:]), int(v[1:])
    regs = {k: str((x or {}).get("verdict", ""))[:200] for k, x in core.items() if isinstance(x, dict)
            and (lambda mm: bool(mm) and _ka < int(mm.group(1)) <= _kv)(re.search(r"_v(\d{3,})$", k))}
    rodada = {"tipo": "COMPLETA", "escada": "%s (rodada_%s_stdout.txt)" % (Fa["escada"]["texto"], v)}
    rodada.update({k: x for k, x in (mb.get("rodada") or {}).items() if k.startswith("errata")})
    rodada["erratas_dos_registros_novos"] = {k: (core.get(k) or {}).get("erratas") for k in Fa["registros_novos"] if (core.get(k) or {}).get("erratas")}
    rodada["contratos_com_expected_ladder"] = {"escada": Fa["escada"]["esperadas"], "contratos": sorted(Fa["contratos_expected_ladder"])}
    mv = {"version": v, "custodia": [v], "ordem_do_operador": [ordem_raw.decode("utf-8")], "ordem_sha256": hashlib.sha256(ordem_raw).hexdigest(),
          "um_version_no_selo": v, "seal_timestamp": selo.get("timestamp"), "result_hash": selo.get("result_hash"), "um_py_pin": pin, "gate": selo["qg_closure_verdict"],
          "gate_identico_ao_da_%s" % ant: True, "selftest": selo["fail_closed_selftest"], "formal_source_hash": pm["formal_source_hash"], "rodada": rodada,
          "kernel": {"formal_files": len(kfiles), "declaracoes_no_axiom_report": len(pm["axiom_report"]), "fora_do_trio": 0, "lean_novos_desde_%s" % ant: len(novos_lean)},
          "kernel_e_derivado_do_um_py": True,
          "pilar_quantico": {"reaproveitado": reuse.get("reused"), "da_rodada": reuse.get("from_run_finished"), "leitura": reuse.get("reading"), "arquivos_no_cofre": n_qp},
          "registros_novos_%s" % v: regs,
          "backup_da_versao_anterior": "%s (a %s que estava no espelho; feito no passo zero da custódia do espelho)" % (
              next(iter(sorted(c.BK.glob("um_%s_*" % Fa["anterior"]))), "<ausente>"), Fa["anterior"]),
          "cadeia_de_selo": "work\\cadeia_de_selo %s e %s_selo filtradas em cadeia_de_selo_%s/ (ver MANIFESTO_CADEIA_DE_SELO_%s.json)" % (v, v, v, v),
          "handoff": "HANDOFF_%s_CUSTODIA.md fica no Nós e neste cofre privado" % v, "emendas_da_irma": em,
          "fatos_custodia": {"arquivo": "FATOS_CUSTODIA.json", "sha256": util.sha256_arquivo(V / "FATOS_CUSTODIA.json")},
          "semantica_custodia": {"arquivo": "SEMANTICA_CUSTODIA.json", "sha256": util.sha256_arquivo(V / "SEMANTICA_CUSTODIA.json"), "estatuto": "DECLARADO", "revisao": 0},
          "artifacts": arts, "mismatches": len(mism), "n_artifacts": len(arts)}
    util.escrever_json(V / "CUSTODY_MANIFEST.json", mv, backup=False)
    return {"artefatos": len(arts), "pilar": n_qp, "kernel": len(kfiles), "lean_novos": len(novos_lean), "manifesto": util.sha256_arquivo(V / "CUSTODY_MANIFEST.json", 16)}


def _conf_c3(ctx):
    m = _manifest_do_cofre(ctx)
    f = []
    if not m:
        return ["CUSTODY_MANIFEST.json ausente"]
    if m.get("mismatches") != 0:
        f.append("artefatos divergentes do selo: %s" % m.get("mismatches"))
    if not m.get("registros_novos_" + ctx.versao):
        f.append("registros_novos_%s saiu vazio (o defeito L1 voltou?)" % ctx.versao)
    if (m.get("pilar_quantico") or {}).get("reaproveitado") is None:
        ctx.aviso("pilar_quantico.reaproveitado nulo no manifesto novo")
    return f


# =================================================================== C4 — medição cofre × cofre (a pedra genérica, em modo leitura)
def _ja_c4(ctx):
    if ctx.trabalho_da_versao("medicao_%s_contra_%s.json" % (ctx.versao, ctx.anterior_cofre)):
        return aplicado("medição gravada")
    return aplicado("a pedra do runner já lê o cofre (C6)") if _runner_tem_pedra(ctx) else falta("medição ainda não feita")


def _ap_c4(ctx):
    r = CG.medir_custodia_generica(ctx.c.OC, ctx.versao, ctx.anterior_cofre)
    ctx.W.mkdir(parents=True, exist_ok=True)
    util.escrever_json(ctx.W / ("medicao_%s_contra_%s.json" % (ctx.versao, ctx.anterior_cofre)), r, backup=True)
    if not r.get("pass"):
        bad = [k for k, x in (r.get("checks") or {}).items() if not x["ok"]]
        raise Parar("a pedra reprova a medição ANTES do runner (pré-voo de C6)", bad + ([r["erro"]] if r.get("erro") else []))
    return {"pass": True, "checks": len(r["checks"])}


# =================================================================== C5 — snapshot incremental do Chatgpt\ (em segundo plano)
def _dia_do_selo(ctx):
    if ctx.corrente:
        return ctx.selo_nos.get("timestamp", "")[:10].replace("-", "")
    b = ctx.bloco_diario
    if b and b.data:
        d, m, a = b.data.split("/")
        return "%s%s%s" % (a, m, d)
    return ""


def _snapshots(ctx):
    return sorted(d for d in ctx.c.BKCEN.glob("Chatgpt_*") if d.is_dir()) if ctx.c.BKCEN.is_dir() else []


def _instante_do_selo(ctx):
    """O instante do selo da versão: o do selo do Nós (corrente) ou o `seal_timestamp` do manifesto do cofre; sem ele, o início do dia do diário."""
    if ctx.corrente:
        return util.instante(ctx.selo_nos.get("timestamp"))
    m = ctx.c.cofre(ctx.versao) / "CUSTODY_MANIFEST.json"
    if m.is_file():
        t = util.instante(util.ler_json(m).get("seal_timestamp"))
        if t is not None:
            return t
    b = ctx.bloco_diario
    return util.instante(b.data + " 00:00:00") if b and b.data else None


def _ja_c5(ctx):
    dia = _dia_do_selo(ctx)
    t_selo = _instante_do_selo(ctx)
    com_m = [d for d in _snapshots(ctx) if (d / "MANIFEST.json").is_file()]
    if com_m:
        sm = util.ler_json(com_m[-1] / "MANIFEST.json")
        t_snap = util.instante(sm.get("snapshot"))
        # o instante COMPLETO do snapshot (não só o dia): um snapshot das 00:10 não cobre um selo das 00:26 do mesmo dia
        posterior = (t_snap >= t_selo) if (t_snap is not None and t_selo is not None) else (str(sm.get("snapshot", ""))[:8] >= dia)
        if posterior and sm.get("conferido_contra_origem") is True:
            return aplicado("%s (%s copiados, %s idênticos à base)" % (com_m[-1].name, sm.get("n_copiados"), sm.get("n_identicos_a_base")))
    pid_f = ctx.c.RUNS / ("%s.snapshot.json" % ctx.versao)
    if pid_f.is_file():
        from .motor import Trava
        pid = int(util.ler_json(pid_f).get("pid") or 0)
        if pid and Trava._vivo(pid):
            return indeterminado("snapshot em curso (pid %d); espere o MANIFEST.json antes do registro (C13)" % pid)
    return falta("nenhum snapshot conferido posterior ao selo (%s)" % (util.fmt_instante(t_selo) if t_selo else "dia " + dia))


def snapshot_incremental(c, saida_log=None):
    """Port de snapshot_chatgpt_v397.py: a origem é só LIDA; a base é o ÚLTIMO snapshot com MANIFEST conferido (não mais um nome literal)."""
    SRC, ROOT = c.CEN / "Chatgpt", c.BKCEN
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    LIMITE, EXCL = 25 * 1024 * 1024, {".lake", "tex_environment"}
    t0 = time.time()
    lp = util.lp
    bases = sorted(d for d in ROOT.iterdir() if d.is_dir() and d.name.startswith("Chatgpt_") and (d / "MANIFEST.json").is_file())
    bases = [b for b in bases if util.ler_json(b / "MANIFEST.json").get("conferido_contra_origem") is True]
    if not bases:
        raise Parar("nenhuma base de snapshot conferida em %s" % ROOT)
    base = bases[-1]
    DST = ROOT / ("Chatgpt_%s_delta_de_%s" % (ts, base.name.split("_")[1] + "_" + base.name.split("_")[2]))
    if DST.exists():
        raise Parar("destino de snapshot existe: %s" % DST)
    bman = util.ler_json(base / "MANIFEST.json")["arquivos"]
    man = {"origem": str(SRC), "snapshot": ts, "tipo": "INCREMENTAL", "base": str(base), "versao_do_script": "G1 (custodia_g1, 24/10/2026; exclusoes iguais as de 15/09)",
           "regra": "custodia do Claude; a origem e EDITADA so pelo ChatGPT — aqui so se LE; arquivo identico a base NAO e copiado de novo", "arquivos": {}, "n_total": 0,
           "n_copiados": 0, "bytes_copiados": 0, "n_identicos_a_base": 0,
           "excluidos": {"lake": {"n": 0, "bytes": 0}, "tex_environment": {"n": 0, "bytes": 0}, "maiores_que_25MB": {"n": 0, "bytes": 0, "lista": []}}}
    inc = []
    for dp, dns, fns in os.walk(lp(SRC)):
        rel_dir = os.path.relpath(dp, str(lp(SRC)))
        keep = []
        for d in dns:
            if d in EXCL:
                n = b = 0
                for dp2, _, fns2 in os.walk(os.path.join(dp, d)):
                    for f2 in fns2:
                        try:
                            b += os.path.getsize(os.path.join(dp2, f2)); n += 1
                        except OSError:
                            pass
                k = "lake" if d == ".lake" else "tex_environment"
                man["excluidos"][k]["n"] += n; man["excluidos"][k]["bytes"] += b
            else:
                keep.append(d)
        dns[:] = keep
        for f in fns:
            full = os.path.join(dp, f)
            try:
                sz = os.path.getsize(full)
            except OSError:
                continue
            rel = f if rel_dir == "." else rel_dir.replace("\\", "/") + "/" + f
            if sz > LIMITE:
                e = man["excluidos"]["maiores_que_25MB"]
                e["n"] += 1; e["bytes"] += sz; e["lista"].append({"caminho": rel, "bytes": sz})
                continue
            inc.append((rel, sz))
    inc.sort()
    for i, (rel, sz) in enumerate(inc):
        src = SRC / rel
        try:
            h = util.sha256_arquivo(src)
        except (OSError, FalhaLeitura) as e:
            man["arquivos"][rel] = {"bytes": sz, "erro_de_leitura": repr(e)[:120]}
            continue
        b = bman.get(rel)
        man["n_total"] += 1
        if b and b.get("sha256") == h:
            man["arquivos"][rel] = {"bytes": sz, "sha256": h, "em": "base"}
            man["n_identicos_a_base"] += 1
            continue
        dst = lp(DST / rel)
        util.mkdir(Path(dst).parent)
        with open(lp(src), "rb") as f:
            data = f.read()
        with open(dst, "wb") as g:
            g.write(data)
        man["arquivos"][rel] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "em": "delta", "novo": b is None}
        man["n_copiados"] += 1
        man["bytes_copiados"] += len(data)
    div = [r for r, m in man["arquivos"].items() if m.get("em") == "delta" and util.sha256_arquivo(DST / r) != m["sha256"]]
    man["conferido_contra_origem"] = (len(div) == 0)
    man["ausentes_na_origem_vs_base"] = sorted(set(bman) - set(man["arquivos"]))
    man["segundos"] = round(time.time() - t0)
    DST.mkdir(parents=True, exist_ok=True)
    util.escrever_atomico(DST / "MANIFEST.json", json.dumps(man, ensure_ascii=False, indent=1).encode("utf-8"), backup=False)
    if div:
        raise Parar("snapshot com cópias divergentes da origem", div[:10])
    return DST.name


def _ap_c5(ctx):
    """Dispara o snapshot DESTACADO (≈35 min) e volta; o registro (C13) espera o MANIFEST.json conferido. Nada de segundo snapshot concorrente."""
    c = ctx.c
    c.RUNS.mkdir(parents=True, exist_ok=True)
    # 25/10/2026 (achado na v400): a marca dizia «em curso (pid N)» e mesmo assim um segundo snapshot era disparado. Agora: snapshot vivo = não dispara.
    _m = _ja_c5(ctx)
    if "em curso" in str(getattr(_m, "detalhe", "") or (_m[1] if isinstance(_m, tuple) and len(_m) > 1 else "")):
        return {"pid": None, "ja_em_curso": True, "detalhe": str(getattr(_m, "detalhe", _m))}
    log = (ctx.run_dir or c.RUNS) / ("snapshot_%s.txt" % ctx.versao)
    log.parent.mkdir(parents=True, exist_ok=True)
    cli = c.CEN / "tools" / "custodiar.py"
    flags = 0x00000008 | 0x00000200 if os.name == "nt" else 0         # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
    with open(log, "wb") as out:
        p = subprocess.Popen([_py(ctx), "-X", "utf8", str(cli), "_snapshot"], stdout=out, stderr=subprocess.STDOUT, creationflags=flags, cwd=str(c.CEN))
    (c.RUNS / ("%s.snapshot.json" % ctx.versao)).write_text(json.dumps({"pid": p.pid, "inicio": util.agora_iso(), "log": str(log)}), encoding="utf-8")
    return {"pid": p.pid, "log": str(log)}


def esperar_snapshot(ctx, max_s=3600):
    """Pré-condição de C13/C14: o snapshot posterior ao selo, conferido. Espera (poll leve, nunca além de `max_s`) enquanto ele está EM CURSO."""
    t0 = time.time()
    while time.time() - t0 < max_s:
        m = _ja_c5(ctx)
        if m.estado == "APLICADO":
            return True
        if m.estado == "FALTA":
            return False
        restante = max_s - (time.time() - t0)
        if restante <= 0:
            break
        time.sleep(min(30, restante))
    return False


# =================================================================== C6 — runner da Fronteira
RUNNER = lambda c: c.CEN / patches.ARQ_RUNNER
FORMULA = lambda c: c.CEN / patches.ARQ_FORMULA


def _runner_tem_pedra(ctx):
    return ("_medir_%s_custodia" % ctx.versao) in util.ler_texto(RUNNER(ctx.c), "replace")


def _ja_c6(ctx):
    if _runner_tem_pedra(ctx):
        return aplicado("o runner tem _medir_%s_custodia" % ctx.versao)
    return falta("o runner ainda não tem _medir_%s_custodia" % ctx.versao)


def _pre_c6(ctx):
    f = []
    rn = util.ler_texto(RUNNER(ctx.c), "replace")
    if "def _custodia_generica" not in rn:
        f.append("G1.0 não instalado no runner: rode work\\custodia_G1\\patches\\instalar_g1_0.py (depois que nenhuma outra custódia esteja remendando o runner)")
    if not (ctx.c.OC / ("tgl_kernel_" + ctx.versao)).is_dir():
        f.append("cofre do kernel %s ausente (C3)" % ctx.versao)
    if not (ctx.c.cofre(ctx.versao) / "FATOS_CUSTODIA.json").is_file():
        f.append("FATOS_CUSTODIA.json não está no cofre (a pedra genérica o exige)")
    return f


def _ap_c6(ctx):
    Fa = ctx.fatos
    sem = _semantica_do_cofre(ctx)
    suf = (sem or {}).get("veredito_camada_sufixo")
    slug = (sem or {}).get("titulo_slug") or titulo_slug(ctx)
    r = patches.aplicar_em_arquivo(RUNNER(ctx.c), lambda s: patches.runner_por_versao(s, ctx.versao, Fa["anterior"], Fa, slug, suf), "v%d" % (patches.runner_numeros(util.ler_eol(RUNNER(ctx.c))[0])[0] + 1))
    return r


def _semantica_do_cofre(ctx):
    cv = ctx.c.cofre(ctx.versao)
    revs = [p for p in cv.glob("SEMANTICA_CUSTODIA.rev*.json")]
    if revs:
        return util.ler_json(max(revs, key=lambda p: int(re.search(r"rev(\d+)", p.name).group(1))))
    p = cv / "SEMANTICA_CUSTODIA.json"
    return util.ler_json(p) if p.is_file() else None


# =================================================================== C7 — runner, duas execuções
def _resultados_do_runner(ctx):
    fs = sorted(glob.glob(str(ctx.c.CEN / "fronteira_tgl" / "results" / "fronteira_*.json")), key=os.path.getmtime)
    return fs


def _runs_com_veredito(ctx, v, maximo=60):
    achados = []
    for f in reversed(_resultados_do_runner(ctx)[-maximo:]):
        try:
            d = json.loads(Path(f).read_text(encoding="utf-8"))
        except ValueError:
            continue
        vd = str(d.get("verdict") or "")
        if vd.startswith("FRONTEIRA_SINCRONIZADA_%s" % v.upper()) and (d.get("the_station") or {}).get("custodia_%s" % v, {}).get("pass") is True:
            achados.append(f)
    return achados


def _ja_c7(ctx):
    h = _tracos_historicos(ctx)
    ach = _runs_com_veredito(ctx, ctx.versao)
    if len(ach) >= 2:
        return aplicado("%d execuções com FRONTEIRA_SINCRONIZADA_%s e custodia_%s.pass" % (len(ach), ctx.versao.upper(), ctx.versao))
    if h:
        return superado_rel("commit custodia(%s) da Central: %s — os resultados do runner da versão já não estão entre os 60 mais novos" % (ctx.versao, h[:8]))
    return falta("%d de 2 execuções aprovadas do runner" % len(ach))


def _ap_c7(ctx):
    c, v = ctx.c, ctx.versao
    antes = set(_resultados_do_runner(ctx))
    saidas = []
    for i in (1, 2):
        log = ctx.W / ("runner_%s_r%d.txt" % (v, i))
        ctx.W.mkdir(parents=True, exist_ok=True)
        r = util.rodar([_py(ctx), "-X", "utf8", "one_fronteira.py"], cwd=c.CEN / "fronteira_tgl" / "runner", timeout=3600, log=log)
        if r["rc"] != 0:
            raise Parar("o runner saiu com rc %s na execução %d" % (r["rc"], i), r["saida"].strip().splitlines()[-6:])
        saidas.append(r["segundos"])
    novos = [f for f in _resultados_do_runner(ctx) if f not in antes]
    if len(novos) < 2:
        raise Parar("o runner não gravou 2 resultados novos (gravou %d)" % len(novos))
    resultados = [json.loads(Path(f).read_text(encoding="utf-8")) for f in novos[-2:]]
    f = []
    for d in resultados:
        vd = str(d.get("verdict") or "")
        if not vd.startswith("FRONTEIRA_SINCRONIZADA_%s" % v.upper()):
            f.append("veredito do runner não começa por FRONTEIRA_SINCRONIZADA_%s: %s" % (v.upper(), vd[:80]))
        est = d.get("the_station") or {}
        if (est.get("custodia_%s" % v) or {}).get("pass") is not True:
            f.append("the_station.custodia_%s.pass != True" % v)
        reprovadas = [k for k, x in est.items() if isinstance(x, dict) and x.get("pass") is False]
        if reprovadas:
            f.append("pedras com pass False: %s" % reprovadas)
        ce = (est.get("custodia_%s" % v) or {}).get("ceticos") or {}
        if not (ce.get("1_reprovou") is True and ce.get("2_reprovou") is True):
            f.append("os dois céticos não reprovaram as injeções")
    pa = [{k: x.get("pass") for k, x in (d.get("the_station") or {}).items() if isinstance(x, dict)} for d in resultados]
    if pa[0] != pa[1]:
        f.append("as duas execuções discordam em algum pass")
    if f:
        raise Parar("o runner reprovou (gates de C7)", f)
    return _recibo(ctx, "C7", {"resultados": [Path(x).name for x in novos[-2:]], "segundos": saidas, "veredito": str(resultados[-1].get("verdict"))[:120]})


# =================================================================== C8 — módulo comum dos 16 dispositivos
def _camada_no_texto(s, v):
    """O texto do módulo comum dos 16 traz a camada de `v` (função artesanal da versão ou a tupla CAMADAS_GENERICAS)."""
    return ("def conferir_%s_no_cofre" % v) in s or bool(re.search(r'^CAMADAS_GENERICAS = \(.*"%s".*\)\r?$' % v, s, re.M))   # 25/10: o módulo é CRLF


def _ja_c8(ctx):
    s = util.ler_texto(FORMULA(ctx.c), "replace")
    v = ctx.versao
    if _camada_no_texto(s, v):
        return aplicado("o módulo tem a camada %s" % v)
    return falta("o módulo ainda não tem a camada %s" % v)


def _pre_c8(ctx):
    f = []
    s = util.ler_texto(FORMULA(ctx.c), "replace")
    if "CAMADAS_GENERICAS" not in s:
        f.append("G1.0 não instalado no módulo dos 16 dispositivos: rode work\\custodia_G1\\patches\\instalar_g1_0.py")
    if not (ctx.c.cofre(ctx.versao) / "FATOS_CUSTODIA.json").is_file():
        f.append("FATOS_CUSTODIA.json não está no cofre")
    return f


def _ap_c8(ctx):
    Fa = ctx.fatos
    core = F.Artefatos(ctx.c, ctx.versao, "cofre").core
    v = ctx.versao
    novos = Fa["registros_novos"]
    estatutos = []
    for k in novos:
        est = str((core.get(k) or {}).get("estatuto") or "")
        pri = re.split(r"(?<=[.;])\s", est, maxsplit=1)[0] if est else ""
        if pri:
            estatutos.append("%s: «%s»" % (k, pri[:300]))
    item = max(int(x) for x in re.findall(r"\(item (\d+)\)", util.ler_texto(FORMULA(ctx.c), "replace"))) + 1
    par = ("Camada %s (custódia %s na Central, %s, sessão %s; handoff %s da gerência c1) — GENÉRICA (camada_generica.py):\n %d. os registros novos da %s (%s), lidos e conferidos no cofre, "
           "sem interpretação, contra o FATOS_CUSTODIA.json do cofre %s: %s Nada disso muda número algum de dispositivo.\n"
           % (v, v, ctx.data, ctx.sessao, v, item, v, ", ".join(novos), v, " ".join(estatutos)))
    suf = "REGISTROS_%s_VERIFICADOS_SEM_GATE__%s__" % (v.upper(), "SEMANTICA_DECLARADA_SEM_REVISAO")
    nao = []
    for k in novos:
        nao += ["(%s, %s) %s" % (v, k, x) for x in (core.get(k) or {}).get("nao_diz", [])]
    mods = [textos._base(m) for m in Fa["kernel"]["modulos_novos"]]
    chave = ("camadas_%s" % v)
    rx = r"TGLExt\.(%s)|%s" % ("|".join(mods) or "NENHUM", "|".join(novos) or "NENHUM")
    r = patches.aplicar_em_arquivo(FORMULA(ctx.c), lambda s: patches.formula_por_versao(s, v, Fa["anterior"], par, suf, nao, chave, 'r"%s"' % rx), v)
    # o módulo tem de rodar: um elo quebrado levanta RuntimeError e o passo para antes de tocar nos 16
    run = util.rodar([_py(ctx), "-X", "utf8", str(FORMULA(ctx.c))], cwd=FORMULA(ctx.c).parent, timeout=600)
    if run["rc"] != 0:
        raise Parar("o módulo comum não roda depois do patch (fail-closed)", run["saida"].strip().splitlines()[-8:])
    return r


# =================================================================== C9 — os 16 dispositivos
def _patentes(c):
    return sorted(glob.glob(str(c.CEN / "patents" / "BR*")))


def _camada_no_resultado(pat, v, so_o_ultimo=True):
    rs = sorted(glob.glob(os.path.join(pat, "results", "*", "results.json")), key=os.path.getmtime)
    rs = rs[-1:] if so_o_ultimo else rs
    return any(('"camada_%s_no_cofre"' % v) in Path(r).read_text(encoding="utf-8", errors="replace") for r in rs)


def _ja_c9(ctx):
    pats = _patentes(ctx.c)
    n = sum(1 for p in pats if _camada_no_resultado(p, ctx.versao, so_o_ultimo=ctx.corrente))
    if pats and n == len(pats):
        return aplicado("%d/%d com a camada %s no resultado %s" % (n, len(pats), ctx.versao, "mais recente" if ctx.corrente else "(em algum resultado)"))
    h = _tracos_historicos(ctx)
    if h:
        return superado_rel("commit custodia(%s) da Central: %s — os resultados dos dispositivos já não trazem a camada da versão" % (ctx.versao, h[:8]))
    return falta("%d/%d dispositivos com a camada %s" % (n, len(pats), ctx.versao))


def rodar_16(ctx):
    base = ctx.c.CEN / "patents"
    runners = sorted(p for p in glob.glob(os.path.join(str(base), "*", "runner", "one_*.py")) if "_FINAL" not in p)
    if not runners or len(runners) != len(_patentes(ctx.c)):
        raise Parar("esperava um runner por patente (%d), achei %d" % (len(_patentes(ctx.c)), len(runners)))
    t0 = time.time()

    def roda(p):
        r = util.rodar([_py(ctx), p], cwd=os.path.dirname(p), timeout=3000)
        return p, r["rc"], r["saida"][-300:]
    res = []
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        for p, rc, out in ex.map(roda, runners):
            pat = os.path.dirname(os.path.dirname(p))
            cand = [f for f in glob.glob(os.path.join(pat, "results", "*", "results.json")) if os.path.getmtime(f) >= t0]
            tem = any(('"camada_%s_no_cofre"' % ctx.versao) in Path(f).read_text(encoding="utf-8", errors="replace") for f in cand)
            res.append({"runner": os.path.basename(p), "rc": rc, "camada": tem, "fim": out[-120:] if rc != 0 else ""})
    ok = sum(1 for r in res if r["rc"] == 0 and r["camada"])
    return _recibo(ctx, "C9", {"dispositivos": res, "ok": ok, "segundos": round(time.time() - t0)})


def _ap_c9(ctx):
    r = rodar_16(ctx)
    if r["ok"] != len(r["dispositivos"]):
        raise Parar("os dispositivos: %d/%d com rc 0 e a camada %s" % (r["ok"], len(r["dispositivos"]), ctx.versao), [x["runner"] for x in r["dispositivos"] if x["rc"] != 0 or not x["camada"]])
    return {"ok": r["ok"], "segundos": r["segundos"]}


# =================================================================== C10 — os 16 *_FINAL.py (build) · C11 (rodar) · C12 (ledger)
def _finais(c):
    return sorted(glob.glob(str(c.CEN / "patents" / "*" / "*_FINAL.py")))


def _problemas_dos_finais(itens, sha_modulo):
    """itens: [(nome, manifesto (dict), sha256 do *_FINAL.py de verdade)]. Cada FINAL tem de ser o que o seu manifesto diz e de embutir o módulo comum
    de `sha_modulo` (o manifesto lista o sha256 de cada arquivo embutido). Conteúdo, não data de arquivo."""
    ruins = []
    for nome, d, sha_final in itens:
        if d.get("final_sha256") != sha_final:
            ruins.append("%s: o FINAL não é o que o manifesto diz" % nome)
        emb = [f for f in d.get("files", []) if str(f.get("path", "")).endswith("_formula_completa/tgl_formula_completa.py")]
        if not emb or emb[0].get("sha256") != sha_modulo:
            ruins.append("%s: o módulo comum embutido não é o do módulo de referência" % nome)
    return ruins


def _finais_no_commit(ctx, h):
    """Os FINAL como estavam no commit `h` da Central (blobs): [(nome, manifesto, sha256 do FINAL)], sha256 do módulo comum e o texto dele. Levanta
    FalhaLeitura se o commit não traz os manifestos."""
    cen = ctx.c.CEN
    nomes = [x for x in util.git(cen, "ls-tree", "-r", "--name-only", h, "--", "patents").splitlines() if x.endswith("_FINAL.manifest.json")]
    if not nomes:
        raise FalhaLeitura("o commit %s da Central não traz *_FINAL.manifest.json" % h[:8])
    mod_b = util.git_bytes(cen, "cat-file", "blob", "%s:patents/_formula_completa/tgl_formula_completa.py" % h)
    itens = []
    for n in nomes:
        d = json.loads(util.git_bytes(cen, "cat-file", "blob", "%s:%s" % (h, n)).decode("utf-8"))
        itens.append((n.rsplit("/", 1)[-1], d, util.git_blob_sha256(cen, h, n[: -len(".manifest.json")] + ".py")))
    return itens, util.sha256_bytes(mod_b), mod_b.decode("utf-8", "replace")


def _ja_c10(ctx):
    """Os 16 FINAL regerados SOBRE o módulo comum com a camada da versão — conferido por CONTEÚDO (o sha256 do FINAL no manifesto e o do módulo embutido),
    não por data de arquivo. Versão histórica: os mesmos blobs no commit custodia(vN) da Central."""
    pats = _patentes(ctx.c)
    if ctx.corrente:
        mans = sorted(glob.glob(str(ctx.c.CEN / "patents" / "*" / "*_FINAL.manifest.json")))
        if not mans or len(mans) != len(pats):
            return falta("%d manifestos *_FINAL.manifest.json para %d dispositivos" % (len(mans), len(pats)))
        c8 = _ja_c8(ctx)
        if not c8.satisfeita:
            return falta("o módulo comum ainda não tem a camada %s (C8): os FINAL seriam regerados sobre o módulo antigo" % ctx.versao)
        itens = [(os.path.basename(m), util.ler_json(m), util.sha256_arquivo(m[: -len(".manifest.json")] + ".py")) for m in mans]
        ruins = _problemas_dos_finais(itens, util.sha256_arquivo(FORMULA(ctx.c)))
        if ruins:
            return falta("%d/%d FINAL desatualizados frente ao módulo comum de hoje (ex.: %s)" % (len(ruins), len(mans), ruins[0]))
        return aplicado("%d/%d FINAL: o sha256 de cada um é o do manifesto e todos embutem o módulo comum de hoje (com a camada %s)" % (len(mans), len(mans), ctx.versao))
    h = _tracos_historicos(ctx)
    if not h:
        return falta("sem o commit custodia(%s) da Central" % ctx.versao)
    try:
        itens, sha_mod, txt_mod = _finais_no_commit(ctx, h)
    except (FalhaLeitura, ValueError) as e:
        return superado_rel("commit custodia(%s) da Central: %s — os FINAL do commit não puderam ser lidos (%s)" % (ctx.versao, h[:8], str(getattr(e, "motivo", e))[:80]))
    ruins = _problemas_dos_finais(itens, sha_mod)
    if not _camada_no_texto(txt_mod, ctx.versao):
        ruins.append("o módulo comum do commit não tem a camada %s" % ctx.versao)
    if ruins:
        return bloqueado("os FINAL do commit %s da Central NÃO batem com o módulo comum do mesmo commit: %s" % (h[:8], "; ".join(ruins[:3])))
    return superado("commit %s da Central: os %d FINAL do commit têm o sha256 do manifesto e embutem o módulo comum do commit (com a camada %s)" % (h[:8], len(itens), ctx.versao))


def _ap_c10(ctx):
    r = util.rodar([_py(ctx), "-X", "utf8", "tools/build_final_code.py"], cwd=ctx.c.CEN, timeout=3600)
    n = len(re.findall(r" OK -> ", r["saida"]))
    if r["rc"] != 0 or n != len(_patentes(ctx.c)):
        raise Parar("build_final_code.py: rc %s, %d de %d ' OK -> '" % (r["rc"], n, len(_patentes(ctx.c))), r["saida"].strip().splitlines()[-6:])
    return {"ok": n}


def _ja_c11(ctx):
    """O rc 0 dos 16 FINAL só existe como PROVA se há o recibo DURÁVEL (`RECIBO_C11_vN.json` na pasta de trabalho da versão, gravado por _ap_c11 com o sha256 de
    cada FINAL que rodou). Na versão corrente o recibo vale enquanto os FINAL de hoje forem os que rodaram; sem recibo, G1 não tem como saber — INDETERMINADO,
    nunca «ok». Na histórica o recibo vale como registro (conferido com os blobs do commit, se houver); sem ele, só a relação: SUPERADO_REL."""
    rc = _recibo_lido(ctx, "C11")
    if rc and rc.get("total") and rc.get("ok") == rc.get("total"):
        gravados = {f["final"]: f.get("sha256") for f in rc.get("finais", [])}
        if ctx.corrente:
            hoje = {os.path.basename(p): util.sha256_arquivo(p) for p in _finais(ctx.c)}
            if hoje != gravados:
                mudaram = sorted(k for k in set(hoje) | set(gravados) if hoje.get(k) != gravados.get(k))
                return falta("os FINAL mudaram depois do recibo de C11 (%s): %d diferem, ex.: %s" % (rc.get("gravado_em", "?")[:19], len(mudaram), ", ".join(mudaram[:3])))
            return aplicado("rc 0 em %d/%d (recibo durável de %s; os %d FINAL de hoje têm os sha256 do recibo)" % (rc["ok"], rc["total"], rc.get("gravado_em", "?")[:19], len(hoje)))
        h = _tracos_historicos(ctx)
        if h:
            try:
                itens, _, _ = _finais_no_commit(ctx, h)
                no_commit = {n: sha for n, _, sha in itens}
                if all(no_commit.get(k) == v for k, v in gravados.items()):
                    return aplicado("rc 0 em %d/%d (recibo durável de %s; os sha256 do recibo são os dos FINAL do commit %s)" % (rc["ok"], rc["total"], rc.get("gravado_em", "?")[:19], h[:8]))
                return bloqueado("o recibo de C11 cita FINAL que NÃO são os do commit %s da Central" % h[:8])
            except (FalhaLeitura, ValueError):
                pass
        return aplicado("rc 0 em %d/%d (recibo durável de %s)" % (rc["ok"], rc["total"], rc.get("gravado_em", "?")[:19]))
    h = _tracos_historicos(ctx)
    if h:
        return superado_rel("commit custodia(%s) da Central: %s — sem recibo de G1 que prove o rc 0 dos 16 FINAL" % (ctx.versao, h[:8]))
    return indeterminado("sem recibo durável do rc dos 16 FINAL (G1 grava RECIBO_C11_%s.json na pasta de trabalho ao rodá-los; rode C11)" % ctx.versao)


def _ap_c11(ctx):
    finais = _finais(ctx.c)
    if not finais or len(finais) != len(_patentes(ctx.c)):
        raise Parar("esperava um *_FINAL.py por patente (%d), achei %d" % (len(_patentes(ctx.c)), len(finais)))
    mqc = [p for p in finais if os.path.basename(p) == "mqc_FINAL.py"]
    outros = [p for p in finais if p not in mqc]

    def roda(p):
        sha_antes = util.sha256_arquivo(p)
        r = util.rodar([_py(ctx), p], cwd=os.path.dirname(p), timeout=3000)
        ls = [l for l in r["saida"].splitlines() if l.strip()]
        return {"final": os.path.basename(p), "rc": r["rc"], "segundos": r["segundos"], "ultima": (ls[-1] if ls else "")[:150], "sha256": sha_antes}
    res = []
    with cf.ThreadPoolExecutor(max_workers=5) as ex:
        res += list(ex.map(roda, outros))
    res += [roda(p) for p in mqc]                           # o do MQC isolado, depois
    ok = sum(1 for r in res if r["rc"] == 0)
    _recibo(ctx, "C11", {"finais": res, "ok": ok, "total": len(res)})
    if ok != len(res):
        raise Parar("FINAL: rc 0 em %d/%d" % (ok, len(res)), [r["final"] for r in res if r["rc"] != 0])
    return {"ok": ok}


def _ja_c12(ctx):
    p = ctx.c.CEN / "fronteira_tgl" / "ledger_de_pinos.json"
    led = util.ler_json(p)
    if ctx.corrente and led.get("erros") == 0 and ctx.versao in json.dumps(led):
        return aplicado("ledger no kernel %s, %s erros, %s avisos" % (ctx.versao, led.get("erros"), led.get("avisos")))
    h = _tracos_historicos(ctx)
    if h:
        # a prova está no BLOB: o ledger como estava no commit custodia(vN) da Central (0 erros, no kernel da versão)
        try:
            led_h = json.loads(util.git_bytes(ctx.c.CEN, "cat-file", "blob", "%s:fronteira_tgl/ledger_de_pinos.json" % h).decode("utf-8"))
        except (FalhaLeitura, ValueError):
            return superado_rel("commit custodia(%s) da Central: %s — o ledger do commit não pôde ser lido" % (ctx.versao, h[:8]))
        if led_h.get("erros") == 0 and ctx.versao in json.dumps(led_h):
            return superado("o ledger do commit %s da Central: no kernel %s, %s erros, %s avisos" % (h[:8], ctx.versao, led_h.get("erros"), led_h.get("avisos")))
        return bloqueado("o ledger do commit %s da Central tem %s erros ou não cita %s" % (h[:8], led_h.get("erros"), ctx.versao))
    return falta("o ledger não está no kernel %s ou tem erros (%s)" % (ctx.versao, led.get("erros")))


def _ap_c12(ctx):
    r = util.rodar([_py(ctx), "-X", "utf8", "tools/ledger_de_pinos.py"], cwd=ctx.c.CEN, timeout=900)
    if r["rc"] != 0:
        raise Parar("ledger de pinos com erros (rc %s)" % r["rc"], r["saida"].strip().splitlines()[-6:])
    led = util.ler_json(ctx.c.CEN / "fronteira_tgl" / "ledger_de_pinos.json")
    return _recibo(ctx, "C12", {"erros": led.get("erros"), "avisos": led.get("avisos"), "linha": r["saida"].strip().splitlines()[-1][:140]})


# =================================================================== C14 — commit e push da Central com LISTA DE PERMISSÃO
def caminhos_a_commitar(ctx):
    """(a) os caminhos gerados, (b) o que o git já vê em patents/ filtrado por _FINAL/results/seals/_formula_completa, (c) o Atlas só se for só acréscimo."""
    c, v = ctx.c, ctx.versao
    cen = c.CEN
    ps = ["vault/originals_copy/um_unificado_" + v, "vault/originals_copy/tgl_kernel_" + v, "fronteira_tgl/runner/one_fronteira.py",
          "fronteira_tgl/runner/custodia_generica.py", "fronteira_tgl/LEDGER_DE_PINOS.md", "fronteira_tgl/ledger_de_pinos.json", "fronteira_tgl/render3d.json",
          "patents/_formula_completa/tgl_formula_completa.py", "patents/_formula_completa/camada_generica.py"]
    rec = _recibo_lido(ctx, "C7")
    nomes = (rec or {}).get("resultados") or [Path(f).name for f in _runs_com_veredito(ctx, v)[:2]]     # sem recibo desta execução: os 2 mais novos com o veredito da versão
    for nome in nomes:
        ps.append("fronteira_tgl/results/" + nome)
    mod = util.git(cen, "diff", "--name-only", "--", "patents").splitlines() + util.git(cen, "ls-files", "--others", "--exclude-standard", "--", "patents").splitlines()
    ps += [p for p in mod if re.search(r"(_FINAL\.py|_FINAL\.manifest\.json|/results/|/seals/|_formula_completa/)", p) and ".bak_" not in p]
    out = []
    for p in dict.fromkeys(ps):
        if (cen / p).exists():
            out.append(p)
    notas = []
    atlas = "memory/TGL_ATLAS.md"
    num = util.git(cen, "diff", "--numstat", "--", atlas).split()
    if num and num[1] == "0" and ("A CUSTÓDIA DA %s" % v) in util.ler_texto(cen / atlas, "replace"):
        out.append(atlas)
    elif num:
        notas.append("Atlas fora: o diff remove linhas (%s) ou não contém «A CUSTÓDIA DA %s»" % (num[1] if len(num) > 1 else "?", v))
    return out, notas


def _ja_c14(ctx):
    h = _commit_central(ctx)
    if not h:
        return falta("sem commit custodia(%s): na Central" % ctx.versao)
    if util.git_ancestral(ctx.c.CEN, h, "origin/main"):
        return aplicado("commit %s em origin/main (ref local)" % h[:8])
    return falta("commit %s ainda não está em origin/main" % h[:8])


def _pre_c14(ctx):
    f = []
    ps, notas = caminhos_a_commitar(ctx)
    if not ps:
        f.append("nada a commitar na lista de permissão")
    m5 = _ja_c5(ctx)
    if not m5.satisfeita:
        # no plano (leitura) não se espera: o snapshot em curso é dito; em `executar` espera até 5 s
        if ctx.leitura or m5.estado == "FALTA" or esperar_snapshot(ctx, 5) is False:
            f.append("o snapshot do Chatgpt\\ ainda não está conferido (C5): %s" % m5.detalhe[:120])
    return f


def _no_escopo(arquivo, lista):
    """O arquivo (caminho do git, com «/») está em algum item da lista de permissão (o próprio arquivo ou uma pasta que o contém)?"""
    return any(arquivo == p.rstrip("/") or arquivo.startswith(p.rstrip("/") + "/") for p in lista)


def _git_pathspec_nul(ps, pasta, nome):
    """Grava a lista de permissão num arquivo de pathspec separado por NUL (sem limite de linha de comando, sem aspas) e devolve o caminho."""
    f = Path(pasta) / nome
    util.escrever_atomico(f, b"\0".join(p.encode("utf-8") for p in ps) + b"\0", backup=False)
    return f


def commitar_so_a_lista(cen, ps, msg_arquivo, pasta_tmp):
    """`git add` da lista de permissão e commit **com pathspec explícito** (`git commit -F msg --pathspec-from-file=<lista>`): só entra no commit o que está na lista.
    O arquivo ALHEIO que outra sessão já pôs no índice (staged) fica no índice, intacto, FORA do commit — achado MEDIA do cético final (24/10/2026): `git commit` sem pathspec
    leva o índice inteiro e o empurrava com o commit `custodia(vN)`. Depois do commit, confere que nada fora da lista entrou (antes do push). Devolve
    {commit, alheios_preservados[], no_commit[]}; levanta Parar (lista negra no escopo, nada a commitar, commit falho ou arquivo de fora no commit)."""
    for p in ps:
        r = util.rodar(["git", "--literal-pathspecs", "-C", str(cen), "add", "--", p])
        if r["rc"] != 0:
            raise Parar("git add falhou: %s" % p, [r["saida"][-200:]])
    todos = util.git(cen, "diff", "--cached", "--name-only").splitlines()
    no_escopo = [x for x in todos if _no_escopo(x, ps)]
    alheios = [x for x in todos if not _no_escopo(x, ps)]
    ruins = [x for x in no_escopo if LISTA_NEGRA.search(x)]
    if ruins:
        raise Parar("arquivo da lista negra no escopo do commit da Central", ruins[:8])
    if not no_escopo:
        raise Parar("nada a commitar na lista de permissão (git diff --cached vazio no escopo)", ["alheios no índice (não entram): %s" % ", ".join(alheios[:5])] if alheios else [])
    pf = _git_pathspec_nul(ps, pasta_tmp, "pathspec_c14_%s.nul" % Path(msg_arquivo).stem.replace("commit_central_", ""))
    c = util.rodar(["git", "--literal-pathspecs", "-C", str(cen), "commit", "-q", "-F", str(msg_arquivo), "--pathspec-from-file=%s" % pf, "--pathspec-file-nul"])
    if c["rc"] != 0:
        raise Parar("git commit da Central falhou", [c["saida"][-300:]])
    no_commit = util.git(cen, "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD").splitlines()
    fora = [x for x in no_commit if not _no_escopo(x, ps)]
    if fora:
        raise Parar("o commit da Central levou arquivo FORA da lista de permissão (nada foi empurrado; o commit local fica para a gerência rever)", fora[:12])
    return {"commit": util.git(cen, "log", "-1", "--format=%h %s")[:100], "alheios_preservados": alheios, "no_commit": no_commit}


def _ap_c14(ctx):
    c, v = ctx.c, ctx.versao
    ps, notas = caminhos_a_commitar(ctx)
    Fa = ctx.fatos
    msg = commit_central(ctx, Fa)
    viol = textos.portao(msg, textos.conhecidos_da_rodada(ctx), rotulo="commit")
    if viol:
        raise Parar("o portão de texto reprovou a mensagem do commit da Central", viol)
    ctx.W.mkdir(parents=True, exist_ok=True)
    mp = ctx.W / ("commit_central_%s.txt" % v)
    util.escrever_atomico(mp, msg.encode("utf-8"), backup=True)
    cm = commitar_so_a_lista(c.CEN, ps, mp, ctx.W)
    p = util.rodar(["git", "-C", str(c.CEN), "push", "origin", "main"], timeout=900)
    if p["rc"] != 0:
        raise Parar("git push da Central falhou", [p["saida"][-300:]])
    return {"commit": cm["commit"], "fora_da_custodia": notas, "alheios_no_indice_preservados": cm["alheios_preservados"]}


def commit_central(ctx, Fa):
    v, ant = ctx.versao, Fa["anterior"]
    bd = ctx.bloco_diario
    tit = util.ascii_sem_acento(bd.titulo_pt).lower() if bd else v
    m = _manifest_do_cofre(ctx) or {}
    mods = ", ".join(textos._base(x) for x in Fa["kernel"]["modulos_novos"]) or "nenhum"
    runner_n = patches.runner_numeros(util.ler_eol(RUNNER(ctx.c))[0])[0]
    led = util.ler_json(ctx.c.CEN / "fronteira_tgl" / "ledger_de_pinos.json")
    nd = len(_patentes(ctx.c))
    corpo = ["custodia(%s): %s - cofre + kernel, runner v%d, %d dispositivos na camada %s, FINAL, ledger, Atlas" % (v, tit, runner_n, nd, v), "",
             "Cofre e kernel:", "- cofre um_unificado_%s: %s artefatos, %s divergentes do selo;" % (v, m.get("n_artifacts"), m.get("mismatches")),
             "- kernel tgl_kernel_%s: %d formais / %d declaracoes, 0 fora do trio (modulo novo %s)." % (v, Fa["kernel"]["formais"], Fa["kernel"]["declaracoes"], mods), "",
             "Runner, dispositivos e ledger:",
             "- runner da Fronteira v%d: a pedra generica le o cofre %s contra o %s pelo nome, com dois ceticos; aprovado duas vezes;" % (runner_n, v, ant),
             "- camada %s do modulo comum: %d/%d;" % (v, nd, nd), "- %d FINAL regerados e rodados, rc 0 em %d/%d;" % (nd, nd, nd),
             "- ledger de pinos: %s erros, %s avisos." % (led.get("erros"), led.get("avisos")), "",
             "Memorias: Atlas e memorias da sessao com o registro da custodia.", ""]          # a rota custodia.vN NAO e' citada: so entra no mapa em C16, depois do push e da conferencia final
    o = ctx.ordem or textos.ordem_padrao(ctx.c)
    if o and o.is_file():
        corpo.append("Ordem do operador (arquivo verbatim %s, sha16 %s)." % (o.name, util.sha16(o)))
    corpo += ["", "PROVADA = validade; a creditacao segue recusada; o gate nao se moveu."]
    if ctx.coautor:
        corpo += ["", "Co-Authored-By: %s" % ctx.coautor]
    return "\n".join(corpo) + "\n"


# =================================================================== C15 — conferência final independente
def _ja_c15(ctx):
    for d in reversed(ctx.c.pastas_trabalho_existentes(ctx.versao)):
        p = d / ("CONFERENCIA_FINAL_%s.json" % ctx.versao)
        if p.is_file():
            j = util.ler_json(p)
            if j.get("ok") == j.get("total") and j.get("total"):
                return aplicado("%s: %d/%d" % (p.name, j["ok"], j["total"]))
            return falta("%s: %s/%s (reprovada)" % (p.name, j.get("ok"), j.get("total")))
    return falta("sem CONFERENCIA_FINAL_%s.json" % ctx.versao)


def _ap_c15(ctx):
    ctx.W.mkdir(parents=True, exist_ok=True)
    saida = ctx.W / ("CONFERENCIA_FINAL_%s.json" % ctx.versao)
    cli = Path(__file__).resolve().parent / "conferencia.py"
    r = util.rodar([_py(ctx), "-X", "utf8", str(cli), ctx.versao, "--saida", str(saida)], timeout=900)
    if r["rc"] != 0:
        raise Parar("a conferência final reprovou", [l for l in r["saida"].splitlines() if l.startswith("FALHA")][:8])
    j = util.ler_json(saida)
    return {"ok": j["ok"], "total": j["total"]}


# =================================================================== a lista de passos
def passos_fase_a(ctx):
    return [
        Passo("C1", 2, "sondagem -> fatos_vNNN.json", _ja_c1, aplicar=_ap_c1, pre=_pre_c1, escreve="work\\custodia_vNNN_<data>\\fatos_vNNN.json, textos_blocos_novos.json"),
        Passo("C5", 2, "snapshot incremental do Chatgpt\\ (segundo plano)", _ja_c5, aplicar=_ap_c5, longo=True, escreve="Central de Patentes_BACKUPS\\Chatgpt_<ts>_delta_de_...\\"),
        Passo("C3", 2, "cofre um_unificado + tgl_kernel", _ja_c3, aplicar=_ap_c3, pre=_pre_c3, conferir=_conf_c3, longo=True,
              escreve="vault\\originals_copy\\um_unificado_vNNN\\, tgl_kernel_vNNN\\ (FATOS_CUSTODIA.json e SEMANTICA_CUSTODIA.json dentro do cofre)"),
        Passo("C4", 2, "medição cofre × cofre (pré-voo da pedra)", _ja_c4, aplicar=_ap_c4, escreve="work\\custodia_vNNN_<data>\\medicao_vNNN_contra_vANT.json"),
        Passo("C6", 2, "runner da Fronteira: repin + stub da pedra genérica", _ja_c6, aplicar=_ap_c6, pre=_pre_c6, escreve="fronteira_tgl\\runner\\one_fronteira.py (backup de bytes)"),
        Passo("C7", 2, "runner: duas execuções", _ja_c7, aplicar=_ap_c7, longo=True, escreve="fronteira_tgl\\results\\fronteira_<ts>.json x2"),
        Passo("C8", 2, "módulo dos 16 dispositivos: camada genérica", _ja_c8, aplicar=_ap_c8, pre=_pre_c8, escreve="patents\\_formula_completa\\tgl_formula_completa.py (backup de bytes)"),
        Passo("C9", 2, "os 16 dispositivos", _ja_c9, aplicar=_ap_c9, longo=True, escreve="patents\\BR*\\results\\<ts>\\ x16"),
        Passo("C10", 2, "os 16 *_FINAL.py (build)", _ja_c10, aplicar=_ap_c10, longo=True, escreve="patents\\*\\*_FINAL.py e manifesto x16 (+ .bak)"),
        Passo("C11", 2, "os 16 *_FINAL.py (rodar)", _ja_c11, aplicar=_ap_c11, longo=True, escreve="(recibo em runs\\)"),
        Passo("C12", 2, "ledger de pinos", _ja_c12, aplicar=_ap_c12, escreve="fronteira_tgl\\LEDGER_DE_PINOS.md e .json"),
    ]


def passos_fase_b(ctx):
    from . import memorias
    return [
        memorias.passo_c2(ctx), memorias.passo_c13(ctx), memorias.passo_c17a(ctx),
        Passo("C14", 2, "commit e push da Central (lista de permissão)", _ja_c14, aplicar=_ap_c14, pre=_pre_c14, externo=True, fase="B", rede=True,
              escreve=".git da Central + GitHub (origin/main)"),
        Passo("C15", 2, "conferência final independente", _ja_c15, aplicar=_ap_c15, fase="B", rede=True, escreve="work\\custodia_vNNN_<data>\\CONFERENCIA_FINAL_vNNN.json"),
        memorias.passo_c16(ctx), memorias.passo_c17b(ctx),
    ]
